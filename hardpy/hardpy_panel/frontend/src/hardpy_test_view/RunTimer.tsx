// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";

type Props = {
  commonTestRunStatus: string | undefined;
  status: string;
};

type State = {
  elapsedTime: number;
  clock: NodeJS.Timeout | null;
};

/**
 * A React component that displays the elapsed time since the timer started.
 * The timer starts when the component is mounted and the status is "run".
 */
export class RunTimer extends React.Component<Props, State> {
  private startTime: number;

  /**
   * Constructs the RunTimer component.
   * @param {Props} props - The props passed to the component.
   */
  constructor(props: Props) {
    super(props);

    const now = new Date();
    this.startTime = now.getTime();

    this.state = {
      elapsedTime: 0,
      clock: null,
    };

    this.initClock = this.initClock.bind(this);
    this.updateClock = this.updateClock.bind(this);

    if ("run" == this.props.status) {
      this.setState({ elapsedTime: 0 });
      this.initClock();
    }
  }

  /**
   * Formats the given milliseconds into seconds with one decimal place.
   * @param {number} ms - The time in milliseconds.
   * @returns {string} The formatted time in seconds.
   */
  private formatMilliseconds(ms: number) {
    return (ms / 1000).toFixed(1);
  }

  /**
   * Renders the component, displaying the elapsed time.
   * @returns {React.ReactElement} The rendered component.
   */
  render(): React.ReactElement {
    return <div>{this.formatMilliseconds(this.state.elapsedTime)}</div>;
  }

  /**
   * Cleans up the interval when the component is unmounted.
   */
  componentWillUnmount(): void {
    if (this.state.clock) {
      clearInterval(this.state.clock);
    }
  }

  /**
   * Updates the elapsed time if the status is "run" and the commonTestRunStatus is "run".
   * Otherwise, it clears the interval.
   */
  private updateClock() {
    const now = new Date();

    if (this.props.status == "run" && this.props.commonTestRunStatus == "run") {
      this.setState({ elapsedTime: now.getTime() - this.startTime });
    } else {
      if (this.state.clock) {
        clearInterval(this.state.clock);
      }
    }
  }

  /**
   * Initializes the clock by setting up an interval to update the elapsed time every 100ms.
   */
  private initClock() {
    this.setState({ clock: setInterval(this.updateClock, 100) });
  }
}

export default RunTimer;
