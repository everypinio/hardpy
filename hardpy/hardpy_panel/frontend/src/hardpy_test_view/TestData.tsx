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
  chart?: ChartData;
}

interface ChartData {
  type: string;
  title?: string;
  x_label?: string;
  y_label?: string;
  marker_name: string[];
  x_data: number[][];
  y_data: number[][];
}

interface GraphData {
  x_data: number[];
  y_data: number[];
  marker_name: string;
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

  const graphData: GraphData[] = React.useMemo(() => {
    if (!props.chart) return [];

    if (
      !props.chart.marker_name ||
      !props.chart.x_data ||
      !props.chart.y_data
    ) {
      return [];
    }

    const seriesCount = props.chart.marker_name.length;
    if (
      props.chart.x_data.length !== seriesCount ||
      props.chart.y_data.length !== seriesCount
    ) {
      console.error("Chart data arrays have different lengths");
      return [];
    }

    return props.chart.marker_name.map((name, index) => ({
      x_data: props.chart!.x_data[index] || [],
      y_data: props.chart!.y_data[index] || [],
      marker_name: name || `Series ${index + 1}`,
    }));
  }, [props.chart]);

  const hasGraphData = graphData.length > 0;

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
    title: props.chart?.title || "Test Data Graph",
    xaxis: {
      title: props.chart?.x_label || undefined,
    },
    yaxis: {
      title: props.chart?.y_label || undefined,
    },
    showlegend: true,
    autosize: true,
  };

  return (
    <div className="test-data" style={{ width: "100%" }}>
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

      {hasGraphData && (
        <>
          <div style={{ width: "100%", marginTop: "10px", minWidth: "300px" }}>
            <GraphComponent
              graphs={graphData}
              isCollapsed={isGraphCollapsed}
              onToggleCollapse={handleToggleCollapse}
              title={props.chart?.title}
              xLabel={props.chart?.x_label}
              yLabel={props.chart?.y_label}
              chartType={props.chart?.type}
            />
          </div>

          <div
            style={{ marginTop: "10px", cursor: "pointer" }}
            onClick={() => setIsModalOpen(true)}
          ></div>

          <Dialog
            isOpen={isModalOpen}
            title={props.chart?.title || "Graph"}
            onClose={() => setIsModalOpen(false)}
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
        </>
      )}
    </div>
  );
}

export default TestData;
