import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const CashFlowChart = ({ data }) => {
  // Transform data for chart
  const chartData = data?.map(item => ({
    period: item.period,
    inflow: item.cash_inflow,
    outflow: item.total_cash_outflow,
    net: item.net_cash_flow,
  })) || [];

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>Cash Flow Analysis</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="period" />
          <YAxis />
          <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="inflow" 
            stroke="#10b981" 
            strokeWidth={2}
            name="Cash Inflow"
          />
          <Line 
            type="monotone" 
            dataKey="outflow" 
            stroke="#ef4444" 
            strokeWidth={2}
            name="Cash Outflow"
          />
          <Line 
            type="monotone" 
            dataKey="net" 
            stroke="#1e40af" 
            strokeWidth={2}
            name="Net Cash Flow"
          />
        </LineChart>
      </ResponsiveContainer>
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
    marginBottom: '1rem',
  },
};

export default CashFlowChart;