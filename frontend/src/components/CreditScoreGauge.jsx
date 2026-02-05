import React from 'react';
import { Award } from 'lucide-react';

const CreditScoreGauge = ({ score = 0, rating = 'N/A' }) => {
  const getScoreColor = (score) => {
    if (score >= 85) return '#10b981';
    if (score >= 70) return '#06a77d';
    if (score >= 55) return '#f59e0b';
    if (score >= 40) return '#f97316';
    return '#ef4444';
  };

  const getScoreLabel = (score) => {
    if (score >= 85) return 'Excellent';
    if (score >= 70) return 'Good';
    if (score >= 55) return 'Fair';
    if (score >= 40) return 'Weak';
    return 'Poor';
  };

  const color = getScoreColor(score);
  const label = getScoreLabel(score);
  const percentage = score;

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h3 style={styles.title}>Credit Score</h3>
        <Award size={24} style={{ color: color }} />
      </div>

      <div style={styles.gaugeContainer}>
        <svg width="200" height="120" viewBox="0 0 200 120">
          {/* Background arc */}
          <path
            d="M 20 100 A 80 80 0 0 1 180 100"
            fill="none"
            stroke="#e2e8f0"
            strokeWidth="20"
            strokeLinecap="round"
          />
          {/* Colored arc */}
          <path
            d="M 20 100 A 80 80 0 0 1 180 100"
            fill="none"
            stroke={color}
            strokeWidth="20"
            strokeLinecap="round"
            strokeDasharray={`${percentage * 2.51} 251`}
            style={{ transition: 'stroke-dasharray 1s ease-in-out' }}
          />
        </svg>
        
        <div style={styles.scoreValue}>
          <div style={{ fontSize: '2.5rem', fontWeight: '700', color: color }}>
            {Math.round(score)}
          </div>
          <div style={{ fontSize: '0.875rem', color: '#64748b' }}>
            out of 100
          </div>
        </div>
      </div>

      <div style={styles.details}>
        <div style={styles.detailRow}>
          <span style={styles.detailLabel}>Rating:</span>
          <span style={{ ...styles.detailValue, color: color, fontWeight: '600' }}>
            {rating}
          </span>
        </div>
        <div style={styles.detailRow}>
          <span style={styles.detailLabel}>Assessment:</span>
          <span style={{ ...styles.detailValue, color: color }}>
            {label}
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
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '1.5rem',
  },
  title: {
    fontSize: '1.25rem',
    fontWeight: '600',
    color: '#1e293b',
  },
  gaugeContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    position: 'relative',
  },
  scoreValue: {
    position: 'absolute',
    top: '60px',
    textAlign: 'center',
  },
  details: {
    marginTop: '2rem',
    paddingTop: '1rem',
    borderTop: '1px solid #e2e8f0',
  },
  detailRow: {
    display: 'flex',
    justifyContent: 'space-between',
    padding: '0.5rem 0',
  },
  detailLabel: {
    color: '#64748b',
    fontSize: '0.875rem',
  },
  detailValue: {
    fontSize: '0.875rem',
    fontWeight: '500',
  },
};

export default CreditScoreGauge;