/** The pure part of the main table: counts against targets, state, bars. */
export const METRICS = [
  "products",
  "categories",
  "attributes",
  "makers",
  "assets",
  "lists",
  "prices",
  "stock",
] as const;
export type Metric = (typeof METRICS)[number];
/** Column headers; "lists" is the pack's price lists. */
export const METRIC_LABEL: Record<Metric, string> = {
  products: "products",
  categories: "categories",
  attributes: "attributes",
  makers: "makers",
  assets: "assets",
  lists: "price lists",
  prices: "prices",
  stock: "stock",
};
/** The columns a narrow window drops first, in this order; the four of the first version stay. */
export const OPTIONAL_METRICS: Metric[] = ["lists", "makers", "attributes", "categories"];
export type Counts = Record<Metric, number>;
export type Targets4 = Record<Metric, number>;

/** A row as a whole: records in the shop (capped at each target) against all targets. */
export const totalOf = (counts: Counts, target: Targets4): { have: number; target: number } =>
  METRICS.reduce((t, m) => ({ have: t.have + Math.min(counts[m], target[m]), target: t.target + target[m] }), {
    have: 0,
    target: 0,
  });
export type PackState = "loaded" | "partial" | "not loaded" | "loading" | "removing" | "unknown";

/** Share of the target that is in the shop, 0..1. An empty target counts as done. */
export const ratio = (have: number, target: number): number =>
  target <= 0 ? 1 : Math.min(1, Math.max(0, have / target));

/**
 * loaded: everything at target or above; not loaded: nothing at all;
 * partial: anything in between. `running` overrides while a run touches the pack.
 */
export const packState = (counts: Counts | null, target: Targets4, running?: "seed" | "remove"): PackState => {
  if (running === "seed") return "loading";
  if (running === "remove") return "removing";
  if (!counts) return "unknown";
  const have = METRICS.map((m) => counts[m]);
  if (have.every((n) => n === 0)) return "not loaded";
  if (METRICS.every((m) => counts[m] >= target[m])) return "loaded";
  return "partial";
};

export const baseState = (found: number, total: number, running?: "seed" | "remove"): PackState => {
  if (running === "seed") return "loading";
  if (running === "remove") return "removing";
  if (total <= 0) return "unknown";
  if (found === 0) return "not loaded";
  return found >= total ? "loaded" : "partial";
};

/** Filled and empty cells of a bar. Anything above 0 shows a cell, anything below 100 % leaves one empty. */
export const bar = (r: number, width: number): { filled: number; empty: number } => {
  const w = Math.max(0, width);
  let filled = Math.round(Math.min(Math.max(r, 0), 1) * w);
  if (r > 0 && filled === 0) filled = 1;
  if (r < 1 && filled === w && w > 1) filled = w - 1;
  return { filled, empty: w - filled };
};

export const formatCount = (have: number | null, target: number): string => `${have ?? "…"}/${target}`;

/** A short ▰▱ bar: filled cells, then empty ones. */
export const cellBar = (r: number, cells = 5): { filled: string; empty: string } => {
  const { filled, empty } = bar(r, cells);
  return { filled: "▰".repeat(filled), empty: "▱".repeat(empty) };
};

/**
 * Whether a load runs the base: when its row is selected, or when the live
 * counts show it missing or incomplete (the packs need it) or are not read yet.
 */
export const needsBase = (selected: boolean, base: { found: number; total: number } | null): boolean =>
  selected || base === null || base.found < base.total;
