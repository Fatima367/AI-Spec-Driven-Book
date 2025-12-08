import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Chatbot from '../Chatbot';
import { selectionService } from '../../../services/selection_service';

// Mock the fetch API
global.fetch = jest.fn();

// Mock selectionService
jest.mock('../../../services/selection_service', () => ({
  selectionService: {
    getSelectedText: jest.fn(() => null),
    addSelectionChangeListener: jest.fn(() => () => {}), // Return a no-op unsubscribe
  },
}));

describe('Chatbot', () => {
  beforeEach(() => {
    // Reset mocks before each test
    (fetch as jest.Mock).mockClear();
    (selectionService.getSelectedText as jest.Mock).mockClear();
    (selectionService.addSelectionChangeListener as jest.Mock).mockClear();
  });

  it('renders the chatbot button initially', () => {
    render(<Chatbot />);
    expect(screen.getByRole('button', { name: /ask book/i })).toBeInTheDocument();
  });

  it('opens the chatbot window when the button is clicked', () => {
    render(<Chatbot />);
    fireEvent.click(screen.getByRole('button', { name: /ask book/i }));
    expect(screen.getByText(/book assistant/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/ask a question/i)).toBeInTheDocument();
  });

  it('displays the welcome message when no messages are present', () => {
    render(<Chatbot />);
    fireEvent.click(screen.getByRole('button', { name: /ask book/i }));
    expect(screen.getByText(/hello! i'm your book assistant/i)).toBeInTheDocument();
  });

  it('sends a user message and receives a bot response', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ answer: 'Hello from bot!', citations: [] }),
    });

    render(<Chatbot />);
    fireEvent.click(screen.getByRole('button', { name: /ask book/i }));

    const input = screen.getByPlaceholderText(/ask a question/i);
    fireEvent.change(input, { target: { value: 'Hi bot!' } });
    fireEvent.click(screen.getByRole('button', { name: /send/i }));

    expect(screen.getByText('Hi bot!')).toBeInTheDocument();
    expect(input).toHaveValue(''); // Input should be cleared

    await waitFor(() => {
      expect(screen.getByText('Hello from bot!')).toBeInTheDocument();
    });
    expect(fetch).toHaveBeenCalledTimes(1);
    expect(fetch).toHaveBeenCalledWith(
      'https://ai-spec-driven-book-production.up.railway.app/api/v1/chat',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({
          query: 'Hi bot!',
          user_id: 'anonymous-user',
          selected_text: null,
        }),
      }),
    );
  });

  it('sends selected text with the query', async () => {
    (selectionService.getSelectedText as jest.Mock).mockReturnValue('selected book text');
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ answer: 'Answer with selection context.', citations: [] }),
    });

    render(<Chatbot />);
    fireEvent.click(screen.getByRole('button', { name: /ask book/i }));

    const input = screen.getByPlaceholderText(/ask a question/i);
    fireEvent.change(input, { target: { value: 'Explain this' } });
    fireEvent.click(screen.getByRole('button', { name: /send/i }));

    await waitFor(() => {
      expect(screen.getByText('Answer with selection context.')).toBeInTheDocument();
    });

    expect(fetch).toHaveBeenCalledWith(
      'https://ai-spec-driven-book-production.up.railway.app/api/v1/chat',
      expect.objectContaining({
        body: JSON.stringify({
          query: 'Explain this',
          user_id: 'anonymous-user',
          selected_text: 'selected book text',
        }),
      }),
    );
  });

  it('displays citations when provided in the bot response', async () => {
    const mockCitations = [{ doc_id: 'Intro', chunk_id: 'intro-1', url: '/docs/intro' }];
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ answer: 'Here is some info.', citations: mockCitations }),
    });

    render(<Chatbot />);
    fireEvent.click(screen.getByRole('button', { name: /ask book/i }));

    const input = screen.getByPlaceholderText(/ask a question/i);
    fireEvent.change(input, { target: { value: 'Info' } });
    fireEvent.click(screen.getByRole('button', { name: /send/i }));

    await waitFor(() => {
      expect(screen.getByText('Here is some info.')).toBeInTheDocument();
      expect(screen.getByText('Sources:')).toBeInTheDocument();
      expect(screen.getByRole('link', { name: /intro/i })).toHaveAttribute('href', '/docs/intro');
    });
  });

  it('handles API errors gracefully', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 500,
      json: async () => ({ detail: 'Internal Server Error' }),
    });

    render(<Chatbot />);
    fireEvent.click(screen.getByRole('button', { name: /ask book/i }));

    const input = screen.getByPlaceholderText(/ask a question/i);
    fireEvent.change(input, { target: { value: 'Error query' } });
    fireEvent.click(screen.getByRole('button', { name: /send/i }));

    await waitFor(() => {
      expect(
        screen.getByText(/sorry, i encountered an error processing your request/i),
      ).toBeInTheDocument();
    });
  });

  it('handles network errors gracefully', async () => {
    (fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

    render(<Chatbot />);
    fireEvent.click(screen.getByRole('button', { name: /ask book/i }));

    const input = screen.getByPlaceholderText(/ask a question/i);
    fireEvent.change(input, { target: { value: 'Network query' } });
    fireEvent.click(screen.getByRole('button', { name: /send/i }));

    await waitFor(() => {
      expect(
        screen.getByText(/sorry, i'm having trouble connecting to the server/i),
      ).toBeInTheDocument();
    });
  });
});
