// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import {
  Ban,
  Bug,
  FolderKanban,
  MousePointerClick,
  Settings,
  Volume2,
  VolumeX,
} from "lucide-react";
import {
  Link,
  NavLink,
  Navigate,
  Route,
  Routes,
  useLocation,
  useNavigate,
} from "react-router";
import { useTranslation } from "react-i18next";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Separator } from "@/components/ui/separator";
import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import {
  DisplayStatus,
  statusLabel,
  toDisplayStatus,
} from "@/lib/testStatus";
import { cn } from "@/lib/utils";
import {
  AppConfig,
  PanelProvider,
  type PanelContextValue,
} from "@/panel/PanelContext";
import GroupPage from "@/pages/GroupPage";
import ResultsPage from "@/pages/ResultsPage";
import RunDetailPage from "@/pages/RunDetailPage";
import TestsPage from "@/pages/TestsPage";

import StartStopButton from "./button/StartStop";
import { TestRunI } from "./jig_test_view/SuiteList";
import DialogBoxHost from "./jig_test_view/DialogBoxHost";
import OperatorMessageHost from "./jig_test_view/OperatorMessageHost";
import TestStatus from "./jig_test_view/TestStatus";
import ReloadAlert from "./restart_alert/RestartAlert";
import PlaySound from "./jig_test_view/PlaySound";
import TestConfigOverlay from "./jig_test_view/TestConfigOverlay";
import TestCompletionModalResult from "./jig_test_view/TestCompletionModalResult";
import StorageStatusMenu from "./storage/StorageStatusMenu";

import { useStorageData } from "./hooks/useStorageData";
import { useStorageStatus } from "./hooks/useStorageStatus";

import "./App.css";

const WINDOW_WIDTH_THRESHOLDS = {
  ULTRAWIDE: 490,
  WIDE: 400,
};

/**
 * Renders a standalone card carrying a connection or database message.
 * @param {Object} props - The component properties
 * @param {string} props.title - The headline shown to the operator
 * @param {string} [props.detail] - An optional technical detail below the headline
 * @returns {JSX.Element} The rendered message card
 */
function PanelMessage({
  title,
  detail,
}: {
  title: string;
  detail?: string;
}): JSX.Element {
  return (
    <Card className="mx-auto mt-8 max-w-xl">
      <CardContent className="space-y-2">
        <h2 className="text-xl font-semibold tracking-tight">{title}</h2>
        {detail && <p className="text-sm text-muted-foreground">{detail}</p>}
      </CardContent>
    </Card>
  );
}

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
  if (!testRunData.modules) {
    return undefined;
  }

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
  let lastFailedTestCase: {
    moduleName: string;
    caseName: string;
    assertionMsg?: string;
  } | null = null;
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

  return lastFailedTestCase || undefined;
};

/**
 * Main application component for the Jig testing interface
 * Provides the main GUI for test execution, monitoring, and result display
 * @param {Object} props - Component properties
 * @param {string} props.syncDocumentId - The id of the PouchDB document to synchronize with
 * @returns {JSX.Element} The main application component
 */
