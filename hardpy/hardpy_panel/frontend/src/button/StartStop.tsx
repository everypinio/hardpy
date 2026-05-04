// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { AnchorButton, AnchorButtonProps } from "@blueprintjs/core";
import { withTranslation, WithTranslation } from "react-i18next";

type Props = {
  testing_status: string;
  useBigButton?: boolean;
  manualCollectMode?: boolean;
  onTestRunStart?: () => void;
} & WithTranslation;

type State = {
  isStopButtonDisabled: boolean;
};

// Global variables for ModalResult state
declare let isCompletionModalResultVisible: boolean;
declare let lastModalResultDismissTime: number;
declare const MODAL_RESULT_DISMISS_COOLDOWN: number;

/**
 * A React component that renders a start/stop button for controlling a testing process.
 * The button's behavior and appearance depend on the testing status.
 * Handles space key events for keyboard control and prevents actions during modal display.
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
  private hardpy_call(uri: string): void {
    fetch(uri).then((response) => {
      if (response.ok) {
        return response.text();
      }
    });
  }

  /**
   * Initiates the start process by making a call to the 'api/start' endpoint.
   * @private
   */
  private hardpy_start(): void {
    if (this.props.manualCollectMode) {
      return;
    }

    if (this.props.onTestRunStart) {
      this.props.onTestRunStart();
    }

    this.hardpy_call("api/start");
  }

  /**
   * Initiates the stop process by making a call to the 'api/stop' endpoint.
   * Temporarily disables the stop button to prevent multiple rapid clicks.
   * @private
   */
  private hardpy_stop(): void {
    if (this.props.manualCollectMode) {
      return;
    }

    if (this.state.isStopButtonDisabled) {
      return;
    }
    this.hardpy_call("api/stop");

    // Disable the stop button for some time to prevent multiple rapid clicks
    this.setState({ isStopButtonDisabled: true });
    this.stopButtonTimer = setTimeout(() => {
      this.setState({ isStopButtonDisabled: false });
    }, 500);
  }
  /**
   * Checks if any dialog is currently open in the application.
   * Searches for both Blueprint.js dialogs and standard ARIA dialogs.
   * @returns {boolean} True if a dialog is open and visible, false otherwise.
   */
  private isDialogOpen(): boolean {
    const blueprintDialogs = document.querySelectorAll(".bp3-dialog");
    for (const dialog of blueprintDialogs) {
      const style = window.getComputedStyle(dialog);
      if (style.display !== "none" && style.visibility !== "hidden") {
        return true;
      }
    }

    const ariaDialogs = document.querySelectorAll('[role="dialog"]');
    for (const dialog of ariaDialogs) {
      const style = window.getComputedStyle(dialog);
      if (style.display !== "none" && style.visibility !== "hidden") {
        return true;
      }
    }

    return false;
  }

  /**
   * Checks if the completion ModalResult is currently visible.
   * First attempts to use the global variable, falls back to DOM inspection.
   * @returns {boolean} True if the completion ModalResult is visible, false otherwise.
   */
  private isCompletionModalResultVisible(): boolean {
    try {
      if (typeof isCompletionModalResultVisible !== "undefined") {
        return isCompletionModalResultVisible;
      }
    } catch (error) {
      console.warn(
        "StartStopButton: Could not access global ModalResult visibility variable"
      );
    }

    // Fallback: check if ModalResult element exists in DOM by z-index
    const ModalResultElements = document.querySelectorAll(
      '[style*="z-index: 9999"]'
    );
    return ModalResultElements.length > 0;
  }

  /**
   * Checks if the application is in the cooldown period after ModalResult dismissal.
   * Prevents immediate space key actions after the ModalResult is dismissed.
   * @returns {boolean} True if within the cooldown period, false otherwise.
   */
  private isInModalResultDismissCooldown(): boolean {
    try {
      if (
        typeof lastModalResultDismissTime !== "undefined" &&
        typeof MODAL_RESULT_DISMISS_COOLDOWN !== "undefined"
      ) {
        const now = Date.now();
        return now - lastModalResultDismissTime < MODAL_RESULT_DISMISS_COOLDOWN;
      }
    } catch (error) {
      console.warn("StartStopButton: Could not access cooldown variables");
    }
    return false;
  }

  /**
   * Handles the space keydown event to start or stop the testing process.
   * Prevents space key actions when ModalResult is visible or during cooldown period.
   * Also prevents action when dialogs are open or interactive elements are focused.
   * @param {KeyboardEvent} event - The keyboard event object
   */
  private readonly handleSpaceKey = (event: KeyboardEvent): void => {
    // Only handle Space key, let other keys pass through
    if (event.key !== " ") {
      return;
    }

    if (this.props.manualCollectMode) {
      event.preventDefault();
      event.stopPropagation();
      return;
    }

    // Check if completion ModalResult is visible
    if (this.isCompletionModalResultVisible()) {
      event.preventDefault();
      event.stopPropagation();
      return;
    }

    // Check if we're in cooldown period after ModalResult dismissal
    if (this.isInModalResultDismissCooldown()) {
      event.preventDefault();
      event.stopPropagation();
      return;
    }

    // Don't handle space if any dialog is open
    if (this.isDialogOpen()) {
      return;
    }

    const target = event.target as HTMLElement;
    if (!target) {
      return;
    }

    // Don't handle space if focused on interactive elements
    const interactiveElements = ["INPUT", "TEXTAREA", "SELECT", "BUTTON"];
    if (
      interactiveElements.includes(target.tagName) ||
      target.isContentEditable
    ) {
      return;
    }

    event.preventDefault();
    const is_testing_in_progress = this.props.testing_status == "run";
    is_testing_in_progress ? this.hardpy_stop() : this.hardpy_start();
  };

  /**
   * Handles the button click event to start the testing process.
   * Prevents button clicks when ModalResult is visible or during cooldown period.
   * @private
   */
  private readonly handleButtonClick = (): void => {
    if (this.props.manualCollectMode) {
      return;
    }

    // Check if completion ModalResult is visible
    if (this.isCompletionModalResultVisible()) {
      return;
    }

    // Check if we're in cooldown period after ModalResult dismissal
    if (this.isInModalResultDismissCooldown()) {
      return;
    }

    this.hardpy_start();
  };

  /**
   * Adds an event listener for the keydown event when the component is mounted.
   * Uses bubbling phase to not interfere with other capture phase listeners.
   */
  componentDidMount(): void {
    window.addEventListener("keydown", this.handleSpaceKey);
  }

  /**
   * Removes the event listener for the keydown event when the component is unmounted.
   * Also clears any pending timers to prevent memory leaks.
   */
  componentWillUnmount(): void {
    window.removeEventListener("keydown", this.handleSpaceKey);
    if (this.stopButtonTimer) {
      clearTimeout(this.stopButtonTimer);
    }
  }

  /**
   * Renders the Start/Stop button with appropriate properties based on the testing status.
   * Shows stop button when testing is in progress, start button otherwise.
   * @returns {React.ReactNode} The Start/Stop button component.
   */
  render(): React.ReactNode {
    const {
      t,
      testing_status,
      useBigButton = false,
      manualCollectMode = false,
    } = this.props;
    const is_testing: boolean = testing_status == "run";
    const button_id: string = "start-stop-button";

    if (useBigButton) {
      const bigButtonStyle = {
        width: "100%",
        height: "96px",
        fontSize: "24px",
        fontWeight: "bold",
        opacity: manualCollectMode ? 0.5 : 1,
      };

      const iconStyle = {
        fontSize: "28px",
        marginLeft: "12px",
      };

      const stop_button: AnchorButtonProps = {
        text: t("button.stop"),
        intent: "danger",
        large: true,
        rightIcon: <span style={iconStyle}>&#9632;</span>,
        onClick: this.hardpy_stop,
        id: button_id,
        fill: true,
        style: bigButtonStyle,
        disabled: manualCollectMode || this.state.isStopButtonDisabled,
      };

      const start_button: AnchorButtonProps = {
        text: t("button.start"),
        intent: is_testing ? undefined : "primary",
        large: true,
        rightIcon: <span style={iconStyle}>&#9658;</span>,
        onClick: this.handleButtonClick,
        id: button_id,
        disabled: manualCollectMode || this.state.isStopButtonDisabled,
        fill: true,
        style: bigButtonStyle,
      };

      return <AnchorButton {...(is_testing ? stop_button : start_button)} />;
    } else {
      const stop_button: AnchorButtonProps = {
        text: t("button.stop"),
        intent: "danger",
        large: true,
        rightIcon: "stop",
        onClick: this.hardpy_stop,
        id: button_id,
        disabled: manualCollectMode || this.state.isStopButtonDisabled,
      };

      const start_button: AnchorButtonProps = {
        text: t("button.start"),
        intent: is_testing ? undefined : "primary",
        large: true,
        rightIcon: "play",
        onClick: this.handleButtonClick,
        id: button_id,
        disabled: manualCollectMode || this.state.isStopButtonDisabled,
      };

      return <AnchorButton {...(is_testing ? stop_button : start_button)} />;
    }
  }
}

export default withTranslation()(StartStopButton);
