import React from 'react';

export const Button = ({ children, variant = 'default', size = 'md', ...props }) => {
  const baseStyle = {
    padding: size === 'sm' ? '6px 12px' : size === 'lg' ? '10px 20px' : '8px 16px',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: size === 'sm' ? '14px' : size === 'lg' ? '18px' : '16px',
  };

  let style;
  if (variant === 'outline') {
    style = { ...baseStyle, background: 'transparent', border: '1px solid #007bff', color: '#007bff' };
  } else if (variant === 'ghost') {
    style = { ...baseStyle, background: 'transparent', color: '#007bff' };
  } else {
    style = { ...baseStyle, background: '#007bff', color: '#fff' };
  }

  return (
    <button {...props} style={style}>
      {children}
    </button>
  );
};

export default Button;
