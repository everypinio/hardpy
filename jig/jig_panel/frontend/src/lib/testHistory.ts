// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import type { StorageRow } from "@/hooks/useStorageData";
import type { HistoryEntry } from "@/jig_test_view/TestHistory";
import type { TestRunI } from "@/jig_test_view/SuiteList";

/**
 * Builds history entries from storage rows, excluding the live sync document.
 * Entries missing a name or status are dropped. Newest runs come first.
 *
 * @param {StorageRow[]} rows - All storage documents.
 * @param {string} syncDocumentId - Live run document id to exclude.
 * @returns {HistoryEntry[]} Sorted history entries.
 */
export function toHistoryEntries(
  rows: StorageRow[],
  syncDocumentId: string
): HistoryEntry[] {
  return rows
    .map((row) => {
      const doc = row.doc as TestRunI | undefined;
      if (!doc || !doc.name || !doc.status) {
        return null;
      }

      return {
        id: row.id,
        name: doc.name,
        status: doc.status,
        start_time: doc.start_time,
        serial_number: doc.dut?.serial_number,
      };
    })
    .filter((entry) => entry && entry.id !== syncDocumentId)
    .filter((entry): entry is HistoryEntry => entry !== null)
    .sort((a, b) => (b.start_time ?? 0) - (a.start_time ?? 0));
}
