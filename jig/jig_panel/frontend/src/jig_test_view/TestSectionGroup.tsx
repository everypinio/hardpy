// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { ChevronDown, ChevronRight, Folder, Play } from "lucide-react";
import { Link, useNavigate } from "react-router";
import { useTranslation } from "react-i18next";

import { Button } from "@/components/ui/button";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import {
  initialFoldState,
  isUnfolded,
  nextFoldState,
  operatorFoldState,
} from "@/lib/foldState";
import {
  SectionNode,
  sectionModuleIds,
  sectionStatuses,
} from "@/lib/testSections";
import { aggregateStatus, isRunInFlight, toDisplayStatus } from "@/lib/testStatus";
import { SectionContents } from "./SectionContents";
import { TestStatus } from "./TestStatus";
import {
  treeChildrenClassName,
  treeIconClassName,
  treeLabelClassName,
  treeMetaClassName,
  treeRowClassName,
} from "./treeStyles";

interface Props {
  node: SectionNode;
  /** Starting module index for continuous numbering across the tree. */
  startIndex: number;
  defaultClose: boolean;
  commonTestRunStatus?: string;
  onTestsSelectionChange?: (selectedTests: string[]) => void;
  selectedTests?: string[];
  selectionSupported?: boolean;
  measurementDisplay?: boolean;
  manualCollectMode?: boolean;
  autoScroll?: boolean;
  onRunSection?: (moduleIds: string[], runName: string) => void;
  onRunModule?: (moduleId: string) => void;
}

/**
 * Collapsible section row in the tests file-tree.
 */
export function TestSectionGroup(props: Readonly<Props>): React.ReactElement {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [foldState, setFoldState] = React.useState(
    initialFoldState(!props.defaultClose)
  );
  const isOpen = isUnfolded(foldState);

  const sectionName = props.node.path[props.node.path.length - 1] ?? "";
  const sectionPath = props.node.path.join("/");
  const groupHref = `/group/${sectionPath}`;
  const moduleIds = sectionModuleIds(props.node);
  const status = aggregateStatus(sectionStatuses(props.node));
  const isSectionRunning = isRunInFlight(status);
  const runStatus = toDisplayStatus(props.commonTestRunStatus);

  const isRunDisabled =
    !props.onRunSection ||
    isRunInFlight(runStatus) ||
    Boolean(props.manualCollectMode) ||
    moduleIds.length === 0;

  // A folded section hides the tests it runs, including the row of the case the
  // operator has to act on, so it unfolds itself while it runs and folds back
  // once done. A manual fold during the run wins until the section goes idle.
  React.useEffect(() => {
    setFoldState((current) =>
      nextFoldState(current, isSectionRunning ? "needs-attention" : "idle")
    );
  }, [isSectionRunning]);

  const handleRun = (event: React.MouseEvent): void => {
    event.stopPropagation();
    if (isRunDisabled || !props.onRunSection) {
      return;
    }
    navigate(groupHref);
    props.onRunSection(moduleIds, sectionPath);
  };

  return (
    <Collapsible
      open={isOpen}
      onOpenChange={(open) => setFoldState(operatorFoldState(open))}
      className="test-section"
      data-section={sectionPath}
    >
      <div className={treeRowClassName}>
        <CollapsibleTrigger asChild>
          <button
            type="button"
            className="inline-flex size-6 shrink-0 items-center justify-center rounded-sm text-muted-foreground hover:bg-muted"
            aria-label={isOpen ? "Collapse" : "Expand"}
          >
            {isOpen ? (
              <ChevronDown className={treeIconClassName} />
            ) : (
              <ChevronRight className={treeIconClassName} />
            )}
          </button>
        </CollapsibleTrigger>
        <Folder className={treeIconClassName} />
        <TestStatus status={status} />
        <Link
          to={groupHref}
          className={`${treeLabelClassName} hover:underline`}
          aria-label={t("section.open", { name: sectionName })}
        >
          {sectionName}
        </Link>
        <span className={treeMetaClassName}>
          {t("section.moduleCount", { count: moduleIds.length })}
        </span>
        <Button
          type="button"
          size="sm"
          variant="ghost"
          disabled={isRunDisabled}
          data-testid={`section-run-${sectionPath}`}
          aria-label={t("section.runAria", { name: sectionName })}
          onClick={handleRun}
        >
          <Play className="size-3.5" />
          {t("section.run")}
        </Button>
      </div>
      <CollapsibleContent>
        <div className={treeChildrenClassName}>
          <SectionContents
            node={props.node}
            startIndex={props.startIndex}
            defaultClose={props.defaultClose}
            commonTestRunStatus={props.commonTestRunStatus}
            onTestsSelectionChange={props.onTestsSelectionChange}
            selectedTests={props.selectedTests}
            selectionSupported={props.selectionSupported}
            measurementDisplay={props.measurementDisplay}
            manualCollectMode={props.manualCollectMode}
            autoScroll={props.autoScroll}
            onRunSection={props.onRunSection}
            onRunModule={props.onRunModule}
          />
        </div>
      </CollapsibleContent>
    </Collapsible>
  );
}

export default TestSectionGroup;
