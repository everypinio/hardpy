// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { AnchorButton, AnchorButtonProps } from "@blueprintjs/core";
import { withTranslation, WithTranslation } from "react-i18next";

type Props = { testing_status: string } & WithTranslation;

type State = {
  isStopButtonDisabled: boolean;
};

/**
 * A React component that renders a start/stop button for controlling a testing process.
 * The button's behavior and appearance depend on the testing status.
 */
class StartStopButton extends React.Component<Props, State> {
  private stopButtonTimer: NodeJS.Timeout | null = null;

  constructor(props: Props) {
    super(props);
    this.state = {
      isStopButtonDisabled: false,
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
          console.log(
            this.props.t("error.requestFailed", { status: response.status })
          );
        }
      })
      .catch((error) => {
        console.log(this.props.t("error.requestError", { error }));
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
   * Checks if any dialog is currently open.
   * @returns {boolean} True if a dialog is open, else false.
   */
  private isDialogOpen(): boolean {
    const blueprintDialogs = document.querySelectorAll('.bp3-dialog');
    for (const dialog of blueprintDialogs) {
      const style = window.getComputedStyle(dialog);
      if (style.display !== 'none' && style.visibility !== 'hidden') {
        return true;
      }
    }

    const ariaDialogs = document.querySelectorAll('[role="dialog"]');
    for (const dialog of ariaDialogs) {
      const style = window.getComputedStyle(dialog);
      if (style.display !== 'none' && style.visibility !== 'hidden') {
        return true;
      }
    }

    return false;
  }

  /**
   * Handles the space keydown event to start or stop the process.
   */
  private readonly handleSpaceKey = (event: KeyboardEvent) => {
    if (this.isDialogOpen()) {
      return;
    }

    const target = event.target as HTMLElement;
    if (!target) return;

    const interactiveElements = ['INPUT', 'TEXTAREA', 'SELECT', 'BUTTON'];
    if (
      interactiveElements.includes(target.tagName) || 
      target.isContentEditable
    ) {
      return;
    }

    if (event.key === " ") {
      event.preventDefault();
      const is_testing_in_progress = this.props.testing_status == "run";
      is_testing_in_progress ? this.hardpy_stop() : this.hardpy_start();
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
    window.addEventListener("keydown", this.handleSpaceKey);
  }

  /**
   * Removes the event listener for the keydown event when the component is unmounted.
   */
  componentWillUnmount(): void {
    window.removeEventListener("keydown", this.handleSpaceKey);
    if (this.stopButtonTimer) {
      clearTimeout(this.stopButtonTimer);
    }
  }

  /**
   * Renders the Start/Stop button with appropriate properties based on the testing status.
   * @returns {React.ReactNode} The Start/Stop button component.
   */
  render(): React.ReactNode {
    const { t, testing_status } = this.props;
    const is_testing: boolean = testing_status == "run";
    const button_id: string = "start-stop-button";

    const stop_button: AnchorButtonProps = {
      text: t("button.stop"),
      intent: "danger",
      large: true,
      rightIcon: "stop",
      onClick: this.hardpy_stop,
      id: button_id,
      fill: true,
      style: { width: "100%", height: "96px", fontSize: "16px" },
    };

    const start_button: AnchorButtonProps = {
      text: t("button.start"),
      intent: is_testing ? undefined : "primary",
      large: true,
      rightIcon: "play",
      onClick: this.handleButtonClick,
      id: button_id,
      disabled: this.state.isStopButtonDisabled,
      fill: true,
      style: { width: "100%", height: "96px", fontSize: "16px" },
    };

    return <AnchorButton {...(is_testing ? stop_button : start_button)} />;
  }
}

export default withTranslation()(StartStopButton);
