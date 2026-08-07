// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

/**
 * Colour utilities for the healthy and degraded states, which the shadcn token
 * set does not cover: it only ships `primary`, `muted` and `destructive`.
 * Kept on the stock Tailwind palette so no extra theme token is needed.
 */
export const STATUS_COLORS = {
  ok: {
    text: "text-emerald-600 dark:text-emerald-400",
    fill: "bg-emerald-600",
  },
  warning: {
    text: "text-amber-600 dark:text-amber-400",
    fill: "bg-amber-500",
  },
} as const;
