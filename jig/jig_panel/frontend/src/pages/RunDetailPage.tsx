// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { useParams } from "react-router";
import { useTranslation } from "react-i18next";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import SuiteList from "@/jig_test_view/SuiteList";
import type { TestRunI } from "@/jig_test_view/SuiteList";
import { usePanel } from "@/panel/PanelContext";

/**
 * Read-only detail view for one past run, nested under the results page.
 */
export function RunDetailPage(): React.ReactElement {
  const { t } = useTranslation();
  const { runId } = useParams();
  const { rows, appConfig, manualCollectMode, ultrawide } = usePanel();

  const selectedHistoryRow = runId
    ? (rows.find((row) => row.id === runId)?.doc as TestRunI | undefined)
    : undefined;

  if (!selectedHistoryRow) {
    return (
      <Card className="py-4">
        <CardContent className="px-4">
          <p className="text-sm text-muted-foreground">
            {t("history.unknownRun")}
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="gap-4 py-4">
      <CardHeader className="px-4">
        <CardTitle className="text-base">{t("history.detailTitle")}</CardTitle>
      </CardHeader>
      <CardContent className="px-4">
        <SuiteList
          db_state={selectedHistoryRow}
          defaultClose={!ultrawide}
          selectionSupported={false}
          selectedTests={[]}
          currentTestConfig={appConfig?.current_test_config}
          measurementDisplay={appConfig?.frontend?.measurement_display}
          manualCollectMode={manualCollectMode}
        />
      </CardContent>
    </Card>
  );
}

export default RunDetailPage;
