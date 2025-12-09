// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL ||
                    process.env.NODE_ENV === 'production'
                    ? 'https://ai-spec-driven-book-backend.up.railway.app' // Replace with your actual Vercel deployment URL
                    : 'http://127.0.0.1:8000';

const API_VERSION = '/api/v1';

export const API_CONFIG = {
  BASE_URL: API_BASE_URL,
  CHAT_ENDPOINT: `${API_BASE_URL}${API_VERSION}/chat`,
  INGEST_ENDPOINT: `${API_BASE_URL}${API_VERSION}/ingest`,
  QUERY_ENDPOINT: `${API_BASE_URL}${API_VERSION}/query`
};