// Simple test script to verify API configuration
import { API_CONFIG } from './src/config/apiConfig';

console.log('API Configuration:');
console.log('Base URL:', API_CONFIG.BASE_URL);
console.log('Chat Endpoint:', API_CONFIG.CHAT_ENDPOINT);
console.log('Ingest Endpoint:', API_CONFIG.INGEST_ENDPOINT);
console.log('Query Endpoint:', API_CONFIG.QUERY_ENDPOINT);

// Test that endpoints are properly constructed
const expectedChatEndpoint = API_CONFIG.BASE_URL + '/api/v1/chat';
const expectedIngestEndpoint = API_CONFIG.BASE_URL + '/api/v1/ingest';
const expectedQueryEndpoint = API_CONFIG.BASE_URL + '/api/v1/query';

console.log('\nEndpoint construction verification:');
console.log('Chat endpoint correct:', API_CONFIG.CHAT_ENDPOINT === expectedChatEndpoint);
console.log('Ingest endpoint correct:', API_CONFIG.INGEST_ENDPOINT === expectedIngestEndpoint);
console.log('Query endpoint correct:', API_CONFIG.QUERY_ENDPOINT === expectedQueryEndpoint);