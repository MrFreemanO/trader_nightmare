import React from 'react';

export const Card = ({ className = '', ...props }) => {
  return React.createElement('div', { className: 'rounded-lg border bg-white shadow-sm ' + className, ...props });
};

export const CardHeader = ({ className = '', ...props }) => {
  return React.createElement('div', { className: 'flex flex-col space-y-1.5 p-6 ' + className, ...props });
};

export const CardTitle = ({ className = '', ...props }) => {
  return React.createElement('h3', { className: 'text-lg font-semibold leading-none tracking-tight ' + className, ...props });
};

export const CardDescription = ({ className = '', ...props }) => {
  return React.createElement('p', { className: 'text-sm text-muted-foreground ' + className, ...props });
};

export const CardContent = ({ className = '', ...props }) => {
  return React.createElement('div', { className: 'p-6 pt-0 ' + className, ...props });
};

export const CardFooter = ({ className = '', ...props }) => {
  return React.createElement('div', { className: 'flex items-center p-6 pt-0 ' + className, ...props });
};

export default Card;
