// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import React, { useState, useEffect } from "react";
import { Classes, Dialog } from "@blueprintjs/core";
import axios from "axios";

interface StartOperatorMsgDialogProps {
  title: string;
  msg: string;
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

const BASE_OPERATOR_MESSAGE_DIMENSIONS = { width: 100, height: 100 };
const MAX_SIZE_FACTOR = 0.6;
const MIN_SIZE_FACTOR = 0.25;
const LINE_HEIGHT_FACTOR = 10;
const BASE_FONT_SIZE = 14;
const HTML_IFRAME_SCALE_FACTOR = 0.75;
const HTML_IFRAME_WIDTH_FACTOR = 0.9;
const IMAGE_SCALE_FACTOR = 100;

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
  border: number
): JSX.Element => (
  <iframe
    srcDoc={htmlCode}
    height={height}
    width={width}
    style={{
      border: `${border}px solid black`,
    }}
    title="HTML Code"
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
  border: number
): JSX.Element => (
  <iframe
    src={htmlUrl}
    height={height}
    width={width}
    style={{
      border: `${border}px solid black`,
    }}
    title="HTML Link"
  />
);

/**
 * A React component that displays a dialog with a message, optional image, and optional HTML content.
 * @param {StartOperatorMsgDialogProps} props - The properties for the dialog.
 * @returns {JSX.Element} The rendered dialog component.
 */
export function StartOperatorMsgDialog(
  props: Readonly<StartOperatorMsgDialogProps>
): JSX.Element {
  const [operatorMessageOpen, setOperatorMessageOpen] = useState(false);
  const [imageDimensions, setImageDimensions] = useState(
    BASE_OPERATOR_MESSAGE_DIMENSIONS
  );
  const screenWidth = window.screen.width;
  const screenHeight = window.screen.height;
  const lineHeight =
    (LINE_HEIGHT_FACTOR * (props.font_size ?? BASE_FONT_SIZE)) / BASE_FONT_SIZE;

  /**
   * Handles the closing of the dialog and sends a confirmation to the server.
   * @async
   * @returns {Promise<void>}
   */
  const handleClose = async (): Promise<void> => {
    setOperatorMessageOpen(false);

    try {
      const response = await axios.post(
        `/api/confirm_operator_msg/${JSON.stringify(operatorMessageOpen)}`
      );
      console.log(response.data);
    } catch (error) {
      console.error("Error confirming operator message:", error);
    }
  };

  /**
   * Calculates the dimensions of the image based on its natural dimensions and a width factor.
   * @param {number} naturalWidth - The natural width of the image.
   * @param {number} naturalHeight - The natural height of the image.
   * @param {number} widthFactor - The factor to scale the width by.
   * @returns {{width: number, height: number}} The calculated dimensions.
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
   * Handles the loading of the image and sets its dimensions.
   * @param {React.SyntheticEvent<HTMLImageElement>} event - The image load event.
   * @returns {void}
   */
  const handleImageLoad = (
    event: React.SyntheticEvent<HTMLImageElement>
  ): void => {
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
   * Calculates the number of lines of text based on the text content and available width.
   * @param {string} text - The text content.
   * @param {number} width - The available width for the text.
   * @returns {number | undefined} The number of lines of text.
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

  const operatorMessageWidth = Math.min(
    imageDimensions.width + BASE_OPERATOR_MESSAGE_DIMENSIONS.width,
    screenWidth * MAX_SIZE_FACTOR
  );

  const textHeight =
    (calculateTextLines(props.msg, operatorMessageWidth) ?? 1) * lineHeight;

  const operatorMessageHeight = Math.max(
    Math.min(
      imageDimensions.height +
        BASE_OPERATOR_MESSAGE_DIMENSIONS.height +
        textHeight,
      screenHeight * MAX_SIZE_FACTOR
    ),
    screenHeight * MIN_SIZE_FACTOR
  );

  const imageStyle = {
    border: `${props.image_border ?? 0}px solid black`,
    display: "block",
    margin: "0 auto",
  };

  useEffect(() => {
    /**
     * Handles the keydown event to close the dialog when the Escape key is pressed.
     * @param {KeyboardEvent} event - The keydown event.
     * @returns {void}
     */
    const handleKeyDown = (event: KeyboardEvent): void => {
      const keyboardEvent =
        event as unknown as React.KeyboardEvent<HTMLInputElement>;
      if (keyboardEvent.key === "Escape") {
        handleClose();
      }
    };

    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  });

  useEffect(() => {
    /**
     * Sets the dialog visibility based on the `is_visible` prop.
     * @returns {void}
     */
    if (props.is_visible) {
      setOperatorMessageOpen(true);
    }
  }, [props.id, props.is_visible]);

  return (
    <Dialog
      title={props.title || "Message"}
      icon="info-sign"
      isOpen={operatorMessageOpen}
      onClose={handleClose}
      canOutsideClickClose={false}
      style={{
        width: "auto",
        height: "auto",
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
        {props.msg.split("\n").map((line) => (
          <p key={line} style={{ textAlign: "left" }}>
            {line}
          </p>
        ))}
        {props.image_base64 && (
          <div className="image-container">
            <img
              src={`data:image/image;base64,${props.image_base64}`}
              alt={""} // Use a more descriptive text or an empty string if not available
              onLoad={handleImageLoad}
              style={{
                width: `${props.image_width}%`,
                height: `${props.image_width}%`,
                maxWidth: `${operatorMessageWidth - BASE_OPERATOR_MESSAGE_DIMENSIONS.width / 2}px`,
                maxHeight: `${operatorMessageHeight - BASE_OPERATOR_MESSAGE_DIMENSIONS.height / 2}px`,
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
              MAX_SIZE_FACTOR *
              HTML_IFRAME_SCALE_FACTOR *
              ((props.html_width ?? IMAGE_SCALE_FACTOR) / IMAGE_SCALE_FACTOR),
            screenWidth *
              MAX_SIZE_FACTOR *
              HTML_IFRAME_WIDTH_FACTOR *
              ((props.html_width ?? IMAGE_SCALE_FACTOR) / IMAGE_SCALE_FACTOR),
            props.html_border ?? 0
          )}
        {props.html_url &&
          renderHTMLLink(
            props.html_url,
            screenHeight *
              MAX_SIZE_FACTOR *
              HTML_IFRAME_SCALE_FACTOR *
              ((props.html_width ?? IMAGE_SCALE_FACTOR) / IMAGE_SCALE_FACTOR),
            screenWidth *
              MAX_SIZE_FACTOR *
              HTML_IFRAME_WIDTH_FACTOR *
              ((props.html_width ?? IMAGE_SCALE_FACTOR) / IMAGE_SCALE_FACTOR),
            props.html_border ?? 0
          )}
      </div>
    </Dialog>
  );
}

export default StartOperatorMsgDialog;
