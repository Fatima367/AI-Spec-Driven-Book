import React, { Suspense } from 'react';
import { AuthProvider } from '../../contexts/AuthContext';
import { PersonalizationProvider } from '../../contexts/PersonalizationContext';

// Wrapper component that provides contexts to the buttons
const PersonalizationButtonsWrapper = (props) => {
  return (
    <AuthProvider>
      <PersonalizationProvider>
        <Suspense fallback={<div>Loading personalization buttons...</div>}>
          {props.children}
        </Suspense>
      </PersonalizationProvider>
    </AuthProvider>
  );
};

export default PersonalizationButtonsWrapper;