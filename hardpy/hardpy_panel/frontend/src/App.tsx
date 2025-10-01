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
import TestCompletionOverlay from "./hardpy_test_view/TestCompletionOverlay";

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

// Global variable to track overlay visibility with timestamp
let isCompletionOverlayVisible = false;
let lastOverlayDismissTime = 0;
const OVERLAY_DISMISS_COOLDOWN = 100; // ms

/**
 * Sets the global overlay visibility state
 */
export const setCompletionOverlayVisible = (visible: boolean): void => {
  console.log(
    "App: Setting global overlay visibility to",
    visible,
    "at time:",
    Date.now()
  );
  isCompletionOverlayVisible = visible;
  if (!visible) {
    lastOverlayDismissTime = Date.now();
    console.log(
      "App: Set last overlay dismiss time to",
      lastOverlayDismissTime
    );
  }
};

/**
 * Gets the global overlay visibility state
 */
export const getCompletionOverlayVisible = (): boolean => {
  return isCompletionOverlayVisible;
};

/**
 * Checks if we're in cooldown period after overlay dismissal
 */
export const isInOverlayDismissCooldown = (): boolean => {
  const now = Date.now();
  const inCooldown = now - lastOverlayDismissTime < OVERLAY_DISMISS_COOLDOWN;
  console.log(
    "App: Cooldown check - now:",
    now,
    "lastDismiss:",
    lastOverlayDismissTime,
    "inCooldown:",
    inCooldown
  );
  return inCooldown;
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

  // Test completion overlay state
  const [showCompletionOverlay, setShowCompletionOverlay] =
    React.useState(false);
  const [testCompletionData, setTestCompletionData] = React.useState<{
    testPassed: boolean;
    testStopped: boolean;
    failedTestCases: Array<{
      moduleName: string;
      caseName: string;
      assertionMsg?: string;
    }>;
  } | null>(null);

  const startTimeRef = React.useRef<number | null>(null);
  const [timerIntervalId, setTimerIntervalId] =
    React.useState<NodeJS.Timeout | null>(null);

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

  // Handle overlay visibility changes
  const handleOverlayVisibilityChange = React.useCallback(
    (isVisible: boolean) => {
      console.log(
        "App: Overlay visibility change callback, isVisible:",
        isVisible
      );
      setCompletionOverlayVisible(isVisible);
    },
    []
  );

  // Handle keyboard events for overlay dismissal
  React.useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (showCompletionOverlay) {
        console.log("App: Key pressed while overlay visible, key:", event.key);
        if (
          event.key === "Enter" ||
          event.key === " " ||
          event.key === "Escape"
        ) {
          console.log(
            "App: Dismissing overlay via keyboard, preventing default"
          );
          event.preventDefault();
          event.stopPropagation();
          setShowCompletionOverlay(false);
          setTestCompletionData(null);
        }
      }
    };

    if (showCompletionOverlay) {
      console.log(
        "App: Adding keyboard event listener for overlay with capture"
      );
      document.addEventListener("keydown", handleKeyDown, { capture: true });
      return () => {
        console.log("App: Removing keyboard event listener for overlay");
        document.removeEventListener("keydown", handleKeyDown, {
          capture: true,
        });
      };
    }
  }, [showCompletionOverlay]);

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

    // Detect test completion and show overlay (only if enabled in config)
    const prevStatus = lastRunStatus;
    if (
      prevStatus === "run" &&
      (status === "passed" || status === "failed" || status === "stopped") &&
      !showCompletionOverlay
    ) {
      console.log("App: Test completed, showing overlay. Status:", status);
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

      setTestCompletionData({
        testPassed,
        testStopped,
        failedTestCases,
      });
      setShowCompletionOverlay(true);
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

  const handleOverlayDismiss = () => {
    console.log("App: Overlay dismissed via click at time:", Date.now());
    setShowCompletionOverlay(false);
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
      {/* Test Completion Overlay */}
      <TestCompletionOverlay
        isVisible={showCompletionOverlay}
        testPassed={testCompletionData?.testPassed || false}
        testStopped={testCompletionData?.testStopped || false}
        failedTestCases={testCompletionData?.failedTestCases || []}
        onDismiss={handleOverlayDismiss}
        onVisibilityChange={handleOverlayVisibilityChange}
      />
    </div>
  );
}

export default App;
