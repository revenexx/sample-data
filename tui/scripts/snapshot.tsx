/** Render the main screen once to text: `node --import tsx scripts/snapshot.tsx [columns] [rows]`. */
import { render } from "ink-testing-library";
import { App } from "../src/app.tsx";
import { configFromEnv } from "../src/config.ts";
import { defaultRoot, loadTargets } from "../src/plan.ts";

const columns = Number(process.argv[2] ?? 100);
const rows = Number(process.argv[3] ?? 30);
const root = defaultRoot();
const r = render(
  <App
    config={configFromEnv()}
    targets={loadTargets(root)}
    root={root}
    size={{ columns, rows }}
    poll={[60000, 60000]}
  />,
);
await new Promise((res) => setTimeout(res, 3000));
console.log(r.lastFrame());
r.unmount();
process.exit(0);
