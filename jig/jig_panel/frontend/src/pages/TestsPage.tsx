// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";

import { Card, CardContent } from "@/components/ui/card";
import SuiteList from "@/jig_test_view/SuiteList";
import { isRunInFlight, toDisplayStatus } from "@/lib/testStatus";
import { usePanel } from "@/panel/PanelContext";

/**
 * Default page listing every collected test module, grouped by section.
 */
export function TestsPage(): React.ReactElement {
  const {
    testRunData,
    appConfig,
    manualCollectMode,
    selectedTests,
    onTestsSelectionChange,
    ultrawide,
    useDebugInfo,
    runSection,
    consumePendingRecollect,
    lastRunStatus,
  } = usePanel();

  React.useEffect(() => {
    if (isRunInFlight(toDisplayStatus(lastRunStatus))) {
      return;
    }
    if (!consumePendingRecollect()) {
      return;
    }
    fetch("/api/collect");
  }, [consumePendingRecollect, lastRunStatus]);

  return (
    <div className="px-4 py-6">
      <div className="flex flex-row gap-5">
        {(ultrawide || !useDebugInfo) && (
          <Card className="min-w-0 flex-[3_1_0%] py-5">
            <CardContent className="px-5">
              <SuiteList
                db_state={testRunData}
                defaultClose={!ultrawide}
                onTestsSelectionChange={onTestsSelectionChange}
                selectedTests={selectedTests}
                selectionSupported={
                  (appConfig?.frontend?.manual_collect || false) &&
                  manualCollectMode
                }
                currentTestConfig={appConfig?.current_test_config}
                measurementDisplay={appConfig?.frontend?.measurement_display}
                manualCollectMode={manualCollectMode}
                autoScroll={appConfig?.frontend?.auto_scroll || false}
                onRunSection={runSection}
              />
            </CardContent>
          </Card>
        )}
        {useDebugInfo && (
          <Card className="min-w-0 flex-1 py-5">
            <CardContent className="px-5">
              <pre className="overflow-x-auto text-xs">
                {JSON.stringify(testRunData, null, 2)}
              </pre>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}

export default TestsPage;
