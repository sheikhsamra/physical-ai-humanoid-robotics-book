import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import FloatingChatbot from './FloatingChatbot';

// Mock fetch API for testing
global.fetch = jest.fn();

describe('FloatingChatbot Component', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders floating icon initially', () => {
    render(<FloatingChatbot />);
    const icon = screen.getByTitle('Open Chat');
    expect(icon).toBeInTheDocument();
  });

  test('toggles chat interface when icon is clicked', () => {
    render(<FloatingChatbot />);

    // Initially, the chat container should not be visible
    expect(screen.queryByRole('form')).not.toBeInTheDocument();

    // Click the floating icon to open the chat
    fireEvent.click(screen.getByTitle('Open Chat'));

    // Now the chat interface should be visible
    expect(screen.getByRole('form')).toBeInTheDocument();

    // Click the close button to close the chat
    fireEvent.click(screen.getByLabelText('Close chat'));

    // The chat interface should no longer be visible
    expect(screen.queryByRole('form')).not.toBeInTheDocument();
  });

  test('submits user message and displays bot response', async () => {
    // Mock successful API response
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        content: 'This is a test response',
        sources: []
      })
    });

    render(<FloatingChatbot />);

    // Open the chat interface
    fireEvent.click(screen.getByTitle('Open Chat'));

    // Type a message
    const input = screen.getByPlaceholderText('Ask a question about Physical AI or Humanoid Robotics...');
    fireEvent.change(input, { target: { value: 'Test question' } });

    // Submit the form
    const form = screen.getByRole('form');
    fireEvent.submit(form);

    // Wait for the response to be displayed
    await waitFor(() => {
      expect(screen.getByText('This is a test response')).toBeInTheDocument();
    });
  });

  test('displays error message when API call fails', async () => {
    // Mock API failure
    fetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
      json: async () => ({ error: 'API Error' })
    });

    render(<FloatingChatbot />);

    // Open the chat interface
    fireEvent.click(screen.getByTitle('Open Chat'));

    // Type a message
    const input = screen.getByPlaceholderText('Ask a question about Physical AI or Humanoid Robotics...');
    fireEvent.change(input, { target: { value: 'Test question' } });

    // Submit the form
    const form = screen.getByRole('form');
    fireEvent.submit(form);

    // Wait for the error message to be displayed
    await waitFor(() => {
      expect(screen.getByText(/Sorry, I encountered an error/i)).toBeInTheDocument();
    });
  });

  test('displays loading indicator during API call', async () => {
    // Create a promise that doesn't resolve immediately to simulate loading
    const mockPromise = new Promise((resolve) => {
      setTimeout(() => resolve({
        ok: true,
        json: async () => ({
          content: 'Delayed response',
          sources: []
        })
      }), 100);
    });
    fetch.mockReturnValueOnce(mockPromise);

    render(<FloatingChatbot />);

    // Open the chat interface
    fireEvent.click(screen.getByTitle('Open Chat'));

    // Type a message
    const input = screen.getByPlaceholderText('Ask a question about Physical AI or Humanoid Robotics...');
    fireEvent.change(input, { target: { value: 'Test question' } });

    // Submit the form
    const form = screen.getByRole('form');
    fireEvent.submit(form);

    // Check that loading indicator appears
    expect(screen.getByText('...')).toBeInTheDocument(); // The send button shows '...' when loading

    // Wait for the response to be displayed
    await waitFor(() => {
      expect(screen.getByText('Delayed response')).toBeInTheDocument();
    });
  });
});