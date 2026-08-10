// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, beforeAll, describe, expect, test, vi } from "vitest";
import i18n from "i18next";
import { I18nextProvider, initReactI18next } from "react-i18next";

import TestHistory, { type HistoryEntry } from "./TestHistory";

beforeAll(async () => {
  if (!i18n.isInitialized) {
    await i18n.use(initReactI18next).init({
      lng: "en",
      resources: {
        en: {
          translation: {
            history: {
              title: "Test history",
              columns: {
                testName: "Test name",
                runName: "Run name",
                startTime: "Start time",
                result: "Result",
                serialNumber: "Serial number",
                details: "Details",
              },
              viewDetails: "View details",
              selected: "Selected",
              unknownRun: "Unnamed run",
            },
            app: { status: { passed: "Pass" } },
          },
        },
      },
    });
  }
});

afterEach(cleanup);

const renderHistory = (history: HistoryEntry[]) =>
  render(
    <I18nextProvider i18n={i18n}>
      <TestHistory
        history={history}
        selectedHistoryId={null}
        onSelectHistoryRun={vi.fn()}
      />
    </I18nextProvider>
  );

const entry = (overrides: Partial<HistoryEntry> = {}): HistoryEntry => ({
  id: "1",
  name: "Full capabilities",
  run_name: "prompts",
  status: "passed",
  start_time: 90,
  serial_number: "SN-1",
  ...overrides,
});

describe("TestHistory", () => {
  test(`given a run of one section,
 when the history is rendered,
 then the test name and what the run executed are shown in their own columns`, () => {
    renderHistory([entry()]);

    expect(screen.getByText("Test name")).toBeTruthy();
    expect(screen.getByText("Run name")).toBeTruthy();
    expect(screen.getByText("Full capabilities")).toBeTruthy();
    expect(screen.getByText("prompts")).toBeTruthy();
  });

  test(`given a run recorded before run names existed,
 when the history is rendered,
 then the run name cell falls back to a dash`, () => {
    renderHistory([entry({ run_name: undefined })]);

    expect(screen.getByText("-")).toBeTruthy();
  });
});
