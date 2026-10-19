import { existsSync, readFileSync } from "node:fs";
/** Tenant, host and credentials: the same environment variables as lib/load.sh. */
export type Config = {
  baseUrl: string;
  tenant: string;
  apiKey: string;
  token: string;
  /** Where the settings came from, for the header: ".env", "environment" or both. */
  source?: string;
};

export const DEFAULT_BASE_URL = "https://api.revenexx.com/v1";

const KEYS = ["REVENEXX_BASE_URL", "REVENEXX_TENANT", "REVENEXX_API_KEY", "REVENEXX_TOKEN"] as const;

/** Same rules as lib/env.sh: plain KEY=value lines, REVENEXX_* only, comments and one pair of quotes dropped, never evaluated. */
export const parseDotenv = (text: string): Record<string, string> => {
  const out: Record<string, string> = {};
  for (const raw of text.split("\n")) {
    const m = /^\s*(?:export\s+)?(REVENEXX_[A-Z_]*)\s*=(.*)$/.exec(raw.replace(/\r$/, ""));
    if (!m) continue;
    let v = m[2].trim();
    const q = /^(["'])(.*)\1$/.exec(v);
    v = q ? q[2] : v.replace(/\s+#.*$/, "").trim();
    out[m[1]] = v;
  }
  return out;
};

/** Environment plus the repo's .env: a variable that is set in the environment wins. */
export const configFromEnv = (env: NodeJS.ProcessEnv = process.env, dotenvFile?: string): Config => {
  let file: Record<string, string> = {};
  if (dotenvFile && existsSync(dotenvFile)) {
    try {
      file = parseDotenv(readFileSync(dotenvFile, "utf8"));
    } catch {}
  }
  const merged: Record<string, string | undefined> = {};
  const from = new Set<string>();
  for (const k of KEYS) {
    if (env[k] !== undefined) {
      merged[k] = env[k];
      from.add("environment");
    } else if (file[k] !== undefined) {
      merged[k] = file[k];
      from.add(".env");
    }
  }
  return {
    baseUrl: (merged.REVENEXX_BASE_URL || DEFAULT_BASE_URL).replace(/\/+$/, ""),
    tenant: merged.REVENEXX_TENANT ?? "",
    apiKey: merged.REVENEXX_API_KEY ?? "",
    token: merged.REVENEXX_TOKEN ?? "",
    source: from.size === 0 ? undefined : [...from].sort().join(" + "),
  };
};

const parse = (baseUrl: string): URL | null => {
  try {
    return new URL(baseUrl);
  } catch {
    return null;
  }
};

/** "localhost:8080" or "api.revenexx.com": what the header shows after the arrow. */
export const hostOf = (baseUrl: string): string => parse(baseUrl)?.host ?? baseUrl;

/** Local means the machine itself: localhost, 127.x, ::1. Anything else is production. */
export const isLocal = (baseUrl: string): boolean => {
  const host = parse(baseUrl)?.hostname.replace(/^\[|\]$/g, "").toLowerCase();
  if (!host) return false;
  return host === "localhost" || host.endsWith(".localhost") || host === "::1" || /^127(\.\d{1,3}){3}$/.test(host);
};

export const hasCredentials = (cfg: Config): boolean => cfg.apiKey !== "" || cfg.token !== "";

export const authHeaders = (cfg: Config): Record<string, string> => {
  const h: Record<string, string> = { "X-Revenexx-Tenant": cfg.tenant, Accept: "application/json" };
  if (cfg.apiKey) h["X-Revenexx-Api-Key"] = cfg.apiKey;
  if (cfg.token) h.Authorization = `Bearer ${cfg.token}`;
  return h;
};

/** The environment a lib/load.sh / lib/remove.sh child process gets. */
export const childEnv = (cfg: Config, base: NodeJS.ProcessEnv = process.env): NodeJS.ProcessEnv => ({
  ...base,
  REVENEXX_BASE_URL: cfg.baseUrl,
  REVENEXX_TENANT: cfg.tenant,
  REVENEXX_API_KEY: cfg.apiKey,
  REVENEXX_TOKEN: cfg.token,
});
