// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, beforeAll, describe, expect, test, vi } from "vitest";
import i18n from "i18next";
import { I18nextProvider, initReactI18next } from "react-i18next";

import {
  PanelProvider,
  type PanelContextValue,
} from "@/panel/PanelContext";

import { OperatorMessageHost } from "./OperatorMessageHost";
import type { TestRunI } from "./SuiteList";

vi.mock("./OperatorMsg", () => ({
  CLOSED_MESSAGES_KEY: "closed_operator_messages",
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

beforeAll(async () => {
  if (!i18n.isInitialized) {
    await i18n.use(initReactI18next).init({
      lng: "en",
      resources: {
        en: {
          translation: {
            operatorDialog: { defaultTitle: "Operator message" },
          },
        },
      },
    });
  }
});

afterEach(() => {
  cleanup();
  localStorage.clear();
});

const basePanelValue = (
  testRunData: TestRunI
): PanelContextValue => ({
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

const renderHost = (testRunData: TestRunI) =>
  render(
    <I18nextProvider i18n={i18n}>
      <PanelProvider value={basePanelValue(testRunData)}>
        <OperatorMessageHost />
      </PanelProvider>
    </I18nextProvider>
  );

describe("OperatorMessageHost", () => {
  test(`given a visible operator message on the run document,
 when the host is mounted outside SuiteList,
 then the dialog is shown`, () => {
    renderHost({
      name: "run-1",
      operator_msg: {
        msg: "This blocking message stays until dismissed.",
        title: "Operator message",
        visible: true,
        id: "msg-1",
      },
    });

    expect(screen.getByTestId("operator-msg-dialog")).toBeTruthy();
    expect(
      screen.getByText("This blocking message stays until dismissed.")
    ).toBeTruthy();
  });

  test(`given no visible operator message,
 when the host is mounted,
 then no dialog is shown`, () => {
    renderHost({
      name: "run-1",
      operator_msg: {
        msg: "Hidden",
        visible: false,
      },
    });

    expect(screen.queryByTestId("operator-msg-dialog")).toBeNull();
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
      operator_msg: { msg: "A", visible: true, id: "msg-1" },
    });

    rerender(
      <I18nextProvider i18n={i18n}>
        <PanelProvider
          value={basePanelValue({
            name: "run-2",
            operator_msg: {
              msg: "New message",
              title: "Operator message",
              visible: true,
              id: "msg-2",
            },
          })}
        >
          <OperatorMessageHost />
        </PanelProvider>
      </I18nextProvider>
    );

    expect(localStorage.getItem("closed_operator_messages")).toBeNull();
    expect(screen.getByText("New message")).toBeTruthy();
  });
});
