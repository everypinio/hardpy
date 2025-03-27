// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";

interface Props {
  name: string;
}

/**
 * Renders the provided name inside a React Fragment.
 * 
 * @param {Props} props - The props object containing the name to be displayed.
 * @param {string} props.name - The name to be rendered.
 * @returns {React.ReactElement} A React element containing the provided name.
 */
export function TestName(props: Readonly<Props>): React.ReactElement {
  return <React.Fragment>{props.name}</React.Fragment>;
}

export default TestName;
