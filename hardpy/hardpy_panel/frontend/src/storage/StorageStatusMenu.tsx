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
} from "@blueprintjs/core";

import {
  OverallStorageStatus,
  StorageStatus,
  useStorageStatus,
} from "../hooks/useStorageStatus";

const STATUS_COLORS: Record<OverallStorageStatus | "loading" | "error", string> =
  {
    standcloud_ready: Colors.GREEN3,
    standcloud_needs_attention: Colors.ORANGE3,
    local_database_only: Colors.GRAY2,
    files_only: Colors.GRAY2,
    loading: Colors.GRAY3,
    error: Colors.RED3,
  };

const POPOVER_WIDTH = 340;

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

const helpTextStyle: React.CSSProperties = {
  color: Colors.GRAY2,
  fontSize: "12px",
  lineHeight: 1.35,
  marginTop: "2px",
  wordBreak: "break-word",
};

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

  return (
    <div style={{ width: POPOVER_WIDTH, padding: "14px" }}>
      <strong>{t("storageStatus.title")}</strong>
      <div style={helpTextStyle}>
        {t("storageStatus.configuredIn", {
          file: data.configured_in,
        })}
      </div>

      <Divider />

      <div style={sectionStyle}>
        <Icon icon="cloud" color={Colors.BLUE3} />
        <div>
          <div>
            <strong>{t("storageStatus.standcloud.title")}</strong>
          </div>
          <div style={statusTextStyle}>
            {t(`storageStatus.standcloud.statuses.${data.standcloud.status}`)}
          </div>
          <div style={helpTextStyle}>
            {t("storageStatus.standcloud.description")}
          </div>
          <div style={helpTextStyle}>
            {t("storageStatus.standcloud.address", {
              address: data.standcloud.address,
            })}
          </div>
          {data.standcloud.api_key_configured ? (
            <div style={helpTextStyle}>
              {t("storageStatus.standcloud.apiKey", {
                apiKey: data.standcloud.api_key_display,
              })}
            </div>
          ) : (
            <StorageLinkButton
              href={data.standcloud.api_key_url}
              text={t("storageStatus.standcloud.apiKeyLink")}
            />
          )}
        </div>
      </div>

      <Divider />

      <div style={sectionStyle}>
        <Icon icon="database" color={Colors.GREEN3} />
        <div>
          <div>
            <strong>{t("storageStatus.localDatabase.title")}</strong>
          </div>
          <div style={statusTextStyle}>
            {t(
              `storageStatus.localDatabase.statuses.${data.local_database.status}`
            )}
          </div>
          <div style={helpTextStyle}>
            {t("storageStatus.localDatabase.description")}
          </div>
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
        </div>
      </div>

      {data.files.visible && (
        <>
          <Divider />
          <div style={sectionStyle}>
            <Icon icon="document" color={Colors.GRAY2} />
            <div>
              <div>
                <strong>{t("storageStatus.files.title")}</strong>
              </div>
              <div style={statusTextStyle}>
                {t(`storageStatus.files.statuses.${data.files.status}`)}
              </div>
              <div style={helpTextStyle}>
                {t("storageStatus.files.description")}
              </div>
              <div style={helpTextStyle}>
                {t("storageStatus.files.folderPath", {
                  path: data.files.folder_path,
                })}
              </div>
              <StorageLinkButton
                href={data.files.folder_url}
                text={t("storageStatus.files.openFolder")}
              />
            </div>
          </div>
        </>
      )}
    </div>
  );
};

const StorageStatusMenu = (): JSX.Element => {
  const { t } = useTranslation();
  const { data, loading, error } = useStorageStatus();
  const statusColor = getStatusColor(data, loading, error);

  return (
    <Popover
      content={
        <StorageStatusContent data={data} loading={loading} error={error} />
      }
    >
      <Button
        className="bp3-minimal"
        icon="database"
        title={t("storageStatus.iconLabel")}
        aria-label={t("storageStatus.iconLabel")}
        style={{ color: statusColor, position: "relative" }}
      >
        <span
          aria-hidden="true"
          style={{
            position: "absolute",
            right: "6px",
            bottom: "5px",
            width: "7px",
            height: "7px",
            borderRadius: "50%",
            background: statusColor,
            border: `1px solid ${Colors.LIGHT_GRAY5}`,
          }}
        />
      </Button>
    </Popover>
  );
};

export default StorageStatusMenu;
