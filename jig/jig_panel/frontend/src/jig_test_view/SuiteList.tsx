// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { Dictionary } from "lodash";
import { withTranslation, WithTranslation } from "react-i18next";

import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { buildSectionTree } from "@/lib/testSections";
import { SectionContents } from "./SectionContents";
import { TestItem } from "./TestSuite";
import { pageTitleClassName } from "./treeStyles";

/**
 * Set of suites
 */

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
  onRunSection?: (moduleIds: string[]) => void;
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

  constructor(props: Props) {
    super(props);
    this.state = {
      initialized: props.i18n?.isInitialized ?? false,
    };
  }

  componentDidMount() {
    if (!this.state.initialized && this.props.i18n) {
      this.props.i18n.on("initialized", () => {
        this.setState({ initialized: true });
      });
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

    const modules: Modules = db_state.modules ?? {};
    this.elements_count = Object.keys(modules).length;
    const tree = buildSectionTree(modules);

    return (
      <>
        <div className="space-y-3">
          <div className="space-y-2">
            <h1 className={pageTitleClassName}>{db_state.name}</h1>
            <div className="flex flex-wrap items-center gap-1.5">
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
          </div>
          <Separator />
          <div className="space-y-0.5">
            <SectionContents
              node={tree}
              startIndex={0}
              defaultClose={this.props.defaultClose}
              commonTestRunStatus={this.props.db_state.status}
              onTestsSelectionChange={this.props.onTestsSelectionChange}
              selectedTests={this.props.selectedTests}
              selectionSupported={this.props.selectionSupported}
              measurementDisplay={this.props.measurementDisplay}
              manualCollectMode={this.props.manualCollectMode}
              autoScroll={this.props.autoScroll}
              onRunSection={this.props.onRunSection}
              onRunModule={
                this.props.onRunSection
                  ? (moduleId: string) => this.props.onRunSection!([moduleId])
                  : undefined
              }
              openRootModulesWhenFew={true}
            />
          </div>
        </div>
      </>
    );
  }
}

export default withTranslation()(SuiteList);
