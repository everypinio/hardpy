// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";

import { cn } from "@/lib/utils";
import { statusPresentation, toDisplayStatus } from "@/lib/testStatus";

interface Props {
  status: string;
  className?: string;
}

/**
 * Renders the icon standing for a test run or test case status.
 *
 * @param {Object} props - The component props.
 * @param {string} props.status - The raw status reported by the backend.
 * @param {string} [props.className] - Extra classes for the icon.
 * @returns {React.ReactElement} A React element representing the status icon.
 */
export function TestStatus(props: Readonly<Props>): React.ReactElement {
  const status = toDisplayStatus(props.status);
  const { icon: Icon, iconClassName } = statusPresentation(status);

  return (
    <Icon
      data-status={status}
      aria-hidden="true"
      className={cn("size-4 shrink-0", iconClassName, props.className)}
    />
  );
}

export default TestStatus;
