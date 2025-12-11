import React from 'react';
import Link from '@docusaurus/Link';
import { useAuth } from '@site/src/contexts/AuthContext';

export default function NavbarAuth() {
  const { user, isLoading, isAuthenticated, signOut } = useAuth();

  const handleLogout = async () => {
    if (signOut) {
      await signOut();
    }
  };

  if (isLoading) {
    return (
      <div className="navbar__item">
        <span style={{ color: 'white' }}>
          Loading...
        </span>
      </div>
    );
  }

  return (
    <div className="navbar__item">
      {isAuthenticated ? (
        <button
          onClick={handleLogout}
          style={{
            color: 'white',
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            padding: 'var(--ifm-navbar-item-padding-vertical) var(--ifm-navbar-item-padding-horizontal)',
            fontSize: 'var(--ifm-font-size-base)',
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