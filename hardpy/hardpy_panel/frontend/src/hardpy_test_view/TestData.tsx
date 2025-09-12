// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { Tag } from "@blueprintjs/core";
import Plot from "react-plotly.js";
import { Dialog, Button, Classes } from "@blueprintjs/core";
import ChartComponent from "./ChartComponent";
import { withTranslation, WithTranslation } from "react-i18next";

import _ from "lodash";

interface Props extends WithTranslation {
  msg: string[] | null;
  assertion_msg: string | null;
  testSuiteIndex: number;
  testCaseIndex: number;
  chart?: ChartData;
  dataColumnWidth?: number;
}

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

interface ChartSeriesData {
  x_data: number[];
  y_data: number[];
  marker_name: string;
  x_label?: string;
  y_label?: string;
  chart_title?: string;
}

const TAG_ELEMENT_STYLE = { margin: 2 };

const MODAL_CONSTANTS = {
  SIZE_RATIO: 0.9,
  MARGIN_TOP: 10,
  MIN_WIDTH: 200,
} as const;

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
  const { t } = props;
  const [isModalOpen, setIsModalOpen] = React.useState(false);
  const storageKey = `chartState_${props.testSuiteIndex}_${props.testCaseIndex}`;

  const [isChartCollapsed, setIsChartCollapsed] = React.useState(() => {
    const savedState = localStorage.getItem(storageKey);
    if (savedState) {
      try {
        const { isCollapsed } = JSON.parse(savedState);
        return isCollapsed || false;
      } catch (e: unknown) {
        console.error(`Error parsing local storage: ${e as Error}.message`);
        return false;
      }
    }
    return false;
  });

  React.useEffect(() => {
    localStorage.setItem(
      storageKey,
      JSON.stringify({
        isCollapsed: isChartCollapsed,
      })
    );
  }, [isChartCollapsed, storageKey]);

  const handleToggleCollapse = () => {
    setIsChartCollapsed(!isChartCollapsed);
  };

  const chartSeriesData: ChartSeriesData[] = React.useMemo(() => {
    if (!props.chart) {
      return [];
    }

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
      marker_name: name || t("chart.series", { number: index + 1 }),
      x_label: props.chart?.x_label_data?.[index] || props.chart?.x_label,
      y_label: props.chart?.y_label_data?.[index] || props.chart?.y_label,
      chart_title: props.chart?.chart_title || props.chart?.title,
    }));
  }, [props.chart, t]);

  const hasChartData = chartSeriesData.length > 0;

  const plotData = chartSeriesData.map((chart, index) => ({
    x: chart.x_data,
    y: chart.y_data,
    type: "scatter",
    mode: "lines+markers",
    name: chart.marker_name,
    marker: {
      color: `hsl(${(index * 360) / chartSeriesData.length}, 70%, 50%)`,
    },
  }));

  const fullScreenLayout = {
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
