// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { Tag } from "@blueprintjs/core";
import Plot from "react-plotly.js";
import { Dialog, Classes } from "@blueprintjs/core";
import ChartComponent from "./ChartComponent";
import { withTranslation, WithTranslation } from "react-i18next";

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

/**
 * Interface representing chart data structure for test results
 * @interface ChartData
 * @property {string} type - Type of chart visualization (e.g., "line", "bar")
 * @property {string} [title] - Optional title for the chart (deprecated, use chart_title)
 * @property {string} [x_label] - Optional label for x-axis
 * @property {string} [y_label] - Optional label for y-axis
 * @property {string[]} marker_name - Array of names/labels for each data series
 * @property {number[][]} x_data - 2D array of x-axis data points for each series
 * @property {number[][]} y_data - 2D array of y-axis data points for each series
 * @property {string} [chart_title] - Optional title for the chart
 * @property {string[]} [x_label_data] - Optional array of x-axis labels for each series
 * @property {string[]} [y_label_data] - Optional array of y-axis labels for each series
 */
interface ChartData {
  type: string;
  title?: string;
  x_label?: string;
  y_label?: string;
  marker_name: string[];
  x_data: number[][];
  y_data: number[][];
  chart_title?: string;
  x_label_data?: string[];
  y_label_data?: string[];
}

/**
 * Interface representing individual chart series data
 * @interface ChartSeriesData
 * @property {number[]} x_data - Array of x-axis data points for the series
 * @property {number[]} y_data - Array of y-axis data points for the series
 * @property {string} marker_name - Name/label for the data series
 * @property {string} [x_label] - Optional label for x-axis of this series
 * @property {string} [y_label] - Optional label for y-axis of this series
 * @property {string} [chart_title] - Optional title for the chart
 */
interface ChartSeriesData {
  x_data: number[];
  y_data: number[];
  marker_name: string;
  x_label?: string;
  y_label?: string;
  chart_title?: string;
}

/**
 * Props interface for TestData component
 * @interface Props
 * @extends {WithTranslation}
 * @property {string[] | null} msg - Array of test messages to display as tags
 * @property {string | null} assertion_msg - Assertion message to display as warning tag
 * @property {number} testSuiteIndex - Index of the test suite for storage key generation
 * @property {number} testCaseIndex - Index of the test case for storage key generation
 * @property {ChartData} [chart] - Optional chart data object for visualization
 * @property {number} [dataColumnWidth] - Optional width for the data column container
 */
interface Props extends WithTranslation {
  msg: string[] | null;
  assertion_msg: string | null;
  testSuiteIndex: number;
  testCaseIndex: number;
  chart?: ChartData;
  dataColumnWidth?: number;
  measurements?: Measurement[];
  measurementDisplay?: boolean;
}

/**
 * Constants for modal styling and configuration
 * @constant
 * @property {number} SIZE_RATIO - Size ratio for fullscreen modal (0-1)
 * @property {number} MARGIN_TOP - Top margin for chart container
 * @property {number} MIN_WIDTH - Minimum width for chart container
 */
const MODAL_CONSTANTS = {
  SIZE_RATIO: 0.9,
  MARGIN_TOP: 10,
  MIN_WIDTH: 200,
} as const;

/**
 * Style constants for tag elements
 * @constant
 * @property {Object} TAG_ELEMENT_STYLE - CSS style object for tag elements
 */
const TAG_ELEMENT_STYLE = { margin: 2 };

/**
 * Determines the lower bracket for range operations (inside range)
 * @param operation - The comparison operation type
 * @returns The lower bracket character - "(" for strict inequalities, "[" for inclusive
 */
const getLowerBracket = (operation?: string): string => {
  switch (operation) {
    case "gtlt":
    case "gtle":
    case "legt":
    case "ltge":
      return "(";
    case "gele":
    case "gelt":
    case "lege":
    case "ltgt":
      return "[";
    default:
      return "[";
  }
};

