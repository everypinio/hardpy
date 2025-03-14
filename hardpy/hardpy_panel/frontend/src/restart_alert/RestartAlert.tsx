// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { Alert } from "@blueprintjs/core";

interface Props {
  reload_timeout_s: number;
}

type States = "BEFORE_RELOAD" | "WAIT_RELOAD" | "RELOAD";
type Action = "RELOAD_START" | "RELOAD";

function reducer(_state: States, action: Action): States {
  switch (action) {
    case "RELOAD_START":
      return "WAIT_RELOAD";
    case "RELOAD":
      return "RELOAD";
    default:
      throw new Error();
  }
}

const RELOAD_MSG = (time_ms: number) =>
  `The application will be updated in ${time_ms} seconds!`;

/**
 * Render alert about app restart (page update) and restart page after
 */
export function ReloadAlert(props: Props): React.ReactElement {
  /** States */
  const [state, dispatch] = React.useReducer(reducer, "BEFORE_RELOAD");

  /** Effects */
  // Handle states of restart alert
  React.useEffect(() => {
    switch (state) {
      case "WAIT_RELOAD":
        setTimeout(() => {
          dispatch("RELOAD");
        }, props.reload_timeout_s * 1000);
        return;
      case "RELOAD":
        window.location.reload(); // reload window
        return;
      default:
        return;
    }
  }, [state, props.reload_timeout_s]);

  /** Render */
  return (
    <Alert
      isOpen={state == "WAIT_RELOAD"}
      confirmButtonText={"Reboot now"}
      onClose={() => dispatch("RELOAD")}
      icon={"warning-sign"}
    >
      <p>{RELOAD_MSG(props.reload_timeout_s)}</p>
    </Alert>
  );
}

export default ReloadAlert;
