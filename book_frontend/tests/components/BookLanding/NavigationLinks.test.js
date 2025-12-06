import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import NavigationLinks from '../../src/components/BookLanding/NavigationLinks';

// Mock the Link component from Docusaurus
jest.mock('@docusaurus/Link', () => {
  return ({ children, to }) => <a href={to}>{children}</a>;
});

describe('NavigationLinks', () => {
  it('renders all required navigation links', () => {
    render(
      <MemoryRouter>
        <NavigationLinks />
      </MemoryRouter>
    );
    
    // Check for the presence of all required navigation links
    expect(screen.getByText('Chapters')).toBeInTheDocument();
    expect(screen.getByText('Login')).toBeInTheDocument();
    expect(screen.getByText('Signup')).toBeInTheDocument();
  });

  it('has links with correct URLs', () => {
    render(
      <MemoryRouter>
        <NavigationLinks />
      </MemoryRouter>
    );
    
    const chaptersLink = screen.getByText('Chapters');
    const loginLink = screen.getByText('Login');
    const signupLink = screen.getByText('Signup');
    
    expect(chaptersLink).toHaveAttribute('href', '/chapters');
    expect(loginLink).toHaveAttribute('href', '/login');
    expect(signupLink).toHaveAttribute('href', '/signup');
  });

  it('applies correct styling to navigation links', () => {
    render(
      <MemoryRouter>
        <NavigationLinks />
      </MemoryRouter>
    );
    
    const links = screen.getAllByRole('link');
    links.forEach(link => {
      // Check that links have the correct color (white)
      expect(link).toHaveStyle({
        'color': 'white',
        'textDecoration': 'none',
        'fontWeight': '500',
        'fontSize': '1rem'
      });
    });
  });

  it('has proper layout and spacing', () => {
    render(
      <MemoryRouter>
        <NavigationLinks />
      </MemoryRouter>
    );
    
    const linkContainer = screen.getByText('Chapters').closest('div');
    const links = screen.getAllByRole('link');
    
    // Check that there are 3 links
    expect(links.length).toBe(3);
    
    // Check that the links are properly spaced
    expect(linkContainer).toHaveStyle({
      'display': 'flex',
      'gap': '20px'
    });
  });
});