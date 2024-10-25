// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import React, { useState } from 'react';
import axios from 'axios';
import { Button, Classes, Dialog, InputGroup, Radio, Checkbox, Tab, Tabs } from '@blueprintjs/core';
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
  Image = "image",
  Multistep = "multistep",
}

interface StepWidgetInfo {
  type: string;
  info: WidgetInfo;
}
interface StepInfo {
  title: string;
  text?: string;
  widget?: StepWidgetInfo;
}

interface Step {
  type: string;
  info: StepInfo;
}

interface WidgetInfo {
  fields?: string[];
  text?: string;
  base64?: string;
  format?: string;
  width?: number;
  steps?: Step[];
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
          if (inputText.trim() === '' || inputText === '.' || inputText === '..') {
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
    const HEX_BASE = 16;

    function processEncodeURLComponent(str: string) {
      return encodeURIComponent(str).replace(/[!-'()*+,/:;<=>?@[\]^`{|}~]/g, function (c) {
        return '%' + c.charCodeAt(0).toString(HEX_BASE);
      });
    }

    switch (props.widget_type) {
      case WidgetType.TextInput:
        textToSend = processEncodeURLComponent(inputText);
        break;
      case WidgetType.NumericInput:
        textToSend = inputText;
        break;
      case WidgetType.RadioButton:
        textToSend = processEncodeURLComponent(selectedRadioButton);
        break;
      case WidgetType.Checkbox:
        textToSend = JSON.stringify(
          selectedCheckboxes.map(checkboxValue => processEncodeURLComponent(checkboxValue))
        );
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

  const widgetType = props.widget_type || WidgetType.Base;
  const inputPlaceholder = "enter answer";

  return (
    <Dialog
      title={props.title_bar}
      icon="info-sign"
      isOpen={dialogOpen}
      onClose={handleClose}
      canOutsideClickClose={false}
      style={{
        width: 'auto',
        height: 'auto',
        minWidth: '300px',
        minHeight: '200px',
        maxWidth: '1000px',
        maxHeight: '800px',
      }}
    >
      <div className={Classes.DIALOG_BODY} style={{ wordWrap: 'break-word', wordBreak: 'break-word' }}>
        <p style={{ textAlign: 'left' }}>{props.dialog_text}</p>
        {widgetType === WidgetType.TextInput && (
          <InputGroup
            value={inputText}
            onChange={(event: React.ChangeEvent<HTMLInputElement>) => setInputText(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={inputPlaceholder}
            type="text"
            autoFocus={true}
          />
        )}
        {widgetType === WidgetType.NumericInput && (
          <InputGroup
            value={inputText}
            onChange={(event: React.ChangeEvent<HTMLInputElement>) => setInputText(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={inputPlaceholder}
            type="number"
            autoFocus={true}
          />
        )}
        {widgetType === WidgetType.RadioButton && (
          <>
            {props.widget_info && props.widget_info.fields &&
              props.widget_info.fields.map((option: string) => (
                <Radio
                  key={option}
                  label={option}
                  checked={selectedRadioButton === option}
                  onChange={() => setSelectedRadioButton(option)}
                  autoFocus={option === (props.widget_info?.fields ?? [])[0]}
                />
              ))}
          </>
        )}
        {widgetType === WidgetType.Checkbox && (
          <>
            {props.widget_info && props.widget_info.fields &&
              props.widget_info.fields.map((option: string) => (
                <Checkbox
                  key={option}
                  label={option}
                  checked={selectedCheckboxes.includes(option)}
                  autoFocus={option === (props.widget_info?.fields ?? [])[0]}
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
          <div className="image-container">
            <img
              src={`data:image/${props.widget_info?.format};base64,${props.widget_info?.base64}`}
              alt="Image"
              style={{ width: props.widget_info?.width && props.widget_info.width <= 800 ? `${props.widget_info.width}%` : 'auto', height: 'auto', display: 'block', margin: '0 auto' }}
            />
          </div>
        )}
        {widgetType === WidgetType.Multistep && (
          <Tabs id={props.title_bar}>
            {props.widget_info?.steps?.map((step: Step) => (
              <Tab
                id={step.info?.title}
                key={step.info?.title}
                title={step.info?.title}
                panel={
                  <div className="step-container" >
                    <div className="step-content" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', flex: 1 }}>
                      <p>{step.info?.text}</p>
                      {step.info?.widget?.type === WidgetType.Image && (
                        <img
                          src={`data:image/${step.info.widget?.info.format};base64,${step.info.widget?.info.base64}`}
                          alt="Image"
                          style={{ width: `${step.info.widget?.info.width}%` || 'auto', height: 'auto', display: 'block', margin: '0 auto' }}
                        />
                      )}
                    </div>
                  </div>}
              >
              </Tab>
            ))}
          </Tabs>
        )}
      </div>
      <div className={Classes.DIALOG_FOOTER}>
        <Button
          intent="primary"
          onClick={handleConfirm}
          autoFocus={
            widgetType === WidgetType.Base ||
            widgetType === WidgetType.Image ||
            widgetType === WidgetType.Multistep
          }
        >
          Confirm
        </Button>
      </div>
    </Dialog>
  );
}

export default StartConfirmationDialog;
