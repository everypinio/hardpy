// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import _, { Dictionary } from "lodash";
import { withTranslation, WithTranslation } from "react-i18next";

import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { TestItem, TestSuiteComponent } from "./TestSuite";
import { StartOperatorMsgDialog, CLOSED_MESSAGES_KEY } from "./OperatorMsg";

/**
 * Set of suites
 */

/** Name of a suite and an its object */
interface Suite {
  name: string;
  test: TestItem;
}

interface TestStand {
  name: string;
  info: Record<string, unknown>;
}

interface DriversInfo {
  driver: Record<string, unknown>;
}

interface DutInfo {
  batch: string;
  board_rev: string;
}

interface Dut {
  serial_number: number;
  info: DutInfo;
}

type Modules = Dictionary<TestItem>;

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

interface OperatorMsgProps {
  msg: string;
  title?: string;
  visible: boolean;
  image?: ImageInfo;
  id?: string;
  font_size?: number;
  html?: HTMLInfo;
}

export interface TestRunI {
  modules?: Modules;
  test_stand?: TestStand;
  dut?: Dut;
  name?: string;
  status?: string;
  start_time?: number;
  timezone?: [string, string];
  stop_time?: number;
  progress?: number;
  drivers?: DriversInfo;
  artifact?: Record<string, unknown>;
  operator_msg?: OperatorMsgProps;
  alert?: string;
}

/**
 * SuiteList react component props type
 */
interface Props extends WithTranslation {
  db_state: TestRunI;
  defaultClose: boolean;
  onTestsSelectionChange?: (selectedTests: string[]) => void;
  selectedTests?: string[];
  selectionSupported?: boolean;
  measurementDisplay?: boolean;
  manualCollectMode?: boolean;
  currentTestConfig?: string;
  autoScroll?: boolean;
}

const SECONDS_TO_MILLISECONDS = 1000;

/**
 * Render a list of suites with tests inside
 */
export class SuiteList extends React.Component<
  Props,
  { initialized: boolean }
> {
  elements_count: number = 0;
  previousTestName: string | undefined;

  constructor(props: Props) {
    super(props);
    this.state = {
      initialized: props.i18n?.isInitialized ?? false,
    };
    this.previousTestName = props.db_state.name;
  }

  componentDidMount() {
    if (!this.state.initialized && this.props.i18n) {
      this.props.i18n.on("initialized", () => {
        this.setState({ initialized: true });
      });
    }
  }

  componentDidUpdate(prevProps: Props) {
    if (prevProps.db_state.name !== this.props.db_state.name) {
      try {
        localStorage.removeItem(CLOSED_MESSAGES_KEY);
        console.log("Cleared closed messages for new test run");
      } catch (error) {
        console.error("Error clearing closed messages:", error);
      }
      this.previousTestName = this.props.db_state.name;
    }
  }

  /**
   * Renders the SuiteList component.
   * @returns {React.ReactElement} The rendered component.
   */
  render(): React.ReactElement {
    const { t, i18n } = this.props;
    if (!i18n || !this.state.initialized) {
      return <div>Loading translations...</div>;
    }

    if (this.props.db_state.name == undefined) {
      return (
        <div className="space-y-1">
          <h2 className="text-xl font-semibold tracking-tight">
            {t("suiteList.loadingTests")}
          </h2>
          <p className="text-sm text-muted-foreground">
            {t("suiteList.refreshHint")}
          </p>
        </div>
      );
    }

    const db_state = this.props.db_state;
    const start = db_state.start_time
      ? new Date(db_state.start_time * SECONDS_TO_MILLISECONDS).toLocaleString()
      : "";
    const stop = db_state.stop_time
      ? new Date(db_state.stop_time * SECONDS_TO_MILLISECONDS).toLocaleString()
      : "";
    const start_tz = db_state.timezone ?? "";
    const alert = db_state.alert;

    let module_names: string[] = [];
    let modules: Modules = {};
    if (db_state.modules) {
      module_names = Object.keys(db_state.modules);
      modules = db_state.modules;
      this.elements_count = module_names.length;
    }

    return (
      <>
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            {db_state.name}
          </h1>
          <div className="mt-2 flex flex-wrap items-center gap-1.5">
            {db_state.test_stand && (
              <Badge variant="secondary">
                {t("suiteList.standName")}: {db_state.test_stand?.name}
              </Badge>
            )}
            {start && (
              <Badge variant="secondary">
                {t("suiteList.startTime")}: {start + start_tz}
              </Badge>
            )}
            {stop && (
              <Badge variant="secondary">
                {t("suiteList.finishTime")}: {stop + start_tz}
              </Badge>
            )}
            {alert && (
              <Badge variant="destructive">
                {t("suiteList.alert")}: {alert}
              </Badge>
            )}
            {db_state.test_stand?.info &&
              Object.entries(db_state.test_stand.info).map(([key, value]) => (
                <Badge key={key} variant="secondary">
                  {db_state.test_stand?.name} {key}:{" "}
                  {typeof value === "string" ? value : JSON.stringify(value)}
                </Badge>
              ))}
          </div>
          <Separator className="my-4" />
          {_.map([...module_names], (name: string, index: number) =>
            this.suiteRender(index, { name: name, test: modules[name] })
          )}
        </div>
        <div>
          {this.props.db_state.operator_msg?.msg &&
            this.props.db_state.operator_msg.msg.length > 0 &&
            this.props.db_state.operator_msg.visible && (
              <StartOperatorMsgDialog
                msg={this.props.db_state.operator_msg?.msg}
                title={
                  this.props.db_state.operator_msg?.title ??
                  t("operatorDialog.defaultTitle")
                }
                image_base64={this.props.db_state.operator_msg?.image?.base64}
                image_width={this.props.db_state.operator_msg?.image?.width}
                image_border={this.props.db_state.operator_msg?.image?.border}
                is_visible={this.props.db_state.operator_msg?.visible}
                id={this.props.db_state.operator_msg?.id}
                font_size={this.props.db_state.operator_msg?.font_size}
                html_code={
                  this.props.db_state.operator_msg?.html?.is_raw_html
                    ? this.props.db_state.operator_msg?.html?.code_or_url
                    : undefined
                }
                html_url={
                  !this.props.db_state.operator_msg?.html?.is_raw_html
                    ? this.props.db_state.operator_msg?.html?.code_or_url
                    : undefined
                }
                html_width={this.props.db_state.operator_msg?.html?.width}
                html_border={this.props.db_state.operator_msg?.html?.border}
              />
            )}
        </div>
      </>
    );
  }

  /**
   * Renders a single suite component.
   * @param {number} index - The index of the suite.
   * @param {Suite} suite - The suite object containing name and test details.
   * @returns {React.ReactElement} The rendered suite component.
   */
  private suiteRender(index: number, suite: Suite): React.ReactElement {
    return (
      <TestSuiteComponent
        key={`${suite.name}_${index}`}
        index={index}
        test={suite.test}
        defaultOpen={this.elements_count < 5 && !this.props.defaultClose}
        commonTestRunStatus={this.props.db_state.status}
        moduleTechName={suite.name}
        onTestsSelectionChange={this.props.onTestsSelectionChange}
        selectedTests={this.props.selectedTests}
        selectionSupported={this.props.selectionSupported}
        measurementDisplay={this.props.measurementDisplay}
        manualCollectMode={this.props.manualCollectMode}
        autoScroll={this.props.autoScroll}
      />
    );
  }
}

export default withTranslation()(SuiteList);
