// Copyright (c) 2025 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import React, { useState, useRef, useEffect } from "react";
import { Dialog, Button, Classes } from "@blueprintjs/core";
import Plot from "react-plotly.js";
import { withTranslation, WithTranslation } from "react-i18next";

/**
 * Interface representing chart data structure
 * @interface ChartData
 * @property {number[]} x_data - Array of x-axis data points
 * @property {number[]} y_data - Array of y-axis data points
 * @property {string} marker_name - Name/label for the data series
 * @property {string} [x_label] - Optional label for x-axis
 * @property {string} [y_label] - Optional label for y-axis
 * @property {string} [chart_title] - Optional title for the chart
 */
interface ChartData {
  x_data: number[];
  y_data: number[];
  marker_name: string;
  x_label?: string;
  y_label?: string;
  chart_title?: string;
}

/**
 * Props interface for ChartComponent
 * @interface ChartComponentProps
 * @extends {WithTranslation}
 * @property {ChartData[]} charts - Array of chart data objects
 * @property {boolean} [isCollapsed] - Whether the chart is currently collapsed
 * @property {() => void} [onToggleCollapse] - Callback function to toggle collapse state
 * @property {string} [title] - Optional chart title (overrides data title)
 * @property {string} [xLabel] - Optional x-axis label (overrides data label)
 * @property {string} [yLabel] - Optional y-axis label (overrides data label)
 * @property {string} [chartType] - Type of chart visualization
 * @property {number} [containerWidth] - Optional fixed container width
 */
interface ChartComponentProps extends WithTranslation {
  charts: ChartData[];
  isCollapsed?: boolean;
  onToggleCollapse?: () => void;
  title?: string;
  xLabel?: string;
  yLabel?: string;
  chartType?: string;
  containerWidth?: number;
}

/**
 * Constants for chart configuration and styling
 * @constant
 * @property {number} MIN_WIDTH - Minimum width of the chart in pixels
 * @property {number} MIN_HEIGHT - Minimum height of the chart in pixels
 * @property {number} ASPECT_RATIO - Width to height ratio for responsive sizing
 * @property {number} COLLAPSED_MIN_WIDTH - Minimum width when chart is collapsed
 * @property {number} COLLAPSED_MIN_HEIGHT - Minimum height when chart is collapsed
 * @property {number} BORDER_RADIUS - Border radius for chart container
 * @property {number} PADDING - Internal padding for chart container
 * @property {Object} MARGIN - Plotly chart margin configuration
 * @property {number} WIDTH_OFFSET - Offset to account for container padding/borders
 * @property {number} MODAL_SIZE - Size ratio for fullscreen modal (0-1)
 * @property {Object} MARKER - Marker styling configuration
 * @property {number} LINE_WIDTH - Line width for chart series
 * @property {Object} FONT_SIZES - Font size configuration for different elements
 * @property {Object} COLORS - Color scheme configuration
 * @property {Object} Z_INDEX - Z-index values for layered elements
 */
const CHART_CONSTANTS = {
  MIN_WIDTH: 250,
  MIN_HEIGHT: 300,
  ASPECT_RATIO: 0.5,
  COLLAPSED_MIN_WIDTH: 150,
  COLLAPSED_MIN_HEIGHT: 200,
  BORDER_RADIUS: 3,
  PADDING: 10,
  MARGIN: {
    LEFT: 60,
    RIGHT: 30,
    BOTTOM: 60,
    TOP: 60,
    PAD: 4,
  },
  WIDTH_OFFSET: 60,
  MODAL_SIZE: 0.9,
  MARKER: {
    SIZE: 8,
    LINE_WIDTH: 1,
  },
  LINE_WIDTH: 2,
  FONT_SIZES: {
    TITLE: 16,
    AXIS: 12,
    MODAL_TITLE: 20,
    MODAL_AXIS: 14,
  },
  COLORS: {
    GRID: "#eee",
    BACKGROUND: "#f9f9f9",
    PAPER: "#fff",
    COLLAPSED_BACKGROUND: "#f5f5f5",
    BORDER: "#ccc",
    LEGEND_BACKGROUND: "rgba(255, 255, 255, 0.8)",
    LEGEND_BORDER: "#ccc",
  },
  Z_INDEX: {
    CONTROLS: 100,
  },
} as const;