/**
 * Determines the upper bracket for range operations (inside range)
 * @param operation - The comparison operation type
 * @returns The upper bracket character - ")" for strict inequalities, "]" for inclusive
 */
const getUpperBracket = (operation?: string): string => {
  switch (operation) {
    case "gtlt":
    case "gelt":
    case "ltgt":
    case "ltge":
      return ")";
    case "gele":
    case "gtle":
    case "lege":
    case "legt":
      return "]";
    default:
      return "]";
  }
};

/**
 * Determines the lower bracket for outside range operations
 * @param operation - The comparison operation type for outside range
 * @returns The lower bracket character for the outside range
 */
const getOutsideLowerBracket = (operation?: string): string => {
  switch (operation) {
    case "ltgt":
    case "ltge":
      return ")";
    case "lege":
    case "legt":
      return "]";
    default:
      return ")";
  }
};

/**
 * Determines the upper bracket for outside range operations
 * @param operation - The comparison operation type for outside range
 * @returns The upper bracket character for the outside range
 */
const getOutsideUpperBracket = (operation?: string): string => {
  switch (operation) {
    case "ltgt":
    case "legt":
      return "(";
    case "lege":
    case "ltge":
      return "[";
    default:
      return "(";
  }
};

/**
 * Checks if the operation is a range operation (involving both lower and upper limits)
 * @param operation - The comparison operation type to check
 * @returns True if the operation is a range operation, false otherwise
 */
const isRangeOperation = (operation?: string): boolean => {
  const rangeOperations = [
    "gtlt",
    "gele",
    "gelt",
    "gtle",
    "ltgt",
    "lege",
    "legt",
    "ltge",
  ];
  return operation ? rangeOperations.includes(operation) : false;
};

/**
 * Converts operation type to its corresponding mathematical symbol
 * @param operation - The comparison operation type
 * @returns The mathematical symbol representing the operation
 */
const getComparisonOperator = (operation?: string): string => {
  switch (operation) {
    case "eq":
      return "=";
    case "ne":
      return "≠";
    case "gt":
      return ">";
    case "ge":
      return "≥";
    case "lt":
      return "<";
    case "le":
      return "≤";
    default:
      return operation || "";
  }
};

/**
 * TestData component displays test messages, assertions, and optional chart visualizations
 * @component
 * @param {Props} props - Component properties
 * @returns {React.ReactElement} Rendered test data component with messages and charts
 * 
 * @example
 * <TestData
 *   msg={["Test passed", "Measurement complete"]}
 *   assertion_msg="Assertion failed: expected 5, got 4"
 *   testSuiteIndex={0}
 *   testCaseIndex={1}
 *   chart={chartData}
 * />
 */
