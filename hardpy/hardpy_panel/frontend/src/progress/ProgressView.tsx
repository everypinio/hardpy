// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";

import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";
import { isRunInFlight, statusPresentation, toDisplayStatus } from "@/lib/testStatus";

const FULL_PERCENTAGE = 100;

/**
 * Props for the ProgressView component.
 * @typedef {Object} Props
 * @property {number} percentage - The progress percentage (0 to 100).
 * @property {string} status - The raw run status reported by the backend.
 */
type Props = {
  percentage: number;
  status: string;
};

/**
 * Displays the run progress, coloured after the run status and striped while
 * the run is still in flight.
 * @param {Props} props - The component props.
 * @returns {React.ReactElement} The rendered progress bar.
 */
export function ProgressView(props: Readonly<Props>): React.ReactElement {
  const status = toDisplayStatus(props.status);
  const { fillClassName } = statusPresentation(status);
  const isAnimated =
    isRunInFlight(status) && props.percentage < FULL_PERCENTAGE;

  return (
    <Progress
      value={props.percentage}
      aria-label={status}
      className="h-2.5 bg-muted"
      indicatorClassName={cn(
        "rounded-full",
        fillClassName,
        isAnimated && "progress-stripes"
      )}
    />
  );
}

export default ProgressView;
