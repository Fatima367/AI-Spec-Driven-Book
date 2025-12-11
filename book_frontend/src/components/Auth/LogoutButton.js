/**
 * Logout button component
 * Provides a simple button to log out the current user
 */

import React from 'react';
import { useAuth } from '../../contexts/AuthContext';

const LogoutButton = ({ onLogoutSuccess }) => {
  const { signOut, isLoading } = useAuth();

  const handleLogout = async () => {
    try {
      await signOut();
      if (onLogoutSuccess) {
        onLogoutSuccess();
      }
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  return (
    <button
      onClick={handleLogout}
      disabled={isLoading}
      className="logout-button"
    >
      {isLoading ? 'Logging out...' : 'Logout'}
    </button>
  );
};

export default LogoutButton;