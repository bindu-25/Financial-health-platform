import React, { useState } from 'react';
import { TrendingUp, PieChart, BarChart3, Activity } from 'lucide-react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart as RePieChart, Pie, Cell } from 'recharts';

const AnalysisSection = ({ language = 'en' }) => {
  const [activeTab, setActiveTab] = useState('trends');

  const translations = {
    en: {
      title: 'Financial Analysis',
      trends: 'Trends & Patterns',
      ratios: 'Financial Ratios',
      breakdown: 'Cost Breakdown',
      performance: 'Performance Metrics',
    },
    hi: {
      title: 'वित्तीय विश्लेषण',
      trends: 'रुझान और पैटर्न',
      ratios: 'वित्तीय अनुपात',
      breakdown: 'लागत विवरण',
      performance: 'प्रदर्शन मेट्रिक्स',
    },
  };

  const t = translations[language] || translations.en;

  // Trend data
  const trendData = [
    { month: 'Jan', revenue: 850000, profit: 120000, margin: 14.1 },
    { month: 'Feb', revenue: 920000, profit: 135000, margin: 14.7 },
    { month: 'Mar', revenue: 890000, profit: 125000, margin: 14.0 },
    { month: 'Apr', revenue: 950000, profit: 145000, margin: 15.3 },
    { month: 'May', revenue: 1020000, profit: 155000, margin: 15.2 },
    { month: 'Jun', revenue: 980000, profit: 142000, margin: 14.5 },
  ];

  // Ratios data
  const ratiosData = [
    { name: 'Current Ratio', value: 2.5, benchmark: 2.0, status: 'good' },
    { name: 'Quick Ratio', value: 1.8, benchmark: 1.5, status: 'good' },
    { name: 'Debt-to-Equity', value: 0.6, benchmark: 1.0, status: 'excellent' },
    { name: 'ROA', value: 12.5, benchmark: 10.0, status: 'good' },
  ];

  // Cost breakdown
  const costData = [
    { name: 'COGS', value: 41.4, amount: 23092791 },
    { name: 'Salaries', value: 21.0, amount: 11715000 },
    { name: 'Rent', value: 10.5, amount: 5857500 },
    { name: 'Marketing', value: 7.0, amount: 3902884 },
    { name: 'Utilities', value: 3.5, amount: 1953750 },
    { name: 'Other', value: 16.6, amount: 9257555 },
  ];

  const COLORS = ['#1e40af', '#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe', '#eff6ff'];

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>{t.title}</h2>

      {/* Tabs */}
      <div style={styles.tabs}>
        <button
          onClick={() => setActiveTab('trends')}
          style={{
            ...styles.tab,
            ...(activeTab === 'trends' && styles.tabActive),
          }}
        >
          <TrendingUp size={18} />
          {t.trends}
        </button>
        <button
          onClick={() => setActiveTab('ratios')}
          style={{
            ...styles.tab,
            ...(activeTab === 'ratios' && styles.tabActive),
          }}
        >
          <BarChart3 size={18} />
          {t.ratios}
        </button>
        <button
          onClick={() => setActiveTab('breakdown')}
          style={{
            ...styles.tab,
            ...(activeTab === 'breakdown' && styles.tabActive),
          }}
        >
          <PieChart size={18} />
          {t.breakdown}
        </button>
        <button
          onClick={() => setActiveTab('performance')}
          style={{
            ...styles.tab,
            ...(activeTab === 'performance' && styles.tabActive),
          }}
        >
          <Activity size={18} />
          {t.performance}
        </button>
      </div>

      {/* Content */}
      <div style={styles.content}>
        {activeTab === 'trends' && (
          <div style={styles.section}>
            <h3 style={styles.sectionTitle}>Revenue & Profit Trends</h3>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip />
                <Legend />
                <Line yAxisId="left" type="monotone" dataKey="revenue" stroke="#1e40af" strokeWidth={2} name="Revenue" />
                <Line yAxisId="left" type="monotone" dataKey="profit" stroke="#10b981" strokeWidth={2} name="Profit" />
                <Line yAxisId="right" type="monotone" dataKey="margin" stroke="#f59e0b" strokeWidth={2} name="Margin %" />
              </LineChart>
            </ResponsiveContainer>

            <div style={styles.insights}>
              <div style={styles.insightCard}>
                <div style={styles.insightLabel}>Growth Rate</div>
                <div style={styles.insightValue}>+18.2%</div>
                <div style={styles.insightSubtext}>Last 6 months</div>
              </div>
              <div style={styles.insightCard}>
                <div style={styles.insightLabel}>Best Month</div>
                <div style={styles.insightValue}>May</div>
                <div style={styles.insightSubtext}>₹1.02M revenue</div>
              </div>
              <div style={styles.insightCard}>
                <div style={styles.insightLabel}>Avg. Margin</div>
                <div style={styles.insightValue}>14.6%</div>
                <div style={styles.insightSubtext}>Consistent performance</div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'ratios' && (
          <div style={styles.section}>
            <h3 style={styles.sectionTitle}>Key Financial Ratios</h3>
            <div style={styles.ratioGrid}>
              {ratiosData.map((ratio, idx) => (
                <div key={idx} style={styles.ratioCard}>
                  <div style={styles.ratioName}>{ratio.name}</div>
                  <div style={styles.ratioValues}>
                    <div style={styles.ratioValue}>{ratio.value}</div>
                    <div style={styles.ratioBenchmark}>Benchmark: {ratio.benchmark}</div>
                  </div>
                  <div style={styles.ratioBar}>
                    <div 
                      style={{
                        ...styles.ratioBarFill,
                        width: `${(ratio.value / (ratio.benchmark * 1.5)) * 100}%`,
                        backgroundColor: ratio.status === 'excellent' ? '#10b981' : '#3b82f6',
                      }}
                    ></div>
                  </div>
                  <div style={{
                    ...styles.ratioStatus,
                    color: ratio.status === 'excellent' ? '#10b981' : '#3b82f6',
                  }}>
                    {ratio.status === 'excellent' ? 'Excellent' : 'Good'}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'breakdown' && (
          <div style={styles.section}>
            <h3 style={styles.sectionTitle}>Cost Structure Analysis</h3>
            <div style={styles.breakdownGrid}>
              <div style={styles.pieChartContainer}>
                <ResponsiveContainer width="100%" height={300}>
                  <RePieChart>
                    <Pie
                      data={costData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, value }) => `${name}: ${value}%`}
                      outerRadius={100}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {costData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </RePieChart>
                </ResponsiveContainer>
              </div>
              <div style={styles.breakdownList}>
                {costData.map((item, idx) => (
                  <div key={idx} style={styles.breakdownItem}>
                    <div style={styles.breakdownItemHeader}>
                      <div 
                        style={{
                          ...styles.breakdownDot,
                          backgroundColor: COLORS[idx % COLORS.length],
                        }}
                      ></div>
                      <span style={styles.breakdownItemName}>{item.name}</span>
                    </div>
                    <div style={styles.breakdownItemValue}>
                      ₹{(item.amount / 1000000).toFixed(2)}M ({item.value}%)
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'performance' && (
          <div style={styles.section}>
            <h3 style={styles.sectionTitle}>Performance Scorecard</h3>
            <div style={styles.scorecardGrid}>
              <ScoreCard title="Profitability" score={82} max={100} color="#10b981" />
              <ScoreCard title="Liquidity" score={95} max={100} color="#3b82f6" />
              <ScoreCard title="Efficiency" score={68} max={100} color="#f59e0b" />
              <ScoreCard title="Growth" score={76} max={100} color="#8b5cf6" />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

const ScoreCard = ({ title, score, max, color }) => (
  <div style={styles.scoreCard}>
    <div style={styles.scoreTitle}>{title}</div>
    <div style={styles.scoreCircle}>
      <svg width="120" height="120" viewBox="0 0 120 120">
        <circle cx="60" cy="60" r="50" fill="none" stroke="#e2e8f0" strokeWidth="10" />
        <circle 
          cx="60" 
          cy="60" 
          r="50" 
          fill="none" 
          stroke={color} 
          strokeWidth="10"
          strokeDasharray={`${(score / max) * 314} 314`}
          strokeLinecap="round"
          transform="rotate(-90 60 60)"
        />
        <text x="60" y="65" textAnchor="middle" fontSize="24" fontWeight="bold" fill="#1e293b">
          {score}
        </text>
      </svg>
    </div>
    <div style={styles.scoreLabel}>Score: {score}/{max}</div>
  </div>
);

const styles = {
  container: {
    padding: '2rem',
    minHeight: '100vh',
  },
  title: {
    fontSize: '2rem',
    fontWeight: '700',
    color: '#1e293b',
    marginBottom: '2rem',
  },
  tabs: {
    display: 'flex',
    gap: '1rem',
    marginBottom: '2rem',
    borderBottom: '2px solid #e2e8f0',
  },
  tab: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    padding: '0.75rem 1.5rem',
    backgroundColor: 'transparent',
    border: 'none',
    borderBottom: '3px solid transparent',
    fontSize: '0.95rem',
    fontWeight: '500',
    color: '#64748b',
    cursor: 'pointer',
    transition: 'all 0.2s',
    marginBottom: '-2px',
  },
  tabActive: {
    color: '#1e40af',
    borderBottomColor: '#1e40af',
  },
  content: {
    backgroundColor: '#fff',
    borderRadius: '12px',
    padding: '2rem',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
  },
  section: {
    minHeight: '400px',
  },
  sectionTitle: {
    fontSize: '1.25rem',
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: '1.5rem',
  },
  insights: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '1rem',
    marginTop: '2rem',
  },
  insightCard: {
    backgroundColor: '#f8fafc',
    padding: '1.5rem',
    borderRadius: '8px',
    textAlign: 'center',
  },
  insightLabel: {
    fontSize: '0.875rem',
    color: '#64748b',
    marginBottom: '0.5rem',
  },
  insightValue: {
    fontSize: '2rem',
    fontWeight: '700',
    color: '#1e293b',
  },
  insightSubtext: {
    fontSize: '0.75rem',
    color: '#94a3b8',
    marginTop: '0.25rem',
  },
  ratioGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '1.5rem',
  },
  ratioCard: {
    backgroundColor: '#f8fafc',
    padding: '1.5rem',
    borderRadius: '8px',
  },
  ratioName: {
    fontSize: '1rem',
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: '1rem',
  },
  ratioValues: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'baseline',
    marginBottom: '0.75rem',
  },
  ratioValue: {
    fontSize: '1.75rem',
    fontWeight: '700',
    color: '#1e40af',
  },
  ratioBenchmark: {
    fontSize: '0.75rem',
    color: '#64748b',
  },
  ratioBar: {
    height: '8px',
    backgroundColor: '#e2e8f0',
    borderRadius: '4px',
    overflow: 'hidden',
    marginBottom: '0.5rem',
  },
  ratioBarFill: {
    height: '100%',
    transition: 'width 0.5s ease',
  },
  ratioStatus: {
    fontSize: '0.875rem',
    fontWeight: '600',
    textAlign: 'right',
  },
  breakdownGrid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '2rem',
  },
  pieChartContainer: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  breakdownList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
  },
  breakdownItem: {
    padding: '1rem',
    backgroundColor: '#f8fafc',
    borderRadius: '8px',
  },
  breakdownItemHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem',
    marginBottom: '0.5rem',
  },
  breakdownDot: {
    width: '12px',
    height: '12px',
    borderRadius: '50%',
  },
  breakdownItemName: {
    fontSize: '0.875rem',
    fontWeight: '600',
    color: '#1e293b',
  },
  breakdownItemValue: {
    fontSize: '1rem',
    fontWeight: '700',
    color: '#1e40af',
    paddingLeft: '1.75rem',
  },
  scorecardGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '2rem',
  },
  scoreCard: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '1.5rem',
    backgroundColor: '#f8fafc',
    borderRadius: '8px',
  },
  scoreTitle: {
    fontSize: '1rem',
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: '1rem',
  },
  scoreCircle: {
    marginBottom: '1rem',
  },
  scoreLabel: {
    fontSize: '0.875rem',
    color: '#64748b',
  },
};

export default AnalysisSection;