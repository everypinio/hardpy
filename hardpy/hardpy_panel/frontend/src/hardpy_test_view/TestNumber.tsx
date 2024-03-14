// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from 'react';
interface Props {
    val: number
}

export function TestNumber(props: Props): React.ReactElement {
    return (
        <>
            {props.val}
        </>
    );
}

export default TestNumber;
