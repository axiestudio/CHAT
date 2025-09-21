import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API functions
export const flowAPI = {
  // Generate a flow
  generateFlow: async (data) => {
    const response = await api.post('/generate', data);
    return response.data;
  },

  // Get available templates
  getTemplates: async () => {
    const response = await api.get('/templates');
    return response.data;
  },

  // Get available components
  getComponents: async () => {
    const response = await api.get('/components');
    return response.data;
  },

  // Get service status
  getStatus: async () => {
    const response = await api.get('/status');
    return response.data;
  },
};

// Health check function
export const healthCheck = async () => {
  try {
    const response = await axios.get(
      process.env.REACT_APP_API_URL?.replace('/api/v1', '/health') || 'http://localhost:8000/health'
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};

export default api;
