import React from 'react';
import { TrendingUp, TrendingDown, Minus, CheckCircle, AlertCircle } from 'lucide-react';

const RBIBenchmarks = ({ language = 'en' }) => {
  const benchmarks = [
    {
      category: 'Profitability',
      metrics: [
        { name: 'Gross Profit Margin', your: 45.2, industry: 42.0, rbi: 40.0, status: 'good' },
        { name: 'Net Profit Margin', your: 14.0, industry: 12.5, rbi: 10.0, status: 'good' },
        { name: 'Return on Assets', your: 12.5, industry: 10.0, rbi: 8.0, status: 'good' },
      ],
    },
    {
      category: 'Liquidity',
      metrics: [
        { name: 'Current Ratio', your: 2.1, industry: 1.8, rbi: 1.5, status: 'good' },
        { name: 'Quick Ratio', your: 1.6, industry: 1.4, rbi: 1.0, status: 'good' },
        { name: 'Cash Ratio', your: 0.8, industry: 0.7, rbi: 0.5, status: 'good' },
      ],
    },
    {
      category: 'Leverage',
      metrics: [
        { name: 'Debt-to-Equity', your: 0.6, industry: 1.0, rbi: 2.0, status: 'excellent' },
        { name: 'Interest Coverage', your: 8.5, industry: 5.0, rbi: 3.0, status: 'excellent' },
        { name: 'Debt Service Coverage', your: 2.8, industry: 2.0, rbi: 1.5, status: 'excellent' },
      ],
    },
    {
      category: 'Efficiency',
      metrics: [
        { name: 'Asset Turnover', your: 1.4, industry: 1.2, rbi: 1.0, status: 'good' },
        { name: 'Inventory Turnover', your: 6.2, industry: 5.5, rbi: 4.0, status: 'good' },
        { name: 'Receivables Turnover', your: 10.5, industry: 9.0, rbi: 8.0, status: 'good' },
      ],
    },
  ];

  const getStatusIcon = (status) => {
    if (status === 'excellent') return <CheckCircle size={16} style={{ color: '#10b981' }} />;
    if (status === 'good') return <CheckCircle size={16} style={{ color: '#3b82f6' }} />;
    return <AlertCircle size={16} style={{ color: '#f59e0b' }} />;
  };

  const getStatusColor = (status) => {
    if (status === 'excellent') return '#10b981';
    if (status === 'good') return '#3b82f6';
    return '#f59e0b';
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div>
          <h2 style={styles.title}>RBI & Industry Benchmarks</h2>
          <p style={styles.subtitle}>Compare your performance against industry standards and RBI norms</p>
        </div>
      </div>

      {benchmarks.map((section, idx) => (
        <div key={idx} style={styles.section}>
          <h3 style={styles.sectionTitle}>{section.category} Metrics</h3>
          <div style={styles.table}>
            <div style={styles.tableHeader}>
              <div style={styles.metricName}>Metric</div>
              <div style={styles.metricValue}>Your Value</div>
              <div style={styles.metricValue}>Industry Avg</div>
              <div style={styles.metricValue}>RBI Norm</div>
              <div style={styles.metricStatus}>Status</div>
            </div>
            {section.metrics.map((metric, midx) => (
              <div key={midx} style={styles.tableRow}>
                <div style={styles.metricName}>{metric.name}</div>
                <div style={{ ...styles.metricValue, fontWeight: '600', color: getStatusColor(metric.status) }}>
                  {metric.name.includes('Ratio') || metric.name.includes('Turnover') || metric.name.includes('Coverage')
                    ? metric.your.toFixed(1)
                    : `${metric.your.toFixed(1)}%`}
                </div>
                <div style={styles.metricValue}>
                  {metric.name.includes('Ratio') || metric.name.includes('Turnover') || metric.name.includes('Coverage')
                    ? metric.industry.toFixed(1)
                    : `${metric.industry.toFixed(1)}%`}
                </div>
                <div style={styles.metricValue}>
                  {metric.name.includes('Ratio') || metric.name.includes('Turnover') || metric.name.includes('Coverage')
                    ? metric.rbi.toFixed(1)
                    : `${metric.rbi.toFixed(1)}%`}
                </div>
                <div style={styles.metricStatus}>
                  <div style={styles.statusBadge}>
                    {getStatusIcon(metric.status)}
                    <span style={{ color: getStatusColor(metric.status), textTransform: 'capitalize' }}>
                      {metric.status}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}

      <div style={styles.legend}>
        <div style={styles.legendTitle}>Performance Indicators:</div>
        <div style={styles.legendItems}>
          <div style={styles.legendItem}>
            <CheckCircle size={16} style={{ color: '#10b981' }} />
            <span>Excellent: Significantly above industry standards</span>
          </div>
          <div style={styles.legendItem}>
            <CheckCircle size={16} style={{ color: '#3b82f6' }} />
            <span>Good: Above industry average</span>
          </div>
          <div style={styles.legendItem}>
            <AlertCircle size={16} style={{ color: '#f59e0b' }} />
            <span>Fair: Near industry average</span>
          </div>
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: {
    padding: '2rem',
    minHeight: '100vh',
    backgroundColor: '#f8fafc',
  },
  header: {
    marginBottom: '2rem',
  },
  title: {
    fontSize: '2rem',
    fontWeight: '700',
    color: '#1e293b',
    marginBottom: '0.5rem',
  },
  subtitle: {
    fontSize: '0.95rem',
    color: '#64748b',
  },
  section: {
    backgroundColor: '#fff',
    borderRadius: '12px',
    padding: '1.5rem',
    marginBottom: '1.5rem',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
  },
  sectionTitle: {
    fontSize: '1.25rem',
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: '1rem',
  },
  table: {
    width: '100%',
  },
  tableHeader: {
    display: 'grid',
    gridTemplateColumns: '2fr 1fr 1fr 1fr 1fr',
    gap: '1rem',
    padding: '0.75rem 1rem',
    backgroundColor: '#f1f5f9',
    borderRadius: '8px',
    fontSize: '0.875rem',
    fontWeight: '600',
    color: '#475569',
    marginBottom: '0.5rem',
  },
  tableRow: {
    display: 'grid',
    gridTemplateColumns: '2fr 1fr 1fr 1fr 1fr',
    gap: '1rem',
    padding: '1rem',
    borderBottom: '1px solid #e2e8f0',
  },
  metricName: {
    fontSize: '0.95rem',
    color: '#1e293b',
  },
  metricValue: {
    fontSize: '0.95rem',
    color: '#64748b',
    textAlign: 'center',
  },
  metricStatus: {
    display: 'flex',
    justifyContent: 'center',
  },
  statusBadge: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    fontSize: '0.875rem',
    fontWeight: '500',
  },
  legend: {
    backgroundColor: '#fff',
    borderRadius: '12px',
    padding: '1.5rem',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
  },
  legendTitle: {
    fontSize: '1rem',
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: '1rem',
  },
  legendItems: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.75rem',
  },
  legendItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem',
    fontSize: '0.875rem',
    color: '#64748b',
  },
};

export default RBIBenchmarks;
