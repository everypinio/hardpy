// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import React, { useState, useEffect } from "react";
import { Classes, Dialog } from "@blueprintjs/core";
import axios from "axios";

interface StartOperatorMsgDialogProps {
  title: string;
  msg: string;
}

export function StartOperatorMsgDialog(props: StartOperatorMsgDialogProps) {
  const [dialogOpen, setDialogOpen] = useState(true);

  const handleClose = async () => {
    setDialogOpen(false);
    const isMsgVisible = false;
    try {
      const response = await axios.post(
        `/api/confirm_operator_msg/${JSON.stringify(isMsgVisible)}`
      );
      console.log(response.data);
    } catch (error) {
      console.error("Error confirming dialog box:", error);
    }
  };

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      const keyboardEvent = event as unknown as React.KeyboardEvent<HTMLInputElement>;
      if (keyboardEvent.key === "Escape") {
        handleClose();
      }
    };
  
    window.addEventListener('keydown', handleKeyDown);
  
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  return (
    <Dialog
      title={props.title || "Message"}
      icon="info-sign"
      isOpen={dialogOpen}
      onClose={handleClose}
      canOutsideClickClose={false}
      style={{
        width: "auto",
        height: "auto",
        minWidth: "300px",
        minHeight: "200px",
        maxWidth: "800px",
      }}
    >
      <div
        className={Classes.DIALOG_BODY}
        style={{ wordWrap: "break-word", wordBreak: "break-word" }}
      >
        {props.msg.split("\n").map((line, index) => (
          <p key={index} style={{ textAlign: "left" }}>
            {line}
          </p>
        ))}
      </div>
    </Dialog>
  );
}

export default StartOperatorMsgDialog;
