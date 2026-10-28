/**
 * The engines' run lock (lib/lock.sh): .run/lock/info while a run goes, .run/last.json
 * once it has ended. The terminal UI reads both to show or follow a run it did not start.
 */
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

export type LockInfo = {
  pid: number;
  pidstart: string;
  pgid: number;
  action: "load" | "remove" | "order";
  scopes: string[];
  /** Epoch seconds. */
  started: number;
  dry: boolean;
  events: string;
};

export type LockState =
  | { kind: "none" }
  /** The lock directory exists but its info is not written yet. */
  | { kind: "starting" }
  | { kind: "live"; info: LockInfo }
  /** The run's process is gone without letting go (kill -9, power loss). */
  | { kind: "stale"; info: LockInfo };

export type LastRun = {
  pid: number;
  action: string;
  scopes: string;
  started: number;
  ended: number;
  code: number;
  events: string;
};

export const runDirOf = (root: string, env: NodeJS.ProcessEnv = process.env): string =>
  env.SAMPLE_DATA_RUN_DIR || join(root, ".run");

export const parseLockInfo = (text: string): LockInfo | null => {
  const kv: Record<string, string> = {};
  for (const line of text.split("\n")) {
    const i = line.indexOf("=");
    if (i > 0) kv[line.slice(0, i)] = line.slice(i + 1);
  }
  const pid = Number(kv.pid);
  const action = kv.action;
  if (!Number.isInteger(pid) || pid <= 0 || (action !== "load" && action !== "remove" && action !== "order"))
    return null;
  return {
    pid,
    pidstart: kv.pidstart ?? "",
    pgid: Number(kv.pgid) || 0,
    action,
    scopes: (kv.scopes ?? "").split(/\s+/).filter(Boolean),
    started: Number(kv.started) || 0,
    dry: kv.dry === "1",
    events: kv.events ?? "",
  };
};

/** Process alive and still the same one (a reused pid has another start time). */
export const pidAlive = (pid: number, pidstart: string): boolean => {
  try {
    process.kill(pid, 0);
  } catch (e: any) {
    if (e?.code !== "EPERM") return false;
  }
  if (!pidstart) return true;
  try {
    const now = execFileSync("ps", ["-o", "lstart=", "-p", String(pid)], {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
    }).trim();
    return now === pidstart;
  } catch {
    return false;
  }
};

export const readLock = (
  root: string,
  alive: (pid: number, pidstart: string) => boolean = pidAlive,
  runDir = runDirOf(root),
): LockState => {
  let text: string;
  try {
    text = readFileSync(join(runDir, "lock", "info"), "utf8");
  } catch {
    // The directory without its info is a run that is just starting.
    return { kind: existsSync(join(runDir, "lock")) ? "starting" : "none" };
  }
  const info = parseLockInfo(text);
  if (!info) return { kind: "starting" };
  return alive(info.pid, info.pidstart) ? { kind: "live", info } : { kind: "stale", info };
};

export const readLast = (root: string, runDir = runDirOf(root)): LastRun | null => {
  try {
    const o = JSON.parse(readFileSync(join(runDir, "last.json"), "utf8"));
    return typeof o?.code === "number" && typeof o?.events === "string" ? (o as LastRun) : null;
  } catch {
    return null;
  }
};

const clock = (epochSeconds: number): string =>
  new Date(epochSeconds * 1000).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", hour12: false });

/** "remove office (dry run) since 16:12 (pid 1234)", as ./sample-data --status prints it. */
export const describeLock = (i: LockInfo): string =>
  `${i.action === "order" ? "test order" : [i.action, ...i.scopes].join(" ")}${i.dry ? " (dry run)" : ""} since ${clock(i.started)} (pid ${i.pid})`;

/** The refusal for a run that is going (the engines print the same line, with ./sample-data --stop). */
export const busyText = (i: LockInfo, stopHint = "wait for it or stop it with ./sample-data --stop"): string =>
  `a run is already going: ${describeLock(i)}; ${stopHint}`;
