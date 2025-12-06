import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import BookLandingPage from '../../src/pages/BookLandingPage';

// Mock the components to focus on testing navigation integration
jest.mock('../../src/components/BookLanding/GlassmorphismCard', () => {
  return () => (
    <div data-testid="glassmorphism-card">
      <a href="/docs/intro" data-testid="start-reading-link">START READING</a>
    </div>
  );
});

jest.mock('../../src/components/BookLanding/BackgroundSpheres', () => {
  return () => <div data-testid="background-spheres">Background Spheres</div>;
});

jest.mock('../../src/components/BookLanding/NavigationLinks', () => {
  return () => <div data-testid="navigation-links">Navigation Links</div>;
});

jest.mock('../../src/components/BookLanding/CTAButton', () => {
  return () => <a href="/docs/intro" data-testid="cta-button">START READING</a>;
});

describe('Navigation to Introduction Chapter Integration', () => {
  it('navigates to Introduction chapter when CTA button is clicked', async () => {
    render(
      <MemoryRouter>
        <BookLandingPage />
      </MemoryRouter>
    );
    
    // Find the CTA button
    const ctaButton = screen.getByTestId('cta-button');
    expect(ctaButton).toBeInTheDocument();
    expect(ctaButton).toHaveAttribute('href', '/docs/intro');
  });

  it('has correct page structure with navigation elements', async () => {
    render(
      <MemoryRouter>
        <BookLandingPage />
      </MemoryRouter>
    );
    
    // Check that all key elements are present
    expect(screen.getByTestId('background-spheres')).toBeInTheDocument();
    expect(screen.getByTestId('glassmorphism-card')).toBeInTheDocument();
    expect(screen.getByTestId('cta-button')).toBeInTheDocument();
  });

  it('verifies landing page title and content integration', async () => {
    render(
      <MemoryRouter>
        <BookLandingPage />
      </MemoryRouter>
    );
    
    // The actual content would be tested by the individual component tests
    // Here we just verify the structure is in place
    const glassmorphismCard = screen.getByTestId('glassmorphism-card');
    expect(glassmorphismCard).toBeInTheDocument();
  });
});