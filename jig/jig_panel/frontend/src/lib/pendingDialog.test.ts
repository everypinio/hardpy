// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import { describe, expect, test } from "vitest";

import type { TestRunI } from "@/jig_test_view/SuiteList";
import type { Case, DialogBoxProps, TestItem } from "@/jig_test_view/TestSuite";
import { findPendingDialog } from "./pendingDialog";

const dialogBox = (
  overrides: Partial<DialogBoxProps> = {},
): DialogBoxProps => ({
  dialog_text: "Insert the DUT and confirm.",
  visible: true,
  id: "dlg-1",
  pass_fail: false,
  ...overrides,
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
  dialog_box: dialogBox(),
  ...overrides,
});

const moduleStub = (cases: Record<string, Case>): TestItem => ({
  status: "run",
  name: "Prompts",
  start_time: 0,
  stop_time: 0,
  artifact: {},
  cases,
});

const runStub = (cases: Record<string, Case>, status = "run"): TestRunI => ({
  status,
  modules: { "prompts/test_1_confirm.py": moduleStub(cases) },
});

describe("findPendingDialog", () => {
  test(`given a running case with a visible dialog,
 when the pending dialog is looked up,
 then the dialog is returned with its module and case`, () => {
    const pending = findPendingDialog(runStub({ test_confirm: caseStub() }));

    expect(pending).toEqual({
      moduleId: "prompts/test_1_confirm.py",
      caseId: "test_confirm",
      caseName: "test_insert_dut",
      dialogBox: dialogBox(),
    });
  });

  test(`given a dialog the test already closed,
 when the pending dialog is looked up,
 then nothing is pending`, () => {
    const pending = findPendingDialog(
      runStub({
        test_confirm: caseStub({ dialog_box: dialogBox({ visible: false }) }),
      }),
    );

    expect(pending).toBeNull();
  });

  test(`given a case that is no longer running,
 when the pending dialog is looked up,
 then nothing is pending`, () => {
    const pending = findPendingDialog(
      runStub({ test_confirm: caseStub({ status: "passed" }) }),
    );

    expect(pending).toBeNull();
  });

  test(`given a finished run keeping the last dialog on its document,
 when the pending dialog is looked up,
 then nothing is pending`, () => {
    const pending = findPendingDialog(
      runStub({ test_confirm: caseStub() }, "passed"),
    );

    expect(pending).toBeNull();
  });
});
