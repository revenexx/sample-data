import assert from "node:assert/strict";
import { test } from "node:test";
import {
  applyEvent,
  etaSeconds,
  finishRun,
  formatDuration,
  formatEta,
  newRun,
  overallFraction,
  parseEventLine,
  rateLimitLeft,
  type SeedEvent,
} from "../src/events.ts";
import type { StepPlan } from "../src/plan.ts";
import { argsFor, scopesFor } from "../src/runner.ts";

const step = (name: string, weight: number, removeWeight = weight): StepPlan => ({
  name,
  kind: "upsert",
  total: 1,
  weight,
  removeWeight,
});
const plans = { base: [step("a", 1), step("b", 1)], lab: [step("x", 1), step("files", 8)] };
const feed = (events: SeedEvent[], action: "seed" | "remove" = "seed") =>
  events.reduce(
    (r, e) => applyEvent(r, e, 1000),
    newRun(action, false, action === "seed" ? ["base", "lab"] : ["lab", "base"], 0),
  );

test("parseEventLine accepts events and ignores everything else", () => {
  assert.deepEqual(parseEventLine('{"ev":"progress","done":5,"total":10}'), { ev: "progress", done: 5, total: 10 });
  assert.equal(parseEventLine("  ✓ products   1 created"), null);
  assert.equal(parseEventLine("{broken"), null);
  assert.equal(parseEventLine('{"no":"ev"}'), null);
  assert.equal(parseEventLine(""), null);
});

test("a step goes from running to done and takes the result line as its detail", () => {
  const r = feed([
    { ev: "scope", action: "seed", scope: "lab", steps: 2 },
    { ev: "step_start", i: 0, name: "files", kind: "files" },
    { ev: "progress", done: 3, total: 10 },
  ]);
  assert.equal(r.log[0].status, "run");
  assert.equal(r.log[0].done, 3);
  const done = applyEvent(
    applyEvent(r, { ev: "ok", text: "files                  10 uploaded, 0 unchanged" }, 0),
    { ev: "step_end", i: 0, name: "files", kind: "files" },
    0,
  );
  assert.equal(done.log[0].status, "ok");
  assert.equal(done.log[0].detail, "10 uploaded, 0 unchanged");
});

test("warn and error events become log lines; error marks the run failed", () => {
  const r = feed([
    { ev: "scope", action: "seed", scope: "lab", steps: 2 },
    { ev: "step_start", i: 0, name: "files", kind: "files" },
    { ev: "warn", text: "something odd" },
    { ev: "error", text: "boom" },
  ]);
  assert.equal(r.failed, true);
  assert.equal(r.error, "boom");
  assert.deepEqual(
    r.log.map((l) => l.status),
    ["err", "warn", "err"],
  );
});

test("a rate-limit warning is not a log line (the status bar shows the wait)", () => {
  const r = feed([
    { ev: "scope", action: "seed", scope: "lab", steps: 2 },
    { ev: "step_start", i: 0, name: "files", kind: "files" },
    { ev: "warn", text: "rate limited, waiting 1s" },
    { ev: "ratelimit", wait: 1 },
  ]);
  assert.deepEqual(
    r.log.map((l) => l.status),
    ["run"],
  );
  assert.equal(r.rateLimitWait, 1);
});

