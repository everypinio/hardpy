// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import { describe, expect, test } from "vitest";

import type { TestItem } from "@/jig_test_view/TestSuite";
import {
  DEFAULT_SECTION_NAME,
  buildSectionTree,
  findSection,
  sectionModuleIds,
} from "./testSections";

const moduleStub = (name: string, section: string[] = []): TestItem => ({
  status: "ready",
  name,
  start_time: 0,
  stop_time: 0,
  artifact: {},
  cases: {},
  section,
});

describe("buildSectionTree", () => {
  test(`given only ungrouped modules,
 when the tree is built,
 then they stay flat on the root with no Default section`, () => {
    const tree = buildSectionTree({
      test_1: moduleStub("One"),
      test_2: moduleStub("Two"),
    });

    expect(tree.path).toEqual([]);
    expect(tree.children).toHaveLength(0);
    expect(tree.modules.map((module) => module.id)).toEqual([
      "test_1",
      "test_2",
    ]);
  });

  test(`given modules in one section,
 when the tree is built,
 then a single child section holds them`, () => {
    const tree = buildSectionTree({
      "autofocus/test_1": moduleStub("Coarse", ["autofocus"]),
      "autofocus/test_2": moduleStub("Peak", ["autofocus"]),
    });

    expect(tree.modules).toHaveLength(0);
    expect(tree.children).toHaveLength(1);
    expect(tree.children[0].path).toEqual(["autofocus"]);
    expect(tree.children[0].modules.map((module) => module.id)).toEqual([
      "autofocus/test_1",
      "autofocus/test_2",
    ]);
  });

  test(`given nested sections,
 when the tree is built,
 then children nest recursively`, () => {
    const tree = buildSectionTree({
      "autofocus/test_1": moduleStub("Coarse", ["autofocus"]),
      "autofocus/fine/test_1": moduleStub("Dither", ["autofocus", "fine"]),
    });

    expect(tree.children).toHaveLength(1);
    const autofocus = tree.children[0];
    expect(autofocus.path).toEqual(["autofocus"]);
    expect(autofocus.modules.map((module) => module.id)).toEqual([
      "autofocus/test_1",
    ]);
    expect(autofocus.children).toHaveLength(1);
    expect(autofocus.children[0].path).toEqual(["autofocus", "fine"]);
    expect(autofocus.children[0].modules.map((module) => module.id)).toEqual([
      "autofocus/fine/test_1",
    ]);
  });

  test(`given ungrouped modules mixed with sections,
 when the tree is built,
 then ungrouped modules sit under Default first among top-level sections`, () => {
    const tree = buildSectionTree({
      "autofocus/test_1": moduleStub("Coarse", ["autofocus"]),
      test_1: moduleStub("Root"),
      test_7: moduleStub("Alignment", ["Alignment"]),
    });

    expect(tree.modules).toHaveLength(0);
    expect(tree.children.map((child) => child.path.join("/"))).toEqual([
      DEFAULT_SECTION_NAME,
      "autofocus",
      "Alignment",
    ]);
    expect(tree.children[0].modules.map((module) => module.id)).toEqual([
      "test_1",
    ]);
  });

  test(`given modules arriving in document order,
 when the tree is built,
 then named section order follows first appearance`, () => {
    const tree = buildSectionTree({
      "b/test_1": moduleStub("B", ["b"]),
      "a/test_1": moduleStub("A", ["a"]),
      "b/test_2": moduleStub("B2", ["b"]),
    });

    expect(tree.children.map((child) => child.path[0])).toEqual(["b", "a"]);
    expect(tree.children[0].modules.map((module) => module.id)).toEqual([
      "b/test_1",
      "b/test_2",
    ]);
  });
});

describe("sectionModuleIds", () => {
  test(`given a nested section tree,
 when module ids are collected,
 then every descendant module is included in document order`, () => {
    const tree = buildSectionTree({
      "autofocus/test_1": moduleStub("Coarse", ["autofocus"]),
      "autofocus/fine/test_1": moduleStub("Dither", ["autofocus", "fine"]),
      "autofocus/test_2": moduleStub("Peak", ["autofocus"]),
    });

    expect(sectionModuleIds(tree.children[0])).toEqual([
      "autofocus/test_1",
      "autofocus/test_2",
      "autofocus/fine/test_1",
    ]);
  });
});

describe("findSection", () => {
  const tree = buildSectionTree({
    "autofocus/test_1": moduleStub("Coarse", ["autofocus"]),
    "autofocus/fine/test_1": moduleStub("Dither", ["autofocus", "fine"]),
    "Alignment/test_7": moduleStub("Alignment", ["Alignment"]),
  });

  test(`given an existing top-level section path,
 when findSection is called,
 then that section node is returned`, () => {
    const node = findSection(tree, ["autofocus"]);
    expect(node?.path).toEqual(["autofocus"]);
    expect(node?.modules.map((module) => module.id)).toEqual([
      "autofocus/test_1",
    ]);
  });

  test(`given a nested section path,
 when findSection is called,
 then the nested node is returned`, () => {
    const node = findSection(tree, ["autofocus", "fine"]);
    expect(node?.path).toEqual(["autofocus", "fine"]);
    expect(node?.modules.map((module) => module.id)).toEqual([
      "autofocus/fine/test_1",
    ]);
  });

  test(`given a missing section path,
 when findSection is called,
 then undefined is returned`, () => {
    expect(findSection(tree, ["missing"])).toBeUndefined();
    expect(findSection(tree, ["autofocus", "missing"])).toBeUndefined();
  });
});
