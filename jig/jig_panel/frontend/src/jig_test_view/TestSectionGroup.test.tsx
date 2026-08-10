// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import type { ComponentProps } from "react";
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, test, vi } from "vitest";
import i18n from "i18next";
import { I18nextProvider, initReactI18next } from "react-i18next";
import { MemoryRouter } from "react-router";

import type { SectionNode } from "@/lib/testSections";
import type { TestItem } from "./TestSuite";
import { TestSectionGroup } from "./TestSectionGroup";

const navigateMock = vi.fn();

vi.mock("react-router", async () => {
  const actual = await vi.importActual<typeof import("react-router")>(
    "react-router"
  );
  return {
    ...actual,
    useNavigate: () => navigateMock,
  };
});

vi.mock("./TestSuite", async () => {
  const actual = await vi.importActual<typeof import("./TestSuite")>("./TestSuite");
  return {
    ...actual,
    TestSuiteComponent: ({ moduleTechName }: { moduleTechName: string }) => (
      <div data-testid={`module-${moduleTechName}`} />
    ),
  };
});

const moduleStub = (name: string, section: string[]): TestItem => ({
  status: "ready",
  name,
  start_time: 0,
  stop_time: 0,
  artifact: {},
  cases: {},
  section,
});

const sectionNode: SectionNode = {
  path: ["autofocus"],
  modules: [
    {
      id: "autofocus/test_1",
      test: moduleStub("Coarse", ["autofocus"]),
    },
  ],
  children: [
    {
      path: ["autofocus", "fine"],
      modules: [
        {
          id: "autofocus/fine/test_1",
          test: moduleStub("Dither", ["autofocus", "fine"]),
        },
      ],
      children: [],
    },
  ],
};

const sectionWithModuleStatus = (status: string): SectionNode => ({
  path: ["autofocus"],
  modules: [
    {
      id: "autofocus/test_1",
      test: { ...moduleStub("Coarse", ["autofocus"]), status },
    },
  ],
  children: [],
});

const sectionElement = (
  props: Partial<ComponentProps<typeof TestSectionGroup>> = {}
) => (
  <MemoryRouter>
    <I18nextProvider i18n={i18n}>
      <TestSectionGroup
        node={sectionNode}
        startIndex={0}
        defaultClose={false}
        commonTestRunStatus="ready"
        {...props}
      />
    </I18nextProvider>
  </MemoryRouter>
);

async function renderSection(
  props: Partial<ComponentProps<typeof TestSectionGroup>> = {}
) {
  if (!i18n.isInitialized) {
    await i18n.use(initReactI18next).init({
      lng: "en",
      resources: {
        en: {
          translation: {
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

  return render(sectionElement(props));
}

describe("TestSectionGroup", () => {
  afterEach(() => {
    cleanup();
    navigateMock.mockReset();
  });

  test(`given a section with nested modules,
 when the Run button is clicked,
 then every descendant module id is emitted with the section path and the group route is opened`, async () => {
    const onRunSection = vi.fn();
    await renderSection({ onRunSection });

    await userEvent.click(screen.getByTestId("section-run-autofocus"));

    expect(navigateMock).toHaveBeenCalledWith("/group/autofocus");
    expect(onRunSection).toHaveBeenCalledWith(
      ["autofocus/test_1", "autofocus/fine/test_1"],
      "autofocus"
    );
  });

  test(`given a run already in flight,
 when the section is rendered,
 then the Run button is disabled`, async () => {
    const onRunSection = vi.fn();
    await renderSection({
      onRunSection,
      commonTestRunStatus: "run",
    });

    expect(screen.getByTestId("section-run-autofocus")).toBeDisabled();
  });

  test(`given a section header,
 when the section name link is rendered,
 then it points at the group route`, async () => {
    await renderSection();

    expect(
      screen.getByRole("link", { name: "Open section autofocus" })
    ).toHaveAttribute("href", "/group/autofocus");
  });

  test(`given a folded section,
 when one of its modules starts running,
 then the section unfolds so the running test is visible`, async () => {
    const { rerender } = await renderSection({
      node: sectionWithModuleStatus("ready"),
      defaultClose: true,
      commonTestRunStatus: "run",
    });
    expect(screen.queryByTestId("module-autofocus/test_1")).toBeNull();

    rerender(
      sectionElement({
        node: sectionWithModuleStatus("run"),
        defaultClose: true,
        commonTestRunStatus: "run",
      })
    );

    expect(screen.getByTestId("module-autofocus/test_1")).toBeTruthy();
  });

  test(`given a section unfolded by a run,
 when its modules are done,
 then the section folds back`, async () => {
    const { rerender } = await renderSection({
      node: sectionWithModuleStatus("run"),
      defaultClose: true,
      commonTestRunStatus: "run",
    });
    expect(screen.getByTestId("module-autofocus/test_1")).toBeTruthy();

    rerender(
      sectionElement({
        node: sectionWithModuleStatus("passed"),
        defaultClose: true,
        commonTestRunStatus: "passed",
      })
    );

    expect(screen.queryByTestId("module-autofocus/test_1")).toBeNull();
  });

  test(`given a section unfolded by a run,
 when the operator folds it back while the run continues,
 then it stays folded`, async () => {
    const { rerender } = await renderSection({
      node: sectionWithModuleStatus("run"),
      defaultClose: true,
      commonTestRunStatus: "run",
    });

    await userEvent.click(screen.getByRole("button", { name: "Collapse" }));
    rerender(
      sectionElement({
        node: sectionWithModuleStatus("run"),
        defaultClose: true,
        commonTestRunStatus: "run",
      })
    );

    expect(screen.queryByTestId("module-autofocus/test_1")).toBeNull();
  });

  test(`given a section the operator folded during a run,
 when a later run reaches it,
 then it unfolds again`, async () => {
    const { rerender } = await renderSection({
      node: sectionWithModuleStatus("run"),
      defaultClose: true,
      commonTestRunStatus: "run",
    });
    await userEvent.click(screen.getByRole("button", { name: "Collapse" }));

    rerender(
      sectionElement({
        node: sectionWithModuleStatus("passed"),
        defaultClose: true,
        commonTestRunStatus: "passed",
      })
    );
    rerender(
      sectionElement({
        node: sectionWithModuleStatus("run"),
        defaultClose: true,
        commonTestRunStatus: "run",
      })
    );

    expect(screen.getByTestId("module-autofocus/test_1")).toBeTruthy();
  });
});
