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
import {
  BASE_DIALOG_DIMENSIONS,
  MAX_SIZE_FACTOR,
  MIN_SIZE_FACTOR,
  LINE_HEIGHT_FACTOR,
  BASE_FONT_SIZE,
  HTML_IFRAME_SCALE_FACTOR,
  HTML_IFRAME_WIDTH_FACTOR,
  IMAGE_SCALE_FACTOR,
  calculateDialogDimensions,
} from "./DialogUtils";
import { useTranslation } from "react-i18next";

const HEX_BASE = 16;
const screenWidth = window.screen.width;
const screenHeight = window.screen.height;
const PHONE_SCALE_FACTOR = 0.8;
const MONITOR_SCALE_FACTOR = 0.6;

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
  language?: string;
  pass_fail?: boolean;
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
  inputPlaceholder?: string;
  type: string;
  passFail?: boolean;
  onEnterPress?: () => void;
}

interface RadioButtonComponentProps {
  fields: string[];
  selectedRadioButton: string;
  setSelectedRadioButton: (value: string) => void;
  handleKeyDown: (event: React.KeyboardEvent) => void;
  fontSize: number;
  passFail?: boolean;
  onEnterPress?: () => void;
}

interface CheckboxComponentProps {
  fields: string[];
  selectedCheckboxes: string[];
  setSelectedCheckboxes: (value: string[]) => void;
  handleKeyDown: (event: React.KeyboardEvent) => void;
  fontSize: number;
  passFail?: boolean;
  onEnterPress?: () => void;
}

/**
 * TextInputComponent is a reusable input component that allows users to enter text.
 * When `pass_fail` is enabled and Enter is pressed, it prevents default submission
 * and focuses the "Pass" button without triggering it.
 *
 * @param {string} inputText - The current value of the input field.
 * @param {function} setInputText - A function to update the input field value.
 * @param {function} handleKeyDown - A function to handle keydown events on the input field.
 * @param {string} inputPlaceholder - The placeholder text to display in the input field.
 * @param {string} type - The type of the input field.
 * @param {boolean} passFail - Whether pass/fail buttons are enabled.
 * @param {function} onEnterPress - Callback to focus the "Pass" button (not trigger it).
 * @returns {JSX.Element} - A controlled input component with auto-focus enabled.
 */
const TextInputComponent = ({
  inputText,
  setInputText,
  handleKeyDown,
  inputPlaceholder,
  type,
  passFail: pass_fail,
  onEnterPress,
}: TextInputComponentProps): JSX.Element => {
  const handleKeyDownWithFocus = (event: React.KeyboardEvent) => {
    if (pass_fail && event.key === "Enter") {
      event.preventDefault(); // Prevent form submission or default behavior
      onEnterPress?.(); // Only focus the "Pass" button, do NOT trigger it
    } else {
      handleKeyDown(event);
    }
  };

  return (
    <InputGroup
      value={inputText}
      onChange={(event: React.ChangeEvent<HTMLInputElement>) =>
        setInputText(event.target.value)
      }
      onKeyDown={handleKeyDownWithFocus}
      placeholder={inputPlaceholder}
      type={type}
      autoFocus={true}
    />
  );
};

/**
 * RadioButtonComponent renders a group of radio buttons.
 * When `pass_fail` is enabled and Enter is pressed, it focuses the "Pass" button
 * without submitting or selecting anything automatically.
 *
 * @param {string[]} fields - An array of options to display as radio buttons.
 * @param {string} selectedRadioButton - The currently selected radio button value.
 * @param {function} setSelectedRadioButton - A function to update the selected radio button.
 * @param {function} handleKeyDown - A function to handle keydown events on the radio buttons.
 * @param {number} fontSize - The font size for the radio button labels.
 * @param {boolean} passFail - Whether pass/fail mode is active.
 * @param {function} onEnterPress - Callback to focus "Pass" button on Enter.
 * @returns {JSX.Element} - A group of radio buttons with dynamic styling and auto-focus on the first option.
 */
