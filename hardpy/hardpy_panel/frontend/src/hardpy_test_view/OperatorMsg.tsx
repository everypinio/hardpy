// Copyright (c) 2024 Everypin
// GNU General Public License v3.0 (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import React, { useState, useEffect } from "react";
import { Classes, Dialog } from "@blueprintjs/core";
import axios from "axios";
import {
  BASE_DIALOG_DIMENSIONS,
  MAX_SIZE_FACTOR,
  MIN_SIZE_FACTOR,
  LINE_HEIGHT_FACTOR,
  BASE_FONT_SIZE,
  HTML_IFRAME_SCALE_FACTOR,
  HTML_IFRAME_WIDTH_FACTOR,
  IMAGE_SCALE_FACTOR,
  calculateDimensions,
  calculateTextLines,
  calculateDialogDimensions,
} from "./DialogUtils";

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
    BASE_DIALOG_DIMENSIONS
  );
  const screenWidth = window.screen.width;
  const screenHeight = window.screen.height;

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
   * Calculates the line height based on font size and scaling factor.
   * Uses base font size for proportional scaling.
   * @type {number}
   */
  const lineHeight: number =
    (LINE_HEIGHT_FACTOR * (props.font_size ?? BASE_FONT_SIZE)) / BASE_FONT_SIZE;
  /**
   * Calculates the optimal dialog width for text content.
   * Ensures the width doesn't exceed maximum screen size factor.
   * @type {number}
   */
  const dialogWidthForText: number = Math.min(
    imageDimensions.width + BASE_DIALOG_DIMENSIONS.width,
    screenWidth * MAX_SIZE_FACTOR
  );

  /**
   * Calculates the total text height based on line count and line height.
   * Uses canvas text measurement for accurate line count estimation.
   * @type {number}
   */
  const textHeight: number =
    (calculateTextLines(props.msg, dialogWidthForText) ?? 1) * lineHeight;

  /**
   * Calculates final dialog dimensions considering all content elements.
   * Handles special cases for HTML content and maintains aspect ratios.
   * @type {Dimensions}
   */
  const { width: operatorMessageWidth, height: operatorMessageHeight } =
    calculateDialogDimensions(
      "base",
      imageDimensions,
      imageDimensions,
      BASE_DIALOG_DIMENSIONS,
      screenWidth,
      screenHeight,
      MAX_SIZE_FACTOR,
      MIN_SIZE_FACTOR,
      textHeight,
      0,
      !!props.html_code || !!props.html_url
    );

  /**
   * Defines base styling for displayed images.
   * Includes border configuration and centering properties.
   * @type {React.CSSProperties}
   */
  const imageStyle: React.CSSProperties = {
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

  useEffect(() => {
    /**
     * Manages the page scroll behavior when the modal dialog is opened or closed.
     */
    if (operatorMessageOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "auto";
    }

    return () => {
      document.body.style.overflow = "auto";
    };
  }, [operatorMessageOpen]);

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
          overflow: "hidden",
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
                maxWidth: `${operatorMessageWidth - BASE_DIALOG_DIMENSIONS.width / 2}px`,
                maxHeight: `${operatorMessageHeight - BASE_DIALOG_DIMENSIONS.height / 2}px`,
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
