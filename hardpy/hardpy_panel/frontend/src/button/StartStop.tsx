// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { AnchorButton, AnchorButtonProps } from "@blueprintjs/core";

type Props = { testing_status: string };

type State = {
  isStopButtonDisabled: boolean;
};

/**
 * A React component that renders a start/stop button for controlling a testing process.
 * The button's behavior and appearance depend on the testing status.
 */
export class StartStopButton extends React.Component<Props, State> {
  private stopButtonTimer: NodeJS.Timeout | null = null;

  constructor(props: Props) {
    super(props);
    this.state = {
      isStopButtonDisabled: false
    };
    this.hardpy_start = this.hardpy_start.bind(this);
    this.hardpy_stop = this.hardpy_stop.bind(this);
  }

  /**
   * Makes a fetch call to the specified URI.
   * @param {string} uri - The URI to which the fetch request is made.
   * @private
   */
  private hardpy_call(uri: string) {
    fetch(uri)
      .then((response) => {
        if (response.ok) {
          return response.text();
        } else {
          console.log("Request failed. Status: " + response.status);
        }
      })
      .catch((error) => {
        console.log("Request failed. Error: " + error);
      });
  }

  /**
   * Initiates the start process by making a call to the 'api/start' endpoint.
   * @private
   */
  private hardpy_start(): void {
    this.hardpy_call("api/start");
  }

  /**
   * Initiates the stop process by making a call to the 'api/stop' endpoint.
   * @private
   */
  private hardpy_stop(): void {
    if (this.state.isStopButtonDisabled) {
      return;
    }
    this.hardpy_call("api/stop");

    // Disable the stop button for some time
    this.setState({ isStopButtonDisabled: true });
    this.stopButtonTimer = setTimeout(() => {
      this.setState({ isStopButtonDisabled: false });
  }, 500);
  }

  /**
   * Handles the keydown event to start the process when the spacebar is pressed.
   * The process starts only if testing is not in progress.
   * @param {KeyboardEvent} event - The keyboard event object.
   * @private
   */
  private readonly hardpy_start_with_space = (event: KeyboardEvent) => {
    const is_testing_in_progress = this.props.testing_status == "run";
    if (event.key === " " && !is_testing_in_progress) {
      this.hardpy_start();
    }
  };

  /**
   * Handles the button click event to start the process.
   * @private
   */
  private readonly handleButtonClick = (): void => {
    this.hardpy_start();
  };

  /**
   * Adds an event listener for the keydown event when the component is mounted.
   */
  componentDidMount(): void {
    window.addEventListener("keydown", this.hardpy_start_with_space);
  }

  /**
   * Removes the event listener for the keydown event when the component is unmounted.
   */
  componentWillUnmount(): void {
    window.removeEventListener("keydown", this.hardpy_start_with_space);
    if (this.stopButtonTimer) {
      clearTimeout(this.stopButtonTimer);
    }
  }

  /**
   * Renders the Start/Stop button with appropriate properties based on the testing status.
   * @returns {React.ReactNode} The Start/Stop button component.
   */
  render(): React.ReactNode {
    const is_testing: boolean = this.props.testing_status == "run";
    const button_id: string = "start-stop-button";

    const stop_button: AnchorButtonProps = {
      text: "Stop",
      intent: "danger",
      large: true,
      rightIcon: "stop",
      onClick: this.hardpy_stop,
      id: button_id,
    };

    const start_button: AnchorButtonProps = {
      text: "Start",
      intent: is_testing ? undefined : "primary",
      large: true,
      rightIcon: "play",
      onClick: this.handleButtonClick,
      id: button_id,
      disabled: this.state.isStopButtonDisabled,
    };

    return <AnchorButton {...(is_testing ? stop_button : start_button)} />;
  }
}

export default StartStopButton;
