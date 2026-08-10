// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import { cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, beforeAll, describe, expect, test, vi } from "vitest";
import i18n from "i18next";
import { I18nextProvider, initReactI18next } from "react-i18next";
import { MemoryRouter } from "react-router";

import type { TestItem } from "./TestSuite";
import SuiteList, { TestRunI } from "./SuiteList";

vi.mock("./TestSuite", async () => {
  const actual = await vi.importActual<typeof import("./TestSuite")>("./TestSuite");
  return {
    ...actual,
    TestSuiteComponent: ({
      moduleTechName,
      index,
    }: {
      moduleTechName: string;
      index: number;
    }) => <div data-testid={`module-${moduleTechName}`}>{index + 1}</div>,
  };
});

const moduleStub = (name: string, section: string[] = []): TestItem => ({
  status: "ready",
  name,
  start_time: 0,
  stop_time: 0,
  artifact: {},
  cases: {},
  section,
});

const runWithSections: TestRunI = {
  name: "Full capabilities",
  status: "ready",
  modules: {
    test_1_identification: moduleStub("Identification"),
    "autofocus/test_1_coarse_search": moduleStub("Coarse search", ["autofocus"]),
    "autofocus/fine/test_1_dither": moduleStub("Dither", ["autofocus", "fine"]),
    test_7_alignment: moduleStub("Alignment checks", ["Alignment"]),
  },
};

beforeAll(async () => {
  if (!i18n.isInitialized) {
    await i18n.use(initReactI18next).init({
      lng: "en",
      resources: {
        en: {
          translation: {
            suiteList: { loadingTests: "Loading tests..." },
            section: {
              run: "Run",
              runAria: "Run section {{name}}",
              moduleCount: "{{count}} modules",
              open: "Open section {{name}}",
            },
          },
        },
      },
    });
  }
});

afterEach(() => {
  cleanup();
});

const renderSuiteList = (db_state: TestRunI) =>
  render(
    <MemoryRouter>
      <I18nextProvider i18n={i18n}>
        <SuiteList db_state={db_state} defaultClose={false} />
      </I18nextProvider>
    </MemoryRouter>
  );

const section = (path: string): HTMLElement => {
  const node = document.querySelector(`[data-section="${path}"]`);
  if (!node) {
    throw new Error(`Section "${path}" was not rendered`);
  }
  return node as HTMLElement;
};

describe("SuiteList", () => {
  test(`given modules belonging to sections,
 when the list is rendered,
 then a section header exists for each section path`, () => {
    renderSuiteList(runWithSections);

    expect(section("autofocus")).toBeInTheDocument();
    expect(section("autofocus/fine")).toBeInTheDocument();
    expect(section("Alignment")).toBeInTheDocument();
  });

  test(`given a module in a nested section,
 when the list is rendered,
 then it is nested inside its parent section rather than shown flat`, () => {
    renderSuiteList(runWithSections);

    const autofocus = section("autofocus");

    expect(
      within(autofocus).getByTestId("module-autofocus/test_1_coarse_search")
    ).toBeInTheDocument();
    expect(
      within(autofocus).getByTestId("module-autofocus/fine/test_1_dither")
    ).toBeInTheDocument();
    expect(
      within(section("autofocus/fine")).getByTestId(
        "module-autofocus/fine/test_1_dither"
      )
    ).toBeInTheDocument();
  });

  test(`given a module with no section mixed with named sections,
 when the list is rendered,
 then it sits under the Default section before other groups`, () => {
    renderSuiteList(runWithSections);

    const defaultSection = section("Default");
    const autofocus = section("autofocus");

    expect(defaultSection).toBeInTheDocument();
    expect(
      within(defaultSection).getByTestId("module-test_1_identification")
    ).toBeInTheDocument();
    expect(
      defaultSection.compareDocumentPosition(autofocus) &
        Node.DOCUMENT_POSITION_FOLLOWING
    ).toBeTruthy();
  });

  test(`given ungrouped modules and sections mixed,
 when the list is rendered,
 then module numbering stays continuous across the tree`, () => {
    renderSuiteList(runWithSections);

    expect(screen.getByTestId("module-test_1_identification")).toHaveTextContent(
      "1"
    );
    expect(
      screen.getByTestId("module-autofocus/test_1_coarse_search")
    ).toHaveTextContent("2");
    expect(
      screen.getByTestId("module-autofocus/fine/test_1_dither")
    ).toHaveTextContent("3");
    expect(screen.getByTestId("module-test_7_alignment")).toHaveTextContent("4");
  });

  test(`given a run with no named sections,
 when the list is rendered,
 then modules stay flat without a Default header`, () => {
    renderSuiteList({
      name: "Flat run",
      status: "ready",
      modules: {
        test_1: moduleStub("One"),
        test_2: moduleStub("Two"),
      },
    });

    expect(document.querySelector("[data-section]")).toBeNull();
    expect(screen.getByTestId("module-test_1")).toBeInTheDocument();
    expect(screen.getByTestId("module-test_2")).toBeInTheDocument();
  });
});
