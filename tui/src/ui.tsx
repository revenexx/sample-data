/** Small drawing helpers: coloured segments, fixed-width rows and boxed panels. */
import type { ReactNode } from "react";
import { Box, Text } from "ink";
import stringWidth from "string-width";
import { theme } from "./theme.ts";

export type Seg = { t: string; color?: string; bg?: string; bold?: boolean; dim?: boolean };

export const seg = (t: string, o: Omit<Seg, "t"> = {}): Seg => ({ t, ...o });
const graphemes = new Intl.Segmenter();

/** Display cells of a string: wide characters (CJK, emoji) count two, combining marks none. */
export const cells = (t: string): number => stringWidth(t);
export const width = (segs: Seg[]): number => segs.reduce((n, s) => n + cells(s.t), 0);

/** The longest start of `t` that fits in `w` cells. */
const cutCells = (t: string, w: number): string => {
  let out = "";
  let used = 0;
  for (const { segment } of graphemes.segment(t)) {
    const c = cells(segment);
    if (used + c > w) break;
    out += segment;
    used += c;
  }
  return out;
};

/** Cut a row to `w` cells. */
export const fit = (segs: Seg[], w: number): Seg[] => {
  const out: Seg[] = [];
  let left = w;
  for (const s of segs) {
    if (left <= 0) break;
    const c = cells(s.t);
    if (c <= left) {
      out.push(s);
      left -= c;
    } else {
      const t = cutCells(s.t, left);
      out.push({ ...s, t });
      left -= cells(t);
      break;
    }
  }
  return out;
};

export const pad = (s: string, w: number): string => {
  const t = cutCells(s, w);
  return t + " ".repeat(w - cells(t));
};

export const padLeft = (s: string, w: number): string => " ".repeat(Math.max(0, w - cells(s))) + s;

const Segs = ({ segs }: { segs: Seg[] }) => (
  <>
    {segs.map((s, i) => (
      <Text key={i} color={s.color} backgroundColor={s.bg} bold={s.bold} dimColor={s.dim}>
        {s.t}
      </Text>
    ))}
  </>
);

/** One row, cut or padded to exactly `w` cells; `bg` fills the padding too. */
export const Line = ({ segs, w, bg }: { segs: Seg[]; w: number; bg?: string }) => {
  const cut = fit(segs, w);
  const gap = Math.max(0, w - width(cut));
  return (
    <Text>
      <Segs segs={cut} />
      {gap > 0 && <Text backgroundColor={bg}>{" ".repeat(gap)}</Text>}
    </Text>
  );
};

const edge = (c: string) => <Text color={theme.accent}>{c}</Text>;

/** A box in the accent colour with its title in the top edge. `rows` are content rows of `w - 2` cells. */
export const Panel = ({ title, rows, w }: { title: string; rows: Seg[][]; w: number }) => {
  const inner = w - 2;
  const head = `┌ ${title} `;
  return (
    <Box flexDirection="column" width={w}>
      <Text color={theme.accent}>
        {head}
        {"─".repeat(Math.max(0, w - cells(head) - 1))}┐
      </Text>
      {rows.map((r, i) => (
        <Text key={i}>
          {edge("│")}
          <Line segs={r} w={inner} />
          {edge("│")}
        </Text>
      ))}
      <Text color={theme.accent}>└{"─".repeat(inner)}┘</Text>
    </Box>
  );
};

export const Badge = ({ children, bg }: { children: ReactNode; bg: string }) => (
  <Text backgroundColor={bg} color={theme.onAccent} bold>
    {children}
  </Text>
);
