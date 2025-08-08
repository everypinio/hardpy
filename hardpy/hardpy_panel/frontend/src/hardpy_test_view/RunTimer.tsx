// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";

const CLOCK_UPDATE_INTERVAL = 100;
const MILLISECONDS_TO_SECONDS = 1000;

type Props = {
  commonTestRunStatus: string | undefined;
  status: string;
  start_time?: number;
  stop_time?: number;
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
  /**
   * Constructs the RunTimer component.
   * @param {Props} props - The props passed to the component.
   */
  constructor(props: Props) {
    super(props);

    this.state = {
      elapsedTime: this.calculateElapsedTime(),
      clock: null,
    };

    this.initClock = this.initClock.bind(this);
    this.updateClock = this.updateClock.bind(this);
    this.calculateElapsedTime = this.calculateElapsedTime.bind(this);
    this.stopClock = this.stopClock.bind(this);
  }

  private calculateElapsedTime(): number {
    const { status, start_time, stop_time } = this.props;

    if (
      status !== "run" &&
      start_time &&
      stop_time &&
      stop_time >= start_time
    ) {
      return stop_time - start_time;
    }
    if (status === "run" && start_time) {
      return Date.now() / 1000 - start_time;
    }

    return 0;
  }

  /**
   * Formats the time in seconds to one decimal place.
   * @param {number} seconds - The time in seconds.
   * @returns {string} The formatted time in seconds.
   */
  private formatSeconds(seconds: number): string {
    return Math.floor(seconds).toString();
  }

  /**
   * Cleans up the interval when the component is unmounted.
   */
  componentWillUnmount(): void {
    this.stopClock();
  }

  componentDidMount() {
    if (this.props.status === "run") {
      this.initClock();
    }
  }

  componentDidUpdate(prevProps: Props) {
    // Handle status changes
    if (this.props.status !== prevProps.status) {
      if (this.props.status === "run") {
        this.setState({ elapsedTime: this.calculateElapsedTime() });
        this.initClock();
      } else if (prevProps.status === "run") {
        this.stopClock();
        this.setState({ elapsedTime: this.calculateElapsedTime() });
      }
    }

    // Handle time changes
    if (
      this.props.start_time !== prevProps.start_time ||
      this.props.stop_time !== prevProps.stop_time
    ) {
      this.setState({ elapsedTime: this.calculateElapsedTime() });
    }
  }

  private stopClock() {
    if (this.state.clock) {
      clearInterval(this.state.clock);
      this.setState({ clock: null });
    }
  }

  /**
   * Updates the elapsed time if the status is "run" and the commonTestRunStatus is "run".
   */
  private updateClock() {
    if (
      this.props.status === "run" &&
      this.props.commonTestRunStatus === "run"
    ) {
      this.setState({ elapsedTime: this.calculateElapsedTime() });
    }
  }

  /**
   * Initializes the clock by setting up an interval to update the elapsed time every 100ms.
   */
  private initClock() {
    this.stopClock();
    this.setState({
      clock: setInterval(this.updateClock, CLOCK_UPDATE_INTERVAL),
    });
  }

  render(): React.ReactElement {
    return <div>{this.formatSeconds(this.state.elapsedTime)}</div>;
  }
}

export default RunTimer;
