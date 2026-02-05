import axios from 'axios';

// API base URL - works in both development and production
const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API endpoints
export const apiService = {
  // Health check
  healthCheck: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      return { status: 'error', message: error.message };
    }
  },

  // SME endpoints
  getSMEs: async () => {
    try {
      const response = await api.get('/smes');
      return response.data;
    } catch (error) {
      console.error('Error fetching SMEs:', error);
      return { smes: [] };
    }
  },

  getDashboard: async (smeId) => {
    try {
      const response = await api.get(`/smes/${smeId}/dashboard`);
      return response.data;
    } catch (error) {
      console.error('Error fetching dashboard:', error);
      // Return mock data if API fails
      return {
        metrics: {
          totalRevenue: 5000000,
          netProfit: 750000,
          profitMargin: 15.0,
          creditScore: 75
        },
        cashFlow: {
          months: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
          inflow: [400000, 450000, 420000, 480000, 500000, 520000],
          outflow: [350000, 380000, 360000, 400000, 420000, 440000]
        },
        forecasts: {
          months: ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
          revenue: [540000, 560000, 580000, 600000, 620000, 640000]
        }
      };
    }
  },

  getCreditScore: async (smeId) => {
    try {
      const response = await api.get(`/smes/${smeId}/credit-score`);
      return response.data;
    } catch (error) {
      console.error('Error fetching credit score:', error);
      return {
        score: 75,
        rating: "B+",
        factors: {
          profitability: 80,
          liquidity: 75,
          leverage: 70,
          efficiency: 72
        }
      };
    }
  },

  getRecommendations: async (smeId) => {
    try {
      const response = await api.get(`/smes/${smeId}/recommendations`);
      return response.data;
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      return {
        recommendations: [
          {
            title: "Improve Working Capital",
            description: "Reduce inventory holding period by 10 days",
            priority: "high",
            impact: "High",
            timeline: "30 days"
          }
        ]
      };
    }
  },

  uploadFile: async (file) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      const response = await api.post('/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      return response.data;
    } catch (error) {
      console.error('Error uploading file:', error);
      throw error;
    }
  }
};

export default apiService;