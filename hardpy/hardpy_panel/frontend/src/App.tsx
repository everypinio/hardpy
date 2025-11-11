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

interface AppConfig {
  frontend?: {
    full_size_button?: boolean;
    sound_on?: boolean;
    manual_tests_selection?: boolean;
    measurement_display?: boolean;
    modal_result?: {
      enable?: boolean;
      auto_dismiss_pass?: boolean;
      auto_dismiss_timeout?: number;
    };
  };
}

/**
 * Checks if the provided status is a valid status key.
 * @param {string} status - The status string to validate
 * @returns {boolean} True if the status is a valid StatusKey, false otherwise
 */
const isValidStatus = (status: string): status is StatusKey => {
  return status in STATUS_MAP;
};

// Global variable to track ModalResult visibility with timestamp
let isCompletionModalResultVisible = false;
let lastModalResultDismissTime = 0;
const MODAL_RESULT_DISMISS_COOLDOWN = 100; // ms

/**
 * Sets the global ModalResult visibility state and updates dismissal timestamp
 * @param {boolean} visible - The visibility state to set
 */
export const setCompletionModalResultVisible = (visible: boolean): void => {
  isCompletionModalResultVisible = visible;
  if (!visible) {
    lastModalResultDismissTime = Date.now();
  }
};

/**
 * Gets the global ModalResult visibility state
 * @returns {boolean} Current visibility state of the completion ModalResult
 */
export const getCompletionModalResultVisible = (): boolean => {
  return isCompletionModalResultVisible;
};

/**
 * Checks if we're in cooldown period after ModalResult dismissal
 * Prevents immediate space key actions after ModalResult is dismissed
 * @returns {boolean} True if within the cooldown period, false otherwise
 */
export const isInModalResultDismissCooldown = (): boolean => {
  const now = Date.now();
  return now - lastModalResultDismissTime < MODAL_RESULT_DISMISS_COOLDOWN;
};

/**
 * Finds the test case that was stopped during test execution
 * Searches through all modules and cases to find the stopped test case
 * @param {TestRunI} testRunData - The test run data to search through
 * @returns {Object|undefined} Object containing module name, case name, and optional assertion message, or undefined if not found
 */
