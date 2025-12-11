/**
 * Authentication service for the Physical AI & Humanoid Robotics textbook application
 * Uses BetterAuth client to communicate with our Python backend auth API
 */

import { API_CONFIG } from '../config/apiConfig';

// Convenience functions that match the API contract defined in our spec
export const authService = {
  // Sign up with background questions
  async signUp(userData) {
    try {
      const response = await fetch(API_CONFIG.AUTH_ENDPOINTS.SIGNUP, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Signup failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Signup error:', error);
      throw error;
    }
  },

  // Login
  async signIn(credentials) {
    try {
      const response = await fetch(API_CONFIG.AUTH_ENDPOINTS.LOGIN, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Login failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },

  // Logout
  async signOut() {
    try {
      // Get the session token from wherever it's stored (cookies, localStorage, etc.)
      const token = localStorage.getItem('session_token'); // or however the token is stored

      if (token) {
        const response = await fetch(API_CONFIG.AUTH_ENDPOINTS.LOGOUT, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          // Even if the server logout fails, we should still clear the local token
          console.warn('Server logout failed, but clearing local session anyway');
        }
      }

      // Clear the stored token
      localStorage.removeItem('session_token');

      return { message: 'Successfully logged out' };
    } catch (error) {
      console.error('Logout error:', error);
      // Still clear local token even if there's an error
      localStorage.removeItem('session_token');
      throw error;
    }
  },

  // Get user profile
  async getProfile() {
    try {
      // Get the session token from wherever it's stored
      const token = localStorage.getItem('session_token'); // or however the token is stored

      const response = await fetch(API_CONFIG.AUTH_ENDPOINTS.PROFILE, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Failed to get profile');
      }

      return await response.json();
    } catch (error) {
      console.error('Get profile error:', error);
      throw error;
    }
  },

  // Update user background
  async updateBackground(backgroundData) {
    try {
      // Get the session token from wherever it's stored
      const token = localStorage.getItem('session_token'); // or however the token is stored

      const response = await fetch(API_CONFIG.AUTH_ENDPOINTS.UPDATE_BACKGROUND, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(backgroundData),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Failed to update background');
      }

      return await response.json();
    } catch (error) {
      console.error('Update background error:', error);
      throw error;
    }
  }
};

export default authService;