import React from 'react';
import './PersonalizationButtons.css';

export function PersonalizeButton() {
  const handleClick = () => {
    alert('Personalize content (integration with backend needed)');
    // TODO: Implement actual API call to /api/personalize/{chapterId}
  };
  return <button className="personalize-btn" onClick={handleClick}>Personalize for Me</button>;
}

export function UrduTranslationButton() {
  const handleClick = () => {
    alert('Translate to Urdu (integration with backend needed)');
    // TODO: Implement actual API call to /api/translate/{chapterId}
  };
  return <button className="urdu-translate-btn" onClick={handleClick}>اردو میں ترجمہ کریں</button>;
}