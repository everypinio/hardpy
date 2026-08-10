// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, test, vi } from "vitest";

import { PanelProvider, type PanelContextValue } from "@/panel/PanelContext";

import { DialogBoxHost } from "./DialogBoxHost";
import type { TestRunI } from "./SuiteList";
import type { Case } from "./TestSuite";

vi.mock("./DialogBox", () => ({
  StartConfirmationDialog: ({
    title_bar,
    dialog_text,
  }: {
    title_bar?: string;
    dialog_text: string;
  }) => (
    <div data-testid="confirmation-dialog">
      <h1>{title_bar}</h1>
      <p>{dialog_text}</p>
    </div>
  ),
  WidgetType: {},
}));

afterEach(cleanup);

const panelValue = (testRunData: TestRunI): PanelContextValue => ({
  testRunData,
  rows: [],
  syncDocumentId: "sync",
  appConfig: null,
  manualCollectMode: false,
  selectedTests: [],
  onTestsSelectionChange: () => undefined,
  ultrawide: false,
  useDebugInfo: false,
  runSection: () => undefined,
  lastRunStatus: "ready",
});

const caseStub = (overrides: Partial<Case> = {}): Case => ({
  status: "run",
  name: "test_insert_dut",
  start_time: 0,
  stop_time: 0,
  assertion_msg: null,
  msg: null,
  measurements: [],
  artifact: {},
  dialog_box: {
    dialog_text: "Insert the DUT and confirm.",
    visible: true,
    id: "dlg-1",
    pass_fail: false,
  },
  ...overrides,
});

const renderHost = (testCase: Case, section: string[] = ["Default"]) =>
  render(
    <PanelProvider
      value={panelValue({
        status: "run",
        modules: {
          "prompts/test_1_confirm.py": {
            status: "run",
            name: "Prompts",
            start_time: 0,
            stop_time: 0,
            artifact: {},
            section,
            cases: { test_confirm: testCase },
          },
        },
      })}
    >
      <DialogBoxHost />
    </PanelProvider>,
  );

describe("DialogBoxHost", () => {
  test(`given a running test waiting on a dialog inside a folded section,
 when the host is mounted outside the test tree,
 then the dialog is shown without unfolding anything`, () => {
    renderHost(caseStub());

    expect(screen.getByTestId("confirmation-dialog")).toBeTruthy();
    expect(screen.getByText("Insert the DUT and confirm.")).toBeTruthy();
  });

  test(`given a dialog without its own title,
 when it is shown,
 then the case name is used as title`, () => {
    renderHost(caseStub());

    expect(screen.getByRole("heading")).toHaveTextContent("test_insert_dut");
  });

  test(`given no test waiting on a dialog,
 when the host is mounted,
 then no dialog is shown`, () => {
    renderHost(caseStub({ status: "passed" }));

    expect(screen.queryByTestId("confirmation-dialog")).toBeNull();
  });
});
