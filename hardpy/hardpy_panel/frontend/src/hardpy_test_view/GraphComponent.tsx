// Copyright (c) 2025 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt  )

import React, { useState, useRef, useEffect } from "react";
import { Dialog, Button } from "@blueprintjs/core";
import Plot from "react-plotly.js";

interface GraphData {
  x_data: number[];
  y_data: number[];
  marker_name: string;
}

interface GraphComponentProps {
  graphs: GraphData[];
  isCollapsed?: boolean;
  onToggleCollapse?: () => void;
  title?: string;
  xLabel?: string;
  yLabel?: string;
  chartType?: string;
  containerWidth?: number;
}

const GraphComponent: React.FC<GraphComponentProps> = ({
  graphs,
  isCollapsed = false,
  onToggleCollapse,
  title,
  xLabel,
  yLabel,
  chartType = "line",
  containerWidth,
}) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

  useEffect(() => {
    const updateDimensions = () => {
      let width = 0;

      if (containerWidth && containerWidth > 0) {
        width = containerWidth - 600;
      } else if (containerRef.current) {
        width = containerRef.current.offsetWidth - 400;
      }

      const finalWidth = Math.max(250, width);
      const finalHeight = Math.max(300, finalWidth * 0.5);

      setDimensions({ width: finalWidth, height: finalHeight });
    };

    updateDimensions();
    window.addEventListener("resize", updateDimensions);

    return () => window.removeEventListener("resize", updateDimensions);
  }, [containerWidth]);

  const getAxisType = (axis: "x" | "y") => {
    switch (chartType) {
      case "line_log_x":
        return axis === "x" ? "log" : "linear";
      case "line_log_y":
        return axis === "y" ? "log" : "linear";
      case "log_x_y":
        return "log";
      default:
        return "linear";
    }
  };

  const plotData = graphs.map((graph, index) => ({
    x: graph.x_data,
    y: graph.y_data,
    type: "scatter" as const,
    mode: "lines+markers",
    name: graph.marker_name,
    marker: { color: `hsl(${(index * 360) / graphs.length}, 70%, 50%)` },
  }));

  const layout = {
    width: dimensions.width,
    height: 300,
    title: title || "Test Data Graph",
    xaxis: {
      title: xLabel || undefined,
      type: getAxisType("x"),
    },
    yaxis: {
      title: yLabel || undefined,
      type: getAxisType("y"),
    },
    showlegend: true,
    autosize: true,
    margin: {
      l: 60,
      r: 30,
      b: 60,
      t: 60,
      pad: 4,
    },
  };

  const fullScreenLayout = {
    width: window.innerWidth * 0.9,
    height: window.innerHeight * 0.9,
    title: title || "Test Data Graph",
    xaxis: {
      title: xLabel || undefined,
      type: getAxisType("x"),
    },
    yaxis: {
      title: yLabel || undefined,
      type: getAxisType("y"),
    },
    showlegend: true,
    autosize: true,
  };

  if (isCollapsed) {
    return (
      <div
        style={{
          border: "1px solid #ccc",
          padding: "10px",
          borderRadius: "3px",
          background: "#f5f5f5",
          width: "100%",
          minWidth: "300px",
        }}
      >
        <Button icon="chevron-down" onClick={onToggleCollapse} minimal small>
          Show graph
        </Button>
      </div>
    );
  }

  return (
    <>
      <div
        ref={containerRef}
        style={{
          position: "relative",
          border: "1px solid #ccc",
          padding: "10px",
          borderRadius: "3px",
          width: "100%",
          minWidth: "600px",
          minHeight: "300px",
          overflow: "hidden",
          boxSizing: "border-box",
        }}
      >
        <div
          style={{
            position: "absolute",
            top: "10px",
            right: "10px",
            zIndex: 100,
          }}
        >
          <Button
            icon="fullscreen"
            onClick={() => setIsModalOpen(true)}
            minimal
            small
            style={{ marginRight: "5px" }}
          />
          <Button icon="chevron-up" onClick={onToggleCollapse} minimal small />
        </div>
        <div style={{ width: "100%", height: "100%" }}>
          <Plot
            data={plotData}
            layout={layout}
            config={{
              displayModeBar: false,
              displaylogo: false,
              responsive: true,
            }}
            style={{ width: "100%", height: "100%" }}
          />
        </div>
      </div>

      <Dialog
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={title || "Graph View"}
        className="graph-modal"
        style={{ width: "90vw", height: "90vh" }}
      >
        <div className="bp4-dialog-body" style={{ height: "100%" }}>
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
      </Dialog>
    </>
  );
};

export default GraphComponent;
