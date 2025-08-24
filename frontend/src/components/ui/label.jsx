import React from 'react';

export function Label({ children, ...props }) {
  return React.createElement('label', props, children);
}

export default Label;
