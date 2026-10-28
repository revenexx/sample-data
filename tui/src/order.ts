/** The test order: what to warn about, how to confirm it, and when it can run. */
import type { Counts } from "./counts.ts";
import type { PackTarget } from "./plan.ts";

export const orderAlert = (tenant: string): string =>
  `Orders cannot be deleted. This places a real test order (reference SAMPLE-TEST) in tenant ${tenant}; removing the sample data later only cancels it, it stays in the order history.`;

/** Locally a y/N is enough; on a production host the tenant name has to be typed. */
export const orderConfirm = (local: boolean): "yn" | "typed" => (local ? "yn" : "typed");

/** Why the test order cannot run now, or null when it can: it needs the base and the industrial pack in the shop. */
export const orderBlocker = (
  industrial: PackTarget | undefined,
  counts: Counts | null,
  base: { found: number; total: number } | null,
): string | null => {
  if (!industrial) return "no industrial pack here";
  if (!counts || !base) return "counts not read yet";
  if (counts.products < industrial.products || base.found < base.total)
    return "load the base and the industrial pack first";
  return null;
};

/** Cut text into lines of at most `w` cells at spaces. */
export const wrapText = (text: string, w: number): string[] => {
  const out: string[] = [];
  let line = "";
  for (const word of text.split(" ")) {
    if (line && [...line].length + 1 + [...word].length > w) {
      out.push(line);
      line = word;
    } else line = line ? `${line} ${word}` : word;
  }
  if (line) out.push(line);
  return out;
};
