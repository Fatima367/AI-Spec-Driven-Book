import React from 'react';
import Link from '@docusaurus/Link';
import { FaBook } from 'react-icons/fa'; // Using react-icons as specified in requirements

/**
 * Call-to-action button for the book landing page
 * Features a gradient background and "START READING" text
 */
const CTAButton = () => {
  return (
    <Link
      to="/docs/intro" // Linking to the introduction chapter as specified in requirements
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '10px',
        padding: '16px 40px',
        background: 'linear-gradient(90deg, #00E0FF 0%, #002BFF 100%)',
        borderRadius: '50px', // Fully rounded pill shape
        color: 'white',
        textDecoration: 'none',
        fontWeight: 'bold',
        textTransform: 'uppercase', // As specified in requirements
        fontSize: '1.2rem',
        border: 'none',
        cursor: 'pointer',
        transition: 'transform 0.3s ease, box-shadow 0.3s ease',
      }}
      aria-label="Start reading the Physical AI & Humanoid Robotics textbook"
      role="button"
      onMouseEnter={(e) => {
        e.target.style.transform = 'scale(1.05)';
        e.target.style.boxShadow = '0 10px 20px rgba(0, 224, 255, 0.3)';
      }}
      onMouseLeave={(e) => {
        e.target.style.transform = 'scale(1)';
        e.target.style.boxShadow = 'none';
      }}
    >
      <FaBook aria-hidden="true" /> {/* React icon as specified in requirements */}
      START READING
    </Link>
  );
};

export default CTAButton;