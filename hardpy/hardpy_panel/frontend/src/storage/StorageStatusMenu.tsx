// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { useTranslation } from "react-i18next";

import {
  AnchorButton,
  Button,
  Colors,
  Divider,
  Icon,
  Popover,
  Position,
  Toaster,
  Tooltip,
} from "@blueprintjs/core";

import {
  OverallStorageStatus,
  StorageStatus,
} from "../hooks/useStorageStatus";

const STATUS_COLORS: Record<OverallStorageStatus | "loading" | "error", string> =
  {
    standcloud_ready: Colors.GREEN3,
    standcloud_needs_attention: Colors.RED3,
    local_database_only: Colors.GREEN3,
    files_only: Colors.GREEN3,
    storage_error: Colors.RED3,
    loading: Colors.GRAY3,
    error: Colors.RED3,
  };

const POPOVER_WIDTH = 340;

const storageToaster = Toaster.create({
  position: Position.TOP,
});

const getStatusColor = (
  data: StorageStatus | null,
  loading: boolean,
  error: string | null
): string => {
  if (error) {
    return STATUS_COLORS.error;
  }
  if (loading || data === null) {
    return STATUS_COLORS.loading;
  }
  return STATUS_COLORS[data.overall_status];
};

const hasStorageProblem = (data: StorageStatus): boolean => {
  const standcloudProblem =
    data.standcloud.visible &&
    data.standcloud.check_enabled &&
    !data.standcloud.configured;
  const localDatabaseProblem =
    data.local_database.configured &&
    data.local_database.status === "connection_failed";

  return standcloudProblem || localDatabaseProblem;
};

const getMenuIconColor = (
  data: StorageStatus | null,
  loading: boolean,
  error: string | null
): string => {
  if (error) {
    return STATUS_COLORS.error;
  }
  if (loading || data === null) {
    return STATUS_COLORS.loading;
  }
  if (hasStorageProblem(data)) {
    return Colors.RED3;
  }
  return Colors.GREEN3;
};

const sectionStyle: React.CSSProperties = {
  display: "grid",
  gridTemplateColumns: "24px 1fr",
  columnGap: "10px",
  alignItems: "start",
  padding: "10px 0",
};

const statusTextStyle: React.CSSProperties = {
  color: Colors.GRAY1,
  fontWeight: 600,
};

const STATUS_TEXT_COLORS: Record<string, string> = {
  configured: Colors.GREEN3,
  not_configured: Colors.RED3,
  needs_api_key: Colors.RED3,
  connection_failed: Colors.RED3,
  autosync_disabled: Colors.ORANGE3,
  check_disabled: Colors.GRAY2,
};

const helpTextStyle: React.CSSProperties = {
  color: Colors.GRAY2,
  fontSize: "12px",
  lineHeight: 1.35,
  marginTop: "2px",
  wordBreak: "break-word",
};

const headingStyle: React.CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  gap: "4px",
};

const groupHeadingStyle: React.CSSProperties = {
  color: Colors.GRAY2,
  fontSize: "12px",
  fontWeight: 700,
  marginTop: "10px",
  textTransform: "uppercase",
};

const InfoTooltip = ({
  content,
}: {
  content: string;
}): JSX.Element => (
  <Tooltip content={content} position={Position.TOP}>
    <span
      aria-label={content}
      role="img"
      style={{
        color: Colors.GRAY2,
        cursor: "help",
        display: "inline-flex",
        lineHeight: 1,
      }}
    >
      <Icon icon="info-sign" size={14} />
    </span>
  </Tooltip>
);

const StorageLinkButton = ({
  href,
  text,
}: {
  href: string;
  text: string;
}): JSX.Element => (
  <AnchorButton
    href={href}
    target="_blank"
    rel="noreferrer"
    minimal={true}
    small={true}
    rightIcon="share"
    text={text}
    style={{ paddingLeft: 0, marginTop: "4px" }}
  />
);

const getStatusTextStyle = (status: string): React.CSSProperties => ({
  ...statusTextStyle,
  color: STATUS_TEXT_COLORS[status] ?? statusTextStyle.color,
});

