import assert from "node:assert/strict";
import { appendFileSync, mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterEach, test } from "node:test";
import { render } from "ink-testing-library";
import { App, tableLayout } from "../src/app.tsx";
import { loadTargets } from "../src/plan.ts";

const targets = loadTargets();
const empty = (async () => ({ ok: true, status: 200, json: async () => ({ items: [], data: [], page: { total: 0, hasMore: false } }) })) as unknown as typeof fetch;
const wait = (ms = 80) => new Promise((r) => setTimeout(r, ms));
const mounted: { unmount: () => void }[] = [];
afterEach(() => {
  while (mounted.length) mounted.pop()!.unmount();
});
const mount = (baseUrl: string, columns = 100) => {
  const app = render(
    <App config={{ baseUrl, tenant: "acme", apiKey: "k", token: "" }} targets={targets} root="/nonexistent" fetchImpl={empty} size={{ columns, rows: 30 }} poll={[60000, 60000]} />,
  );
  mounted.push(app);
  return app;
};

test("local host shows a LOCAL badge, any other a PRODUCTION badge", async () => {
  const a = mount("http://localhost:8080/v1");
  await wait();
  assert.match(a.lastFrame()!, /LOCAL .*tenant acme → localhost:8080/);
  a.unmount();
  const b = mount("https://api.revenexx.com/v1");
  await wait();
  assert.match(b.lastFrame()!, /▲ PRODUCTION .*tenant acme → api\.revenexx\.com/);
  b.unmount();
});

test("the table shows the base and every pack on one line each: counts against targets", async () => {
  const a = mount("http://localhost:8080/v1");
  await wait();
  const f = a.lastFrame()!;
  for (const p of ["industrial", "electrical", "office", "lab"]) assert.match(f, new RegExp(p));
  assert.match(f, /industrial\s+not loaded\s+0\/125\s+0\/\d+\s+0\/\d+\s+0\/\d+/);
  assert.match(f, /base\s+not loaded\s+0\/1\s+0\/5\s+0\/6\s+0\/2/);
  assert.match(f, /company\+contacts/);
  a.unmount();
});

test("a wide window shows all eight counts and a total bar per row; a narrow one keeps the first four", () => {
  const wide = tableLayout(160);
  assert.deepEqual(wide.metrics, ["products", "categories", "attributes", "makers", "assets", "lists", "prices", "stock"]);
  assert.ok(wide.totalBar >= 6);
  assert.ok(wide.prefix + wide.metrics.length * wide.col + 2 + wide.totalBar + wide.pctW <= 160);
  const narrow = tableLayout(98);
  assert.deepEqual(narrow.metrics, ["products", "assets", "prices", "stock"]);
  assert.equal(narrow.totalBar, 0);
  assert.ok(narrow.baseCol >= 17);
});

test("on production, seeding asks for the tenant name before anything runs", async () => {
  const a = mount("https://api.revenexx.com/v1");
  await wait();
  a.stdin.write(" ");
  await wait();
  a.stdin.write("s");
  await wait();
  assert.match(a.lastFrame()!, /type the tenant name to confirm/);
  a.stdin.write("wrong");
  a.stdin.write("\r");
  await wait();
  assert.match(a.lastFrame()!, /type acme exactly to confirm/);
  assert.doesNotMatch(a.lastFrame()!, /SEEDING/);
  a.unmount();
});

test("a selection is needed, space toggles it, t changes the tenant and the header follows", async () => {
  const a = mount("http://localhost:8080/v1");
  await wait();
  a.stdin.write("s");
  await wait();
  assert.match(a.lastFrame()!, /select a row first/);
  a.stdin.write(" ");
  await wait();
  assert.match(a.lastFrame()!, /\[x\]\s+base/);
  a.stdin.write("j");
  await wait();
  a.stdin.write(" ");
  await wait();
  assert.match(a.lastFrame()!, /\[x\]\s+industrial/);
  a.stdin.write("t");
  await wait();
  for (let i = 0; i < 4; i++) a.stdin.write("\x7f");
  a.stdin.write("beta");
  a.stdin.write("\r");
  await wait();
  a.stdin.write("\r");
  await wait();
  assert.match(a.lastFrame()!, /Save tenant and address to \.env\?/);
  a.stdin.write("n");
  await wait();
  assert.match(a.lastFrame()!, /tenant beta → localhost:8080/);
  a.unmount();
});

test("at 80 columns no line is wider than the terminal", async () => {
  const a = mount("https://api.revenexx.com/v1", 80);
  await wait();
  for (const line of a.lastFrame()!.split("\n")) assert.ok([...line].length <= 80, `too wide (${[...line].length}): ${line}`);
  a.unmount();
});

test("a run that is already going is shown live; s is refused, q asks and leaves it running, x asks before stopping", async () => {
  const dir = mkdtempSync(join(tmpdir(), "tui-run-"));
  const prev = process.env.SAMPLE_DATA_RUN_DIR;
  process.env.SAMPLE_DATA_RUN_DIR = dir;
  try {
    const events = join(dir, "events-1.jsonl");
    writeFileSync(
      events,
      [
        '{"ev":"start","action":"remove","tenant":"acme","dry":false,"base":false,"packs":["office"]}',
        '{"ev":"scope","action":"remove","scope":"office","steps":3}',
        '{"ev":"step_start","i":2,"name":"products","kind":"upsert"}',
        '{"ev":"progress","done":5,"total":10}',
      ].join("\n") + "\n",
    );
    mkdirSync(join(dir, "lock"));
    writeFileSync(
      join(dir, "lock", "info"),
      [`pid=${process.pid}`, "pidstart=", "pgid=1", "action=remove", "scopes=office", `started=${Math.floor(Date.now() / 1000)}`, "dry=0", `events=${events}`, ""].join("\n"),
    );
    const a = mount("http://localhost:8080/v1");
    await wait(700);
    assert.match(a.lastFrame()!, /REMOVING office/);
    assert.match(a.lastFrame()!, /office · products\s+5 \/ 10/);
    a.stdin.write("s");
    await wait();
    assert.match(a.lastFrame()!, /a run is going \(x stops it\)/);
    a.stdin.write("q");
    await wait();
    assert.match(a.lastFrame()!, /The run goes on in the background\. Quit\? \(y\/N\)/);
    a.stdin.write("n");
    await wait();
    assert.doesNotMatch(a.lastFrame()!, /Quit\?/);
    a.stdin.write("x");
    await wait();
    assert.match(a.lastFrame()!, /Stop the run\? \(y\/N\)/);
    a.stdin.write("n");
    await wait();
    assert.match(a.lastFrame()!, /REMOVING office/);
    // the run ends: the lock goes, last.json says how
    appendFileSync(events, '{"ev":"done"}\n');
    writeFileSync(join(dir, "last.json"), JSON.stringify({ pid: process.pid, action: "remove", scopes: "office", started: 1, ended: 2, code: 0, events }));
    rmSync(join(dir, "lock"), { recursive: true });
    await wait(700);
    assert.match(a.lastFrame()!, /✓ DONE\s+remove office/);
    a.unmount();
  } finally {
    if (prev === undefined) delete process.env.SAMPLE_DATA_RUN_DIR;
    else process.env.SAMPLE_DATA_RUN_DIR = prev;
    rmSync(dir, { recursive: true, force: true });
  }
});
