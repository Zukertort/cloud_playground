import React from 'react';

interface ContainerProps {
  children: React.ReactNode;
  className?: string; // Allow passing extra classes if needed
}

export function Container({ children, className = '' }: ContainerProps) {
  return (
    <div className={`mx-auto w-full max-w-lg ${className}`}>
      {children}
    </div>
  );
}