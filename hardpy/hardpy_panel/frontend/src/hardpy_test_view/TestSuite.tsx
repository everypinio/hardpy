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
import {
  StartConfirmationDialog,
  WidgetType,
} from "hardpy_test_view/DialogBox";

import { TestNumber } from "./TestNumber";
import { TestName } from "./TestName";
import { TestStatus } from "./TestStatus";
import TestData from "./TestData";
import RunTimer from "./RunTimer";

import "./TestSuite.css";
import { Spin } from "antd";

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

interface DialogBoxProps {
  title_bar?: string;
  dialog_text: string;
  widget?: WidgetDescription;
  image?: ImageInfo;
  visible: boolean;
  id: string;
  font_size?: number;
  html?: string;
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
  key: string;
  index: number;
  test: TestItem;
  defaultOpen: boolean;
  commonTestRunStatus: string | undefined;
};

type State = {
  isOpen: boolean;
};

const SUITE_NAME_STUB = "Lorem ipsum";

export class TestSuite extends React.Component<Props, State> {
  private static LOADING_ICON = (
    <div style={{ margin: 30 }}>
      <LoadingOutlined spin />
    </div>
  );

  static defaultProps: { defaultOpen: boolean };

  render(): React.ReactElement {
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
                <span>
                  {this.renderName(this.props.test.name, this.props.index + 1)}
                </span>
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

  constructor(props: Props) {
    super(props);

    this.state = {
      isOpen: props.defaultOpen,
    };

    this.handleClick = this.handleClick.bind(this);
  }

  private renderName(name: string, test_number: number) {
    const is_loading = _.isEmpty(name);

    return (
      <H4 className={`test-suite-name ${is_loading ? Classes.SKELETON : ""}`}>
        {<span className={Classes.TEXT_DISABLED}>{test_number}</span>}
        {
          <span style={{ marginLeft: "0.5em" }}>
            {is_loading ? SUITE_NAME_STUB : name}
          </span>
        }
      </H4>
    );
  }

  private renderTests(test_topics: Cases) {
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
      {
        id: "test_number",
        name: "",
        selector: (row) => row,
        cell: this.cellRendererNumber.bind(this, case_array),
        grow: 0.5,
        width: "65px",
      },
      {
        id: "name",
        name: "Name",
        selector: (row) => row,
        cell: this.cellRendererName.bind(this, case_array),
        grow: 6,
      },
      {
        id: "data",
        name: "Data",
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

  private renderTestSuiteRightPanel(test_topics: TestItem) {
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

        <Tag minimal={true} style={{ margin: "2px", minWidth: "30px" }}>
          {"ready" != test_topics.status && (
            <RunTimer
              status={test_topics.status}
              commonTestRunStatus={this.props.commonTestRunStatus}
            />
          )}
        </Tag>
      </div>
    );
  }

  private commonCellRender(
    cell_content: React.ReactElement,
    key: string,
    is_loading = false
  ) {
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

  private cellRendererNumber(
    test_topics: Case[],
    row_: string,
    rowIndex: number
  ) {
    return this.commonCellRender(
      <div style={{ marginTop: "0.2em", marginBottom: "0.2em" }}>
        <TestNumber val={rowIndex + 1} />
      </div>,
      `number_${rowIndex}_${row_}}`
    );
  }

  private cellRendererName(
    test_topics: Case[],
    row_: string,
    rowIndex: number
  ) {
    const test = test_topics[rowIndex];
    return this.commonCellRender(
      <div style={{ marginTop: "0.2em", marginBottom: "0.2em" }}>
        <TestName name={test.name} />
      </div>,
      `name_${rowIndex}_${row_}`
    );
  }

  private cellRendererData(
    test_topics: Case[],
    row_: string,
    rowIndex: number
  ) {
    const test = test_topics[rowIndex];

    return this.commonCellRender(
      <div style={{ marginTop: "0.2em", marginBottom: "0.2em" }}>
        <TestData assertion_msg={test.assertion_msg} msg={test.msg} />
      </div>,
      `data_${rowIndex}_${row_}`
    );
  }

  private cellRendererStatus(
    test_topics: Case[],
    row_: string,
    rowIndex: number
  ) {
    const test = test_topics[rowIndex];
    const { info: widget_info, type: widget_type } =
      test.dialog_box.widget || {};
    const {
      base64: image_base64,
      width: image_width,
      border: image_border,
    } = test.dialog_box.image || {};

    const htmlTest = `
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Bokeh Plot</title>
    <style>
      html, body {
        box-sizing: border-box;
        display: flow-root;
        height: 100%;
        margin: 0;
        padding: 0;
      }
    </style>
    <script type="text/javascript" src="https://cdn.bokeh.org/bokeh/release/bokeh-3.6.2.min.js"></script>
    <script type="text/javascript">
        Bokeh.set_log_level("info");
    </script>
  </head>
  <body>
    <div id="efef3b46-ba60-4830-a312-8559a89a4f5e" data-root-id="p1001" style="display: contents;"></div>
  
    <script type="application/json" id="cad74b1d-c39c-4a69-ab28-c88f98ff3906">
      {"00b465c9-7e2a-4124-b65c-0ba1782dee51":{"version":"3.6.2","title":"Bokeh Application","roots":[{"type":"object","name":"Figure","id":"p1001","attributes":{"width":400,"height":400,"x_range":{"type":"object","name":"DataRange1d","id":"p1002"},"y_range":{"type":"object","name":"DataRange1d","id":"p1003"},"x_scale":{"type":"object","name":"LinearScale","id":"p1010"},"y_scale":{"type":"object","name":"LinearScale","id":"p1011"},"title":{"type":"object","name":"Title","id":"p1008"},"renderers":[{"type":"object","name":"GlyphRenderer","id":"p1041","attributes":{"data_source":{"type":"object","name":"ColumnDataSource","id":"p1035","attributes":{"selected":{"type":"object","name":"Selection","id":"p1036","attributes":{"indices":[],"line_indices":[]}},"selection_policy":{"type":"object","name":"UnionRenderers","id":"p1037"},"data":{"type":"map","entries":[["x",[1,2,3,4]],["y",[10,20,25,30]]]}}},"view":{"type":"object","name":"CDSView","id":"p1042","attributes":{"filter":{"type":"object","name":"AllIndices","id":"p1043"}}},"glyph":{"type":"object","name":"Line","id":"p1038","attributes":{"x":{"type":"field","field":"x"},"y":{"type":"field","field":"y"},"line_color":"#1f77b4","line_width":2}},"nonselection_glyph":{"type":"object","name":"Line","id":"p1039","attributes":{"x":{"type":"field","field":"x"},"y":{"type":"field","field":"y"},"line_color":"#1f77b4","line_alpha":0.1,"line_width":2}},"muted_glyph":{"type":"object","name":"Line","id":"p1040","attributes":{"x":{"type":"field","field":"x"},"y":{"type":"field","field":"y"},"line_color":"#1f77b4","line_alpha":0.2,"line_width":2}}}}],"toolbar":{"type":"object","name":"Toolbar","id":"p1009","attributes":{"tools":[{"type":"object","name":"PanTool","id":"p1022"},{"type":"object","name":"WheelZoomTool","id":"p1023","attributes":{"renderers":"auto"}},{"type":"object","name":"BoxZoomTool","id":"p1024","attributes":{"overlay":{"type":"object","name":"BoxAnnotation","id":"p1025","attributes":{"syncable":false,"line_color":"black","line_alpha":1.0,"line_width":2,"line_dash":[4,4],"fill_color":"lightgrey","fill_alpha":0.5,"level":"overlay","visible":false,"left":{"type":"number","value":"nan"},"right":{"type":"number","value":"nan"},"top":{"type":"number","value":"nan"},"bottom":{"type":"number","value":"nan"},"left_units":"canvas","right_units":"canvas","top_units":"canvas","bottom_units":"canvas","handles":{"type":"object","name":"BoxInteractionHandles","id":"p1031","attributes":{"all":{"type":"object","name":"AreaVisuals","id":"p1030","attributes":{"fill_color":"white","hover_fill_color":"lightgray"}}}}}}}},{"type":"object","name":"SaveTool","id":"p1032"},{"type":"object","name":"ResetTool","id":"p1033"},{"type":"object","name":"HelpTool","id":"p1034"}]}},"left":[{"type":"object","name":"LinearAxis","id":"p1017","attributes":{"ticker":{"type":"object","name":"BasicTicker","id":"p1018","attributes":{"mantissas":[1,2,5]}},"formatter":{"type":"object","name":"BasicTickFormatter","id":"p1019"},"major_label_policy":{"type":"object","name":"AllLabels","id":"p1020"}}}],"below":[{"type":"object","name":"LinearAxis","id":"p1012","attributes":{"ticker":{"type":"object","name":"BasicTicker","id":"p1013","attributes":{"mantissas":[1,2,5]}},"formatter":{"type":"object","name":"BasicTickFormatter","id":"p1014"},"major_label_policy":{"type":"object","name":"AllLabels","id":"p1015"}}}],"center":[{"type":"object","name":"Grid","id":"p1016","attributes":{"axis":{"id":"p1012"}}},{"type":"object","name":"Grid","id":"p1021","attributes":{"dimension":1,"axis":{"id":"p1017"}}}]}}]}}
    </script>
    <script type="text/javascript">
      (function() {
        const fn = function() {
          Bokeh.safely(function() {
            (function(root) {
              function embed_document(root) {
              const docs_json = document.getElementById('cad74b1d-c39c-4a69-ab28-c88f98ff3906').textContent;
              const render_items = [{"docid":"00b465c9-7e2a-4124-b65c-0ba1782dee51","roots":{"p1001":"efef3b46-ba60-4830-a312-8559a89a4f5e"},"root_ids":["p1001"]}];
              root.Bokeh.embed.embed_items(docs_json, render_items);
              }
              if (root.Bokeh !== undefined) {
                embed_document(root);
              } else {
                let attempts = 0;
                const timer = setInterval(function(root) {
                  if (root.Bokeh !== undefined) {
                    clearInterval(timer);
                    embed_document(root);
                  } else {
                    attempts++;
                    if (attempts > 100) {
                      clearInterval(timer);
                      console.log("Bokeh: ERROR: Unable to run BokehJS code because BokehJS library is missing");
                    }
                  }
                }, 10, root)
              }
            })(window);
          });
        };
        if (document.readyState != "loading") fn();
        else document.addEventListener("DOMContentLoaded", fn);
      })();
    </script>
  </body>
</html>
  `;

    return this.commonCellRender(
      <div style={{ marginTop: "0.2em", marginBottom: "0.2em" }}>
        {test.dialog_box.dialog_text &&
          test.status === "run" &&
          this.props.commonTestRunStatus === "run" &&
          test.dialog_box.visible == true && (
            <StartConfirmationDialog
              title_bar={test.dialog_box.title_bar || test.name}
              dialog_text={test.dialog_box.dialog_text}
              widget_info={widget_info}
              widget_type={widget_type}
              image_base64={image_base64}
              image_width={image_width}
              image_border={image_border}
              is_visible={test.dialog_box.visible}
              id={test.dialog_box.id}
              font_size={test.dialog_box.font_size}
              html={test.dialog_box.html || htmlTest}
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

  private handleClick = () =>
    this.setState((state: State) => ({ isOpen: !state.isOpen }));
}

TestSuite.defaultProps = {
  defaultOpen: true,
};

export default TestSuite;
