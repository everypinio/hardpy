// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";

import type { StorageRow } from "@/hooks/useStorageData";
import type { TestRunI } from "@/jig_test_view/SuiteList";

export interface AppConfig {
  database?: {
    host?: string;
    port?: number;
    storage_type?: "couchdb" | "json";
  };
  frontend?: {
    full_size_button?: boolean;
    sound_on?: boolean;
    manual_collect?: boolean;
    measurement_display?: boolean;
    test_history?: boolean;
    auto_scroll?: boolean;
    modal_result?: {
      enable?: boolean;
      auto_dismiss_pass?: boolean;
      auto_dismiss_timeout?: number;
    };
    reports_storage_menu?: {
      show_standcloud?: boolean;
      check_standcloud?: boolean;
    };
  };
  current_test_config?: string;
  test_configs?: Array<{
    name: string;
    description: string;
    file?: string;
  }>;
}

export interface PanelContextValue {
  testRunData: TestRunI;
  rows: StorageRow[];
  syncDocumentId: string;
  appConfig: AppConfig | null;
  manualCollectMode: boolean;
  selectedTests: string[];
  onTestsSelectionChange: (tests: string[]) => void;
  ultrawide: boolean;
  useDebugInfo: boolean;
  runSection: (moduleIds: string[]) => void;
  lastRunStatus: string;
}

const PanelContext = React.createContext<PanelContextValue | null>(null);

/**
 * Provides shared panel state to routed pages.
 */
export function PanelProvider({
  value,
  children,
}: {
  value: PanelContextValue;
  children: React.ReactNode;
}): React.ReactElement {
  return (
    <PanelContext.Provider value={value}>{children}</PanelContext.Provider>
  );
}

/**
 * Reads the panel context. Must be used under a PanelProvider.
 */
export function usePanel(): PanelContextValue {
  const value = React.useContext(PanelContext);
  if (!value) {
    throw new Error("usePanel must be used within a PanelProvider");
  }
  return value;
}
