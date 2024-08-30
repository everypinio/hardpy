// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from 'react';
import _, { Dictionary, } from "lodash"
import { H1, H2, H4, Tag, Divider } from "@blueprintjs/core";

import { TestItem, TestSuite as TestSuiteComponent } from "./TestSuite_v3"
import { StartOperatorMsgDialog } from 'hardpy_test_view/OperatorMsg';

/**
 * Set of suites
 */

/** Name of a suite and an its object */
interface Suite { name: string; test: TestItem };


interface TestStand {
    name: string
}

interface DriversInfo {
    driver: Record<string, unknown>
}

interface DutInfo {
    batch: string
    board_rev: string
}

interface Dut {
    serial_number: number
    info: DutInfo
}

type Modules = Dictionary<TestItem>

interface OperatorMsgProps {
    msg: string
    title?: string
}

export interface TestRunI {
    modules?: Modules
    test_stand?: TestStand
    dut?: Dut
    name?: string
    status?: string
    start_time?: number,
    timezone?: [string, string],
    stop_time?: number,
    progress?: number,
    drivers?: DriversInfo,
    artifact?: Record<string, unknown>,
    operator_msg?: OperatorMsgProps,
}

/**
 * SuiteList react component props type
*/
interface Props {
    db_state: TestRunI
    defaultClose: boolean
}

/**
 * Render a list of suites with tests inside
 */
export class SuiteList extends React.Component<Props> {
    elements_count: number = 0;

    render(): React.ReactElement {

        if (this.props.db_state.name == undefined) {
            return <div>
                <H2>Loading tests... 🤔</H2>
                {
                    <H4>Try refreshing the page.</H4>
                }
            </div>;
        }

        const db_state = this.props.db_state;
        const start = db_state.start_time ? new Date(db_state.start_time * 1000).toLocaleString() : ""
        const stop = db_state.stop_time ? new Date(db_state.stop_time * 1000).toLocaleString() : ""
        const start_tz = db_state.timezone ? db_state.timezone[0] : ""
        const stop_tz = db_state.timezone ? db_state.timezone[1] : ""


        let module_names: string[] = []
        let modules: Modules = {}
        if (db_state.modules) {
            module_names = Object.keys(db_state.modules)
            modules = db_state.modules
            this.elements_count = module_names.length
        }

        const TAG_ELEMENT_STYLE = { margin: 1 };

        return (
            <>
                <div>
                    <H1>
                        {db_state.name}
                    </H1>
                    {db_state.test_stand &&
                        <Tag minimal style={TAG_ELEMENT_STYLE}>Stand name: {db_state.test_stand?.name}</Tag>
                    }
                    {db_state.status &&
                        <Tag minimal style={TAG_ELEMENT_STYLE}>Status: {db_state.status}</Tag>
                    }
                    {start &&
                        <Tag minimal style={TAG_ELEMENT_STYLE}>Start time: {start + start_tz}</Tag>
                    }
                    {stop &&
                        <Tag minimal style={TAG_ELEMENT_STYLE}>Finish time: {stop + stop_tz}</Tag>
                    }
                    <Divider />
                    {_.map(
                        [...module_names],
                        (name: string, index: number) => this.suiteRender(index, { name: name, test: modules[name] })
                    )}
                </div>
                <div>
                    {this.props.db_state.operator_msg && this.props.db_state.operator_msg.msg && this.props.db_state.operator_msg.msg.length > 0 && (
                        <StartOperatorMsgDialog
                            msg={this.props.db_state.operator_msg?.msg}
                            title={this.props.db_state.operator_msg?.title || "Message"}
                        />
                    )}
                </div>
            </>
        );
    }

    private suiteRender(index: number, suite: Suite) {
        return <TestSuiteComponent
            key={`${suite.name}_${index}`}
            index={index}
            test={suite.test}
            defaultOpen={(this.elements_count < 5) && (this.props.defaultClose == false)}
            commonTestRunStatus={(this.props.db_state.status)}
        />
    }
}


export default SuiteList;
