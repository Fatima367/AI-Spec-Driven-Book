import React from 'react';
import { FaSignInAlt, FaUserPlus, FaSignOutAlt } from 'react-icons/fa';
import { useAuth } from '../../contexts/AuthContext';

/**
 * Navigation links for the book landing page
 * Contains buttons to open Login and Signup modals with React icons
 * Shows Login/Signup when not authenticated, Logout when authenticated
 */
const NavigationLinks = ({ onOpenLogin, onOpenSignup }) => {
  const { user, isLoading, signOut } = useAuth();

  const handleLoginClick = (e) => {
    e.preventDefault();
    if (onOpenLogin) {
      onOpenLogin();
    }
  };

  const handleSignupClick = (e) => {
    e.preventDefault();
    if (onOpenSignup) {
      onOpenSignup();
    }
  };

  const handleLogout = async (e) => {
    e.preventDefault();
    if (signOut) {
      await signOut();
    }
  };

  if (isLoading) {
    return (
      <div style={{ color: 'white', fontSize: '1rem' }}>
        Loading...
      </div>
    );
  }

  return (
    <>
      <div
        style={{ display: 'flex', gap: '20px' }}
        role="navigation"
        aria-label="Main navigation"
      >
        {!user ? (
          <>
            <button
              onClick={handleLoginClick}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '5px',
                color: 'white',
                textDecoration: 'none',
                fontWeight: '500',
                fontSize: '1rem',
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                padding: 0,
              }}
              aria-label="Open login modal"
            >
              <FaSignInAlt aria-hidden="true" /> Login
            </button>
            <button
              onClick={handleSignupClick}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '5px',
                color: 'white',
                textDecoration: 'none',
                fontWeight: '500',
                fontSize: '1rem',
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                padding: 0,
              }}
              aria-label="Open signup modal"
            >
              <FaUserPlus aria-hidden="true" /> Signup
            </button>
          </>
        ) : (
          <button
            onClick={handleLogout}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '5px',
              color: 'white',
              textDecoration: 'none',
              fontWeight: '500',
              fontSize: '1rem',
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              padding: 0,
            }}
            aria-label="Logout"
          >
            <FaSignOutAlt aria-hidden="true" /> Logout
          </button>
        )}
      </div>
    </>
  );
};

export default NavigationLinks;