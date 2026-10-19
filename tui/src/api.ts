/**
 * Live counts: how much of each pack is in the shop right now. Read-only.
 * The list routes filter by exact value only (no prefix), so a pack's records
 * are found through what the pack owns: its manufacturers (products), its
 * storage folder (files), its price lists, and its SKUs among the stock rows.
 */
import { authHeaders, type Config } from "./config.ts";
import type { Counts } from "./counts.ts";
import type { BaseTarget, PackTarget } from "./plan.ts";

export type Fetch = typeof fetch;

export class ApiError extends Error {
  constructor(message: string, readonly status = 0) {
    super(message);
  }
}

/** At most this many requests in flight at once; the first read of a pack used to send dozens together. */
const MAX_IN_FLIGHT = 3;
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

const items = (b: any): any[] => b?.items ?? b?.data ?? (Array.isArray(b) ? b : []);

export class ShopReader {
  private ids = new Map<string, string>();
  private inFlight = 0;
  private waiting: Array<() => void> = [];
  /** Set when the API answered 429 (a retry may have succeeded); the app shows one calm note and polls slower. */
  rateLimitedAt: number | null = null;
  constructor(
    readonly cfg: Config,
    private readonly doFetch: Fetch = fetch,
    private readonly backoffMs: number = 1000,
  ) {}

  private async slot<T>(fn: () => Promise<T>): Promise<T> {
    if (this.inFlight >= MAX_IN_FLIGHT) await new Promise<void>((r) => this.waiting.push(r));
    this.inFlight++;
    try {
      return await fn();
    } finally {
      this.inFlight--;
      this.waiting.shift()?.();
    }
  }

  /** Fetch with a quiet back-off: a 429 waits (Retry-After, else 1 s, 2 s, 4 s) and tries again, up to 3 times. */
  private async fetchQuiet(path: string): Promise<Response> {
    for (let attempt = 0; ; attempt++) {
      const res = await this.slot(() =>
        this.doFetch(this.cfg.baseUrl + path, { headers: authHeaders(this.cfg), signal: AbortSignal.timeout(15000) }),
      );
      if (res.status !== 429) return res;
      this.rateLimitedAt = Date.now();
      if (attempt >= 3) return res;
      const ra = Number(res.headers.get("retry-after"));
      await sleep(ra > 0 ? Math.min(ra, 30) * 1000 : this.backoffMs * 2 ** attempt);
    }
  }

  async get(path: string): Promise<any> {
    let res: Response;
    try {
      res = await this.fetchQuiet(path);
    } catch (e: any) {
      throw new ApiError(`${new URL(this.cfg.baseUrl).host} not reachable: ${e?.cause?.code ?? e?.message ?? e}`);
    }
    if (!res.ok) {
      let msg = "";
      try {
        const b: any = await res.json();
        msg = b?.message ?? b?.error?.message ?? "";
      } catch {}
      throw new ApiError(`${path.split("?")[0]} answered ${res.status}${msg ? `: ${String(msg).slice(0, 120)}` : ""}`, res.status);
    }
    return res.json();
  }

  /** Id of the record with this exact code, cached for the life of the reader. */
  private async idOf(route: string, key: string, value: string): Promise<string | null> {
    const k = `${route}|${key}|${value}`;
    const hit = this.ids.get(k);
    if (hit) return hit;
    const id = items(await this.get(`${route}?${key}=${encodeURIComponent(value)}&limit=2`))[0]?.id ?? null;
    if (id) this.ids.set(k, id);
    return id;
  }

  /**
   * Total of a list under a cached parent id; a parent that is gone (removed since) counts zero.
   * A filter by a gone id answers 200 with total 0, not 404, so an empty answer also drops the
   * cached id: a remove and a new load give the parent a new id, and the next read finds it.
   */
  private async totalUnder(route: string, key: string, code: string, child: (id: string) => string): Promise<number> {
    const id = await this.idOf(route, key, code);
    if (!id) return 0;
    try {
      const b = await this.get(child(id));
      const total = b?.page?.total ?? items(b).length;
      if (total === 0) this.ids.delete(`${route}|${key}|${code}`);
      return total;
    } catch (e) {
      if (e instanceof ApiError && e.status === 404) {
        this.ids.delete(`${route}|${key}|${code}`);
        return 0;
      }
      throw e;
    }
  }

