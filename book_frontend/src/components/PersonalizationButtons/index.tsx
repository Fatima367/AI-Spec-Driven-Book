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
      // Check if the Urdu version exists by making a quick check
      // For now, we'll just navigate assuming the file exists
      // In a real implementation, we would check if the file exists first

      // Check if the current location is already the Urdu version
      // Only access window if we're in browser environment
      if (typeof window !== 'undefined') {
        const currentPath = window.location.pathname;
        if (currentPath.includes('/docs/urdu-')) {
          // If already on Urdu version, go back to original
          // For root level: urdu-filename -> filename
          // For directory index: directory/urdu-index -> directory/ (redirects to index)
          // For nested: directory/urdu-filename -> directory/filename
          let originalPath;
          if (currentChapterId.includes('/')) {
            // Nested path: directory/urdu-filename -> directory/filename
            const [directory, urduFilename] = currentChapterId.split('/');
            if (urduFilename === 'urdu-index') {
              // This is a directory index file: directory/urdu-index -> directory/
              originalPath = directory;
            } else {
              // Regular nested file: directory/urdu-filename -> directory/filename
              const originalFilename = urduFilename.replace('urdu-', '');
              originalPath = `${directory}/${originalFilename}`;
            }
          } else {
            // Root level: urdu-filename -> filename
            originalPath = currentChapterId.replace('urdu-', '');
          }

          // Navigate back to the original path by reconstructing the URL
          // Find the position of /docs/ and replace everything after it
          const docsIndex = currentPath.indexOf('/docs/');
          if (docsIndex !== -1) {
            let basePath = currentPath.substring(0, docsIndex + 6); // '/docs/' length is 6
            let newPath = basePath + originalPath;

            // Add trailing slash for directory index files if the original had one
            if (originalPath === 'module1-ros2' || originalPath === 'module2-digital-twin' ||
                originalPath === 'module3-ai-robot-brain' || originalPath === 'module4-vla' ||
                originalPath === 'capstone') {
              if (currentPath.endsWith('/')) {
                newPath += '/';
              }
            }

            window.location.href = newPath;
          }
        } else {
          // Navigate to Urdu version
          // For root level files: filename -> urdu-filename (intro -> urdu-intro, hardware-lab -> urdu-hardware-lab)
          // For directory index files: directory -> directory/urdu-index (module1-ros2 -> module1-ros2/urdu-index)
          // For nested files: directory/filename -> directory/urdu-filename (part1/chapter1.1 -> part1/urdu-chapter1.1)
          let urduPath;
          if (currentChapterId.includes('/')) {
            // Nested path: directory/filename -> directory/urdu-filename
            const [directory, filename] = currentChapterId.split('/');
            urduPath = `${directory}/urdu-${filename}`;
          } else {
            // Check if this looks like a directory name (contains hyphens and represents a module/capstone)
            // If it's a directory with an index file, go to directory/urdu-index
            // Otherwise, it's a root level file, go to urdu-filename
            if (currentChapterId === 'module1-ros2' || currentChapterId === 'module2-digital-twin' ||
                currentChapterId === 'module3-ai-robot-brain' || currentChapterId === 'module4-vla' ||
                currentChapterId === 'capstone') {
              // These are directory names that have index files
              urduPath = `${currentChapterId}/urdu-index`;
            } else {
              // Root level: filename -> urdu-filename
              urduPath = `urdu-${currentChapterId}`;
            }
          }

          // Construct the Urdu URL by reconstructing the full path
          // Find the position of /docs/ and replace everything after it
          const docsIndex = currentPath.indexOf('/docs/');
          if (docsIndex !== -1) {
            let basePath = currentPath.substring(0, docsIndex + 6); // '/docs/' length is 6
            let urduUrl = basePath + urduPath;

            // In a real implementation, we would make a HEAD request to check if the file exists
            // For now, we'll just navigate and handle 404s on the server side
            fetch(urduUrl, { method: 'HEAD' })
              .then(response => {
                if (response.status === 404) {
                  alert('Urdu translation is not available for this chapter yet. Please check back later.');
                } else {
                  // Navigate to Urdu version
                  window.location.href = urduUrl;
                }
              })
              .catch(() => {
                // If the HEAD request fails, assume the file doesn't exist or is unreachable
                alert('Unable to verify Urdu translation availability. Redirecting anyway...');
                window.location.href = urduUrl;
              });
          }
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
      {loading ? 'Loading...' : 'اردو میں ترجمہ کریں'}
    </button>
  );
}