export function TestData(props: Readonly<Props>): React.ReactElement {
  const { t } = props;
  const [isModalOpen, setIsModalOpen] = React.useState(false);

  /**
   * Unique storage key for persisting chart collapse state per test case
   * @constant
   * @type {string}
   */
  const storageKey: string = `chartState_${props.testSuiteIndex}_${props.testCaseIndex}`;

    /**
   * Formats a measurement for display with proper mathematical notation
   * @param measurement - The measurement object containing value, limits, and operation
   * @param index - The index of the measurement in the list (for React keys)
   * @returns Formatted string representation of the measurement
   */
  const formatMeasurement = (
    measurement: Measurement,
    index: number
  ): string => {
    let display = "";
    if (measurement.name) {
      display += `${measurement.name}: `;
    }

    display += `${measurement.value}`;

    if (measurement.unit) {
      if (["%", "°", "′", "″"].includes(measurement.unit)) {
        display += measurement.unit;
      } else {
        display += ` ${measurement.unit}`;
      }
    }

    const hasLowerLimit =
      measurement.lower_limit !== undefined && measurement.lower_limit !== null;
    const hasUpperLimit =
      measurement.upper_limit !== undefined && measurement.upper_limit !== null;
    const isRangeOp = isRangeOperation(measurement.operation);

    if (isRangeOp && (hasLowerLimit || hasUpperLimit)) {
      display += " ";

      const isOutsideRangeOp =
        measurement.operation &&
        ["ltgt", "lege", "legt", "ltge"].includes(measurement.operation);

      if (isOutsideRangeOp) {
        const lowerBracket = getOutsideLowerBracket(measurement.operation);
        const upperBracket = getOutsideUpperBracket(measurement.operation);

        if (hasLowerLimit && hasUpperLimit) {
          display += `(-∞; ${measurement.lower_limit}${lowerBracket} ∪ ${upperBracket}${measurement.upper_limit}; ∞)`;
        } else if (hasLowerLimit) {
          display += `(-∞; ${measurement.lower_limit}${lowerBracket}`;
        } else if (hasUpperLimit) {
          display += `${upperBracket}${measurement.upper_limit}; ∞)`;
        }
      } else {
        const lowerBracket = getLowerBracket(measurement.operation);
        const upperBracket = getUpperBracket(measurement.operation);

        if (hasLowerLimit && hasUpperLimit) {
          display += `${lowerBracket}${measurement.lower_limit}; ${measurement.upper_limit}${upperBracket}`;
        } else if (hasLowerLimit) {
          display += `${lowerBracket}${measurement.lower_limit}; ∞)`;
        } else if (hasUpperLimit) {
          display += `(-∞; ${measurement.upper_limit}${upperBracket}`;
        }
      }

    } else if (
      measurement.operation &&
      measurement.comparison_value !== undefined &&
      measurement.comparison_value !== null &&
      !isRangeOp
    ) {
      const operator = measurement.operation;
      const comparisonValue = measurement.comparison_value;
      
      switch (operator) {
        case "gt":
          display += ` (${comparisonValue}; ∞)`;
          break;
        case "ge":
          display += ` [${comparisonValue}; ∞)`;
          break;
        case "lt":
          display += ` (-∞; ${comparisonValue})`;
          break;
        case "le":
          display += ` (-∞; ${comparisonValue}]`;
          break;
        case "eq":
          display += ` [= ${comparisonValue}]`;
          break;
        case "ne":
          display += ` [≠ ${comparisonValue}]`;
          break;
        default:
          { const defaultOperator = getComparisonOperator(measurement.operation);
          display += ` [${defaultOperator} ${comparisonValue}]`; }
      }
    }

    return display;
  };

  /**
   * State hook for chart collapse/expand functionality with localStorage persistence
   * @type {[boolean, React.Dispatch<React.SetStateAction<boolean>>]}
   */
  const [isChartCollapsed, setIsChartCollapsed] = React.useState(() => {
    const savedState = localStorage.getItem(storageKey);
    if (savedState) {
      try {
        const { isCollapsed } = JSON.parse(savedState);
        return isCollapsed || false;
      } catch (e: unknown) {
        console.error(`Error parsing local storage: ${(e as Error).message}`);
        return false;
      }
    }
    return false;
  });

  /**
   * Effect hook to persist chart collapse state to localStorage
   * Runs when isChartCollapsed or storageKey changes
   */
  React.useEffect(() => {
    localStorage.setItem(
      storageKey,
      JSON.stringify({
        isCollapsed: isChartCollapsed,
      })
    );
  }, [isChartCollapsed, storageKey]);

  /**
   * Toggles the chart collapse state between expanded and collapsed
   * @function
   */
  const handleToggleCollapse = () => {
    setIsChartCollapsed(!isChartCollapsed);
  };

  /**
   * Memoized transformation of chart data into series format for ChartComponent
   * Validates data integrity and provides fallback values for missing properties
   * @type {ChartSeriesData[]}
   */
  const chartSeriesData: ChartSeriesData[] = React.useMemo(() => {
    if (!props.chart) {
      return [];
    }

    // Validate required chart data properties
    if (
      !props.chart.marker_name ||
      !props.chart.x_data ||
      !props.chart.y_data
    ) {
      return [];
    }

    const seriesCount = props.chart.marker_name.length;

    // Validate array length consistency
    if (
      props.chart.x_data.length !== seriesCount ||
      props.chart.y_data.length !== seriesCount
    ) {
      console.error("Chart data arrays have different lengths");
      return [];
    }

    // Transform chart data into series format
    return props.chart.marker_name.map((name, index) => ({
      x_data: props.chart!.x_data[index] || [],
      y_data: props.chart!.y_data[index] || [],
      marker_name: name || t("chart.series", { number: index + 1 }),
      x_label: props.chart?.x_label_data?.[index] || props.chart?.x_label,
      y_label: props.chart?.y_label_data?.[index] || props.chart?.y_label,
      chart_title: props.chart?.chart_title || props.chart?.title,
    }));
  }, [props.chart, t]);

  /**
   * Flag indicating whether chart data is available for rendering
   * @type {boolean}
   */
  const hasChartData: boolean = chartSeriesData.length > 0;

  /**
   * Plotly-compatible data format for fullscreen modal chart
   * @type {Array<Object>}
   */
  const plotData: Array<object> = chartSeriesData.map((chart, index) => ({
    x: chart.x_data,
    y: chart.y_data,
    type: "scatter",
    mode: "lines+markers",
    name: chart.marker_name,
    marker: {
      color: `hsl(${(index * 360) / chartSeriesData.length}, 70%, 50%)`,
    },
  }));

  /**
   * Layout configuration for fullscreen modal chart
   * @type {Object}
   */
  const fullScreenLayout: object = {
    width: window.innerWidth * MODAL_CONSTANTS.SIZE_RATIO,
    height: window.innerHeight * MODAL_CONSTANTS.SIZE_RATIO,
    title:
      props.chart?.chart_title || props.chart?.title || t("chart.dataChart"),
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
      {/* Render measurements first */}
      {props.measurementDisplay !== false &&
        props.measurements &&
        props.measurements.length > 0 && (
          <div style={{ marginBottom: "10px" }}>
            {_.map(
              props.measurements,
              (measurement: Measurement, index: number) => {
                const intent =
                  measurement.result === true
                    ? "success"
                    : measurement.result === false
                      ? "danger"
                      : "success";
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
              }
            )}
          </div>
        )}

      {/* Render test messages as primary tags */}
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

      {/* Render assertion message as warning tag (first line only) */}
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

      {/* Chart visualization section */}
      {hasChartData && (
        <>
          <div
            style={{
              width: "100%",
              marginTop: `${MODAL_CONSTANTS.MARGIN_TOP}px`,
              minWidth: `${MODAL_CONSTANTS.MIN_WIDTH}px`,
              boxSizing: "border-box",
            }}
          >
            <ChartComponent
              charts={chartSeriesData}
              isCollapsed={isChartCollapsed}
              onToggleCollapse={handleToggleCollapse}
              title={props.chart?.chart_title || props.chart?.title}
              xLabel={props.chart?.x_label}
              yLabel={props.chart?.y_label}
              chartType={props.chart?.type}
              containerWidth={props.dataColumnWidth}
            />
          </div>

          <div
            style={{
              marginTop: `${MODAL_CONSTANTS.MARGIN_TOP}px`,
              cursor: "pointer",
            }}
            onClick={() => setIsModalOpen(true)}
          ></div>

          {/* Fullscreen chart modal dialog */}
          <Dialog
            isOpen={isModalOpen}
            title={
              props.chart?.chart_title || props.chart?.title || t("chart.chart")
            }
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
          </Dialog>
        </>
      )}
    </div>
  );
}

export default withTranslation()(TestData);
