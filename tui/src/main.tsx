import { join } from "node:path";
import { render } from "ink";
import { App } from "./app.tsx";
import { configFromEnv } from "./config.ts";
import { defaultRoot, loadTargets } from "./plan.ts";

if (!process.stdin.isTTY || !process.stdout.isTTY) {
  console.error("The seeder TUI needs an interactive terminal. Run ./sample-data --help for the flags to use in scripts.");
  process.exit(1);
}

const root = defaultRoot();
const targets = loadTargets(root);
const out = process.stdout;
out.write("\x1b[?1049h\x1b[H");
const leave = () => out.write("\x1b[?1049l");
process.on("exit", leave);
const app = render(<App config={configFromEnv(process.env, join(root, ".env"))} targets={targets} root={root} />, { exitOnCtrlC: false });
await app.waitUntilExit();
// A run started here is detached and goes on; nothing else should keep this process alive.
process.exit(0);
