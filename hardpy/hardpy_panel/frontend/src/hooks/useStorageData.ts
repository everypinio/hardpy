// Copyright (c) 2025 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { useAllDocs } from "use-pouchdb";

type StorageState = "loading" | "done" | "error";

interface StorageRow {
  id: string;
  key: string;
  value: { rev: string };
  doc: any;
}

interface StorageData {
  rows: StorageRow[];
  state: StorageState;
  loading: boolean;
  error: Error | null;
  /** Total number of history runs in storage (JSON storage only) */
  historyTotal?: number;
}

interface StorageTypeResponse {
  storage_type: string;
}

interface JsonDataResponse {
  rows: StorageRow[];
  total_rows: number;
  history_total?: number;
  error?: string;
}

const JSON_POLL_INTERVAL_MS = 500;

/**
 * Custom hook to fetch data from either JSON storage or CouchDB
 * Automatically detects storage type and uses appropriate method
 *
 * With JSON storage the current run is polled, while the test history
 * is fetched only on load and when the number of history runs changes
 * (a run has finished), because history documents never change.
 * @param {number} historyLimit - Number of newest history runs to fetch
 *   from JSON storage
 */
export const useStorageData = (historyLimit: number): StorageData => {
  const [storageType, setStorageType] = React.useState<string | null>(null);
  const [currentRows, setCurrentRows] = React.useState<StorageRow[]>([]);
  const [historyRows, setHistoryRows] = React.useState<StorageRow[]>([]);
  const [jsonLoading, setJsonLoading] = React.useState(true);
  const [jsonError, setJsonError] = React.useState<Error | null>(null);
  const [historyTotal, setHistoryTotal] = React.useState<number | undefined>(
    undefined
  );

  // Fetch storage type on mount
  React.useEffect(() => {
    fetch("/api/storage_type")
      .then((res) => res.json())
      .then((data: StorageTypeResponse) => {
        setStorageType(data.storage_type);
      })
      .catch((err) => {
        console.error("Failed to fetch storage type:", err);
        setStorageType("couchdb"); // Default to CouchDB
      });
  }, []);

  // For JSON storage, poll the current run only.
  // The next request is scheduled only after the previous one finishes,
  // so slow responses never pile up.
  React.useEffect(() => {
    if (storageType !== "json") return;

    let cancelled = false;
    let timeout: ReturnType<typeof setTimeout> | undefined;
    const controller = new AbortController();

    const fetchCurrentRun = () => {
      fetch("/api/json_data?history_limit=0", { signal: controller.signal })
        .then((res) => res.json())
        .then((data: JsonDataResponse) => {
          if (cancelled) return;
          if (data.error) {
            setJsonError(new Error(data.error));
          } else {
            setCurrentRows(data.rows);
            setHistoryTotal(data.history_total);
            setJsonError(null);
          }
          setJsonLoading(false);
        })
        .catch((err) => {
          if (cancelled) return;
          setJsonError(err);
          setJsonLoading(false);
        })
        .finally(() => {
          if (!cancelled) {
            timeout = setTimeout(fetchCurrentRun, JSON_POLL_INTERVAL_MS);
          }
        });
    };

    fetchCurrentRun();

    return () => {
      cancelled = true;
      controller.abort();
      clearTimeout(timeout);
    };
  }, [storageType]);

  // For JSON storage, fetch history once the history size is known and
  // again only when it changes or more runs are requested
  React.useEffect(() => {
    if (storageType !== "json" || historyTotal === undefined) return;
    if (historyLimit === 0) {
      setHistoryRows([]);
      return;
    }

    const controller = new AbortController();
    fetch(`/api/json_data?history_limit=${historyLimit}`, {
      signal: controller.signal,
    })
      .then((res) => res.json())
      .then((data: JsonDataResponse) => {
        if (!data.error) {
          setHistoryRows(data.rows);
        }
      })
      .catch((err) => {
        if (err.name !== "AbortError") {
          console.error("Failed to fetch test history:", err);
        }
      });

    return () => controller.abort();
  }, [storageType, historyLimit, historyTotal]);

  // Current run rows take precedence over the same rows from history fetch
  const jsonRows = React.useMemo(() => {
    const currentIds = new Set(currentRows.map((row) => row.id));
    return [
      ...currentRows,
      ...historyRows.filter((row) => !currentIds.has(row.id)),
    ];
  }, [currentRows, historyRows]);

  // For CouchDB, use the existing PouchDB hook
  const pouchDbData = useAllDocs({
    include_docs: true,
  });

  // Return appropriate data based on storage type
  if (storageType === null) {
    // Still detecting storage type
    return {
      rows: [],
      state: "loading",
      loading: true,
      error: null,
    };
  }

  if (storageType === "json") {
    return {
      rows: jsonRows,
      state: jsonError ? "error" : jsonLoading ? "loading" : "done",
      loading: jsonLoading,
      error: jsonError,
      historyTotal,
    };
  }

  // Default to CouchDB
  return pouchDbData;
};
