// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import { cleanup, render, screen } from "@testing-library/react";
import {
  afterEach,
  beforeAll,
  beforeEach,
  describe,
  expect,
  test,
  vi,
} from "vitest";
import i18n from "i18next";
import { I18nextProvider, initReactI18next } from "react-i18next";

import {
  PanelProvider,
  type PanelContextValue,
} from "@/panel/PanelContext";

import { OperatorMessageHost } from "./OperatorMessageHost";
import type { TestRunI } from "./SuiteList";

vi.mock("./OperatorMsg", () => ({
  StartOperatorMsgDialog: ({
    msg,
    title,
  }: {
    msg: string;
    title?: string;
  }) => (
    <div data-testid="operator-msg-dialog">
      <h1>{title}</h1>
      <p>{msg}</p>
    </div>
  ),
}));

const infoToast = vi.fn();
vi.mock("sonner", () => ({
  toast: {
    info: (...args: unknown[]) => infoToast(...args),
  },
}));

const navigateMock = vi.fn();
vi.mock("react-router", async () => {
  const actual =
    await vi.importActual<typeof import("react-router")>("react-router");
  return {
    ...actual,
    useNavigate: () => navigateMock,
  };
});

type ToastOptions = {
  id?: string;
  description?: string;
  action?: { label: string; onClick: () => void };
};

const lastToastOptions = (): ToastOptions =>
  infoToast.mock.calls[0][1] as ToastOptions;

beforeAll(async () => {
  if (!i18n.isInitialized) {
    await i18n.use(initReactI18next).init({
      lng: "en",
      resources: {
        en: {
          translation: {
            operatorDialog: { defaultTitle: "Operator message" },
            history: { viewDetails: "View details" },
          },
        },
      },
    });
  }
});

beforeEach(() => {
  infoToast.mockClear();
  navigateMock.mockClear();
});

afterEach(() => {
  cleanup();
  localStorage.clear();
});

const basePanelValue = (
  testRunData: TestRunI,
  rows: PanelContextValue["rows"] = []
): PanelContextValue => ({
  testRunData,
  rows,
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

const hostElement = (
  testRunData: TestRunI,
  rows: PanelContextValue["rows"] = []
) => (
  <I18nextProvider i18n={i18n}>
    <PanelProvider value={basePanelValue(testRunData, rows)}>
      <OperatorMessageHost />
    </PanelProvider>
  </I18nextProvider>
);

const renderHost = (
  testRunData: TestRunI,
  rows: PanelContextValue["rows"] = []
) => render(hostElement(testRunData, rows));

describe("OperatorMessageHost", () => {
  test(`given a message the test waits on,
 when the host is mounted outside SuiteList,
 then the dialog is shown`, () => {
    renderHost({
      name: "run-1",
      operator_msg: {
        msg: "This blocking message stays until dismissed.",
        title: "Operator message",
        visible: true,
        block: true,
        id: "msg-1",
      },
    });

    expect(screen.getByTestId("operator-msg-dialog")).toBeTruthy();
    expect(
      screen.getByText("This blocking message stays until dismissed.")
    ).toBeTruthy();
    expect(infoToast).not.toHaveBeenCalled();
  });

  test(`given a message stored without a block flag,
 when the host is mounted,
 then it is still shown as a dialog`, () => {
    renderHost({
      name: "run-1",
      operator_msg: {
        msg: "Written by an older Jig.",
        visible: true,
        id: "msg-1",
      },
    });

    expect(screen.getByTestId("operator-msg-dialog")).toBeTruthy();
  });

  test(`given a message the test does not wait on,
 when the host is mounted,
 then it is notified instead of opening a dialog`, () => {
    renderHost({
      name: "run-1",
      operator_msg: {
        msg: "Report saved in /tmp/reports",
        title: "End of testing",
        visible: true,
        block: false,
        id: "msg-1",
      },
    });

    expect(screen.queryByTestId("operator-msg-dialog")).toBeNull();
    expect(infoToast).toHaveBeenCalledTimes(1);
    expect(infoToast).toHaveBeenCalledWith(
      "End of testing",
      expect.objectContaining({
        id: "msg-1",
        description: "Report saved in /tmp/reports",
      })
    );
  });

  test(`given a message the test does not wait on,
 when the run document updates again,
 then the operator is notified only once`, () => {
    const testRunData: TestRunI = {
      name: "run-1",
      operator_msg: {
        msg: "Report saved in /tmp/reports",
        title: "End of testing",
        visible: true,
        block: false,
        id: "msg-1",
      },
    };
    const { rerender } = renderHost(testRunData);

    rerender(hostElement({ ...testRunData }));

    expect(infoToast).toHaveBeenCalledTimes(1);
  });

  test(`given a message raised once the run is stored in the history,
 when the operator follows the notification link,
 then the result page of that run is opened`, () => {
    renderHost(
      {
        name: "run-1",
        start_time: 30,
        stop_time: 45,
        operator_msg: {
          msg: "Report saved in /tmp/reports",
          title: "End of testing",
          visible: true,
          block: false,
          id: "msg-1",
        },
      },
      [
        {
          id: "stored-run",
          key: "stored-run",
          value: { rev: "1" },
          doc: { name: "run-1", status: "passed", start_time: 30 },
        },
      ]
    );

    const { action } = lastToastOptions();
    expect(action?.label).toBe("View details");

    action?.onClick();

    expect(navigateMock).toHaveBeenCalledWith("/results/stored-run");
  });

  test(`given a message raised while the run is still going,
 when the notification is shown,
 then it carries no result link`, () => {
    renderHost({
      name: "run-1",
      start_time: 30,
      operator_msg: {
        msg: "Insert the next board",
        visible: true,
        block: false,
        id: "msg-1",
      },
    });

    expect(lastToastOptions().action).toBeUndefined();
  });

  test(`given no visible operator message,
 when the host is mounted,
 then nothing is shown`, () => {
    renderHost({
      name: "run-1",
      operator_msg: {
        msg: "Hidden",
        visible: false,
      },
    });

    expect(screen.queryByTestId("operator-msg-dialog")).toBeNull();
    expect(infoToast).not.toHaveBeenCalled();
  });

  test(`given a previously closed message id in localStorage,
 when a new run name arrives,
 then closed-message state is cleared`, () => {
    localStorage.setItem(
      "closed_operator_messages",
      JSON.stringify(["old-id"])
    );

    const { rerender } = renderHost({
      name: "run-1",
      operator_msg: { msg: "A", visible: true, block: true, id: "msg-1" },
    });

    rerender(
      hostElement({
        name: "run-2",
        operator_msg: {
          msg: "New message",
          title: "Operator message",
          visible: true,
          block: true,
          id: "msg-2",
        },
      })
    );

    expect(localStorage.getItem("closed_operator_messages")).toBeNull();
    expect(screen.getByText("New message")).toBeTruthy();
  });
});
