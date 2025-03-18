// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { Tooltip } from "antd";
import { AnchorButton, AnchorButtonProps } from "@blueprintjs/core";

type Props = {
  testing_status: string;
  is_authenticated: boolean;
};

/**
 * A React component that renders a start/stop button for controlling a testing process.
 * The button's behavior and appearance depend on the testing status and authentication state.
 */
export class StartStopButton extends React.Component<Props> {
  constructor(props: Props) {
    super(props);
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
    this.hardpy_call("api/stop");
  }

  /**
   * Handles the keydown event to start the process when the spacebar is pressed.
   * The process starts only if testing is not in progress and the user is authenticated.
   * @param {KeyboardEvent} event - The keyboard event object.
   * @private
   */
  private readonly hardpy_start_with_space = (event: KeyboardEvent) => {
    const is_testing_in_progress = this.props.testing_status == "run";
    if (
      event.key === " " &&
      !is_testing_in_progress &&
      this.props.is_authenticated
    ) {
      this.hardpy_start();
    }
  };

  /**
   * Handles the button click event to start the process.
   * If the user is not authenticated, it logs a message indicating that authentication is required.
   * @private
   */
  private readonly handleButtonClick = (): void => {
    if (this.props.is_authenticated) {
      this.hardpy_start();
    } else {
      console.log("Authentication required");
    }
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
  }

  /**
   * Renders the Start/Stop button with appropriate properties based on the testing status.
   * @returns {React.ReactNode} The rendered button component.
   */
  render(): React.ReactNode {
    const is_authenticated = this.props.is_authenticated;
    const is_testing_in_progress = this.props.testing_status == "run";

    const intent = is_testing_in_progress ? "danger" : undefined;
    const props: AnchorButtonProps = is_testing_in_progress
      ? {
          text: "Stop",
          intent: "danger",
          large: true,
          rightIcon: "stop",
          onClick: this.hardpy_stop,
          id: "start-stop-button",
        }
      : {
          text: "Start",
          intent: is_authenticated ? "primary" : intent,
          large: true,
          rightIcon: "play",
          onClick: is_authenticated
            ? this.handleButtonClick
            : () => {
                console.log("Authentication required");
              },
          id: "start-stop-button",
        };

    return (
      <Tooltip
        title="It is impossible to connect to the database"
        key="leftButton"
        placement="top"
        trigger="hover"
        open={!is_authenticated}
      >
        <AnchorButton {...props} />
      </Tooltip>
    );
  }
}

export default StartStopButton;
