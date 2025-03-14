// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";

interface Props {
  name: string;
}

export function TestName(props: Props): React.ReactElement {
  return <React.Fragment>{props.name}</React.Fragment>;
}

export default TestName;
