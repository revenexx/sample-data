import assert from "node:assert/strict";
import { test } from "node:test";
import { orderAlert, orderBlocker, orderConfirm, wrapText } from "../src/order.ts";
import type { PackTarget } from "../src/plan.ts";

const industrial = { name: "industrial", products: 125 } as PackTarget;
const counts = (products: number) => ({
  products,
  categories: 0,
  attributes: 0,
  makers: 0,
  lists: 0,
  assets: 0,
  stock: 0,
  prices: 0,
});

test("the alert names the reference, the tenant and that orders cannot be deleted", () => {
  const t = orderAlert("acme");
  assert.match(t, /cannot be deleted/);
  assert.match(t, /SAMPLE-TEST/);
  assert.match(t, /tenant acme/);
  assert.match(t, /only cancels it/);
});

test("local asks y/N, any other host asks for the tenant name", () => {
  assert.equal(orderConfirm(true), "yn");
  assert.equal(orderConfirm(false), "typed");
});

test("the test order is blocked until the base and the industrial pack are in the shop", () => {
  assert.match(orderBlocker(undefined, null, null)!, /no industrial pack/);
  assert.match(orderBlocker(industrial, null, null)!, /not read yet/);
  assert.match(orderBlocker(industrial, counts(0), { found: 14, total: 14 })!, /load the base and the industrial pack/);
  assert.match(orderBlocker(industrial, counts(125), { found: 3, total: 14 })!, /load the base/);
  assert.equal(orderBlocker(industrial, counts(125), { found: 14, total: 14 }), null);
});

test("wrapText breaks at spaces and never exceeds the width", () => {
  const lines = wrapText(orderAlert("acme"), 40);
  assert.ok(lines.length > 2);
  for (const l of lines) assert.ok([...l].length <= 40, l);
  assert.equal(lines.join(" "), orderAlert("acme"));
});
