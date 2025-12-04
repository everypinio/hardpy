// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { Icon, Spinner } from "@blueprintjs/core";

interface Props {
  status: string;
}

/**
 * Renders a status icon or spinner based on the provided status.
 *
 * @param {Object} props - The component props.
 * @param {string} props.status - The status to display. Possible values: "ready", "run", "passed", "failed", "", or any other value.
 * @returns {React.ReactElement} - A React element representing the status icon or spinner.
 */
export function TestStatus(props: Readonly<Props>): React.ReactElement {
  switch (props.status) {
    case "ready":
      return (
        <Icon
          icon="time"
          intent="success"
          className="status-icon status-icon-wait"
        />
      );
    case "run":
      return (
        <div
          style={{ marginTop: "4px" }}
          className="status-icon status-icon-run"
        >
          {" "}
          <Spinner size={15} />
        </div>
      );
    case "passed":
      return (
        <Icon
          icon="tick-circle"
          intent="success"
          className="status-icon status-icon-success"
        />
      );
    case "failed":
      return (
        <Icon
          icon="cross"
          intent="danger"
          className="status-icon status-icon-fail"
        />
      );
    case "skipped":
      return (
        <Icon
          icon="disable"
          intent="warning"
          className="status-icon status-icon-skipped"
        />
      );
    case "":
      return (
        <Icon
          icon="time"
          intent="none"
          className="status-icon status-icon-wait"
        />
      );
    default:
      return (
        <Icon
          icon="circle"
          intent="none"
          className="status-icon status-icon-empty"
        />
      );
  }
}

TestStatus.defaultProps = {
  defaultOpen: true,
};

export default TestStatus;
