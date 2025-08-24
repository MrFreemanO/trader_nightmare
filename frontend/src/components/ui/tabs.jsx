import React, { createContext, useContext, useState } from 'react';

const TabsContext = createContext({ value: '', setValue: () => {} });

export function Tabs({ defaultValue = '', value: controlledValue, onValueChange, children, className = '', ...props }) {
  const [value, setValue] = useState(defaultValue);
  const currentValue = controlledValue !== undefined ? controlledValue : value;
  const handleChange = (newValue) => {
    if (controlledValue === undefined) {
      setValue(newValue);
    }
    if (onValueChange) {
      onValueChange(newValue);
    }
  };
  return React.createElement(
    TabsContext.Provider,
    { value: { value: currentValue, setValue: handleChange } },
    React.createElement('div', { className, ...props }, children)
  );
}

export function TabsList({ children, className = '', ...props }) {
  return React.createElement('div', { className: `flex gap-2 border-b ${className}`, ...props }, children);
}

export function TabsTrigger({ children, value, className = '', ...props }) {
  const { value: currentValue, setValue } = useContext(TabsContext);
  const isActive = currentValue === value;
  const finalClass = `${isActive ? 'border-b-2 font-semibold' : 'text-gray-500'} ${className}`;
  return React.createElement(
    'button',
    {
      type: 'button',
      onClick: () => setValue(value),
      className: finalClass,
      ...props,
    },
    children
  );
}

export function TabsContent({ children, value, className = '', ...props }) {
  const { value: currentValue } = useContext(TabsContext);
  if (currentValue !== value) return null;
  return React.createElement('div', { className, ...props }, children);
}

export default Tabs;
