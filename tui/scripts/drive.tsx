/**
 * Drives the real TUI against a tenant through ink-testing-library's stdin, to
 * check it end to end: `node --import tsx scripts/drive.tsx <pack> dry|remove|seed ...`.
 * Local tenants only. Prints a frame every 20 s and the final one.
 */
import { render } from "ink-testing-library";
import { App } from "../src/app.tsx";
import { configFromEnv, isLocal } from "../src/config.ts";
import { defaultRoot, loadTargets } from "../src/plan.ts";

const [pack, ...steps] = process.argv.slice(2);
const cfg = configFromEnv();
if (!isLocal(cfg.baseUrl)) throw new Error("drive.tsx only runs against a local tenant");
const root = defaultRoot();
const targets = loadTargets(root);
const idx = targets.packs.findIndex((p) => p.name === pack);
if (idx < 0) throw new Error(`no pack ${pack}`);
const r = render(<App config={cfg} targets={targets} root={root} size={{ columns: 100, rows: 28 }} poll={[3000, 1500]} />);
const sleep = (ms: number) => new Promise((res) => setTimeout(res, ms));
const key = async (k: string) => { r.stdin.write(k); await sleep(150); };

await sleep(2500);
for (let i = 0; i < idx; i++) await key("j");
await key(" ");
for (const step of steps) {
  console.log(`\n===== ${step} ${pack} =====`);
  if (step === "dry") await key("d");
  if (step === "seed") await key("s");
  if (step === "remove") { await key("r"); await key("y"); }
  await sleep(1000);
  let last = 0;
  for (;;) {
    const f = r.lastFrame()!;
    if (Date.now() - last > 20000) { last = Date.now(); console.log(f, "\n"); }
    if (/ DONE | FAILED /.test(f)) { console.log(f); break; }
    await sleep(500);
  }
  await sleep(4000);
  console.log(`----- after ${step}, counts refreshed -----`);
  console.log(r.lastFrame());
}
r.unmount();
process.exit(0);
