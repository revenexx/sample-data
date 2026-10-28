/**
 * The progress events lib/load.sh and lib/remove.sh write when SEED_EVENTS is set
 * (one JSON line each), and the run state built from them.
 */
import type { StepPlan } from "./plan.ts";

export type SeedEvent =
  | { ev: "start"; action: "seed" | "remove"; tenant: string; dry: boolean; packs: string[]; base?: boolean }
  | { ev: "scope"; action: "seed" | "remove"; scope: string; steps: number }
  | { ev: "step_start" | "step_end"; i: number; name: string; kind: string }
  | { ev: "progress"; done: number; total: number }
  | { ev: "ratelimit"; wait: number }
  | { ev: "ok" | "warn" | "error"; text: string }
  | { ev: "done" };

export const parseEventLine = (line: string): SeedEvent | null => {
  const t = line.trim();
  if (!t.startsWith("{")) return null;
  try {
    const o = JSON.parse(t);
    return o && typeof o.ev === "string" ? (o as SeedEvent) : null;
  } catch {
    return null;
  }
};

export type LogEntry = {
  status: "run" | "ok" | "warn" | "err";
  scope: string;
  name: string;
  detail: string;
  done?: number;
  total?: number;
};

type ScopeState = { n: number; pos: number; frac: number };

export type RunState = {
  action: "seed" | "remove";
  dry: boolean;
  /** Scopes in the order the run will visit them ("base" and pack names). */
  scopes: string[];
  scope: string | null;
  scopeStates: Record<string, ScopeState>;
  stepIndex: number;
  stepCount: number;
  stepName: string;
  stepKind: string;
  log: LogEntry[];
  rateLimitWait: number | null;
  rateLimitAt: number | null;
  finished: boolean;
  failed: boolean;
  error: string | null;
  startedAt: number;
  endedAt: number | null;
};

export const newRun = (action: "seed" | "remove", dry: boolean, scopes: string[], now: number): RunState => ({
  action,
  dry,
  scopes,
  scope: null,
  scopeStates: {},
  stepIndex: 0,
  stepCount: 0,
  stepName: "",
  stepKind: "",
  log: [],
  rateLimitWait: null,
  rateLimitAt: null,
  finished: false,
  failed: false,
  error: null,
  startedAt: now,
  endedAt: null,
});

const LOG_CAP = 500;
const push = (log: LogEntry[], e: LogEntry): LogEntry[] => [...log, e].slice(-LOG_CAP);
const lastIdx = (log: LogEntry[], pred: (e: LogEntry) => boolean): number => {
  for (let i = log.length - 1; i >= 0; i--) if (pred(log[i])) return i;
  return -1;
};
const patchLast = (log: LogEntry[], idx: number, patch: Partial<LogEntry>): LogEntry[] =>
  log.map((e, i) => (i === idx ? { ...e, ...patch } : e));

/** "files   212 uploaded, 0 unchanged" -> "212 uploaded, 0 unchanged" (lib/load.sh pads the step name in). */
const stripName = (text: string, name: string): string =>
  (text.startsWith(name) ? text.slice(name.length) : text).trim();

export const applyEvent = (run: RunState, e: SeedEvent, now: number): RunState => {
  switch (e.ev) {
    case "scope": {
      const scopeStates = { ...run.scopeStates, [e.scope]: { n: e.steps, pos: 0, frac: 0 } };
      return { ...run, scope: e.scope, scopeStates, stepCount: e.steps };
    }
    case "step_start": {
      const sc = run.scope ? run.scopeStates[run.scope] : undefined;
      if (!run.scope || !sc) return run;
      const pos = run.action === "remove" ? sc.n - 1 - e.i : e.i;
      return {
        ...run,
        stepIndex: e.i,
        stepName: e.name,
        stepKind: e.kind,
        rateLimitWait: null,
        scopeStates: { ...run.scopeStates, [run.scope]: { ...sc, pos, frac: 0 } },
        log: push(run.log, { status: "run", scope: run.scope, name: e.name, detail: "" }),
      };
    }
    case "progress": {
      const sc = run.scope ? run.scopeStates[run.scope] : undefined;
      if (!run.scope || !sc) return run;
      const idx = lastIdx(run.log, (l) => l.status === "run");
      const frac = e.total > 0 ? Math.min(1, e.done / e.total) : 0;
      return {
        ...run,
        rateLimitWait: null,
        scopeStates: { ...run.scopeStates, [run.scope]: { ...sc, frac } },
        log: idx < 0 ? run.log : patchLast(run.log, idx, { done: e.done, total: e.total }),
      };
    }
    case "step_end": {
      const sc = run.scope ? run.scopeStates[run.scope] : undefined;
      const idx = lastIdx(run.log, (l) => l.status === "run");
      return {
        ...run,
        scopeStates:
          sc && run.scope ? { ...run.scopeStates, [run.scope]: { ...sc, pos: sc.pos + 1, frac: 0 } } : run.scopeStates,
        log: idx < 0 ? run.log : patchLast(run.log, idx, { status: "ok" }),
      };
    }
    case "ok": {
      const idx = lastIdx(run.log, (l) => l.status === "run");
      if (idx >= 0) {
        const cur = run.log[idx];
        // A second result line for the same step (remove_files) gets its own row.
        if (cur.detail !== "")
          return { ...run, log: push(run.log, { status: "ok", scope: cur.scope, name: "", detail: e.text }) };
        return {
          ...run,
          log: patchLast(run.log, idx, { detail: stripName(e.text, cur.name), done: undefined, total: undefined }),
        };
      }
      return { ...run, log: push(run.log, { status: "ok", scope: run.scope ?? "", name: "", detail: e.text }) };
    }
    case "ratelimit":
      return { ...run, rateLimitWait: e.wait, rateLimitAt: now };
    case "warn":
      // A rate-limit wait is shown once in the status bar (the "ratelimit" event), not as a log line per retry.
      if (/^rate limited/i.test(e.text)) return run;
      return { ...run, log: push(run.log, { status: "warn", scope: run.scope ?? "", name: "", detail: e.text }) };
    case "error": {
      const idx = lastIdx(run.log, (l) => l.status === "run");
      const log = idx >= 0 ? patchLast(run.log, idx, { status: "err" }) : run.log;
      return {
        ...run,
        failed: true,
        error: e.text,
        log: push(log, { status: "err", scope: run.scope ?? "", name: "", detail: e.text }),
      };
    }
    case "done":
      return { ...run, finished: true, endedAt: now };
    default:
      return run;
  }
};

