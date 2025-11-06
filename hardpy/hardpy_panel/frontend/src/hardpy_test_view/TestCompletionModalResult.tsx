// Copyright (c) 2025 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { useTranslation } from "react-i18next";
import { Classes } from "@blueprintjs/core";

interface FailedTestCase {
  moduleName: string;
  caseName: string;
  assertionMsg?: string;
}

interface StoppedTestCase {
  moduleName: string;
  caseName: string;
  assertionMsg?: string;
}

interface TestCompletionModalResultProps {
  isVisible: boolean;
  testPassed: boolean;
  testStopped: boolean;
  failedTestCases?: FailedTestCase[];
  stoppedTestCase?: StoppedTestCase;
  onDismiss: () => void;
  onVisibilityChange?: (isVisible: boolean) => void;
  autoDismissPass?: boolean; // Whether to auto-dismiss PASS ModalResult
  autoDismissTimeout?: number; // Timeout for auto-dismiss in seconds
}

/**
 * ModalResult component that displays test completion results with PASS/FAIL/STOP status
 */
const TestCompletionModalResult: React.FC<TestCompletionModalResultProps> = ({
  isVisible,
  testPassed,
  testStopped,
  failedTestCases = [],
  stoppedTestCase,
  onDismiss,
  onVisibilityChange,
  autoDismissPass = true, // Default to true for backward compatibility
  autoDismissTimeout = 5, // Default to 5 seconds for backward compatibility
}) => {
  const { t } = useTranslation();
  const [timeLeft, setTimeLeft] = React.useState(autoDismissTimeout);

  /**
   * Handles visibility changes and resets timer when modal becomes visible
   */
  React.useEffect(() => {
    onVisibilityChange?.(isVisible);

    if (isVisible) {
      setTimeLeft(autoDismissTimeout);
    }
  }, [isVisible, onVisibilityChange, autoDismissTimeout]);

  /**
   * Manages auto-dismiss functionality with countdown timer
   */
  React.useEffect(() => {
    if (isVisible && testPassed && autoDismissPass) {
      setTimeLeft(autoDismissTimeout);

      const countdownTimer = setInterval(() => {
        setTimeLeft((prevTime) => {
          if (prevTime <= 1) {
            clearInterval(countdownTimer);
            return 0;
          }
          return prevTime - 1;
        });
      }, 1000);

      // Auto-dismiss after specified timeout only for PASS and if auto-dismiss is enabled
      const dismissTimer = setTimeout(() => {
        onDismiss();
      }, autoDismissTimeout * 1000); // Convert seconds to milliseconds

      return () => {
        clearInterval(countdownTimer);
        clearTimeout(dismissTimer);
      };
    }
  }, [isVisible, testPassed, onDismiss, autoDismissPass, autoDismissTimeout]);

  if (!isVisible) {
    return null;
  }

  // Determine ModalResult color based on status
  let backgroundColor: string;
  if (testStopped) {
    backgroundColor = "rgba(255, 179, 0, 0.95)"; // Yellow for STOP
  } else if (testPassed) {
    backgroundColor = "rgba(15, 153, 96, 0.95)"; // Green for PASS
  } else {
    backgroundColor = "rgba(219, 55, 55, 0.95)"; // Red for FAIL
  }

  // Determine status text and translation
  let statusText: string;
  let statusTranslation: string;

  if (testStopped) {
    statusText = "STOP";
    statusTranslation = t("app.status.stopped");
  } else if (testPassed) {
    statusText = "PASS";
    statusTranslation = t("app.status.passed");
  } else {
    statusText = "FAIL";
    statusTranslation = t("app.status.failed");
  }

  const ModalResultStyle: React.CSSProperties = {
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: backgroundColor,
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    zIndex: 9999,
    cursor: "pointer",
    color: "white",
    textAlign: "center",
    padding: "20px",
  };

  const titleStyle: React.CSSProperties = {
    fontSize: "clamp(60px, 15vw, 120px)", // Responsive font size
    fontWeight: "bold",
    marginBottom: "10px",
    textShadow: "0 4px 8px rgba(0,0,0,0.3)",
  };

  const subtitleStyle: React.CSSProperties = {
    fontSize: "clamp(24px, 6vw, 48px)", // Responsive font size
    fontWeight: "bold",
    marginBottom: "30px",
    textShadow: "0 2px 4px rgba(0,0,0,0.3)",
  };

  const casesContainerStyle: React.CSSProperties = {
    maxHeight: "50vh",
    overflowY: "auto",
    backgroundColor: "rgba(0,0,0,0.3)",
    borderRadius: "8px",
    padding: "15px",
    marginTop: "10px",
    width: "90%",
    maxWidth: "800px",
    marginBottom: "20px", // Add margin at bottom to separate from dismiss hint
  };

  const caseItemStyle: React.CSSProperties = {
    marginBottom: "12px",
    textAlign: "left",
    borderBottom: "1px solid rgba(255,255,255,0.2)",
    paddingBottom: "8px",
    wordBreak: "break-word", // Ensure long text breaks properly
  };

  const caseNameStyle: React.CSSProperties = {
    fontSize: "clamp(14px, 3vw, 18px)", // Responsive font size
    fontWeight: "bold",
    marginBottom: "4px",
  };

  const assertionStyle: React.CSSProperties = {
    fontSize: "clamp(12px, 2.5vw, 14px)", // Responsive font size
    opacity: 0.9,
    fontStyle: "italic",
  };

  const dismissHintStyle: React.CSSProperties = {
    position: "absolute",
    bottom: "20px",
    fontSize: "clamp(12px, 3vw, 16px)",
    opacity: 0.8,
    width: "100%",
    textAlign: "center",
    padding: "0 10px",
  };

  /**
   * Handles click event on the modal result to dismiss it
   */
  const handleModalResultClick = () => {
    onDismiss();
  };

  /**
   * Renders the stopped test case information if available
   * @returns {JSX.Element | null} Stopped test case component or null if no stopped test case
   */
  const renderStoppedTestCase = (): JSX.Element | null => {
    if (!stoppedTestCase) return null;

    return (
      <div style={casesContainerStyle}>
        <h3
          style={{
            marginTop: 0,
            marginBottom: "15px",
            fontSize: "clamp(16px, 4vw, 24px)",
          }}
        >
          {t("app.stoppedTestCase") || "Stopped Test Case"}:
        </h3>
        <div style={caseItemStyle}>
          <div style={caseNameStyle}>
            {stoppedTestCase.moduleName} → {stoppedTestCase.caseName}
          </div>
          {stoppedTestCase.assertionMsg && (
            <div style={assertionStyle}>{stoppedTestCase.assertionMsg}</div>
          )}
        </div>
      </div>
    );
  };

  /**
   * Renders the list of failed test cases if any exist
   * @returns {JSX.Element | null} Failed test cases component or null if no failed test cases
   */
  const renderFailedTestCases = (): JSX.Element | null => {
    if (failedTestCases.length === 0) return null;

    return (
      <div style={casesContainerStyle}>
        <h3
          style={{
            marginTop: 0,
            marginBottom: "15px",
            fontSize: "clamp(16px, 4vw, 24px)",
          }}
        >
          {t("app.failedTestCases") || "Failed Test Cases"}:
        </h3>
        {failedTestCases.map((testCase, index) => (
          <div key={index} style={caseItemStyle}>
            <div style={caseNameStyle}>
              {testCase.moduleName} → {testCase.caseName}
            </div>
            {testCase.assertionMsg && (
              <div style={assertionStyle}>{testCase.assertionMsg.split("\n")[0]}</div>
            )}
          </div>
        ))}
      </div>
    );
  };

  // Show dismiss hint only if manual dismissal is required
  const showDismissHint = !testPassed || !autoDismissPass;

  return (
    <div
      style={ModalResultStyle}
      onClick={handleModalResultClick}
      className={Classes.DARK}
    >
      <div style={titleStyle}>{statusText}</div>
      <div style={subtitleStyle}>{statusTranslation}</div>

      {/* Show stopped test case for STOP status */}
      {testStopped && renderStoppedTestCase()}

      {/* Show failed test cases for FAIL status */}
      {!testPassed && !testStopped && renderFailedTestCases()}

      {showDismissHint && (
        <div style={dismissHintStyle}>
          {t("app.modalResultDismissHint") ||
            "Click anywhere or press any key to dismiss"}
        </div>
      )}

      {testPassed && autoDismissPass && (
        <div style={dismissHintStyle}>
          {t("app.modalResultAutoDismissHint", {
            seconds: timeLeft,
          }) +
            " " +
            t("app.modalResultDismissHint") ||
            `Auto-dismissing in ${timeLeft} seconds...`}
        </div>
      )}
    </div>
  );
};

export default TestCompletionModalResult;