const RadioButtonComponent = ({
  fields,
  selectedRadioButton,
  setSelectedRadioButton,
  handleKeyDown,
  fontSize,
  passFail: pass_fail,
  onEnterPress,
}: RadioButtonComponentProps): JSX.Element => {
  const handleKeyDownWithFocus = (event: React.KeyboardEvent) => {
    if (pass_fail && event.key === "Enter") {
      event.preventDefault();
      onEnterPress?.();
    } else {
      handleKeyDown(event);
    }
  };

  return (
    <>
      {fields?.map((option: string) => (
        <Radio
          key={option}
          label={option}
          checked={selectedRadioButton === option}
          onChange={() => setSelectedRadioButton(option)}
          onKeyDown={handleKeyDownWithFocus}
          style={{ fontSize: `${fontSize}px` }}
          autoFocus={option === fields[0]}
        />
      ))}
    </>
  );
};

/**
 * CheckboxComponent is a reusable component that renders a group of checkboxes.
 * When `pass_fail` is enabled and Enter is pressed, it focuses the "Pass" button
 * without triggering any action.
 *
 * @param {string[]} fields - An array of options to display as checkboxes.
 * @param {string[]} selectedCheckboxes - An array of currently selected checkbox values.
 * @param {function} setSelectedCheckboxes - A function to update the selected checkboxes.
 * @param {function} handleKeyDown - A function to handle keydown events on the checkboxes.
 * @param {number} fontSize - The font size for the checkbox labels.
 * @param {boolean} passFail - Whether pass/fail mode is active.
 * @param {function} onEnterPress - Callback to focus "Pass" button on Enter.
 * @returns {JSX.Element} - A group of checkboxes with dynamic styling and auto-focus on the first option.
 */
