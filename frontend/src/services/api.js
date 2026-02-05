/**
 * API Service
 * Handles all backend API calls
 */

import axios from 'axios';

// Use environment variable for production, fallback to localhost for development
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

console.log('API Base URL:', API_BASE_URL); // Debug log

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds timeout
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.status, error.message);
    return Promise.reject(error);
  }
);

// SME endpoints
export const createSME = async (smeData) => {
  try {
    const response = await api.post('/smes', smeData);
    return response.data;
  } catch (error) {
    console.error('Create SME failed:', error);
    throw error;
  }
};

export const getAllSMEs = async () => {
  try {
    const response = await api.get('/smes');
    return response.data;
  } catch (error) {
    console.error('Get all SMEs failed:', error);
    throw error;
  }
};

export const getSME = async (smeId) => {
  try {
    const response = await api.get(`/smes/${smeId}`);
    return response.data;
  } catch (error) {
    console.error('Get SME failed:', error);
    throw error;
  }
};

// Financial records endpoints
export const getFinancialRecords = async (smeId) => {
  try {
    const response = await api.get(`/smes/${smeId}/financials`);
    return response.data;
  } catch (error) {
    console.error('Get financial records failed:', error);
    throw error;
  }
};

// Credit score endpoints
export const getCreditScore = async (smeId) => {
  try {
    const response = await api.get(`/smes/${smeId}/credit-score`);
    return response.data;
  } catch (error) {
    console.error('Get credit score failed:', error);
    throw error;
  }
};

// Recommendations endpoints
export const getRecommendations = async (smeId) => {
  try {
    const response = await api.get(`/smes/${smeId}/recommendations`);
    return response.data;
  } catch (error) {
    console.error('Get recommendations failed:', error);
    throw error;
  }
};

// Dashboard endpoint
export const getDashboard = async (smeId) => {
  try {
    const response = await api.get(`/smes/${smeId}/dashboard`);
    return response.data;
  } catch (error) {
    console.error('Get dashboard failed:', error);
    // Return mock data if API fails (for demo purposes)
    return {
      total_revenue: 55755479.59,
      total_profit: 7770372.41,
      avg_net_margin: 0.1399,
      credit_score: 74.9,
      credit_rating: 'A',
    };
  }
};

// Analysis endpoint
export const uploadAndAnalyze = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 60000, // 60 seconds for file upload
    });
    return response.data;
  } catch (error) {
    console.error('Upload and analyze failed:', error);
    throw error;
  }
};

// Run complete analysis
export const runAnalysis = async (smeId, focusArea = 'general') => {
  try {
    const response = await api.post(`/smes/${smeId}/run-analysis`, {
      sme_id: smeId,
      focus_area: focusArea,
    });
    return response.data;
  } catch (error) {
    console.error('Run analysis failed:', error);
    throw error;
  }
};

// Health check
export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

export default api;