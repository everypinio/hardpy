import React, { useState } from 'react';
import axios from 'axios';
import { Button, Classes, Dialog, InputGroup } from '@blueprintjs/core';


interface Props {
  title_bar: string;
  dialog_text: string;
  onConfirm?: (inputText: string) => void; 
  width?: string;
  widget_type?: WidgetType;
  widget_info?: Record<string, unknown>;
}

export type WidgetType = "base" | "textinput" | "radiobutton" | "checkbox" | "numericinput";

export function StartConfirmationDialog(props: Props) {
  const [dialogOpen, setDialogOpen] = useState(true);
  const [inputText, setInputText] = useState('');

  const handleClose = () => {
    setDialogOpen(false);
  };

  // const handleConfirm = () => {
  //   setDialogOpen(false);
  //   if (props.onConfirm) {
  //     props.onConfirm(inputText);
  //   }
  // };

  const handleConfirm = async () => {
    setDialogOpen(false);
    const textToSend = (props.widget_type === "textinput" || props.widget_type === "numericinput") ? inputText : 'ok';

    if (props.onConfirm) {
      props.onConfirm(textToSend);
    }
    try {
      const response = await axios.post(`/api/confirm_dialog_box/${textToSend}`);
      console.log(response.data);
    } catch (error) {
      console.error('Error confirming dialog box:', error);
    }
  };

  const defaultWidth = '500px';
  const dialogWidth = props.width || defaultWidth;

  const widgetType = props.widget_type || "base";
  const inputPlaceholder = "enter answer";

  return (
    <Dialog
      title={props.title_bar}
      icon="info-sign"
      isOpen={dialogOpen}
      onClose={handleClose}
      style={{ width: dialogWidth }}
    >
      <div className={Classes.DIALOG_BODY}>
        <p>{props.dialog_text}</p>
        {widgetType === "textinput" && (
          <InputGroup
            value={inputText}
            onChange={(event) => setInputText(event.target.value)}
            placeholder={inputPlaceholder}
          />
        )}
        {widgetType === "numericinput" && (
          <InputGroup
            type="number"
            value={inputText}
            onChange={(event) => setInputText(event.target.value)}
            placeholder={inputPlaceholder}
            step="0.01"
          />
        )}
      </div>
      <div className={Classes.DIALOG_FOOTER}>
        <Button intent="primary" onClick={handleConfirm}>
          Confirm
        </Button>
      </div>
    </Dialog>
  );
}

export default StartConfirmationDialog;