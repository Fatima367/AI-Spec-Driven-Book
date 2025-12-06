import React from 'react';
import PropTypes from 'prop-types';
import clsx from 'clsx';

/**
 * A reusable Button component with various styling options
 * Follows the design system requirements for the book landing page
 */
const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'medium', 
  className = '', 
  disabled = false,
  onClick,
  href,
  type = 'button',
  ...props 
}) => {
  // Determine button classes based on variant and size
  const baseClasses = 'button';
  const variantClasses = {
    primary: 'button--primary',
    secondary: 'button--secondary',
    gradient: 'button--gradient', // For CTA buttons with gradient effect
    link: 'button--link',
  };
  const sizeClasses = {
    small: 'button--sm',
    medium: 'button--md',
    large: 'button--lg',
  };

  // Determine if it's a link button
  const isLink = href && !disabled;
  
  const buttonClasses = clsx(
    baseClasses,
    variantClasses[variant],
    sizeClasses[size],
    { 'button--disabled': disabled },
    className
  );

  // For gradient buttons, we need special styling
  const getGradientStyle = () => {
    if (variant === 'gradient') {
      return {
        background: 'linear-gradient(90deg, #00E0FF 0%, #002BFF 100%)',
        border: 'none',
        color: 'white',
        fontWeight: 'bold',
        textTransform: 'uppercase',
        borderRadius: '50px', // Fully rounded pill shape
      };
    }
    return {};
  };

  if (isLink) {
    return (
      <a
        href={href}
        className={buttonClasses}
        style={{ ...getGradientStyle() }}
        onClick={disabled ? undefined : onClick}
        {...props}
      >
        {children}
      </a>
    );
  }

  return (
    <button
      type={type}
      className={buttonClasses}
      style={{ ...getGradientStyle() }}
      onClick={disabled ? undefined : onClick}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
};

Button.propTypes = {
  children: PropTypes.node.isRequired,
  variant: PropTypes.oneOf(['primary', 'secondary', 'gradient', 'link']),
  size: PropTypes.oneOf(['small', 'medium', 'large']),
  className: PropTypes.string,
  disabled: PropTypes.bool,
  onClick: PropTypes.func,
  href: PropTypes.string,
  type: PropTypes.oneOf(['button', 'submit', 'reset']),
};

export default Button;