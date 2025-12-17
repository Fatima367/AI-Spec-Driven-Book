import React from 'react';
import { PersonalizationProvider } from '../contexts/PersonalizationContext';
import { AuthProvider } from '../contexts/AuthContext';

// Root component that wraps the entire application
function Root({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <PersonalizationProvider>
        {children}
      </PersonalizationProvider>
    </AuthProvider>
  );
}

export default Root;