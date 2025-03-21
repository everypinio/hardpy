// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { Intent, ProgressBar } from "@blueprintjs/core";

/**
 * Props for the ProgressView component.
 * @typedef {Object} Props
 * @property {number} percentage - The progress percentage (0 to 100).
 * @property {string} status - The status of the progress, which can be "run", "failed", or "passed".
 */
type Props = {
  percentage: number;
  status: string;
};

/**
 * A React component that displays a progress bar with different intents based on the status.
 * @class ProgressView
 * @extends {React.Component<Props>}
 */
export class ProgressView extends React.Component<Props> {
  /**
   * Renders the ProgressView component.
   * @returns {React.ReactElement} The rendered progress bar.
   */
  render(): React.ReactElement {
    /**
     * Determines the intent of the progress bar based on the status.
     * @param {string} status - The status of the progress.
     * @returns {Intent} The intent corresponding to the status.
     */
    const intent = (status: string): Intent => {
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
