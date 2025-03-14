// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import Ajv, { AnySchema, JTDSchemaType } from "ajv/dist/jtd";
const ajv = new Ajv();

interface NotificationCommon {
  message: string;
  level: "INFO" | "WARN" | "ERROR" | "CRITICAL" | "DEBUG";
  source: string;
  error?: number;
  additional_info?: string;
}

interface NotificationTestResult {
  status: "PASS" | "FAIL" | "SKIP";
  case_number?: number;
  case_name?: string;
  suite_number?: number;
  suite_name?: string;
}

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
 * Checks Data Type
 *
 * Usage:
 *
 * Pass any Data and one of predefined Schema
 *
 * @param data: unknown
 * @param schema: T
 * @returns schema_validator : ValidateFunction
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