test("overall progress is weighted by step cost, base first", () => {
  let r = feed([{ ev: "scope", action: "seed", scope: "base", steps: 2 }]);
  assert.equal(overallFraction(r, plans), 0);
  r = feed([
    { ev: "scope", action: "seed", scope: "base", steps: 2 },
    { ev: "step_start", i: 0, name: "a", kind: "upsert" },
    { ev: "step_end", i: 0, name: "a", kind: "upsert" },
    { ev: "step_start", i: 1, name: "b", kind: "upsert" },
    { ev: "step_end", i: 1, name: "b", kind: "upsert" },
    { ev: "scope", action: "seed", scope: "lab", steps: 2 },
  ]);
  // base (weight 2) done, lab (weight 9) not started: 2 of 11.
  assert.equal(overallFraction(r, plans), 2 / 11);
  r = applyEvent(
    applyEvent(
      applyEvent(r, { ev: "step_start", i: 0, name: "x", kind: "upsert" }, 0),
      { ev: "step_end", i: 0, name: "x", kind: "upsert" },
      0,
    ),
    { ev: "step_start", i: 1, name: "files", kind: "files" },
    0,
  );
  r = applyEvent(r, { ev: "progress", done: 5, total: 10 }, 0);
  assert.equal(overallFraction(r, plans), (2 + 1 + 4) / 11);
  assert.equal(overallFraction(applyEvent(r, { ev: "done" }, 0), plans), 1);
});

test("removing walks the steps last first and skips what lib/remove.sh skips", () => {
  const rp = { lab: [step("x", 1, 0), step("y", 1, 2), step("z", 1, 2)] };
  let r = feed([{ ev: "scope", action: "remove", scope: "lab", steps: 3 }], "remove");
  r = { ...r, scopes: ["lab"] };
  r = applyEvent(
    applyEvent(r, { ev: "step_start", i: 2, name: "z", kind: "upsert" }, 0),
    { ev: "step_end", i: 2, name: "z", kind: "upsert" },
    0,
  );
  assert.equal(overallFraction(r, rp), 0.5);
  r = applyEvent(
    applyEvent(r, { ev: "step_start", i: 1, name: "y", kind: "upsert" }, 0),
    { ev: "step_end", i: 1, name: "y", kind: "upsert" },
    0,
  );
  assert.equal(overallFraction(r, rp), 1);
});

test("eta needs some progress and some time, and is proportional", () => {
  assert.equal(etaSeconds(0.01, 60000), null);
  assert.equal(etaSeconds(0.5, 2000), null);
  assert.equal(etaSeconds(0.5, 60000), 60);
  assert.equal(etaSeconds(0.25, 60000), 180);
  assert.equal(formatEta(20), "<1 min left");
  assert.equal(formatEta(240), "~4 min left");
  assert.equal(formatEta(3900), "~1 h 5 min left");
  assert.equal(formatDuration(192000), "3 min 12 s");
});

test("rate limit countdown", () => {
  const r = applyEvent(newRun("seed", false, [], 0), { ev: "ratelimit", wait: 42 }, 10_000);
  assert.equal(rateLimitLeft(r, 10_000), 42);
  assert.equal(rateLimitLeft(r, 40_500), 12);
  assert.equal(rateLimitLeft(r, 99_000), 0);
  assert.equal(rateLimitLeft(newRun("seed", false, [], 0), 0), null);
});

test("a child that dies without events fails the run with its last stderr line", () => {
  const r = finishRun(newRun("seed", false, ["base"], 0), 2, "unknown option: --x", 5);
  assert.equal(r.failed, true);
  assert.equal(r.error, "unknown option: --x");
  assert.equal(finishRun(newRun("seed", false, ["base"], 0), 0, "", 5).failed, false);
});

test("command line and scope order of a run", () => {
  const seed = { action: "seed" as const, packs: ["lab", "office"], base: true, dry: true };
  assert.deepEqual(argsFor(seed), ["--pack", "lab", "--pack", "office", "--dry-run"]);
  assert.deepEqual(scopesFor(seed), ["base", "lab", "office"]);
  const noBase = { ...seed, base: false };
  assert.deepEqual(argsFor(noBase), ["--pack", "lab", "--pack", "office", "--no-base", "--dry-run"]);
  assert.deepEqual(scopesFor(noBase), ["lab", "office"]);
  const rm = { action: "remove" as const, packs: ["lab"], base: true, dry: false };
  assert.deepEqual(argsFor(rm), ["--pack", "lab", "--base"]);
  assert.deepEqual(scopesFor(rm), ["lab", "base"]);
});
