// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, test, vi } from "vitest";
import i18n from "i18next";
import { I18nextProvider, initReactI18next } from "react-i18next";
import { MemoryRouter, Route, Routes } from "react-router";

import type { PanelContextValue } from "@/panel/PanelContext";
import { PanelProvider } from "@/panel/PanelContext";
import type { TestItem } from "@/jig_test_view/TestSuite";
import { GroupPage } from "./GroupPage";

vi.mock("@/jig_test_view/SectionContents", () => ({
  SectionContents: ({
    node,
  }: {
    node: { modules: Array<{ id: string }> };
  }) => (
    <div data-testid="section-contents">
      {node.modules.map((module) => (
        <div key={module.id} data-testid={`module-${module.id}`} />
      ))}
    </div>
  ),
}));

const moduleStub = (name: string, section: string[]): TestItem => ({
  status: "ready",
  name,
  start_time: 0,
  stop_time: 0,
  artifact: {},
  cases: {},
  section,
});

async function renderGroup(path: string) {
  if (!i18n.isInitialized) {
    await i18n.use(initReactI18next).init({
      lng: "en",
      resources: {
        en: {
          translation: {
            group: {
              back: "All tests",
              notFound: "This section was not found.",
            },
            section: {
              run: "Run",
              runAria: "Run section {{name}}",
            },
          },
        },
      },
    });
  }

  const value: PanelContextValue = {
    testRunData: {
      name: "Demo",
      status: "ready",
      modules: {
        "autofocus/test_1": moduleStub("Coarse", ["autofocus"]),
        "autofocus/fine/test_1": moduleStub("Dither", ["autofocus", "fine"]),
        test_1: moduleStub("Root", []),
      },
    },
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
  };

  return render(
    <MemoryRouter initialEntries={[path]}>
      <I18nextProvider i18n={i18n}>
        <PanelProvider value={value}>
          <Routes>
            <Route path="/group/*" element={<GroupPage />} />
          </Routes>
        </PanelProvider>
      </I18nextProvider>
    </MemoryRouter>
  );
}

describe("GroupPage", () => {
  afterEach(() => {
    cleanup();
  });

  test(`given a known section route,
 when the page is rendered,
 then only that section's modules are shown`, async () => {
    await renderGroup("/group/autofocus");

    expect(screen.getByTestId("module-autofocus/test_1")).toBeInTheDocument();
    expect(
      screen.queryByTestId("module-test_1")
    ).not.toBeInTheDocument();
  });

  test(`given the Default section route,
 when the page is rendered,
 then only ungrouped modules are shown`, async () => {
    await renderGroup("/group/Default");

    expect(screen.getByTestId("module-test_1")).toBeInTheDocument();
    expect(
      screen.queryByTestId("module-autofocus/test_1")
    ).not.toBeInTheDocument();
  });

  test(`given an unknown section route,
 when the page is rendered,
 then a not-found message and back link are shown`, async () => {
    await renderGroup("/group/missing");

    expect(screen.getByText("This section was not found.")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /All tests/i })).toHaveAttribute(
      "href",
      "/"
    );
  });
});
