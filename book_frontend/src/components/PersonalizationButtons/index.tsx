import React, { useState, useContext } from 'react';
import { PersonalizationContext } from '../../contexts/PersonalizationContext';
import { useAuth } from '../../contexts/AuthContext';
import { API_CONFIG } from '../../config/apiConfig';
import './PersonalizationButtons.css';

export function PersonalizeButton({ chapterId }: { chapterId?: string } = {}) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();
  const context = useContext(PersonalizationContext);

  // Check if context is undefined (not properly wrapped)
  if (context === undefined) {
    console.warn('PersonalizationButton is not wrapped in PersonalizationProvider');
  }

  // Extract chapterId from URL if not provided
  const currentChapterId = chapterId || (() => {
    // Check if we're in the browser environment before accessing window
    if (typeof window !== 'undefined') {
      const pathParts = window.location.pathname.split('/').filter(part => part !== '');
      const docsIndex = pathParts.indexOf('docs');
      if (docsIndex !== -1 && docsIndex + 1 < pathParts.length) {
        // Join all parts after 'docs' to get the full path (e.g., 'part1/chapter1.1')
        return pathParts.slice(docsIndex + 1).join('/');
      }
      // If 'docs' is not found, try to get the last part of the path
      if (pathParts.length > 0) {
        return pathParts[pathParts.length - 1];
      }
    }
    return 'unknown';
  })();

  // Ensure context is available before using it
  const userPreferences = context ? {
    learning_mode: context.learningMode,
    difficulty: context.difficulty,
    focus_area: context.focusArea
  } : null;

  const handleClick = async () => {
    if (!user) {
      // Check if we're in the browser environment before using alert
      if (typeof window !== 'undefined') {
        alert('Please log in to use personalization features');
      }
      return;
    }

    // Check if user profile is incomplete (only if user exists)
    if (user && (!user.softwareExperience || !user.hardwareExperience)) {
      // Check if we're in the browser environment before using confirm
      let shouldContinue = true;
      if (typeof window !== 'undefined') {
        shouldContinue = window.confirm(
          'Your profile appears to be incomplete. Would you like to update your profile before personalizing content? ' +
          'Click OK to update your profile, or Cancel to continue with default personalization.'
        );
      }

      if (shouldContinue) {
        // Redirect to profile update page or modal
        // For now, we'll just show an alert
        if (typeof window !== 'undefined') {
          alert('Please update your profile with experience information for better personalization.');
        }
        return;
      }
    }

    setLoading(true);
    setError(null);

    try {
      // Extract just the final part of the path for the API call (e.g., from 'part1/chapter1.1' get 'chapter1.1')
      const apiChapterId = currentChapterId.split('/').pop() || currentChapterId;
      const response = await fetch(`${API_CONFIG.BASE_URL}/api/v1/personalize/${apiChapterId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${user?.token || ''}` // Safely access token property
        },
        body: JSON.stringify({
          user_preferences: userPreferences
        })
      });

      // Handle different response statuses
      if (response.status === 401) {
        const errorData = await response.json();
        alert(`Authentication error: ${errorData.detail || 'Session expired. Please log in again.'}`);
        return;
      } else if (response.status === 429) {
        alert('Too many requests. Please try again later.');
        return;
      } else if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Server error: ${response.status}`);
      }

      const data = await response.json();

      if (data.success) {
        // Apply personalized content to the page
        // This would involve updating the content dynamically
        console.log('Personalized content:', data.content);

        // Show success message with more details
        alert('Content has been personalized for you based on your profile!');
      } else {
        throw new Error(data.error || 'Failed to personalize content');
      }
    } catch (err: any) {
      setError(err.message);

      // Handle specific error types
      if (err.message.includes('Failed to fetch')) {
        alert('Unable to connect to the personalization service. Please check your internet connection and try again.');
      } else if (err.message.includes('401') || err.message.toLowerCase().includes('unauthorized')) {
        alert('Your session may have expired. Please log in again.');
      } else {
        alert(`Error personalizing content: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      className={`personalize-btn ${loading ? 'loading' : ''}`}
      onClick={handleClick}
      disabled={loading}
    >
      {loading ? 'Personalizing...' : 'Personalize for Me'}
    </button>
  );
}

