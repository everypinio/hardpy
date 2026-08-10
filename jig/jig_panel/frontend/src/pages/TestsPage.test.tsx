// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import { cleanup, render } from "@testing-library/react";
import { afterEach, describe, expect, test, vi } from "vitest";

import type { PanelContextValue } from "@/panel/PanelContext";
import { PanelProvider } from "@/panel/PanelContext";
import { TestsPage } from "./TestsPage";

vi.mock("@/jig_test_view/SuiteList", () => ({
  default: () => <div data-testid="suite-list" />,
}));

function renderTestsPage(overrides: Partial<PanelContextValue> = {}) {
  const value: PanelContextValue = {
    testRunData: { name: "Demo", status: "ready", modules: {} },
    rows: [],
    syncDocumentId: "localhost_8000",
    appConfig: null,
    manualCollectMode: false,
    selectedTests: [],
    onTestsSelectionChange: () => undefined,
    ultrawide: true,
    useDebugInfo: false,
    runSection: vi.fn(),
    consumePendingRecollect: () => false,
    lastRunStatus: "ready",
    ...overrides,
  };

  return render(
    <PanelProvider value={value}>
      <TestsPage />
    </PanelProvider>
  );
}

describe("TestsPage", () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  test(`given a pending re-collect and no run in flight,
 when the page mounts,
 then /api/collect is fetched`, () => {
    const fetchMock = vi.fn().mockResolvedValue({});
    vi.stubGlobal("fetch", fetchMock);

    renderTestsPage({
      consumePendingRecollect: () => true,
      lastRunStatus: "ready",
    });

    expect(fetchMock).toHaveBeenCalledWith("/api/collect");
  });

  test(`given a pending re-collect while a run is in flight,
 when the page mounts,
 then /api/collect is not fetched`, () => {
    const fetchMock = vi.fn().mockResolvedValue({});
    vi.stubGlobal("fetch", fetchMock);

    renderTestsPage({
      consumePendingRecollect: () => true,
      lastRunStatus: "run",
    });

    expect(fetchMock).not.toHaveBeenCalled();
  });
});
