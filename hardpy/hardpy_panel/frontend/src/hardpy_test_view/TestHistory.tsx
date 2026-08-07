// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { withTranslation, WithTranslation } from "react-i18next";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { statusLabel, toDisplayStatus } from "@/lib/testStatus";
import { cn } from "@/lib/utils";
import TestStatus from "./TestStatus";

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
    <Card className="gap-4 py-4">
      <CardHeader className="px-4">
        <CardTitle className="text-base">{t("history.title")}</CardTitle>
      </CardHeader>
      <CardContent className="px-2">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>{t("history.columns.runName")}</TableHead>
              <TableHead>{t("history.columns.startTime")}</TableHead>
              <TableHead>{t("history.columns.result")}</TableHead>
              <TableHead>{t("history.columns.serialNumber")}</TableHead>
              <TableHead className="text-right">
                {t("history.columns.details")}
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {history.map((entry) => {
              const isSelected = selectedHistoryId === entry.id;
              const status = toDisplayStatus(entry.status);

              return (
                <TableRow
                  key={entry.id}
                  data-state={isSelected ? "selected" : undefined}
                  className={cn(isSelected && "bg-accent")}
                >
                  <TableCell className="font-medium whitespace-normal">
                    {entry.name || t("history.unknownRun")}
                  </TableCell>
                  <TableCell className="whitespace-normal text-muted-foreground">
                    {formatTime(entry.start_time)}
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1.5">
                      <TestStatus status={entry.status ?? ""} />
                      {statusLabel(status, t) || entry.status || "-"}
                    </div>
                  </TableCell>
                  <TableCell>{entry.serial_number ?? "-"}</TableCell>
                  <TableCell className="text-right">
                    <Button
                      size="sm"
                      variant={isSelected ? "secondary" : "ghost"}
                      className={cn(!isSelected && "text-primary")}
                      onClick={() => onSelectHistoryRun(entry.id)}
                    >
                      {isSelected
                        ? t("history.selected")
                        : t("history.viewDetails")}
                    </Button>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
};

export default withTranslation()(TestHistory);
