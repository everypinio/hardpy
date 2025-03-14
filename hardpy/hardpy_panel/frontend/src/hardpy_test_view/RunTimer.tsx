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

export class RunTimer extends React.Component<Props, State> {
  private startTime: number;

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

  private formatMilliseconds(ms: number) {
    return (ms / 1000).toFixed(1);
  }

  render(): React.ReactElement {
    return <div>{this.formatMilliseconds(this.state.elapsedTime)}</div>;
  }

  componentWillUnmount(): void {
    if (this.state.clock) {
      clearInterval(this.state.clock);
    }
  }

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

  private initClock() {
    this.setState({ clock: setInterval(this.updateClock, 100) });
  }
}

export default RunTimer;
