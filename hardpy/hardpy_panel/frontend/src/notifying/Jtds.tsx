// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import Ajv, { AnySchema, JTDSchemaType } from "ajv/dist/jtd";
const ajv = new Ajv();

/**
 * Represents a common notification object.
 */
interface NotificationCommon {
  message: string;
  level: "INFO" | "WARN" | "ERROR" | "CRITICAL" | "DEBUG";
  source: string;
  error?: number;
  additional_info?: string;
}

/**
 * Represents a notification object for test results.
 */
interface NotificationTestResult {
  status: "PASS" | "FAIL" | "SKIP";
  case_number?: number;
  case_name?: string;
  suite_number?: number;
  suite_name?: string;
}

/**
 * Schema for validating NotificationCommon objects.
 */
const schemaNotificationCommon: JTDSchemaType<NotificationCommon> = {
  properties: {
    message: { type: "string" },
    level: { enum: ["INFO", "WARN", "ERROR", "CRITICAL", "DEBUG"] },
    source: { type: "string" },
  },
  optionalProperties: {
    error: { type: "int32" },
    additional_info: { type: "string" },
  },
};

/**
 * Schema for validating NotificationTestResult objects.
 */
const schemaNotificationTestResult: JTDSchemaType<NotificationTestResult> = {
  properties: {
    status: { enum: ["PASS", "FAIL", "SKIP"] },
  },
  optionalProperties: {
    case_number: { type: "int32" },
    case_name: { type: "string" },
    suite_number: { type: "int32" },
    suite_name: { type: "string" },
  },
};

/**
 * Validates data against a given schema.
 *
 * @param {unknown} data - The data to validate.
 * @param {AnySchema} schema - The schema to validate the data against.
 * @returns {boolean | Promise<unknown>} - Returns `true` if the data is valid according to the schema, otherwise `false` or a promise that resolves to the validation result.
 *
 * @example
 * const data = { message: "Test", level: "INFO", source: "Test Source" };
 * const isValid = is_valid(data, schemaNotificationCommon);
 * console.log(isValid); // true or false
 */
function is_valid(
  data: unknown,
  schema: AnySchema
): boolean | Promise<unknown> {
  const validate = ajv.compile(schema);
  const valid = validate(data);
  return valid;
}

export { is_valid };
export { schemaNotificationCommon };
export { schemaNotificationTestResult };
export type { NotificationTestResult };
