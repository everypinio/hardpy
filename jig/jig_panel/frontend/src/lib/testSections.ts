// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import type { Dictionary } from "lodash";

import type { TestItem } from "@/jig_test_view/TestSuite";

/** Section name used for modules that have no directory or marker section. */
export const DEFAULT_SECTION_NAME = "Default";

/** A module entry inside a section tree node. */
export interface SectionModule {
  id: string;
  test: TestItem;
}

/**
 * A node in the recursive section tree.
 * The root node has `path: []` and only holds child sections; ungrouped
 * modules are placed under {@link DEFAULT_SECTION_NAME}.
 */
export interface SectionNode {
  path: string[];
  modules: SectionModule[];
  children: SectionNode[];
}

/**
 * Builds a recursive section tree from a flat modules dictionary.
 *
 * Modules with an empty section path stay flat on the root when the run has
 * no named sections. When named sections exist, those ungrouped modules are
 * placed under {@link DEFAULT_SECTION_NAME} (always first among top-level
 * sections) so they are not flattened beside group headers.
 *
 * Named section order otherwise follows first appearance in the document
 * (object key order), which already reflects the backend's collection order.
 *
 * @param {Dictionary<TestItem>} modules - Modules keyed by module id.
 * @returns {SectionNode} The root node (path `[]`).
 */
export function buildSectionTree(modules: Dictionary<TestItem>): SectionNode {
  const root: SectionNode = { path: [], modules: [], children: [] };
  const ungrouped: SectionModule[] = [];

  for (const [id, test] of Object.entries(modules)) {
    const section = test.section ?? [];
    if (section.length === 0) {
      ungrouped.push({ id, test });
      continue;
    }
    ensurePath(root, section).modules.push({ id, test });
  }

  if (ungrouped.length === 0) {
    return root;
  }

  if (root.children.length === 0) {
    root.modules = ungrouped;
    return root;
  }

  const defaultNode = ensurePath(root, [DEFAULT_SECTION_NAME]);
  defaultNode.modules.push(...ungrouped);
  moveDefaultSectionFirst(root);
  return root;
}

/**
 * Moves the top-level Default section to the front of the root children.
 */
function moveDefaultSectionFirst(root: SectionNode): void {
  const defaultIndex = root.children.findIndex(
    (child) =>
      child.path.length === 1 && child.path[0] === DEFAULT_SECTION_NAME
  );
  if (defaultIndex <= 0) {
    return;
  }
  const [defaultNode] = root.children.splice(defaultIndex, 1);
  root.children.unshift(defaultNode);
}

/**
 * Collects every module id under a section node, recursively.
 * @param {SectionNode} node - The section to flatten.
 * @returns {string[]} Module ids in document order (depth-first).
 */
export function sectionModuleIds(node: SectionNode): string[] {
  const ids = node.modules.map((module) => module.id);
  for (const child of node.children) {
    ids.push(...sectionModuleIds(child));
  }
  return ids;
}

/**
 * Collects every module status under a section node, recursively.
 * @param {SectionNode} node - The section to flatten.
 * @returns {string[]} Raw status strings in document order.
 */
export function sectionStatuses(node: SectionNode): string[] {
  const statuses = node.modules.map((module) => module.test.status);
  for (const child of node.children) {
    statuses.push(...sectionStatuses(child));
  }
  return statuses;
}

/**
 * Finds a section node by its path relative to the root.
 * @param {SectionNode} root - The root section tree node.
 * @param {string[]} path - Ordered section path segments.
 * @returns {SectionNode | undefined} The matching node, or undefined if missing.
 */
export function findSection(
  root: SectionNode,
  path: string[]
): SectionNode | undefined {
  if (path.length === 0) {
    return root;
  }

  let current: SectionNode | undefined = root;
  for (const segment of path) {
    current = current.children.find(
      (child) => child.path[child.path.length - 1] === segment
    );
    if (!current) {
      return undefined;
    }
  }
  return current;
}

function ensurePath(root: SectionNode, path: string[]): SectionNode {
  let current = root;
  for (let depth = 0; depth < path.length; depth += 1) {
    const targetPath = path.slice(0, depth + 1);
    const name = path[depth];
    let child = current.children.find(
      (candidate) => candidate.path[candidate.path.length - 1] === name
    );
    if (!child) {
      child = { path: targetPath, modules: [], children: [] };
      current.children.push(child);
    }
    current = child;
  }
  return current;
}
