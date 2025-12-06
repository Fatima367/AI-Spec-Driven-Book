/**
 * Responsive utility functions for the book landing page
 * Provides breakpoints and responsive helper functions
 */

// Breakpoints as defined in Docusaurus config
export const breakpoints = {
  mobile: 768,    // Max width for mobile devices
  tablet: 992,    // Max width for tablet devices
  desktop: 1200,  // Min width for desktop devices
};

/**
 * Check if the current screen size is mobile
 * @returns {boolean} True if screen width is less than or equal to mobile breakpoint
 */
export const isMobile = () => {
  if (typeof window !== 'undefined') {
    return window.innerWidth <= breakpoints.mobile;
  }
  return false; // Default to false when server-side rendering
};

/**
 * Check if the current screen size is tablet
 * @returns {boolean} True if screen width is between mobile and tablet breakpoints
 */
export const isTablet = () => {
  if (typeof window !== 'undefined') {
    return (
      window.innerWidth > breakpoints.mobile &&
      window.innerWidth <= breakpoints.tablet
    );
  }
  return false; // Default to false when server-side rendering
};

/**
 * Check if the current screen is desktop
 * @returns {boolean} True if screen width is greater than tablet breakpoint
 */
export const isDesktop = () => {
  if (typeof window !== 'undefined') {
    return window.innerWidth > breakpoints.tablet;
  }
  return false; // Default to false when server-side rendering
};

/**
 * Get the current device type based on screen width
 * @returns {string} 'mobile', 'tablet', or 'desktop'
 */
export const getDeviceType = () => {
  if (typeof window !== 'undefined') {
    const width = window.innerWidth;
    if (width <= breakpoints.mobile) {
      return 'mobile';
    } else if (width <= breakpoints.tablet) {
      return 'tablet';
    } else {
      return 'desktop';
    }
  }
  return 'desktop'; // Default to desktop when server-side rendering
};

/**
 * Convert pixel values to rem for responsive design
 * @param {number} px - Pixel value to convert
 * @param {number} baseFontSize - Base font size in pixels (default: 16)
 * @returns {string} Rem value as a string
 */
export const pxToRem = (px, baseFontSize = 16) => {
  return `${px / baseFontSize}rem`;
};

/**
 * Generate responsive spacing based on screen size
 * @param {number} mobileSpacing - Spacing value for mobile
 * @param {number} tabletSpacing - Spacing value for tablet (optional)
 * @param {number} desktopSpacing - Spacing value for desktop (optional)
 * @returns {string} CSS spacing value that adapts to screen size
 */
export const responsiveSpacing = (mobileSpacing, tabletSpacing, desktopSpacing) => {
  const tabletVal = tabletSpacing !== undefined ? tabletSpacing : mobileSpacing;
  const desktopVal = desktopSpacing !== undefined ? desktopSpacing : tabletVal;
  
  return {
    mobile: `${mobileSpacing}px`,
    tablet: `${tabletVal}px`,
    desktop: `${desktopVal}px`,
  };
};

export default {
  breakpoints,
  isMobile,
  isTablet,
  isDesktop,
  getDeviceType,
  pxToRem,
  responsiveSpacing,
};