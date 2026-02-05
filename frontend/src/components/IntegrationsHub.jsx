import React, { useState } from 'react';
import { Link, CheckCircle, XCircle, Settings, RefreshCw, Shield } from 'lucide-react';
import { t } from '../translations';

const IntegrationsHub = ({ language = 'en' }) => {
  const [connections, setConnections] = useState({
    icici: false,
    razorpay: false,
  });

  const integrations = [
    {
      id: 'icici',
      name: 'ICICI Bank API',
      description: 'Real-time account balance, transaction history, and payment initiation',
      icon: '🏦',
      color: '#ff6b35',
      features: [
        'Account balance check',
        'Transaction history',
        'Payment initiation',
        'Statement download',
      ],
      status: connections.icici,
    },
    {
      id: 'razorpay',
      name: 'Razorpay Payment Gateway',
      description: 'Payment gateway integration for collections, refunds, and vendor payments',
      icon: '💳',
      color: '#3395ff',
      features: [
        'Payment collection',
        'Automated reconciliation',
        'Vendor payouts',
        'Settlement reports',
      ],
      status: connections.razorpay,
    },
  ];

  const connectedCount = Object.values(connections).filter(Boolean).length;
  const canConnect = connectedCount < 2;

  const handleToggleConnection = (id) => {
    if (connections[id]) {
      setConnections(prev => ({ ...prev, [id]: false }));
    } else if (canConnect) {
      setConnections(prev => ({ ...prev, [id]: true }));
    } else {
      alert(t('limitReached', language));
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div>
          <h2 style={styles.title}>{t('integrationsTitle', language)}</h2>
          <p style={styles.subtitle}>{t('integrationsSubtitle', language)}</p>
        </div>
        <div style={styles.statusSummary}>
          <div style={styles.statusItem}>
            <CheckCircle size={20} style={{ color: '#10b981' }} />
            <span>{connectedCount} {t('connected', language)}</span>
          </div>
          <div style={styles.statusItem}>
            <XCircle size={20} style={{ color: '#ef4444' }} />
            <span>{2 - connectedCount} {t('notConnected', language)}</span>
          </div>
          <div style={styles.limitBadge}>
            <Shield size={18} style={{ color: '#f59e0b' }} />
            <span>{connectedCount}/2 APIs</span>
          </div>
        </div>
      </div>

      <div style={styles.integrationsGrid}>
        {integrations.map((integration) => (
          <div key={integration.id} style={styles.integrationCard}>
            <div style={styles.cardHeader}>
              <div style={styles.iconWrapper}>
                <span style={styles.icon}>{integration.icon}</span>
              </div>
              <div 
                style={{
                  ...styles.statusBadge,
                  backgroundColor: integration.status ? '#dcfce7' : '#fee2e2',
                  color: integration.status ? '#10b981' : '#ef4444',
                }}
              >
                {integration.status ? (
                  <>
                    <CheckCircle size={14} />
                    {t('connected', language)}
                  </>
                ) : (
                  <>
                    <XCircle size={14} />
                    {t('notConnected', language)}
                  </>
                )}
              </div>
            </div>

            <h3 style={styles.integrationName}>{integration.name}</h3>
            <p style={styles.integrationDescription}>{integration.description}</p>

            <div style={styles.features}>
              <div style={styles.featuresTitle}>Key Features:</div>
              <ul style={styles.featuresList}>
                {integration.features.map((feature, idx) => (
                  <li key={idx} style={styles.featureItem}>
                    <span style={styles.featureBullet}>•</span>
                    {feature}
                  </li>
                ))}
              </ul>
            </div>

            <div style={styles.actions}>
              {integration.status ? (
                <>
                  <button 
                    onClick={() => handleToggleConnection(integration.id)}
                    style={styles.disconnectButton}
                  >
                    <XCircle size={16} />
                    {t('disconnect', language)}
                  </button>
                  <button style={styles.configureButton}>
                    <Settings size={16} />
                    {t('configure', language)}
                  </button>
                  <button style={styles.syncButton}>
                    <RefreshCw size={16} />
                    {t('sync', language)}
                  </button>
                </>
              ) : (
                <button 
                  onClick={() => handleToggleConnection(integration.id)}
                  style={{
                    ...styles.connectButton,
                    ...((!canConnect) && styles.connectButtonDisabled),
                  }}
                  disabled={!canConnect}
                >
                  <Link size={16} />
                  {t('connect', language)}
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const styles = {
  container: {
    padding: '2rem',
    minHeight: '100vh',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '2rem',
    flexWrap: 'wrap',
    gap: '1rem',
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
  statusSummary: {
    display: 'flex',
    gap: '1rem',
    flexWrap: 'wrap',
  },
  statusItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    padding: '0.75rem 1.25rem',
    backgroundColor: '#fff',
    borderRadius: '8px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    fontSize: '0.875rem',
    fontWeight: '600',
    color: '#1e293b',
  },
  limitBadge: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    padding: '0.75rem 1.25rem',
    backgroundColor: '#fef3c7',
    borderRadius: '8px',
    fontSize: '0.875rem',
    fontWeight: '700',
    color: '#d97706',
    border: '2px solid #fbbf24',
  },
  integrationsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
    gap: '2rem',
    marginBottom: '2rem',
  },
  integrationCard: {
    backgroundColor: '#fff',
    padding: '1.75rem',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    border: '1px solid #e2e8f0',
    transition: 'all 0.3s ease',
  },
  cardHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '1rem',
  },
  iconWrapper: {
    width: '50px',
    height: '50px',
    borderRadius: '10px',
    backgroundColor: '#f8fafc',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    border: '1px solid #e2e8f0',
  },
  icon: {
    fontSize: '2rem',
  },
  statusBadge: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    padding: '0.5rem 1rem',
    borderRadius: '6px',
    fontSize: '0.75rem',
    fontWeight: '600',
  },
  integrationName: {
    fontSize: '1.25rem',
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: '0.5rem',
  },
  integrationDescription: {
    fontSize: '0.875rem',
    color: '#64748b',
    lineHeight: '1.5',
    marginBottom: '1rem',
  },
  features: {
    marginBottom: '1.5rem',
  },
  featuresTitle: {
    fontSize: '0.8rem',
    fontWeight: '600',
    color: '#475569',
    marginBottom: '0.5rem',
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
  },
  featuresList: {
    listStyle: 'none',
    padding: 0,
    margin: 0,
  },
  featureItem: {
    display: 'flex',
    alignItems: 'flex-start',
    gap: '0.5rem',
    fontSize: '0.85rem',
    color: '#64748b',
    marginBottom: '0.4rem',
    lineHeight: '1.4',
  },
  featureBullet: {
    color: '#1e40af',
    fontWeight: '700',
  },
  actions: {
    display: 'flex',
    gap: '0.75rem',
    flexWrap: 'wrap',
  },
  connectButton: {
    flex: 1,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '0.5rem',
    padding: '0.875rem',
    backgroundColor: '#1e40af',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '0.875rem',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  connectButtonDisabled: {
    backgroundColor: '#cbd5e1',
    cursor: 'not-allowed',
  },
  disconnectButton: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '0.5rem',
    padding: '0.75rem 1rem',
    backgroundColor: '#fee2e2',
    color: '#ef4444',
    border: 'none',
    borderRadius: '8px',
    fontSize: '0.8rem',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  configureButton: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '0.5rem',
    padding: '0.75rem 1rem',
    backgroundColor: '#f1f5f9',
    color: '#475569',
    border: 'none',
    borderRadius: '8px',
    fontSize: '0.8rem',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  syncButton: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '0.5rem',
    padding: '0.75rem 1rem',
    backgroundColor: '#dbeafe',
    color: '#1e40af',
    border: 'none',
    borderRadius: '8px',
    fontSize: '0.8rem',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
};

export default IntegrationsHub;