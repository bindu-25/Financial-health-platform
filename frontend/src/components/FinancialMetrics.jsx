import React, { useState } from 'react';
import { TrendingUp, TrendingDown, DollarSign, Percent, Award, Info } from 'lucide-react';
import { t } from '../translations';

const FinancialMetrics = ({ data, language = 'en' }) => {
  const metrics = [
    {
      title: t('totalRevenue', language),
      value: data?.total_revenue ? `$${(data.total_revenue / 1000000).toFixed(2)}M` : 'N/A',
      change: '+12%',
      trend: 'up',
      icon: DollarSign,
      tooltip: t('totalRevenueDesc', language),
      details: [
        'Period: Last 62 months',
        'Average Monthly: $900K',
        'Peak Month: $2.48M',
      ],
    },
    {
      title: t('netProfit', language),
      value: data?.total_profit ? `$${(data.total_profit / 1000000).toFixed(2)}M` : 'N/A',
      change: '+8%',
      trend: 'up',
      icon: TrendingUp,
      tooltip: t('netProfitDesc', language),
      details: [
        'Gross Profit: $32.66M',
        'Operating Expenses: $19.51M',
        'Tax Paid: $2.96M',
      ],
    },
    {
      title: t('profitMargin', language),
      value: data?.avg_net_margin ? `${(data.avg_net_margin * 100).toFixed(1)}%` : 'N/A',
      change: 'Healthy',
      trend: 'up',
      icon: Percent,
      tooltip: t('profitMarginDesc', language),
      details: [
        'Your Margin: 14.0%',
        'Industry Avg: 12.5%',
        'Status: Above Average',
      ],
    },
    {
      title: t('creditScore', language),
      value: data?.credit_score ? `${Math.round(data.credit_score)}/100` : 'N/A',
      change: data?.credit_rating || 'N/A',
      trend: 'up',
      icon: Award,
      tooltip: t('creditScoreDesc', language),
      details: [
        'Rating: A (Good)',
        'Profitability: 81.8/100',
        'Liquidity: 100/100',
      ],
    },
  ];

  return (
    <div style={styles.container}>
      {metrics.map((metric, index) => (
        <MetricCard key={index} {...metric} />
      ))}
    </div>
  );
};

const MetricCard = ({ title, value, change, trend, icon: Icon, tooltip, details }) => {
  const [showTooltip, setShowTooltip] = useState(false);
  const TrendIcon = trend === 'up' ? TrendingUp : TrendingDown;
  const trendColor = trend === 'up' ? '#10b981' : '#ef4444';

  return (
    <div 
      style={styles.card}
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
    >
      <div style={styles.cardHeader}>
        <div style={styles.titleRow}>
          <span style={styles.cardTitle}>{title}</span>
          <Info size={14} style={styles.infoIcon} />
        </div>
        <Icon size={20} style={{ ...styles.cardIcon, color: '#1e40af' }} />
      </div>
      
      <div style={styles.cardValue}>{value}</div>
      
      <div style={styles.cardChange}>
        <TrendIcon size={14} style={{ color: trendColor }} />
        <span style={{ color: trendColor, fontSize: '0.8rem' }}>{change}</span>
      </div>

      {/* Tooltip */}
      {showTooltip && (
        <div style={styles.tooltip}>
          <div style={styles.tooltipTitle}>{tooltip}</div>
          <div style={styles.tooltipDivider}></div>
          {details.map((detail, idx) => (
            <div key={idx} style={styles.tooltipDetail}>{detail}</div>
          ))}
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    display: 'grid',
    gridTemplateColumns: 'repeat(4, 1fr)', 
    gap: '1rem',
    padding: '1.5rem 2rem',
  },
  card: {
    position: 'relative',
    backgroundColor: '#fff',
    padding: '1.25rem', // Reduced padding
    borderRadius: '10px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    border: '1px solid #e2e8f0',
    transition: 'all 0.3s ease',
    cursor: 'pointer',
    minWidth: 0, // Allow shrinking
  },
  cardHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '0.75rem',
  },
  titleRow: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.4rem',
    flex: 1,
  },
  cardTitle: {
    fontSize: '0.75rem', // Smaller font
    fontWeight: '600',
    color: '#64748b',
    textTransform: 'uppercase',
    letterSpacing: '0.03em',
    lineHeight: '1.2',
  },
  infoIcon: {
    color: '#94a3b8',
    flexShrink: 0,
  },
  cardIcon: {
    flexShrink: 0,
  },
  cardValue: {
    fontSize: '1.75rem', // Reduced from 2.25rem
    fontWeight: '700',
    color: '#1e293b',
    marginBottom: '0.4rem',
    lineHeight: '1',
  },
  cardChange: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.25rem',
    fontSize: '0.8rem',
    fontWeight: '600',
  },
  tooltip: {
    position: 'absolute',
    top: '100%',
    left: '50%',
    transform: 'translateX(-50%)',
    marginTop: '0.5rem',
    width: '280px',
    backgroundColor: '#1e293b',
    color: '#fff',
    padding: '1rem',
    borderRadius: '8px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.2)',
    zIndex: 10,
  },
  tooltipTitle: {
    fontSize: '0.85rem',
    lineHeight: '1.4',
    marginBottom: '0.75rem',
  },
  tooltipDivider: {
    height: '1px',
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    marginBottom: '0.75rem',
  },
  tooltipDetail: {
    fontSize: '0.75rem',
    color: '#cbd5e1',
    marginBottom: '0.4rem',
  },
};

// Responsive design
const mediaQuery = '@media (max-width: 1200px)';
styles.container[mediaQuery] = {
  gridTemplateColumns: 'repeat(2, 1fr)', // 2 columns on smaller screens
};

export default FinancialMetrics;