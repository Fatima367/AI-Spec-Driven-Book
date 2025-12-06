import React from 'react';
import { render, screen } from '@testing-library/react';
import GlassmorphismCard from '../../src/components/BookLanding/GlassmorphismCard';

// This test will fail initially as per the task requirements until we implement the component
describe('GlassmorphismCard', () => {
  it('renders with glassmorphism styling', () => {
    // This test should fail initially since the component doesn't exist yet
    // We're verifying the test fails as expected before implementing the component
    render(<GlassmorphismCard />);

    // Check for the glassmorphism effect in the DOM
    const glassCard = screen.getByTestId('glassmorphism-card');
    expect(glassCard).toHaveClass('glass-card');

    // Check for backdrop filter property
    expect(glassCard).toHaveStyle({
      'backdropFilter': 'blur(25px)',
      'WebkitBackdropFilter': 'blur(25px)',
      'backgroundColor': 'rgba(255, 255, 255, 0.03)',
      'border': '1px solid rgba(255, 255, 255, 0.1)',
    });
  });

  it('displays book information correctly', () => {
    render(<GlassmorphismCard />);

    expect(screen.getByText('Physical AI & Humanoid Robotics')).toBeInTheDocument();
    expect(screen.getByText('Tutorial • Educational • 2024')).toBeInTheDocument();
    expect(screen.getByText(/This textbook guides you through the journey/i)).toBeInTheDocument();
  });

  it('has proper content alignment (title, synopsis, button on left)', () => {
    render(<GlassmorphismCard />);

    // The test should verify the layout structure
    const glassCard = screen.getByTestId('glassmorphism-card');
    expect(glassCard).toBeInTheDocument();

    // Check if elements are positioned as specified in requirements
    const leftAlignedElements = screen.getAllByTestId('left-aligned');
    expect(leftAlignedElements.length).toBeGreaterThan(0);

    // Check if search input is on the right side
    const rightAlignedElements = screen.getAllByTestId('right-aligned');
    expect(rightAlignedElements.length).toBeGreaterThan(0);
  });
});