export function UrduTranslationButton({ chapterId }: { chapterId?: string } = {}) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();

  // Extract chapterId from URL if not provided
  const currentChapterId = chapterId || (() => {
    // Check if we're in the browser environment before accessing window
    if (typeof window !== 'undefined') {
      const pathParts = window.location.pathname.split('/').filter(part => part !== '');
      const docsIndex = pathParts.indexOf('docs');
      if (docsIndex !== -1 && docsIndex + 1 < pathParts.length) {
        // Join all parts after 'docs' to get the full path (e.g., 'part1/chapter1.1')
        return pathParts.slice(docsIndex + 1).join('/');
      }
      // If 'docs' is not found, try to get the last part of the path
      if (pathParts.length > 0) {
        return pathParts[pathParts.length - 1];
      }
    }
    return 'unknown';
  })();

  // Check if current page is Urdu - using currentChapterId and window location to determine this
  const isUrduPage = currentChapterId.startsWith('urdu-') ||
                     currentChapterId.includes('/urdu-') ||
                     currentChapterId.includes('urdu-index') ||
                     currentChapterId.includes('urdu-chapter') ||
                     (typeof window !== 'undefined' && window.location.pathname.includes('/urdu-'));

  const handleClick = () => {
    if (!user) {
      // Check if we're in the browser environment before using confirm
      let shouldLogin = true;
      if (typeof window !== 'undefined') {
        shouldLogin = window.confirm(
          'Please log in to access Urdu translation features. Would you like to proceed to login?'
        );
      }
      if (shouldLogin) {
        // In a real implementation, this would redirect to login
        if (typeof window !== 'undefined') {
          alert('Redirecting to login page...');
        }
      }
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Only access window if we're in browser environment
      if (typeof window !== 'undefined') {
        const currentPath = window.location.pathname;

        // Determine if we're currently on a Urdu page based on the current path
        const isCurrentlyUrduPage = currentPath.includes('/urdu-');

        if (isCurrentlyUrduPage) {
          // If on Urdu page, navigate to English version
          // Handle different patterns:
          // /docs/urdu-intro -> /docs/intro
          // /docs/part1/urdu-chapter1.1 -> /docs/part1/chapter1.1
          // /docs/module1-ros2/urdu-index -> /docs/module1-ros2/ (not /docs/module1-ros2/index)
          let englishPath = currentPath;

          // Handle the urdu-index case: /docs/module/urdu-index -> /docs/module/ (not /docs/module/index)
          // In Docusaurus, index.mdx files are served at the directory route, not /index
          if (currentPath.includes('/urdu-index')) {
            englishPath = currentPath.replace('/urdu-index', '/');
          } else {
            // Handle general urdu- prefix: /docs/urdu-... -> /docs/...
            // Need to be more specific to avoid replacing /docs/urdu- with /docs/-
            englishPath = currentPath.replace('/docs/urdu-', '/docs/');
            // Handle cases like /docs/part1/urdu-chapter1.1 -> /docs/part1/chapter1.1
            englishPath = englishPath.replace('/urdu-', '/');
          }

          window.location.href = englishPath;
        } else {
          // If on English page, navigate to Urdu version
          // Handle different patterns:
          // /docs/intro -> /docs/urdu-intro
          // /docs/part1/chapter1.1 -> /docs/part1/urdu-chapter1.1
          // /docs/module1-ros2/index -> /docs/module1-ros2/urdu-index
          let urduPath = currentPath;

          // If it's a directory with index (like /docs/module1-ros2/index), we want to go to urdu-index
          if (currentPath.endsWith('/index')) {
            urduPath = currentPath.replace('/index', '/urdu-index');
          } else if (currentPath.endsWith('/')) {
            // If it's a directory ending with /, we want to go to urdu-index
            urduPath = currentPath.replace(/\/$/, '/urdu-index');
          } else {
            // For regular files, add 'urdu-' prefix to the last part after the last '/'
            const lastSlashIndex = currentPath.lastIndexOf('/');
            if (lastSlashIndex !== -1) {
              const basePath = currentPath.substring(0, lastSlashIndex + 1);
              const fileName = currentPath.substring(lastSlashIndex + 1);
              if (fileName && fileName !== 'index') {
                urduPath = basePath + 'urdu-' + fileName;
              } else if (fileName === 'index') {
                // For /docs/index, should become /docs/urdu-index
                urduPath = currentPath.replace('/index', '/urdu-index');
              }
            } else {
              // If no slash found after /docs/, it's a root level file like /docs/intro
              urduPath = currentPath.replace('/docs/', '/docs/urdu-');
            }
          }

          // Check if the Urdu version exists before navigating
          fetch(urduPath, { method: 'HEAD' })
            .then(response => {
              if (response.status === 404) {
                alert('Urdu translation is not available for this chapter yet. Please check back later.');
              } else {
                // Navigate to Urdu version
                window.location.href = urduPath;
              }
            })
            .catch(() => {
              // If the HEAD request fails, assume the file doesn't exist or is unreachable
              alert('Unable to verify Urdu translation availability. Redirecting anyway...');
              window.location.href = urduPath;
            });
        }
      }
    } catch (err: any) {
      setError(err.message);
      // Check if we're in the browser environment before using alert
      if (typeof window !== 'undefined') {
        alert(`Error with translation: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      className={`urdu-translate-btn ${loading ? 'loading' : ''}`}
      onClick={handleClick}
      disabled={loading}
    >
      {loading ? 'Loading...' : (isUrduPage ? 'Translate to English' : 'اردو میں ترجمہ کریں')}
    </button>
  );
}