// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from 'react';
import { Tooltip } from 'antd';
import { AnchorButton, AnchorButtonProps } from '@blueprintjs/core';

type Props = {
    testing_status: string;
    is_authenticated: boolean;
};

export class StartStopButton extends React.Component<Props> {
    constructor(props: Props) {
        super(props);
        this.hardpy_start = this.hardpy_start.bind(this);
        this.hardpy_stop = this.hardpy_stop.bind(this);
    }

    private hardpy_call(uri: string) {
        fetch(uri)
            .then(response => {
                if (response.ok) {
                    return response.text();
                } else {
                    console.log("Request failed. Status: " + response.status);
                }
            })
            .catch(error => {
                console.log("Request failed. Error: " + error);
            });
    }

    private hardpy_start(): void {
        localStorage.clear();
        this.hardpy_call('api/start')
    }

    private hardpy_stop(): void {
        this.hardpy_call('api/stop')
    }

    private hardpy_start_with_space = (event: KeyboardEvent) => {
        const is_testing_in_progress = this.props.testing_status == 'run';
        if (event.key === ' ' && !is_testing_in_progress && this.props.is_authenticated) {
            this.hardpy_start();
        }
    };

    private handleButtonClick = (): void => {
        if (this.props.is_authenticated) {
            this.hardpy_start();
        } else {
            console.log("Authentication required");
        }
    };

    componentDidMount(): void {
        window.addEventListener('keydown', this.hardpy_start_with_space);
    }

    componentWillUnmount(): void {
        window.removeEventListener('keydown', this.hardpy_start_with_space);
    }

    render(): React.ReactNode {
        const is_authenticated = this.props.is_authenticated == true;
        const is_testing_in_progress = this.props.testing_status == 'run';

        const props: AnchorButtonProps =
            is_testing_in_progress ?
                {
                    text: 'Stop',
                    intent: 'danger',
                    large: true,
                    rightIcon: 'stop',
                    onClick: this.hardpy_stop,
                    id: "start-stop-button"
                } :
                {
                    text: 'Start',
                    intent: is_authenticated ? 'primary' : (is_testing_in_progress ? 'danger' : undefined),
                    large: true,
                    rightIcon: 'play',
                    onClick: is_authenticated ? this.handleButtonClick : () => {
                        console.log("Authentication required");
                    },
                    id: "start-stop-button"
                }

        return (
            <Tooltip
                title="It is impossible to connect to the database"
                key="leftButton"
                placement="top"
                trigger="hover"
                visible={!is_authenticated}
            >
                <AnchorButton {...props} />
            </Tooltip>
        );
    }
}

export default StartStopButton;
