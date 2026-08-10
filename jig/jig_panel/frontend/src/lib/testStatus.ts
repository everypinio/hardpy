// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import type { TFunction } from "i18next";
import {
  Ban,
  Circle,
  CircleCheck,
  CircleX,
  Clock,
  LoaderCircle,
  OctagonX,
  type LucideIcon,
} from "lucide-react";

import { STATUS_COLORS } from "@/lib/statusColors";

/** Statuses the backend reports for a test run or a single test case. */
export const RUN_STATUSES = [
  "ready",
  "run",
  "passed",
  "failed",
  "stopped",
  "skipped",
] as const;

export type RunStatus = (typeof RUN_STATUSES)[number];

/**
 * A status ready to be rendered. Beyond the statuses the backend reports, it
 * covers a case that has not started yet ("pending") and a value the backend
 * sent that this frontend does not know ("unknown").
 */
export type DisplayStatus = RunStatus | "pending" | "unknown";

/** Everything the UI needs to render a status, in one place. */
interface StatusPresentation {
  icon: LucideIcon;
  /** Translation key of the human readable status, absent when there is none. */
  labelKey?: string;
  /** Utility colouring the status icon. */
  iconClassName: string;
  /** Utility filling a surface with the status colour, e.g. the progress bar. */
  fillClassName: string;
}

const STATUS_PRESENTATIONS: Record<DisplayStatus, StatusPresentation> = {
  ready: {
    icon: Clock,
    labelKey: "app.status.ready",
    iconClassName: STATUS_COLORS.ok.text,
    fillClassName: "bg-muted-foreground/40",
  },
  run: {
    icon: LoaderCircle,
    labelKey: "app.status.run",
    iconClassName: "text-primary animate-spin",
    fillClassName: "bg-primary",
  },
  passed: {
    icon: CircleCheck,
    labelKey: "app.status.passed",
    iconClassName: STATUS_COLORS.ok.text,
    fillClassName: STATUS_COLORS.ok.fill,
  },
  failed: {
    icon: CircleX,
    labelKey: "app.status.failed",
    iconClassName: "text-destructive",
    fillClassName: "bg-destructive",
  },
  stopped: {
    icon: OctagonX,
    labelKey: "app.status.stopped",
    iconClassName: STATUS_COLORS.warning.text,
    fillClassName: STATUS_COLORS.warning.fill,
  },
  skipped: {
    icon: Ban,
    labelKey: "testSuite.skipped",
    iconClassName: STATUS_COLORS.warning.text,
    fillClassName: STATUS_COLORS.warning.fill,
  },
  pending: {
    icon: Clock,
    iconClassName: "text-muted-foreground",
    fillClassName: "bg-muted-foreground/40",
  },
  unknown: {
    icon: Circle,
    labelKey: "app.status.unknown",
    iconClassName: "text-muted-foreground",
    fillClassName: "bg-muted-foreground/40",
  },
};

const isRunStatus = (status: string): status is RunStatus =>
  (RUN_STATUSES as readonly string[]).includes(status);

/**
 * Narrows a raw status coming from the database to a renderable status.
 * @param {string | undefined} status - The raw status value.
 * @returns {DisplayStatus} The matching known status, "pending" when empty,
 * "unknown" when the value is not recognized.
 */
export function toDisplayStatus(status: string | undefined): DisplayStatus {
  if (!status) {
    return "pending";
  }
  return isRunStatus(status) ? status : "unknown";
}

/**
 * Looks up how a status should be presented.
 * @param {DisplayStatus} status - The status to present.
 * @returns {StatusPresentation} Icon, label key and colour utilities.
 */
export function statusPresentation(status: DisplayStatus): StatusPresentation {
  return STATUS_PRESENTATIONS[status];
}

/**
 * Translates a status into the text shown to the operator.
 * @param {DisplayStatus} status - The status to translate.
 * @param {TFunction} t - The i18next translation function.
 * @returns {string} The translated status, empty when the status has no label.
 */
export function statusLabel(status: DisplayStatus, t: TFunction): string {
  const { labelKey } = STATUS_PRESENTATIONS[status];
  return labelKey ? t(labelKey) : "";
}

/**
 * Tells whether a run is currently executing.
 * @param {DisplayStatus} status - The status to check.
 * @returns {boolean} True while the run is in flight.
 */
export function isRunInFlight(status: DisplayStatus): boolean {
  return status === "run";
}

/**
 * Status of a module or a case the run left behind while executing it, which
 * this frontend does not know and therefore renders as "unknown".
 */
const STUCK_STATUS = "stucked";

/**
 * Narrows the status of a module or a case to what the operator should see.
 *
 * A node still marked as running once the run is over never reported its
 * outcome, so it is shown as stuck. A node left at "ready" simply was not part
 * of the run, for instance during a partial run, and keeps its status.
 * @param {string} status - The raw node status from the database.
 * @param {string | undefined} runStatus - The raw status of the whole run.
 * @returns {string} The status to render.
 */
export function toNodeDisplayStatus(
  status: string,
  runStatus: string | undefined,
): string {
  const isRunOver = !isRunInFlight(toDisplayStatus(runStatus));
  return isRunOver && status === "run" ? STUCK_STATUS : status;
}

/**
 * Status priority for aggregating several statuses into one.
 * Higher index wins. "run" is highest so an in-flight child keeps the
 * section animated; "failed" beats every settled status; "ready" beats
 * "passed" so a section holding a test that has not run yet stays neutral
 * instead of claiming success.
 */
const AGGREGATE_PRIORITY: DisplayStatus[] = [
  "pending",
  "passed",
  "ready",
  "skipped",
  "stopped",
  "unknown",
  "failed",
  "run",
];

/**
 * Aggregates several statuses into a single display status.
 * Empty input yields "pending".
 * @param {readonly string[]} statuses - Raw status strings from modules/cases.
 * @returns {DisplayStatus} The highest-priority status among the inputs.
 */
export function aggregateStatus(statuses: readonly string[]): DisplayStatus {
  if (statuses.length === 0) {
    return "pending";
  }
  let best: DisplayStatus = "pending";
  let bestRank = -1;
  for (const raw of statuses) {
    const display = toDisplayStatus(raw);
    const rank = AGGREGATE_PRIORITY.indexOf(display);
    if (rank > bestRank) {
      best = display;
      bestRank = rank;
    }
  }
  return best;
}
