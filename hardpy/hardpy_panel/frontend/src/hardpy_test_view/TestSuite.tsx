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

interface WidgetDescription {
  info: Record<string, unknown>;
  type: WidgetType;
}

interface ImageInfo {
  base64?: string;
  format?: string;
  width?: number;
  border?: number;
}

interface HTMLInfo {
  code_or_url?: string;
  is_raw_html?: boolean;
  width?: number;
  border?: number;
}

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

interface Case {
  status: string;
  name: string;
  start_time: number;
  stop_time: number;
  assertion_msg: string | null;
  msg: string[] | null;
  artifact: Record<string, unknown>;
  dialog_box: DialogBoxProps;
}

type Cases = Dictionary<Case>;

export interface TestItem {
  status: string;
  name: string;
  start_time: number;
  stop_time: number;
  artifact: Record<string, unknown>;
  cases: Cases;
}

type Props = {
  index: number;
  test: TestItem;
  defaultOpen: boolean;
  commonTestRunStatus: string | undefined;
  onTestsSelectionChange?: (selectedTests: string[]) => void;
  selectionSupported?: boolean;
} & WithTranslation;

type State = {
  isOpen: boolean;
  selectedTests: Set<string>;
};

const LOADING_ICON_MARGIN = 30;

/**
 * TestSuite component displays a collapsible test suite with test cases.
 * It includes functionality to render test names, statuses, and data.
 */
export class TestSuite extends React.Component<Props, State> {
  private static readonly LOADING_ICON = (
    <div style={{ margin: LOADING_ICON_MARGIN }}>
      <LoadingOutlined spin />
    </div>
  );

  static defaultProps: Partial<Props> = {
    defaultOpen: true,
    selectionSupported: true,
  };

  /**
   * Constructs the TestSuite component.
   * @param {Props} props - The properties passed to the component.
   */
  constructor(props: Props) {
    super(props);

    this.state = {
      isOpen: props.defaultOpen,
      selectedTests: new Set<string>(),
    };

    this.handleClick = this.handleClick.bind(this);
    this.handleTestSelection = this.handleTestSelection.bind(this);
    this.handleSelectAll = this.handleSelectAll.bind(this);
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
            this.renderTests(this.props.test.cases)
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
    const { test } = this.props;
    const case_names = Object.keys(test.cases);

    if (case_names.length === 0) {
      return false;
    }

    return case_names.every((caseName) => {
      const testFullPath = `${test.name}::${test.cases[caseName].name}`;
      return this.state.selectedTests.has(testFullPath);
    });
  }

  /**
   * Checks if some (but not all) tests in a module are selected
   */
  private isSomeTestsSelected(): boolean {
    const { test } = this.props;
    const case_names = Object.keys(test.cases);

    if (case_names.length === 0) {
      return false;
    } else {
      const selectedCount = case_names.filter((caseName) => {
        const testFullPath = `${test.name}::${test.cases[caseName].name}`;
        return this.state.selectedTests.has(testFullPath);
      }).length;
      console.log("Selected tests being sent:", this.state.selectedTests);

      return selectedCount > 0 && selectedCount < case_names.length;
    }
  }