const CheckboxComponent = ({
  fields,
  selectedCheckboxes,
  setSelectedCheckboxes,
  handleKeyDown,
  fontSize,
  passFail: pass_fail,
  onEnterPress,
}: CheckboxComponentProps): JSX.Element => {
  const handleKeyDownWithFocus = (event: React.KeyboardEvent) => {
    if (pass_fail && event.key === "Enter") {
      event.preventDefault();
      onEnterPress?.();
    } else {
      handleKeyDown(event);
    }
  };

  return (
    <>
      {fields?.map((option: string) => (
        <Checkbox
          key={option}
          label={option}
          checked={selectedCheckboxes.includes(option)}
          autoFocus={option === fields[0]}
          onKeyDown={handleKeyDownWithFocus}
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
};

/**
 * Renders a text input component.
 * @param {Props} props - The properties passed to the component.
 * @param {string} inputText - The current value of the input field.
 * @param {function} setInputText - A function to update the value of the input field.
 * @param {function} handleKeyDown - A function to handle keydown events on the input field.
 * @returns {JSX.Element} - A text input component with specified properties.
 */
const renderTextInput = (
  props: Props,
  inputText: string,
  setInputText: (value: string) => void,
  handleKeyDown: (event: React.KeyboardEvent) => void,
  t: (key: string) => string,
  onEnterPress?: () => void
): JSX.Element => (
  <TextInputComponent
    inputText={inputText}
    setInputText={setInputText}
    handleKeyDown={handleKeyDown}
    inputPlaceholder={t("operatorDialog.enterAnswer")}
    type="text"
    passFail={props.pass_fail}
    onEnterPress={onEnterPress}
  />
);

/**
 * Renders a numeric input component.
 * @param {Props} props - The properties passed to the component.
 * @param {string} inputText - The current value of the input field.
 * @param {function} setInputText - A function to update the value of the input field.
 * @param {function} handleKeyDown - A function to handle keydown events on the input field.
 * @returns {JSX.Element} - A numeric input component with specified properties.
 */
const renderNumericInput = (
  props: Props,
  inputText: string,
  setInputText: (value: string) => void,
  handleKeyDown: (event: React.KeyboardEvent) => void,
  t: (key: string) => string,
  onEnterPress?: () => void
): JSX.Element => (
  <TextInputComponent
    inputText={inputText}
    setInputText={setInputText}
    handleKeyDown={handleKeyDown}
    inputPlaceholder={t("operatorDialog.enterAnswer")}
    type="number"
    passFail={props.pass_fail}
    onEnterPress={onEnterPress}
  />
);

/**
 * Renders a radio button component.
 * @param {Props} props - The properties passed to the component.
 * @param {string} selectedRadioButton - The currently selected radio button.
 * @param {function} setSelectedRadioButton - A function to update the selected radio button.
 * @param {function} handleKeyDown - A function to handle keydown events on the radio buttons.
 * @returns {JSX.Element} - A radio button component with specified properties.
 */
const renderRadioButton = (
  props: Props,
  selectedRadioButton: string,
  setSelectedRadioButton: (value: string) => void,
  handleKeyDown: (event: React.KeyboardEvent) => void,
  onEnterPress?: () => void
): JSX.Element => (
  <RadioButtonComponent
    fields={props.widget_info?.fields ?? []}
    selectedRadioButton={selectedRadioButton}
    setSelectedRadioButton={setSelectedRadioButton}
    handleKeyDown={handleKeyDown}
    fontSize={props.font_size ?? 12}
    passFail={props.pass_fail}
    onEnterPress={onEnterPress}
  />
);

/**
 * Renders a checkbox component.
 * @param {Props} props - The properties passed to the component.
 * @param {string[]} selectedCheckboxes - An array of currently selected checkbox values.
 * @param {function} setSelectedCheckboxes - A function to update the selected checkboxes.
 * @param {function} handleKeyDown - A function to handle keydown events on the checkboxes.
 * @returns {JSX.Element} - A checkbox component with specified properties.
 */
const renderCheckbox = (
  props: Props,
  selectedCheckboxes: string[],
  setSelectedCheckboxes: (value: string[]) => void,
  handleKeyDown: (event: React.KeyboardEvent) => void,
  onEnterPress?: () => void
): JSX.Element => (
  <CheckboxComponent
    fields={props.widget_info?.fields ?? []}
    selectedCheckboxes={selectedCheckboxes}
    setSelectedCheckboxes={setSelectedCheckboxes}
    handleKeyDown={handleKeyDown}
    fontSize={props.font_size ?? 12}
    passFail={props.pass_fail}
    onEnterPress={onEnterPress}
  />
);

/**
 * Renders an HTML code iframe.
 * @param {string} htmlCode - The HTML code to render.
 * @param {number} height - The height of the iframe.
 * @param {number} width - The width of the iframe.
 * @param {number} border - The border size of the iframe.
 * @returns {JSX.Element} - An iframe element with the specified HTML code.
 */
const renderHTMLCode = (
  htmlCode: string,
  height: number,
  width: number,
  border: number,
  t: (key: string) => string
): JSX.Element => (
  <iframe
    srcDoc={htmlCode}
    height={height}
    width={width}
    style={{
      border: `${border}px solid black`,
    }}
    title={t("operatorDialog.htmlCodeTitle")}
  />
);

/**
 * Renders an HTML link iframe.
 * @param {string} htmlUrl - The URL to render.
 * @param {number} height - The height of the iframe.
 * @param {number} width - The width of the iframe.
 * @param {number} border - The border size of the iframe.
 * @returns {JSX.Element} - An iframe element with the specified URL.
 */
const renderHTMLLink = (
  htmlUrl: string,
  height: number,
  width: number,
  border: number,
  t: (key: string) => string
): JSX.Element => (
  <iframe
    src={htmlUrl}
    height={height}
    width={width}
    style={{
      border: `${border}px solid black`,
    }}
    title={t("operatorDialog.htmlLinkTitle")}
  />
);

/**
 * Renders a multistep component with tabs, each containing text, images, or HTML content.
 * @param {Props} props - The properties passed to the component.
 * @param {Object} imageStepDimensions - The dimensions of the image step.
 * @param {Object} baseDialogDimensions - The base dimensions of the dialog.
 * @param {number} htmlHeightIndex - The height index for HTML content.
 * @param {number} htmlWidthIndex - The width index for HTML content.
 * @param {React.CSSProperties} imageStyle - The style properties for the image.
 * @returns {JSX.Element} - A multistep component with tabs containing various content types.
 */
const renderMultistep = (
  props: Props,
  imageStepDimensions: { width: number; height: number },
  baseDialogDimensions: { width: number; height: number },
  htmlHeightIndex: number,
  htmlWidthIndex: number,
  imageStyle: React.CSSProperties,
  maxSizeFactor: number,
  t: (key: string) => string
): JSX.Element => (
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
                    maxWidth: `${Math.min(
                      imageStepDimensions.width + baseDialogDimensions.width,
                      screenWidth * maxSizeFactor
                    )}px`,
                    maxHeight: `${Math.min(
                      imageStepDimensions.height + baseDialogDimensions.height,
                      screenHeight * maxSizeFactor
                    )}px`,
                    transform: `scale(${(step.info.image?.width ?? IMAGE_SCALE_FACTOR) / IMAGE_SCALE_FACTOR})`,
                    transformOrigin: `top center`,
                    ...imageStyle,
                  }}
                />
              )}
              {step.info.html?.code_or_url &&
                step.info.html?.is_raw_html &&
                renderHTMLCode(
                  step.info.html.code_or_url,
                  Math.min(
                    (imageStepDimensions.height + baseDialogDimensions.height) *
                      htmlHeightIndex *
                      ((step.info.html?.width ?? IMAGE_SCALE_FACTOR) /
                        IMAGE_SCALE_FACTOR),
                    screenHeight * maxSizeFactor
                  ),
                  Math.min(
                    (imageStepDimensions.width + baseDialogDimensions.width) *
                      htmlWidthIndex *
                      ((step.info.html?.width ?? IMAGE_SCALE_FACTOR) /
                        IMAGE_SCALE_FACTOR),
                    screenWidth * maxSizeFactor
                  ),
                  step.info.html?.border ?? 0,
                  t
                )}
              {step.info.html?.code_or_url &&
                !step.info.html?.is_raw_html &&
                renderHTMLLink(
                  step.info.html.code_or_url,
                  Math.min(
                    (imageStepDimensions.height + baseDialogDimensions.height) *
                      htmlHeightIndex *
                      ((step.info.html?.width ?? IMAGE_SCALE_FACTOR) /
                        IMAGE_SCALE_FACTOR),
                    screenHeight * maxSizeFactor
                  ),
                  Math.min(
                    (imageStepDimensions.width + baseDialogDimensions.width) *
                      htmlWidthIndex *
                      ((step.info.html?.width ?? IMAGE_SCALE_FACTOR) /
                        IMAGE_SCALE_FACTOR),
                    screenWidth * maxSizeFactor
                  ),
                  step.info.html?.border ?? 0,
                  t
                )}
            </div>
          </div>
        }
      ></Tab>
    ))}
  </Tabs>
);

