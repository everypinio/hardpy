// Copyright (c) 2026 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router";
import { toast } from "sonner";

import {
  clearClosedMessages,
  getClosedMessages,
  markMessageAsClosed,
} from "@/lib/closedOperatorMessages";
import { findStoredRunId } from "@/lib/testHistory";
import { usePanel } from "@/panel/PanelContext";

import { StartOperatorMsgDialog } from "./OperatorMsg";

/** How long a notification stays before it fades on its own. */
const NOTIFICATION_DURATION_MS = 10000;

/**
 * Shows the live operator message on every panel route.
 *
 * Operator messages live on the run document, not on a specific module view,
 * so this host must stay mounted outside SuiteList / group pages.
 *
 * A message the test waits on is shown as a dialog box, since closing it is
 * what lets the run continue. A message the test does not wait on is shown as a
 * notification instead, leaving the panel usable.
 */
export function OperatorMessageHost(): React.ReactElement | null {
  const { t } = useTranslation();
  const { testRunData, rows, syncDocumentId, appConfig } = usePanel();
  const navigate = useNavigate();
  const operatorMsg = testRunData.operator_msg;
  const previousRunName = React.useRef(testRunData.name);

  React.useEffect(() => {
    if (previousRunName.current === testRunData.name) {
      return;
    }
    previousRunName.current = testRunData.name;
    clearClosedMessages();
  }, [testRunData.name]);

  const isVisible = Boolean(operatorMsg?.msg?.length && operatorMsg.visible);
  // A message stored by an older Jig has no block flag and was always awaited.
  const isBlocking = operatorMsg?.block ?? true;
  const title = operatorMsg?.title ?? t("operatorDialog.defaultTitle");
  const notificationId = operatorMsg?.id ?? operatorMsg?.msg;

  // The run that raised the message can be stored a moment after it, so the
  // result page is resolved when the operator follows the link.
  const finishedRunRef = React.useRef({
    rows,
    syncDocumentId,
    startTime: testRunData.start_time,
  });
  React.useEffect(() => {
    finishedRunRef.current = {
      rows,
      syncDocumentId,
      startTime: testRunData.start_time,
    };
  }, [rows, syncDocumentId, testRunData.start_time]);

  const openRunResults = React.useCallback(() => {
    const { rows, syncDocumentId, startTime } = finishedRunRef.current;
    const runId = findStoredRunId(rows, syncDocumentId, startTime);
    navigate(runId ? `/results/${runId}` : "/results");
  }, [navigate]);

  const hasResultPage =
    appConfig?.frontend?.test_history !== false &&
    Boolean(testRunData.stop_time);

  React.useEffect(() => {
    if (
      !isVisible ||
      isBlocking ||
      !notificationId ||
      getClosedMessages().has(notificationId)
    ) {
      return;
    }
    markMessageAsClosed(notificationId);
    toast.info(title, {
      id: notificationId,
      description: operatorMsg?.msg,
      duration: NOTIFICATION_DURATION_MS,
      closeButton: true,
      action: hasResultPage
        ? { label: t("history.viewDetails"), onClick: openRunResults }
        : undefined,
    });
  }, [
    isVisible,
    isBlocking,
    notificationId,
    title,
    operatorMsg?.msg,
    hasResultPage,
    openRunResults,
    t,
  ]);

  if (!operatorMsg || !isVisible || !isBlocking) {
    return null;
  }

  return (
    <StartOperatorMsgDialog
      msg={operatorMsg.msg}
      title={title}
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
