// API Configuration
// For Docusaurus, we need to handle environment variables differently
const getApiBaseUrl = () => {
  if (typeof window !== 'undefined') {
    // Client-side
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      return 'http://127.0.0.1:8000';
    } else {
      // Production URL - adjust as needed
      return 'https://ai-spec-driven-book-backend.up.railway.app';
    }
  }
  // Fallback for server-side
  return 'http://127.0.0.1:8000';
};

const API_BASE_URL = getApiBaseUrl();
const API_VERSION = '/api/v1';

export const API_CONFIG = {
  BASE_URL: API_BASE_URL,
  CHAT_ENDPOINT: `${API_BASE_URL}${API_VERSION}/chat`,
  INGEST_ENDPOINT: `${API_BASE_URL}${API_VERSION}/ingest`,
  QUERY_ENDPOINT: `${API_BASE_URL}${API_VERSION}/query`,
  AUTH_ENDPOINTS: {
    SIGNUP: `${API_BASE_URL}${API_VERSION}/auth/signup`,
    LOGIN: `${API_BASE_URL}${API_VERSION}/auth/login`,
    LOGOUT: `${API_BASE_URL}${API_VERSION}/auth/logout`,
    PROFILE: `${API_BASE_URL}${API_VERSION}/auth/profile`,
    UPDATE_BACKGROUND: `${API_BASE_URL}${API_VERSION}/auth/profile/background`,
  }
};