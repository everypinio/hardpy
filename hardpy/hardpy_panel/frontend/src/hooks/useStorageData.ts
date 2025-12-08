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
}

interface StorageTypeResponse {
  storage_type: string;
}

interface JsonDataResponse {
  rows: StorageRow[];
  total_rows: number;
  error?: string;
}

/**
 * Custom hook to fetch data from either JSON storage or CouchDB
 * Automatically detects storage type and uses appropriate method
 */
export const useStorageData = (): StorageData => {
  const [storageType, setStorageType] = React.useState<string | null>(null);
  const [jsonData, setJsonData] = React.useState<StorageRow[]>([]);
  const [jsonLoading, setJsonLoading] = React.useState(true);
  const [jsonError, setJsonError] = React.useState<Error | null>(null);

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

  // For JSON storage, poll the API endpoint
  React.useEffect(() => {
    if (storageType !== "json") return;

    const fetchJsonData = () => {
      fetch("/api/json_data")
        .then((res) => res.json())
        .then((data: JsonDataResponse) => {
          if (data.error) {
            setJsonError(new Error(data.error));
            setJsonLoading(false);
          } else {
            setJsonData(data.rows);
            setJsonLoading(false);
            setJsonError(null);
          }
        })
        .catch((err) => {
          setJsonError(err);
          setJsonLoading(false);
        });
    };

    // Initial fetch
    fetchJsonData();

    // Poll every 500ms for updates
    const interval = setInterval(fetchJsonData, 500);

    return () => clearInterval(interval);
  }, [storageType]);

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
      rows: jsonData,
      state: jsonError ? "error" : jsonLoading ? "loading" : "done",
      loading: jsonLoading,
      error: jsonError,
    };
  }

  // Default to CouchDB
  return pouchDbData;
};
