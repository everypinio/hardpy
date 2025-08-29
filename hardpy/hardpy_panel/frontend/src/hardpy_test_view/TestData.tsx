// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { Tag } from "@blueprintjs/core";
import Plot from "react-plotly.js";
import { Dialog, Button, Classes } from "@blueprintjs/core";
import GraphComponent from "./GraphComponent";

import _ from "lodash";

interface Props {
  msg: string[] | null;
  assertion_msg: string | null;
}

interface GraphData {
  x_data: number[];
  y_data: number[];
  marker_name: string;
}

const TAG_ELEMENT_STYLE = { margin: 2 };

const graphData: GraphData[] = [
  {
    x_data: [1, 2, 3],
    y_data: [1, 2, 3],
    marker_name: "a",
  },
  {
    x_data: [1, 2, 4],
    y_data: [5, 4, 3],
    marker_name: "b",
  },
];

/**
 * Renders a list of messages and an assertion message as styled tags.
 *
 * @component
 * @param {Object} props - The component props.
 * @param {string[] | null} props.msg - An array of messages to display as primary tags.
 * @param {string | null} props.assertion_msg - An assertion message to display as a warning tag.
 * @returns {React.ReactElement} A React element representing the component.
 */
export function TestData(props: Readonly<Props>): React.ReactElement {
  const [isModalOpen, setIsModalOpen] = React.useState(false);
  const [isGraphCollapsed, setIsGraphCollapsed] = React.useState(false);

  const plotData = graphData.map((graph, index) => ({
    x: graph.x_data,
    y: graph.y_data,
    type: "scatter",
    mode: "lines+markers",
    name: graph.marker_name,
    marker: { color: `hsl(${(index * 360) / graphData.length}, 70%, 50%)` },
  }));

  const layout = {
    width: 400,
    height: 300,
    title: "Test Data Graph",
    showlegend: true,
  };

  const fullScreenLayout = {
    width: window.innerWidth * 0.9,
    height: window.innerHeight * 0.9,
    title: "Test Data Graph",
    showlegend: true,
  };

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
      <GraphComponent
        graphs={graphData}
        isCollapsed={isGraphCollapsed}
        onToggleCollapse={() => setIsGraphCollapsed(!isGraphCollapsed)}
      />
      <div
        style={{ marginTop: "10px", cursor: "pointer" }}
        onClick={() => setIsModalOpen(true)}
      ></div>

      <Dialog
        isOpen={isModalOpen}
        title="Modal Title"
        onClose={() => console.log("Modal closed")}
      >
        <div className={Classes.DIALOG_BODY}>
          <Plot
            data={plotData}
            layout={fullScreenLayout}
            config={{
              displayModeBar: true,
              displaylogo: false,
              modeBarButtonsToAdd: ["toggleHover", "resetScale2d"],
              modeBarButtonsToRemove: [
                "pan2d",
                "select2d",
                "lasso2d",
                "autoScale2d",
              ],
            }}
          />
        </div>
        <div className={Classes.DIALOG_FOOTER}>
          <Button onClick={() => setIsModalOpen(false)}>Close</Button>
        </div>
      </Dialog>
    </div>
  );
}

export default TestData;
