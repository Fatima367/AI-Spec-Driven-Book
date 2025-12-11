/**
 * Reusable authentication modal component that can display either login or signup forms
 */
import React, { useState } from 'react';
import LoginForm from './LoginForm';
import SignupForm from './SignupForm';
import './Auth.css';

const AuthModal = ({ isOpen, onClose, initialView = 'login', onLoginSuccess, onSignupSuccess }) => {
  const [currentView, setCurrentView] = useState(initialView);

  if (!isOpen) {
    return null;
  }

  const handleLoginSuccess = (user) => {
    if (onLoginSuccess) {
      onLoginSuccess(user);
    } else {
      onClose();
      // Fallback to page reload if no specific success handler provided
      window.location.reload();
    }
  };

  const handleSignupSuccess = (user) => {
    if (onSignupSuccess) {
      onSignupSuccess(user);
    } else {
      onClose();
      // Fallback to page reload if no specific success handler provided
      window.location.reload();
    }
  };

  return (
    <div className="auth-modal-overlay" onClick={onClose}>
      <div className="auth-modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="auth-modal-header">
          <h2>{currentView === 'login' ? 'Sign In' : 'Create Account'}</h2>
          <button className="auth-modal-close" onClick={onClose} aria-label="Close modal">
            ×
          </button>
        </div>

        <div className="auth-modal-body">
          {currentView === 'login' ? (
            <LoginForm onLoginSuccess={handleLoginSuccess} />
          ) : (
            <SignupForm onSignupSuccess={handleSignupSuccess} />
          )}
        </div>

        <div className="auth-modal-footer">
          <p>
            {currentView === 'login' ? "Don't have an account? " : "Already have an account? "}
            <button
              className="auth-toggle-link"
              onClick={() => setCurrentView(currentView === 'login' ? 'signup' : 'login')}
            >
              {currentView === 'login' ? 'Sign Up' : 'Sign In'}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default AuthModal;