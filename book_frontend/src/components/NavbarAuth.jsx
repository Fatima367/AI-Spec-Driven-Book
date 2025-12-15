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
          className="navbar__item navbar__link"
          style={{
            color: 'inherit',
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            padding: 'var(--ifm-navbar-item-padding-vertical) var(--ifm-navbar-item-padding-horizontal)',
            fontSize: 'var(--ifm-font-size-base)',
            fontWeight: 'var(--ifm-font-weight-base)',
            textDecoration: 'none',
            fontFamily: 'inherit',
            lineHeight: 'var(--ifm-navbar-item-height)',
            display: 'flex',
            alignItems: 'center',
            height: 'var(--ifm-navbar-item-height)',
            outline: 'none',
            WebkitFontSmoothing: 'antialiased',
          }}
        >
          Logout
        </button>
      ) : (
        <div style={{ display: 'flex', gap: '15px' }}>
          <Link
            to="/login"
            className="navbar__item navbar__link"
            style={{
              color: 'inherit',
              padding: 'var(--ifm-navbar-item-padding-vertical) var(--ifm-navbar-item-padding-horizontal)',
              textDecoration: 'none',
            }}
          >
            Login
          </Link>
          <Link
            to="/signup"
            className="navbar__item navbar__link"
            style={{
              color: 'inherit',
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