/**
 * StartConfirmationDialog is a React component that renders a dialog box with various types of input widgets.
 * It supports text input, numeric input, radio buttons, checkboxes, and multi-step forms.
 *
 * When `pass_fail` is enabled:
 * - Pressing Enter in any input field will **focus the "Pass" button** but **will not trigger it**.
 * - The operator must explicitly click "Pass" or "Fail".
 *
 * @param {Props} props - The properties passed to the component.
 * @returns {JSX.Element} - The rendered dialog box.
 */
export function StartConfirmationDialog(props: Readonly<Props>): JSX.Element {
  const { t, i18n } = useTranslation();
  const [dialogOpen, setDialogOpen] = useState(false);
  const [inputText, setInputText] = useState("");
  const [selectedRadioButton, setSelectedRadioButton] = useState("");
  const [selectedCheckboxes, setSelectedCheckboxes] = useState<string[]>([]);
  const [imageDimensions, setImageDimensions] = useState(
    BASE_DIALOG_DIMENSIONS
  );
  const [imageStepDimensions, setStepImageDimensions] = useState(
    BASE_DIALOG_DIMENSIONS
  );
  const [hasHTML, setHasHTML] = useState(false);
  const maxDimensions = useRef(BASE_DIALOG_DIMENSIONS);
  const passButtonRef = useRef<HTMLButtonElement>(null);

  const widgetType = props.widget_type ?? WidgetType.Base;
  const maxSizeFactor =
    screenWidth < screenHeight ? PHONE_SCALE_FACTOR : MONITOR_SCALE_FACTOR;

  const lineHeight =
    (LINE_HEIGHT_FACTOR *
      (props.font_size ? props.font_size : BASE_FONT_SIZE)) /
    BASE_FONT_SIZE;

  const hasInputField = [
    WidgetType.TextInput,
    WidgetType.NumericInput,
    WidgetType.RadioButton,
    WidgetType.Checkbox,
  ].includes(widgetType);

  /**
   * Focuses the "Pass" button without triggering its `onClick`.
   */
  const focusPassButton = () => {
    if (passButtonRef.current) {
      setTimeout(() => {
        passButtonRef.current?.focus();
      }, 1);
    }
  };

  /**
   * Encodes a URL component, replacing special characters with their hexadecimal equivalents.
   *
   * @param {string} str - The string to encode.
   * @returns {string} - The encoded string.
   */
  const processEncodeURLComponent = (str: string): string => {
    return encodeURIComponent(str).replace(
      /[!-'()*+,/:;<=>?@[\]^`{|}~]/g,
      function (c) {
        return "%" + c.charCodeAt(0).toString(HEX_BASE);
      }
    );
  };

  /**
   * Prepares widget data based on the current widget type and state.
   *
   * @returns {string} - The prepared widget data as a string.
   */
  const prepareWidgetData = (): string => {
    let widgetData = "";

    switch (widgetType) {
      case WidgetType.TextInput:
        widgetData = processEncodeURLComponent(inputText);
        break;
      case WidgetType.NumericInput:
        widgetData = inputText;
        break;
      case WidgetType.RadioButton:
        widgetData = processEncodeURLComponent(selectedRadioButton);
        break;
      case WidgetType.Checkbox:
        widgetData = JSON.stringify(
          selectedCheckboxes.map((checkboxValue) =>
            processEncodeURLComponent(checkboxValue)
          )
        );
        break;
      default:
        widgetData = "ok";
        break;
    }

    return widgetData;
  };

  /**
   * Validates input based on the current widget type.
   *
   * @returns {boolean} - True if input is valid, false otherwise.
   */
  const validateInput = (): boolean => {
    if (props.widget_type) {
      switch (props.widget_type) {
        case WidgetType.TextInput:
        case WidgetType.NumericInput:
          if (
            inputText.trim() === "" ||
            inputText === "." ||
            inputText === ".."
          ) {
            alert(t("operatorDialog.fieldNotEmpty"));
            return false;
          }
          break;
        case WidgetType.RadioButton:
          if (selectedRadioButton === "") {
            alert(t("operatorDialog.fieldNotEmpty"));
            return false;
          }
          break;
        case WidgetType.Checkbox:
          if (selectedCheckboxes.length === 0) {
            alert(t("operatorDialog.fieldNotEmpty"));
            return false;
          }
          break;
        default:
          break;
      }
    }
    return true;
  };

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
      message: t("operatorDialog.notificationTitle"),
      description: t("operatorDialog.notificationDesc"),
    });
  };

  /**
   * Handles the pass/fail button clicks and sends the response to the server.
   * @async
   * @param {boolean} passed - True for PASS, False for FAIL
   * @returns {Promise<void>}
   */
  const handlePassFail = async (passed: boolean): Promise<void> => {
    // Validate input for widgets when using pass/fail
    if (!validateInput()) {
      return;
    }

    setDialogOpen(false);

    const widgetData = prepareWidgetData();

    try {
      const result = passed ? "passed" : "failed";
      // Send unified JSON payload structure
      const response = await axios.post(`/api/confirm_dialog_box`, {
        result: result,
        data: widgetData,
      });
      console.log(response.data);
    } catch (error) {
      console.error("Error sending dialog response:", error);
    }
  };

  /**
   * Handles the confirm event of the dialog box.
   * Validates the input and sends the confirmed data to the server.
   */
  const handleConfirm = async () => {
    if (!validateInput()) {
      return;
    }

    setDialogOpen(false);

    const widgetData = prepareWidgetData();

    if (props.onConfirm) {
      props.onConfirm(widgetData);
    }

    try {
      // Send unified JSON payload structure
      const response = await axios.post(`/api/confirm_dialog_box`, {
        result: "confirm",
        data: widgetData,
      });
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

    // Only handle Enter for confirmation when pass_fail is NOT enabled
    if (key === "Enter" && !props.pass_fail) {
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
    width:
      (naturalWidth * (widthFactor || IMAGE_SCALE_FACTOR)) / IMAGE_SCALE_FACTOR,
    height:
      (naturalHeight * (widthFactor || IMAGE_SCALE_FACTOR)) /
      IMAGE_SCALE_FACTOR,
  });

  /**
   * Handles the load event of an image, calculating its dimensions and updating the state.
   *
   * @param {React.SyntheticEvent<HTMLImageElement>} event - The image load event.
   */
  const handleImageLoad = (event: React.SyntheticEvent<HTMLImageElement>) => {
    const { naturalWidth, naturalHeight } = event.target as HTMLImageElement;
    setImageDimensions(
      calculateDimensions(
        naturalWidth,
        naturalHeight,
        props.image_width ?? IMAGE_SCALE_FACTOR
      )
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

  const dialogWidthForText = Math.min(
    (widgetType === WidgetType.Multistep
      ? maxDimensions.current
      : imageDimensions
    ).width + BASE_DIALOG_DIMENSIONS.width,
    screenWidth * MAX_SIZE_FACTOR
  );

  const textHeight =
    (calculateTextLines(props.dialog_text, dialogWidthForText) ?? 1) *
    lineHeight;
  const step = props.widget_info?.steps?.[0];
  const textStepHeight = step?.info?.text
    ? (calculateTextLines(step.info.text, dialogWidthForText) ?? 1) * lineHeight
    : lineHeight * 2;

  const { width: dialogWidth, height: dialogHeight } =
    calculateDialogDimensions(
      widgetType,
      maxDimensions.current,
      imageDimensions,
      BASE_DIALOG_DIMENSIONS,
      screenWidth,
      screenHeight,
      MAX_SIZE_FACTOR,
      MIN_SIZE_FACTOR,
      textHeight,
      textStepHeight,
      hasHTML
    );

  const imageStyle = {
    border: `${props.image_border ?? 0}px solid black`,
    display: "block",
    margin: "0 auto",
  };

  useEffect(() => {
    if (props.language) {
      i18n.changeLanguage(props.language);
    }
  }, [props.language, i18n]);

  useEffect(() => {
    console.log("Current language:", i18n.language);
    console.log(
      "All translations:",
      i18n.getResourceBundle(i18n.language, "translation")
    );
  }, [i18n]);

  useEffect(() => {
    if (props.is_visible) {
      setDialogOpen(true);
    }
  }, [props.is_visible, props.id]);

  useEffect(() => {
    if (widgetType === WidgetType.Multistep) {
      let htmlFound = false;

      const handleStepImageLoad = (
        image: HTMLImageElement,
        widthFactor: number
      ) => {
        const { naturalWidth, naturalHeight } = image;

        maxDimensions.current.width = Math.max(
          maxDimensions.current.width,
          naturalWidth * (widthFactor / IMAGE_SCALE_FACTOR)
        );
        maxDimensions.current.height = Math.max(
          maxDimensions.current.height,
          naturalHeight * (widthFactor / IMAGE_SCALE_FACTOR)
        );
        setStepImageDimensions(maxDimensions.current);
      };

      props.widget_info?.steps?.forEach((step) => {
        if (step.info.image) {
          const base64Src = `data:image/image;base64,${step.info.image?.base64}`;

          const image = new Image();
          image.src = base64Src;
          image.onload = () =>
            handleStepImageLoad(
              image,
              step.info.image?.width ?? IMAGE_SCALE_FACTOR
            );
        }
        if (step.info.html?.code_or_url) {
          htmlFound = true;
        }
      });
      setHasHTML(htmlFound);
    }
  }, [props.widget_info, widgetType]);

  return (
    <Dialog
      title={props.title_bar}
      icon="info-sign"
      isOpen={dialogOpen}
      onClose={handleClose}
      canOutsideClickClose={false}
      canEscapeKeyClose={true}
      style={{
        width:
          widgetType === WidgetType.Multistep ? `${dialogWidth}px` : "auto",
        height:
          widgetType === WidgetType.Multistep ? `${dialogHeight}px` : "auto",
        minWidth: screenWidth * MIN_SIZE_FACTOR,
        minHeight: screenHeight * MIN_SIZE_FACTOR,
        maxWidth: screenWidth * MAX_SIZE_FACTOR,
        maxHeight: screenHeight * MAX_SIZE_FACTOR,
        fontSize: `${props.font_size}px`,
      }}
    >
      <div
        className={Classes.DIALOG_BODY}
        style={{
          wordWrap: "break-word",
          wordBreak: "break-word",
          maxHeight: screenHeight * MAX_SIZE_FACTOR,
          overflowY: "auto",
          maxWidth: screenWidth * MAX_SIZE_FACTOR,
          padding: "10px",
        }}
      >
        {props.dialog_text.split("\n").map((line) => (
          <p key={line.trim()} style={{ textAlign: "left" }}>
            {line}
          </p>
        ))}
        {widgetType === WidgetType.TextInput &&
          renderTextInput(
            props,
            inputText,
            setInputText,
            handleKeyDown,
            t,
            focusPassButton
          )}
        {widgetType === WidgetType.NumericInput &&
          renderNumericInput(
            props,
            inputText,
            setInputText,
            handleKeyDown,
            t,
            focusPassButton
          )}
        {widgetType === WidgetType.RadioButton &&
          renderRadioButton(
            props,
            selectedRadioButton,
            setSelectedRadioButton,
            handleKeyDown,
            focusPassButton
          )}
        {widgetType === WidgetType.Checkbox &&
          renderCheckbox(
            props,
            selectedCheckboxes,
            setSelectedCheckboxes,
            handleKeyDown,
            focusPassButton
          )}
        {widgetType === WidgetType.Multistep &&
          renderMultistep(
            props,
            imageStepDimensions,
            BASE_DIALOG_DIMENSIONS,
            HTML_IFRAME_SCALE_FACTOR,
            HTML_IFRAME_WIDTH_FACTOR,
            imageStyle,
            maxSizeFactor,
            t
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
                maxWidth: `${dialogWidth - BASE_DIALOG_DIMENSIONS.width / 2}px`,
                maxHeight: `${dialogHeight - BASE_DIALOG_DIMENSIONS.height / 2}px`,
                objectFit: "scale-down",
                transform: `scale(${(props.image_width ?? IMAGE_SCALE_FACTOR) / IMAGE_SCALE_FACTOR})`,
                transformOrigin: `top center`,
                ...imageStyle,
              }}
            />
          </div>
        )}
        {props.html_code &&
          renderHTMLCode(
            props.html_code,
            screenHeight *
              (screenWidth < screenHeight
                ? PHONE_SCALE_FACTOR
                : MONITOR_SCALE_FACTOR) * // Dynamic size factor
              HTML_IFRAME_SCALE_FACTOR *
              ((props.html_width ?? IMAGE_SCALE_FACTOR) / IMAGE_SCALE_FACTOR),
            screenWidth *
              (screenWidth < screenHeight
                ? PHONE_SCALE_FACTOR
                : MONITOR_SCALE_FACTOR) * // Dynamic size factor
              HTML_IFRAME_WIDTH_FACTOR *
              ((props.html_width ?? IMAGE_SCALE_FACTOR) / IMAGE_SCALE_FACTOR),
            props.html_border ?? 0,
            t
          )}
        {props.html_url &&
          renderHTMLLink(
            props.html_url,
            screenHeight *
              (screenWidth < screenHeight
                ? PHONE_SCALE_FACTOR
                : MONITOR_SCALE_FACTOR) * // Dynamic size factor
              HTML_IFRAME_SCALE_FACTOR *
              ((props.html_width ?? IMAGE_SCALE_FACTOR) / IMAGE_SCALE_FACTOR),
            screenWidth *
              (screenWidth < screenHeight
                ? PHONE_SCALE_FACTOR
                : MONITOR_SCALE_FACTOR) * // Dynamic size factor
              HTML_IFRAME_WIDTH_FACTOR *
              ((props.html_width ?? IMAGE_SCALE_FACTOR) / IMAGE_SCALE_FACTOR),
            props.html_border ?? 0,
            t
          )}
      </div>
      <div className={Classes.DIALOG_FOOTER}>
        {props.pass_fail ? (
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              gap: "10px",
            }}
          >
            <Button
              ref={passButtonRef}
              intent="success"
              text={t("button.pass")}
              onClick={() => handlePassFail(true)}
              autoFocus={!hasInputField}
              style={{
                minWidth: "65px",
                fontSize: "14px",
              }}
            />
            <Button
              intent="danger"
              text={t("button.fail")}
              onClick={() => handlePassFail(false)}
              style={{
                minWidth: "65px",
                fontSize: "14px",
              }}
            />
          </div>
        ) : (
          <Button
            intent="primary"
            onClick={handleConfirm}
            autoFocus={
              widgetType === WidgetType.Base ||
              widgetType === WidgetType.Multistep
            }
            style={{
              minWidth: "65px",
            }}
          >
            {t("button.confirm")}
          </Button>
        )}
      </div>
    </Dialog>
  );
}

export default StartConfirmationDialog;
