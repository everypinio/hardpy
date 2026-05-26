// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { HTMLTable, Button, Card, H3 } from "@blueprintjs/core";
import { withTranslation, WithTranslation } from "react-i18next";
import TestStatus from "./TestStatus";
import { TestRunI } from "./SuiteList";

export interface HistoryEntry {
  id: string;
  name?: string;
  status?: string;
  start_time?: number;
  serial_number?: string | number;
}

interface Props extends WithTranslation {
  history: HistoryEntry[];
  selectedHistoryId: string | null;
  onSelectHistoryRun: (id: string) => void;
}

const SECONDS_TO_MILLISECONDS = 1000;

const formatTime = (timestamp?: number): string => {
  if (!timestamp) {
    return "-";
  }
  return new Date(timestamp * SECONDS_TO_MILLISECONDS).toLocaleString();
};

const TestHistory: React.FC<Props> = ({
  t,
  history,
  selectedHistoryId,
  onSelectHistoryRun,
}) => {
  if (!history || history.length === 0) {
    return null;
  }

  return (
    <Card style={{ marginTop: "20px" }}>
      <H3>{t("history.title")}</H3>
      <HTMLTable bordered condensed striped style={{ width: "100%" }}>
        <thead>
          <tr>
            <th>{t("history.columns.runName")}</th>
            <th>{t("history.columns.startTime")}</th>
            <th>{t("history.columns.result")}</th>
            <th>{t("history.columns.serialNumber")}</th>
            <th>{t("history.columns.details")}</th>
          </tr>
        </thead>
        <tbody>
          {history.map((entry) => (
            <tr
              key={entry.id}
              style={{
                background:
                  selectedHistoryId === entry.id ? "rgba(16, 119, 255, 0.05)" :
                  "transparent",
              }}
            >
              <td>{entry.name || t("history.unknownRun")}</td>
              <td>{formatTime(entry.start_time)}</td>
              <td>
                <div style={{ display: "flex", alignItems: "center", gap: "5px" }}>
                  <TestStatus status={entry.status || ""} />
                  {entry.status
                    ? t(`app.status.${entry.status}`) || entry.status
                    : "-"}
                </div>
              </td>
              <td>{entry.serial_number ?? "-"}</td>
              <td>
                <Button
                  small
                  minimal
                  intent={selectedHistoryId === entry.id ? "success" : "primary"}
                  text={
                    selectedHistoryId === entry.id
                      ? t("history.selected")
                      : t("history.viewDetails")
                  }
                  onClick={() => onSelectHistoryRun(entry.id)}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </HTMLTable>
    </Card>
  );
};

export default withTranslation()(TestHistory);
