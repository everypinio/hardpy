// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import {
  Button,
  Classes,
  Dialog,
  InputGroup,
  Radio,
  Checkbox,
  Tab,
  Tabs,
} from "@blueprintjs/core";
import { notification } from "antd";

interface Props {
  title_bar: string;
  dialog_text: string;
  onConfirm?: (inputText: string) => void;
  width?: string;
  widget_type?: WidgetType;
  widget_info?: WidgetInfo;
  image_base64?: string;
  image_width?: number;
  image_border?: number;
  is_visible?: boolean;
}

export enum WidgetType {
  Base = "base",
  TextInput = "textinput",
  NumericInput = "numericinput",
  RadioButton = "radiobutton",
  Checkbox = "checkbox",
  Multistep = "multistep",
}

interface ImageComponent {
  base64?: string;
  width?: number;
  border?: number;
}

interface StepWidgetInfo {
  type: string;
  info: WidgetInfo;
}

interface StepInfo {
  title: string;
  text?: string;
  widget?: StepWidgetInfo;
  image?: ImageComponent;
}

interface Step {
  type: string;
  info: StepInfo;
}

interface WidgetInfo {
  fields?: string[];
  text?: string;
  steps?: Step[];
}

export function StartConfirmationDialog(props: Props) {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [inputText, setInputText] = useState("");
  const [selectedRadioButton, setSelectedRadioButton] = useState("");
  const [selectedCheckboxes, setSelectedCheckboxes] = useState<string[]>([]);
  const [imageDimensions, setImageDimensions] = useState({
    width: 0,
    height: 0,
  });
  const [imageStepDimensions, setStepImageDimensions] = useState({
    width: 0,
    height: 0,
  });
  const maxDimensions = useRef({ width: 0, height: 0 });

  const HEX_BASE = 16;

  const widgetType = props.widget_type || WidgetType.Base;
  const inputPlaceholder = "enter answer";

  const screenWidth = window.screen.width;
  const screenHeight = window.screen.height;

  const baseDialogDimensions = { width: 100, height: 100 };
  const maxSize = 0.6;
  const minSize = 0.25;
  const lineHeight = 10;

  const handleClose = () => {
    setDialogOpen(false);
    fetch("api/stop")
      .then((response) => {
        if (response.ok) {
          return response.text();
        } else {
          console.log("Request failed. Status: " + response.status);
        }
      })
      .catch((error) => {
        console.log("Request failed. Error: " + error);
      });
    notification.error({
      message: "Notification",
      description: "The window was closed. Tests stopped.",
    });
  };

  const handleConfirm = async () => {
    if (props.widget_type) {
      switch (props.widget_type) {
        case WidgetType.TextInput:
        case WidgetType.NumericInput:
          if (
            inputText.trim() === "" ||
            inputText === "." ||
            inputText === ".."
          ) {
            alert("The field must not be empty");
            return;
          }
          break;
        case WidgetType.RadioButton:
          if (selectedRadioButton === "") {
            alert("The field must not be empty");
            return;
          }
          break;
        case WidgetType.Checkbox:
          if (selectedCheckboxes.length === 0) {
            alert("The field must not be empty");
            return;
          }
          break;
        default:
          break;
      }
    }
    setDialogOpen(false);
    let textToSend = "";

    function processEncodeURLComponent(str: string) {
      return encodeURIComponent(str).replace(
        /[!-'()*+,/:;<=>?@[\]^`{|}~]/g,
        function (c) {
          return "%" + c.charCodeAt(0).toString(HEX_BASE);
        }
      );
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
          selectedCheckboxes.map((checkboxValue) =>
            processEncodeURLComponent(checkboxValue)
          )
        );
        break;
      default:
        textToSend = "ok";
        break;
    }

    if (props.onConfirm) {
      props.onConfirm(textToSend);
    }
    try {
      const response = await axios.post(
        `/api/confirm_dialog_box/${textToSend}`
      );
      console.log(response.data);
    } catch (error) {
      console.error("Error confirming dialog box:", error);
    }
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      handleConfirm();
    }
  };

  const calculateDimensions = (
    naturalWidth: number,
    naturalHeight: number,
    widthFactor: number
  ) => ({
    width: (naturalWidth * (widthFactor || 100)) / 100,
    height: (naturalHeight * (widthFactor || 100)) / 100,
  });

  const handleImageLoad = (event: React.SyntheticEvent<HTMLImageElement>) => {
    const { naturalWidth, naturalHeight } = event.target as HTMLImageElement;
    setImageDimensions(
      calculateDimensions(naturalWidth, naturalHeight, props.image_width ?? 100)
    );
  };

  const calculateTextLines = (text: string, width: number) => {
    const context = document.createElement("canvas").getContext("2d");
    if (context) {
      context.font = "10px sans-serif";
      const linesCount = Math.ceil(
        (text.length * context.measureText("M").width) / width
      );
      return linesCount;
    }
  };

  const dialogWidth = Math.min(
    (widgetType === WidgetType.Multistep
      ? maxDimensions.current
      : imageDimensions
    ).width + baseDialogDimensions.width,
    screenWidth * maxSize
  );

  const textHeight =
    (calculateTextLines(props.dialog_text, dialogWidth) || 1) * lineHeight;
  const step = props.widget_info?.steps?.[0];
  const textStepHeight = step?.info?.text
    ? (calculateTextLines(step.info.text, dialogWidth) || 1) * lineHeight
    : lineHeight * 2;

  const dialogHeight = Math.max(
    Math.min(
      (widgetType === WidgetType.Multistep
        ? maxDimensions.current.height + baseDialogDimensions.height
        : imageDimensions.height) +
        baseDialogDimensions.height +
        textHeight +
        textStepHeight,
      screenHeight * maxSize
    ),
    screenHeight * minSize
  );

  const imageStyle = {
    border: `${props.image_border || 0}px solid black`,
    display: "block",
    margin: "0 auto",
  };

  useEffect(() => {
    // console.log("AAA "+ props.widget_info);
    // console.log("widgetType "+ widgetType);
    // console.log("props.dialog_text " + props.dialog_text);
    // console.log()

    if (props.is_visible) {
      setDialogOpen(true);
    }

    if (widgetType === WidgetType.Multistep) {
      const handleStepImageLoad = (
        image: HTMLImageElement,
        widthFactor: number
      ) => {
        const { naturalWidth, naturalHeight } = image;

        maxDimensions.current.width = Math.max(
          maxDimensions.current.width,
          naturalWidth * (widthFactor / 100)
        );
        maxDimensions.current.height = Math.max(
          maxDimensions.current.height,
          naturalHeight * (widthFactor / 100)
        );
        setStepImageDimensions(maxDimensions.current);
      };

      props.widget_info?.steps?.forEach((step) => {
        if (step.info.image) {
          const base64Src = `data:image/image;base64,${step.info.image?.base64}`;

          const image = new Image();
          image.src = base64Src;
          image.onload = () =>
            handleStepImageLoad(image, step.info.image?.width || 100);
        }
      });
    }
  }, [props.widget_info, widgetType]);

  return (
    <Dialog
      title={props.title_bar}
      icon="info-sign"
      isOpen={dialogOpen}
      onClose={handleClose}
      canOutsideClickClose={false}
      style={{
        width:
          widgetType === WidgetType.Multistep ? `${dialogWidth}px` : "auto",
        height:
          widgetType === WidgetType.Multistep ? `${dialogHeight}px` : "auto",
        minWidth: screenWidth * minSize,
        minHeight: screenHeight * minSize,
        maxWidth: screenWidth * maxSize,
        maxHeight: screenHeight * maxSize,
        fontSize: "1rem",
      }}
    >
      <div
        className={Classes.DIALOG_BODY}
        style={{
          wordWrap: "break-word",
          wordBreak: "break-word",
          maxHeight: screenHeight * maxSize,
          overflowY: "auto",
          maxWidth: screenWidth * maxSize,
          padding: "10px",
        }}
      >
        {props.dialog_text.split("\n").map((line, index) => (
          <p key={index} style={{ textAlign: "left" }}>
            {line}
          </p>
        ))}
        {widgetType === WidgetType.TextInput && (
          <InputGroup
            value={inputText}
            onChange={(event: React.ChangeEvent<HTMLInputElement>) =>
              setInputText(event.target.value)
            }
            onKeyDown={handleKeyDown}
            placeholder={inputPlaceholder}
            type="text"
            autoFocus={true}
          />
        )}
        {widgetType === WidgetType.NumericInput && (
          <InputGroup
            value={inputText}
            onChange={(event: React.ChangeEvent<HTMLInputElement>) =>
              setInputText(event.target.value)
            }
            onKeyDown={handleKeyDown}
            placeholder={inputPlaceholder}
            type="number"
            autoFocus={true}
          />
        )}

        {widgetType === WidgetType.RadioButton && (
          <>
            {props.widget_info &&
              props.widget_info.fields &&
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
            {props.widget_info &&
              props.widget_info.fields &&
              props.widget_info.fields.map((option: string) => (
                <Checkbox
                  key={option}
                  label={option}
                  checked={selectedCheckboxes.includes(option)}
                  autoFocus={option === (props.widget_info?.fields ?? [])[0]}
                  onChange={() => {
                    if (selectedCheckboxes.includes(option)) {
                      setSelectedCheckboxes(
                        selectedCheckboxes.filter((item) => item !== option)
                      );
                    } else {
                      setSelectedCheckboxes([...selectedCheckboxes, option]);
                    }
                  }}
                />
              ))}
          </>
        )}
        {widgetType === WidgetType.Multistep && (
          <Tabs id={props.title_bar}>
            {props.widget_info?.steps?.map((step: Step) => (
              <Tab
                id={step.info?.title}
                key={step.info?.title}
                title={step.info?.title}
                panel={
                  <div className="step-container">
                    <div className="step-content">
                      {step.info?.text?.split("\n").map((line, index) => (
                        <p key={index} style={{ textAlign: "left" }}>
                          {line}
                        </p>
                      ))}
                      {step.info.image && (
                        <img
                          src={`data:image/image;base64,${step.info.image?.base64}`}
                          alt="Image"
                          style={{
                            maxWidth: `${imageStepDimensions.width + baseDialogDimensions.width}px`,
                            maxHeight: `${imageStepDimensions.height + baseDialogDimensions.height}px`,
                            transform: `scale(${(step.info.image?.width || 100) / 100})`,
                            transformOrigin: `top center`,
                            ...imageStyle,
                          }}
                        />
                      )}
                    </div>
                  </div>
                }
              ></Tab>
            ))}
          </Tabs>
        )}
        <p> </p>
        {props.image_base64 && (
          <div className="image-container">
            <img
              src={`data:image/image;base64,${props.image_base64}`}
              alt="Image"
              onLoad={handleImageLoad}
              style={{
                width: `${props.image_width}%`,
                height: `${props.image_width}%`,
                maxWidth: `${dialogWidth - baseDialogDimensions.width / 2}px`,
                maxHeight: `${dialogHeight - baseDialogDimensions.height / 2}px`,
                objectFit: "scale-down",
                transform: `scale(${(props.image_width || 100) / 100})`,
                transformOrigin: `top center`,
                ...imageStyle,
              }}
            />
          </div>
        )}
      </div>
      <div className={Classes.DIALOG_FOOTER}>
        <Button
          intent="primary"
          onClick={handleConfirm}
          autoFocus={
            widgetType === WidgetType.Base ||
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
