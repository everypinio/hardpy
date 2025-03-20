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
  id?: string;
  font_size?: number;
  html_url?: string;
  html_code?: string;
  html_width?: number;
  html_border?: number;
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

interface HTMLComponent {
  code_or_url?: string;
  is_raw_html?: boolean;
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
  html?: HTMLComponent;
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

interface TextInputComponentProps {
  inputText: string;
  setInputText: (value: string) => void;
  handleKeyDown: (event: React.KeyboardEvent) => void;
  inputPlaceholder: string;
  type: string;
}

interface RadioButtonComponentProps {
  fields: string[];
  selectedRadioButton: string;
  setSelectedRadioButton: (value: string) => void;
  handleKeyDown: (event: React.KeyboardEvent) => void;
  fontSize: number;
}

interface CheckboxComponentProps {
  fields: string[]; // Add this line
  selectedCheckboxes: string[];
  setSelectedCheckboxes: (value: string[]) => void;
  handleKeyDown: (event: React.KeyboardEvent) => void;
  fontSize: number;
}

/**
 * TextInputComponent is a reusable input component that allows users to enter text.
 * @param {string} inputText - The current value of the input field.
 * @returns {JSX.Element} - A controlled input component with auto-focus enabled.
 */
const TextInputComponent = ({
  inputText,
  setInputText,
  handleKeyDown,
  inputPlaceholder,
  type,
}: TextInputComponentProps): JSX.Element => (
  <InputGroup
    value={inputText}
    onChange={(event: React.ChangeEvent<HTMLInputElement>) =>
      setInputText(event.target.value)
    }
    onKeyDown={handleKeyDown}
    placeholder={inputPlaceholder}
    type={type}
    autoFocus={true}
  />
);

/**
 * RadioButtonComponent is a reusable component that renders a group of radio buttons.
 * @param {string[]} fields - An array of options to display as radio buttons.
 * @param {function} setSelectedRadioButton - A function to update the selected radio button.
 * @param {function} handleKeyDown - A function to handle keydown events on the radio buttons.
 * @param {number} fontSize - The font size for the radio button labels.
 * @returns {JSX.Element} - A group of radio buttons with dynamic styling and auto-focus on the first option.
 */
/** */
const RadioButtonComponent = ({
  fields,
  selectedRadioButton,
  setSelectedRadioButton,
  handleKeyDown,
  fontSize,
}: RadioButtonComponentProps): JSX.Element => (
  <>
    {fields?.map((option: string) => (
      <Radio
        key={option}
        label={option}
        checked={selectedRadioButton === option}
        onChange={() => setSelectedRadioButton(option)}
        onKeyDown={handleKeyDown}
        style={{ fontSize: `${fontSize}px` }}
        autoFocus={option === fields[0]}
      />
    ))}
  </>
);

/**
 * CheckboxComponent is a reusable component that renders a group of checkboxes.
 *
 * @param {string[]} fields - An array of options to display as checkboxes.
 * @param {string[]} selectedCheckboxes - An array of currently selected checkbox values.
 * @param {function} setSelectedCheckboxes - A function to update the selected checkboxes.
 * @param {function} handleKeyDown - A function to handle keydown events on the checkboxes.
 * @param {number} fontSize - The font size for the checkbox labels.
 * @returns {JSX.Element} - A group of checkboxes with dynamic styling and auto-focus on the first option.
 */
/** */
const CheckboxComponent = ({
  fields,
  selectedCheckboxes,
  setSelectedCheckboxes,
  handleKeyDown,
  fontSize,
}: CheckboxComponentProps): JSX.Element => (
  <>
    {fields?.map((option: string) => (
      <Checkbox
        key={option}
        label={option}
        checked={selectedCheckboxes.includes(option)}
        autoFocus={option === fields[0]}
        onKeyDown={handleKeyDown}
        style={{ fontSize: `${fontSize}px` }}
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
);

/**
 * StartConfirmationDialog is a React component that renders a dialog box with various types of input widgets.
 * It supports text input, numeric input, radio buttons, checkboxes, and multi-step forms.
 *
 * @param {Props} props - The properties passed to the component.
 * @returns {JSX.Element} - The rendered dialog box.
 */
export function StartConfirmationDialog(props: Readonly<Props>): JSX.Element {
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

  const widgetType = props.widget_type ?? WidgetType.Base;
  const inputPlaceholder = "enter answer";

  const screenWidth = window.screen.width;
  const screenHeight = window.screen.height;

  const baseDialogDimensions = { width: 100, height: 100 };
  const maxSize = 0.8;
  const minSize = 0.25;
  const htmlHeightIndex = 0.75;
  const htmlWidthIndex = 0.9;
  const lineHeight = (10 * (props.font_size ? props.font_size : 14)) / 14;

  /**
   * Handles the close event of the dialog box.
   * Sends a request to stop the tests and displays a notification.
   */
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

  /**
   * Handles the confirm event of the dialog box.
   * Validates the input and sends the confirmed data to the server.
   */
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

    /**
     * Encodes a URL component, replacing special characters with their hexadecimal equivalents.
     *
     * @param {string} str - The string to encode.
     * @returns {string} - The encoded string.
     */
    function processEncodeURLComponent(str: string): string {
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

  /**
   * Handles keydown events for the dialog box.
   *
   * @param {React.KeyboardEvent} event - The keyboard event.
   */
  const handleKeyDown = (event: React.KeyboardEvent) => {
    const key = event.key;

    if (key === "Enter") {
      handleConfirm();
      return;
    }

    if (props.widget_info?.fields) {
      handleWidgetKeyDown(key);
    }
  };

  /**
   * Handles keydown events for widget-specific actions.
   *
   * @param {string} key - The key that was pressed.
   */
  const handleWidgetKeyDown = (key: string) => {
    const index = findFieldIndexByKey(key);

    if (index >= 0) {
      if (widgetType === WidgetType.RadioButton) {
        handleRadioButtonKeyDown(index);
      } else if (widgetType === WidgetType.Checkbox) {
        handleCheckboxKeyDown(index);
      }
    }
  };

  /**
   * Finds the index of the field that starts with the given key.
   *
   * @param {string} key - The key to search for.
   * @returns {number} The index of the field, or -1 if not found.
   */
  const findFieldIndexByKey = (key: string): number => {
    return (
      props.widget_info?.fields?.findIndex((option) =>
        option.startsWith(key)
      ) ?? -1
    );
  };

  /**
   * Handles keydown events for RadioButton widget.
   *
   * @param {number} index - The index of the selected field.
   */
  const handleRadioButtonKeyDown = (index: number) => {
    if (props.widget_info?.fields) {
      setSelectedRadioButton(props.widget_info.fields[index]);
    }
  };

  /**
   * Handles keydown events for Checkbox widget.
   *
   * @param {number} index - The index of the selected field.
   */
  const handleCheckboxKeyDown = (index: number) => {
    if (props.widget_info?.fields) {
      const option = props.widget_info.fields[index];
      if (selectedCheckboxes.includes(option)) {
        setSelectedCheckboxes(
          selectedCheckboxes.filter((item) => item !== option)
        );
      } else {
        setSelectedCheckboxes([...selectedCheckboxes, option]);
      }
    }
  };

  /**
   * Calculates the dimensions of an image based on its natural dimensions and a width factor.
   *
   * @param {number} naturalWidth - The natural width of the image.
   * @param {number} naturalHeight - The natural height of the image.
   * @param {number} widthFactor - The width factor to scale the image by.
   * @returns {{width: number, height: number}} - The calculated dimensions.
   */
  const calculateDimensions = (
    naturalWidth: number,
    naturalHeight: number,
    widthFactor: number
  ): { width: number; height: number } => ({
    width: (naturalWidth * (widthFactor || 100)) / 100,
    height: (naturalHeight * (widthFactor || 100)) / 100,
  });

  /**
   * Handles the load event of an image, calculating its dimensions and updating the state.
   *
   * @param {React.SyntheticEvent<HTMLImageElement>} event - The image load event.
   */
  const handleImageLoad = (event: React.SyntheticEvent<HTMLImageElement>) => {
    const { naturalWidth, naturalHeight } = event.target as HTMLImageElement;
    setImageDimensions(
      calculateDimensions(naturalWidth, naturalHeight, props.image_width ?? 100)
    );
  };

  /**
   * Calculates the number of text lines required to display a given text within a specified width.
   *
   * @param {string} text - The text to measure.
   * @param {number} width - The width within which the text should fit.
   * @returns {number} - The number of lines required.
   */
  const calculateTextLines = (
    text: string,
    width: number
  ): number | undefined => {
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
    (calculateTextLines(props.dialog_text, dialogWidth) ?? 1) * lineHeight;
  const step = props.widget_info?.steps?.[0];
  const textStepHeight = step?.info?.text
    ? (calculateTextLines(step.info.text, dialogWidth) ?? 1) * lineHeight
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
    border: `${props.image_border ?? 0}px solid black`,
    display: "block",
    margin: "0 auto",
  };

  useEffect(() => {
    if (props.is_visible) {
      setDialogOpen(true);
    }
  }, [props.is_visible, props.id]);

  useEffect(() => {
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
            handleStepImageLoad(image, step.info.image?.width ?? 100);
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
        fontSize: `${props.font_size}px`,
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
        {props.dialog_text.split("\n").map((line) => (
          <p key={line.trim()} style={{ textAlign: "left" }}>
            {line}
          </p>
        ))}
        {widgetType === WidgetType.TextInput && (
          <TextInputComponent
            inputText={inputText}
            setInputText={setInputText}
            handleKeyDown={handleKeyDown}
            inputPlaceholder={inputPlaceholder}
            type="text"
          />
        )}
        {widgetType === WidgetType.NumericInput && (
          <TextInputComponent
            inputText={inputText}
            setInputText={setInputText}
            handleKeyDown={handleKeyDown}
            inputPlaceholder={inputPlaceholder}
            type="number"
          />
        )}
        {widgetType === WidgetType.RadioButton && (
          <RadioButtonComponent
            fields={props.widget_info?.fields ?? []}
            selectedRadioButton={selectedRadioButton}
            setSelectedRadioButton={setSelectedRadioButton}
            handleKeyDown={handleKeyDown}
            fontSize={props.font_size ?? 12}
          />
        )}
        {widgetType === WidgetType.Checkbox && (
          <CheckboxComponent
            fields={props.widget_info?.fields ?? []}
            selectedCheckboxes={selectedCheckboxes}
            setSelectedCheckboxes={setSelectedCheckboxes}
            handleKeyDown={handleKeyDown}
            fontSize={props.font_size ?? 12}
          />
        )}
        {widgetType === WidgetType.Multistep && (
          <Tabs id={props.title_bar}>
            {props.widget_info?.steps?.map((step: Step) => (
              <Tab
                id={step.info?.title}
                key={step.info?.title}
                title={step.info?.title}
                style={{ fontSize: `${props.font_size}px` }}
                panel={
                  <div className="step-container">
                    <div className="step-content">
                      {step.info?.text?.split("\n").map((line) => (
                        <p key={line} style={{ textAlign: "left" }}>
                          {line}
                        </p>
                      ))}
                      {step.info.image && (
                        <img
                          src={`data:image/image;base64,${step.info.image?.base64}`}
                          alt={""}
                          style={{
                            maxWidth: `${imageStepDimensions.width + baseDialogDimensions.width}px`,
                            maxHeight: `${imageStepDimensions.height + baseDialogDimensions.height}px`,
                            transform: `scale(${(step.info.image?.width ?? 100) / 100})`,
                            transformOrigin: `top center`,
                            ...imageStyle,
                          }}
                        />
                      )}
                      {step.info.html?.code_or_url &&
                        step.info.html?.is_raw_html && (
                          <iframe
                            srcDoc={step.info.html?.code_or_url}
                            height={
                              (imageStepDimensions.height +
                                baseDialogDimensions.height) *
                              htmlHeightIndex *
                              ((step.info.html?.width ?? 100) / 100)
                            }
                            width={
                              (imageStepDimensions.width +
                                baseDialogDimensions.width) *
                              htmlWidthIndex *
                              ((step.info.html?.width ?? 100) / 100)
                            }
                            style={{
                              border: step.info.html?.border
                                ? `${step.info.html?.border}px solid black`
                                : "none",
                            }}
                            title="HTML Code"
                          />
                        )}
                      {step.info.html?.code_or_url &&
                        !step.info.html?.is_raw_html && (
                          <iframe
                            src={step.info.html?.code_or_url}
                            height={
                              (imageStepDimensions.height +
                                baseDialogDimensions.height) *
                              htmlHeightIndex *
                              ((step.info.html?.width ?? 100) / 100)
                            }
                            width={
                              (imageStepDimensions.width +
                                baseDialogDimensions.width) *
                              htmlWidthIndex *
                              ((step.info.html?.width ?? 100) / 100)
                            }
                            style={{
                              border: `${step.info.html?.border ?? 0}px solid black`,
                            }}
                            title="HTML Link"
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
              alt={""}
              onLoad={handleImageLoad}
              style={{
                width: `${props.image_width}%`,
                height: `${props.image_width}%`,
                maxWidth: `${dialogWidth - baseDialogDimensions.width / 2}px`,
                maxHeight: `${dialogHeight - baseDialogDimensions.height / 2}px`,
                objectFit: "scale-down",
                transform: `scale(${(props.image_width ?? 100) / 100})`,
                transformOrigin: `top center`,
                ...imageStyle,
              }}
            />
          </div>
        )}
        {props.html_code && (
          <iframe
            srcDoc={props.html_code}
            height={
              screenHeight *
              maxSize *
              htmlHeightIndex *
              ((props.html_width ?? 100) / 100)
            }
            width={
              screenWidth *
              maxSize *
              htmlWidthIndex *
              ((props.html_width ?? 100) / 100)
            }
            style={{
              border: `${props.html_border ?? 0}px solid black`,
            }}
            title="HTML Code"
          />
        )}
        {props.html_url && (
          <iframe
            src={props.html_url}
            height={
              screenHeight *
              maxSize *
              htmlHeightIndex *
              ((props.html_width ?? 100) / 100)
            }
            width={
              screenWidth *
              maxSize *
              htmlWidthIndex *
              ((props.html_width ?? 100) / 100)
            }
            style={{
              border: `${props.html_border ?? 0}px solid black`,
            }}
            title="HTML Link"
          />
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
