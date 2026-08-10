// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import { describe, expect, test } from "vitest";

import type { StorageRow } from "@/hooks/useStorageData";
import { findStoredRunId, toHistoryEntries } from "./testHistory";

function row(
  id: string,
  doc: Record<string, unknown> | undefined
): StorageRow {
  return {
    id,
    key: id,
    value: { rev: "1" },
    doc,
  };
}

describe("toHistoryEntries", () => {
  test(`given live and history documents,
 when history entries are built,
 then the live document is excluded`, () => {
    const entries = toHistoryEntries(
      [
        row("localhost_8000", {
          name: "Live",
          status: "ready",
          start_time: 100,
        }),
        row("111", {
          name: "Past",
          status: "passed",
          start_time: 90,
        }),
      ],
      "localhost_8000"
    );

    expect(entries.map((entry) => entry.id)).toEqual(["111"]);
  });

  test(`given documents missing name or status,
 when history entries are built,
 then those documents are dropped`, () => {
    const entries = toHistoryEntries(
      [
        row("1", { name: "Named", status: "passed", start_time: 2 }),
        row("2", { name: "No status", start_time: 3 }),
        row("3", { status: "failed", start_time: 4 }),
        row("4", undefined),
      ],
      "live"
    );

    expect(entries.map((entry) => entry.id)).toEqual(["1"]);
  });

  test(`given a run document naming what it executed,
 when history entries are built,
 then that name is carried over`, () => {
    const entries = toHistoryEntries(
      [
        row("1", {
          name: "Full capabilities",
          run_name: "autofocus/fine",
          status: "passed",
          start_time: 2,
        }),
        row("2", {
          name: "Full capabilities",
          status: "passed",
          start_time: 1,
        }),
      ],
      "live"
    );

    expect(entries.map((entry) => entry.run_name)).toEqual([
      "autofocus/fine",
      undefined,
    ]);
  });

  test(`given multiple history runs,
 when history entries are built,
 then they are sorted newest first`, () => {
    const entries = toHistoryEntries(
      [
        row("old", { name: "Old", status: "passed", start_time: 10 }),
        row("new", { name: "New", status: "failed", start_time: 30 }),
        row("mid", { name: "Mid", status: "stopped", start_time: 20 }),
      ],
      "live"
    );

    expect(entries.map((entry) => entry.id)).toEqual(["new", "mid", "old"]);
  });
});

describe("findStoredRunId", () => {
  const storedRuns = [
    row("live", { name: "Live", status: "passed", start_time: 30 }),
    row("111", { name: "Past", status: "passed", start_time: 10 }),
    row("222", { name: "Just finished", status: "passed", start_time: 30 }),
  ];

  test(`given a finished run also kept in the history,
 when its stored run is looked up by start time,
 then the stored id is returned instead of the live document`, () => {
    expect(findStoredRunId(storedRuns, "live", 30)).toBe("222");
  });

  test(`given a run that is not stored yet,
 when its stored run is looked up,
 then nothing is returned`, () => {
    expect(findStoredRunId(storedRuns, "live", 40)).toBeUndefined();
  });

  test(`given a run that never started,
 when its stored run is looked up,
 then nothing is returned`, () => {
    expect(findStoredRunId(storedRuns, "live", undefined)).toBeUndefined();
  });
});
