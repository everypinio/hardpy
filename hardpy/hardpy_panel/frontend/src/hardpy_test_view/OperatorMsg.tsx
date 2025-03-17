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

/**
 * A React component that displays a dialog with a message, optional image, and optional HTML content.
 * @param {StartOperatorMsgDialogProps} props - The properties for the dialog.
 * @returns {JSX.Element} The rendered dialog component.
 */
export function StartOperatorMsgDialog(props: StartOperatorMsgDialogProps) {
  const [operatorMessageOpen, setOperatorMessageOpen] = useState(false);
  const [imageDimensions, setImageDimensions] = useState({
    width: 0,
    height: 0,
  });
  const screenWidth = window.screen.width;
  const screenHeight = window.screen.height;
  const baseOperatorMessageDimensions = { width: 100, height: 100 };
  const maxSize = 0.6;
  const minSize = 0.25;
  const lineHeight = (10 * (props.font_size ? props.font_size : 14)) / 14;

  /**
   * Handles the closing of the dialog and sends a confirmation to the server.
   * @async
   * @returns {Promise<void>}
   */
  const handleClose = async () => {
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
  ) => ({
    width: (naturalWidth * (widthFactor || 100)) / 100,
    height: (naturalHeight * (widthFactor || 100)) / 100,
  });

  /**
   * Handles the loading of the image and sets its dimensions.
   * @param {React.SyntheticEvent<HTMLImageElement>} event - The image load event.
   * @returns {void}
   */
  const handleImageLoad = (event: React.SyntheticEvent<HTMLImageElement>) => {
    const { naturalWidth, naturalHeight } = event.target as HTMLImageElement;
    setImageDimensions(
      calculateDimensions(naturalWidth, naturalHeight, props.image_width ?? 100)
    );
  };

  /**
   * Calculates the number of lines of text based on the text content and available width.
   * @param {string} text - The text content.
   * @param {number} width - The available width for the text.
   * @returns {number | undefined} The number of lines of text.
   */
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

  const operatorMessageWidth = Math.min(
    imageDimensions.width + baseOperatorMessageDimensions.width,
    screenWidth * maxSize
  );

  const textHeight =
    (calculateTextLines(props.msg, operatorMessageWidth) || 1) * lineHeight;

  const operatorMessageHeight = Math.max(
    Math.min(
      imageDimensions.height +
        baseOperatorMessageDimensions.height +
        textHeight,
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
    /**
     * Handles the keydown event to close the dialog when the Escape key is pressed.
     * @param {KeyboardEvent} event - The keydown event.
     * @returns {void}
     */
    const handleKeyDown = (event: KeyboardEvent) => {
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
        {props.msg.split("\n").map((line, index) => (
          <p key={index} style={{ textAlign: "left" }}>
            {line}
          </p>
        ))}
        {props.image_base64 && (
          <div className="image-container">
            <img
              src={`data:image/image;base64,${props.image_base64}`}
              alt="Image"
              onLoad={handleImageLoad}
              style={{
                width: `${props.image_width}%`,
                height: `${props.image_width}%`,
                maxWidth: `${operatorMessageWidth - baseOperatorMessageDimensions.width / 2}px`,
                maxHeight: `${operatorMessageHeight - baseOperatorMessageDimensions.height / 2}px`,
                objectFit: "scale-down",
                transform: `scale(${(props.image_width || 100) / 100})`,
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
              screenHeight * maxSize * 0.75 * ((props.html_width ?? 100) / 100)
            }
            width={
              screenWidth * maxSize * 0.9 * ((props.html_width ?? 100) / 100)
            }
            style={{
              border: `${props.html_border}px solid black`,
            }}
            title="HTML Code"
          />
        )}
        {props.html_url && (
          <iframe
            src={props.html_url}
            height={
              screenHeight * maxSize * 0.75 * ((props.html_width ?? 100) / 100)
            }
            width={
              screenWidth * maxSize * 0.9 * ((props.html_width ?? 100) / 100)
            }
            style={{
              border: `${props.html_border}px solid black`,
            }}
            title="HTML Link"
          />
        )}
      </div>
    </Dialog>
  );
}

export default StartOperatorMsgDialog;
