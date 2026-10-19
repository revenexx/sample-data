/** The seeder screen (design A1a): packs as rows, live counts with mini bars, log, status bar. */
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Box, Text, useApp, useInput, useStdout } from "ink";
import { join } from "node:path";
import { orderAlert, orderBlocker, orderConfirm, wrapText } from "./order.ts";
import { updateEnvFile } from "./dotenv.ts";
import { ApiError, ShopReader, readCounts, type Fetch } from "./api.ts";
import { baseState, cellBar, needsBase, formatCount, METRICS, METRIC_LABEL, OPTIONAL_METRICS, packState, ratio, totalOf, type Counts, type Metric, type PackState } from "./counts.ts";
import { hasCredentials, hostOf, isLocal, type Config } from "./config.ts";
import {
  applyEvent,
  etaSeconds,
  finishRun,
  formatDuration,
  formatEta,
  newRun,
  overallFraction,
  rateLimitLeft,
  type LogEntry,
  type RunState,
} from "./events.ts";
import type { Targets } from "./plan.ts";
import { busyText, readLock, type LockInfo } from "./lock.ts";
import { attachRun, scopesFor, startRun, type Handle, type RunCallbacks, type RunRequest } from "./runner.ts";
import { gradientColors, theme } from "./theme.ts";
import { Badge, Line, Panel, cells, fit, pad, padLeft, seg, width as segWidth, type Seg } from "./ui.tsx";

type Mode =
  | { kind: "normal" }
  | { kind: "tenant"; value: string }
  | { kind: "baseUrl"; value: string; tenant: string }
  | { kind: "typed"; value: string; req: RunRequest }
  | { kind: "yn"; req: RunRequest }
  | { kind: "quit" }
  | { kind: "stop" }
  | { kind: "saveEnv"; tenant: string; baseUrl: string };

export type AppProps = {
  config: Config;
  targets: Targets;
  root: string;
  fetchImpl?: Fetch;
  /** Fixed size for tests; otherwise the terminal's. */
  size?: { columns: number; rows: number };
  /** Polling intervals in ms: [idle, while running]. */
  poll?: [number, number];
};

const STATE_LABEL: Record<PackState, string> = {
  loaded: "loaded",
  partial: "partial",
  "not loaded": "not loaded",
  loading: "loading",
  removing: "removing",
  unknown: "…",
};
const stateColor = (s: PackState): Partial<Seg> =>
  s === "loaded" ? { color: theme.success }
  : s === "partial" || s === "loading" ? { color: theme.warn }
  : s === "removing" ? { color: theme.danger }
  : { dim: true };

const useSize = (fixed?: { columns: number; rows: number }) => {
  const { stdout } = useStdout();
  const read = () => fixed ?? { columns: stdout?.columns ?? 100, rows: stdout?.rows ?? 30 };
  const [size, setSize] = useState(read);
  useEffect(() => {
    if (fixed || !stdout) return;
    const on = () => setSize({ columns: stdout.columns ?? 100, rows: stdout.rows ?? 30 });
    stdout.on("resize", on);
    return () => void stdout.off("resize", on);
  }, [stdout, fixed]);
  return size;
};

const Header = ({ cfg, w }: { cfg: Config; w: number }) => {
  const local = isLocal(cfg.baseUrl);
  const word = [..."revenexx"];
  const colors = gradientColors(word.length);
  return (
    <Box width={w} justifyContent="space-between">
      <Text bold>
        {word.map((c, i) => (
          <Text key={i} color={colors[i]}>{c}</Text>
        ))}
        <Text color={theme.accent}> seed</Text>
      </Text>
      <Box gap={1}>
        {local ? <Badge bg={theme.success}>{" LOCAL "}</Badge> : <Badge bg={theme.warn}>{" ▲ PRODUCTION "}</Badge>}
        <Text dimColor>tenant</Text>
        <Text bold color={theme.accent}>{cfg.tenant || "(none)"}</Text>
        <Text dimColor>→</Text>
        <Text color={theme.accent}>{hostOf(cfg.baseUrl)}</Text>
        {cfg.source ? <Text dimColor>({cfg.source})</Text> : null}
      </Box>
    </Box>
  );
};

