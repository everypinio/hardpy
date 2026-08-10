// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

/**
 * Ids of the operator messages the operator has already seen.
 *
 * A message stays visible on the run document until the test clears it, so the
 * panel must remember what it already showed to avoid reopening a dialog or
 * repeating a notification on every document update and on reload.
 */

export const CLOSED_MESSAGES_KEY = "closed_operator_messages";

/**
 * Reads the ids of the messages already seen. Returns an empty set on error.
 *
 * @returns {Set<string>} Ids of the messages already seen.
 */
export function getClosedMessages(): Set<string> {
  try {
    const stored = localStorage.getItem(CLOSED_MESSAGES_KEY);
    return new Set(stored ? JSON.parse(stored) : []);
  } catch {
    return new Set();
  }
}

/**
 * Records one message id as seen.
 *
 * @param {string} id - Id of the message the operator has seen.
 * @returns {Set<string>} Ids of the messages already seen, including `id`.
 */
export function markMessageAsClosed(id: string): Set<string> {
  const closedMessages = getClosedMessages();
  closedMessages.add(id);
  try {
    localStorage.setItem(
      CLOSED_MESSAGES_KEY,
      JSON.stringify(Array.from(closedMessages))
    );
  } catch (error) {
    console.error("Error saving closed messages to localStorage:", error);
  }
  return closedMessages;
}

/**
 * Forgets every message id, so the messages of a new run are shown again.
 *
 * @returns {void}
 */
export function clearClosedMessages(): void {
  try {
    localStorage.removeItem(CLOSED_MESSAGES_KEY);
  } catch (error) {
    console.error("Error clearing closed messages:", error);
  }
}
