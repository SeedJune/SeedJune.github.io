/**
 * Formats a "YYYY-MM" string as e.g. "Sep 2023".
 *
 * Anything that is not a well-formed YYYY-MM is returned untouched — that way
 * the literal `YYYY-MM` placeholders in src/data/site.ts show up on the page
 * as themselves instead of as "Invalid Date", which makes them easy to spot
 * and impossible to miss.
 */
export function formatMonth(value: string): string {
  const match = /^(\d{4})-(\d{2})$/.exec(value);
  if (!match) return value;

  const year = Number(match[1]);
  const month = Number(match[2]);
  if (month < 1 || month > 12) return value;

  return new Date(year, month - 1, 1).toLocaleDateString('en-US', {
    month: 'short',
    year: 'numeric',
  });
}

/** Formats a start/end pair as "Sep 2023 — Present". */
export function formatRange(
  start: string,
  end?: string | null,
  current?: boolean,
): string {
  const from = formatMonth(start);
  const to = current || !end ? 'Present' : formatMonth(end);
  return `${from} — ${to}`;
}

/** Formats a Date from collection frontmatter as e.g. "8 Nov 2025". */
export function formatDay(date: Date): string {
  return date.toLocaleDateString('en-US', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });
}

/** ISO yyyy-mm-dd, for <time datetime="…">. */
export function isoDay(date: Date): string {
  return date.toISOString().slice(0, 10);
}
