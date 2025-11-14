/**
 * Checks if any dialog is currently open.
 * @returns {boolean} True if a dialog is open, else false.
 */
export function isDialogOpen(): boolean {
  const blueprintDialogs = document.querySelectorAll(".bp3-dialog");
  for (const dialog of blueprintDialogs) {
    const style = window.getComputedStyle(dialog);
    if (style.display !== "none" && style.visibility !== "hidden") {
      return true;
    }
  }

  const ariaDialogs = document.querySelectorAll('[role="dialog"]');
  for (const dialog of ariaDialogs) {
    const style = window.getComputedStyle(dialog);
    if (style.display !== "none" && style.visibility !== "hidden") {
      return true;
    }
  }

  return false;
}
