import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, ComposedChart } from 'recharts';

const ForecastChart = ({ data }) => {
  const chartData = data?.map(item => ({
    period: item.period,
    forecast: item.forecast_revenue,
    lower: item.lower_bound,
    upper: item.upper_bound,
  })) || [];

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>6-Month Revenue Forecast</h3>
      <p style={styles.subtitle}>
        Predicted revenue with confidence intervals
      </p>
      
      <ResponsiveContainer width="100%" height={300}>
        <ComposedChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="period" />
          <YAxis />
          <Tooltip formatter={(value) => `$${value?.toLocaleString() || 0}`} />
          <Legend />
          
          {/* Confidence interval area */}
          <Area
            type="monotone"
            dataKey="upper"
            fill="#93c5fd"
            stroke="none"
            fillOpacity={0.3}
            name="Upper Bound"
          />
          <Area
            type="monotone"
            dataKey="lower"
            fill="#93c5fd"
            stroke="none"
            fillOpacity={0.3}
            name="Lower Bound"
          />
          
          {/* Forecast line */}
          <Line
            type="monotone"
            dataKey="forecast"
            stroke="#1e40af"
            strokeWidth={3}
            dot={{ r: 4 }}
            name="Forecast"
          />
        </ComposedChart>
      </ResponsiveContainer>

      <div style={styles.info}>
        <div style={styles.infoItem}>
          <span style={styles.infoLabel}>Average Forecast:</span>
          <span style={styles.infoValue}>
            ${chartData.length > 0 
              ? (chartData.reduce((sum, d) => sum + d.forecast, 0) / chartData.length).toLocaleString(undefined, {maximumFractionDigits: 0})
              : 0
            }
          </span>
        </div>
        <div style={styles.infoItem}>
          <span style={styles.infoLabel}>Total 6-Month:</span>
          <span style={styles.infoValue}>
            ${chartData.reduce((sum, d) => sum + d.forecast, 0).toLocaleString(undefined, {maximumFractionDigits: 0})}
          </span>
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: {
    backgroundColor: '#fff',
    padding: '1.5rem',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    border: '1px solid #e2e8f0',
    margin: '2rem',
  },
  title: {
    fontSize: '1.25rem',
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: '0.25rem',
  },
  subtitle: {
    fontSize: '0.875rem',
    color: '#64748b',
    marginBottom: '1rem',
  },
  info: {
    display: 'flex',
    gap: '2rem',
    marginTop: '1rem',
    paddingTop: '1rem',
    borderTop: '1px solid #e2e8f0',
  },
  infoItem: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.25rem',
  },
  infoLabel: {
    fontSize: '0.75rem',
    color: '#64748b',
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
  },
  infoValue: {
    fontSize: '1.25rem',
    fontWeight: '600',
    color: '#1e293b',
  },
};

export default ForecastChart;