// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { Tag } from "@blueprintjs/core";

import _ from "lodash";

interface Props {
  msg: string[] | null;
  assertion_msg: string | null;
}

const TAG_ELEMENT_STYLE = { margin: 2 };

/**
 * Renders a list of messages and an assertion message as styled tags.
 * 
 * @component
 * @param {Object} props - The component props.
 * @param {string[] | null} props.msg - An array of messages to display as primary tags.
 * @param {string | null} props.assertion_msg - An assertion message to display as a warning tag.
 * @returns {React.ReactElement} A React element representing the component.
 */
export function TestData(props: Props): React.ReactElement {
  return (
    <div className="test-data">
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