  async products(pack: PackTarget): Promise<number> {
    const counts = await Promise.all(
      pack.manufacturers.map((code) =>
        this.totalUnder("/products/manufacturers", "code", code, (id) => `/products?manufacturer_id=${id}&limit=1`),
      ),
    );
    return counts.reduce((a, b) => a + b, 0);
  }

  /** Files of the pack's storage folder whose name is one of the pack's files. */
  async assets(pack: PackTarget): Promise<number> {
    const folders = items(await this.get("/storage/folders"));
    const folder = folders.find((f: any) => f.path === `/${pack.folder}/`);
    if (!folder) return 0;
    const names = new Set(pack.assetNames);
    let n = 0;
    for (let page = 1; ; page++) {
      const b = await this.get(`/storage/assets?filter%5Bfolder_id%5D=${folder.id}&limit=200&sort=original_name&page=${page}`);
      for (const a of items(b)) if (names.has(a.original_name)) n++;
      if (page >= (b?.meta?.last_page ?? 1)) break;
    }
    return n;
  }

  /** One field of every record of a list, read once and shared by all packs of a refresh. */
  async allOf(route: string, field: string): Promise<Set<string>> {
    const out = new Set<string>();
    for (let offset = 0; ; offset += 200) {
      const b = await this.get(`${route}?limit=200&offset=${offset}`);
      for (const r of items(b)) out.add(String(r[field]));
      if (!b?.page?.hasMore) break;
    }
    return out;
  }

  /** Every stock row, once: shared by all packs of a refresh. */
  stockSkus(): Promise<Set<string>> {
    return this.allOf("/inventories/stock", "sku");
  }

  async prices(pack: PackTarget): Promise<number> {
    const counts = await Promise.all(
      pack.priceLists.map((code) => this.totalUnder("/prices/lists", "code", code, (id) => `/prices/lists/${id}/entries?limit=1`)),
    );
    return counts.reduce((a, b) => a + b, 0);
  }

  /** The base's records that exist, per column and in total, against each column's target. */
  async base(base: BaseTarget): Promise<{ found: number; total: number; cols: number[] }> {
    const cols = await Promise.all(
      base.checks.map(async (c) => {
        const per = await Promise.all(
          c.parts.flatMap((p) =>
            p.values.map(async (v) => {
              const b = await this.get(`${p.route}?${p.key}=${encodeURIComponent(v)}&limit=1`);
              const hit = items(b)[0];
              if (!hit) return 0;
              if (!p.tiers) return 1;
              try {
                return 1 + (items(await this.get(`${p.route}/${hit.id}/tiers?limit=1`)).length > 0 ? 1 : 0);
              } catch {
                return 1;
              }
            }),
          ),
        );
        return Math.min(per.reduce((a, b) => a + b, 0), c.target);
      }),
    );
    return { found: cols.reduce((a, b) => a + b, 0), total: base.checks.reduce((a, c) => a + c.target, 0), cols };
  }
}

/** The counts of the given packs (one shared read of each list: stock, categories, attributes, makers, price lists). */
export const readCounts = async (reader: ShopReader, packs: PackTarget[]): Promise<Record<string, Counts>> => {
  const [stock, categories, attributes, makers, lists] = await Promise.all([
    reader.stockSkus(),
    reader.allOf("/products/categories", "code"),
    reader.allOf("/products/attributes", "code"),
    reader.allOf("/products/manufacturers", "code"),
    reader.allOf("/prices/lists", "code"),
  ]);
  const among = (codes: string[], have: Set<string>) => codes.filter((c) => have.has(c)).length;
  const rows = await Promise.all(
    packs.map(async (p) => {
      const [products, assets, prices] = await Promise.all([reader.products(p), reader.assets(p), reader.prices(p)]);
      const counts: Counts = {
        products,
        categories: among(p.categoryCodes, categories),
        attributes: among(p.attributeCodes, attributes),
        makers: among(p.manufacturers, makers),
        assets,
        lists: among(p.priceLists, lists),
        prices,
        stock: among(p.stockSkus, stock),
      };
      return [p.name, counts] as const;
    }),
  );
  return Object.fromEntries(rows);
};
