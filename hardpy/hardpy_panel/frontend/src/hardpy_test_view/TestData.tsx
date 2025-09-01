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
  testSuiteIndex: number;
  testCaseIndex: number;
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

export function TestData(props: Readonly<Props>): React.ReactElement {
  const [isModalOpen, setIsModalOpen] = React.useState(false);
  const storageKey = `graphState_${props.testSuiteIndex}_${props.testCaseIndex}`;

  const [isGraphCollapsed, setIsGraphCollapsed] = React.useState(() => {
    const savedState = localStorage.getItem(storageKey);
    if (savedState) {
      try {
        const { isCollapsed } = JSON.parse(savedState);
        return isCollapsed || false;
      } catch (e) {
        return false;
      }
    }
    return false;
  });

  React.useEffect(() => {
    localStorage.setItem(
      storageKey,
      JSON.stringify({
        isCollapsed: isGraphCollapsed,
      })
    );
  }, [isGraphCollapsed, storageKey]);

  const handleToggleCollapse = () => {
    setIsGraphCollapsed(!isGraphCollapsed);
  };

  const plotData = graphData.map((graph, index) => ({
    x: graph.x_data,
    y: graph.y_data,
    type: "scatter",
    mode: "lines+markers",
    name: graph.marker_name,
    marker: { color: `hsl(${(index * 360) / graphData.length}, 70%, 50%)` },
  }));

  const fullScreenLayout = {
    width: window.innerWidth * 0.9,
    height: window.innerHeight * 0.9,
    title: "Test Data Graph",
    showlegend: true,
    autosize: true,
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
        onToggleCollapse={handleToggleCollapse}
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
              responsive: true,
              modeBarButtonsToAdd: ["toggleHover", "resetScale2d"],
              modeBarButtonsToRemove: [
                "pan2d",
                "select2d",
                "lasso2d",
                "autoScale2d",
              ],
            }}
            style={{ width: "100%", height: "100%" }}
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
