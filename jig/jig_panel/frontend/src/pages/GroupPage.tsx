// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { ArrowLeft, Folder, Play } from "lucide-react";
import { Link, useParams } from "react-router";
import { useTranslation } from "react-i18next";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { SectionContents } from "@/jig_test_view/SectionContents";
import {
  pageTitleClassName,
  treeIconClassName,
} from "@/jig_test_view/treeStyles";
import {
  buildSectionTree,
  findSection,
  sectionModuleIds,
} from "@/lib/testSections";
import { isRunInFlight, toDisplayStatus } from "@/lib/testStatus";
import { usePanel } from "@/panel/PanelContext";

/**
 * Dedicated page for one section: shows its modules and can re-run the group.
 */
export function GroupPage(): React.ReactElement {
  const { t } = useTranslation();
  const { "*": sectionSplat } = useParams();
  const {
    testRunData,
    appConfig,
    manualCollectMode,
    selectedTests,
    onTestsSelectionChange,
    ultrawide,
    runSection,
  } = usePanel();

  const sectionPath = (sectionSplat ?? "")
    .split("/")
    .map((segment) => segment.trim())
    .filter((segment) => segment.length > 0);

  const tree = buildSectionTree(testRunData.modules ?? {});
  const node = findSection(tree, sectionPath);

  if (!node || sectionPath.length === 0) {
    return (
      <div className="px-4 py-6">
        <Card className="mx-auto max-w-xl py-5">
          <CardContent className="space-y-4 px-5">
            <p className="text-sm text-muted-foreground">
              {t("group.notFound")}
            </p>
            <Button asChild variant="outline">
              <Link to="/">
                <ArrowLeft className="size-4" />
                {t("group.back")}
              </Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const moduleIds = sectionModuleIds(node);
  const runStatus = toDisplayStatus(testRunData.status);
  const isRunDisabled =
    isRunInFlight(runStatus) ||
    Boolean(manualCollectMode) ||
    moduleIds.length === 0;
  const sectionName = sectionPath[sectionPath.length - 1] ?? "";

  return (
    <div className="px-4 py-6">
      <Card className="min-w-0 py-5">
        <CardContent className="space-y-3 px-5">
          <div className="flex flex-wrap items-center gap-2">
            <Button asChild variant="ghost" size="sm">
              <Link to="/">
                <ArrowLeft className="size-4" />
                {t("group.back")}
              </Link>
            </Button>
            <Folder className={treeIconClassName} />
            <h1 className={`${pageTitleClassName} flex-1`}>
              {sectionPath.join(" / ")}
            </h1>
            <Button
              type="button"
              size="sm"
              variant="ghost"
              disabled={isRunDisabled}
              data-testid={`group-run-${sectionPath.join("/")}`}
              aria-label={t("section.runAria", { name: sectionName })}
              onClick={() => runSection(moduleIds)}
            >
              <Play className="size-3.5" />
              {t("section.run")}
            </Button>
          </div>
          <Separator />
          <div className="space-y-0.5">
            <SectionContents
              node={node}
              startIndex={0}
              defaultClose={!ultrawide}
              commonTestRunStatus={testRunData.status}
              onTestsSelectionChange={onTestsSelectionChange}
              selectedTests={selectedTests}
              selectionSupported={
                (appConfig?.frontend?.manual_collect || false) &&
                manualCollectMode
              }
              measurementDisplay={appConfig?.frontend?.measurement_display}
              manualCollectMode={manualCollectMode}
              autoScroll={appConfig?.frontend?.auto_scroll || false}
              onRunSection={runSection}
              onRunModule={(moduleId) => runSection([moduleId])}
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default GroupPage;
