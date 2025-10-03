// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { useTranslation } from "react-i18next";

import {
  Button,
  Navbar,
  Alignment,
  Classes,
  Colors,
  Menu,
  MenuItem,
  H2,
  Popover,
  Card,
} from "@blueprintjs/core";

import StartStopButton from "./button/StartStop";
import { TestRunI } from "./hardpy_test_view/SuiteList";
import SuiteList from "./hardpy_test_view/SuiteList";
import ProgressView from "./progress/ProgressView";
import TestStatus from "./hardpy_test_view/TestStatus";
import ReloadAlert from "./restart_alert/RestartAlert";
import PlaySound from "./hardpy_test_view/PlaySound";
import TestCompletionModalResult from "./hardpy_test_view/TestCompletionModalResult";

import { useAllDocs } from "use-pouchdb";

import "./App.css";

const WINDOW_WIDTH_THRESHOLDS = {
  ULTRAWIDE: 490,
  WIDE: 400,
};

const STATUS_MAP = {
  ready: "app.status.ready",
  run: "app.status.run",
  passed: "app.status.passed",
  failed: "app.status.failed",
  stopped: "app.status.stopped",
} as const;

type StatusKey = keyof typeof STATUS_MAP;

/**
 * Checks if the provided status is a valid status key.
 */
const isValidStatus = (status: string): status is StatusKey => {
  return status in STATUS_MAP;
};

// Global variable to track ModalResult visibility with timestamp
let isCompletionModalResultVisible = false;
let lastModalResultDismissTime = 0;
const MODAL_RESULT_DISMISS_COOLDOWN = 100; // ms

/**
 * Sets the global ModalResult visibility state
 */
export const setCompletionModalResultVisible = (visible: boolean): void => {
  console.log(
    "App: Setting global ModalResult visibility to",
    visible,
    "at time:",
    Date.now()
  );
  isCompletionModalResultVisible = visible;
  if (!visible) {
    lastModalResultDismissTime = Date.now();
    console.log(
      "App: Set last ModalResult dismiss time to",
      lastModalResultDismissTime
    );
  }
};

/**
 * Gets the global ModalResult visibility state
 */
export const getCompletionModalResultVisible = (): boolean => {
  return isCompletionModalResultVisible;
};

/**
 * Checks if we're in cooldown period after ModalResult dismissal
 */
export const isInModalResultDismissCooldown = (): boolean => {
  const now = Date.now();
  const inCooldown =
    now - lastModalResultDismissTime < MODAL_RESULT_DISMISS_COOLDOWN;
  console.log(
    "App: Cooldown check - now:",
    now,
    "lastDismiss:",
    lastModalResultDismissTime,
    "inCooldown:",
    inCooldown
  );
  return inCooldown;
};

/**
 * Finds the test case that was stopped during test execution
 */
const findStoppedTestCase = (
  testRunData: TestRunI
):
  | { moduleName: string; caseName: string; assertionMsg?: string }
  | undefined => {
  if (!testRunData.modules) return undefined;

  for (const [moduleId, module] of Object.entries(testRunData.modules)) {
    if (module.cases) {
      for (const [caseId, testCase] of Object.entries(module.cases)) {
        if (testCase.status === "stopped") {
          return {
            moduleName: module.name || moduleId,
            caseName: testCase.name || caseId,
            assertionMsg: testCase.assertion_msg || undefined,
          };
        }
      }
    }
  }

  let lastFailedTestCase: any = null;

  for (const [moduleId, module] of Object.entries(testRunData.modules)) {
    if (module.cases) {
      for (const [caseId, testCase] of Object.entries(module.cases)) {
        if (testCase.status === "failed") {
          lastFailedTestCase = {
            moduleName: module.name || moduleId,
            caseName: testCase.name || caseId,
            assertionMsg: testCase.assertion_msg || undefined,
          };
        }
      }
    }
  }

  return lastFailedTestCase;
};

/**
 * Main component of the GUI.
 * @param {string} syncDocumentId - The id of the PouchDB document to syncronize.
 * @returns {JSX.Element} The main application component.
 */
