import React, { useState } from 'react';
import { Button, Classes, Dialog, InputGroup } from '@blueprintjs/core';

interface Props {
  title_bar: string;
  dialog_text: string;
  onConfirm?: (inputText: string) => void; 
  width?: string;
  widget_type?: WidgetType;
  widget_text?: string;
}

export type WidgetType = "base" | "textinput" | "radiobutton" | "checkbox" | "numericinput";

export function StartConfirmationDialog(props: Props) {
  const [dialogOpen, setDialogOpen] = useState(true);
  const [inputText, setInputText] = useState('');

  const handleClose = () => {
    setDialogOpen(false);
  };

  const handleConfirm = () => {
    setDialogOpen(false);
    if (props.onConfirm) {
      props.onConfirm(inputText);
    }
  };

  const defaultWidth = '500px';
  const dialogWidth = props.width || defaultWidth;

  const widgetType = props.widget_type || "base";
  const inputPlaceholder = props.widget_text || "widget_text опять не передан";

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