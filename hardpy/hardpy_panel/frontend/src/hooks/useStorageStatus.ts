// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";

export type OverallStorageStatus =
  | "standcloud_ready"
  | "standcloud_needs_attention"
  | "local_database_only"
  | "files_only";

export type StandCloudStorageStatus =
  | "configured"
  | "needs_api_key"
  | "autosync_disabled"
  | "not_configured";

interface StandCloudStatus {
  configured: boolean;
  autosync: boolean;
  address: string;
  api_key_configured: boolean;
  api_key_display: string;
  api_key_url: string;
  status: StandCloudStorageStatus;
  docs_url: string;
}

interface LocalDatabaseStatus {
  configured: boolean;
  type: "couchdb";
  status: "configured" | "not_configured";
  management_url: string;
  docs_url: string;
}

interface FileStorageStatus {
  visible: boolean;
  configured: boolean;
  type: "json";
  status: "configured" | "hidden";
  folder_path: string;
  folder_url: string;
  docs_url: string;
}

export interface StorageStatus {
  primary: "standcloud";
  overall_status: OverallStorageStatus;
  configured_in: string;
  standcloud: StandCloudStatus;
  local_database: LocalDatabaseStatus;
  files: FileStorageStatus;
}

interface UseStorageStatusResult {
  data: StorageStatus | null;
  loading: boolean;
  error: string | null;
}

export const useStorageStatus = (
  refreshIntervalMs = 60000
): UseStorageStatusResult => {
  const [data, setData] = React.useState<StorageStatus | null>(null);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    let cancelled = false;

    const loadStorageStatus = async (): Promise<void> => {
      try {
        const response = await fetch("/api/storage_status");
        if (!response.ok) {
          throw new Error(response.statusText);
        }
        const storageStatus = (await response.json()) as StorageStatus;
        if (!cancelled) {
          setData(storageStatus);
          setError(null);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : String(err));
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    loadStorageStatus();
    const intervalId = window.setInterval(
      loadStorageStatus,
      refreshIntervalMs
    );

    return () => {
      cancelled = true;
      window.clearInterval(intervalId);
    };
  }, [refreshIntervalMs]);

  return { data, loading, error };
};
