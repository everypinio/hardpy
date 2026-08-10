// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import type { ComponentProps } from "react";
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeAll, describe, expect, test, vi } from "vitest";
import i18n from "i18next";
import { I18nextProvider, initReactI18next } from "react-i18next";

import { TestSuiteComponent, type TestItem } from "./TestSuite";

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
});

const moduleStub: TestItem = {
  status: "ready",
  name: "Coarse search",
  start_time: 0,
  stop_time: 0,
  artifact: {},
  cases: {
    test_coarse_peak: {
      status: "ready",
      name: "Coarse peak",
      start_time: 0,
      stop_time: 0,
      assertion_msg: "",
      msg: {},
      artifact: {},
      chart: [],
      attempt: 1,
      dialog_box: {},
    },
  },
};

async function renderModule(
  props: Partial<ComponentProps<typeof TestSuiteComponent>> = {}
) {
  if (!i18n.isInitialized) {
    await i18n.use(initReactI18next).init({
      lng: "en",
      resources: {
        en: {
          translation: {
            testSuite: { loading: "Loading..." },
            module: {
              run: "Run",
              runAria: "Run module {{name}}",
            },
          },
        },
      },
    });
  }

  return render(
    <I18nextProvider i18n={i18n}>
      <TestSuiteComponent
        index={0}
        test={moduleStub}
        defaultOpen={false}
        commonTestRunStatus="ready"
        moduleTechName="autofocus/test_1_coarse_search"
        {...props}
      />
    </I18nextProvider>
  );
}

describe("TestSuite module Run button", () => {
  afterEach(() => {
    cleanup();
  });

  test(`given a module with onRunModule,
 when the Run button is clicked,
 then the module id is emitted`, async () => {
    const onRunModule = vi.fn();
    await renderModule({ onRunModule });

    await userEvent.click(
      screen.getByTestId("module-run-autofocus/test_1_coarse_search")
    );

    expect(onRunModule).toHaveBeenCalledWith("autofocus/test_1_coarse_search");
  });

  test(`given a run already in flight,
 when the module is rendered,
 then the Run button is disabled`, async () => {
    await renderModule({
      onRunModule: vi.fn(),
      commonTestRunStatus: "run",
    });

    expect(
      screen.getByTestId("module-run-autofocus/test_1_coarse_search")
    ).toBeDisabled();
  });
});
