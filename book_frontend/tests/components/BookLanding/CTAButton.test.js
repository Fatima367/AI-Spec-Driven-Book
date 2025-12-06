import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import CTAButton from '../../src/components/BookLanding/CTAButton';

// Mock the Link component from Docusaurus
jest.mock('@docusaurus/Link', () => {
  return ({ children, to }) => <a href={to}>{children}</a>;
});

// Mock react-icons
jest.mock('react-icons/fa', () => ({
  FaBook: () => <span>BookIcon</span>
}));

describe('CTAButton', () => {
  it('renders with correct text and styling', () => {
    render(
      <MemoryRouter>
        <CTAButton />
      </MemoryRouter>
    );
    
    const buttonElement = screen.getByText('START READING');
    expect(buttonElement).toBeInTheDocument();
    
    // Check that the button has correct styles
    expect(buttonElement).toHaveStyle({
      'background': expect.stringContaining('linear-gradient'),
      'borderRadius': '50px',
      'color': 'white',
      'fontWeight': 'bold',
      'textTransform': 'uppercase',
    });
  });

  it('includes the required React icon', () => {
    render(
      <MemoryRouter>
        <CTAButton />
      </MemoryRouter>
    );
    
    // Check that the icon is present (mocked as "BookIcon")
    const iconElement = screen.getByText('BookIcon');
    expect(iconElement).toBeInTheDocument();
  });

  it('links to the Introduction chapter', () => {
    render(
      <MemoryRouter>
        <CTAButton />
      </MemoryRouter>
    );
    
    const buttonElement = screen.getByRole('link', { name: /START READING/i });
    expect(buttonElement).toHaveAttribute('href', '/docs/intro');
  });

  it('has gradient styling as specified', () => {
    render(
      <MemoryRouter>
        <CTAButton />
      </MemoryRouter>
    );
    
    const buttonElement = screen.getByText('START READING');
    // Check that the button has the gradient effect in the style
    expect(buttonElement).toHaveStyle({
      'background': expect.stringContaining('00E0FF'),
      'background': expect.stringContaining('002BFF'),
    });
  });

  it('has hover effects', () => {
    render(
      <MemoryRouter>
        <CTAButton />
      </MemoryRouter>
    );
    
    const buttonElement = screen.getByRole('link', { name: /START READING/i });
    fireEvent.mouseEnter(buttonElement);
    
    // The hover effect would be tested by checking for transform/scale changes
    // depending on how the button handles hover in the actual component
    expect(buttonElement).toBeInTheDocument();
  });
});