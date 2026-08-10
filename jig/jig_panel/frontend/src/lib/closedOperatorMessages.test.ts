// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import { afterEach, describe, expect, test } from "vitest";

import {
  CLOSED_MESSAGES_KEY,
  clearClosedMessages,
  getClosedMessages,
  markMessageAsClosed,
} from "./closedOperatorMessages";

afterEach(() => {
  localStorage.clear();
});

describe("closedOperatorMessages", () => {
  test(`given no message seen yet,
 when the seen ids are read,
 then the set is empty`, () => {
    expect(getClosedMessages().size).toBe(0);
  });

  test(`given a message the operator has seen,
 when another message is marked,
 then both ids are kept`, () => {
    markMessageAsClosed("msg-1");
    markMessageAsClosed("msg-2");

    expect(Array.from(getClosedMessages())).toEqual(["msg-1", "msg-2"]);
  });

  test(`given the same message marked twice,
 when the seen ids are read,
 then the id is stored once`, () => {
    markMessageAsClosed("msg-1");
    markMessageAsClosed("msg-1");

    expect(Array.from(getClosedMessages())).toEqual(["msg-1"]);
  });

  test(`given seen messages of a finished run,
 when they are cleared,
 then nothing is remembered`, () => {
    markMessageAsClosed("msg-1");

    clearClosedMessages();

    expect(getClosedMessages().size).toBe(0);
    expect(localStorage.getItem(CLOSED_MESSAGES_KEY)).toBeNull();
  });

  test(`given corrupted storage content,
 when the seen ids are read,
 then the set is empty instead of throwing`, () => {
    localStorage.setItem(CLOSED_MESSAGES_KEY, "not json");

    expect(getClosedMessages().size).toBe(0);
  });
});
