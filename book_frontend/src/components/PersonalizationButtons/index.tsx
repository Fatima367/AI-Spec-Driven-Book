import React from 'react';

export function PersonalizeButton() {
  const handleClick = () => {
    alert('Personalize content (integration with backend needed)');
    // TODO: Implement actual API call to /api/personalize/{chapterId}
  };
  return <button onClick={handleClick}>Personalize for Me</button>;
}

export function UrduTranslationButton() {
  const handleClick = () => {
    alert('Translate to Urdu (integration with backend needed)');
    // TODO: Implement actual API call to /api/translate/{chapterId}
  };
  return <button onClick={handleClick}>اردو میں ترجمہ کریں</button>;
}