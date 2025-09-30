// Copyright (c) 2025 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { Classes } from "@blueprintjs/core";

interface FailedTestCase {
  moduleName: string;
  caseName: string;
  assertionMsg?: string;
}

interface TestCompletionOverlayProps {
  isVisible: boolean;
  testPassed: boolean;
  failedTestCases?: FailedTestCase[];
  onDismiss: () => void;
}

/**
 * Overlay component that displays test completion results with PASS/FAIL status
 */
const TestCompletionOverlay: React.FC<TestCompletionOverlayProps> = ({
  isVisible,
  testPassed,
  failedTestCases = [],
  onDismiss,
}) => {
  React.useEffect(() => {
    if (isVisible && testPassed) {
      // Auto-dismiss after 5 seconds only for PASS
      const timer = setTimeout(() => {
        onDismiss();
      }, 5000);

      return () => clearTimeout(timer);
    }
  }, [isVisible, testPassed, onDismiss]);

  if (!isVisible) {
    return null;
  }

  const overlayStyle: React.CSSProperties = {
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: testPassed
      ? "rgba(15, 153, 96, 0.95)" // Green with transparency
      : "rgba(219, 55, 55, 0.95)", // Red with transparency
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

  return (
    <div style={overlayStyle} onClick={onDismiss} className={Classes.DARK}>
      <div style={titleStyle}>{testPassed ? "PASS" : "FAIL"}</div>
      <div style={subtitleStyle}>{testPassed ? "通过" : "失败"}</div>

      {!testPassed && failedTestCases.length > 0 && (
        <div style={failedCasesStyle}>
          <h3 style={{ marginTop: 0, marginBottom: "20px", fontSize: "24px" }}>
            Failed Test Cases:
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
        Click anywhere to dismiss
      </div>
    </div>
  );
};

export default TestCompletionOverlay;
