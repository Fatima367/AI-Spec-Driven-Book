import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import SignupForm from '../../../src/components/Auth/SignupForm';
import { AuthContext } from '../../../src/contexts/AuthContext';

// Mock the AuthContext
const mockSignUp = jest.fn();
const mockAuthContext = {
  user: null,
  signIn: jest.fn(),
  signUp: mockSignUp,
  signOut: jest.fn(),
  updateProfile: jest.fn(),
  updateBackground: jest.fn(),
  session: null,
  isLoading: false,
};

describe('SignupForm', () => {
  beforeEach(() => {
    mockSignUp.mockClear();
    // Reset any state in mockAuthContext if necessary
  });

  it('renders the signup form with email, password, and background fields', () => {
    render(
      <AuthContext.Provider value={mockAuthContext}>
        <SignupForm />
      </AuthContext.Provider>
    );

    expect(screen.getByLabelText(/Email:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Password:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/First Name:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Last Name:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Software Experience:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Hardware Experience:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Technical Background:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Primary Programming Language:/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Sign Up/i })).toBeInTheDocument();
  });

  it('calls signUp with correct data on form submission', async () => {
    render(
      <AuthContext.Provider value={mockAuthContext}>
        <SignupForm />
      </AuthContext.Provider>
    );

    fireEvent.change(screen.getByLabelText(/Email:/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByLabelText(/Password:/i), { target: { value: 'password123' } });
    fireEvent.change(screen.getByLabelText(/First Name:/i), { target: { value: 'John' } });
    fireEvent.change(screen.getByLabelText(/Last Name:/i), { target: { value: 'Doe' } });
    fireEvent.change(screen.getByLabelText(/Software Experience:/i), { target: { value: 'intermediate' } });
    fireEvent.change(screen.getByLabelText(/Hardware Experience:/i), { target: { value: 'beginner' } });
    fireEvent.change(screen.getByLabelText(/Technical Background:/i), { target: { value: 'computer_science' } });
    fireEvent.change(screen.getByLabelText(/Primary Programming Language:/i), { target: { value: 'python' } });

    fireEvent.click(screen.getByRole('button', { name: /Sign Up/i }));

    await waitFor(() => {
      expect(mockSignUp).toHaveBeenCalledTimes(1);
      expect(mockSignUp).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
        firstName: 'John',
        lastName: 'Doe',
        softwareExperience: 'intermediate',
        hardwareExperience: 'beginner',
        technicalBackground: 'computer_science',
        primaryProgrammingLanguage: 'python',
      });
    });
  });

  it('displays an error message if signUp fails', async () => {
    const errorMessage = 'An error occurred during signup';
    mockSignUp.mockImplementationOnce(() => Promise.reject(new Error('API Error'))); // Simulate API error

    render(
      <AuthContext.Provider value={mockAuthContext}>
        <SignupForm />
      </AuthContext.Provider>
    );

    fireEvent.change(screen.getByLabelText(/Email:/i), { target: { value: 'fail@example.com' } });
    fireEvent.change(screen.getByLabelText(/Password:/i), { target: { value: 'password123' } });
    fireEvent.click(screen.getByRole('button', { name: /Sign Up/i }));

    await waitFor(() => {
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });
  });

  it('shows loading state during signup', async () => {
    mockSignUp.mockImplementation(() => new Promise((resolve) => setTimeout(() => resolve({ success: true }), 100))); // Simulate async call

    render(
      <AuthContext.Provider value={mockAuthContext}>
        <SignupForm />
      </AuthContext.Provider>
    );

    fireEvent.change(screen.getByLabelText(/Email:/i), { target: { value: 'loading@example.com' } });
    fireEvent.change(screen.getByLabelText(/Password:/i), { target: { value: 'password123' } });
    fireEvent.click(screen.getByRole('button', { name: /Sign Up/i }));

    expect(screen.getByRole('button', { name: /Creating Account.../i })).toBeDisabled();

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /Sign Up/i })).toBeEnabled();
    });
  });
});