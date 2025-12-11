/**
 * Authentication Context for the Physical AI & Humanoid Robotics textbook application
 * Manages authentication state and provides authentication functions to components
 */

import React, { createContext, useContext, useReducer, useEffect } from 'react';
import authService from '../services/authService';

// Define initial state
const initialState = {
  user: null,
  isLoading: false,
  isAuthenticated: false,
  error: null,
};

// Define reducer actions
const AuthReducer = (state, action) => {
  switch (action.type) {
    case 'SET_LOADING':
      return {
        ...state,
        isLoading: action.payload,
      };
    case 'SET_USER':
      return {
        ...state,
        user: action.payload,
        isAuthenticated: !!action.payload,
        isLoading: false,
        error: null,
      };
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
        isLoading: false,
      };
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null,
      };
    case 'LOGOUT':
      return {
        ...initialState,
        isLoading: false,
      };
    default:
      return state;
  }
};

// Create context
const AuthContext = createContext();

// AuthProvider component
export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(AuthReducer, initialState);

  // Check for existing session on app load
  useEffect(() => {
    const checkSession = async () => {
      const token = localStorage.getItem('session_token');
      if (token) {
        try {
          dispatch({ type: 'SET_LOADING', payload: true });
          const profile = await authService.getProfile();
          dispatch({ type: 'SET_USER', payload: profile });
        } catch (error) {
          console.error('Session validation failed:', error);
          localStorage.removeItem('session_token');
          dispatch({ type: 'SET_LOADING', payload: false });
        }
      } else {
        dispatch({ type: 'SET_LOADING', payload: false });
      }
    };

    checkSession();
  }, []);

  // Sign up function
  const signUp = async (userData) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const result = await authService.signUp(userData);
      const { user, session } = result;

      // Store session token - check for token field in session first, then fallback to id
      if (session) {
        if (session.token) {
          localStorage.setItem('session_token', session.token);
        } else if (session.id) {
          localStorage.setItem('session_token', session.id);
        }
      }

      dispatch({ type: 'SET_USER', payload: user });

      return { success: true, user };
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
      return { success: false, error: error.message };
    }
  };

  // Sign in function
  const signIn = async (credentials) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const result = await authService.signIn(credentials);
      const { user, session } = result;

      // Store session token - check for token field in session first, then fallback to id
      if (session) {
        if (session.token) {
          localStorage.setItem('session_token', session.token);
        } else if (session.id) {
          localStorage.setItem('session_token', session.id);
        }
      }

      dispatch({ type: 'SET_USER', payload: user });

      return { success: true, user };
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
      return { success: false, error: error.message };
    }
  };

  // Sign out function
  const signOut = async () => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      await authService.signOut();
      localStorage.removeItem('session_token');
      dispatch({ type: 'LOGOUT' });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
    }
  };

  // Update user background
  const updateBackground = async (backgroundData) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const updatedUser = await authService.updateBackground(backgroundData);
      dispatch({ type: 'SET_USER', payload: updatedUser });
      return { success: true, user: updatedUser };
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
      return { success: false, error: error.message };
    }
  };

  // Clear error function
  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  // Context value
  const value = {
    ...state,
    signUp,
    signIn,
    signOut,
    updateBackground,
    clearError,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;