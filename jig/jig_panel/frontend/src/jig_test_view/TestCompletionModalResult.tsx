// Copyright (c) 2025 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import * as React from "react";
import { CircleAlert, CircleCheck, OctagonPause } from "lucide-react";
import { useTranslation } from "react-i18next";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { cn } from "@/lib/utils";

interface FailedTestCase {
  moduleName: string;
  caseName: string;
  assertionMsg?: string;
}

interface StoppedTestCase {
  moduleName: string;
  caseName: string;
  assertionMsg?: string;
}

interface TestCompletionModalResultProps {
  isVisible: boolean;
  testPassed: boolean;
  testStopped: boolean;
  failedTestCases?: FailedTestCase[];
  stoppedTestCase?: StoppedTestCase;
  onDismiss: () => void;
  onVisibilityChange?: (isVisible: boolean) => void;
  autoDismissPass?: boolean;
  autoDismissTimeout?: number;
}

/**
 * Compact dialog that reports PASS / FAIL / STOP when a run finishes.
 */
const TestCompletionModalResult: React.FC<TestCompletionModalResultProps> = ({
  isVisible,
  testPassed,
  testStopped,
  failedTestCases = [],
  stoppedTestCase,
  onDismiss,
  onVisibilityChange,
  autoDismissPass = true,
  autoDismissTimeout = 5,
}) => {
  const { t } = useTranslation();
  const [timeLeft, setTimeLeft] = React.useState(autoDismissTimeout);

  React.useEffect(() => {
    onVisibilityChange?.(isVisible);
    if (isVisible) {
      setTimeLeft(autoDismissTimeout);
    }
  }, [isVisible, onVisibilityChange, autoDismissTimeout]);

  React.useEffect(() => {
    if (!(isVisible && testPassed && autoDismissPass)) {
      return;
    }

    setTimeLeft(autoDismissTimeout);

    const countdownTimer = setInterval(() => {
      setTimeLeft((prevTime) => (prevTime <= 1 ? 0 : prevTime - 1));
    }, 1000);

    const dismissTimer = setTimeout(() => {
      onDismiss();
    }, autoDismissTimeout * 1000);

    return () => {
      clearInterval(countdownTimer);
      clearTimeout(dismissTimer);
    };
  }, [isVisible, testPassed, onDismiss, autoDismissPass, autoDismissTimeout]);

  let statusText: string;
  let statusTranslation: string;
  let StatusIcon: typeof CircleCheck;
  let accentClassName: string;

  if (testStopped) {
    statusText = "STOP";
    statusTranslation = t("app.status.stopped");
    StatusIcon = OctagonPause;
    accentClassName = "text-amber-600 dark:text-amber-400";
  } else if (testPassed) {
    statusText = "PASS";
    statusTranslation = t("app.status.passed");
    StatusIcon = CircleCheck;
    accentClassName = "text-emerald-600 dark:text-emerald-400";
  } else {
    statusText = "FAIL";
    statusTranslation = t("app.status.failed");
    StatusIcon = CircleAlert;
    accentClassName = "text-destructive";
  }

  return (
    <Dialog
      open={isVisible}
      onOpenChange={(open) => {
        if (!open) {
          onDismiss();
        }
      }}
    >
      <DialogContent className="sm:max-w-md" showCloseButton={true}>
        <DialogHeader>
          <div className="flex items-center gap-3">
            <StatusIcon className={cn("size-8 shrink-0", accentClassName)} />
            <div className="min-w-0 space-y-1">
              <DialogTitle className={cn("text-2xl", accentClassName)}>
                {statusText}
              </DialogTitle>
              <DialogDescription>{statusTranslation}</DialogDescription>
            </div>
          </div>
        </DialogHeader>

        {testStopped && stoppedTestCase && (
          <div className="max-h-56 space-y-2 overflow-y-auto rounded-md border bg-muted/40 p-3 text-sm">
            <p className="font-medium">{t("app.stoppedTestCase")}</p>
            <div className="space-y-1">
              <p>
                {stoppedTestCase.moduleName} → {stoppedTestCase.caseName}
              </p>
              {stoppedTestCase.assertionMsg && (
                <p className="text-muted-foreground italic">
                  {stoppedTestCase.assertionMsg}
                </p>
              )}
            </div>
          </div>
        )}

        {!testPassed && !testStopped && failedTestCases.length > 0 && (
          <div className="max-h-56 space-y-2 overflow-y-auto rounded-md border bg-muted/40 p-3 text-sm">
            <p className="font-medium">{t("app.failedTestCases")}</p>
            {failedTestCases.map((testCase) => (
              <div
                key={`${testCase.moduleName}-${testCase.caseName}`}
                className="space-y-0.5 border-b border-border/60 pb-2 last:border-0 last:pb-0"
              >
                <p>
                  {testCase.moduleName} → {testCase.caseName}
                </p>
                {testCase.assertionMsg && (
                  <p className="text-muted-foreground italic">
                    {testCase.assertionMsg.split("\n")[0]}
                  </p>
                )}
              </div>
            ))}
          </div>
        )}

        <DialogFooter className="sm:justify-between">
          <p className="text-xs text-muted-foreground">
            {testPassed && autoDismissPass
              ? t("app.modalResultAutoDismissHint", { seconds: timeLeft })
              : t("app.modalResultDismissHint")}
          </p>
          <Button type="button" variant="outline" onClick={onDismiss}>
            {t("button.confirm")}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default TestCompletionModalResult;
