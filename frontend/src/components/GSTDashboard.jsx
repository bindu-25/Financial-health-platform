import React from 'react';
import { Receipt, TrendingUp, AlertCircle, CheckCircle } from 'lucide-react';

const GSTDashboard = ({ language = 'en' }) => {
  const translations = {
    en: {
      title: 'GST Management',
      subtitle: 'Track GST collections, payments, and compliance',
      collected: 'GST Collected',
      paid: 'GST Paid',
      netPayable: 'Net GST Payable',
      compliance: 'Compliance Status',
      filingDue: 'Next Filing Due',
      itc: 'Input Tax Credit',
    },
    hi: {
      title: 'जीएसटी प्रबंधन',
      subtitle: 'जीएसटी संग्रह, भुगतान और अनुपालन ट्रैक करें',
      collected: 'जीएसटी एकत्र',
      paid: 'जीएसटी भुगतान',
      netPayable: 'शुद्ध जीएसटी देय',
      compliance: 'अनुपालन स्थिति',
      filingDue: 'अगली फाइलिंग नियत',
      itc: 'इनपुट टैक्स क्रेडिट',
    },
  };

  const t = translations[language] || translations.en;

  const gstData = {
    collected: 10036086.13,
    paid: 4156702.42,
    netPayable: 5879383.71,
    itcAvailable: 856234.50,
    complianceRate: 100,
    nextDue: '2024-02-20',
  };

  const monthlyGST = [
    { month: 'Aug', collected: 1520000, paid: 640000, net: 880000 },
    { month: 'Sep', collected: 1580000, paid: 660000, net: 920000 },
    { month: 'Oct', collected: 1640000, paid: 680000, net: 960000 },
    { month: 'Nov', collected: 1700000, paid: 710000, net: 990000 },
    { month: 'Dec', collected: 1760000, paid: 730000, net: 1030000 },
    { month: 'Jan', collected: 1836086, paid: 736702, net: 1099384 },
  ];

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div>
          <h2 style={styles.title}>{t.title}</h2>
          <p style={styles.subtitle}>{t.subtitle}</p>
        </div>
        <div style={styles.complianceBadge}>
          <CheckCircle size={20} style={{ color: '#10b981' }} />
          <span style={styles.complianceText}>100% Compliant</span>
        </div>
      </div>

      {/* Summary Cards */}
      <div style={styles.summaryGrid}>
        <div style={styles.summaryCard}>
          <div style={styles.summaryIcon} style={{ backgroundColor: '#dbeafe' }}>
            <Receipt size={24} style={{ color: '#1e40af' }} />
          </div>
          <div style={styles.summaryContent}>
            <div style={styles.summaryLabel}>{t.collected}</div>
            <div style={styles.summaryValue}>₹{(gstData.collected / 100000).toFixed(2)}L</div>
            <div style={styles.summaryChange}>
              <TrendingUp size={14} style={{ color: '#10b981' }} />
              <span style={{ color: '#10b981' }}>+6.2%</span>
            </div>
          </div>
        </div>

        <div style={styles.summaryCard}>
          <div style={styles.summaryIcon} style={{ backgroundColor: '#fef3c7' }}>
            <Receipt size={24} style={{ color: '#f59e0b' }} />
          </div>
          <div style={styles.summaryContent}>
            <div style={styles.summaryLabel}>{t.paid}</div>
            <div style={styles.summaryValue}>₹{(gstData.paid / 100000).toFixed(2)}L</div>
            <div style={styles.summaryChange}>
              <TrendingUp size={14} style={{ color: '#10b981' }} />
              <span style={{ color: '#10b981' }}>+5.8%</span>
            </div>
          </div>
        </div>

        <div style={styles.summaryCard}>
          <div style={styles.summaryIcon} style={{ backgroundColor: '#dcfce7' }}>
            <CheckCircle size={24} style={{ color: '#10b981' }} />
          </div>
          <div style={styles.summaryContent}>
            <div style={styles.summaryLabel}>{t.netPayable}</div>
            <div style={styles.summaryValue}>₹{(gstData.netPayable / 100000).toFixed(2)}L</div>
            <div style={styles.summarySubtext}>Due: {gstData.nextDue}</div>
          </div>
        </div>

        <div style={styles.summaryCard}>
          <div style={styles.summaryIcon} style={{ backgroundColor: '#e0e7ff' }}>
            <TrendingUp size={24} style={{ color: '#6366f1' }} />
          </div>
          <div style={styles.summaryContent}>
            <div style={styles.summaryLabel}>{t.itc}</div>
            <div style={styles.summaryValue}>₹{(gstData.itcAvailable / 100000).toFixed(2)}L</div>
            <div style={styles.summarySubtext}>Available to claim</div>
          </div>
        </div>
      </div>

      {/* Monthly Trend */}
      <div style={styles.trendCard}>
        <h3 style={styles.trendTitle}>Monthly GST Trend (Last 6 Months)</h3>
        <div style={styles.chartContainer}>
          {monthlyGST.map((item, index) => (
            <div key={index} style={styles.barGroup}>
              <div style={styles.barsContainer}>
                <div 
                  style={{
                    ...styles.bar,
                    height: `${(item.collected / 2000000) * 100}%`,
                    backgroundColor: '#1e40af',
                  }}
                  title={`Collected: ₹${item.collected.toLocaleString()}`}
                ></div>
                <div 
                  style={{
                    ...styles.bar,
                    height: `${(item.paid / 2000000) * 100}%`,
                    backgroundColor: '#f59e0b',
                  }}
                  title={`Paid: ₹${item.paid.toLocaleString()}`}
                ></div>
                <div 
                  style={{
                    ...styles.bar,
                    height: `${(item.net / 2000000) * 100}%`,
                    backgroundColor: '#10b981',
                  }}
                  title={`Net: ₹${item.net.toLocaleString()}`}
                ></div>
              </div>
              <div style={styles.barLabel}>{item.month}</div>
            </div>
          ))}
        </div>
        <div style={styles.legend}>
          <div style={styles.legendItem}>
            <div style={{ ...styles.legendDot, backgroundColor: '#1e40af' }}></div>
            <span>Collected</span>
          </div>
          <div style={styles.legendItem}>
            <div style={{ ...styles.legendDot, backgroundColor: '#f59e0b' }}></div>
            <span>Paid</span>
          </div>
          <div style={styles.legendItem}>
            <div style={{ ...styles.legendDot, backgroundColor: '#10b981' }}></div>
            <span>Net Payable</span>
          </div>
        </div>
      </div>

      {/* Filing Reminders */}
      <div style={styles.remindersCard}>
        <h3 style={styles.remindersTitle}>
          <AlertCircle size={20} style={{ color: '#f59e0b' }} />
          Upcoming Filings & Reminders
        </h3>
        <div style={styles.remindersList}>
          <div style={styles.reminderItem}>
            <div style={styles.reminderDate}>Feb 20, 2024</div>
            <div style={styles.reminderText}>GSTR-3B Filing Due</div>
            <div style={styles.reminderBadge}>7 days</div>
          </div>
          <div style={styles.reminderItem}>
            <div style={styles.reminderDate}>Feb 25, 2024</div>
            <div style={styles.reminderText}>GST Payment Due</div>
            <div style={styles.reminderBadge}>12 days</div>
          </div>
          <div style={styles.reminderItem}>
            <div style={styles.reminderDate}>Mar 11, 2024</div>
            <div style={styles.reminderText}>GSTR-1 Filing Due</div>
            <div style={styles.reminderBadge}>27 days</div>
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
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
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
  complianceBadge: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    padding: '0.75rem 1.25rem',
    backgroundColor: '#dcfce7',
    borderRadius: '8px',
  },
  complianceText: {
    fontSize: '0.95rem',
    fontWeight: '600',
    color: '#10b981',
  },
  summaryGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
    gap: '1.5rem',
    marginBottom: '2rem',
  },
  summaryCard: {
    display: 'flex',
    gap: '1rem',
    backgroundColor: '#fff',
    padding: '1.5rem',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    border: '1px solid #e2e8f0',
  },
  summaryIcon: {
    width: '50px',
    height: '50px',
    borderRadius: '10px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    flexShrink: 0,
  },
  summaryContent: {
    flex: 1,
  },
  summaryLabel: {
    fontSize: '0.8rem',
    color: '#64748b',
    marginBottom: '0.25rem',
    fontWeight: '500',
  },
  summaryValue: {
    fontSize: '1.75rem',
    fontWeight: '700',
    color: '#1e293b',
    marginBottom: '0.25rem',
  },
  summaryChange: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.25rem',
    fontSize: '0.8rem',
    fontWeight: '600',
  },
  summarySubtext: {
    fontSize: '0.75rem',
    color: '#94a3b8',
  },
  trendCard: {
    backgroundColor: '#fff',
    padding: '1.75rem',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    marginBottom: '2rem',
  },
  trendTitle: {
    fontSize: '1.125rem',
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: '1.5rem',
  },
  chartContainer: {
    display: 'flex',
    justifyContent: 'space-around',
    alignItems: 'flex-end',
    height: '200px',
    marginBottom: '1rem',
    padding: '1rem 0',
    borderBottom: '2px solid #e2e8f0',
  },
  barGroup: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '0.5rem',
  },
  barsContainer: {
    display: 'flex',
    gap: '4px',
    alignItems: 'flex-end',
    height: '180px',
  },
  bar: {
    width: '20px',
    borderRadius: '4px 4px 0 0',
    transition: 'height 0.3s ease',
  },
  barLabel: {
    fontSize: '0.75rem',
    color: '#64748b',
    fontWeight: '500',
  },
  legend: {
    display: 'flex',
    justifyContent: 'center',
    gap: '2rem',
    marginTop: '1rem',
  },
  legendItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    fontSize: '0.875rem',
    color: '#64748b',
  },
  legendDot: {
    width: '12px',
    height: '12px',
    borderRadius: '50%',
  },
  remindersCard: {
    backgroundColor: '#fff',
    padding: '1.75rem',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
  },
  remindersTitle: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    fontSize: '1.125rem',
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: '1rem',
  },
  remindersList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
  },
  reminderItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '1rem',
    padding: '1rem',
    backgroundColor: '#f8fafc',
    borderRadius: '8px',
    border: '1px solid #e2e8f0',
  },
  reminderDate: {
    fontSize: '0.875rem',
    fontWeight: '600',
    color: '#1e40af',
    minWidth: '100px',
  },
  reminderText: {
    flex: 1,
    fontSize: '0.95rem',
    color: '#1e293b',
  },
  reminderBadge: {
    padding: '0.25rem 0.75rem',
    backgroundColor: '#fef3c7',
    color: '#d97706',
    fontSize: '0.75rem',
    fontWeight: '600',
    borderRadius: '12px',
  },
};

export default GSTDashboard;