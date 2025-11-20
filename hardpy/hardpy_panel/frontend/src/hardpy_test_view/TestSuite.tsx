// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import {
  Callout,
  Collapse,
  Button,
  H4,
  Classes,
  Icon,
  Tag,
} from "@blueprintjs/core";
import _, { Dictionary } from "lodash";
import DataTable, { TableColumn } from "react-data-table-component";
import { LoadingOutlined } from "@ant-design/icons";
import { StartConfirmationDialog, WidgetType } from "./DialogBox";
import { withTranslation, WithTranslation } from "react-i18next";

import { TestNumber } from "./TestNumber";
import { TestName } from "./TestName";
import { TestStatus } from "./TestStatus";
import TestData from "./TestData";
import RunTimer from "./RunTimer";

import "./TestSuite.css";
import { Spin, Checkbox } from "antd";

/**
 * Interface representing widget description for dialog boxes
 * @interface WidgetDescription
 * @property {Record<string, unknown>} info - Widget configuration and data
 * @property {WidgetType} type - Type of widget (input, selection, etc.)
 */
interface WidgetDescription {
  info: Record<string, unknown>;
  type: WidgetType;
}

/**
 * Interface representing image information for dialog boxes
 * @interface ImageInfo
 * @property {string} [base64] - Base64 encoded image data
 * @property {string} [format] - Image format (png, jpg, etc.)
 * @property {number} [width] - Image display width
 * @property {number} [border] - Image border thickness
 */
interface ImageInfo {
  base64?: string;
  format?: string;
  width?: number;
  border?: number;
}

/**
 * Interface representing HTML content information for dialog boxes
 * @interface HTMLInfo
 * @property {string} [code_or_url] - HTML code or URL
 * @property {boolean} [is_raw_html] - Whether the content is raw HTML or a URL
 * @property {number} [width] - HTML content display width
 * @property {number} [border] - HTML content border thickness
 */
interface HTMLInfo {
  code_or_url?: string;
  is_raw_html?: boolean;
  width?: number;
  border?: number;
}

/**
 * Interface representing dialog box properties
 * @interface DialogBoxProps
 * @property {string} [title_bar] - Dialog box title
 * @property {string} dialog_text - Main dialog text content
 * @property {WidgetDescription} [widget] - Optional widget configuration
 * @property {ImageInfo} [image] - Optional image configuration
 * @property {boolean} visible - Whether the dialog is visible
 * @property {string} id - Unique identifier for the dialog
 * @property {number} [font_size] - Font size for dialog text
 * @property {HTMLInfo} [html] - Optional HTML content configuration
 */
interface DialogBoxProps {
  title_bar?: string;
  dialog_text: string;
  widget?: WidgetDescription;
  image?: ImageInfo;
  visible: boolean;
  id: string;
  font_size?: number;
  html?: HTMLInfo;
}

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
 * Interface representing a test case
 * @interface Case
 * @property {string} status - Current status of the test case
 * @property {string} name - Name of the test case
 * @property {number} start_time - Timestamp when the test started
 * @property {number} stop_time - Timestamp when the test stopped
 * @property {string | null} assertion_msg - Assertion message if test failed
 * @property {string[] | null} msg - Array of test messages
 * @property {Record<string, unknown>} artifact - Test artifacts and metadata
 * @property {DialogBoxProps} dialog_box - Dialog box configuration
 * @property {ChartData} [chart] - Optional chart data for visualization
 */
interface Case {
  status: string;
  name: string;
  start_time: number;
  stop_time: number;
  assertion_msg: string | null;
  msg: string[] | null;
  measurements: Measurement[];
  artifact: Record<string, unknown>;
  dialog_box: DialogBoxProps;
  chart?: ChartData;
}

/**
 * Interface representing chart data for test visualization
 * @interface ChartData
 * @property {string} type - Type of chart (line, bar, etc.)
 * @property {string} [title] - Chart title
 * @property {string} [x_label] - X-axis label
 * @property {string} [y_label] - Y-axis label
 * @property {string[]} marker_name - Array of series names
 * @property {number[][]} x_data - 2D array of x-axis data points
 * @property {number[][]} y_data - 2D array of y-axis data points
 */