function App({ syncDocumentId }: { syncDocumentId: string }): JSX.Element {
  const { t } = useTranslation();
  const [use_end_test_sound, setUseEndTestSound] = React.useState(false);
  const [use_debug_info, setUseDebugInfo] = React.useState(false);

  const [lastRunStatus, setLastRunStatus] = React.useState<
    StatusKey | "unknown"
  >("ready");
  const [lastProgress, setProgress] = React.useState(0);
  const [isAuthenticated, setIsAuthenticated] = React.useState(true);
  const [lastRunDuration, setLastRunDuration] = React.useState<number>(0);

  // HardPy config state
  const [hardpyConfig, setHardpyConfig] = React.useState<any>(null);

  // Test completion ModalResult state
  const [showCompletionModalResult, setShowCompletionModalResult] =
    React.useState(false);
  const [testCompletionData, setTestCompletionData] = React.useState<{
    testPassed: boolean;
    testStopped: boolean;
    failedTestCases: Array<{
      moduleName: string;
      caseName: string;
      assertionMsg?: string;
    }>;
    stoppedTestCase?: {
      moduleName: string;
      caseName: string;
      assertionMsg?: string;
    };
  } | null>(null);

  const startTimeRef = React.useRef<number | null>(null);
  const [timerIntervalId, setTimerIntervalId] =
    React.useState<NodeJS.Timeout | null>(null);

  React.useEffect(() => {
    const loadConfig = async () => {
      try {
        const response = await fetch("/api/hardpy_config");
        const config = await response.json();
        setHardpyConfig(config);

        if (config.sound_on !== undefined) {
          setUseEndTestSound(config.sound_on);
        }

        if (
          !config.current_test_config &&
          config.test_configs &&
          config.test_configs.length > 0
        ) {
          // This can be used for config ModalResult, keeping for reference
        }
      } catch (error) {
        console.error("Failed to load HardPy config:", error);
      }
    };

    loadConfig();
  }, []);

  /**
   * Custom hook to determine if the window width is greater than a specified size.
   * @param {number} size - The width threshold to compare against.
   * @returns {boolean} True if the window width is greater than the specified size, otherwise false.
   */
  const useWindowWide = (size: number): boolean => {
    const [width, setWidth] = React.useState(0);

    React.useEffect(() => {
      function handleResize() {
        setWidth(window.innerWidth);
      }

      window.addEventListener("resize", handleResize);

      handleResize();

      return () => {
        window.removeEventListener("resize", handleResize);
      };
    }, [setWidth]);

    return width > size;
  };

  const ultrawide = useWindowWide(WINDOW_WIDTH_THRESHOLDS.ULTRAWIDE);
  const wide = useWindowWide(WINDOW_WIDTH_THRESHOLDS.WIDE);

  // Handle ModalResult visibility changes
  const handleModalResultVisibilityChange = React.useCallback(
    (isVisible: boolean) => {
      console.log(
        "App: ModalResult visibility change callback, isVisible:",
        isVisible
      );
      setCompletionModalResultVisible(isVisible);
    },
    []
  );

  // Handle keyboard events for ModalResult dismissal
  React.useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (showCompletionModalResult) {
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation();

        setShowCompletionModalResult(false);
        setTestCompletionData(null);

        if (event.key === " ") {
          event.preventDefault();
          const activeElement = document.activeElement as HTMLElement;
          if (activeElement && activeElement.blur) {
            activeElement.blur();
          }
        }
      }
    };

    if (showCompletionModalResult) {
      document.addEventListener("keydown", handleKeyDown, {
        capture: true,
        passive: false,
      });
      return () => {
        document.removeEventListener("keydown", handleKeyDown, {
          capture: true,
        });
      };
    }
  }, [showCompletionModalResult]);

  React.useEffect(() => {
    if (lastRunStatus === "run") {
      if (startTimeRef.current !== null) {
        const updateDuration = () => {
          const currentTimeInSeconds = Math.floor(Date.now() / 1000);
          setLastRunDuration(currentTimeInSeconds - startTimeRef.current!);
        };

        updateDuration();

        const id = setInterval(updateDuration, 1000);
        setTimerIntervalId(id);

        return () => {
          if (id) {
            clearInterval(id);
          }
        };
      }
    } else if (timerIntervalId) {
      clearInterval(timerIntervalId);
      setTimerIntervalId(null);
    }
  }, [lastRunStatus]);

  /**
   * Finds the index of a row in a list based on its ID.
   * @param {Array} rows - The list of rows to search.
   * @param {string} searchTerm - The ID to search for.
   * @returns {number} The index of the row, or -1 if not found.
   */
  function findRowIndex(rows: { id: string }[], searchTerm: string): number {
    for (let i = 0; i < rows.length; i++) {
      if (rows[i].id === searchTerm) {
        return i;
      }
    }
    return -1;
  }

  const { rows, state, loading, error } = useAllDocs({
    include_docs: true,
  });

  React.useEffect(() => {
    if (rows.length === 0) return;

    const index = findRowIndex(rows, syncDocumentId);
    if (index === -1) return;
    const db_row = rows[index].doc as TestRunI;
    const status = db_row.status || "";
    const progress = db_row.progress || 0;

    if (status !== lastRunStatus) {
      setLastRunStatus(isValidStatus(status) ? status : "unknown");
    }

    if (progress !== lastProgress) {
      setProgress(progress);
    }

    if (db_row.start_time) {
      startTimeRef.current = db_row.start_time;

      if (db_row.stop_time && status !== "run") {
        const duration = db_row.stop_time - db_row.start_time;
        if (duration !== lastRunDuration) {
          setLastRunDuration(duration);
        }
      }
    }

    // Detect test completion and show ModalResult (only if enabled in config)
    const prevStatus = lastRunStatus;
    const ModalResultEnabled =
      hardpyConfig?.frontend?.modal_result?.enabled ?? true;
    if (
      ModalResultEnabled &&
      prevStatus === "run" &&
      (status === "passed" || status === "failed" || status === "stopped") &&
      !showCompletionModalResult
    ) {
      console.log("App: Test completed, showing ModalResult. Status:", status);
      const testPassed = status === "passed";
      const testStopped = status === "stopped";
      const failedTestCases: Array<{
        moduleName: string;
        caseName: string;
        assertionMsg?: string;
      }> = [];

      // Extract failed test cases if test failed
      if (!testPassed && !testStopped && db_row.modules) {
        Object.entries(db_row.modules).forEach(
          ([moduleId, module]: [string, any]) => {
            if (module.cases) {
              Object.entries(module.cases).forEach(
                ([caseId, testCase]: [string, any]) => {
                  if (testCase.status === "failed") {
                    failedTestCases.push({
                      moduleName: module.name || moduleId,
                      caseName: testCase.name || caseId,
                      assertionMsg: testCase.assertion_msg || undefined,
                    });
                  }
                }
              );
            }
          }
        );
      }

      const stoppedTestCase = testStopped
        ? findStoppedTestCase(db_row)
        : undefined;

      setTestCompletionData({
        testPassed,
        testStopped,
        failedTestCases,
        stoppedTestCase,
      });
      setShowCompletionModalResult(true);
    }

    if (state === "error") {
      setIsAuthenticated(false);
    } else if (isAuthenticated === false) {
      setIsAuthenticated(true);
    }
  }, [
    rows,
    state,
    lastRunStatus,
    lastProgress,
    lastRunDuration,
    isAuthenticated,
    hardpyConfig,
  ]);

  /**
   * Renders the database content.
   * @returns {JSX.Element} The rendered content.
   */
  const renderDbContent = (): JSX.Element => {
    if (loading && rows.length === 0) {
      return (
        <Card style={{ marginTop: "60px" }}>
          <H2>{t("app.connection")}</H2>
        </Card>
      );
    }

    if (state === "error") {
      return (
        <Card style={{ marginTop: "60px" }}>
          <H2>{t("app.dbError")}</H2>
          {error && <p>{error.message}</p>}
        </Card>
      );
    }

    if (rows.length === 0) {
      return (
        <Card style={{ marginTop: "60px" }}>
          <H2>{t("app.noEntries")}</H2>
        </Card>
      );
    }

    const index = findRowIndex(rows, syncDocumentId);
    if (index === -1) {
      return (
        <Card style={{ marginTop: "60px" }}>
          <H2>{t("app.dbError")}</H2>
          {error && <p>{error.message}</p>}
        </Card>
      );
    }

    const document_row = rows[index];

    if (!document_row) {
      return (
        <Card style={{ marginTop: "60px" }}>
          <H2>{t("app.dbError")}</H2>
          {error && <p>{error.message}</p>}
        </Card>
      );
    }

    const testRunData: TestRunI = document_row.doc as TestRunI;

    return (
      <div style={{ marginTop: "40px" }}>
        <div
          key={document_row.id}
          style={{ display: "flex", flexDirection: "row" }}
        >
          {(ultrawide || !use_debug_info) && (
            <Card
              style={{
                flexDirection: "column",
                padding: "20px",
                flexGrow: 1,
                flexShrink: 1,
                marginTop: "20px",
                marginBottom: "20px",
              }}
            >
              <SuiteList
                db_state={testRunData}
                defaultClose={!ultrawide}
              ></SuiteList>
            </Card>
          )}
          {use_debug_info && (
            <Card
              style={{
                flexDirection: "column",
                padding: "20px",
                marginTop: "20px",
                marginBottom: "20px",
              }}
            >
              <pre>{JSON.stringify(testRunData, null, 2)}</pre>
            </Card>
          )}
        </div>
      </div>
    );
  };

  /**
   * Renders the settings menu.
   * @returns {JSX.Element} The settings menu component.
   */
  const renderSettingsMenu = (): JSX.Element => {
    return (
      <Menu>
        <MenuItem
          shouldDismissPopover={false}
          text={use_end_test_sound ? t("app.soundOff") : t("app.soundOn")}
          icon={use_end_test_sound ? "volume-up" : "volume-off"}
          id="use_end_test_sound"
          onClick={() => setUseEndTestSound(!use_end_test_sound)}
        />
        <MenuItem
          shouldDismissPopover={false}
          text={use_debug_info ? t("app.debugOff") : t("app.debugOn")}
          icon={"bug"}
          id="use_debug_info"
          onClick={() => setUseDebugInfo(!use_debug_info)}
        />
      </Menu>
    );
  };

  /**
   * Renders the status of the test run.
   * @param status - The status to render.
   * @returns {string} The status text.
   */
  const getStatusText = (status: StatusKey | "unknown"): string => {
    if (status === "unknown") {
      console.error("Unknown status encountered");
      return t("app.status.unknown") || "Unknown status";
    }
    return t(STATUS_MAP[status]);
  };

  const handleModalResultDismiss = () => {
    console.log("App: ModalResult dismissed via click at time:", Date.now());
    setShowCompletionModalResult(false);
    setTestCompletionData(null);
  };

  return (
    <div className="App">
      <ReloadAlert reload_timeout_s={3} />

      {/* Header */}
      <Navbar
        fixedToTop={true}
        style={{ background: Colors.LIGHT_GRAY4, margin: "auto" }}
      >
        <Navbar.Group align={Alignment.LEFT}>
          <Navbar.Heading id={"main-heading"}>
            <div className={"logo-smol"}></div>
            {wide && (
              <div>
                <b>{ultrawide ? t("app.title") : "HardPy"}</b>
              </div>
            )}
          </Navbar.Heading>

          {wide && <Navbar.Divider />}

          <div
            style={{
              display: "flex",
              flexDirection: wide ? "row" : "column",
              alignItems: "center",
              gap: wide ? "10px" : "5px",
            }}
          >
            <Navbar.Heading
              id={"last-exec-heading"}
              style={{
                margin: 0,
                display: "flex",
                alignItems: "center",
                gap: "5px",
                whiteSpace: "nowrap",
              }}
            >
              <div>{t("app.lastLaunch")}</div>
              <div>{getStatusText(lastRunStatus)}</div>
              <TestStatus
                status={lastRunStatus === "unknown" ? "" : lastRunStatus}
              />
            </Navbar.Heading>

            {use_end_test_sound && (
              <PlaySound key="sound" status={lastRunStatus} />
            )}
            <Navbar.Divider />
            <Navbar.Heading>
              {t("app.duration")}: {lastRunDuration} {t("app.seconds")}
            </Navbar.Heading>
          </div>

          <Navbar.Divider />
        </Navbar.Group>

        <Navbar.Group align={Alignment.RIGHT}>
          <Popover content={renderSettingsMenu()}>
            <Button className="bp3-minimal" icon="cog" />
          </Popover>
        </Navbar.Group>
      </Navbar>

      {/* Tests panel */}
      <div className={Classes.DRAWER_BODY} style={{ marginBottom: "60px" }}>
        {renderDbContent()}
      </div>

      {/* Footer */}

      <div
        className={Classes.DRAWER_FOOTER}
        style={{
          width: "100%",
          display: "flex",
          flexDirection: "row",
          position: "fixed",
          bottom: 0,
          background: Colors.LIGHT_GRAY5,
          margin: "auto",
        }}
      >
        <div
          style={{
            flexDirection: "column",
            flexGrow: 1,
            flexShrink: 1,
            marginTop: "auto",
            marginBottom: "auto",
            padding: "20px",
          }}
        >
          <ProgressView percentage={lastProgress} status={lastRunStatus} />
        </div>
        <div style={{ flexDirection: "column" }}>
          <StartStopButton testing_status={lastRunStatus} />
        </div>
      </div>
      {/* Test Completion ModalResult */}
      <TestCompletionModalResult
        isVisible={showCompletionModalResult}
        testPassed={testCompletionData?.testPassed || false}
        testStopped={testCompletionData?.testStopped || false}
        failedTestCases={testCompletionData?.failedTestCases || []}
        stoppedTestCase={testCompletionData?.stoppedTestCase}
        onDismiss={handleModalResultDismiss}
        onVisibilityChange={handleModalResultVisibilityChange}
        autoDismissPass={
          hardpyConfig?.frontend?.modal_result?.auto_dismiss_pass ?? true
        }
        autoDismissTimeout={
          hardpyConfig?.frontend?.modal_result?.auto_dismiss_timeout ?? 5
        }
      />
    </div>
  );
}

export default App;
