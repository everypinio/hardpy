// Copyright (c) 2025 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { Button, Dialog, H2, Classes } from "@blueprintjs/core";
import { useTranslation } from "react-i18next";

interface TestConfig {
  name: string;
  description?: string;
  file?: string;
}

interface TestConfigOverlayProps {
  isOpen: boolean;
  testConfigs: TestConfig[];
  currentConfig?: string;
  isTestRunning?: boolean;
  onSelect: (configName: string) => void;
  onClose?: () => void;
}

/**
 * Overlay component for selecting test configuration when none is currently selected
 */
const TestConfigOverlay: React.FC<TestConfigOverlayProps> = ({
  isOpen,
  testConfigs,
  currentConfig,
  isTestRunning = false,
  onSelect,
  onClose,
}) => {
  const handleConfigSelect = (configName: string) => {
    onSelect(configName);
  };

  // Allow closing if there's already a current config selected
  const canClose = !!currentConfig;

  const handleClose = () => {
    if (canClose && onClose) {
      onClose();
    }
  };

  const { t } = useTranslation();

  return (
    <Dialog
      isOpen={isOpen}
      canEscapeKeyClose={canClose}
      canOutsideClickClose={canClose}
      onClose={handleClose}
      hasBackdrop={true}
      className={Classes.DARK}
      style={{
        width: "80%",
        maxWidth: "600px",
        minHeight: "400px",
      }}
    >
      <div className={Classes.DIALOG_BODY}>
        <H2 style={{ textAlign: "center", marginBottom: "30px" }}>
          {t("app.testConfigurationSelector")}
        </H2>

        {isTestRunning && (
          <div
            style={{
              textAlign: "center",
              marginBottom: "20px",
              padding: "10px",
              backgroundColor: "#FF7373",
              borderRadius: "4px",
              color: "white",
              fontWeight: "bold",
            }}
          >
            Cannot change configuration while test is running
          </div>
        )}

        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "15px",
            alignItems: "center",
          }}
        >
          {testConfigs.map((config) => {
            const isSelected = config.name === currentConfig;
            return (
              <Button
                key={config.name}
                large={true}
                disabled={isTestRunning}
                intent={isSelected ? "success" : "primary"}
                style={{
                  width: "300px",
                  height: "60px",
                  fontSize: "16px",
                  fontWeight: "bold",
                  opacity: isTestRunning ? 0.5 : isSelected ? 0.8 : 1,
                }}
                onClick={() => handleConfigSelect(config.name)}
              >
                {isSelected && "✓ "}
                {config.name}
                {config.description && (
                  <div
                    style={{
                      fontSize: "12px",
                      fontWeight: "normal",
                      marginTop: "4px",
                    }}
                  >
                    {config.description}
                  </div>
                )}
              </Button>
            );
          })}
        </div>

        {testConfigs.length === 0 && (
          <div
            style={{
              textAlign: "center",
              marginTop: "20px",
              color: "#888",
            }}
          >
            No test configurations available
          </div>
        )}
      </div>
    </Dialog>
  );
};

export default TestConfigOverlay;