const findStoppedTestCase = (
  testRunData: TestRunI
):
  | { moduleName: string; caseName: string; assertionMsg?: string }
  | undefined => {
  if (!testRunData.modules) return undefined;

  // First, look for explicitly stopped test cases
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

  // If no explicitly stopped case found, return the last failed test case
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
 * Main application component for the HardPy testing interface
 * Provides the main GUI for test execution, monitoring, and result display
 * @param {Object} props - Component properties
 * @param {string} props.syncDocumentId - The id of the PouchDB document to synchronize with
 * @returns {JSX.Element} The main application component
 */
function App({ syncDocumentId }: { syncDocumentId: string }): JSX.Element {
  const { t } = useTranslation();
  const [use_end_test_sound, setUseEndTestSound] = React.useState(false);
  const [use_debug_info, setUseDebugInfo] = React.useState(false);
  const [appConfig, setAppConfig] = React.useState<AppConfig | null>(null);
  const [isConfigLoaded, setIsConfigLoaded] = React.useState(false);

  const [lastRunStatus, setLastRunStatus] = React.useState<
    StatusKey | "unknown"
  >("ready");
  const [lastProgress, setProgress] = React.useState(0);
  const [isAuthenticated, setIsAuthenticated] = React.useState(true);
  const [lastRunDuration, setLastRunDuration] = React.useState<number>(0);

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
  const [selectedTests, setSelectedTests] = React.useState<string[]>([]);
  const [allTests, setAllTests] = React.useState<string[]>([]);

  /**
   * Loads HardPy configuration from the backend API on component mount
   * Initializes frontend configurations
   */
  React.useEffect(() => {
    const loadConfig = async () => {
      try {
        const response = await fetch("/api/hardpy_config");
        const config = await response.json();
        setAppConfig(config);

        // Initialize sound setting from TOML config
        if (config.frontend?.sound_on !== undefined) {
          setUseEndTestSound(config.frontend.sound_on);
        }

        if (config.frontend?.manual_tests_selection) {
          const savedTests = localStorage.getItem("hardpy_selected_tests");
          if (savedTests) {
            setSelectedTests(JSON.parse(savedTests));
          }
        }
      } catch (error) {
        console.error("Failed to load HardPy config:", error);
      } finally {
        setIsConfigLoaded(true);
      }
    };

    loadConfig();
  }, []);

  /**
   * Custom hook to determine if the window width is greater than a specified size
   * @param {number} size - The width threshold to compare against in pixels
   * @returns {boolean} True if the window width is greater than the specified size, otherwise false
   */
  const useWindowWide = (size: number): boolean => {
    const [width, setWidth] = React.useState(0);

    React.useEffect(() => {
      /**
       * Updates the current window width state
       */
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

  /**
   * Handles ModalResult visibility changes and updates global state
   */
  const handleModalResultVisibilityChange = React.useCallback(
    (isVisible: boolean) => {
      setCompletionModalResultVisible(isVisible);
    },
    []
  );

  /**
   * Handles keyboard events for ModalResult dismissal
   * Prevents space key propagation and dismisses ModalResult on any key press
   */
  React.useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (showCompletionModalResult) {
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation();

        setShowCompletionModalResult(false);
        setTestCompletionData(null);

        // Additional handling for space key to prevent focus issues
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

  /**
   * Manages test execution timer and duration calculation
   * Updates the test duration every second while test is running
   */
  React.useEffect(() => {
    if (lastRunStatus === "run") {
      if (startTimeRef.current !== null) {
        /**
         * Updates the test duration by calculating difference from start time
         */
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
   * Finds the index of a row in a list based on its ID
   * @param {Array} rows - The list of rows to search
   * @param {string} searchTerm - The ID to search for
   * @returns {number} The index of the row, or -1 if not found
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

  /**
   * Monitors database changes and updates application state accordingly
   * Handles test status changes, progress updates, and ModalResult display
   */
  React.useEffect(() => {
    if (rows.length === 0) return;

    const index = findRowIndex(rows, syncDocumentId);
    if (index === -1) return;
    const db_row = rows[index].doc as TestRunI;
    const status = db_row.status || "";
    const progress = db_row.progress || 0;

    // Update run status if changed
    if (status !== lastRunStatus) {
      setLastRunStatus(isValidStatus(status) ? status : "unknown");
    }

    // Update progress if changed
    if (progress !== lastProgress) {
      setProgress(progress);
    }

    // Update start time and calculate duration
    if (db_row.start_time) {
      startTimeRef.current = db_row.start_time;

      if (db_row.stop_time && status !== "run") {
        const duration = db_row.stop_time - db_row.start_time;
        if (duration !== lastRunDuration) {
          setLastRunDuration(duration);
        }
      }
    }

    // Extract all available tests
    if (db_row.modules) {
      const allAvailableTests: string[] = [];
      Object.entries(db_row.modules).forEach(([moduleId, module]) => {
        if (module.cases) {
          Object.keys(module.cases).forEach((caseId) => {
            allAvailableTests.push(`${moduleId}::${caseId}`);
          });
        }
      });
      setAllTests(allAvailableTests);

      // If manual selection is enabled and no tests are selected yet, select all by default
      if (
        appConfig?.frontend?.manual_tests_selection &&
        selectedTests.length === 0
      ) {
        setSelectedTests(allAvailableTests);
      }
    }

    // --- Test completion logic starts here ---
    const prevStatus = lastRunStatus;
    const ModalResultEnable =
      appConfig?.frontend?.modal_result?.enable ?? false;

    // Close ModalResult when test starts running (status changes to "run")
    if (prevStatus !== "run" && status === "run" && showCompletionModalResult) {
      setShowCompletionModalResult(false);
      setTestCompletionData(null);
    }

    // Show ModalResult on test completion
    if (
      ModalResultEnable &&
      prevStatus === "run" &&
      (status === "passed" || status === "failed" || status === "stopped") &&
      !showCompletionModalResult
    ) {
      const testPassed = status === "passed";
      const testStopped = status === "stopped";
      const failedTestCases: Array<{
        moduleName: string;
        caseName: string;
        assertionMsg?: string;
      }> = [];

      if (!testPassed && !testStopped && db_row.modules) {
        Object.entries(db_row.modules).forEach(([moduleId, module]) => {
          if (module.cases) {
            Object.entries(module.cases).forEach(([caseId, testCase]) => {
              if (testCase.status === "failed") {
                failedTestCases.push({
                  moduleName: module.name || moduleId,
                  caseName: testCase.name || caseId,
                  assertionMsg: testCase.assertion_msg || undefined,
                });
              }
            });
          }
        });
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

    // Handle authentication state based on database connection
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
    appConfig,
    showCompletionModalResult,
    syncDocumentId,
    selectedTests.length,
  ]);

  /**
   * Handles selection change from SuiteList
   */
  const handleTestsSelectionChange = (tests: string[]) => {
    setSelectedTests(tests);
    localStorage.setItem("hardpy_selected_tests", JSON.stringify(tests));
  };

  /**
   * Renders the database content including test suites and debug information
   * @returns {JSX.Element} The rendered database content component
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
                onTestsSelectionChange={handleTestsSelectionChange}
                selectedTests={selectedTests}
                selectionSupported={
                  appConfig?.frontend?.manual_tests_selection || false
                }
                measurementDisplay={appConfig?.frontend?.measurement_display}
              />
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
   * Renders the settings menu with sound and debug options
   * @returns {JSX.Element} The settings menu component
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
   * Renders the status text of the test run based on the current status
   * @param {StatusKey | "unknown"} status - The status to render
   * @returns {string} The translated status text
   */
  const getStatusText = (status: StatusKey | "unknown"): string => {
    if (status === "unknown") {
      return t("app.status.unknown") || "Unknown status";
    }
    return t(STATUS_MAP[status]);
  };

  const useBigButton = appConfig?.frontend?.full_size_button !== false;

  /**
   * Handles ModalResult dismissal by hiding it and clearing completion data
   */
  const handleModalResultDismiss = () => {
    setShowCompletionModalResult(false);
    setTestCompletionData(null);
  };

  return (
    <div className="App">
      <ReloadAlert reload_timeout_s={3} />

      {/* Header with navigation and status information */}
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
              gap: wide ? "10px" : "2px",
              fontSize: wide ? "inherit" : "12px",
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
                flexWrap: wide ? "nowrap" : "wrap",
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

            {wide && <Navbar.Divider />}

            <Navbar.Heading style={{ whiteSpace: "nowrap" }}>
              {t("app.duration")}: {lastRunDuration}s
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

      {/* Main content area with test suites and results */}
      <div
        className={Classes.DRAWER_BODY}
        style={{
          marginBottom: "60px",
          paddingBottom: useBigButton ? "120px" : "80px",
        }}
      >
        {renderDbContent()}
      </div>

      {/* Footer with progress bar and control buttons */}
      {isConfigLoaded && (
        <div
          className={Classes.DRAWER_FOOTER}
          style={{
            width: "100%",
            display: "flex",
            flexDirection: "column",
            position: "fixed",
            bottom: 0,
            background: Colors.LIGHT_GRAY5,
            margin: "auto",
          }}
        >
          {useBigButton ? (
            <>
              <div
                style={{
                  width: "100%",
                  padding: "10px 20px 0px 20px",
                }}
              >
                <ProgressView
                  percentage={lastProgress}
                  status={lastRunStatus}
                />
              </div>
              <div
                style={{
                  width: "100%",
                  padding: "10px 20px",
                  display: "flex",
                  justifyContent: "center",
                }}
              >
                <div style={{ width: "100%" }}>
                  <StartStopButton
                    testing_status={lastRunStatus}
                    useBigButton={true}
                    selectedTests={selectedTests}
                  />
                </div>
              </div>
            </>
          ) : (
            <div
              style={{
                width: "100%",
                display: "flex",
                flexDirection: "row",
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
                <ProgressView
                  percentage={lastProgress}
                  status={lastRunStatus}
                />
              </div>
              <div style={{ flexDirection: "column" }}>
                <StartStopButton
                  testing_status={lastRunStatus}
                  useBigButton={false}
                  selectedTests={selectedTests}
                />
              </div>
            </div>
          )}
        </div>
      )}

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
          appConfig?.frontend?.modal_result?.auto_dismiss_pass ?? true
        }
        autoDismissTimeout={
          appConfig?.frontend?.modal_result?.auto_dismiss_timeout ?? 5
        }
      />
    </div>
  );
}

export default App;