function App({ syncDocumentId }: { syncDocumentId: string }): JSX.Element {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();
  const [use_end_test_sound, setUseEndTestSound] = React.useState(false);
  const [use_debug_info, setUseDebugInfo] = React.useState(false);
  const [appConfig, setAppConfig] = React.useState<AppConfig | null>(null);
  const [isConfigLoaded, setIsConfigLoaded] = React.useState(false);
  const [manualCollectMode, setManualCollectMode] = React.useState(false);

  const [lastRunStatus, setLastRunStatus] =
    React.useState<DisplayStatus>("ready");
  const [isAuthenticated, setIsAuthenticated] = React.useState(true);
  const [lastRunDuration, setLastRunDuration] = React.useState<number>(0);

  // Test config selection state
  const [showConfigOverlay, setShowConfigOverlay] = React.useState(false);

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
  /** Tells whether the run in flight covers a subset of the tests. */
  const partialRunRef = React.useRef(false);
  const [timerIntervalId, setTimerIntervalId] =
    React.useState<NodeJS.Timeout | null>(null);
  const [allTests, setAllTests] = React.useState<string[]>([]);
  const [previousTestStructure, setPreviousTestStructure] =
    React.useState<string>("");
  let [selectedTests, setSelectedTests] = React.useState<string[]>([]);

  /**
   * Loads Jig configuration from the backend API on component mount
   * Initializes frontend configurations
   */
  React.useEffect(() => {
    const loadConfig = async () => {
      try {
        const response = await fetch("/api/jig_config");
        const config = await response.json();
        setAppConfig(config);

        // Initialize sound setting from TOML config
        if (config.frontend?.sound_on !== undefined) {
          setUseEndTestSound(config.frontend.sound_on);
        }

        // Load manual collect mode state
        const manualCollectResponse = await fetch("/api/manual_collect_mode");
        const manualCollectData = await manualCollectResponse.json();
        setManualCollectMode(manualCollectData.manual_collect_mode);

        if (config.frontend?.manual_collect) {
          const savedTests = localStorage.getItem("jig_selected_tests");
          if (savedTests) {
            setSelectedTests(JSON.parse(savedTests));
          }
        }

        // Show overlay if no current test config is selected
        if (
          !config.current_test_config &&
          config.test_configs &&
          config.test_configs.length > 0
        ) {
          setShowConfigOverlay(true);
        }
      } catch (error) {
        console.error("Failed to load Jig config:", error);
      } finally {
        setIsConfigLoaded(true);
      }
    };

    loadConfig();
  }, []);

  /**
   * Toggles manual collect mode
   */
  const toggleManualCollectMode = async () => {
    try {
      const newMode = !manualCollectMode;
      const response = await fetch("/api/manual_collect_mode", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ enabled: newMode }),
      });

      const result = await response.json();
      if (result.status === "success") {
        setManualCollectMode(newMode);
      }

      if (result.manual_collect_mode === false) {
        const testsToSend = selectedTests || [];
        const testsJsonString = JSON.stringify(testsToSend);

        fetch(`/api/selected_tests`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: testsJsonString,
        }).then((response) => response.json());
      }
    } catch (error) {
      console.error("Failed to toggle manual collect mode:", error);
    }
  };

  /**
   * Filters selected tests to only include those that exist in current test structure
   */
  const filterSelectedTests = React.useCallback((currentAllTests: string[]) => {
    setSelectedTests((prevSelected) => {
      const filtered = prevSelected.filter((test) =>
        currentAllTests.includes(test)
      );

      if (JSON.stringify(filtered) !== JSON.stringify(prevSelected)) {
        localStorage.setItem("jig_selected_tests", JSON.stringify(filtered));
      }

      return filtered;
    });
  }, []);

  /**
   * Handler for test config selection
   */
  const handleConfigSelection = async (configName: string) => {
    // Prevent config changes during test runs
    if (lastRunStatus === "run") {
      console.warn("Cannot change test config while test is running");
      return;
    }

    try {
      // Update the backend with the selected config
      const response = await fetch(
        `/api/set_test_config/${encodeURIComponent(configName)}`,
        {
          method: "POST",
        }
      );

      if (response.ok) {
        // Update local state
        setAppConfig((prev) =>
          prev ? { ...prev, current_test_config: configName } : null
        );
        setShowConfigOverlay(false);
      } else {
        console.error("Failed to set test config");
      }
    } catch (error) {
      console.error("Error setting test config:", error);
    }
  };

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
   * Close config overlay when test starts running
   */
  React.useEffect(() => {
    if (lastRunStatus === "run" && showConfigOverlay) {
      setShowConfigOverlay(false);
    }
  }, [lastRunStatus, showConfigOverlay]);

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

  const { rows, state, loading, error } = useStorageData();
  const {
    data: storageStatus,
    loading: storageStatusLoading,
    error: storageStatusError,
  } = useStorageStatus();

  /**
   * Monitors database changes and updates application state accordingly
   * Handles test status changes, progress updates, and ModalResult display
   */
  React.useEffect(() => {
    if (rows.length === 0) {
      return;
    }

    const index = findRowIndex(rows, syncDocumentId);
    if (index === -1) {
      return;
    }
    const db_row = rows[index].doc as TestRunI;
    const status = db_row.status || "";

    // Update run status if changed
    if (status !== lastRunStatus) {
      setLastRunStatus(toDisplayStatus(status));
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

    // Extract all available tests and detect structure changes
    if (db_row.modules) {
      const allAvailableTests: string[] = [];
      Object.entries(db_row.modules).forEach(([moduleId, module]) => {
        if (module.cases) {
          Object.keys(module.cases).forEach((caseId) => {
            // Safe check for case existence
            if (module.cases[caseId]) {
              allAvailableTests.push(`${moduleId}::${caseId}`);
            }
          });
        }
      });

      const currentStructure = JSON.stringify(allAvailableTests);

      // Sort selected tests by Available tests order
      const selectedTestsSet = new Set(selectedTests);
      selectedTests = allAvailableTests.filter((test) =>
        selectedTestsSet.has(test)
      );

      if (currentStructure !== previousTestStructure) {
        setAllTests(allAvailableTests);
        setPreviousTestStructure(currentStructure);

        // Filter selected tests when test structure changes
        filterSelectedTests(allAvailableTests);
      }

      // If manual selection is enabled and no tests are selected yet, select all by default
      if (
        appConfig?.frontend?.manual_collect &&
        selectedTests.length === 0 &&
        allAvailableTests.length > 0
      ) {
        setSelectedTests(allAvailableTests);
        localStorage.setItem(
          "jig_selected_tests",
          JSON.stringify(allAvailableTests)
        );
      }
    }

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
    lastRunDuration,
    isAuthenticated,
    appConfig,
    showCompletionModalResult,
    syncDocumentId,
    selectedTests.length,
    previousTestStructure,
    filterSelectedTests,
  ]);

  /**
   * Handles selection change from SuiteList
   */
  const handleTestsSelectionChange = (tests: string[]) => {
    setSelectedTests(tests);
    localStorage.setItem("jig_selected_tests", JSON.stringify(tests));
  };

  /**
   * Clears selected tests when starting a new test run
   */
  const handleTestRunStart = React.useCallback(() => {
    partialRunRef.current = false;
    filterSelectedTests(allTests);
  }, [allTests, filterSelectedTests]);

  /**
   * Starts a partial run limited to the modules of one section.
   *
   * `runName` names what the operator ran, a section path or a module path, and
   * is reported next to the test name in the results.
   */
  const handleRunSection = React.useCallback(
    (moduleIds: string[], runName: string) => {
      if (manualCollectMode || moduleIds.length === 0) {
        return;
      }
      handleTestRunStart();
      partialRunRef.current = true;
      const params = new URLSearchParams();
      for (const moduleId of moduleIds) {
        params.append("tests", moduleId);
      }
      params.append("run_name", runName);
      fetch(`/api/start?${params.toString()}`);
    },
    [handleTestRunStart, manualCollectMode]
  );

  /**
   * When a full run starts from a group page (footer Start), leave the group
   * view so the operator sees the full suite.
   */
  React.useEffect(() => {
    if (
      lastRunStatus === "run" &&
      !partialRunRef.current &&
      location.pathname.startsWith("/group/")
    ) {
      navigate("/");
    }
  }, [lastRunStatus, location.pathname, navigate]);

  /**
   * Renders routed panel content once the live document is available.
   */
  const renderDbContent = (): JSX.Element => {
    const dbErrorMessage = (
      <PanelMessage title={t("app.dbError")} detail={error?.message} />
    );

    if (loading && rows.length === 0) {
      return <PanelMessage title={t("app.connection")} />;
    }

    if (state === "error") {
      return dbErrorMessage;
    }

    if (rows.length === 0) {
      return <PanelMessage title={t("app.noEntries")} />;
    }

    const index = findRowIndex(rows, syncDocumentId);
    if (index === -1) {
      return dbErrorMessage;
    }

    const document_row = rows[index];
    if (!document_row) {
      return dbErrorMessage;
    }

    const testRunData: TestRunI = document_row.doc as TestRunI;
    const panelValue: PanelContextValue = {
      testRunData,
      rows,
      syncDocumentId,
      appConfig,
      manualCollectMode,
      selectedTests,
      onTestsSelectionChange: handleTestsSelectionChange,
      ultrawide,
      useDebugInfo: use_debug_info,
      runSection: handleRunSection,
      lastRunStatus,
    };

    const historyEnabled = appConfig?.frontend?.test_history !== false;

    return (
      <PanelProvider value={panelValue}>
        <Routes>
          <Route path="/" element={<TestsPage />} />
          <Route path="/group/*" element={<GroupPage />} />
          {historyEnabled ? (
            <Route path="/results" element={<ResultsPage />}>
              <Route path=":runId" element={<RunDetailPage />} />
            </Route>
          ) : (
            <Route path="/results/*" element={<Navigate to="/" replace />} />
          )}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
        <DialogBoxHost />
        <OperatorMessageHost />
      </PanelProvider>
    );
  };

  /**
   * Renders the settings menu with sound and debug options
   * @returns {JSX.Element} The settings menu items
   */
  const renderSettingsMenu = (): JSX.Element => {
    return (
      <>
        <DropdownMenuItem
          id="use_end_test_sound"
          onSelect={(event) => {
            event.preventDefault();
            setUseEndTestSound(!use_end_test_sound);
          }}
        >
          {use_end_test_sound ? <Volume2 /> : <VolumeX />}
          {use_end_test_sound ? t("app.soundOff") : t("app.soundOn")}
        </DropdownMenuItem>
        <DropdownMenuItem
          id="use_debug_info"
          onSelect={(event) => {
            event.preventDefault();
            setUseDebugInfo(!use_debug_info);
          }}
        >
          <Bug />
          {use_debug_info ? t("app.debugOff") : t("app.debugOn")}
        </DropdownMenuItem>
        {appConfig?.frontend?.manual_collect && (
          <DropdownMenuItem
            onSelect={(event) => {
              event.preventDefault();
              toggleManualCollectMode();
            }}
          >
            {manualCollectMode ? <Ban /> : <MousePointerClick />}
            {manualCollectMode
              ? t("app.manualCollectOff")
              : t("app.manualCollectOn")}
          </DropdownMenuItem>
        )}
      </>
    );
  };

  const isTestRunning = lastRunStatus === "run";

  /**
   * Handles ModalResult dismissal by hiding it and clearing completion data
   */
  const handleModalResultDismiss = () => {
    setShowCompletionModalResult(false);
    setTestCompletionData(null);
  };

  return (
    <TooltipProvider>
      <div className="App">
        <ReloadAlert reload_timeout_s={3} />
        <Toaster position="bottom-right" />

        {/* Header with navigation and status information */}
        <header
          id="panel-header"
          className="fixed inset-x-0 top-0 z-20 flex h-[50px] items-center gap-2 border-b bg-card px-4 shadow-sm"
        >
          <Link
            to="/"
            id="main-heading"
            className="flex items-center gap-2 text-inherit no-underline"
          >
            <div className="logo-smol" />
            {wide && (
              <span className="font-semibold">
                {ultrawide ? t("app.title") : "Jig"}
              </span>
            )}
          </Link>

          {wide && <Separator orientation="vertical" className="mx-1 h-6" />}

          <nav className="flex items-center gap-1 text-sm">
            <NavLink
              to="/"
              end
              className={({ isActive }) =>
                cn(
                  "rounded-md px-2 py-1 font-medium transition-colors",
                  isActive
                    ? "bg-accent text-accent-foreground"
                    : "text-muted-foreground hover:text-foreground"
                )
              }
            >
              {t("nav.tests")}
            </NavLink>
            {appConfig?.frontend?.test_history !== false && (
              <NavLink
                to="/results"
                className={({ isActive }) =>
                  cn(
                    "rounded-md px-2 py-1 font-medium transition-colors",
                    isActive
                      ? "bg-accent text-accent-foreground"
                      : "text-muted-foreground hover:text-foreground"
                  )
                }
              >
                {t("nav.results")}
              </NavLink>
            )}
          </nav>

          {wide && <Separator orientation="vertical" className="mx-1 h-6" />}

          <div
            className={cn(
              "flex items-center",
              wide ? "flex-row gap-2.5 text-sm" : "flex-col gap-0.5 text-xs"
            )}
          >
            <div className="flex flex-wrap items-center gap-1.5 whitespace-nowrap">
              <span className="text-muted-foreground">
                {t("app.lastLaunch")}
              </span>
              <span className="font-medium">
                {statusLabel(lastRunStatus, t)}
              </span>
              <TestStatus status={lastRunStatus} />
            </div>

            {use_end_test_sound && (
              <PlaySound key="sound" status={lastRunStatus} />
            )}

            {wide && <Separator orientation="vertical" className="h-6" />}

            <span className="whitespace-nowrap text-muted-foreground">
              {t("app.duration")}: {lastRunDuration}
              {t("app.seconds")}
            </span>
          </div>

          <div className="ml-auto flex items-center gap-1">
            {isConfigLoaded && (
              <StartStopButton
                testing_status={lastRunStatus}
                compact={true}
                manualCollectMode={manualCollectMode}
                onTestRunStart={handleTestRunStart}
              />
            )}
            {appConfig && appConfig.current_test_config && (
              <Button
                variant="outline"
                disabled={isTestRunning}
                onClick={() => setShowConfigOverlay(true)}
              >
                <FolderKanban aria-hidden="true" />
                {appConfig.current_test_config}
              </Button>
            )}
            <StorageStatusMenu
              data={storageStatus}
              loading={storageStatusLoading}
              error={storageStatusError}
              jigConfig={appConfig}
            />
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="ghost"
                  size="icon"
                  aria-label={t("app.settings")}
                >
                  <Settings aria-hidden="true" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56">
                {renderSettingsMenu()}
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </header>

        {/* Main content area with test suites and results */}
        <main id="panel-content" className="pt-[50px] pb-6">
          {renderDbContent()}
        </main>

        {/* Test Config Selection Overlay */}
        {appConfig && (
          <TestConfigOverlay
            isOpen={showConfigOverlay}
            testConfigs={appConfig.test_configs || []}
            currentConfig={appConfig.current_test_config}
            isTestRunning={isTestRunning}
            onSelect={handleConfigSelection}
            onClose={() => setShowConfigOverlay(false)}
          />
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
    </TooltipProvider>
  );
}

export default App;
