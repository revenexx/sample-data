import assert from "node:assert/strict";
import { test } from "node:test";
import { ShopReader, readCounts } from "../src/api.ts";
import type { PackTarget } from "../src/plan.ts";

const pack = {
  name: "p", products: 3, categories: 2, attributes: 2, makers: 2, assets: 2, lists: 1, stock: 2, prices: 4,
  manufacturers: ["M1", "M2"], categoryCodes: ["C1", "C2"], attributeCodes: ["a1", "a2"], assetNames: ["a.jpg", "b.jpg"],
  stockSkus: ["S1", "S2"], priceLists: ["L1"], folder: "sample-data/p", steps: [],
} as PackTarget;

const fakeFetch = (calls: string[]) =>
  (async (url: string) => {
    const path = url.replace("http://x/v1", "");
    calls.push(path);
    const json = (b: unknown) => ({ ok: true, status: 200, json: async () => b }) as Response;
    if (path.startsWith("/products/manufacturers?limit=200")) return json({ items: [{ code: "M1" }, { code: "M2" }], page: { hasMore: false } });
    if (path.startsWith("/products/manufacturers")) return json({ items: [{ id: path.includes("M1") ? "m1" : "m2" }] });
    if (path.startsWith("/products/categories")) return json({ items: [{ code: "C1" }, { code: "OTHER" }], page: { hasMore: false } });
    if (path.startsWith("/products/attributes?limit=200&offset=0")) return json({ items: [{ code: "a1" }], page: { hasMore: true } });
    if (path.startsWith("/products/attributes?limit=200&offset=200")) return json({ items: [{ code: "a2" }], page: { hasMore: false } });
    if (path.startsWith("/prices/lists?limit=200")) return json({ items: [{ code: "L1" }], page: { hasMore: false } });
    if (path.startsWith("/products?manufacturer_id=m1")) return json({ items: [{}], page: { total: 2 } });
    if (path.startsWith("/products?manufacturer_id=m2")) return json({ items: [{}], page: { total: 1 } });
    if (path === "/storage/folders") return json({ data: [{ id: "f1", path: "/sample-data/p/" }] });
    if (path.startsWith("/storage/assets")) return json({ data: [{ original_name: "a.jpg" }, { original_name: "old.jpg" }], meta: { last_page: 1 } });
    if (path.startsWith("/inventories/stock")) return json({ items: [{ sku: "S1" }, { sku: "OTHER" }], page: { hasMore: false } });
    if (path.startsWith("/prices/lists?")) return json({ items: [{ id: "l1" }] });
    if (path.startsWith("/prices/lists/l1/entries")) return json({ items: [{}], page: { total: 4 } });
    return { ok: false, status: 404, json: async () => ({}) } as Response;
  }) as unknown as typeof fetch;

test("counts a pack by its manufacturers, folder, price lists and stock SKUs", async () => {
  const calls: string[] = [];
  const reader = new ShopReader({ baseUrl: "http://x/v1", tenant: "t", apiKey: "", token: "tok" }, fakeFetch(calls));
  const c = await readCounts(reader, [pack]);
  assert.deepEqual(c.p, { products: 3, categories: 1, attributes: 2, makers: 2, assets: 1, lists: 1, prices: 4, stock: 1 });
});

test("a pack that is not there counts zero", async () => {
  const reader = new ShopReader({ baseUrl: "http://x/v1", tenant: "t", apiKey: "", token: "tok" }, (async (u: string) => ({
    ok: true, status: 200, json: async () => (u.includes("/storage/folders") ? { data: [] } : { items: [], page: { total: 0, hasMore: false } }),
  })) as unknown as typeof fetch);
  assert.deepEqual((await readCounts(reader, [pack])).p, { products: 0, categories: 0, attributes: 0, makers: 0, assets: 0, lists: 0, prices: 0, stock: 0 });
});

test("API errors name the route and status", async () => {
  const reader = new ShopReader({ baseUrl: "http://x/v1", tenant: "t", apiKey: "", token: "" }, (async () => ({
    ok: false, status: 401, json: async () => ({ message: "no" }),
  })) as unknown as typeof fetch);
  await assert.rejects(reader.get("/products?limit=1"), /\/products answered 401: no/);
});

test("a 429 is retried quietly and noted, never more than 3 requests at once", async () => {
  let n = 0;
  let live = 0;
  let peak = 0;
  const f = (async () => {
    live++;
    peak = Math.max(peak, live);
    await new Promise((r) => setTimeout(r, 5));
    live--;
    if (++n === 1) return { ok: false, status: 429, headers: new Headers(), json: async () => ({}) } as Response;
    return { ok: true, status: 200, headers: new Headers(), json: async () => ({ items: [] }) } as Response;
  }) as unknown as typeof fetch;
  const reader = new ShopReader({ baseUrl: "http://x/v1", tenant: "t", apiKey: "", token: "tok" }, f, 1);
  await Promise.all(Array.from({ length: 8 }, () => reader.get("/x")));
  assert.ok(reader.rateLimitedAt !== null);
  assert.ok(peak <= 3);
});

test("products follow a remove and a new load: a gone manufacturer id is looked up again", async () => {
  // After a remove and a new load the manufacturer has a new id; a filter by the old id answers 200, total 0.
  let mid = "old";
  const f = (async (url: string) => {
    const path = url.replace("http://x/v1", "");
    const json = (b: unknown) => ({ ok: true, status: 200, headers: new Headers(), json: async () => b }) as Response;
    if (path.startsWith("/products/manufacturers")) return json({ items: [{ id: mid }] });
    if (path.startsWith("/products?manufacturer_id=new")) return json({ items: [{}], page: { total: 5 } });
    return json({ items: [], page: { total: 0 } });
  }) as unknown as typeof fetch;
  const reader = new ShopReader({ baseUrl: "http://x/v1", tenant: "t", apiKey: "", token: "tok" }, f);
  const one = { ...pack, manufacturers: ["M1"] } as PackTarget;
  assert.equal(await reader.products(one), 0);
  mid = "new";
  assert.equal(await reader.products(one), 5);
});
