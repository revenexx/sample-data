/**
 * Palette, matching the revenexx CLI's TUI: accents only, body text stays
 * terminal-native. Truecolor hex; chalk downgrades it for Terminal.app (256
 * colours) and drops it when colour is off.
 */
export const theme = {
  accent: "#A090E0",
  success: "#5fd38d",
  warn: "#FFF200",
  danger: "#ff6a55",
  /** Text on an accent / success / warn background. */
  onAccent: "#0b0522",
  /** The empty part of a bar. */
  rest: "#4a4d56",
  /** Background of the row under the cursor: a muted tint, clearly darker than the accent. */
  selection: "#2E2A45",
  gradient: [
    [0x62, 0x0d, 0xff],
    [0x89, 0x77, 0xcd],
    [0xa0, 0x90, 0xe0],
  ] as const,
};

const hex = (n: number): string => Math.round(n).toString(16).padStart(2, "0");

/** One colour per glyph across the brand gradient (same ramp as the CLI). */
export const gradientColors = (length: number): string[] => {
  const stops = theme.gradient;
  if (length <= 0) return [];
  const spans = stops.length - 1;
  return Array.from({ length }, (_, i) => {
    const t = length === 1 ? 0 : (i / (length - 1)) * spans;
    const lo = Math.min(Math.floor(t), spans - 1);
    const f = t - lo;
    const [r1, g1, b1] = stops[lo];
    const [r2, g2, b2] = stops[lo + 1];
    return `#${hex(r1 + (r2 - r1) * f)}${hex(g1 + (g2 - g1) * f)}${hex(b1 + (b2 - b1) * f)}`;
  });
};
