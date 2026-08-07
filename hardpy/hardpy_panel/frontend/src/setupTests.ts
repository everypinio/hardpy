// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

// Registers the jest-dom matchers on vitest's expect, so tests can assert with
// expect(element).toHaveTextContent(/react/i) and friends.
import "@testing-library/jest-dom/vitest";
