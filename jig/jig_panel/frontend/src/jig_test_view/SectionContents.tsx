// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";

import { sectionModuleIds, type SectionNode } from "@/lib/testSections";
import { TestSectionGroup } from "./TestSectionGroup";
import { TestSuiteComponent } from "./TestSuite";

export interface SectionContentsProps {
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
  onRunSection?: (moduleIds: string[]) => void;
  onRunModule?: (moduleId: string) => void;
  /** When true, root modules open by default only if fewer than 5 modules exist. */
  openRootModulesWhenFew?: boolean;
}

/**
 * Renders a section node's modules followed by its child sections, keeping
 * continuous module numbering across the tree.
 */
export function SectionContents(
  props: Readonly<SectionContentsProps>
): React.ReactElement {
  const totalModules = sectionModuleIds(props.node).length;
  let nextIndex = props.startIndex;

  const moduleElements = props.node.modules.map((module) => {
    const index = nextIndex;
    nextIndex += 1;
    const defaultOpen = props.openRootModulesWhenFew
      ? totalModules < 5 && !props.defaultClose
      : !props.defaultClose;
    return (
      <TestSuiteComponent
        key={module.id}
        index={index}
        test={module.test}
        defaultOpen={defaultOpen}
        commonTestRunStatus={props.commonTestRunStatus}
        moduleTechName={module.id}
        onTestsSelectionChange={props.onTestsSelectionChange}
        selectedTests={props.selectedTests}
        selectionSupported={props.selectionSupported}
        measurementDisplay={props.measurementDisplay}
        manualCollectMode={props.manualCollectMode}
        autoScroll={props.autoScroll}
        onRunModule={props.onRunModule}
      />
    );
  });

  const childElements = props.node.children.map((child) => {
    const childStart = nextIndex;
    nextIndex += sectionModuleIds(child).length;
    return (
      <TestSectionGroup
        key={child.path.join("/")}
        node={child}
        startIndex={childStart}
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
    );
  });

  return <>{[...moduleElements, ...childElements]}</>;
}
