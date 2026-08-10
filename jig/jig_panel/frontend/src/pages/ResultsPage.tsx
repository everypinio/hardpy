// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { Outlet, useMatch, useNavigate } from "react-router";
import { useTranslation } from "react-i18next";

import { Button } from "@/components/ui/button";
import TestHistory from "@/jig_test_view/TestHistory";
import { toHistoryEntries } from "@/lib/testHistory";
import { usePanel } from "@/panel/PanelContext";

/** How many more history runs are revealed each time "show more" is clicked. */
const HISTORY_PAGE_SIZE = 5;

/**
 * Results page: past-run history list with an optional nested detail outlet.
 */
export function ResultsPage(): React.ReactElement {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const detailMatch = useMatch("/results/:runId");
  const { rows, syncDocumentId } = usePanel();
  const [historyDisplayCount, setHistoryDisplayCount] =
    React.useState(HISTORY_PAGE_SIZE);

  const filteredRows = toHistoryEntries(rows, syncDocumentId);
  const historyEntries = filteredRows.slice(0, historyDisplayCount);
  const selectedHistoryId = detailMatch?.params.runId ?? null;

  return (
    <div className="px-4 py-6">
      <div className="mb-4">
        <h1 className="text-2xl font-semibold tracking-tight">
          {t("results.title")}
        </h1>
      </div>
      <div className="flex min-w-0 flex-col gap-5 lg:flex-row">
        <div className="flex min-w-0 flex-[1_1_22rem] flex-col gap-3">
          <TestHistory
            history={historyEntries}
            selectedHistoryId={selectedHistoryId}
            onSelectHistoryRun={(id) => {
              navigate(`/results/${id}`);
            }}
          />
          {filteredRows.length > historyDisplayCount && (
            <Button
              variant="ghost"
              className="w-full"
              onClick={() =>
                setHistoryDisplayCount(
                  historyDisplayCount + HISTORY_PAGE_SIZE
                )
              }
            >
              {t("history.showMore")}
            </Button>
          )}
        </div>
        <div className="min-w-0 flex-[2_1_0%]">
          <Outlet />
        </div>
      </div>
    </div>
  );
}

export default ResultsPage;
