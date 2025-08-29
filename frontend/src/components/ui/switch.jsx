import React from 'react';

function SwitchComponent({ checked, ...props }) {
  const handleChange = (event) => {
    if (props.onCheckedChange) {
      props.onCheckedChange(event.target.checked);
    }
    if (props.onChange) {
      props.onChange(event);
    }
  };
  const inputProps = Object.assign({}, props, {
    type: 'checkbox',
    checked: checked,
    onChange: handleChange,
  });
  return React.createElement('input', inputProps);
}

export const Switch = SwitchComponent;
export default SwitchComponent;
