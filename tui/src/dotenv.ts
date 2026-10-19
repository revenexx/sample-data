/** Writes settings into the repo's .env, keeping every other line (and comments) as they are. */
import { existsSync, readFileSync, writeFileSync } from "node:fs";

export const updateEnvFile = (file: string, updates: Record<string, string>): void => {
  const lines = existsSync(file) ? readFileSync(file, "utf8").split("\n") : [];
  if (lines.length > 0 && lines[lines.length - 1] === "") lines.pop();
  const left = new Map(Object.entries(updates));
  const out = lines.map((line) => {
    const m = /^\s*(?:export\s+)?([A-Z][A-Z0-9_]*)\s*=/.exec(line);
    if (!m || !left.has(m[1])) return line;
    const v = left.get(m[1])!;
    left.delete(m[1]);
    return `${m[1]}=${v}`;
  });
  for (const [k, v] of left) out.push(`${k}=${v}`);
  writeFileSync(file, out.join("\n") + "\n", { mode: 0o600 });
};
