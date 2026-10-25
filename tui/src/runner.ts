/**
 * Starts lib/load.sh, lib/remove.sh or the test-order example detached, so the run outlives this
 * window, and follows its progress events from the file the engine writes in .run/. A run that is
 * already going (started here earlier, or from a script) is followed the same way.
 */
import { spawn } from "node:child_process";
import { appendFileSync, closeSync, mkdirSync, openSync, readFileSync, readSync, statSync } from "node:fs";
import { join } from "node:path";
import { childEnv, type Config } from "./config.ts";
import { parseEventLine, type SeedEvent } from "./events.ts";
import { readLast, readLock, runDirOf, type LockInfo } from "./lock.ts";

export type RunRequest = {
  action: "seed" | "remove" | "order";
  packs: string[];
  base: boolean;
  dry: boolean;
};

export const argsFor = (r: RunRequest): string[] => {
  const a: string[] = [];
  for (const p of r.packs) a.push("--pack", p);
  if (r.action === "remove" && r.base) a.push("--base");
  if (r.action === "seed" && !r.base) a.push("--no-base");
  if (r.dry) a.push("--dry-run");
  return a;
};

/** Order the run visits its scopes: seed does the base first (when it runs at all), remove does it last. */
export const scopesFor = (r: RunRequest): string[] =>
  r.action === "order"
    ? ["order"]
    : r.action === "seed"
      ? [...(r.base ? ["base"] : []), ...r.packs]
      : [...r.packs, ...(r.base ? ["base"] : [])];

export type Handle = {
  /** Asks the engine to stop the run (./sample-data --stop). */
  stop: () => void;
  /** Stops following; the run itself goes on. */
  close: () => void;
};

export type RunCallbacks = {
  events: (es: SeedEvent[]) => void;
  exit: (code: number | null, tail: string) => void;
};

/** New bytes of a file from an offset on (a missing file is empty). */
export const readAppended = (file: string, offset: number): { text: string; offset: number } => {
  try {
    const size = statSync(file).size;
    if (size <= offset) return { text: "", offset: size < offset ? 0 : offset };
    const fd = openSync(file, "r");
    try {
      const buf = Buffer.alloc(size - offset);
      const n = readSync(fd, buf, 0, buf.length, offset);
      return { text: buf.subarray(0, n).toString("utf8"), offset: offset + n };
    } finally {
      closeSync(fd);
    }
  } catch {
    return { text: "", offset };
  }
};

/** Cuts text into event lines, keeping a half-written last line for the next read. */
export class LineBuffer {
  private rest = "";
  push(text: string): SeedEvent[] {
    this.rest += text;
    const out: SeedEvent[] = [];
    let nl: number;
    while ((nl = this.rest.indexOf("\n")) >= 0) {
      const e = parseEventLine(this.rest.slice(0, nl));
      this.rest = this.rest.slice(nl + 1);
      if (e) out.push(e);
    }
    return out;
  }
}

/** The last meaningful line of the output file next to an events file (events-X.jsonl -> out-X.log). */
export const outputTail = (eventsFile: string): string => {
  try {
    const text = readFileSync(eventsFile.replace(/events-([^/]*)\.jsonl$/, "out-$1.log"), "utf8");
    const lines = text
      .split("\n")
      .map((l) => l.replace(/^\s*[✓✗!]\s*/, "").trim())
      .filter(Boolean);
    return lines[lines.length - 1] ?? "";
  } catch {
    return "";
  }
};

/**
 * Follows one run: replays its events file from the start, then reads on as it grows, until the run's
 * lock is gone. The end is read from .run/last.json (the engine writes it before it lets go), or from
 * the child's exit when the run never got as far as taking the lock.
 */
const follow = (
  root: string,
  eventsFile: string,
  on: RunCallbacks,
  child: { code: () => number | null | undefined } | null,
  every = 300,
): Handle => {
  const runDir = runDirOf(root);
  const lines = new LineBuffer();
  let offset = 0;
  let seen = false;
  let closed = false;
  const since = Date.now();
  const drain = () => {
    const r = readAppended(eventsFile, offset);
    offset = r.offset;
    const es = lines.push(r.text);
    if (es.length) on.events(es);
  };
  const finish = () => {
    clearInterval(timer);
    closed = true;
    drain();
    const last = readLast(root, runDir);
    const code = last && last.events === eventsFile ? last.code : (child?.code() ?? null);
    on.exit(code, code === null ? "the run ended without a result" : outputTail(eventsFile));
  };
  const tick = () => {
    if (closed) return;
    drain();
    const st = readLock(root, undefined, runDir);
    if (st.kind === "starting") return;
    if (st.kind === "live" && st.info.events === eventsFile) {
      seen = true;
      return;
    }
    // Not our lock any more. A run just started may not have taken it yet.
    if (!seen && st.kind === "none" && child && child.code() === undefined && Date.now() - since < 10000) return;
    finish();
  };
  const timer = setInterval(tick, every);
  tick();
  return {
    stop: () => {
      spawn(join(root, "sample-data"), ["--stop"], { cwd: root, stdio: "ignore", detached: true }).unref();
    },
    close: () => {
      closed = true;
      clearInterval(timer);
    },
  };
};

/** Follows a run that is already going: the whole events file is replayed, then followed live. */
export const attachRun = (root: string, info: LockInfo, on: RunCallbacks, every?: number): Handle =>
  follow(root, info.events, on, null, every);

/** Starts a run in its own session (closing this window does not touch it), output into .run/out-<id>.log. */
export const startRun = (root: string, cfg: Config, req: RunRequest, on: RunCallbacks, every?: number): Handle => {
  const script = join(
    root,
    req.action === "seed" ? "lib/load.sh" : req.action === "order" ? "examples/place-test-order.sh" : "lib/remove.sh",
  );
  const runDir = runDirOf(root);
  mkdirSync(runDir, { recursive: true });
  const id = `${Date.now()}`;
  const events = join(runDir, `events-${id}.jsonl`);
  const outFile = join(runDir, `out-${id}.log`);
  const out = openSync(outFile, "a");
  let code: number | null | undefined;
  const child = spawn("bash", [script, ...argsFor(req)], {
    cwd: root,
    env: { ...childEnv(cfg), SEED_EVENTS: events },
    stdio: ["ignore", out, out],
    detached: true,
  });
  closeSync(out);
  child.on("error", (e) => {
    code = 1;
    appendFileSync(outFile, `could not start bash: ${e.message}\n`);
  });
  child.on("exit", (c) => {
    code = c ?? 1;
  });
  child.unref();
  return follow(root, events, on, { code: () => code }, every);
};
