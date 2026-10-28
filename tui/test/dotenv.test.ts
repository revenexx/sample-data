import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";
import { updateEnvFile } from "../src/dotenv.ts";

test("updateEnvFile changes the given keys and keeps everything else", () => {
  const f = join(mkdtempSync(join(tmpdir(), "env-")), ".env");
  writeFileSync(f, "# mine\nREVENEXX_TENANT=old\nREVENEXX_TOKEN=secret\n\n");
  updateEnvFile(f, { REVENEXX_TENANT: "new", REVENEXX_BASE_URL: "http://localhost:8080/v1" });
  assert.equal(
    readFileSync(f, "utf8"),
    "# mine\nREVENEXX_TENANT=new\nREVENEXX_TOKEN=secret\n\nREVENEXX_BASE_URL=http://localhost:8080/v1\n",
  );
});
