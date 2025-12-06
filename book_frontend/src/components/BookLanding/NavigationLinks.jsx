import React from 'react';
import Link from '@docusaurus/Link';
import { FaBook, FaSignInAlt, FaUserPlus } from 'react-icons/fa'; // Using react-icons as specified in requirements

/**
 * Navigation links for the book landing page
 * Contains links to Chapters, Login, and Signup with React icons
 */
const NavigationLinks = () => {
  return (
    <div
      style={{ display: 'flex', gap: '20px' }}
      role="navigation"
      aria-label="Main navigation"
    >
      <Link
        to="/docs/"
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '5px',
          color: 'white',
          textDecoration: 'none',
          fontWeight: '500',
          fontSize: '1rem'
        }}
        aria-label="Go to book chapters"
      >
        <FaBook aria-hidden="true" /> Chapters
      </Link>
      <Link
        to="/login"
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '5px',
          color: 'white',
          textDecoration: 'none',
          fontWeight: '500',
          fontSize: '1rem'
        }}
        aria-label="Go to login page"
      >
        <FaSignInAlt aria-hidden="true" /> Login
      </Link>
      <Link
        to="/signup"
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '5px',
          color: 'white',
          textDecoration: 'none',
          fontWeight: '500',
          fontSize: '1rem'
        }}
        aria-label="Go to signup page"
      >
        <FaUserPlus aria-hidden="true" /> Signup
      </Link>
    </div>
  );
};

export default NavigationLinks;