// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import { describe, expect, test } from "vitest";

import type { StorageRow } from "@/hooks/useStorageData";
import { toHistoryEntries } from "./testHistory";

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
