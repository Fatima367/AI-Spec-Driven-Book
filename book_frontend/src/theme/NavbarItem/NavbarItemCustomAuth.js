import React, { useState, useEffect } from 'react';
import Link from '@docusaurus/Link';

// Custom navbar item component for authentication
function NavbarItemCustomAuth({
  className,
  to,
  href,
  activeClassName = 'navbar__link--active',
  prependBaseUrlToHref,
  ...props
}) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for token in localStorage to determine auth status
    const token = localStorage.getItem('session_token');
    setIsAuthenticated(!!token);
    setIsLoading(false);

    // Listen for storage changes (in case of login/logout in another tab)
    const handleStorageChange = (e) => {
      if (e.key === 'session_token') {
        setIsAuthenticated(!!localStorage.getItem('session_token'));
      }
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  const handleLogout = async () => {
    try {
      // Get the API base URL (similar to how it's done in apiConfig)
      const API_BASE_URL = typeof window !== 'undefined'
        ? window.location.origin
        : process.env.BACKEND_URL || 'https://ai-spec-driven-book-backend.up.railway.app';
      const API_VERSION = '/api/v1';

      // Call logout endpoint (server-side cleanup)
      const token = localStorage.getItem('session_token');
      if (token) {
        await fetch(`${API_BASE_URL}${API_VERSION}/auth/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });
      }

      // Clear local token
      localStorage.removeItem('session_token');

      // Update state
      setIsAuthenticated(false);

      // Refresh the page to update navbar and clear any cached user data
      window.location.reload();
    } catch (error) {
      console.error('Logout error:', error);
      // Still clear local token even if there's an error
      localStorage.removeItem('session_token');
      setIsAuthenticated(false);
    }
  };

  if (isLoading) {
    return (
      <div className={className}>
        <span style={{ color: 'white' }}>
          Loading...
        </span>
      </div>
    );
  }

  return (
    <div className={className}>
      {isAuthenticated ? (
        <button
          onClick={handleLogout}
          className="navbar__link"
          style={{
            color: 'white',
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            padding: 'var(--ifm-navbar-item-padding-vertical) var(--ifm-navbar-item-padding-horizontal)',
            fontSize: 'var(--ifm-font-size-base)',
            textDecoration: 'none',
          }}
        >
          Logout
        </button>
      ) : (
        <div style={{ display: 'flex', gap: '15px' }}>
          <Link
            to="/login"
            style={{
              color: 'white',
              padding: 'var(--ifm-navbar-item-padding-vertical) var(--ifm-navbar-item-padding-horizontal)',
              textDecoration: 'none',
            }}
          >
            Login
          </Link>
          <Link
            to="/signup"
            style={{
              color: 'white',
              padding: 'var(--ifm-navbar-item-padding-vertical) var(--ifm-navbar-item-padding-horizontal)',
              textDecoration: 'none',
            }}
          >
            Signup
          </Link>
        </div>
      )}
    </div>
  );
}

export default NavbarItemCustomAuth;