import React from 'react';
import NavigationLinks from './NavigationLinks';
import CTAButton from './CTAButton';
import SearchInput from '../common/SearchInput';

/**
 * Glassmorphism card component for the book landing page
 * Features a frosted glass effect with backdrop blur
 */
const GlassmorphismCard = () => {
  // Using actual book content from the textbook
  const title = "Physical AI & Humanoid Robotics";
  const subtitle = "Tutorial • Educational • 2024";
  const synopsis = "This textbook guides you through the journey of creating embodied intelligence—AI systems that function in reality, comprehend physical laws, and engage naturally with human environments. Explore the intersection of digital AI with the physical world and understand how humanoid robots can bridge the gap between traditional AI models and real-world applications.";

  return (
    <div
      className="glass-card"
      data-testid="glassmorphism-card"
      role="region"
      aria-label="Book information card"
      style={{
        position: 'relative',
        width: '100%',
        maxWidth: '800px',
        padding: '40px',
        display: 'grid',
        gridTemplateColumns: '1fr', // Single column layout
        gap: '30px',
        alignItems: 'start'
      }}
    >
      {/* Left side: Content and navigation */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {/* Navigation links positioned top right of the card */}
        <div style={{
          display: 'flex',
          justifyContent: 'flex-end',
          gap: '20px',
          position: 'absolute',
          top: '20px',
          right: '20px'
        }}>
          <NavigationLinks />
        </div>

        {/* Title and subtitle */}
        <div style={{ marginTop: '40px' }}>
          <h1 className="title" data-testid="left-aligned" tabIndex="0">{title}</h1>
          <p className="subtitle" data-testid="left-aligned" tabIndex="0">{subtitle}</p>
        </div>

        {/* Synopsis */}
        <p className="synopsis" data-testid="left-aligned" tabIndex="0">
          {synopsis}
        </p>

        {/* CTA Button and Search - side by side on desktop, stacked on mobile */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }} data-testid="left-aligned">
          <div style={{ display: 'flex', gap: '15px', flexWrap: 'wrap', alignItems: 'center' }}>
            <CTAButton />
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', flex: 1, minWidth: '200px' }}>
              <h3 style={{ marginBottom: '0', color: 'white', fontSize: '1rem', fontWeight: '500' }} tabIndex="0">Search Chapters</h3>
              <SearchInput placeholder="Search Chapters..." />
            </div>
          </div>
        </div>
      </div>

      {/* Add responsive styles via CSS class */}
      <style jsx>{`
        @media (max-width: 768px) {
          div[data-testid="glassmorphism-card"] {
            padding: 25px;
            text-align: center;
          }

          [data-testid="left-aligned"] {
            text-align: center;
          }

          div[style*="position: absolute"] {
            position: relative !important;
            top: 0 !important;
            right: 0 !important;
            order: -1; /* Move navigation to top on mobile */
            margin-bottom: 15px;
          }

          /* On mobile, stack CTA button and search vertically */
          div[style*="display: flex"] > div[style*="flex-direction: column"] {
            display: flex !important;
            flex-direction: column !important;
          }
        }

        @media (max-width: 480px) {
          div[data-testid="glassmorphism-card"] {
            padding: 20px;
          }

          .title {
            font-size: 2rem !important;
          }

          .subtitle {
            font-size: 0.9rem !important;
          }

          .synopsis {
            font-size: 1rem !important;
          }

          div[style*="gap: 15px"] {
            flex-direction: column !important;
          }
        }
      `}</style>
    </div>
  );
};

export default GlassmorphismCard;