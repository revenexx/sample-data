import assert from "node:assert/strict";
import { appendFileSync, mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";
import { busyText, describeLock, parseLockInfo, pidAlive, readLast, readLock, runDirOf } from "../src/lock.ts";
import { attachRun, LineBuffer, readAppended } from "../src/runner.ts";

const INFO = ["pid=4242", "pidstart=Mon Oct 19 16:12:03 2026", "pgid=4242", "action=remove", "scopes=office base", "started=1760883123", "dry=0", "events=/r/.run/events-1.jsonl", ""].join("\n");
const tmp = () => mkdtempSync(join(tmpdir(), "run-lock-"));
const withLock = (dir: string, info: string | null) => {
  mkdirSync(join(dir, "lock"), { recursive: true });
  if (info !== null) writeFileSync(join(dir, "lock", "info"), info);
};
const wait = (ms: number) => new Promise((r) => setTimeout(r, ms));
const inRunDir = async (fn: (dir: string) => Promise<void>) => {
  const dir = tmp();
  const prev = process.env.SAMPLE_DATA_RUN_DIR;
  process.env.SAMPLE_DATA_RUN_DIR = dir;
  try {
    await fn(dir);
  } finally {
    if (prev === undefined) delete process.env.SAMPLE_DATA_RUN_DIR;
    else process.env.SAMPLE_DATA_RUN_DIR = prev;
    rmSync(dir, { recursive: true, force: true });
  }
};

test("parseLockInfo reads what lib/lock.sh writes", () => {
  const i = parseLockInfo(INFO)!;
  assert.equal(i.pid, 4242);
  assert.equal(i.action, "remove");
  assert.deepEqual(i.scopes, ["office", "base"]);
  assert.equal(i.pidstart, "Mon Oct 19 16:12:03 2026");
  assert.equal(i.started, 1760883123);
  assert.equal(i.dry, false);
  assert.equal(i.events, "/r/.run/events-1.jsonl");
});

test("parseLockInfo rejects a half-written or foreign file", () => {
  assert.equal(parseLockInfo(""), null);
  assert.equal(parseLockInfo("pid=abc\naction=load\n"), null);
  assert.equal(parseLockInfo("pid=5\naction=explode\n"), null);
});

test("readLock: none without a lock, starting without its info, live or stale by the process", () => {
  const dir = tmp();
  try {
    assert.equal(readLock("/x", () => true, dir).kind, "none");
    withLock(dir, null);
    assert.equal(readLock("/x", () => true, dir).kind, "starting");
    withLock(dir, "pid=\n");
    assert.equal(readLock("/x", () => true, dir).kind, "starting");
    withLock(dir, INFO);
    assert.equal(readLock("/x", () => true, dir).kind, "live");
    const stale = readLock("/x", () => false, dir);
    assert.equal(stale.kind, "stale");
    assert.equal(stale.kind === "stale" && stale.info.pid, 4242);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("readLock hands the pid and its start time to the alive check", () => {
  const dir = tmp();
  try {
    withLock(dir, INFO);
    let seen: [number, string] | null = null;
    readLock("/x", (pid, start) => ((seen = [pid, start]), true), dir);
    assert.deepEqual(seen, [4242, "Mon Oct 19 16:12:03 2026"]);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("pidAlive: this process is alive, a gone pid is not, a reused pid (other start time) is not", () => {
  assert.equal(pidAlive(process.pid, ""), true);
  assert.equal(pidAlive(4194301, ""), false);
  assert.equal(pidAlive(process.pid, "Thu Jan  1 00:00:00 1970"), false);
});

test("runDirOf honours SAMPLE_DATA_RUN_DIR", () => {
  assert.equal(runDirOf("/r", {}), "/r/.run");
  assert.equal(runDirOf("/r", { SAMPLE_DATA_RUN_DIR: "/t" }), "/t");
});

test("readLast needs a code and an events path", () => {
  const dir = tmp();
  try {
    assert.equal(readLast("/x", dir), null);
    writeFileSync(join(dir, "last.json"), JSON.stringify({ pid: 1, action: "load", scopes: "office", started: 1, ended: 2, code: 143, events: "/e" }));
    assert.equal(readLast("/x", dir)?.code, 143);
    writeFileSync(join(dir, "last.json"), "{ not json");
    assert.equal(readLast("/x", dir), null);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("the refusal names the run and the way out", () => {
  const i = parseLockInfo(INFO)!;
  assert.match(describeLock(i), /^remove office base since \d\d:\d\d \(pid 4242\)$/);
  assert.match(busyText(i), /^a run is already going: remove office base since \d\d:\d\d \(pid 4242\); wait for it or stop it with \.\/sample-data --stop$/);
  assert.match(describeLock({ ...i, action: "order", scopes: ["order"], dry: false }), /^test order since/);
  assert.match(describeLock({ ...i, dry: true }), /\(dry run\) since/);
});

test("LineBuffer keeps a half-written line for the next read; readAppended reads from an offset", () => {
  const b = new LineBuffer();
  assert.equal(b.push('{"ev":"ok","text":"a"}\n{"ev":"do').length, 1);
  assert.deepEqual(b.push('ne"}\nnoise\n').map((e) => e.ev), ["done"]);
  const dir = tmp();
  try {
    const f = join(dir, "e.jsonl");
    assert.deepEqual(readAppended(f, 0), { text: "", offset: 0 });
    writeFileSync(f, "abc\n");
    assert.deepEqual(readAppended(f, 0), { text: "abc\n", offset: 4 });
    appendFileSync(f, "def\n");
    assert.deepEqual(readAppended(f, 4), { text: "def\n", offset: 8 });
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("attachRun replays the events file, follows it, and reports the exit from last.json once the lock is gone", () =>
  inRunDir(async (dir) => {
    const events = join(dir, "events-1.jsonl");
    writeFileSync(events, '{"ev":"scope","action":"seed","scope":"office","steps":2}\n{"ev":"step_start","i":0,"name":"x","kind":"upsert"}\n');
    const info = [`pid=${process.pid}`, "pidstart=", "pgid=1", "action=load", "scopes=office", "started=1", "dry=0", `events=${events}`, ""].join("\n");
    withLock(dir, info);
    const got: string[] = [];
    let exit: [number | null, string] | null = null;
    const h = attachRun("/x", parseLockInfo(info)!, { events: (es) => got.push(...es.map((e) => e.ev)), exit: (c, t) => (exit = [c, t]) }, 20);
    await wait(100);
    assert.deepEqual(got, ["scope", "step_start"]);
    assert.equal(exit, null);
    appendFileSync(events, '{"ev":"done"}\n');
    writeFileSync(join(dir, "last.json"), JSON.stringify({ pid: process.pid, action: "load", scopes: "office", started: 1, ended: 2, code: 0, events }));
    rmSync(join(dir, "lock"), { recursive: true });
    await wait(100);
    assert.deepEqual(got, ["scope", "step_start", "done"]);
    assert.deepEqual(exit, [0, ""]);
    h.close();
  }));

test("attachRun: a lock whose process died without last.json ends as a run without a result", () =>
  inRunDir(async (dir) => {
    const events = join(dir, "events-2.jsonl");
    writeFileSync(events, "");
    const info = ["pid=4194301", "pidstart=", "pgid=1", "action=remove", "scopes=lab", "started=1", "dry=0", `events=${events}`, ""].join("\n");
    withLock(dir, info);
    let exit: [number | null, string] | null = null;
    attachRun("/x", parseLockInfo(info)!, { events: () => {}, exit: (c, t) => (exit = [c, t]) }, 20);
    await wait(100);
    assert.deepEqual(exit, [null, "the run ended without a result"]);
  }));
