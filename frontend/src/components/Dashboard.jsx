import React, { useState, useEffect } from 'react';
import FinancialMetrics from './FinancialMetrics';
import CashFlowChart from './CashFlowChart';
import CreditScoreGauge from './CreditScoreGauge';
import ForecastChart from './ForecastChart';
import RecommendationsList from './RecommendationsList';
import { getDashboard } from '../services/api';
import { t } from '../translations';

const Dashboard = ({ smeId = 1, language = 'en' }) => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboard();
  }, [smeId]);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const result = await getDashboard(smeId);
      setData(result);
    } catch (err) {
      setError(err.message);
      // Use mock data for demo
      setData(mockData);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={styles.loading}>
        <div style={styles.spinner}></div>
        <p>{t('loading', language)}...</p>
      </div>
    );
  }

  if (error && !data) {
    return (
      <div style={styles.error}>
        <p>{t('error', language)}: {error}</p>
        <button onClick={loadDashboard} style={styles.retryButton}>
          Retry
        </button>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <FinancialMetrics 
        data={{
          total_revenue: 55755479.59,
          total_profit: 7770372.41,
          avg_net_margin: 0.1399,
          credit_score: 74.9,
          credit_rating: 'A',
        }}
        language={language}
      />
      
      <div style={styles.chartsRow}>
        <div style={styles.chartCol}>
          <CashFlowChart data={mockCashFlowData} language={language} />
        </div>
        <div style={styles.chartCol}>
          <CreditScoreGauge score={74.9} rating="A" language={language} />
        </div>
      </div>

      <ForecastChart data={mockForecastData} language={language} />
      
      <RecommendationsList recommendations={[]} language={language} />
    </div>
  );
};

// Mock data for demo
const mockCashFlowData = [
  { period: '2021-01', cash_inflow: 900000, total_cash_outflow: 750000, net_cash_flow: 150000 },
  { period: '2021-02', cash_inflow: 950000, total_cash_outflow: 780000, net_cash_flow: 170000 },
  { period: '2021-03', cash_inflow: 1000000, total_cash_outflow: 800000, net_cash_flow: 200000 },
];

const mockForecastData = [
  { period: '2021-04', forecast_revenue: 850000, lower_bound: 750000, upper_bound: 950000 },
  { period: '2021-05', forecast_revenue: 880000, lower_bound: 770000, upper_bound: 990000 },
  { period: '2021-06', forecast_revenue: 920000, lower_bound: 800000, upper_bound: 1040000 },
  { period: '2021-07', forecast_revenue: 950000, lower_bound: 820000, upper_bound: 1080000 },
  { period: '2021-08', forecast_revenue: 980000, lower_bound: 850000, upper_bound: 1110000 },
  { period: '2021-09', forecast_revenue: 1000000, lower_bound: 870000, upper_bound: 1130000 },
];

const mockData = {};

const styles = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#f8fafc',
  },
  loading: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh',
    gap: '1rem',
  },
  spinner: {
    width: '40px',
    height: '40px',
    border: '4px solid #e2e8f0',
    borderTop: '4px solid #1e40af',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
  },
  error: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh',
    gap: '1rem',
  },
  retryButton: {
    padding: '0.75rem 1.5rem',
    backgroundColor: '#1e40af',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
  },
  chartsRow: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '0',
    padding: '0 2rem',
  },
  chartCol: {
    minHeight: '300px',
  },
};

export default Dashboard;