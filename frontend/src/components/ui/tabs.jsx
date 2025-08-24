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
  return (
    <TabsContext.Provider value={{ value: currentValue, setValue: handleChange }}>
      <div className={className} {...props}>{children}</div>
    </TabsContext.Provider>
  );
}

export function TabsList({ children, className = '', ...props }) {
  return <div className={`flex gap-2 border-b ${className}`} {...props}>{children}</div>;
}

export function TabsTrigger({ children, value, className = '', ...props }) {
  const { value: currentValue, setValue } = useContext(TabsContext);
  const isActive = currentValue === value;
  return (
    <button type="button" onClick={() => setValue(value)} className={`${isActive ? 'border-b-2 font-semibold' : 'text-gray-500'} ${className}`} {...props}>
      {children}
    </button>
  );
}

export function TabsContent({ children, value, className = '', ...props }) {
  const { value: currentValue } = useContext(TabsContext);
  if (currentValue !== value) return null;
  return <div className={className} {...props}>{children}</div>;
}

export default Tabs;
