// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import {
  Cloud,
  Copy,
  Database,
  ExternalLink,
  FileText,
  Info,
} from "lucide-react";
import { useTranslation } from "react-i18next";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Separator } from "@/components/ui/separator";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { cn } from "@/lib/utils";

import {
  OverallStorageStatus,
  StorageStatus,
} from "../hooks/useStorageStatus";

const OVERALL_STATUS_ICON_COLORS: Record<
  OverallStorageStatus | "loading" | "error",
  string
> = {
  standcloud_ready: "text-success",
  standcloud_needs_attention: "text-destructive",
  local_database_only: "text-success",
  files_only: "text-success",
  storage_error: "text-destructive",
  loading: "text-muted-foreground",
  error: "text-destructive",
};

const SECTION_STATUS_TEXT_COLORS: Record<string, string> = {
  configured: "text-success",
  not_configured: "text-destructive",
  needs_api_key: "text-destructive",
  connection_failed: "text-destructive",
  autosync_disabled: "text-warning",
  check_disabled: "text-muted-foreground",
};

const DEFAULT_STATUS_TEXT_COLOR = "text-foreground";

const STANDCLOUD_API_KEYS_URL =
  "https://standcloud.everypin.io/dashboard/organization-profile/organization-api-keys?utm_source=hardpy_UI";
const COUCHDB_DOCS_URL =
  "https://everypinio.github.io/hardpy/documentation/database/#couchdb-instance";
const DEFAULT_COUCHDB_HOST = "localhost";
const DEFAULT_COUCHDB_PORT = 5984;
const PATH_COPIED_TOAST_DURATION_MS = 2000;

interface HardpyStorageMenuConfig {
  database?: {
    host?: string;
    port?: number;
    storage_type?: "couchdb" | "json";
  };
  frontend?: {
    reports_storage_menu?: {
      show_standcloud?: boolean;
      check_standcloud?: boolean;
    };
  };
}

const isStandCloudVisible = (
  hardpyConfig: HardpyStorageMenuConfig | null
): boolean =>
  hardpyConfig?.frontend?.reports_storage_menu?.show_standcloud ?? true;

const isStandCloudCheckEnabled = (
  hardpyConfig: HardpyStorageMenuConfig | null
): boolean =>
  hardpyConfig?.frontend?.reports_storage_menu?.check_standcloud ?? true;

const getStorageType = (
  hardpyConfig: HardpyStorageMenuConfig | null
): "couchdb" | "json" => hardpyConfig?.database?.storage_type ?? "couchdb";

const hasStorageProblem = (
  data: StorageStatus,
  hardpyConfig: HardpyStorageMenuConfig | null
): boolean => {
  const standcloudProblem =
    isStandCloudVisible(hardpyConfig) &&
    isStandCloudCheckEnabled(hardpyConfig) &&
    data.standcloud.status !== "configured";
  const localDatabaseProblem =
    getStorageType(hardpyConfig) === "couchdb" &&
    data.local_database.status === "connection_failed";

  return standcloudProblem || localDatabaseProblem;
};

const getMenuIconColor = (
  data: StorageStatus | null,
  loading: boolean,
  error: string | null,
  hardpyConfig: HardpyStorageMenuConfig | null
): string => {
  if (error) {
    return OVERALL_STATUS_ICON_COLORS.error;
  }
  if (loading || data === null) {
    return OVERALL_STATUS_ICON_COLORS.loading;
  }
  if (hasStorageProblem(data, hardpyConfig)) {
    return OVERALL_STATUS_ICON_COLORS.storage_error;
  }
  return OVERALL_STATUS_ICON_COLORS.standcloud_ready;
};

const getStatusTextColor = (status: string): string =>
  SECTION_STATUS_TEXT_COLORS[status] ?? DEFAULT_STATUS_TEXT_COLOR;

