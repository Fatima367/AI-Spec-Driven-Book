import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import SearchInput from '../../src/components/common/SearchInput';

// Mock the search service
jest.mock('../../src/services/searchService', () => ({
  mockSearchBookContent: jest.fn(() => ({
    results: [
      {
        id: '1',
        title: 'Introduction to Physical AI',
        content: 'Physical AI represents a paradigm shift...',
        url: '/docs/intro',
        chapter: 'Introduction',
        score: 0.95
      }
    ],
    total: 1
  }))
}));

describe('SearchInput', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders with the correct placeholder text', () => {
    render(<SearchInput placeholder="Search the book..." />);
    
    const inputElement = screen.getByPlaceholderText('Search the book...');
    expect(inputElement).toBeInTheDocument();
  });

  it('allows user to type in the search field', () => {
    render(<SearchInput />);
    
    const inputElement = screen.getByPlaceholderText('Search Chapters');
    fireEvent.change(inputElement, { target: { value: 'Physical AI' } });
    
    expect(inputElement.value).toBe('Physical AI');
  });

  it('triggers search when Enter key is pressed', async () => {
    const mockOnSearch = jest.fn();
    render(<SearchInput onSearch={mockOnSearch} />);
    
    const inputElement = screen.getByPlaceholderText('Search Chapters');
    fireEvent.change(inputElement, { target: { value: 'Physical AI' } });
    fireEvent.keyDown(inputElement, { key: 'Enter', code: 'Enter' });
    
    // Wait for the mock search to complete
    await waitFor(() => {
      expect(mockOnSearch).toHaveBeenCalled();
    });
  });

  it('displays search results when search is performed', async () => {
    render(<SearchInput />);
    
    const inputElement = screen.getByPlaceholderText('Search Chapters');
    fireEvent.change(inputElement, { target: { value: 'Physical AI' } });
    fireEvent.keyDown(inputElement, { key: 'Enter', code: 'Enter' });
    
    // Wait for the search results to appear
    await waitFor(() => {
      const resultElement = screen.getByText('Introduction to Physical AI');
      expect(resultElement).toBeInTheDocument();
    });
  });

  it('has proper styling that matches glassmorphism aesthetic', () => {
    render(<SearchInput />);
    
    const inputElement = screen.getByPlaceholderText('Search Chapters');
    expect(inputElement).toHaveStyle({
      'backgroundColor': 'rgba(255, 255, 255, 0.05)',
      'border': '1px solid rgba(255, 255, 255, 0.1)',
      'borderRadius': '50px',
      'backdropFilter': 'blur(10px)',
    });
  });
});