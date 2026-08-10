// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import { describe, expect, test } from "vitest";

import {
  initialFoldState,
  isUnfolded,
  nextFoldState,
  operatorFoldState,
  resetFoldState,
} from "./foldState";

describe("foldState", () => {
  test(`given a node open by default,
 when its initial fold state is built,
 then it is unfolded and held so no run folds it back`, () => {
    const state = initialFoldState(true);

    expect(isUnfolded(state)).toBe(true);
    expect(nextFoldState(state, "idle")).toBe(state);
  });

  test(`given a folded node,
 when its content needs the operator's attention,
 then the run unfolds it`, () => {
    expect(nextFoldState("folded", "needs-attention")).toBe("unfolded-by-run");
  });

  test(`given a node unfolded by the run,
 when its content goes idle,
 then the run folds it back`, () => {
    expect(nextFoldState("unfolded-by-run", "idle")).toBe("folded");
  });

  test(`given a node unfolded by the run,
 when it sits between two cases,
 then it stays unfolded`, () => {
    expect(nextFoldState("unfolded-by-run", "between-cases")).toBe(
      "unfolded-by-run"
    );
  });

  test(`given a node the operator folded,
 when its content still needs attention,
 then it stays folded`, () => {
    const state = operatorFoldState(false);

    expect(nextFoldState(state, "needs-attention")).toBe(state);
    expect(isUnfolded(state)).toBe(false);
  });

  test(`given a node the operator folded while it was running,
 when it goes idle,
 then the hold expires so the next run unfolds it again`, () => {
    const folded = nextFoldState(operatorFoldState(false), "idle");

    expect(nextFoldState(folded, "needs-attention")).toBe("unfolded-by-run");
  });

  test(`given a node the operator unfolded,
 when its content goes idle,
 then it stays unfolded`, () => {
    const state = operatorFoldState(true);

    expect(nextFoldState(state, "idle")).toBe(state);
    expect(isUnfolded(state)).toBe(true);
  });

  test(`given a node the operator folded during a run,
 when a new run resets it,
 then the run may unfold it again`, () => {
    const state = resetFoldState();

    expect(isUnfolded(state)).toBe(false);
    expect(nextFoldState(state, "needs-attention")).toBe("unfolded-by-run");
  });
});