const InfoTooltip = ({ content }: { content: string }): JSX.Element => (
  <Tooltip>
    <TooltipTrigger asChild>
      <span
        aria-label={content}
        role="img"
        className="inline-flex cursor-help leading-none text-muted-foreground"
      >
        <Info className="size-3.5" />
      </span>
    </TooltipTrigger>
    <TooltipContent side="top">{content}</TooltipContent>
  </Tooltip>
);

const StorageLinkButton = ({
  href,
  text,
}: {
  href: string;
  text: string;
}): JSX.Element => (
  <Button asChild variant="link" size="sm" className="mt-1 h-auto px-0">
    <a href={href} target="_blank" rel="noreferrer">
      {text}
      <ExternalLink aria-hidden="true" />
    </a>
  </Button>
);

const SectionHeading = ({ children }: { children: React.ReactNode }) => (
  <div className="mt-2.5 text-xs font-bold uppercase text-muted-foreground">
    {children}
  </div>
);

const StorageSection = ({
  icon,
  title,
  tooltip,
  children,
}: {
  icon: React.ReactNode;
  title: string;
  tooltip: string;
  children: React.ReactNode;
}): JSX.Element => (
  <div className="grid grid-cols-[24px_1fr] items-start gap-x-2.5 py-2.5">
    {icon}
    <div className="min-w-0">
      <div className="inline-flex items-center gap-1">
        <strong className="text-sm">{title}</strong>
        <InfoTooltip content={tooltip} />
      </div>
      {children}
    </div>
  </div>
);

