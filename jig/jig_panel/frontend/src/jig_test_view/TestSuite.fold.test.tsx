// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import type { ComponentProps } from "react";
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeAll, describe, expect, test, vi } from "vitest";
import i18n from "i18next";
import { I18nextProvider, initReactI18next } from "react-i18next";

import { TestSuiteComponent, type Case, type TestItem } from "./TestSuite";

vi.mock("./DialogBox", () => ({
  StartConfirmationDialog: () => null,
  WidgetType: {},
}));

vi.mock("./TestData", () => ({
  default: () => null,
}));

beforeAll(() => {
  class ResizeObserverStub {
    observe(): void {
      return undefined;
    }
    unobserve(): void {
      return undefined;
    }
    disconnect(): void {
      return undefined;
    }
  }
  vi.stubGlobal("ResizeObserver", ResizeObserverStub);
  Element.prototype.scrollIntoView = vi.fn();
});

const CASE_NAME = "Coarse peak";

const caseStub = (status: string): Case => ({
  status,
  name: CASE_NAME,
  start_time: 0,
  stop_time: 0,
  assertion_msg: null,
  msg: null,
  measurements: [],
  artifact: {},
  dialog_box: {
    dialog_text: "",
    visible: false,
    id: "dialog",
    pass_fail: false,
  },
});

/** Builds a fresh module object, as the 500 ms storage poll delivers one. */
const moduleWithCaseStatus = (status: string): TestItem => ({
  status,
  name: "Coarse search",
  start_time: 0,
  stop_time: 0,
  artifact: {},
  cases: { test_coarse_peak: caseStub(status) },
});

const moduleElement = (
  props: Partial<ComponentProps<typeof TestSuiteComponent>> = {}
) => (
  <I18nextProvider i18n={i18n}>
    <TestSuiteComponent
      index={0}
      test={moduleWithCaseStatus("failed")}
      defaultOpen={true}
      commonTestRunStatus="failed"
      moduleTechName="autofocus/test_1_coarse_search"
      selectionSupported={false}
      autoScroll={true}
      {...props}
    />
  </I18nextProvider>
);

async function renderModule(
  props: Partial<ComponentProps<typeof TestSuiteComponent>> = {}
) {
  if (!i18n.isInitialized) {
    await i18n.use(initReactI18next).init({
      lng: "en",
      resources: {
        en: {
          translation: {
            testSuite: {
              loading: "Loading...",
              nameColumn: "Name",
              dataColumn: "Data",
            },
          },
        },
      },
    });
  }

  return render(moduleElement(props));
}

describe("TestSuite folding", () => {
  afterEach(() => {
    cleanup();
  });

  test(`given a module unfolded while one of its cases failed,
 when the operator folds it with the chevron,
 then the next storage update leaves it folded`, async () => {
    const { rerender } = await renderModule();

    await userEvent.click(screen.getByRole("button", { name: "Collapse" }));
    rerender(moduleElement({ test: moduleWithCaseStatus("failed") }));

    expect(screen.queryByText(CASE_NAME)).toBeNull();
  });

  test(`given a module unfolded while one of its cases failed,
 when the operator folds it with the module name,
 then the next storage update leaves it folded`, async () => {
    const { rerender } = await renderModule();

    await userEvent.click(screen.getByRole("button", { name: /Coarse search/ }));
    rerender(moduleElement({ test: moduleWithCaseStatus("failed") }));

    expect(screen.queryByText(CASE_NAME)).toBeNull();
  });

  test(`given a folded module,
 when one of its cases starts running,
 then it unfolds so the operator sees the case`, async () => {
    const { rerender } = await renderModule({
      test: moduleWithCaseStatus("ready"),
      commonTestRunStatus: "run",
      defaultOpen: false,
    });
    expect(screen.queryByText(CASE_NAME)).toBeNull();

    rerender(
      moduleElement({
        test: moduleWithCaseStatus("run"),
        commonTestRunStatus: "run",
        defaultOpen: false,
      })
    );

    expect(screen.getByText(CASE_NAME)).toBeTruthy();
  });

  test(`given a module unfolded by the run,
 when all its cases are done,
 then it folds back`, async () => {
    const { rerender } = await renderModule({
      test: moduleWithCaseStatus("ready"),
      commonTestRunStatus: "run",
      defaultOpen: false,
    });
    rerender(
      moduleElement({
        test: moduleWithCaseStatus("run"),
        commonTestRunStatus: "run",
        defaultOpen: false,
      })
    );
    expect(screen.getByText(CASE_NAME)).toBeTruthy();

    rerender(
      moduleElement({
        test: moduleWithCaseStatus("passed"),
        commonTestRunStatus: "passed",
        defaultOpen: false,
      })
    );

    expect(screen.queryByText(CASE_NAME)).toBeNull();
  });
});
