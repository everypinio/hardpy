// Copyright (c) 2025 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt  )

import React, { useState, useRef, useEffect } from "react";
import { Dialog, Button, Classes } from "@blueprintjs/core";
import Plot from "react-plotly.js";
import { withTranslation, WithTranslation } from "react-i18next";

interface GraphData {
  x_data: number[];
  y_data: number[];
  marker_name: string;
  x_label?: string;
  y_label?: string;
  graph_title?: string;
}

interface GraphComponentProps extends WithTranslation {
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
  t,
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

  const markerSymbols = [
    "circle",
    "square",
    "diamond",
    "cross",
    "x",
    "triangle-up",
    "triangle-down",
    "triangle-left",
    "triangle-right",
    "pentagon",
    "hexagon",
    "hexagon2",
    "octagon",
    "star",
    "hexagram",
    "star-triangle-up",
    "star-triangle-down",
    "star-square",
    "star-diamond",
    "diamond-tall",
  ];

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

  const graphTitle =
    title ||
    (graphs.length > 0 && graphs[0].graph_title) ||
    t("graph.testDataGraph");

  const xAxisLabel =
    xLabel || (graphs.length > 0 && graphs[0].x_label) || t("graph.xAxis");
  const yAxisLabel =
    yLabel || (graphs.length > 0 && graphs[0].y_label) || t("graph.yAxis");

  const plotData = graphs.map((graph, index) => ({
    x: graph.x_data,
    y: graph.y_data,
    type: "scatter" as const,
    mode: "lines+markers",
    name: graph.marker_name,
    marker: {
      color: `hsl(${(index * 360) / graphs.length}, 70%, 50%)`,
      symbol: markerSymbols[index % markerSymbols.length],
      size: 8,
      line: {
        width: 1,
        color: `hsl(${(index * 360) / graphs.length}, 70%, 30%)`,
      },
    },
    line: {
      width: 2,
    },
  }));

  const layout = {
    width: dimensions.width,
    height: 300,
    title: {
      text: graphTitle,
      x: 0.5,
      xanchor: "center",
      font: {
        size: 16,
        weight: "bold",
      },
    },
    xaxis: {
      title: {
        text: xAxisLabel,
        font: {
          size: 12,
          weight: "bold",
        },
      },
      type: getAxisType("x"),
      showgrid: true,
      gridcolor: "#eee",
      zeroline: false,
    },
    yaxis: {
      title: {
        text: yAxisLabel,
        font: {
          size: 12,
          weight: "bold",
        },
      },
      type: getAxisType("y"),
      showgrid: true,
      gridcolor: "#eee",
      zeroline: false,
    },
    showlegend: true,
    legend: {
      x: 1,
      y: 1,
      xanchor: "right",
      yanchor: "top",
      bgcolor: "rgba(255, 255, 255, 0.8)",
      bordercolor: "#ccc",
      borderwidth: 1,
    },
    autosize: true,
    margin: {
      l: 60,
      r: 30,
      b: 60,
      t: 60,
      pad: 4,
    },
    hovermode: "closest",
    plot_bgcolor: "#f9f9f9",
    paper_bgcolor: "#fff",
  };

  const fullScreenLayout = {
    ...layout,
    width: window.innerWidth * 0.9,
    height: window.innerHeight * 0.9,
    title: {
      ...layout.title,
      font: {
        size: 20,
      },
    },
    xaxis: {
      ...layout.xaxis,
      title: {
        ...layout.xaxis.title,
        font: {
          size: 14,
        },
      },
    },
    yaxis: {
      ...layout.yaxis,
      title: {
        ...layout.yaxis.title,
        font: {
          size: 14,
        },
      },
    },
  };

  if (isCollapsed) {
    return (
      <div
        style={{
          border: "1px solid #ccc",
          padding: "10px",
          borderRadius: "3px",
          background: "#f5f5f5",
          display: "inline-block",
          minWidth: "150px",
          maxWidth: "100%",
        }}
      >
        <Button icon="chevron-down" onClick={onToggleCollapse} minimal small>
          {t("graph.showGraph", { title: graphTitle })}
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
          background: "#fff",
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
            title={t("graph.fullscreenButton")}
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
        title={graphTitle}
        className="graph-modal"
        style={{
          width: "90vw",
          height: "90vh",
          padding: "10px",
          boxSizing: "border-box",
        }}
      >
        <div
          className={Classes.DIALOG_BODY}
          style={{
            height: "calc(100% - 50px)",
            padding: "0",
            margin: "0",
          }}
        >
          <Plot
            data={plotData}
            layout={{
              ...fullScreenLayout,
              width: undefined,
              height: undefined,
              autosize: true,
            }}
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
            style={{
              width: "100%",
              height: "100%",
              display: "block",
            }}
            useResizeHandler={true}
          />
        </div>
      </Dialog>
    </>
  );
};

export default withTranslation()(GraphComponent);
