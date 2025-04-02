export const BASE_DIALOG_DIMENSIONS = { width: 100, height: 100 };
export const MAX_SIZE_FACTOR = 0.85;
export const MIN_SIZE_FACTOR = 0.25;
export const LINE_HEIGHT_FACTOR = 10;
export const BASE_FONT_SIZE = 14;
export const HTML_IFRAME_SCALE_FACTOR = 0.75;
export const HTML_IFRAME_WIDTH_FACTOR = 0.9;
export const IMAGE_SCALE_FACTOR = 100;

export interface Dimensions {
  width: number;
  height: number;
}

/**
 * Calculates scaled dimensions while maintaining aspect ratio
 * @param {number} naturalWidth - Original width of the element
 * @param {number} naturalHeight - Original height of the element
 * @param {number} widthFactor - Scaling factor (percentage)
 * @returns {Dimensions} - Calculated width and height
 */
export const calculateDimensions = (
  naturalWidth: number,
  naturalHeight: number,
  widthFactor: number
): Dimensions => ({
  width:
    (naturalWidth * (widthFactor || IMAGE_SCALE_FACTOR)) / IMAGE_SCALE_FACTOR,
  height:
    (naturalHeight * (widthFactor || IMAGE_SCALE_FACTOR)) / IMAGE_SCALE_FACTOR,
});

/**
 * Estimates the number of text lines needed to display content
 * @param {string} text - The text content to measure
 * @param {number} width - Available width for text wrapping
 * @returns {number|undefined} - Estimated line count or undefined if measurement fails
 */
export const calculateTextLines = (
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

/**
 * Calculates optimal dialog dimensions based on content type and screen constraints
 * @param {string} widgetType - Type of widget being displayed
 * @param {Dimensions} maxDimensions - Maximum content dimensions
 * @param {Dimensions} imageDimensions - Image dimensions (if applicable)
 * @param {Dimensions} baseDialogDimensions - Minimum dialog dimensions
 * @param {number} screenWidth - Available screen width
 * @param {number} screenHeight - Available screen height
 * @param {number} maxSize - Maximum size factor (0-1)
 * @param {number} minSize - Minimum size factor (0-1)
 * @param {number} textHeight - Calculated height needed for text content
 * @param {number} textStepHeight - Additional height for step-based content
 * @param {boolean} hasHTML - Flag indicating HTML content presence
 * @returns {Dimensions} - Final calculated dialog dimensions
 */
export const calculateDialogDimensions = (
  widgetType: string,
  maxDimensions: Dimensions,
  imageDimensions: Dimensions,
  baseDialogDimensions: Dimensions,
  screenWidth: number,
  screenHeight: number,
  maxSize: number,
  minSize: number,
  textHeight: number,
  textStepHeight: number,
  hasHTML: boolean
): Dimensions => {
  if (hasHTML) {
    return {
      width: screenWidth * maxSize,
      height: screenHeight * maxSize,
    };
  }

  const dialogWidth = Math.min(
    (widgetType === "multistep" ? maxDimensions : imageDimensions).width +
      baseDialogDimensions.width,
    screenWidth * maxSize
  );

  const dialogHeight = Math.max(
    Math.min(
      (widgetType === "multistep"
        ? maxDimensions.height + baseDialogDimensions.height
        : imageDimensions.height) +
        baseDialogDimensions.height +
        textHeight +
        textStepHeight,
      screenHeight * maxSize
    ),
    screenHeight * minSize
  );

  return { width: dialogWidth, height: dialogHeight };
};