const StorageStatusContent = ({
  data,
  loading,
  error,
  hardpyConfig,
}: {
  data: StorageStatus | null;
  loading: boolean;
  error: string | null;
  hardpyConfig: HardpyStorageMenuConfig | null;
}): JSX.Element => {
  const { t } = useTranslation();

  const copyFileStoragePath = async (): Promise<void> => {
    if (data?.files.folder_path) {
      await navigator.clipboard.writeText(data.files.folder_path);
      toast.success(t("storageStatus.pathCopied"), {
        duration: PATH_COPIED_TOAST_DURATION_MS,
      });
    }
  };

  if (loading && data === null) {
    return <div className="text-sm">{t("storageStatus.loading")}</div>;
  }

  if (error || data === null) {
    return (
      <div>
        <strong className="text-sm">{t("storageStatus.title")}</strong>
        <p className="mt-2 text-xs text-muted-foreground">
          {t("storageStatus.unavailable")}
        </p>
      </div>
    );
  }

  const isFilesBackend = getStorageType(hardpyConfig) === "json";
  const standcloudVisible = isStandCloudVisible(hardpyConfig);
  const standcloudCheckEnabled = isStandCloudCheckEnabled(hardpyConfig);
  const localDatabaseConfigured = getStorageType(hardpyConfig) === "couchdb";
  const LocalBackendIcon = isFilesBackend ? FileText : Database;
  const localBackendIconColor = isFilesBackend
    ? "text-muted-foreground"
    : data.local_database.status === "connection_failed"
      ? "text-destructive"
      : "text-success";
  const localBackendTitle = isFilesBackend
    ? t("storageStatus.files.title")
    : t("storageStatus.localDatabase.title");
  const localBackendTooltip = isFilesBackend
    ? t("storageStatus.tooltips.files")
    : t("storageStatus.tooltips.localDatabase");
  const standcloudIconColor = !standcloudCheckEnabled
    ? "text-muted-foreground"
    : data.standcloud.status === "configured"
      ? "text-success"
      : "text-destructive";
  const couchDbPanelUrl = `http://${
    hardpyConfig?.database?.host ?? DEFAULT_COUCHDB_HOST
  }:${hardpyConfig?.database?.port ?? DEFAULT_COUCHDB_PORT}/_utils/`;

  return (
    <div>
      <div className="inline-flex items-center gap-1">
        <strong className="text-sm">{t("storageStatus.title")}</strong>
        <InfoTooltip content={t("storageStatus.tooltips.reportsStorage")} />
      </div>

      <Separator className="mt-2" />

      {standcloudVisible && (
        <>
          <SectionHeading>{t("storageStatus.cloudStorage")}</SectionHeading>

          <StorageSection
            icon={<Cloud className={cn("size-4", standcloudIconColor)} />}
            title={t("storageStatus.standcloud.title")}
            tooltip={t("storageStatus.tooltips.standcloud")}
          >
            <div
              className={cn(
                "text-sm font-semibold",
                getStatusTextColor(data.standcloud.status)
              )}
            >
              {t(`storageStatus.standcloud.statuses.${data.standcloud.status}`)}
            </div>
            {data.standcloud.status === "needs_api_key" &&
              standcloudCheckEnabled && (
                <StorageLinkButton
                  href={STANDCLOUD_API_KEYS_URL}
                  text={t("storageStatus.standcloud.apiKeyLink")}
                />
              )}
          </StorageSection>

          <Separator />
        </>
      )}

      <SectionHeading>{t("storageStatus.localStorage")}</SectionHeading>

      <StorageSection
        icon={<LocalBackendIcon className={cn("size-4", localBackendIconColor)} />}
        title={localBackendTitle}
        tooltip={localBackendTooltip}
      >
        {isFilesBackend ? (
          <>
            <div
              className={cn(
                "text-sm font-semibold",
                getStatusTextColor("configured")
              )}
            >
              {t("storageStatus.files.statuses.configured")}
            </div>
            <div className="mt-0.5 flex items-center gap-1 text-xs break-words text-muted-foreground">
              <span>
                {t("storageStatus.files.folderPath", {
                  path: data.files.folder_path,
                })}
              </span>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    aria-label={t("storageStatus.copyPath")}
                    variant="ghost"
                    size="icon-xs"
                    className="shrink-0"
                    onClick={copyFileStoragePath}
                  >
                    <Copy aria-hidden="true" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent side="top">
                  {t("storageStatus.copyPath")}
                </TooltipContent>
              </Tooltip>
            </div>
            <StorageLinkButton
              href={data.files.folder_url}
              text={t("storageStatus.files.openFolder")}
            />
          </>
        ) : (
          <>
            <div
              className={cn(
                "text-sm font-semibold",
                getStatusTextColor(data.local_database.status)
              )}
            >
              {t(
                `storageStatus.localDatabase.statuses.${data.local_database.status}`
              )}
            </div>
            {data.local_database.status === "connection_failed" &&
              localDatabaseConfigured && (
                <p className="mt-0.5 text-xs text-destructive">
                  {t("storageStatus.localDatabase.connectionFailedMessage")}
                </p>
              )}
            <StorageLinkButton
              href={localDatabaseConfigured ? couchDbPanelUrl : COUCHDB_DOCS_URL}
              text={
                localDatabaseConfigured
                  ? t("storageStatus.localDatabase.openPanel")
                  : t("storageStatus.localDatabase.docs")
              }
            />
          </>
        )}
      </StorageSection>
    </div>
  );
};

const StorageStatusMenu = ({
  data,
  loading,
  error,
  hardpyConfig,
}: {
  data: StorageStatus | null;
  loading: boolean;
  error: string | null;
  hardpyConfig: HardpyStorageMenuConfig | null;
}): JSX.Element => {
  const { t } = useTranslation();
  const statusColor = getMenuIconColor(data, loading, error, hardpyConfig);

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button
          variant="ghost"
          size="icon"
          title={t("storageStatus.iconLabel")}
          aria-label={t("storageStatus.iconLabel")}
        >
          <Database aria-hidden="true" className={statusColor} />
        </Button>
      </PopoverTrigger>
      <PopoverContent align="end" className="w-[340px] p-3.5">
        <StorageStatusContent
          data={data}
          loading={loading}
          error={error}
          hardpyConfig={hardpyConfig}
        />
      </PopoverContent>
    </Popover>
  );
};

export default StorageStatusMenu;
