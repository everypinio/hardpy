// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { Icon, Spinner } from "@blueprintjs/core";

interface Props {
  status: string;
}

export function TestStatus(props: Props): React.ReactElement {
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
