import React from 'react';

export function Switch({ checked, oncheckedchange, onchange, ...props }) {
  const handlechange = (event) => {
    if (oncheckedchange) {
      oncheckedchange(event.target.checked);
    }
    if (onchange) {
      onchange(event);
    }
  };
  const inputProps = Object.assign({}, props, {
    type: 'checkbox',
    checked: checked,
    onChange: handlechange,
  });
  return React.createElement('input', inputProps);
}

export default Switch;
