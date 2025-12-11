/**
 * Content personalization component that adjusts content based on user's background
 * Uses user's software/hardware experience to determine content complexity
 */

import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';

const ContentPersonalizer = ({ children, originalContent }) => {
  const { user } = useAuth();
  const [personalizedContent, setPersonalizedContent] = useState(originalContent || children);
  const [isPersonalized, setIsPersonalized] = useState(false);

  const personalizeContent = (content, userProfile) => {
    if (!userProfile) return content;

    const { softwareExperience, hardwareExperience, technicalBackground } = userProfile;

    // Create a simplified version for beginners
    if (softwareExperience === 'beginner' || hardwareExperience === 'beginner') {
      // Replace complex technical terms with simpler explanations
      let simplifiedContent = content;

      // This is a simplified example - in a real implementation,
      // this would involve more sophisticated content transformation
      simplifiedContent = simplifiedContent.replace(/algorithm/gi, 'step-by-step process');
      simplifiedContent = simplifiedContent.replace(/optimization/gi, 'improvement');
      simplifiedContent = simplifiedContent.replace(/implementation/gi, 'creation');

      return simplifiedContent;
    }
    // Create an advanced version for experts
    else if (softwareExperience === 'advanced' || hardwareExperience === 'advanced') {
      // Add more technical depth
      let enhancedContent = content;

      // This would add more technical details in a real implementation
      enhancedContent += '\n\n<details class="advanced-content">Advanced implementation considerations...</details>';

      return enhancedContent;
    }

    // Return original content for intermediate users
    return content;
  };

  const handlePersonalizeForMe = () => {
    if (user) {
      const newContent = personalizeContent(originalContent || children, user);
      setPersonalizedContent(newContent);
      setIsPersonalized(true);
    }
  };

  const handleReset = () => {
    setPersonalizedContent(originalContent || children);
    setIsPersonalized(false);
  };

  return (
    <div className="content-personalizer">
      <div className="personalization-controls">
        {user && (
          <button
            className="personalize-button"
            onClick={handlePersonalizeForMe}
          >
            {isPersonalized ? 'Reset Content' : 'Personalize for Me'}
          </button>
        )}
        {isPersonalized && (
          <button
            className="reset-button"
            onClick={handleReset}
          >
            Reset
          </button>
        )}
      </div>

      <div className="personalized-content">
        {personalizedContent}
      </div>
    </div>
  );
};

export default ContentPersonalizer;