  /**
   * Renders the name of the test suite.
   * @param {string} name - The name of the test suite.
   * @returns {React.ReactElement} The rendered name element.
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
   * Renders the test cases within the test suite.
   * @param {Cases} test_topics - The test cases to render.
   * @returns {React.ReactElement} The rendered test cases.
   */
  private renderTests(test_topics: Cases): React.ReactElement {
    let case_names: string[] = [];

    if (test_topics) {
      case_names = Object.keys(test_topics);
    }

    const case_array: Case[] = case_names.map((n) => test_topics[n]);

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
        grow: 6,
      },
      {
        id: "data",
        name: this.props.t("testSuite.dataColumn"),
        selector: (row) => row,
        cell: this.cellRendererData.bind(this, case_array),
        grow: 18,
      },
    ];

    return (
      // compensation for 1px shadow of Table
      <div style={{ margin: "3px", paddingBottom: "4px", borderRadius: "2px" }}>
        <DataTable
          noHeader={true}
          columns={columns}
          data={case_names}
          highlightOnHover={true}
          dense={true}
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
    const test = test_topics[rowIndex];
    const testFullPath = `${this.props.test.name}::${test.name}`;
    const isSelected = this.state.selectedTests.has(testFullPath);

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
    this.setState((prevState) => {
      const newSelectedTests = new Set(prevState.selectedTests);

      if (isChecked) {
        newSelectedTests.add(testPath);
      } else {
        newSelectedTests.delete(testPath);
      }

      const selectedTestsArray = Array.from(newSelectedTests);

      this.sendSelectedTestsToBackend(selectedTestsArray);

      if (this.props.onTestsSelectionChange) {
        this.props.onTestsSelectionChange(selectedTestsArray);
      }

      return { selectedTests: newSelectedTests };
    });
  }

  /**
   * Handles select all/deselect all.
   */
  private handleSelectAll(e: React.ChangeEvent<HTMLInputElement>): void {
    const { test } = this.props;
    const case_names = Object.keys(test.cases);

    this.setState((prevState) => {
      const newSelectedTests = new Set(prevState.selectedTests);

      if (e.target.checked) {
        // Select all
        case_names.forEach((caseName) => {
          const testFullPath = `${test.name}::${test.cases[caseName].name}`;
          newSelectedTests.add(testFullPath);
        });
      } else {
        // Deselect all
        case_names.forEach((caseName) => {
          const testFullPath = `${test.name}::${test.cases[caseName].name}`;
          newSelectedTests.delete(testFullPath);
        });
      }

      const selectedTestsArray = Array.from(newSelectedTests);

      this.sendSelectedTestsToBackend(selectedTestsArray);

      // Notify parent component about selection change
      if (this.props.onTestsSelectionChange) {
        this.props.onTestsSelectionChange(selectedTestsArray);
      }

      return { selectedTests: newSelectedTests };
    });
  }

  /**
   * Renders the right panel of the test suite.
   * @param {TestItem} test_topics - The test item containing cases.
   * @returns {React.ReactElement} The rendered right panel.
   */
  private renderTestSuiteRightPanel(test_topics: TestItem): React.ReactElement {
    return (
      <div
        className={Classes.ALIGN_RIGHT}
        style={{ display: "flex", padding: "5px" }}
      >
        {!this.state.isOpen && (
          <>
            {Object.entries(test_topics.cases).map(([_key, value]) => {
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
   * Common method to render a cell with optional loading skeleton.
   * @param {React.ReactElement} cell_content - The content to render in the cell.
   * @param {string} key - The unique key for the cell.
   * @param {boolean} is_loading - Whether to show a loading skeleton.
   * @returns {React.ReactElement} The rendered cell.
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
   * Renders the test number in a cell.
   * @param {Case[]} test_topics - The test cases.
   * @param {string} row_ - The row data.
   * @param {number} rowIndex - The index of the row.
   * @returns {React.ReactElement} The rendered test number cell.
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
   * Renders the test name in a cell.
   * @param {Case[]} test_topics - The test cases.
   * @param {string} row_ - The row data.
   * @param {number} rowIndex - The index of the row.
   * @returns {React.ReactElement} The rendered test name cell.
   */
  private cellRendererName(
    test_topics: Case[],
    row_: string,
    rowIndex: number
  ): React.ReactElement {
    const test = test_topics[rowIndex];
    return this.commonCellRender(
      <div style={{ marginTop: "0.2em", marginBottom: "0.2em" }}>
        <TestName name={test.name} />
      </div>,
      `name_${rowIndex}_${row_}`
    );
  }

  /**
   * Renders the test data in a cell.
   * @param {Case[]} test_topics - The test cases.
   * @param {string} row_ - The row data.
   * @param {number} rowIndex - The index of the row.
   * @returns {React.ReactElement} The rendered test data cell.
   */
  private cellRendererData(
    test_topics: Case[],
    row_: string,
    rowIndex: number
  ): React.ReactElement {
    const test = test_topics[rowIndex];

    return this.commonCellRender(
      <div style={{ marginTop: "0.2em", marginBottom: "0.2em" }}>
        <TestData assertion_msg={test.assertion_msg} msg={test.msg} />
      </div>,
      `data_${rowIndex}_${row_}`
    );
  }

  /**
   * Renders the test status in a cell.
   * @param {Case[]} test_topics - The test cases.
   * @param {string} row_ - The row data.
   * @param {number} rowIndex - The index of the row.
   * @returns {React.ReactElement} The rendered test status cell.
   */
  private cellRendererStatus(
    test_topics: Case[],
    row_: string,
    rowIndex: number
  ): React.ReactElement {
    const test = test_topics[rowIndex];
    const { info: widget_info, type: widget_type } =
      test.dialog_box.widget || {};
    const {
      base64: image_base64,
      width: image_width,
      border: image_border,
    } = test.dialog_box.image || {};

    return this.commonCellRender(
      <div style={{ marginTop: "0.2em", marginBottom: "0.2em" }}>
        {test.dialog_box.dialog_text &&
          test.status === "run" &&
          this.props.commonTestRunStatus === "run" &&
          test.dialog_box.visible && (
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
            />
          )}
        <TestStatus
          status={
            this.props.commonTestRunStatus !== "run" &&
            (test.status === "run" || test.status === "ready")
              ? "stucked"
              : test.status
          }
        />
      </div>,
      `status_${rowIndex}_${row_}`
    );
  }


  private sendSelectedTestsToBackend(selectedTests: string[]): void {
      const testsJsonString = JSON.stringify(selectedTests);
      
      console.log("Selected tests being sent:", selectedTests);
      fetch(`/api/selected_tests`, {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
          },
          body: testsJsonString,
      })
          .then((response) => response.json())
          .then((data) => {
              console.log("Selected tests sent to backend:", data);
          })
          .catch((error) => {
              console.error("Error sending selected tests:", error);
          });
  }

  /**
   * Handles the click event to toggle the collapse state of the test suite.
   */
  private readonly handleClick = () =>
    this.setState((state: State) => ({ isOpen: !state.isOpen }));
}

TestSuite.defaultProps = {
  defaultOpen: true,
  selectionSupported: true,
};

const TestSuiteComponent = withTranslation()(TestSuite);
export { TestSuiteComponent };
