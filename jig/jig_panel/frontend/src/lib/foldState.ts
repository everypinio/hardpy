// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

/**
 * Whether a node of the tests tree is unfolded, and who decided it.
 *
 * A run unfolds the node holding what the operator has to watch and folds it
 * back once that node is done, but it only moves nodes it owns: as soon as the
 * operator folds or unfolds a node by hand, that choice holds. A hold on a
 * folded node expires once the node goes idle, so the next run may unfold it
 * again; a hold on an unfolded node never expires, since the operator is
 * reading it.
 */
export type FoldState =
  | "folded"
  | "unfolded-by-run"
  | "held-folded"
  | "held-unfolded";

/**
 * How much of the operator's attention the content of a node needs.
 *
 * "between-cases" is the gap between one case finishing and the next starting:
 * the node is neither worth unfolding nor done, so its fold state must not move.
 */
export type NodeActivity = "needs-attention" | "between-cases" | "idle";

/**
 * Tells whether the node shows its content.
 * @param {FoldState} state - The fold state of the node.
 * @returns {boolean} True when the node is unfolded.
 */
export function isUnfolded(state: FoldState): boolean {
  return state === "unfolded-by-run" || state === "held-unfolded";
}

/**
 * Fold state a node starts with, before any run touches it.
 * @param {boolean} isOpenByDefault - Whether the node shows its content at first.
 * @returns {FoldState} A held state when open, so a run never folds it back.
 */
export function initialFoldState(isOpenByDefault: boolean): FoldState {
  return isOpenByDefault ? "held-unfolded" : "folded";
}

/**
 * Fold state resulting from the operator folding or unfolding a node.
 * @param {boolean} isOpen - Whether the operator asked for the content.
 * @returns {FoldState} The matching held state, which no run may override.
 */
export function operatorFoldState(isOpen: boolean): FoldState {
  return isOpen ? "held-unfolded" : "held-folded";
}

/**
 * Fold state a node returns to when a new run starts, dropping whatever the
 * operator or the previous run decided.
 * @returns {FoldState} The neutral folded state.
 */
export function resetFoldState(): FoldState {
  return "folded";
}

/**
 * Advances the fold state of a node after its content changed.
 * @param {FoldState} state - The current fold state.
 * @param {NodeActivity} activity - What the run is doing inside the node.
 * @returns {FoldState} The next fold state, unchanged when the run owns nothing.
 */
export function nextFoldState(
  state: FoldState,
  activity: NodeActivity
): FoldState {
  if (activity === "needs-attention" && state === "folded") {
    return "unfolded-by-run";
  }
  if (
    activity === "idle" &&
    (state === "unfolded-by-run" || state === "held-folded")
  ) {
    return "folded";
  }
  return state;
}