/**
 * Column layout of the table for a given inner width. The packs get one count column per metric,
 * the base its four columns over the same width (each at least `baseMin` wide), so the totals line
 * up; then one total bar with a percentage per row. A narrow window drops the optional metrics
 * first (the four of the first version stay), then the total column, then narrows the columns.
 */
export const tableLayout = (inner: number, baseCols = 4, baseMin = 17) => {
  const prefix = 1 + 3 + 2 + 11 + 11; // gap, [x], gap, pack, state
  const pctW = 6; // " 100 %"
  const col = 13;
  let metrics: Metric[] = [...METRICS];
  let totalBar = 12;
  const cellsW = () => Math.max(metrics.length * col, baseCols * baseMin);
  const totalW = () => (totalBar > 0 ? 2 + totalBar + pctW : 0);
  const fits = () => prefix + cellsW() + totalW() <= inner;
  for (const m of OPTIONAL_METRICS) if (!fits()) metrics = metrics.filter((x) => x !== m);
  while (!fits() && totalBar > 6) totalBar--;
  if (!fits()) totalBar = 0;
  // Spare width goes to the columns, so the total sits at the right edge.
  const cells = Math.max(baseCols * 9, inner - prefix - totalW() - 1);
  return {
    prefix,
    metrics,
    col: Math.floor(cells / metrics.length),
    baseCol: Math.floor(cells / baseCols),
    totalBar,
    pctW,
  };
};

const labelOf = (e: LogEntry) => (e.name ? `${e.scope} · ${e.name}` : "");

const logRow = (e: LogEntry, labelW: number): Seg[] => {
  const glyph =
    e.status === "ok" ? seg("✓ ", { color: theme.success })
    : e.status === "run" ? seg("● ", { color: theme.warn })
    : e.status === "warn" ? seg("! ", { color: theme.warn })
    : seg("✗ ", { color: theme.danger });
  const label = labelOf(e);
  const detail = e.status === "run" && e.total ? `${e.done ?? 0} / ${e.total}` : e.detail;
  return [
    seg(" "),
    glyph,
    seg(pad(label, labelW - 2) + "  "),
    e.status === "warn" ? seg(detail, { color: theme.warn }) : e.status === "err" ? seg(detail, { color: theme.danger }) : seg(detail, { bold: e.status === "run" }),
  ];
};

