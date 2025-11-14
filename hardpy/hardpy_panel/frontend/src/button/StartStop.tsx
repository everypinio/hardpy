// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { AnchorButton, AnchorButtonProps } from "@blueprintjs/core";
import { withTranslation, WithTranslation } from "react-i18next";

type Props = {
  testing_status: string;
  useBigButton?: boolean;
  isAuthenticated: boolean;
  onUnauthorizedAction?: () => void;
} & WithTranslation;

type State = {
  isStopButtonDisabled: boolean;
  showAuthWarning: boolean;
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
  private authWarningTimer: NodeJS.Timeout | null = null;

  constructor(props: Props) {
    super(props);
    this.state = {
      isStopButtonDisabled: false,
      showAuthWarning: false,
    };
    this.hardpy_start = this.hardpy_start.bind(this);
    this.hardpy_stop = this.hardpy_stop.bind(this);
  }

  /**
   * Makes a fetch call to the specified URI with authentication check.
   * @param {string} uri - The URI to which the fetch request is made.
   * @private
   */
  private async hardpy_call(uri: string): Promise<void> {
    if (!this.props.isAuthenticated) {
      this.showAuthWarning();
      if (this.props.onUnauthorizedAction) {
        this.props.onUnauthorizedAction();
      }
      return;
    }

    try {
      const response = await fetch(uri);
      if (response.ok) {
        const result = await response.json();

        if (result.status === "unauthorized") {
          console.log(this.props.t("error.unauthorized"));
          this.showAuthWarning();
          if (this.props.onUnauthorizedAction) {
            this.props.onUnauthorizedAction();
          }
          return;
        }

        return result;
      } else {
        console.log(
          this.props.t("error.requestFailed", { status: response.status })
        );
      }
    } catch (error) {
      console.log(this.props.t("error.requestError", { error }));
    }
  }

  /**
   * Shows authentication warning and hides it after timeout
   * @private
   */
  private showAuthWarning(): void {
    this.setState({ showAuthWarning: true });

    // Clear existing timer
    if (this.authWarningTimer) {
      clearTimeout(this.authWarningTimer);
    }

    // Hide warning after 3 seconds
    this.authWarningTimer = setTimeout(() => {
      this.setState({ showAuthWarning: false });
    }, 3000);
  }

  /**
   * Initiates the start process by making a call to the 'api/start' endpoint.
   * @private
   */
  private hardpy_start(): void {
    // Early check for authentication
    if (!this.props.isAuthenticated) {
      console.log("StartStopButton: User not authenticated, cannot start test");
      this.showAuthWarning();
      if (this.props.onUnauthorizedAction) {
        this.props.onUnauthorizedAction();
      }
      return;
    }

    console.log("StartStopButton: Starting test execution");
    this.hardpy_call("api/start");
  }

  /**
   * Initiates the stop process by making a call to the 'api/stop' endpoint.
   * Temporarily disables the stop button to prevent multiple rapid clicks.
   * @private
   */
  private hardpy_stop(): void {
    // Early check for authentication
    if (!this.props.isAuthenticated) {
      console.log("StartStopButton: User not authenticated, cannot stop test");
      this.showAuthWarning();
      if (this.props.onUnauthorizedAction) {
        this.props.onUnauthorizedAction();
      }
      return;
    }

    if (this.state.isStopButtonDisabled) {
      return;
    }
    console.log("StartStopButton: Stopping test execution");
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
   * Checks if the authentication modal is currently visible.
   * Uses the data-auth-modal attribute from LoginModal component.
   * @returns {boolean} True if the auth modal is visible, false otherwise.
   */
  private isAuthModalVisible(): boolean {
    const authModalElements = document.querySelectorAll(
      '[data-auth-modal="true"]'
    );
    for (const modal of authModalElements) {
      const style = window.getComputedStyle(modal);
      if (style.display !== "none" && style.visibility !== "hidden") {
        return true;
      }
    }
    return false;
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
   * Checks if any blocking modal is currently visible (auth or completion).
   * @returns {boolean} True if any blocking modal is visible, false otherwise.
   */
  private isAnyBlockingModalVisible(): boolean {
    return this.isAuthModalVisible() || this.isCompletionModalResultVisible();
  }

  /**
   * Handles the space keydown event to start or stop the testing process.
   * Prevents space key actions when ModalResult or Auth modal is visible or during cooldown period.
   * Also prevents action when dialogs are open or interactive elements are focused.
   * @param {KeyboardEvent} event - The keyboard event object
   */
  private readonly handleSpaceKey = (event: KeyboardEvent): void => {
    // Only handle Space key, let other keys pass through
    if (event.key !== " ") {
      return;
    }

    // Check if any blocking modal (auth or completion) is visible
    if (this.isAnyBlockingModalVisible()) {
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
    if (!target) return;

    // Don't handle space if focused on interactive elements
    const interactiveElements = ["INPUT", "TEXTAREA", "SELECT", "BUTTON"];
    if (
      interactiveElements.includes(target.tagName) ||
      target.isContentEditable
    ) {
      return;
    }

    // Check authentication before proceeding
    if (!this.props.isAuthenticated) {
      event.preventDefault();
      event.stopPropagation();
      this.showAuthWarning();
      if (this.props.onUnauthorizedAction) {
        this.props.onUnauthorizedAction();
      }
      return;
    }

    event.preventDefault();
    const is_testing_in_progress = this.props.testing_status == "run";
    is_testing_in_progress ? this.hardpy_stop() : this.hardpy_start();
  };

  /**
   * Handles the button click event to start the testing process.
   * Prevents button clicks when ModalResult or Auth modal is visible or during cooldown period.
   * @private
   */
  private readonly handleButtonClick = (): void => {
    // Check if any blocking modal (auth or completion) is visible
    if (this.isAnyBlockingModalVisible()) {
      return;
    }

    // Check if we're in cooldown period after ModalResult dismissal
    if (this.isInModalResultDismissCooldown()) {
      return;
    }

    // Check authentication
    if (!this.props.isAuthenticated) {
      this.showAuthWarning();
      if (this.props.onUnauthorizedAction) {
        this.props.onUnauthorizedAction();
      }
      return;
    }

    this.hardpy_start();
  };

  /**
   * Handles the stop button click event.
   * Prevents stop button clicks when ModalResult or Auth modal is visible or during cooldown period.
   * @private
   */
  private readonly handleStopButtonClick = (): void => {
    // Check if any blocking modal (auth or completion) is visible
    if (this.isAnyBlockingModalVisible()) {
      return;
    }

    // Check if we're in cooldown period after ModalResult dismissal
    if (this.isInModalResultDismissCooldown()) {
      return;
    }

    // Check authentication
    if (!this.props.isAuthenticated) {
      this.showAuthWarning();
      if (this.props.onUnauthorizedAction) {
        this.props.onUnauthorizedAction();
      }
      return;
    }

    this.hardpy_stop();
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
    if (this.authWarningTimer) {
      clearTimeout(this.authWarningTimer);
    }
  }

  /**
   * Renders the Start/Stop button with appropriate properties based on the testing status.
   * Shows stop button when testing is in progress, start button otherwise.
   * Includes authentication warning when user is not authenticated.
   * @returns {React.ReactNode} The Start/Stop button component.
   */
  render(): React.ReactNode {
    const {
      t,
      testing_status,
      useBigButton = false,
      isAuthenticated,
    } = this.props;
    const { showAuthWarning } = this.state;
    const is_testing: boolean = testing_status == "run";
    const button_id: string = "start-stop-button";

    // Determine button properties based on authentication status
    const isButtonDisabled =
      !isAuthenticated || this.state.isStopButtonDisabled;
    const buttonTooltip = !isAuthenticated ? t("auth.pleaseLogin") : undefined;

    if (useBigButton) {
      const bigButtonStyle = {
        width: "100%",
        height: "96px",
        fontSize: "24px",
        fontWeight: "bold",
        position: "relative" as const,
      };

      const iconStyle = {
        fontSize: "28px",
        marginLeft: "12px",
      };

      const warningStyle = {
        position: "absolute" as const,
        top: "-30px",
        left: "50%",
        transform: "translateX(-50%)",
        backgroundColor: "#DB3737",
        color: "white",
        padding: "5px 10px",
        borderRadius: "3px",
        fontSize: "14px",
        fontWeight: "normal",
        whiteSpace: "nowrap" as const,
        zIndex: 10,
      };

      const stop_button: AnchorButtonProps = {
        text: t("button.stop"),
        intent: "danger",
        large: true,
        rightIcon: <span style={iconStyle}>&#9632;</span>,
        onClick: this.handleStopButtonClick,
        id: button_id,
        fill: true,
        style: bigButtonStyle,
        disabled: isButtonDisabled,
        title: buttonTooltip,
      };

      const start_button: AnchorButtonProps = {
        text: t("button.start"),
        intent: is_testing ? undefined : "primary",
        large: true,
        rightIcon: <span style={iconStyle}>&#9658;</span>,
        onClick: this.handleButtonClick,
        id: button_id,
        disabled: isButtonDisabled,
        fill: true,
        style: bigButtonStyle,
        title: buttonTooltip,
      };

      return (
        <div style={{ position: "relative" }}>
          {showAuthWarning && (
            <div style={warningStyle}>{t("auth.pleaseLogin")}</div>
          )}
          <AnchorButton {...(is_testing ? stop_button : start_button)} />
        </div>
      );
    } else {
      const containerStyle = {
        position: "relative" as const,
        display: "inline-block",
      };

      const warningStyle = {
        position: "absolute" as const,
        top: "-35px",
        left: "50%",
        transform: "translateX(-50%)",
        backgroundColor: "#DB3737",
        color: "white",
        padding: "4px 8px",
        borderRadius: "3px",
        fontSize: "12px",
        fontWeight: "normal",
        whiteSpace: "nowrap" as const,
        zIndex: 10,
      };

      const stop_button: AnchorButtonProps = {
        text: t("button.stop"),
        intent: "danger",
        large: true,
        rightIcon: "stop",
        onClick: this.handleStopButtonClick,
        id: button_id,
        disabled: isButtonDisabled,
        title: buttonTooltip,
      };

      const start_button: AnchorButtonProps = {
        text: t("button.start"),
        intent: is_testing ? undefined : "primary",
        large: true,
        rightIcon: "play",
        onClick: this.handleButtonClick,
        id: button_id,
        disabled: isButtonDisabled,
        title: buttonTooltip,
      };

      return (
        <div style={containerStyle}>
          {showAuthWarning && (
            <div style={warningStyle}>{t("auth.pleaseLogin")}</div>
          )}
          <AnchorButton {...(is_testing ? stop_button : start_button)} />
        </div>
      );
    }
  }
}

export default withTranslation()(StartStopButton);
