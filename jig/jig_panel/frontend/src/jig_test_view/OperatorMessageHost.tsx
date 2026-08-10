// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { useTranslation } from "react-i18next";

import { usePanel } from "@/panel/PanelContext";

import { CLOSED_MESSAGES_KEY, StartOperatorMsgDialog } from "./OperatorMsg";

/**
 * Shows the live operator-message dialog on every panel route.
 *
 * Operator messages live on the run document, not on a specific module view,
 * so this host must stay mounted outside SuiteList / group pages.
 */
export function OperatorMessageHost(): React.ReactElement | null {
  const { t } = useTranslation();
  const { testRunData } = usePanel();
  const operatorMsg = testRunData.operator_msg;
  const previousRunName = React.useRef(testRunData.name);

  React.useEffect(() => {
    if (previousRunName.current === testRunData.name) {
      return;
    }
    previousRunName.current = testRunData.name;
    try {
      localStorage.removeItem(CLOSED_MESSAGES_KEY);
    } catch (error) {
      console.error("Error clearing closed messages:", error);
    }
  }, [testRunData.name]);

  if (
    !operatorMsg?.msg ||
    operatorMsg.msg.length === 0 ||
    !operatorMsg.visible
  ) {
    return null;
  }

  return (
    <StartOperatorMsgDialog
      msg={operatorMsg.msg}
      title={operatorMsg.title ?? t("operatorDialog.defaultTitle")}
      image_base64={operatorMsg.image?.base64}
      image_width={operatorMsg.image?.width}
      image_border={operatorMsg.image?.border}
      is_visible={operatorMsg.visible}
      id={operatorMsg.id}
      font_size={operatorMsg.font_size}
      html_code={
        operatorMsg.html?.is_raw_html
          ? operatorMsg.html?.code_or_url
          : undefined
      }
      html_url={
        !operatorMsg.html?.is_raw_html
          ? operatorMsg.html?.code_or_url
          : undefined
      }
      html_width={operatorMsg.html?.width}
      html_border={operatorMsg.html?.border}
    />
  );
}

export default OperatorMessageHost;