export const App = ({ config, targets, root, fetchImpl, size, poll = [8000, 6000] }: AppProps) => {
  const { exit } = useApp();
  const dims = useSize(size);
  const W = Math.max(80, dims.columns);
  const [cfg, setCfg] = useState<Config>(config);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [cursor, setCursor] = useState(0);
  const [mode, setModeState] = useState<Mode>(config.tenant ? { kind: "normal" } : { kind: "tenant", value: "" });
  // Keys can arrive faster than React renders (paste, key repeat): the ref is the truth.
  const modeRef = useRef<Mode>(mode);
  const setMode = (m: Mode) => {
    modeRef.current = m;
    setModeState(m);
  };
  const [fullLog, setFullLog] = useState(false);
  const [message, setMessage] = useState("");
  const [run, setRun] = useState<RunState | null>(null);
  const [now, setNow] = useState(Date.now());
  const [counts, setCounts] = useState<Record<string, Counts>>({});
  const [base, setBase] = useState<{ found: number; total: number; cols: number[] } | null>(null);
  const [readError, setReadError] = useState("");
  const [throttled, setThrottled] = useState(false);
  const [readAt, setReadAt] = useState<number | null>(null);
  const [kick, setKick] = useState(0);
  const refreshNow = useRef<() => void>(() => {});
  const handle = useRef<Handle | null>(null);
  const running = run !== null && !run.finished;

  const packs = targets.packs;
  const plans = useMemo(() => {
    const p: Record<string, typeof targets.base.steps> = { base: targets.base.steps };
    p.order = Array.from({ length: 7 }, (_, i) => ({ name: `step ${i + 1}`, kind: "upsert", total: 1, weight: 1, removeWeight: 0 }));
    for (const k of packs) p[k.name] = k.steps;
    return p;
  }, [targets, packs]);

  // ---- live counts ------------------------------------------------------------
  const reader = useMemo(() => new ShopReader(cfg, fetchImpl), [cfg, fetchImpl]);
  const runScopes = useRef<string[]>([]);
  runScopes.current = running ? run!.scopes : [];
  useEffect(() => {
    setCounts({});
    setBase(null);
    setReadAt(null);
  }, [reader]);
  useEffect(() => {
    if (!cfg.tenant) return;
    if (!hasCredentials(cfg)) {
      setReadError("no credentials: set REVENEXX_API_KEY or REVENEXX_TOKEN");
      return;
    }
    let dead = false;
    let slow = 1;
    let timer: ReturnType<typeof setTimeout>;
    let busy = false;
    let again = false;
    const tick = async () => {
      if (busy) {
        again = true;
        return;
      }
      busy = true;
      clearTimeout(timer);
      try {
        const active = runScopes.current;
        const which = active.length ? packs.filter((p) => active.includes(p.name)) : packs;
        const [c, b] = await Promise.all([readCounts(reader, which), reader.base(targets.base)]);
        if (dead) return;
        setCounts((prev) => ({ ...prev, ...c }));
        setBase(b);
        setReadError("");
        setReadAt(Date.now());
        if (!dead) slow = 1;
      } catch (e: any) {
        if (!dead) {
          if (e instanceof ApiError && e.status === 429) slow = Math.min(slow * 2, 8);
          else setReadError(String(e?.message ?? e));
        }
      }
      busy = false;
      if (!dead) {
        if (reader.rateLimitedAt !== null && Date.now() - reader.rateLimitedAt < 60000) slow = Math.max(slow, 2);
        setThrottled(slow > 1);
        if (again && slow === 1) {
          again = false;
          void tick();
        } else {
          again = false;
          timer = setTimeout(tick, (runScopes.current.length ? poll[1] : poll[0]) * slow);
        }
      }
    };
    refreshNow.current = () => void tick();
    void tick();
    return () => {
      dead = true;
      clearTimeout(timer);
      refreshNow.current = () => {};
    };
  }, [reader, kick, cfg, packs, targets.base, poll]);

  useEffect(() => {
    if (!running) return;
    const t = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(t);
  }, [running]);

  // ---- runs -------------------------------------------------------------------
  // A run lives in its own process and writes events to a file; this window only follows that file.
  const follower = useCallback(
    (dry: boolean): RunCallbacks => ({
      events: (es) => {
        setRun((r) => (r ? es.reduce((st, e) => applyEvent(st, e, Date.now()), r) : r));
        // A finished step can change what the shop holds: read the counts again right away, so the
        // table follows a load or remove live (a read in progress is not cut short). Dry runs change nothing.
        if (!dry && es.some((e) => e.ev === "step_end")) refreshNow.current();
      },
      exit: (code, tail) => {
        handle.current = null;
        setRun((r) => (r ? finishRun(r, code, tail, Date.now()) : r));
        setKick((k) => k + 1);
      },
    }),
    [],
  );

  const begin = useCallback(
    (req: RunRequest) => {
      setMessage("");
      const fresh = newRun(req.action === "remove" ? "remove" : "seed", req.dry, scopesFor(req), Date.now());
      if (req.action === "seed" && !req.base) fresh.log = [{ status: "ok", scope: "base", name: "", detail: "base already loaded, skipped" }];
      setRun(fresh);
      handle.current = startRun(root, cfg, req, follower(req.dry));
    },
    [root, cfg, follower],
  );

  // A run that is going but was not started by this window (an earlier window, or ./sample-data --load): follow it.
  const attach = useCallback(
    (info: LockInfo) => {
      setMessage("");
      setRun(newRun(info.action === "remove" ? "remove" : "seed", info.dry, info.scopes, info.started * 1000));
      handle.current = attachRun(root, info, follower(info.dry));
    },
    [root, follower],
  );
  useEffect(() => {
    if (running) return;
    const look = () => {
      if (handle.current) return;
      const st = readLock(root);
      if (st.kind === "live") attach(st.info);
    };
    look();
    const t = setInterval(look, 2000);
    return () => clearInterval(t);
  }, [running, root, attach]);
  useEffect(() => () => handle.current?.close(), []);

  /** The refusal line when a run is going, else null. */
  const busy = (): string | null => {
    if (running) return "a run is going (x stops it); only one run at a time";
    const st = readLock(root);
    return st.kind === "live" ? busyText(st.info) : null;
  };

  const ask = (req: RunRequest) => {
    if (req.dry) return begin(req);
    if (req.action === "order") return setMode(orderConfirm(isLocal(cfg.baseUrl)) === "yn" ? { kind: "yn", req } : { kind: "typed", value: "", req });
    if (!isLocal(cfg.baseUrl)) return setMode({ kind: "typed", value: "", req });
    if (req.action === "remove") return setMode({ kind: "yn", req });
    begin(req);
  };

  const request = (action: "seed" | "remove", dry: boolean, everything = false) => {
    if (!cfg.tenant) return setMessage("set a tenant first (t)");
    const refused = busy();
    if (refused) return setMessage(refused);
    const names = everything ? packs.map((p) => p.name) : packs.map((p) => p.name).filter((n) => selected.has(n));
    const picked = everything || selected.has("base");
    if (names.length === 0 && !picked) return setMessage("select a row first (space)");
    // A load runs the base only when it is picked or missing; a removal only when it is picked.
    ask({ action, packs: names, base: action === "seed" ? needsBase(picked, base) : picked, dry });
  };

  const industrial = packs.find((p) => p.name === "industrial");
  const orderBlock = orderBlocker(industrial, counts.industrial ?? null, base);
  const placeOrder = () => {
    if (!cfg.tenant) return setMessage("set a tenant first (t)");
    const refused = busy();
    if (refused) return setMessage(refused);
    if (orderBlock) return setMessage(`test order: ${orderBlock}`);
    ask({ action: "order", packs: [], base: false, dry: false });
  };

  const describe = (req: RunRequest) =>
    req.action === "order" ? "test order" : `${req.action} ${[...req.packs, ...(req.base ? ["base"] : [])].join(" + ")}`;

  // ---- keys -------------------------------------------------------------------
  useInput((input, key) => {
    if (key.ctrl && input === "c") {
      handle.current?.close();
      return exit();
    }
    if (modeRef.current.kind !== "normal") return handlePrompt(input, key);
    if (key.upArrow || input === "k") return setCursor((c) => (c + packs.length) % (packs.length + 1));
    if (key.downArrow || input === "j") return setCursor((c) => (c + 1) % (packs.length + 1));
    if (input === " ") {
      const name = cursor === 0 ? "base" : packs[cursor - 1].name;
      return setSelected((s) => {
        const n = new Set(s);
        n.has(name) ? n.delete(name) : n.add(name);
        return n;
      });
    }
    if (input === "a") return setSelected(new Set(["base", ...packs.map((p) => p.name)]));
    if (input === "s") return request("seed", false);
    if (input === "d") return request("seed", true);
    if (input === "r") return request("remove", false);
    if (input === "R") return request("remove", false, true);
    if (input === "o") return placeOrder();
    if (input === "l") return setFullLog((v) => !v);
    if (input === "t") return setMode({ kind: "tenant", value: cfg.tenant });
    if (input === "x") return running ? setMode({ kind: "stop" }) : undefined;
    if (input === "q") {
      if (!running) return exit();
      return setMode({ kind: "quit" });
    }
  });

  const handlePrompt = (input: string, key: { return?: boolean; escape?: boolean; backspace?: boolean; delete?: boolean }) => {
    const mode = modeRef.current;
    if (mode.kind === "normal") return;
    if (key.escape) return setMode({ kind: "normal" });
    if (mode.kind === "saveEnv") {
      if (input === "y" || input === "Y") {
        try {
          updateEnvFile(join(root, ".env"), { REVENEXX_TENANT: mode.tenant, REVENEXX_BASE_URL: mode.baseUrl });
          setMessage("saved to .env");
        } catch (e: any) {
          setMessage(`could not write .env: ${e?.message ?? e}`);
        }
        setMode({ kind: "normal" });
      } else if (input !== "") setMode({ kind: "normal" });
      return;
    }
    if (mode.kind === "quit" || mode.kind === "stop") {
      if (input === "y" || input === "Y") {
        setMode({ kind: "normal" });
        if (mode.kind === "quit") {
          handle.current?.close();
          return exit();
        }
        handle.current?.stop();
        setMessage("stopping the run…");
      } else if (input !== "") setMode({ kind: "normal" });
      return;
    }
    if (mode.kind === "yn") {
      if (input === "y" || input === "Y") {
        const req = mode.req;
        setMode({ kind: "normal" });
        begin(req);
      } else if (input !== "") setMode({ kind: "normal" });
      return;
    }
    if (key.return) {
      if (mode.kind === "tenant") {
        const tenant = mode.value.trim();
        if (!tenant) return;
        return setMode({ kind: "baseUrl", value: cfg.baseUrl, tenant });
      }
      if (mode.kind === "baseUrl") {
        const url = mode.value.trim().replace(/\/+$/, "");
        if (!/^https?:\/\/[^/\s]+/.test(url)) return setMessage("the API address must start with http:// or https://");
        setCfg({ ...cfg, tenant: mode.tenant, baseUrl: url, source: "changed here" });
        setMessage("");
        return setMode({ kind: "saveEnv", tenant: mode.tenant, baseUrl: url });
      }
      if (mode.kind === "typed") {
        if (mode.value !== cfg.tenant) return setMessage(`type ${cfg.tenant} exactly to confirm`);
        const req = mode.req;
        setMode({ kind: "normal" });
        setMessage("");
        return begin(req);
      }
      return;
    }
    if (key.backspace || key.delete) return setMode({ ...mode, value: [...mode.value].slice(0, -1).join("") } as Mode);
    if (input && !/[\x00-\x1f]/.test(input)) setMode({ ...mode, value: mode.value + input } as Mode);
  };

  // ---- table rows ----------------------------------------------------------------
  const inner = W - 2;
  const lay = tableLayout(inner, targets.base.checks.length, Math.max(...targets.base.checks.map((c) => c.label.length)) + 1);
  const runningScope = (name: string): "seed" | "remove" | undefined => (running && run!.scopes.includes(name) ? run!.action : undefined);

  const tableRows: Seg[][] = [];
  // One line per row: the coloured counts, then one ▰▱ bar with a percentage for the row as a whole.
  // The cursor row gets a muted tint across the whole line.
  type Cell = { text: string; ratio: number; dim: boolean };
  const tone = (c: Cell) => (c.dim ? undefined : c.ratio >= 1 ? theme.success : c.ratio > 0 ? theme.warn : theme.danger);
  const rowLine = (name: string, st: PackState, cells: Cell[], colW: number, total: Cell, at: number): Seg[] => {
    const isCursor = at === cursor && mode.kind === "normal";
    const on = selected.has(name);
    const bg = isCursor ? theme.selection : undefined;
    const b = isCursor ? { bold: true, bg } : {};
    const line: Seg[] = [
      seg(isCursor ? "▸" : " ", isCursor ? { bold: true, color: theme.accent, bg } : {}),
      seg(on ? "[x]" : "[ ]", { ...b, ...(on ? { color: theme.success } : {}) }),
      seg("  ", b),
      seg(pad(name, 11), b),
      seg(pad(STATE_LABEL[st], 11), { ...stateColor(st), ...b }),
    ];
    // complete green, partly there yellow, nothing there red; not counted yet stays dim
    for (const c of cells) {
      const t = tone(c);
      line.push(seg(pad(c.text, colW), { ...(c.dim && !isCursor ? { dim: true } : {}), ...(t ? { color: t } : {}), ...b }));
    }
    if (lay.totalBar > 0) {
      const t = tone(total);
      const cb = cellBar(total.ratio, lay.totalBar);
      line.push(seg("  ", b), seg(cb.filled, { color: t ?? theme.accent, ...b }), seg(cb.empty, { dim: true, ...b }));
      line.push(seg(padLeft(total.dim ? "" : `${Math.floor(total.ratio * 100)} %`, lay.pctW), { ...(t ? { color: t } : {}), ...b }));
    }
    if (bg) line.push(seg(" ".repeat(200), { bg }));
    return line;
  };
  const header = (first: string, cols: string[], colW: number): Seg[] => [
    seg(" ".repeat(6) + pad(first, 11) + pad("state", 11), { dim: true }),
    ...cols.map((m) => seg(pad(m, colW), { dim: true })),
    ...(lay.totalBar > 0 ? [seg(pad("  total", lay.totalBar + 2 + lay.pctW), { dim: true })] : []),
  ];
  const baseColW = lay.baseCol;
  const baseCols = targets.base.checks.map((c) => c.label);
  const bst = base ? baseState(base.found, base.total, runningScope("base")) : runningScope("base") ? "loading" : "unknown";
  tableRows.push(header("base", baseCols, baseColW));
  tableRows.push(
    rowLine(
      "base",
      bst,
      targets.base.checks.map((c, i) => {
        const have = base ? base.cols[i] : null;
        return { text: formatCount(have, c.target), ratio: have === null ? 0 : ratio(have, c.target), dim: have === null };
      }),
      baseColW,
      { text: "", ratio: base ? ratio(base.found, base.total) : 0, dim: !base },
      0,
    ),
  );
  tableRows.push([]);
  tableRows.push(header("pack", lay.metrics.map((m) => METRIC_LABEL[m]), lay.col));
  packs.forEach((p, i) => {
    const c = counts[p.name] ?? null;
    const sum = c ? totalOf(c, p) : null;
    tableRows.push(
      rowLine(
        p.name,
        packState(c, p, runningScope(p.name)),
        lay.metrics.map((m) => {
          const have = c ? c[m] : null;
          return { text: formatCount(have, p[m]), ratio: c ? ratio(c[m], p[m]) : 0, dim: have === null };
        }),
        lay.col,
        { text: "", ratio: sum ? ratio(sum.have, sum.target) : 0, dim: !sum },
        i + 1,
      ),
    );
  });

  // ---- log ---------------------------------------------------------------------------
  const logLines = fullLog ? Math.max(3, dims.rows - 6) : Math.max(2, Math.min(6, dims.rows - 16));
  const entries = run?.log ?? [];
  const shown = entries.slice(-logLines);
  const labelW = Math.min(40, Math.max(...shown.map((e) => labelOf(e).length), 20)) + 2;
  const logRows: Seg[][] = shown.map((e) => logRow(e, labelW));
  while (logRows.length < logLines) logRows.push([seg(logRows.length === 0 && !run ? " nothing run yet · s seed, d dry run" : "", { dim: true })]);

  // ---- status bar --------------------------------------------------------------------
  const status = (): { segs: Seg[]; bg: string } => {
    const bg = theme.selection;
    if (run && !run.finished) {
      const frac = overallFraction(run, plans);
      const eta = etaSeconds(frac, now - run.startedAt);
      const verb = run.scopes[0] === "order" ? "TEST ORDER" : run.dry ? "DRY RUN" : run.action === "seed" ? "SEEDING" : "REMOVING";
      const left = ` ${verb} ${run.scope ?? "…"}  step ${run.action === "remove" ? run.stepCount - run.stepIndex : run.stepIndex + 1}/${run.stepCount || "…"} ${run.stepName} `;
      const wait = rateLimitLeft(run, now);
      const pct = ` ${Math.round(frac * 100)} %`;
      const note = wait !== null && wait > 0 ? `rate limit, ${wait} s` : throttled ? "rate limited, counting slower" : eta !== null ? formatEta(eta) : "estimating…";
      const right = `  ${note} `;
      const barW = Math.max(6, Math.min(30, W - cells(left) - cells(pct) - cells(right) - 1));
      const cb = cellBar(frac, barW);
      const leftW = Math.max(0, W - barW - cells(pct) - cells(right));
      return {
        bg,
        segs: [
          seg(fit([seg(left)], leftW)[0]?.t ?? "", { bold: true }),
          seg(cb.filled, { color: theme.accent }),
          seg(cb.empty, { dim: true }),
          seg(pct),
          seg(right, wait !== null && wait > 0 ? { color: theme.warn } : { dim: true }),
        ],
      };
    }
    if (run && run.finished) {
      const orderNo = run.scopes[0] === "order" ? run.log.map((l) => /^(\S+): [\d.]+ \w+ incl\. tax/.exec(l.detail)?.[1]).filter(Boolean).pop() : undefined;
      const took = formatDuration((run.endedAt ?? now) - run.startedAt);
      const what = `${run.dry ? "dry run: " : ""}${describe({ action: run.scopes[0] === "order" ? "order" : run.action, packs: run.scopes.filter((s) => s !== "base" && s !== "order"), base: run.scopes.includes("base"), dry: run.dry })}`;
      return run.failed
        ? { bg, segs: [seg(` ✗ FAILED  ${what} · ${run.error ?? ""}`, { color: theme.danger, bold: true })] }
        : { bg, segs: [seg(` ✓ DONE  ${what}${orderNo ? ` ${orderNo}` : ""} · ${took}`, { color: theme.success, bold: true })] };
    }
    return { bg: "", segs: [] };
  };
  const st = status();
  const idleLine: Seg[] = [];
  if (!run && mode.kind !== "normal" && message) {
    idleLine.push(seg(` ${message}`, { color: theme.warn }));
  } else if (!run) {
    const age = readAt ? `${Math.max(0, Math.round((now - readAt) / 1000))} s ago` : "…";
    idleLine.push(seg(` ${selected.size} selected · counts ${age}${orderBlock && readAt ? ` · test order: ${orderBlock}` : ""}${throttled ? " · rate limited, counting slower" : ""}`, { dim: true }));
  }
  const note = readError || message;
  const hints = running
    ? "x stop the run · l log · q quit (the run goes on)"
    : "space select · s seed · d dry run · r remove · R all · o order · t tenant · l log · q quit";

  // ---- bottom lines -------------------------------------------------------------------
  let prompt: Seg[] | null = null;
  if (mode.kind === "tenant") prompt = [seg(" Tenant: ", { color: theme.accent, bold: true }), seg(mode.value), seg("▮"), seg("   enter next · esc cancel", { dim: true })];
  if (mode.kind === "baseUrl") prompt = [seg(" API address: ", { color: theme.accent, bold: true }), seg(mode.value), seg("▮"), seg("   enter apply · esc cancel", { dim: true })];
  if (mode.kind === "typed")
    prompt = [seg(" ▲ PRODUCTION ", { color: theme.onAccent, bg: theme.warn, bold: true }), seg(` ${describe(mode.req)} on ${cfg.tenant}: type the tenant name to confirm: `), seg(mode.value), seg("▮"), seg("  esc cancel", { dim: true })];
  if (mode.kind === "saveEnv") prompt = [seg(" Save tenant and address to .env? ", { color: theme.accent, bold: true }), seg("y / N", { bold: true })];
  if (mode.kind === "quit") prompt = [seg(" The run goes on in the background. Quit? ", { color: theme.accent, bold: true }), seg("(y/N)", { bold: true })];
  if (mode.kind === "stop") prompt = [seg(" Stop the run? ", { color: theme.danger, bold: true }), seg("(y/N)", { bold: true })];
  const isOrder = (mode.kind === "yn" || mode.kind === "typed") && mode.req.action === "order";
  const alertRows: Seg[][] = isOrder ? wrapText(orderAlert(cfg.tenant), W - 2).map((l) => [seg(` ${l}`, { color: theme.warn, bold: true })]) : [];
  if (mode.kind === "yn" && isOrder) prompt = [seg(" Place it? ", { color: theme.warn, bold: true }), seg("(y/N)", { bold: true })];
  else if (mode.kind === "yn") prompt = [seg(` ${describe(mode.req)} on ${cfg.tenant}: deletes the sample records. Continue? `, { color: theme.danger, bold: true }), seg("y / N", { bold: true })];

  return (
    <Box flexDirection="column" width={W}>
      <Header cfg={cfg} w={W} />
      {!fullLog && <Panel title="Packs in the shop" rows={tableRows} w={W} />}
      <Panel title={fullLog ? "Log (l to close)" : "Log"} rows={logRows} w={W} />
      {st.segs.length > 0 ? (
        <Box flexDirection="column">
          <Line segs={st.segs.map((s) => ({ ...s, bg: st.bg }))} w={W} bg={st.bg} />
        </Box>
      ) : (
        <Line segs={idleLine} w={W} />
      )}
      {alertRows.map((r, i) => (
        <Line key={i} segs={r} w={W} />
      ))}
      {prompt ? (
        <Line segs={prompt} w={W} />
      ) : note ? (
        <Line segs={[seg(` ${note}`, { color: readError ? theme.warn : undefined })]} w={W} />
      ) : (
        <Line segs={[seg(` ${hints}`, { dim: true })]} w={W} />
      )}
    </Box>
  );
};
