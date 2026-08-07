// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import { render } from "@testing-library/react";
import { describe, expect, test } from "vitest";

import { ProgressView } from "./ProgressView";

const indicator = (container: HTMLElement): HTMLElement | null =>
  container.querySelector("[data-slot=progress-indicator]");

describe("ProgressView", () => {
  test(`given a run in progress,
 when the progress is rendered,
 then the bar is striped and coloured as primary`, () => {
    const { container } = render(<ProgressView percentage={40} status="run" />);

    expect(indicator(container)).toHaveClass("bg-primary");
    expect(indicator(container)).toHaveClass("progress-stripes");
  });

  test(`given a run that reached 100 percent while still marked as running,
 when the progress is rendered,
 then the bar stops being striped`, () => {
    const { container } = render(<ProgressView percentage={100} status="run" />);

    expect(indicator(container)).not.toHaveClass("progress-stripes");
  });

  test(`given a passed run,
 when the progress is rendered,
 then the bar is coloured as success and is not striped`, () => {
    const { container } = render(
      <ProgressView percentage={100} status="passed" />
    );

    expect(indicator(container)).toHaveClass("bg-success");
    expect(indicator(container)).not.toHaveClass("progress-stripes");
  });

  test(`given a failed run,
 when the progress is rendered,
 then the bar is coloured as destructive`, () => {
    const { container } = render(
      <ProgressView percentage={62} status="failed" />
    );

    expect(indicator(container)).toHaveClass("bg-destructive");
  });

  test(`given a run that has not started,
 when the progress is rendered,
 then the bar is empty and neutrally coloured`, () => {
    const { container } = render(<ProgressView percentage={0} status="" />);

    expect(indicator(container)).toHaveStyle({
      transform: "translateX(-100%)",
    });
    expect(indicator(container)).not.toHaveClass("bg-primary");
  });

  test(`given a run halfway through,
 when the progress is rendered,
 then the bar is filled by half`, () => {
    const { container } = render(<ProgressView percentage={50} status="run" />);

    expect(indicator(container)).toHaveStyle({
      transform: "translateX(-50%)",
    });
  });
});
