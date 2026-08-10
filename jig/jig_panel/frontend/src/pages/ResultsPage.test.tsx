// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import { cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, test, vi } from "vitest";
import i18n from "i18next";
import { I18nextProvider, initReactI18next } from "react-i18next";
import { createMemoryRouter, RouterProvider } from "react-router";

import type { PanelContextValue } from "@/panel/PanelContext";
import { PanelProvider } from "@/panel/PanelContext";
import { ResultsPage } from "./ResultsPage";
import { RunDetailPage } from "./RunDetailPage";

vi.mock("@/jig_test_view/SuiteList", () => ({
  default: ({ db_state }: { db_state: { name?: string } }) => (
    <div data-testid="run-detail">{db_state.name}</div>
  ),
}));

async function renderResults(initialPath = "/results") {
  if (!i18n.isInitialized) {
    await i18n.use(initReactI18next).init({
      lng: "en",
      resources: {
        en: {
          translation: {
            results: { title: "Results" },
            history: {
              title: "Test history",
              detailTitle: "Test run details",
              columns: {
                runName: "Run name",
                startTime: "Start time",
                result: "Result",
                serialNumber: "Serial number",
                details: "Details",
              },
              viewDetails: "View details",
              selected: "Selected",
              unknownRun: "Unnamed run",
              showMore: "Show more",
            },
            app: {
              status: {
                ready: "Ready",
                run: "Run",
                passed: "Pass",
                failed: "Fail",
                stopped: "Stopped",
                unknown: "Unknown",
              },
            },
          },
        },
      },
    });
  }

  const value: PanelContextValue = {
    testRunData: { name: "Live", status: "ready" },
    rows: [
      {
        id: "localhost_8000",
        key: "localhost_8000",
        value: { rev: "1" },
        doc: { name: "Live", status: "ready", start_time: 100 },
      },
      {
        id: "111",
        key: "111",
        value: { rev: "1" },
        doc: {
          name: "Past run",
          status: "passed",
          start_time: 90,
          modules: {},
        },
      },
    ],
    syncDocumentId: "localhost_8000",
    appConfig: null,
    manualCollectMode: false,
    selectedTests: [],
    onTestsSelectionChange: () => undefined,
    ultrawide: true,
    useDebugInfo: false,
    runSection: vi.fn(),
    lastRunStatus: "ready",
  };

  const router = createMemoryRouter(
    [
      {
        path: "/results",
        element: <ResultsPage />,
        children: [{ path: ":runId", element: <RunDetailPage /> }],
      },
    ],
    { initialEntries: [initialPath] }
  );

  return render(
    <I18nextProvider i18n={i18n}>
      <PanelProvider value={value}>
        <RouterProvider router={router} />
      </PanelProvider>
    </I18nextProvider>
  );
}

describe("ResultsPage", () => {
  afterEach(() => {
    cleanup();
  });

  test(`given a history entry,
 when View details is clicked,
 then the detail route renders that run`, async () => {
    await renderResults("/results");

    await userEvent.click(screen.getByRole("button", { name: "View details" }));

    await waitFor(() => {
      expect(screen.getByTestId("run-detail")).toHaveTextContent("Past run");
    });
  });

  test(`given a results detail route,
 when the page is rendered,
 then that run's detail is shown`, async () => {
    await renderResults("/results/111");

    expect(screen.getByTestId("run-detail")).toHaveTextContent("Past run");
  });
});
