// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { Intent, ProgressBar } from "@blueprintjs/core";
type Props = {
  percentage: number;
  status: string;
};

export class ProgressView extends React.Component<Props> {
  render(): React.ReactElement {
    const intent = (status: string) => {
      switch (status) {
        case "run":
          return Intent.PRIMARY;
        case "failed":
          return Intent.DANGER;
        case "passed":
          return Intent.SUCCESS;
        default:
          return Intent.NONE;
      }
    };
    return (
      <ProgressBar
        intent={intent(this.props.status)}
        value={this.props.percentage / 100}
        animate={this.props.percentage / 100 < 1 && this.props.status == "run"}
      />
    );
  }
}

export default ProgressView;