interface ChartData {
  type: string;
  title?: string;
  x_label?: string;
  y_label?: string;
  marker_name: string[];
  x_data: number[][];
  y_data: number[][];
}

/**
 * Type representing a dictionary of test cases
 * @type {Dictionary<Case>}
 */
type Cases = Dictionary<Case>;

/**
 * Interface representing a test item (test suite)
 * @interface TestItem
 * @property {string} status - Current status of the test suite
 * @property {string} name - Name of the test suite
 * @property {number} start_time - Timestamp when the suite started
 * @property {number} stop_time - Timestamp when the suite stopped
 * @property {Record<string, unknown>} artifact - Suite artifacts and metadata
 * @property {Cases} cases - Dictionary of test cases in this suite
 */
export interface TestItem {
  status: string;
  name: string;
  start_time: number;
  stop_time: number;
  artifact: Record<string, unknown>;
  cases: Cases;
}

/**
 * Props interface for TestSuite component
 * @interface Props
 * @extends {WithTranslation}
 * @property {number} index - Index of the test suite in the list
 * @property {TestItem} test - Test suite data object
 * @property {boolean} [defaultOpen] - Whether the suite should be initially expanded
 * @property {string | undefined} commonTestRunStatus - Global test run status
 */
type Props = {
  index: number;
  test: TestItem;
  defaultOpen?: boolean;
  commonTestRunStatus: string | undefined;
  onTestsSelectionChange?: (selectedTests: string[]) => void;
  selectionSupported?: boolean;
  moduleTechName: string;
  selectedTests?: string[];
  measurementDisplay?: boolean;
  manualCollectMode?: boolean;
} & WithTranslation;

/**
 * State interface for TestSuite component
 * @interface State
 * @property {boolean} isOpen - Whether the test suite is expanded
 * @property {number} dataColumnWidth - Current width of the data column
 */
type State = {
  isOpen: boolean;
  dataColumnWidth: number;
};

/**
 * Margin constant for loading icon
 * @constant
 */
const LOADING_ICON_MARGIN = 30;

/**
 * TestSuite component displays a collapsible test suite with test cases.
 * It provides functionality to render test names, statuses, timing information,
 * and detailed test data including charts and dialog boxes.
 *
 * @component
 * @example
 * <TestSuite
 *   index={0}
 *   test={testSuiteData}
 *   defaultOpen={true}
 *   commonTestRunStatus="run"
 * />
 */
export class TestSuite extends React.Component<Props, State> {
  /**
   * Static loading icon component for busy states
   * @static
   * @type {React.ReactElement}
   */
  private static readonly LOADING_ICON: React.ReactElement = (
    <div style={{ margin: LOADING_ICON_MARGIN }}>
      <LoadingOutlined spin />
    </div>
  );

  /**
   * Default props for the TestSuite component
   * @static
   * @type {Partial<Props>}
   */
  static defaultProps: Partial<Props> = {
    defaultOpen: true,
    selectionSupported: true,
  };

  /**
   * Reference to the data column container for width measurement
   * @private
   * @type {React.RefObject<HTMLDivElement>}
   */
  private readonly dataColumnRef: React.RefObject<HTMLDivElement>;

  /**
   * Resize observer for tracking data column width changes
   * @private
   * @type {ResizeObserver | null}
   */
  private resizeObserver: ResizeObserver | null = null;

  /**
   * Constructs the TestSuite component.
   * @param {Props} props - The properties passed to the component.
   */
  constructor(props: Props) {
    super(props);

    this.state = {
      isOpen: props.defaultOpen ?? false,
      dataColumnWidth: 0,
    };

    this.handleClick = this.handleClick.bind(this);
    this.handleTestSelection = this.handleTestSelection.bind(this);
    this.handleSelectAll = this.handleSelectAll.bind(this);
    this.dataColumnRef = React.createRef();
  }