/**
 * Array of marker symbols for differentiating data series
 * @constant
 * @type {string[]}
 */
const MARKER_SYMBOLS = [
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

/**
 * React component for displaying interactive charts with multiple data series
 * @component
 * @param {ChartComponentProps} props - Component properties
 * @returns {JSX.Element} Rendered chart component
 */
const ChartComponent: React.FC<ChartComponentProps> = ({
  charts,
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

  /**
   * Effect hook to handle responsive chart sizing
   * Updates dimensions on mount, container width changes, and window resize
   */
  useEffect(() => {
    const updateDimensions = () => {
      let width = 0;

      if (containerWidth && containerWidth > 0) {
        width = containerWidth - CHART_CONSTANTS.WIDTH_OFFSET;
      } else if (containerRef.current) {
        const currentWidth = containerRef.current.offsetWidth;
        width = currentWidth - CHART_CONSTANTS.WIDTH_OFFSET;
      }

      const finalWidth = Math.max(CHART_CONSTANTS.MIN_WIDTH, width);
      const finalHeight = Math.max(
        CHART_CONSTANTS.MIN_HEIGHT,
        finalWidth * CHART_CONSTANTS.ASPECT_RATIO
      );

      setDimensions({ width: finalWidth, height: finalHeight });
    };

    updateDimensions();
    window.addEventListener("resize", updateDimensions);

    return () => window.removeEventListener("resize", updateDimensions);
  }, [containerWidth]);

  /**
   * Determines the axis type based on chart type configuration
   * @param {"x" | "y"} axis - Which axis to get type for
   * @returns {"linear" | "log"} The axis scale type
   */
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

  // Determine chart title and labels with fallback logic
  const chartTitle =
    title || (charts.length > 0 ? charts[0].chart_title : undefined);
  const xAxisLabel =
    xLabel || (charts.length > 0 ? charts[0].x_label : undefined);
  const yAxisLabel =
    yLabel || (charts.length > 0 ? charts[0].y_label : undefined);

  /**
   * Transforms chart data into Plotly-compatible format
   * @type {Array<Object>}
   */
  const plotData = charts.map((chart, index) => ({
    x: chart.x_data,
    y: chart.y_data,
    type: "scatter" as const,
    mode: "lines+markers",
    name: chart.marker_name,
    marker: {
      color: `hsl(${(index * 360) / charts.length}, 70%, 50%)`,
      symbol: MARKER_SYMBOLS[index % MARKER_SYMBOLS.length],
      size: CHART_CONSTANTS.MARKER.SIZE,
      line: {
        width: CHART_CONSTANTS.MARKER.LINE_WIDTH,
        color: `hsl(${(index * 360) / charts.length}, 70%, 30%)`,
      },
    },
    line: {
      width: CHART_CONSTANTS.LINE_WIDTH,
    },
  }));

  /**
   * Layout configuration for the main chart
   * @type {Object}
   */
  const layout = {
    width: dimensions.width,
    height: CHART_CONSTANTS.MIN_HEIGHT,
    title: chartTitle
      ? {
          text: chartTitle,
          x: 0.5,
          xanchor: "center",
          font: {
            size: CHART_CONSTANTS.FONT_SIZES.TITLE,
            weight: "bold",
          },
        }
      : undefined,
    xaxis: {
      title: xAxisLabel
        ? {
            text: xAxisLabel,
            font: {
              size: CHART_CONSTANTS.FONT_SIZES.AXIS,
              weight: "bold",
            },
          }
        : undefined,
      type: getAxisType("x"),
      showgrid: true,
      gridcolor: CHART_CONSTANTS.COLORS.GRID,
      zeroline: false,
    },
    yaxis: {
      title: yAxisLabel
        ? {
            text: yAxisLabel,
            font: {
              size: CHART_CONSTANTS.FONT_SIZES.AXIS,
              weight: "bold",
            },
          }
        : undefined,
      type: getAxisType("y"),
      showgrid: true,
      gridcolor: CHART_CONSTANTS.COLORS.GRID,
      zeroline: false,
    },
    showlegend: true,
    legend: {
      x: 1,
      y: 1,
      xanchor: "right",
      yanchor: "top",
      bgcolor: CHART_CONSTANTS.COLORS.LEGEND_BACKGROUND,
      bordercolor: CHART_CONSTANTS.COLORS.LEGEND_BORDER,
      borderwidth: 1,
    },
    autosize: true,
    margin: {
      l: CHART_CONSTANTS.MARGIN.LEFT,
      r: CHART_CONSTANTS.MARGIN.RIGHT,
      b: CHART_CONSTANTS.MARGIN.BOTTOM,
      t: CHART_CONSTANTS.MARGIN.TOP,
      pad: CHART_CONSTANTS.MARGIN.PAD,
    },
    hovermode: "closest",
    plot_bgcolor: CHART_CONSTANTS.COLORS.BACKGROUND,
    paper_bgcolor: CHART_CONSTANTS.COLORS.PAPER,
  };

  /**
   * Layout configuration for fullscreen modal chart
   * @type {Object}
   */
  const fullScreenLayout = {
    ...layout,
    width: window.innerWidth * CHART_CONSTANTS.MODAL_SIZE,
    height: window.innerHeight * CHART_CONSTANTS.MODAL_SIZE,
    title: chartTitle
      ? {
          ...layout.title,
          font: {
            size: CHART_CONSTANTS.FONT_SIZES.MODAL_TITLE,
          },
        }
      : undefined,
    xaxis: {
      ...layout.xaxis,
      title: xAxisLabel
        ? {
            ...layout.xaxis?.title,
            font: {
              size: CHART_CONSTANTS.FONT_SIZES.MODAL_AXIS,
            },
          }
        : undefined,
    },
    yaxis: {
      ...layout.yaxis,
      title: yAxisLabel
        ? {
            ...layout.yaxis?.title,
            font: {
              size: CHART_CONSTANTS.FONT_SIZES.MODAL_AXIS,
            },
          }
        : undefined,
    },
  };

  // Render collapsed state if isCollapsed is true
  if (isCollapsed) {
    return (
      <div
        style={{
          border: `1px solid ${CHART_CONSTANTS.COLORS.BORDER}`,
          padding: `${CHART_CONSTANTS.PADDING}px`,
          borderRadius: `${CHART_CONSTANTS.BORDER_RADIUS}px`,
          background: CHART_CONSTANTS.COLORS.COLLAPSED_BACKGROUND,
          display: "inline-block",
          minWidth: `${CHART_CONSTANTS.COLLAPSED_MIN_WIDTH}px`,
          maxWidth: "100%",
        }}
      >
      <Button icon="chevron-down" onClick={onToggleCollapse} minimal small>
        {t("chart.showChart", {
          title: chartTitle || "",
        })}
      </Button>
      </div>
    );
  }

  // Render expanded chart with fullscreen modal capability
  return (
    <>
      <div
        ref={containerRef}
        style={{
          position: "relative",
          border: `1px solid ${CHART_CONSTANTS.COLORS.BORDER}`,
          padding: `${CHART_CONSTANTS.PADDING}px`,
          borderRadius: `${CHART_CONSTANTS.BORDER_RADIUS}px`,
          width: "100%",
          minWidth: `${CHART_CONSTANTS.COLLAPSED_MIN_WIDTH}px`,
          minHeight: `${CHART_CONSTANTS.COLLAPSED_MIN_HEIGHT}px`,
          overflow: "hidden",
          boxSizing: "border-box",
          background: CHART_CONSTANTS.COLORS.PAPER,
        }}
      >
        <div
          style={{
            position: "absolute",
            top: `${CHART_CONSTANTS.PADDING}px`,
            right: `${CHART_CONSTANTS.PADDING}px`,
            zIndex: CHART_CONSTANTS.Z_INDEX.CONTROLS,
          }}
        >
          <Button
            icon="fullscreen"
            onClick={() => setIsModalOpen(true)}
            minimal
            small
            style={{ marginRight: "5px" }}
            title={t("chart.fullscreenButton")}
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
        title={chartTitle}
        className="chart-modal"
        style={{
          width: "90vw",
          height: "90vh",
          padding: `${CHART_CONSTANTS.PADDING}px`,
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

export default withTranslation()(ChartComponent);
