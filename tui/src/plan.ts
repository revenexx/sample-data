/**
 * What a pack should look like in the shop (the targets), read from the pack's
 * own files, plus the step list with weights for the progress estimate.
 */
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { basename, dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

export type StepPlan = {
  name: string;
  kind: string;
  total: number;
  /** Rough share of a run's time when seeding. */
  weight: number;
  /** The same when removing (0 for steps lib/remove.sh skips). */
  removeWeight: number;
};

export type PackTarget = {
  name: string;
  products: number;
  categories: number;
  attributes: number;
  makers: number;
  assets: number;
  lists: number;
  categoryCodes: string[];
  attributeCodes: string[];
  stock: number;
  prices: number;
  manufacturers: string[];
  assetNames: string[];
  stockSkus: string[];
  priceLists: string[];
  folder: string;
  steps: StepPlan[];
};

/** Records of one route, looked up by exact key; `tiers` also counts the shipping method's rate-tier set. */
export type BasePart = { route: string; key: string; values: string[]; tiers?: boolean };
/** One column of the base row: a few routes counted together against one target. */
export type BaseCheck = { label: string; parts: BasePart[]; target: number };
export type BaseTarget = { checks: BaseCheck[]; steps: StepPlan[] };
export type Targets = { packs: PackTarget[]; base: BaseTarget };

export const defaultRoot = (): string =>
  process.env.SAMPLE_DATA_ROOT || resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");

const readJson = (file: string): any => JSON.parse(readFileSync(file, "utf8"));
const readArray = (file: string): any[] => (existsSync(file) ? readJson(file) : []);

/** Weight of a step: an upload takes about a second (storage rate limit), a record a tenth. */
export const stepWeight = (kind: string, total: number): number => {
  if (kind === "files") return Math.max(total, 1);
  if (kind === "price_entries") return Math.max(total, 1) * 3;
  return Math.max(total * 0.12, 0.5);
};

const removable = (step: any): boolean => {
  const kind = step.kind ?? "upsert";
  if (step.mode === "ensure" || step.remove === "with_parent") return false;
  return kind === "upsert" || kind === "files" || kind === "stock";
};

export const loadSteps = (manifestFile: string): StepPlan[] => {
  const dir = dirname(manifestFile);
  return (readJson(manifestFile).steps as any[]).map((s) => {
    const kind = s.kind ?? "upsert";
    const total = s.file ? readArray(join(dir, s.file)).length || 1 : 1;
    const weight = stepWeight(kind, total);
    return { name: s.name, kind, total, weight, removeWeight: removable(s) ? weight : 0 };
  });
};

export const loadPack = (root: string, name: string): PackTarget => {
  const dir = join(root, "packs", name);
  const products = readArray(join(dir, "products.json"));
  const assets = readArray(join(dir, "assets.json"));
  // lib/load.sh books no row for a target of 0 without other fields (an out-of-stock product).
  const stock = readArray(join(dir, "stock.json")).filter((s) => s.on_hand > 0 || Object.keys(s).some((k) => !["sku", "location", "on_hand"].includes(k)));
  const priceFiles = readArray(join(dir, "price-entries.json"));
  const manifest = readJson(join(dir, "manifest.json"));
  const filesStep = (manifest.steps as any[]).find((s) => s.kind === "files");
  const categories = readArray(join(dir, "categories.json"));
  const attributes = readArray(join(dir, "attributes.json"));
  const makers = [...new Set<string>(products.map((p) => p.manufacturer).filter(Boolean))];
  return {
    name,
    products: products.length,
    categories: categories.length,
    attributes: attributes.length,
    makers: makers.length,
    assets: assets.length,
    lists: priceFiles.length,
    categoryCodes: categories.map((c) => String(c.code)),
    attributeCodes: attributes.map((a) => String(a.code)),
    stock: stock.length,
    prices: priceFiles.reduce((n, l) => n + (l.entries?.length ?? 0), 0),
    manufacturers: makers,
    assetNames: assets.map((a) => basename(a.file)),
    stockSkus: stock.map((s) => s.sku),
    priceLists: priceFiles.map((l) => l.list),
    folder: filesStep?.folder ?? `sample-data/${name}`,
    steps: loadSteps(join(dir, "manifest.json")),
  };
};

export const loadBase = (root: string): BaseTarget => {
  const dir = join(root, "base");
  const part = (route: string, key: string, file: string, tiers = false): BasePart => ({
    route,
    key,
    values: readArray(join(dir, file)).map((r) => String(r[key])),
    ...(tiers ? { tiers } : {}),
  });
  const column = (label: string, ...parts: BasePart[]): BaseCheck => ({
    label,
    parts,
    target: parts.reduce((n, p) => n + p.values.length + (p.tiers ? 1 : 0), 0),
  });
  return {
    checks: [
      column("market", part("/markets", "code", "markets.json")),
      column(
        "company+contacts",
        part("/customers/organizations", "customer_number", "organizations.json"),
        part("/customers/contacts", "external_id", "contacts.json"),
        part("/customers/addresses", "external_id", "addresses.json"),
      ),
      column(
        "promos+vouchers",
        part("/promotions/promotions", "code", "promotions.json"),
        part("/promotions/batches", "request_ref", "voucher-batches.json"),
        part("/promotions/vouchers", "code", "vouchers.json"),
      ),
      column("shipping", part("/shipping/methods", "code", "shipping-methods.json", true)),
    ],
    steps: loadSteps(join(dir, "manifest.json")),
  };
};

export const loadTargets = (root: string = defaultRoot()): Targets => {
  const names = readdirSync(join(root, "packs"), { withFileTypes: true })
    .filter((d) => d.isDirectory() && existsSync(join(root, "packs", d.name, "manifest.json")))
    .map((d) => d.name);
  const order = ["industrial", "electrical", "office", "lab"];
  names.sort((a, b) => (order.indexOf(a) + 1 || 99) - (order.indexOf(b) + 1 || 99) || a.localeCompare(b));
  return { packs: names.map((n) => loadPack(root, n)), base: loadBase(root) };
};