/** A child that ended without a "done" event: the exit code decides. */
export const finishRun = (run: RunState, code: number | null, stderrTail: string, now: number): RunState => {
  if (run.finished || run.failed) return { ...run, finished: true, endedAt: run.endedAt ?? now };
  if (code === 0) return { ...run, finished: true, endedAt: now };
  const text = stderrTail || `exited with code ${code}`;
  return {
    ...run,
    finished: true,
    failed: true,
    error: text,
    endedAt: now,
    log: push(run.log, { status: "err", scope: run.scope ?? "", name: "", detail: text }),
  };
};

/** Weighted fraction (0..1) of one scope's steps that are behind us. */
export const scopeFraction = (steps: StepPlan[], st: ScopeState | undefined, action: "seed" | "remove"): number => {
  const w = (s: StepPlan) => (action === "remove" ? s.removeWeight : s.weight);
  const total = steps.reduce((n, s) => n + w(s), 0);
  if (!st || total <= 0) return st ? Math.min(1, st.n > 0 ? st.pos / st.n : 0) : 0;
  // Steps in execution order: manifest order, or last first when removing.
  const ordered = action === "remove" ? [...steps].reverse() : steps;
  let done = 0;
  for (let i = 0; i < Math.min(st.pos, ordered.length); i++) done += w(ordered[i]);
  if (st.pos < ordered.length) done += w(ordered[st.pos]) * st.frac;
  return Math.min(1, done / total);
};

/** Overall progress (0..1) of a run over its scopes, weighted by step cost. */
export const overallFraction = (run: RunState, plans: Record<string, StepPlan[]>): number => {
  if (run.finished && !run.failed) return 1;
  let sum = 0;
  let total = 0;
  const cur = run.scope ? run.scopes.indexOf(run.scope) : -1;
  run.scopes.forEach((scope, i) => {
    const steps = plans[scope] ?? [];
    const w = steps.reduce((n, s) => n + (run.action === "remove" ? s.removeWeight : s.weight), 0) || 1;
    total += w;
    if (cur >= 0 && i < cur) sum += w;
    else if (i === cur) sum += w * scopeFraction(steps, run.scopeStates[scope], run.action);
  });
  return total > 0 ? Math.min(1, sum / total) : 0;
};

/** Seconds left, or null while there is too little to go on. */
export const etaSeconds = (fraction: number, elapsedMs: number): number | null => {
  if (fraction < 0.02 || elapsedMs < 5000 || fraction >= 1) return null;
  return (elapsedMs * (1 - fraction)) / fraction / 1000;
};

export const formatEta = (sec: number): string => {
  if (sec < 60) return "<1 min left";
  if (sec < 3600) return `~${Math.round(sec / 60)} min left`;
  return `~${Math.floor(sec / 3600)} h ${Math.round((sec % 3600) / 60)} min left`;
};

export const formatDuration = (ms: number): string => {
  const s = Math.round(ms / 1000);
  if (s < 60) return `${s} s`;
  const m = Math.floor(s / 60);
  return m < 60 ? `${m} min ${s % 60} s` : `${Math.floor(m / 60)} h ${m % 60} min`;
};

/** Seconds of an announced rate-limit wait that are left. */
export const rateLimitLeft = (run: RunState, now: number): number | null =>
  run.rateLimitWait == null || run.rateLimitAt == null
    ? null
    : Math.max(0, Math.ceil(run.rateLimitWait - (now - run.rateLimitAt) / 1000));
