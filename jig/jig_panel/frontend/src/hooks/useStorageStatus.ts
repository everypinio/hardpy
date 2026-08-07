// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";

export type OverallStorageStatus =
  | "standcloud_ready"
  | "standcloud_needs_attention"
  | "local_database_only"
  | "files_only"
  | "storage_error";

export type StandCloudStorageStatus =
  | "configured"
  | "needs_api_key"
  | "autosync_disabled"
  | "not_configured"
  | "check_disabled";

interface StandCloudStatus {
  status: StandCloudStorageStatus;
}

interface LocalDatabaseStatus {
  status: "configured" | "not_configured" | "connection_failed";
}

interface FileStorageStatus {
  folder_path: string;
  folder_url: string;
}

export interface StorageStatus {
  overall_status: OverallStorageStatus;
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
  refreshIntervalMs = 5000
): UseStorageStatusResult => {
  const [data, setData] = React.useState<StorageStatus | null>(null);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  const loadStorageStatus = React.useCallback(async (): Promise<void> => {
    try {
      const response = await fetch("/api/storage_status");
      if (!response.ok) {
        throw new Error(response.statusText);
      }
      const storageStatus = (await response.json()) as StorageStatus;
      setData(storageStatus);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoading(false);
    }
  }, []);

  React.useEffect(() => {
    loadStorageStatus();
    const intervalId = window.setInterval(
      loadStorageStatus,
      refreshIntervalMs
    );

    return () => {
      window.clearInterval(intervalId);
    };
  }, [loadStorageStatus, refreshIntervalMs]);

  return { data, loading, error };
};
