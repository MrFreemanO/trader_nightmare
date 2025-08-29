import React from 'react';

export const Badge = ({ children, variant = 'default', ...props }) => {
  const baseStyle = {
    display: 'inline-block',
    padding: '2px 8px',
    fontSize: '12px',
    fontWeight: '500',
    borderRadius: '8px',
  };

  let style;

  if (variant === 'destructive') {
    style = { ...baseStyle, backgroundColor: '#dc3545', color: '#fff' };
  } else if (variant === 'secondary') {
    style = { ...baseStyle, backgroundColor: '#e2e8f0', color: '#000' };
  } else if (variant === 'outline') {
    style = { ...baseStyle, backgroundColor: 'transparent', border: '1px solid #333', color: '#333' };
  } else {
    style = { ...baseStyle, backgroundColor: '#eee', color: '#333' };
  }

  return (
    <span {...props} style={style}>
      {children}
    </span>
  );
};

export default Badge;
