// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import React, { useState } from 'react';
import axios from 'axios';
import { Button, Classes, Dialog, InputGroup, Radio, Checkbox } from '@blueprintjs/core';
import { notification } from 'antd';

interface Props {
  title_bar: string;
  dialog_text: string;
  onConfirm?: (inputText: string) => void;
  width?: string;
  widget_type?: WidgetType;
  widget_info?: WidgetInfo;
}

export enum WidgetType {
  Base = "base",
  TextInput = "textinput",
  NumericInput = "numericinput",
  RadioButton = "radiobutton",
  Checkbox = "checkbox",
  Image = "image"
}

interface WidgetInfo {
  options?: string[];
  text?: string;
  image_base64?: string;
  image_format?: string;
}

export function StartConfirmationDialog(props: Props) {
  const [dialogOpen, setDialogOpen] = useState(true);
  const [inputText, setInputText] = useState('');
  const [selectedRadioButton, setSelectedRadioButton] = useState('');
  const [selectedCheckboxes, setSelectedCheckboxes] = useState<string[]>([]);

  const handleClose = () => {
    setDialogOpen(false);
    fetch('api/stop')
      .then(response => {
        if (response.ok) {
          return response.text();
        } else {
          console.log("Request failed. Status: " + response.status);
        }
      })
      .catch(error => {
        console.log("Request failed. Error: " + error);
      });
    notification.error({
      message: 'Notification',
      description: 'The window was closed. Tests stopped.',
    });
  };

  const handleConfirm = async () => {
    if (props.widget_type) {
      switch (props.widget_type) {
        case WidgetType.TextInput:
        case WidgetType.NumericInput:
          if (inputText.trim() === '') {
            alert('The field must not be empty');
            return;
          }
          break;
        case WidgetType.RadioButton:
          if (selectedRadioButton === '') {
            alert('The field must not be empty');
            return;
          }
          break;
        case WidgetType.Checkbox:
          if (selectedCheckboxes.length === 0) {
            alert('The field must not be empty');
            return;
          }
          break;
        default:
          break;
      }
    }
    setDialogOpen(false);
    let textToSend = '';

    switch (props.widget_type) {
      case WidgetType.TextInput:
      case WidgetType.NumericInput:
        textToSend = inputText;
        break;
      case WidgetType.RadioButton:
        textToSend = selectedRadioButton;
        break;
      case WidgetType.Checkbox:
        textToSend = JSON.stringify(selectedCheckboxes);
        break;
      default:
        textToSend = 'ok';
        break;
    }

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

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      handleConfirm();
    }
  };

  const defaultWidth = '500px';
  const dialogWidth = props.width || defaultWidth;

  const widgetType = props.widget_type || WidgetType.Base;
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
        {widgetType === WidgetType.TextInput && (
          <InputGroup
            value={inputText}
            onChange={(event) => setInputText(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={inputPlaceholder}
            type="text"
            autoFocus={true}
          />
        )}
        {widgetType === WidgetType.NumericInput && (
          <InputGroup
            value={inputText}
            onChange={(event) => setInputText(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={inputPlaceholder}
            type="number"
            autoFocus={true}
          />
        )}
        {widgetType === WidgetType.RadioButton && (
          <>
            {props.widget_info && props.widget_info.options && props.widget_info.options.map((option: string) => (
              <Radio
                key={option}
                label={option}
                checked={selectedRadioButton === option}
                onChange={() => setSelectedRadioButton(option)}
              />
            ))}
          </>
        )}
        {widgetType === WidgetType.Checkbox && (
          <>
            {props.widget_info && props.widget_info.options && props.widget_info.options.map((option: string) => (
              <Checkbox
                key={option}
                label={option}
                checked={selectedCheckboxes.includes(option)}
                onChange={() => {
                  if (selectedCheckboxes.includes(option)) {
                    setSelectedCheckboxes(selectedCheckboxes.filter(item => item !== option));
                  } else {
                    setSelectedCheckboxes([...selectedCheckboxes, option]);
                  }
                }}
              />
            ))}
          </>
        )}
        {widgetType === WidgetType.Image && (
          <img src={`data:image/${props.widget_info?.image_format};base64,${props.widget_info?.image_base64}`} alt="Image" style={{ width: '100%' }} />
        )}
      </div>
      <div className={Classes.DIALOG_FOOTER}>
        <Button
          intent="primary"
          onClick={handleConfirm}
          autoFocus={widgetType === WidgetType.Base}
        >
          Confirm
        </Button>
      </div>
    </Dialog>
  );
}

export default StartConfirmationDialog;
