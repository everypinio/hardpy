// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { Tag } from "@blueprintjs/core";

import _ from "lodash";

interface Measurement {
  name?: string;
  result?: boolean;
  type: string;
  value: number | string;
  unit?: string;
  comparison_value?: number | string;
  operation?: string;
  lower_limit?: number;
  upper_limit?: number;
}

interface Props {
  msg: string[] | null;
  assertion_msg: string | null;
  measurements?: Measurement[];
}

const TAG_ELEMENT_STYLE = { margin: 2 };

/**
 * Renders a list of messages, measurements, and an assertion message as styled tags.
 * 
 * @component
 * @param {Object} props - The component props.
 * @param {string[] | null} props.msg - An array of messages to display as primary tags.
 * @param {string | null} props.assertion_msg - An assertion message to display as a warning tag.
 * @param {Measurement[] | undefined} props.measurements - An array of measurements to display as success/danger tags based on results.
 * @returns {React.ReactElement} A React element representing the component.
 */
export function TestData(props: Readonly<Props>): React.ReactElement {
  const formatMeasurement = (measurement: Measurement, index: number): string => {
    const measurementText = measurement.name || `D ${index + 1}`;
    let display = `${measurementText}: ${measurement.value}`;
    
    // Add unit if it exists
    if (measurement.unit) {
      display += `${measurement.unit}`;
    }
    
    // Add limits if they exist
    const hasLowerLimit = measurement.lower_limit !== undefined && measurement.lower_limit !== null;
    const hasUpperLimit = measurement.upper_limit !== undefined && measurement.upper_limit !== null;
    
    if (hasLowerLimit || hasUpperLimit) {
      display += '   [';
      if (hasLowerLimit && hasUpperLimit) {
        display += `${measurement.lower_limit} : ${measurement.upper_limit}`;
      } else if (hasLowerLimit) {
        display += `${measurement.lower_limit} :`;
      } else if (hasUpperLimit) {
        display += `: ${measurement.upper_limit}`;
      }
      if (measurement.unit) {
        display += ` ${measurement.unit}`;
      }
      display += ']';
    }

    if (measurement.operation && measurement.comparison_value !== undefined && measurement.comparison_value !== null) {
      display += ` [${measurement.operation} ${measurement.comparison_value}]`;
    }

    return display;
  };

  return (
    <div 
      className="test-data" 
      style={{ 
        display: "flex", 
        flexDirection: "column", 
        alignItems: "flex-start",
        gap: "2px"
      }}
    >
      {/* Render measurements first */}
      {_.map(props.measurements, (measurement: Measurement, index: number) => {
        const intent = measurement.result === true ? "success" : measurement.result === false ? "danger" : "none";
        
        return (
          <Tag
            key={`measurement-${index}`}
            style={TAG_ELEMENT_STYLE}
            minimal={true}
            intent={intent}
          >
            {formatMeasurement(measurement, index)}
          </Tag>
        );
      })}
      
      {/* Render messages */}
      {_.map(props.msg, (value: string, key: string) => {
        return (
          value && (
            <Tag
              key={key}
              style={TAG_ELEMENT_STYLE}
              minimal={true}
              intent="primary"
            >
              {value}
            </Tag>
          )
        );
      })}
      
      {/* Render assertions last */}
      {props.assertion_msg && (
        <Tag
          key={"assertion"}
          style={TAG_ELEMENT_STYLE}
          minimal={true}
          intent="warning"
        >
          {props.assertion_msg.split("\n")[0]}
        </Tag>
      )}
    </div>
  );
}

export default TestData;
