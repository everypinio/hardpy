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