  /**
   * Renders the TestSuite component.
   * @returns {React.ReactElement} The rendered component.
   */
  render(): React.ReactElement {
    const { t, i18n } = this.props;

    if (!i18n?.isInitialized) {
      return <div>{t("testSuite.loading")}</div>;
    }
    return (
      <Callout style={{ padding: 0, borderRadius: 0 }} className="test-suite">
        <div style={{ display: "flex" }}>
          <div style={{ flex: "1 1 0%" }}>
            <Button
              style={{ margin: "2px" }}
              minimal={true}
              onClick={this.handleClick}
            >
              <div style={{ display: "flex", alignItems: "center" }}>
                <TestStatus
                  status={
                    this.props.commonTestRunStatus != "run" &&
                    (this.props.test.status == "run" ||
                      this.props.test.status == "ready")
                      ? "stucked"
                      : this.props.test.status
                  }
                />
                <Icon
                  style={{ marginRight: "10px", marginLeft: "10px" }}
                  icon={this.state.isOpen ? "chevron-down" : "chevron-right"}
                ></Icon>
                {this.props.selectionSupported && (
                  <Checkbox
                    style={{ marginRight: "60px" }}
                    checked={this.isAllTestsSelected()}
                    indeterminate={this.isSomeTestsSelected()}
                    onChange={this.handleSelectAll}
                    onClick={(e) => e.stopPropagation()}
                  />
                )}
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    minWidth: "65px",
                  }}
                >
                  <span
                    className={Classes.TEXT_DISABLED}
                    style={{ marginRight: "20px" }}
                  >
                    {this.props.index + 1}
                  </span>
                  <span>{this.renderName(this.props.test.name)}</span>
                </div>
              </div>
            </Button>
          </div>
          {this.renderTestSuiteRightPanel(this.props.test)}
        </div>
        <Collapse
          isOpen={this.state.isOpen}
          keepChildrenMounted={true}
          className="test-suite-content"
        >
          {this.props.test.status != "busy" ? (
            <div>{this.renderTests(this.props.test.cases)}</div>
          ) : (
            <Spin indicator={TestSuite.LOADING_ICON} />
          )}
        </Collapse>
      </Callout>
    );
  }

  /**
   * Checks if all tests in a module are selected.
   */
  private isAllTestsSelected(): boolean {
    const { test, selectedTests = [], manualCollectMode = false } = this.props;
    const case_names = Object.keys(test.cases || {});

    if (case_names.length === 0) {
      return false;
    }
    if (!manualCollectMode) {
      return true;
    }
    return case_names.every((caseName) => {
      const testFullPath = `${this.getModuleTechName()}::${caseName}`;
      return selectedTests.includes(testFullPath);
    });
  }

  /**
   * Checks if some (but not all) tests in a module are selected
   */
  private isSomeTestsSelected(): boolean {
    const { test, selectedTests = [], manualCollectMode = false } = this.props;
    const case_names = Object.keys(test.cases || {});

    if (case_names.length === 0) {
      return false;
    }

    if (!manualCollectMode) {
      return false;
    }

    const selectedCount = case_names.filter((caseName) => {
      const testFullPath = `${this.getModuleTechName()}::${caseName}`;
      return selectedTests.includes(testFullPath);
    }).length;

    return selectedCount > 0 && selectedCount < case_names.length;
  }

  /**
   * Lifecycle method called after component mounts
   * Sets up resize observer and initial data column width
   */
  componentDidMount() {
    this.setupResizeObserver();
    this.updateDataColumnWidth();
  }

  /**
   * Lifecycle method called after component updates
   * Handles responsive width updates when test status changes or panel opens
   * @param {Props} prevProps - Previous props
   * @param {State} prevState - Previous state
   */
  componentDidUpdate(prevProps: Props, prevState: State) {
    const statusBecameReady =
      this.props.test.status === "ready" && prevProps.test.status !== "ready";
    const panelJustOpened = this.state.isOpen && !prevState.isOpen;

    if (statusBecameReady || panelJustOpened) {
      this.updateDataColumnWidth();
    }
  }

  /**
   * Lifecycle method called before component unmounts
   * Cleans up resize observer to prevent memory leaks
   */
  componentWillUnmount() {
    this.destroyResizeObserver();
  }

  /**
   * Sets up resize observer to track data column width changes
   * @private
   */
  private readonly setupResizeObserver = () => {
    if (this.dataColumnRef.current) {
      this.destroyResizeObserver();

      this.resizeObserver = new ResizeObserver((entries) => {
        for (const entry of entries) {
          const dataCells = entry.target.querySelectorAll(
            '[data-column-id="data"]'
          );
          if (dataCells.length > 0) {
            const firstDataCell = dataCells[0] as HTMLElement;
            this.setState({ dataColumnWidth: firstDataCell.offsetWidth });
          }
        }
      });

      this.resizeObserver.observe(this.dataColumnRef.current);
    }
  };

  /**
   * Destroys the resize observer and cleans up resources
   * @private
   */
  private readonly destroyResizeObserver = () => {
    if (this.resizeObserver) {
      this.resizeObserver.disconnect();
      this.resizeObserver = null;
    }
  };

  /**
   * Updates the data column width state based on current DOM measurements
   * @private
   */
  private readonly updateDataColumnWidth = () => {
    if (this.dataColumnRef.current) {
      const dataCells = this.dataColumnRef.current.querySelectorAll(
        '[data-column-id="data"]'
      );
      if (dataCells.length > 0) {
        const firstDataCell = dataCells[0] as HTMLElement;
        this.setState({
          dataColumnWidth: firstDataCell.offsetWidth,
        });
      }
    }
  };

  /**
   * Renders the name of the test suite with optional loading state
   * @param {string} name - The name of the test suite
   * @returns {React.ReactElement} The rendered name element
   *
   */
  private renderName(name: string): React.ReactElement {
    const is_loading = _.isEmpty(name);

    return (
      <H4
        className={`test-suite-name ${is_loading ? Classes.SKELETON : ""}`}
        style={{ margin: 0 }}
      >
        {is_loading ? this.props.t("testSuite.stubName") : name}
      </H4>
    );
  }

  /**
   * Renders the test cases within the test suite as a data table
   * @param {Cases} test_topics - The test cases to render
   * @returns {React.ReactElement} The rendered test cases table
   * @private
   */
  private renderTests(test_topics: Cases): React.ReactElement {
    let case_names: string[] = [];

    if (test_topics) {
      case_names = Object.keys(test_topics);
    }

    // Filter out undefined test cases and create safe arrays
    const case_names_filtered = case_names.filter((n) => {
      const testCase = test_topics[n];
      return testCase !== undefined && testCase !== null;
    });
    const case_array: Case[] = case_names_filtered.map((n) => test_topics[n]);

    /**
     * Column configuration for the test cases data table
     * @type {TableColumn<string>[]}
     */
    const columns: TableColumn<string>[] = [
      {
        id: "status",
        name: "",
        selector: (row) => row,
        cell: this.cellRendererStatus.bind(this, case_array),
        grow: 0.5,
        width: "10px",
      },
      ...(this.props.selectionSupported
        ? [
            {
              id: "selection",
              name: this.props.t("testSuite.selectionColumn"),
              selector: (row: any) => row,
              cell: this.cellRendererSelection.bind(this, case_array),
              grow: 0.5,
              width: "80px",
              center: true,
            },
          ]
        : []),
      {
        id: "test_number",
        name: "",
        selector: (row) => row,
        cell: this.cellRendererNumber.bind(this, case_array),
        grow: 0.5,
        width: "65px",
        style: { paddingLeft: "12px" },
      },
      {
        id: "name",
        name: this.props.t("testSuite.nameColumn"),
        selector: (row) => row,
        cell: this.cellRendererName.bind(this, case_array),
        grow: 4,
      },
      {
        id: "data",
        name: this.props.t("testSuite.dataColumn"),
        selector: (row) => row,
        cell: this.cellRendererData.bind(this, case_array),
        grow: 18,
        cellProps: () => ({ "data-column-id": "data" }),
      },
    ];

    return (
      // compensation for 1px shadow of Table
      <div
        ref={this.dataColumnRef}
        style={{ margin: "3px", paddingBottom: "4px", borderRadius: "2px" }}
      >
        <DataTable
          noHeader={true}
          columns={columns}
          data={case_names_filtered}
          highlightOnHover={true}
          dense={true}
          responsive={true}
          persistTableHead={false}
          fixedHeader={false}
          fixedHeaderScrollHeight="unset"
        />
      </div>
    );
  }

  /**
   * Renders the selection checkbox in a cell.
   * @param {Case[]} test_topics - The test cases.
   * @param {string} row_ - The row data.
   * @param {number} rowIndex - The index of the row.
   * @returns {React.ReactElement} The rendered selection cell.
   */
  private cellRendererSelection(
    test_topics: Case[],
    row_: string,
    rowIndex: number
  ): React.ReactElement {
    const { selectedTests = [], manualCollectMode = false } = this.props;
    const testFullPath = `${this.getModuleTechName()}::${row_}`;
    const isSelected = manualCollectMode
      ? selectedTests.includes(testFullPath)
      : true;

    return this.commonCellRender(
      <div
        style={{
          marginTop: "0.2em",
          marginBottom: "0.2em",
          textAlign: "center",
        }}
      >
        <Checkbox
          checked={isSelected}
          disabled={!manualCollectMode}
          onChange={(e) =>
            this.handleTestSelection(testFullPath, e.target.checked)
          }
        />
      </div>,
      `selection_${rowIndex}_${row_}`
    );
  }

  /**
   * Handles individual test selection.
   * @param {string} testPath - The full path of the test.
   * @param {boolean} isChecked - Whether the checkbox is checked.
   */
  private handleTestSelection(testPath: string, isChecked: boolean): void {
    const {
      selectedTests = [],
      onTestsSelectionChange,
      manualCollectMode = false,
    } = this.props;

    if (!manualCollectMode) {
      return;
    }

    let newSelectedTests: string[];
    if (isChecked) {
      newSelectedTests = [...selectedTests, testPath];
    } else {
      newSelectedTests = selectedTests.filter((test) => test !== testPath);
    }

    if (onTestsSelectionChange) {
      onTestsSelectionChange(newSelectedTests);
    }
  }

  /**
   * Handles select all/deselect all.
   */
  private handleSelectAll(e: React.ChangeEvent<HTMLInputElement>): void {
    const {
      test,
      selectedTests = [],
      onTestsSelectionChange,
      manualCollectMode = false,
    } = this.props;

    if (!manualCollectMode) {
      return;
    }

    const case_names = Object.keys(test.cases || {});

    let newSelectedTests: string[];
    if (e.target.checked) {
      // Select all
      newSelectedTests = [
        ...selectedTests.filter(
          (test) => !test.startsWith(`${this.getModuleTechName()}::`)
        ),
        ...case_names.map(
          (caseName) => `${this.getModuleTechName()}::${caseName}`
        ),
      ];
    } else {
      // Deselect all
      newSelectedTests = selectedTests.filter(
        (test) => !test.startsWith(`${this.getModuleTechName()}::`)
      );
    }

    if (onTestsSelectionChange) {
      onTestsSelectionChange(newSelectedTests);
    }
  }

  /**
   * Renders the right panel of the test suite with status icons and timer
   * @param {TestItem} test_topics - The test item containing cases
   * @returns {React.ReactElement} The rendered right panel
   * @private
   */
  private renderTestSuiteRightPanel(test_topics: TestItem): React.ReactElement {
    return (
      <div
        className={Classes.ALIGN_RIGHT}
        style={{ display: "flex", padding: "5px" }}
      >
        {!this.state.isOpen && (
          <>
            {Object.entries(test_topics.cases || {}).map(([key, value]) => {
              if (!value) {
                return null;
              }
              return (
                <span key={value.name} style={{ margin: "2px" }}>
                  <TestStatus status={value.status} />
                </span>
              );
            })}
          </>
        )}

        <Tag minimal={true} style={{ margin: "2px", minWidth: "15px" }}>
          {"ready" != test_topics.status && (
            <RunTimer
              status={test_topics.status}
              commonTestRunStatus={this.props.commonTestRunStatus}
              start_time={test_topics.start_time}
              stop_time={test_topics.stop_time}
            />
          )}
        </Tag>
      </div>
    );
  }

  /**
   * Returns the module tech name
   * @returns {string} The module tech name
   * @private
   */
  private getModuleTechName(): string {
    return this.props.moduleTechName;
  }

  /**
   * Common method to render a table cell with optional loading skeleton
   * @param {React.ReactElement} cell_content - The content to render in the cell
   * @param {string} key - The unique key for the cell
   * @param {boolean} is_loading - Whether to show a loading skeleton
   * @returns {React.ReactElement} The rendered cell
   * @private
   */
  private commonCellRender(
    cell_content: React.ReactElement,
    key: string,
    is_loading: boolean = false
  ): React.ReactElement {
    return (
      <div
        className={is_loading ? Classes.SKELETON : undefined}
        key={key}
        style={{ display: "inline-block", verticalAlign: "middle" }}
      >
        {cell_content}
      </div>
    );
  }

  /**
   * Renders the test number in a table cell
   * @param {Case[]} test_topics - The test cases array
   * @param {string} row_ - The row identifier
   * @param {number} rowIndex - The index of the row
   * @returns {React.ReactElement} The rendered test number cell
   * @private
   */
  private cellRendererNumber(
    test_topics: Case[],
    row_: string,
    rowIndex: number
  ): React.ReactElement {
    return this.commonCellRender(
      <div
        style={{
          marginTop: "0.2em",
          marginBottom: "0.2em",
          paddingLeft: "12px",
        }}
      >
        <TestNumber val={rowIndex + 1} />
      </div>,
      `number_${rowIndex}_${row_}`
    );
  }

  /**
   * Renders the test name in a table cell
   * @param {Case[]} test_topics - The test cases array
   * @param {string} row_ - The row identifier
   * @param {number} rowIndex - The index of the row
   * @returns {React.ReactElement} The rendered test name cell
   * @private
   */
  private cellRendererName(
    test_topics: Case[],
    row_: string,
    rowIndex: number
  ): React.ReactElement {
    const test = test_topics[rowIndex];
    const { selectedTests = [], manualCollectMode = false } = this.props;
    const testFullPath = `${this.getModuleTechName()}::${row_}`;
    const isSelected = manualCollectMode
      ? selectedTests.includes(testFullPath)
      : true;

    const nameStyle: React.CSSProperties = {
      marginTop: "0.2em",
      marginBottom: "0.2em",
      opacity: isSelected ? 1 : 0.6,
    };

    // Safe check for test existence
    if (!test) {
      return this.commonCellRender(
        <div style={nameStyle}>
          <TestName name={""} />
          {manualCollectMode && !isSelected && (
            <Tag
              minimal
              style={{ marginLeft: "8px" }}
              title={this.props.t("testSuite.notSelected")}
            >
              {this.props.t("testSuite.skipped")}
            </Tag>
          )}
        </div>,
        `name_${rowIndex}_${row_}`
      );
    }

    return this.commonCellRender(
      <div style={nameStyle}>
        <TestName name={test.name} />
        {manualCollectMode && !isSelected && (
          <Tag
            minimal
            style={{ marginLeft: "8px" }}
            title={this.props.t("testSuite.notSelected")}
          >
            {this.props.t("testSuite.skipped")}
          </Tag>
        )}
      </div>,
      `name_${rowIndex}_${row_}`
    );
  }

  /**
   * Renders the test data in a table cell
   * @param {Case[]} test_topics - The test cases array
   * @param {string} row_ - The row identifier
   * @param {number} rowIndex - The index of the row
   * @returns {React.ReactElement} The rendered test data cell
   * @private
   */
  private cellRendererData(
    test_topics: Case[],
    row_: string,
    rowIndex: number
  ): React.ReactElement {
    const test = test_topics[rowIndex];

    // Safe check for test existence
    if (!test) {
      return this.commonCellRender(
        <div
          style={{ marginTop: "0.2em", marginBottom: "0.2em" }}
          data-column-id="data"
        ></div>,
        `data_${rowIndex}_${row_}`
      );
    }

    return this.commonCellRender(
      <div
        style={{ marginTop: "0.2em", marginBottom: "0.2em" }}
        data-column-id="data"
      >
        <TestData
          assertion_msg={test.assertion_msg}
          msg={test.msg}
          measurements={test.measurements}
          testSuiteIndex={this.props.index}
          testCaseIndex={rowIndex}
          chart={test.chart}
          dataColumnWidth={this.state.dataColumnWidth}
          measurementDisplay={this.props.measurementDisplay}
        />
      </div>,
      `data_${rowIndex}_${row_}`
    );
  }

  /**
   * Renders the test status and dialog box in a table cell
   * @param {Case[]} test_topics - The test cases array
   * @param {string} row_ - The row identifier
   * @param {number} rowIndex - The index of the row
   * @returns {React.ReactElement} The rendered test status cell
   * @private
   */
  private cellRendererStatus(
    test_topics: Case[],
    row_: string,
    rowIndex: number
  ): React.ReactElement {
    const test = test_topics[rowIndex];
    const { selectedTests = [], manualCollectMode = false } = this.props;
    const testFullPath = `${this.getModuleTechName()}::${row_}`;
    const isSelected = manualCollectMode
      ? selectedTests.includes(testFullPath)
      : true;

    // Safe check for test existence
    if (!test) {
      let displayStatus = "";
      if (
        manualCollectMode &&
        !isSelected &&
        this.props.commonTestRunStatus === "run"
      ) {
        displayStatus = "skipped";
      }

      return this.commonCellRender(
        <div style={{ marginTop: "0.2em", marginBottom: "0.2em" }}>
          <TestStatus
            status={
              this.props.commonTestRunStatus !== "run" &&
              (displayStatus === "run" || displayStatus === "ready")
                ? "stucked"
                : displayStatus
            }
          />
        </div>,
        `status_${rowIndex}_${row_}`
      );
    }

    let displayStatus = test.status;
    if (test.status === "skipped") {
      displayStatus = "skipped";
    } else if (
      manualCollectMode &&
      !isSelected &&
      this.props.commonTestRunStatus === "run"
    ) {
      displayStatus = "skipped";
    }

    const { info: widget_info, type: widget_type } =
      test.dialog_box?.widget || {};
    const {
      base64: image_base64,
      width: image_width,
      border: image_border,
    } = test.dialog_box?.image || {};

    return this.commonCellRender(
      <div style={{ marginTop: "0.2em", marginBottom: "0.2em" }}>
        {test.dialog_box?.dialog_text &&
          test.status === "run" &&
          this.props.commonTestRunStatus === "run" &&
          test.dialog_box?.visible &&
          isSelected && (
            <StartConfirmationDialog
              title_bar={test.dialog_box.title_bar ?? test.name}
              dialog_text={test.dialog_box.dialog_text}
              widget_info={widget_info}
              widget_type={widget_type}
              image_base64={image_base64}
              image_width={image_width}
              image_border={image_border}
              is_visible={test.dialog_box.visible}
              id={test.dialog_box.id}
              font_size={test.dialog_box.font_size}
              html_code={
                test.dialog_box.html?.is_raw_html
                  ? test.dialog_box.html?.code_or_url
                  : undefined
              }
              html_url={
                !test.dialog_box.html?.is_raw_html
                  ? test.dialog_box.html?.code_or_url
                  : undefined
              }
              html_width={test.dialog_box.html?.width}
              html_border={test.dialog_box.html?.border}
              pass_fail={test.dialog_box.pass_fail}
            />
          )}
        <TestStatus
          status={
            this.props.commonTestRunStatus !== "run" &&
            (displayStatus === "run" || displayStatus === "ready")
              ? "stucked"
              : displayStatus
          }
        />
      </div>,
      `status_${rowIndex}_${row_}`
    );
  }

  /**
   * Handles the click event to toggle the collapse state of the test suite
   * @private
   */
  private readonly handleClick = () =>
    this.setState((state) => ({ isOpen: !state.isOpen }));
}

TestSuite.defaultProps = {
  defaultOpen: true,
  selectionSupported: true,
};

/**
 * Higher-order component that wraps TestSuite with translation capabilities
 * @type {React.ComponentType<Omit<Props, keyof WithTranslation>>}
 */
const TestSuiteComponent: React.ComponentType<
  Omit<Props, keyof WithTranslation>
> = withTranslation()(TestSuite);
export { TestSuiteComponent };
