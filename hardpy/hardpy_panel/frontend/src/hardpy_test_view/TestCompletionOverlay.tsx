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

interface TestCompletionOverlayProps {
  isVisible: boolean;
  testPassed: boolean;
  testStopped: boolean;
  failedTestCases?: FailedTestCase[];
  onDismiss: () => void;
  onVisibilityChange?: (isVisible: boolean) => void;
}

/**
 * Overlay component that displays test completion results with PASS/FAIL/STOP status
 */
const TestCompletionOverlay: React.FC<TestCompletionOverlayProps> = ({
  isVisible,
  testPassed,
  testStopped,
  failedTestCases = [],
  onDismiss,
  onVisibilityChange,
}) => {
  const { t } = useTranslation();

  React.useEffect(() => {
    console.log("TestCompletionOverlay: Visibility changed to", isVisible);
    onVisibilityChange?.(isVisible);
  }, [isVisible, onVisibilityChange]);

  React.useEffect(() => {
    if (isVisible && testPassed) {
      // Auto-dismiss after 5 seconds only for PASS
      const timer = setTimeout(() => {
        console.log("TestCompletionOverlay: Auto-dismissing PASS overlay");
        onDismiss();
      }, 5000);

      return () => clearTimeout(timer);
    }
  }, [isVisible, testPassed, onDismiss]);

  if (!isVisible) {
    return null;
  }

  // Determine overlay color based on status
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
    statusTranslation = t("app.status.stopped") || "停止";
  } else if (testPassed) {
    statusText = "PASS";
    statusTranslation = t("app.status.passed") || "通过";
  } else {
    statusText = "FAIL";
    statusTranslation = t("app.status.failed") || "失败";
  }

  const overlayStyle: React.CSSProperties = {
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
    padding: "40px",
  };

  const titleStyle: React.CSSProperties = {
    fontSize: "120px",
    fontWeight: "bold",
    marginBottom: "20px",
    textShadow: "0 4px 8px rgba(0,0,0,0.3)",
  };

  const subtitleStyle: React.CSSProperties = {
    fontSize: "48px",
    fontWeight: "bold",
    marginBottom: "40px",
    textShadow: "0 2px 4px rgba(0,0,0,0.3)",
  };

  const failedCasesStyle: React.CSSProperties = {
    maxHeight: "60vh",
    overflowY: "auto",
    backgroundColor: "rgba(0,0,0,0.3)",
    borderRadius: "8px",
    padding: "20px",
    marginTop: "20px",
    width: "80%",
    maxWidth: "800px",
  };

  const caseItemStyle: React.CSSProperties = {
    marginBottom: "15px",
    textAlign: "left",
    borderBottom: "1px solid rgba(255,255,255,0.2)",
    paddingBottom: "10px",
  };

  const caseNameStyle: React.CSSProperties = {
    fontSize: "18px",
    fontWeight: "bold",
    marginBottom: "5px",
  };

  const assertionStyle: React.CSSProperties = {
    fontSize: "14px",
    opacity: 0.9,
    fontStyle: "italic",
  };

  const handleOverlayClick = () => {
    console.log("TestCompletionOverlay: Overlay clicked, dismissing");
    onDismiss();
  };

  return (
    <div
      style={overlayStyle}
      onClick={handleOverlayClick}
      className={Classes.DARK}
    >
      <div style={titleStyle}>{statusText}</div>
      <div style={subtitleStyle}>{statusTranslation}</div>

      {!testPassed && !testStopped && failedTestCases.length > 0 && (
        <div style={failedCasesStyle}>
          <h3 style={{ marginTop: 0, marginBottom: "20px", fontSize: "24px" }}>
            {t("app.failedTestCases") || "Failed Test Cases"}:
          </h3>
          {failedTestCases.map((testCase, index) => (
            <div key={index} style={caseItemStyle}>
              <div style={caseNameStyle}>
                {testCase.moduleName} → {testCase.caseName}
              </div>
              {testCase.assertionMsg && (
                <div style={assertionStyle}>{testCase.assertionMsg}</div>
              )}
            </div>
          ))}
        </div>
      )}

      <div
        style={{
          position: "absolute",
          bottom: "40px",
          fontSize: "16px",
          opacity: 0.8,
        }}
      >
        {t("app.overlayDismissHint") ||
          "Click anywhere or press any key to dismiss"}
      </div>
    </div>
  );
};

export default TestCompletionOverlay;
