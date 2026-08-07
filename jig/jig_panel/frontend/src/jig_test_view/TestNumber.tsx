// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
interface Props {
  /**
   * The numeric value to be displayed.
   */
  val: number;
}

/**
 * A React functional component that renders a numeric value.
 *
 * @param {Props} props - The props passed to the component.
 * @param {number} props.val - The numeric value to be displayed.
 * @returns {React.ReactElement} A React element that displays the provided numeric value.
 */
export function TestNumber(props: Readonly<Props>): React.ReactElement {
  return <>{props.val}</>;
}

export default TestNumber;
