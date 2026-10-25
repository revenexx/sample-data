import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import assert from "node:assert/strict";
import { test } from "node:test";
import { bar, baseState, needsBase, formatCount, packState, ratio, totalOf } from "../src/counts.ts";
import { configFromEnv, parseDotenv, hostOf, isLocal } from "../src/config.ts";
import { loadTargets } from "../src/plan.ts";

const target = { categories: 0, attributes: 0, makers: 0, lists: 0, products: 10, assets: 20, stock: 5, prices: 8 };

test("totalOf: a row as a whole, each count capped at its target", () => {
  const t = { ...target, categories: 7, lists: 2 };
  assert.deepEqual(totalOf({ ...t, products: 12, categories: 3 }, t), {
    have: 10 + 3 + 20 + 5 + 8 + 2,
    target: 10 + 7 + 20 + 5 + 8 + 2,
  });
});

test("packState: loaded, partial, not loaded, running", () => {
  assert.equal(
    packState(
      { categories: 0, attributes: 0, makers: 0, lists: 0, products: 10, assets: 20, stock: 5, prices: 8 },
      target,
    ),
    "loaded",
  );
  assert.equal(
    packState(
      { categories: 0, attributes: 0, makers: 0, lists: 0, products: 12, assets: 20, stock: 5, prices: 8 },
      target,
    ),
    "loaded",
  );
  assert.equal(
    packState(
      { categories: 0, attributes: 0, makers: 0, lists: 0, products: 10, assets: 19, stock: 5, prices: 8 },
      target,
    ),
    "partial",
  );
  assert.equal(
    packState(
      { categories: 0, attributes: 0, makers: 0, lists: 0, products: 0, assets: 0, stock: 0, prices: 0 },
      target,
    ),
    "not loaded",
  );
  assert.equal(packState(null, target), "unknown");
  assert.equal(
    packState(
      { categories: 0, attributes: 0, makers: 0, lists: 0, products: 0, assets: 0, stock: 0, prices: 0 },
      target,
      "seed",
    ),
    "loading",
  );
  assert.equal(
    packState(
      { categories: 0, attributes: 0, makers: 0, lists: 0, products: 10, assets: 20, stock: 5, prices: 8 },
      target,
      "remove",
    ),
    "removing",
  );
});

test("baseState", () => {
  assert.equal(baseState(0, 6), "not loaded");
  assert.equal(baseState(3, 6), "partial");
  assert.equal(baseState(6, 6), "loaded");
  assert.equal(baseState(0, 0), "unknown");
});

test("ratio is clamped and an empty target is done", () => {
  assert.equal(ratio(5, 10), 0.5);
  assert.equal(ratio(15, 10), 1);
  assert.equal(ratio(0, 0), 1);
});

test("bar never shows a full bar below 100 % nor an empty one above 0 %", () => {
  assert.deepEqual(bar(0, 8), { filled: 0, empty: 8 });
  assert.deepEqual(bar(1, 8), { filled: 8, empty: 0 });
  assert.deepEqual(bar(0.001, 8), { filled: 1, empty: 7 });
  assert.deepEqual(bar(0.999, 8), { filled: 7, empty: 1 });
  assert.deepEqual(bar(0.5, 8), { filled: 4, empty: 4 });
});

test("formatCount", () => {
  assert.equal(formatCount(61, 125), "61/125");
  assert.equal(formatCount(null, 125), "…/125");
});

test("local hosts get the LOCAL badge, others are production", () => {
  for (const u of ["http://localhost:8080/v1", "http://127.0.0.1:8080/v1", "http://[::1]:8080/v1"])
    assert.equal(isLocal(u), true, u);
  for (const u of [
    "https://api.revenexx.com/v1",
    "https://localhost.evil.com/v1",
    "https://127.0.0.1.example.com",
    "nonsense",
  ])
    assert.equal(isLocal(u), false, u);
  assert.equal(hostOf("http://localhost:8080/v1"), "localhost:8080");
});

test("config reads the lib/load.sh variables", () => {
  const c = configFromEnv({ REVENEXX_TENANT: "t", REVENEXX_TOKEN: "x", REVENEXX_BASE_URL: "http://localhost:1/v1/" });
  assert.deepEqual(c, { tenant: "t", token: "x", apiKey: "", baseUrl: "http://localhost:1/v1", source: "environment" });
  assert.equal(configFromEnv({}).baseUrl, "https://api.revenexx.com/v1");
});

test("targets come from the pack files", () => {
  const t = loadTargets();
  assert.deepEqual(
    t.packs.map((p) => p.name),
    ["industrial", "electrical", "office", "lab"],
  );
  const lab = t.packs.find((p) => p.name === "lab")!;
  assert.equal(lab.products, 125);
  assert.equal(lab.assets, 557);
  assert.equal(lab.stock, 120);
  assert.equal(lab.prices, 166);
  assert.equal(lab.assetNames.length, lab.assets);
  assert.ok(lab.steps.some((s) => s.kind === "files"));
  assert.ok(t.base.checks.every((c) => c.target > 0));
});

test("config reads the repo's .env and the environment wins", () => {
  const dir = mkdtempSync(join(tmpdir(), "cfg-"));
  const f = join(dir, ".env");
  writeFileSync(
    f,
    '# c\nREVENEXX_TENANT="from-file"\nexport REVENEXX_TOKEN=tok # note\nOTHER=1\nREVENEXX_BASE_URL=http://localhost:8080/v1\n',
  );
  const fileOnly = configFromEnv({}, f);
  assert.deepEqual(
    [fileOnly.tenant, fileOnly.token, fileOnly.baseUrl, fileOnly.source],
    ["from-file", "tok", "http://localhost:8080/v1", ".env"],
  );
  const mixed = configFromEnv({ REVENEXX_TENANT: "shell" }, f);
  assert.equal(mixed.tenant, "shell");
  assert.equal(mixed.token, "tok");
  assert.equal(mixed.source, ".env + environment");
  assert.equal(configFromEnv({ REVENEXX_TENANT: "t" }, join(dir, "none")).source, "environment");
  assert.deepEqual(parseDotenv("REVENEXX_TENANT=$(touch x)\nPATH=/evil"), { REVENEXX_TENANT: "$(touch x)" });
});

test("a load runs the base only when it is picked, incomplete or not read yet", () => {
  assert.equal(needsBase(false, { found: 14, total: 14 }), false);
  assert.equal(needsBase(true, { found: 14, total: 14 }), true);
  assert.equal(needsBase(false, { found: 13, total: 14 }), true);
  assert.equal(needsBase(false, { found: 0, total: 14 }), true);
  assert.equal(needsBase(false, null), true);
});
