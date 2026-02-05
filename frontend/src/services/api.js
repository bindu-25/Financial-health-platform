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

// Named exports - matching what your components import
export const getDashboard = async (smeId) => {
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
};

export const getSMEs = async () => {
  try {
    const response = await api.get('/smes');
    return response.data;
  } catch (error) {
    console.error('Error fetching SMEs:', error);
    return { smes: [] };
  }
};

export const getCreditScore = async (smeId) => {
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
};

export const getRecommendations = async (smeId) => {
  try {
    const response = await api.get(`/smes/${smeId}/recommendations`);
    return response.data;
  } catch (error) {
    console.error('Error fetching recommendations:', error);
    return {
      recommendations: [
        {
          title: "Improve Working Capital",
          description: "Reduce inventory holding period by 10 days to free up ₹50,000 in cash",
          priority: "high",
          impact: "High",
          timeline: "30 days"
        },
        {
          title: "Optimize Payment Terms",
          description: "Negotiate with suppliers for 45-day payment terms instead of 30",
          priority: "medium",
          impact: "Medium",
          timeline: "60 days"
        },
        {
          title: "Improve Collection Process",
          description: "Implement automated payment reminders to reduce average collection time",
          priority: "medium",
          impact: "Medium",
          timeline: "45 days"
        }
      ]
    };
  }
};

export const getFinancials = async (smeId) => {
  try {
    const response = await api.get(`/smes/${smeId}/financials`);
    return response.data;
  } catch (error) {
    console.error('Error fetching financials:', error);
    return {
      revenue: [],
      expenses: [],
      profit: []
    };
  }
};

export const getForecasts = async (smeId) => {
  try {
    const response = await api.get(`/smes/${smeId}/forecasts`);
    return response.data;
  } catch (error) {
    console.error('Error fetching forecasts:', error);
    return {
      revenue: [],
      confidence: []
    };
  }
};

export const uploadFile = async (file) => {
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
};

export const runAnalysis = async (smeId) => {
  try {
    const response = await api.post(`/smes/${smeId}/run-analysis`);
    return response.data;
  } catch (error) {
    console.error('Error running analysis:', error);
    throw error;
  }
};

export const generateReport = async (smeId, reportType) => {
  try {
    const response = await api.get(`/smes/${smeId}/reports/${reportType}`, {
      responseType: 'blob'
    });
    return response.data;
  } catch (error) {
    console.error('Error generating report:', error);
    throw error;
  }
};

export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    return { status: 'error', message: error.message };
  }
};

// Default export
export default api;