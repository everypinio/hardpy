// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import type { TestRunI } from "@/jig_test_view/SuiteList";
import type { Case, DialogBoxProps } from "@/jig_test_view/TestSuite";

/** The operator interaction a running test is blocked on. */
export interface PendingDialog {
  moduleId: string;
  caseId: string;
  /** Name of the case, used as dialog title when the test provides none. */
  caseName: string;
  dialogBox: DialogBoxProps;
}

/**
 * Tells whether a case is waiting for the operator to answer its dialog.
 * @param {Case | undefined} testCase - The case to inspect.
 * @returns {boolean} True while the case blocks on operator input.
 */
function isWaitingForOperator(testCase: Case | undefined): boolean {
  return (
    testCase?.status === "run" &&
    testCase.dialog_box?.visible === true &&
    Boolean(testCase.dialog_box?.dialog_text)
  );
}

/**
 * Finds the interaction the run is currently blocked on.
 *
 * The run document holds at most one open dialog, since a test blocks until
 * the operator answers. Reading it from the document instead of from the test
 * tree keeps the dialog independent of which sections are unfolded and of the
 * page the operator is on.
 * @param {TestRunI} run - The live run document.
 * @returns {PendingDialog | null} The pending interaction, null when none.
 */
export function findPendingDialog(run: TestRunI): PendingDialog | null {
  if (run.status !== "run") {
    return null;
  }

  for (const [moduleId, module] of Object.entries(run.modules ?? {})) {
    for (const [caseId, testCase] of Object.entries(module.cases ?? {})) {
      if (isWaitingForOperator(testCase)) {
        return {
          moduleId,
          caseId,
          caseName: testCase.name,
          dialogBox: testCase.dialog_box,
        };
      }
    }
  }

  return null;
}
