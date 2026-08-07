// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import type { TFunction } from "i18next";
import { describe, expect, test } from "vitest";

import {
  DisplayStatus,
  RUN_STATUSES,
  isRunInFlight,
  statusLabel,
  statusPresentation,
  toDisplayStatus,
} from "./testStatus";

const echoKey = ((key: string) => key) as unknown as TFunction;

describe("toDisplayStatus", () => {
  test.each(RUN_STATUSES)(
    `given the backend status "%s",
 when it is narrowed,
 then it is kept as is`,
    (status) => {
      expect(toDisplayStatus(status)).toBe(status);
    }
  );

  test(`given an empty status,
 when it is narrowed,
 then it becomes "pending"`, () => {
    expect(toDisplayStatus("")).toBe("pending");
  });

  test(`given no status at all,
 when it is narrowed,
 then it becomes "pending"`, () => {
    expect(toDisplayStatus(undefined)).toBe("pending");
  });

  test(`given a status this frontend does not know,
 when it is narrowed,
 then it becomes "unknown"`, () => {
    expect(toDisplayStatus("exploded")).toBe("unknown");
  });
});

describe("statusPresentation", () => {
  const allStatuses: DisplayStatus[] = [
    ...RUN_STATUSES,
    "pending",
    "unknown",
  ];

  test.each(allStatuses)(
    `given the status "%s",
 when its presentation is looked up,
 then an icon and colour utilities are returned`,
    (status) => {
      const presentation = statusPresentation(status);

      expect(presentation.icon).toBeTruthy();
      expect(presentation.iconClassName).not.toBe("");
      expect(presentation.fillClassName).not.toBe("");
    }
  );

  test(`given a run in flight,
 when its presentation is looked up,
 then the icon spins`, () => {
    expect(statusPresentation("run").iconClassName).toContain("animate-spin");
  });

  test(`given a passed and a failed run,
 when their presentations are looked up,
 then they do not share a colour`, () => {
    expect(statusPresentation("passed").fillClassName).not.toBe(
      statusPresentation("failed").fillClassName
    );
  });
});

describe("statusLabel", () => {
  test(`given a status carrying a translation key,
 when it is labelled,
 then the key is translated`, () => {
    expect(statusLabel("passed", echoKey)).toBe("app.status.passed");
  });

  test(`given a status without a translation key,
 when it is labelled,
 then the label is empty`, () => {
    expect(statusLabel("pending", echoKey)).toBe("");
  });
});

describe("isRunInFlight", () => {
  test(`given a running test run,
 when its progress is checked,
 then it is reported as in flight`, () => {
    expect(isRunInFlight("run")).toBe(true);
  });

  test.each(["ready", "passed", "failed", "stopped"] as DisplayStatus[])(
    `given a run with status "%s",
 when its progress is checked,
 then it is not reported as in flight`,
    (status) => {
      expect(isRunInFlight(status)).toBe(false);
    }
  );
});
