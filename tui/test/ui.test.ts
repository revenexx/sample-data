import assert from "node:assert/strict";
import { test } from "node:test";
import { fit, pad, seg, width } from "../src/ui.tsx";

test("pad and fit count display cells, so wide characters never overflow a panel row", () => {
  assert.equal(width([seg("日本語")]), 6);
  assert.equal(width(fit([seg("日本語ab")], 5)), 4); // a wide char is never cut in half
  assert.equal(width([seg(pad("日本", 6))]), 6);
  assert.equal(pad("abcdef", 4), "abcd");
});
