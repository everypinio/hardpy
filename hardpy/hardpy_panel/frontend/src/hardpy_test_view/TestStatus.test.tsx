// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import { render } from "@testing-library/react";
import { describe, expect, test } from "vitest";

import { TestStatus } from "./TestStatus";

const statusIcon = (container: HTMLElement): SVGElement | null =>
  container.querySelector("svg[data-status]");

describe("TestStatus", () => {
  test(`given a passed test,
 when the status is rendered,
 then a success coloured icon is shown`, () => {
    const { container } = render(<TestStatus status="passed" />);

    expect(statusIcon(container)).toHaveClass("text-success");
  });

  test(`given a failed test,
 when the status is rendered,
 then a destructive coloured icon is shown`, () => {
    const { container } = render(<TestStatus status="failed" />);

    expect(statusIcon(container)).toHaveClass("text-destructive");
  });

  test(`given a running test,
 when the status is rendered,
 then the icon spins`, () => {
    const { container } = render(<TestStatus status="run" />);

    expect(statusIcon(container)).toHaveClass("animate-spin");
  });

  test(`given a test that has not started,
 when the status is rendered,
 then the icon is marked as pending`, () => {
    const { container } = render(<TestStatus status="" />);

    expect(statusIcon(container)).toHaveAttribute("data-status", "pending");
  });

  test(`given a status this frontend does not know,
 when the status is rendered,
 then the icon is marked as unknown`, () => {
    const { container } = render(<TestStatus status="exploded" />);

    expect(statusIcon(container)).toHaveAttribute("data-status", "unknown");
  });

  test(`given extra classes,
 when the status is rendered,
 then they are applied on top of the status colour`, () => {
    const { container } = render(
      <TestStatus status="passed" className="size-6" />
    );

    expect(statusIcon(container)).toHaveClass("size-6");
  });
});