const StorageStatusContent = ({
  data,
  loading,
  error,
}: {
  data: StorageStatus | null;
  loading: boolean;
  error: string | null;
}): JSX.Element => {
  const { t } = useTranslation();

  const copyFileStoragePath = async (): Promise<void> => {
    if (data?.files.folder_path) {
      await navigator.clipboard.writeText(data.files.folder_path);
      storageToaster.show({
        message: t("storageStatus.pathCopied"),
        intent: "success",
        timeout: 2000,
      });
    }
  };

  if (loading && data === null) {
    return (
      <div style={{ width: POPOVER_WIDTH, padding: "14px" }}>
        {t("storageStatus.loading")}
      </div>
    );
  }

  if (error || data === null) {
    return (
      <div style={{ width: POPOVER_WIDTH, padding: "14px" }}>
        <strong>{t("storageStatus.title")}</strong>
        <div style={{ ...helpTextStyle, marginTop: "8px" }}>
          {t("storageStatus.unavailable")}
        </div>
      </div>
    );
  }

  const isFilesBackend = data.local_storage.type === "json";
  const localBackendIcon = isFilesBackend ? "document" : "database";
  const localBackendIconColor = isFilesBackend
    ? Colors.GRAY2
    : data.local_database.status === "connection_failed"
      ? Colors.RED3
      : Colors.GREEN3;
  const localBackendTitle = isFilesBackend
    ? t("storageStatus.files.title")
    : t("storageStatus.localDatabase.title");
  const localBackendTooltip = isFilesBackend
    ? t("storageStatus.tooltips.files")
    : t("storageStatus.tooltips.localDatabase");
  const standcloudIconColor = !data.standcloud.check_enabled
    ? Colors.GRAY2
    : data.standcloud.configured
      ? Colors.GREEN3
      : Colors.RED3;

  return (
    <div style={{ width: POPOVER_WIDTH, padding: "14px" }}>
      <div style={headingStyle}>
        <strong>{t("storageStatus.title")}</strong>
        <InfoTooltip content={t("storageStatus.tooltips.reportsStorage")} />
      </div>

      <Divider />

      {data.standcloud.visible && (
        <>
          <div style={groupHeadingStyle}>{t("storageStatus.cloudStorage")}</div>

          <div style={sectionStyle}>
            <Icon icon="cloud" color={standcloudIconColor} />
            <div>
              <div style={headingStyle}>
                <strong>{t("storageStatus.standcloud.title")}</strong>
                <InfoTooltip content={t("storageStatus.tooltips.standcloud")} />
              </div>
              <div style={getStatusTextStyle(data.standcloud.status)}>
                {t(
                  `storageStatus.standcloud.statuses.${data.standcloud.status}`
                )}
              </div>
              {!data.standcloud.api_key_configured &&
                data.standcloud.check_enabled && (
                  <StorageLinkButton
                    href={data.standcloud.api_key_url}
                    text={t("storageStatus.standcloud.apiKeyLink")}
                  />
                )}
            </div>
          </div>

          <Divider />
        </>
      )}

      <div style={groupHeadingStyle}>{t("storageStatus.localStorage")}</div>

      <div style={sectionStyle}>
        <Icon icon={localBackendIcon} color={localBackendIconColor} />
        <div>
          <div style={headingStyle}>
            <strong>{localBackendTitle}</strong>
            <InfoTooltip content={localBackendTooltip} />
          </div>
          {isFilesBackend ? (
            <>
              <div style={getStatusTextStyle(data.files.status)}>
                {t(`storageStatus.files.statuses.${data.files.status}`)}
              </div>
              <div
                style={{
                  ...helpTextStyle,
                  display: "flex",
                  alignItems: "center",
                  gap: "4px",
                }}
              >
                <span>
                  {t("storageStatus.files.folderPath", {
                    path: data.files.folder_path,
                  })}
                </span>
                <Tooltip
                  content={t("storageStatus.copyPath")}
                  position={Position.TOP}
                >
                  <Button
                    aria-label={t("storageStatus.copyPath")}
                    icon="duplicate"
                    minimal={true}
                    small={true}
                    onClick={copyFileStoragePath}
                    style={{ flex: "0 0 auto", minWidth: "20px" }}
                  />
                </Tooltip>
              </div>
              <StorageLinkButton
                href={data.files.folder_url}
                text={t("storageStatus.files.openFolder")}
              />
            </>
          ) : (
            <>
              <div style={getStatusTextStyle(data.local_database.status)}>
                {t(
                  `storageStatus.localDatabase.statuses.${data.local_database.status}`
                )}
              </div>
              {data.local_database.status === "connection_failed" &&
                data.local_database.message && (
                  <div style={{ ...helpTextStyle, color: Colors.RED3 }}>
                    {data.local_database.message}
                  </div>
                )}
              <StorageLinkButton
                href={
                  data.local_database.configured
                    ? data.local_database.management_url
                    : data.local_database.docs_url
                }
                text={
                  data.local_database.configured
                    ? t("storageStatus.localDatabase.openPanel")
                    : t("storageStatus.localDatabase.docs")
                }
              />
            </>
          )}
        </div>
      </div>
    </div>
  );
};

const StorageStatusMenu = ({
  data,
  loading,
  error,
}: {
  data: StorageStatus | null;
  loading: boolean;
  error: string | null;
}): JSX.Element => {
  const { t } = useTranslation();
  const statusColor = getMenuIconColor(data, loading, error);

  return (
    <Popover
      content={
        <StorageStatusContent data={data} loading={loading} error={error} />
      }
    >
      <Button
        className="bp3-minimal"
        icon={<Icon icon="database" color={statusColor} />}
        title={t("storageStatus.iconLabel")}
        aria-label={t("storageStatus.iconLabel")}
      />
    </Popover>
  );
};

export default StorageStatusMenu;
