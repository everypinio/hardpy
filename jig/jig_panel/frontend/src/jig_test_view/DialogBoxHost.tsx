// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";

import { findPendingDialog } from "@/lib/pendingDialog";
import { usePanel } from "@/panel/PanelContext";

import { StartConfirmationDialog } from "./DialogBox";

/**
 * Shows the dialog a running test is waiting on, on every panel route.
 *
 * A test blocks until the operator answers, so the dialog must never depend on
 * the test tree being unfolded or on the page being displayed. This host stays
 * mounted outside SuiteList / group pages and reads the pending interaction
 * straight from the run document.
 */
export function DialogBoxHost(): React.ReactElement | null {
  const { testRunData } = usePanel();
  const pending = findPendingDialog(testRunData);

  if (!pending) {
    return null;
  }

  const { dialogBox } = pending;
  const { info: widgetInfo, type: widgetType } = dialogBox.widget ?? {};
  const {
    base64: imageBase64,
    width: imageWidth,
    border: imageBorder,
  } = dialogBox.image ?? {};

  return (
    <StartConfirmationDialog
      key={dialogBox.id}
      title_bar={dialogBox.title_bar ?? pending.caseName}
      dialog_text={dialogBox.dialog_text}
      widget_info={widgetInfo}
      widget_type={widgetType}
      image_base64={imageBase64}
      image_width={imageWidth}
      image_border={imageBorder}
      is_visible={dialogBox.visible}
      id={dialogBox.id}
      font_size={dialogBox.font_size}
      html_code={
        dialogBox.html?.is_raw_html ? dialogBox.html?.code_or_url : undefined
      }
      html_url={
        !dialogBox.html?.is_raw_html ? dialogBox.html?.code_or_url : undefined
      }
      html_width={dialogBox.html?.width}
      html_border={dialogBox.html?.border}
      pass_fail={dialogBox.pass_fail}
      button_text={dialogBox.button_text}
    />
  );
}

export default DialogBoxHost;
