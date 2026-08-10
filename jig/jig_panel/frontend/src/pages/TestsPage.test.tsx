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

  test(`given a run that just finished,
 when the page mounts,
 then no collection is triggered so the results stay on screen`, () => {
    const fetchMock = vi.fn().mockResolvedValue({});
    vi.stubGlobal("fetch", fetchMock);

    renderTestsPage({
      testRunData: { name: "Demo", status: "passed", modules: {} },
      lastRunStatus: "passed",
    });

    expect(fetchMock).not.toHaveBeenCalled();
  });
});
