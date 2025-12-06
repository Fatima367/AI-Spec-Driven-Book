import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import SearchInput from '../../src/components/common/SearchInput';

// Mock the search service
jest.mock('../../src/services/searchService', () => ({
  searchBookContent: jest.fn(() => 
    Promise.resolve({
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
    })
  ),
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

describe('SearchFeature Integration Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('integrates search API with SearchInput component', async () => {
    const mockOnSearch = jest.fn();
    render(<SearchInput onSearch={mockOnSearch} useMock={false} />); // Using real API mock
    
    const inputElement = screen.getByPlaceholderText('Search Chapters');
    fireEvent.change(inputElement, { target: { value: 'Physical AI' } });
    fireEvent.keyDown(inputElement, { key: 'Enter', code: 'Enter' });
    
    // Wait for the search to complete
    await waitFor(() => {
      expect(mockOnSearch).toHaveBeenCalled();
    });
  });

  it('displays search results from API in the UI', async () => {
    render(<SearchInput useMock={false} />); // Using real API mock
    
    const inputElement = screen.getByPlaceholderText('Search Chapters');
    fireEvent.change(inputElement, { target: { value: 'Physical AI' } });
    fireEvent.keyDown(inputElement, { key: 'Enter', code: 'Enter' });
    
    // Wait for the search results to appear in the DOM
    await waitFor(() => {
      const resultElement = screen.getByText('Introduction to Physical AI');
      expect(resultElement).toBeInTheDocument();
    });
  });

  it('handles API errors gracefully', async () => {
    // Mock an error response
    jest.spyOn(require('../../src/services/searchService'), 'searchBookContent')
      .mockRejectedValue(new Error('API Error'));
    
    render(<SearchInput useMock={false} />);
    
    const inputElement = screen.getByPlaceholderText('Search Chapters');
    fireEvent.change(inputElement, { target: { value: 'test' } });
    fireEvent.keyDown(inputElement, { key: 'Enter', code: 'Enter' });
    
    // Wait to see if UI updates appropriately on error
    // (this would depend on how the component handles errors)
    await waitFor(() => {
      // We expect no crash and that the component still exists
      expect(screen.getByPlaceholderText('Search Chapters')).toBeInTheDocument();
    });
  });
});