// book_frontend/src/services/authService.ts
import { AuthClient } from '@better-auth/client';
import { UserProfileResponse, UpdateBackgroundRequest } from '../../backend/src/models'; // Assuming models are shared or re-defined

// Initialize BetterAuth client (assuming a simple client for API calls)
// This client will interact with your FastAPI backend's /api/v1/auth endpoints
export const authClient = new AuthClient({
  // baseURL: process.env.NEXT_PUBLIC_API_URL || 'https://ai-spec-driven-book-backend.up.railway.app/api/v1',
  baseURL: 'https://ai-spec-driven-book-backend.up.railway.app/api/v1', // Using direct URL for now, will use env var later
  endpoints: {
    signup: '/auth/signup',
    login: '/auth/login',
    logout: '/auth/logout',
    profile: '/auth/profile',
    updateProfile: '/auth/profile', // PUT request for general profile update
    updateBackground: '/auth/profile/background', // PUT request for background specific update
  },
  // You might need to configure how tokens are stored and sent (e.g., cookies, localStorage, Authorization header)
  // For now, assuming @better-auth/client/react's useAuth handles much of this automatically
});

// Additional service methods to interact with the backend
// These are not directly from BetterAuth's client, but helper functions for our API contract
export const getProfile = async (): Promise<UserProfileResponse> => {
  const response = await fetch(`${authClient.options.baseURL}/auth/profile`, {
    headers: {
      'Content-Type': 'application/json',
      // Assuming session token is handled by BetterAuth client or cookies
      // 'Authorization': `Bearer ${sessionToken}`
    },
  });
  if (!response.ok) {
    throw new Error('Failed to fetch user profile');
  }
  return response.json();
};

export const updateProfile = async (profileData: Partial<UserProfileResponse>): Promise<UserProfileResponse> => {
  const response = await fetch(`${authClient.options.baseURL}/auth/profile`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      // 'Authorization': `Bearer ${sessionToken}`
    },
    body: JSON.stringify(profileData),
  });
  if (!response.ok) {
    throw new Error('Failed to update user profile');
  }
  return response.json();
};

export const updateBackground = async (backgroundData: UpdateBackgroundRequest): Promise<UserProfileResponse> => {
  const response = await fetch(`${authClient.options.baseURL}/auth/profile/background`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      // 'Authorization': `Bearer ${sessionToken}`
    },
    body: JSON.stringify(backgroundData),
  });
  if (!response.ok) {
    throw new Error('Failed to update user background');
  }
  return response.json();
};