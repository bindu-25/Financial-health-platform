import React, { useState, useEffect } from 'react';
import FinancialMetrics from './FinancialMetrics';
import CashFlowChart from './CashFlowChart';
import CreditScoreGauge from './CreditScoreGauge';
import ForecastChart from './ForecastChart';
import RecommendationsList from './RecommendationsList';
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
      const response = await fetch(`/api/smes/${smeId}/dashboard`);
      const result = await response.json();
      console.log('Dashboard data loaded:', result);
      setData(result);
      setError(null);
    } catch (err) {
      console.error('Error loading dashboard:', err);
      setError(err.message);
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

  if (error) {
    return (
      <div style={styles.error}>
        <p>{t('error', language)}: {error}</p>
        <button onClick={loadDashboard} style={styles.retryButton}>
          Retry
        </button>
      </div>
    );
  }

  if (!data) {
    return <div style={styles.error}>No data available</div>;
  }

  // Extract data with fallbacks
  const metricsData = {
    total_revenue: data.profit_loss?.revenue || data.metrics?.totalRevenue || 0,
    total_profit: data.profit_loss?.net_profit || data.metrics?.netProfit || 0,
    avg_net_margin: data.profit_loss?.margin || data.metrics?.profitMargin || 0,
    credit_score: data.credit_score?.score || data.metrics?.creditScore || 0,
    credit_rating: data.credit_score?.rating || 'N/A',
  };

  // Cash flow data
  const cashFlowData = data.cashFlow ? [
    {
      period: '6 months avg',
      cash_inflow: data.cashFlow.inflow?.reduce((a, b) => a + b, 0) / (data.cashFlow.inflow?.length || 1),
      total_cash_outflow: data.cashFlow.outflow?.reduce((a, b) => a + b, 0) / (data.cashFlow.outflow?.length || 1),
      net_cash_flow: (data.cashFlow.inflow?.reduce((a, b) => a + b, 0) - data.cashFlow.outflow?.reduce((a, b) => a + b, 0)) / (data.cashFlow.inflow?.length || 1)
    }
  ] : [];

  // Forecast data
  const forecastData = data.forecasts?.next_6_months?.map((value, idx) => ({
    period: `Month ${idx + 1}`,
    forecast_revenue: value,
    lower_bound: value * 0.9,
    upper_bound: value * 1.1,
  })) || [];

  return (
    <div style={styles.container}>
      <FinancialMetrics 
        data={metricsData}
        language={language}
      />
      
      <div style={styles.chartsRow}>
        <div style={styles.chartCol}>
          <CashFlowChart data={cashFlowData} language={language} />
        </div>
        <div style={styles.chartCol}>
          <CreditScoreGauge 
            score={metricsData.credit_score} 
            rating={metricsData.credit_rating} 
            language={language} 
          />
        </div>
      </div>

      <ForecastChart data={forecastData} language={language} />
      
      <RecommendationsList 
        recommendations={[]} 
        language={language} 
      />
    </div>
  );
};

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