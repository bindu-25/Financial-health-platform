import React from 'react';
import { Target, TrendingUp, Award, AlertTriangle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';

const RBIBenchmarks = ({ language = 'en' }) => {
  const translations = {
    en: {
      title: 'RBI Industry Benchmarks',
      subtitle: 'Compare your performance against RBI MSME sector benchmarks',
      yourPerformance: 'Your Performance',
      industryAvg: 'Industry Average',
      topPerformers: 'Top 25%',
      status: 'Status',
      creditGap: 'MSME Credit Gap Analysis',
    },
    hi: {
      title: 'आरबीआई उद्योग बेंचमार्क',
      subtitle: 'आरबीआई एमएसएमई क्षेत्र बेंचमार्क के विरुद्ध अपने प्रदर्शन की तुलना करें',
      yourPerformance: 'आपका प्रदर्शन',
      industryAvg: 'उद्योग औसत',
      topPerformers: 'शीर्ष 25%',
      status: 'स्थिति',
      creditGap: 'एमएसएमई क्रेडिट गैप विश्लेषण',
    },
    ta: {
      title: 'RBI தொழில்துறை தரநிலைகள்',
      subtitle: 'RBI MSME துறை தரநிலைகளுக்கு எதிராக உங்கள் செயல்திறனை ஒப்பிடுங்கள்',
      yourPerformance: 'உங்கள் செயல்திறன்',
      industryAvg: 'தொழில்துறை சராசரி',
      topPerformers: 'சிறந்த 25%',
      status: 'நிலை',
      creditGap: 'MSME கடன் இடைவெளி பகுப்பாய்வு',
    },
    te: {
      title: 'RBI పరిశ్రమ ప్రమాణాలు',
      subtitle: 'RBI MSME రంగ ప్రమాణాలకు వ్యతిరేకంగా మీ పనితీరును పోల్చండి',
      yourPerformance: 'మీ పనితీరు',
      industryAvg: 'పరిశ్రమ సగటు',
      topPerformers: 'టాప్ 25%',
      status: 'స్థితి',
      creditGap: 'MSME క్రెడిట్ గ్యాప్ విశ్లేషణ',
    },
    mr: {
      title: 'RBI उद्योग बेंचमार्क',
      subtitle: 'RBI MSME क्षेत्र बेंचमार्क विरुद्ध आपल्या कामगिरीची तुलना करा',
      yourPerformance: 'तुमची कामगिरी',
      industryAvg: 'उद्योग सरासरी',
      topPerformers: 'शीर्ष 25%',
      status: 'स्थिती',
      creditGap: 'MSME क्रेडिट गॅप विश्लेषण',
    },
  };

  const t = translations[language] || translations.en;

  // Benchmark comparison data
  const benchmarkData = [
    {
      metric: 'Gross Margin',
      yourValue: 58.6,
      industryAvg: 45.0,
      topPerformers: 55.0,
      unit: '%',
      status: 'excellent',
    },
    {
      metric: 'Net Margin',
      yourValue: 14.0,
      industryAvg: 10.0,
      topPerformers: 15.0,
      unit: '%',
      status: 'good',
    },
    {
      metric: 'Current Ratio',
      yourValue: 33.6,
      industryAvg: 1.8,
      topPerformers: 2.5,
      unit: 'x',
      status: 'excellent',
    },
    {
      metric: 'Debt-to-Equity',
      yourValue: 0.47,
      industryAvg: 1.0,
      topPerformers: 0.5,
      unit: 'x',
      status: 'excellent',
    },
    {
      metric: 'ROA',
      yourValue: 12.5,
      industryAvg: 8.0,
      topPerformers: 12.0,
      unit: '%',
      status: 'excellent',
    },
    {
      metric: 'Inventory Turnover',
      yourValue: 0.67,
      industryAvg: 6.0,
      topPerformers: 8.0,
      unit: 'x',
      status: 'weak',
    },
  ];

  // Radar chart data
  const radarData = [
    { metric: 'Profitability', your: 85, industry: 65, fullMark: 100 },
    { metric: 'Liquidity', your: 95, industry: 70, fullMark: 100 },
    { metric: 'Efficiency', your: 40, industry: 75, fullMark: 100 },
    { metric: 'Leverage', your: 90, industry: 65, fullMark: 100 },
    { metric: 'Growth', your: 75, industry: 60, fullMark: 100 },
  ];

  // RBI Credit Gap data
  const creditGapData = {
    estimatedCredit: 25.0,
    formalCredit: 7.5,
    creditGap: 17.5,
    yourPosition: 'Well-funded',
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'excellent': return '#10b981';
      case 'good': return '#3b82f6';
      case 'fair': return '#f59e0b';
      case 'weak': return '#ef4444';
      default: return '#64748b';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'excellent': return Award;
      case 'good': return TrendingUp;
      case 'fair': return Target;
      case 'weak': return AlertTriangle;
      default: return Target;
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div>
          <h2 style={styles.title}>{t.title}</h2>
          <p style={styles.subtitle}>{t.subtitle}</p>
        </div>
        <div style={styles.rbiBadge}>
          <img 
            src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Reserve_Bank_of_India_Logo.svg/120px-Reserve_Bank_of_India_Logo.svg.png" 
            alt="RBI Logo" 
            style={styles.rbiLogo}
          />
          <span style={styles.rbiBadgeText}>RBI Data 2024</span>
        </div>
      </div>

      {/* Radar Chart - Overall Comparison */}
      <div style={styles.radarSection}>
        <h3 style={styles.sectionTitle}>Performance Radar - You vs Industry</h3>
        <ResponsiveContainer width="100%" height={400}>
          <RadarChart data={radarData}>
            <PolarGrid />
            <PolarAngleAxis dataKey="metric" />
            <PolarRadiusAxis angle={90} domain={[0, 100]} />
            <Radar name={t.yourPerformance} dataKey="your" stroke="#1e40af" fill="#1e40af" fillOpacity={0.6} />
            <Radar name={t.industryAvg} dataKey="industry" stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.3} />
            <Legend />
            <Tooltip />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      {/* Detailed Benchmarks */}
      <div style={styles.benchmarksSection}>
        <h3 style={styles.sectionTitle}>Detailed Benchmark Comparison</h3>
        <div style={styles.benchmarksGrid}>
          {benchmarkData.map((item, index) => {
            const StatusIcon = getStatusIcon(item.status);
            const statusColor = getStatusColor(item.status);

            return (
              <div key={index} style={styles.benchmarkCard}>
                <div style={styles.benchmarkHeader}>
                  <span style={styles.benchmarkMetric}>{item.metric}</span>
                  <StatusIcon size={20} style={{ color: statusColor }} />
                </div>

                <div style={styles.benchmarkValues}>
                  <div style={styles.benchmarkValueRow}>
                    <span style={styles.benchmarkLabel}>Your Performance:</span>
                    <span style={styles.benchmarkValue}>
                      {item.yourValue}{item.unit}
                    </span>
                  </div>
                  <div style={styles.benchmarkValueRow}>
                    <span style={styles.benchmarkLabel}>Industry Avg:</span>
                    <span style={styles.benchmarkValueSecondary}>
                      {item.industryAvg}{item.unit}
                    </span>
                  </div>
                  <div style={styles.benchmarkValueRow}>
                    <span style={styles.benchmarkLabel}>Top 25%:</span>
                    <span style={styles.benchmarkValueSecondary}>
                      {item.topPerformers}{item.unit}
                    </span>
                  </div>
                </div>

                {/* Progress Bar */}
                <div style={styles.progressBar}>
                  <div 
                    style={{
                      ...styles.progressFill,
                      width: `${Math.min((item.yourValue / item.topPerformers) * 100, 100)}%`,
                      backgroundColor: statusColor,
                    }}
                  ></div>
                </div>

                <div style={styles.benchmarkStatus}>
                  <span style={{
                    ...styles.statusBadge,
                    backgroundColor: statusColor + '20',
                    color: statusColor,
                  }}>
                    {item.status.toUpperCase()}
                  </span>
                  <span style={styles.statusText}>
                    {item.yourValue > item.industryAvg 
                      ? `+${((item.yourValue - item.industryAvg) / item.industryAvg * 100).toFixed(1)}% above avg`
                      : `${((item.industryAvg - item.yourValue) / item.industryAvg * 100).toFixed(1)}% below avg`
                    }
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* RBI Credit Gap Analysis */}
      <div style={styles.creditGapSection}>
        <h3 style={styles.sectionTitle}>
          <AlertTriangle size={20} style={{ color: '#f59e0b' }} />
          {t.creditGap} (RBI Report 2024)
        </h3>
        
        <div style={styles.creditGapGrid}>
          <div style={styles.creditGapCard}>
            <div style={styles.creditGapLabel}>Estimated MSME Credit Demand</div>
            <div style={styles.creditGapValue}>₹{creditGapData.estimatedCredit} Lakh Crore</div>
            <div style={styles.creditGapSubtext}>Total market potential</div>
          </div>

          <div style={styles.creditGapCard}>
            <div style={styles.creditGapLabel}>Formal Credit Supply</div>
            <div style={styles.creditGapValue}>₹{creditGapData.formalCredit} Lakh Crore</div>
            <div style={styles.creditGapSubtext}>Banks + NBFCs</div>
          </div>

          <div style={{...styles.creditGapCard, border: '2px solid #ef4444'}}>
            <div style={styles.creditGapLabel}>Credit Gap</div>
            <div style={{...styles.creditGapValue, color: '#ef4444'}}>
              ₹{creditGapData.creditGap} Lakh Crore
            </div>
            <div style={styles.creditGapSubtext}>Unmet demand (70%)</div>
          </div>

          <div style={{...styles.creditGapCard, border: '2px solid #10b981'}}>
            <div style={styles.creditGapLabel}>Your Position</div>
            <div style={{...styles.creditGapValue, color: '#10b981'}}>
              {creditGapData.yourPosition}
            </div>
            <div style={styles.creditGapSubtext}>Access to formal credit</div>
          </div>
        </div>

        <div style={styles.creditGapInsight}>
          <p style={styles.insightText}>
            <strong>Key Insight:</strong> With a credit score of 74.9/100 and A rating, you are well-positioned 
            to access formal credit channels. 70% of MSMEs face credit constraints. Your strong financial 
            metrics put you in the top 30% with better access to institutional financing.
          </p>
        </div>
      </div>

      {/* Sector-wise Performance */}
      <div style={styles.sectorSection}>
        <h3 style={styles.sectionTitle}>Retail Electronics - Sector Performance</h3>
        <div style={styles.sectorStats}>
          <div style={styles.sectorStat}>
            <div style={styles.sectorStatLabel}>Sector Growth Rate</div>
            <div style={styles.sectorStatValue}>15.2%</div>
            <div style={styles.sectorStatSubtext}>FY 2023-24</div>
          </div>
          <div style={styles.sectorStat}>
            <div style={styles.sectorStatLabel}>Market Size</div>
            <div style={styles.sectorStatValue}>₹1.2T</div>
            <div style={styles.sectorStatSubtext}>India retail electronics</div>
          </div>
          <div style={styles.sectorStat}>
            <div style={styles.sectorStatLabel}>Total MSMEs</div>
            <div style={styles.sectorStatValue}>2.8L</div>
            <div style={styles.sectorStatSubtext}>In this sector</div>
          </div>
          <div style={styles.sectorStat}>
            <div style={styles.sectorStatLabel}>Avg. Credit Cycle</div>
            <div style={styles.sectorStatValue}>45 days</div>
            <div style={styles.sectorStatSubtext}>Industry standard</div>
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
  rbiBadge: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem',
    padding: '0.75rem 1.25rem',
    backgroundColor: '#fff',
    borderRadius: '8px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    border: '1px solid #e2e8f0',
  },
  rbiLogo: {
    height: '30px',
  },
  rbiBadgeText: {
    fontSize: '0.875rem',
    fontWeight: '600',
    color: '#1e40af',
  },
  radarSection: {
    backgroundColor: '#fff',
    padding: '2rem',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    marginBottom: '2rem',
  },
  sectionTitle: {
    fontSize: '1.25rem',
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: '1.5rem',
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
  },
  benchmarksSection: {
    marginBottom: '2rem',
  },
  benchmarksGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
    gap: '1.5rem',
  },
  benchmarkCard: {
    backgroundColor: '#fff',
    padding: '1.5rem',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    border: '1px solid #e2e8f0',
  },
  benchmarkHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '1rem',
  },
  benchmarkMetric: {
    fontSize: '1rem',
    fontWeight: '600',
    color: '#1e293b',
  },
  benchmarkValues: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
    marginBottom: '1rem',
  },
  benchmarkValueRow: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  benchmarkLabel: {
    fontSize: '0.875rem',
    color: '#64748b',
  },
  benchmarkValue: {
    fontSize: '1.25rem',
    fontWeight: '700',
    color: '#1e40af',
  },
  benchmarkValueSecondary: {
    fontSize: '0.95rem',
    fontWeight: '600',
    color: '#64748b',
  },
  progressBar: {
    height: '8px',
    backgroundColor: '#e2e8f0',
    borderRadius: '4px',
    overflow: 'hidden',
    marginBottom: '1rem',
  },
  progressFill: {
    height: '100%',
    transition: 'width 0.5s ease',
  },
  benchmarkStatus: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  statusBadge: {
    padding: '0.25rem 0.75rem',
    borderRadius: '12px',
    fontSize: '0.75rem',
    fontWeight: '600',
  },
  statusText: {
    fontSize: '0.75rem',
    color: '#64748b',
  },
  creditGapSection: {
    backgroundColor: '#fff',
    padding: '2rem',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    marginBottom: '2rem',
  },
  creditGapGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
    gap: '1.5rem',
    marginBottom: '1.5rem',
  },
  creditGapCard: {
    padding: '1.5rem',
    backgroundColor: '#f8fafc',
    borderRadius: '8px',
    border: '1px solid #e2e8f0',
    textAlign: 'center',
  },
  creditGapLabel: {
    fontSize: '0.875rem',
    color: '#64748b',
    marginBottom: '0.75rem',
  },
  creditGapValue: {
    fontSize: '1.75rem',
    fontWeight: '700',
    color: '#1e293b',
    marginBottom: '0.5rem',
  },
  creditGapSubtext: {
    fontSize: '0.75rem',
    color: '#94a3b8',
  },
  creditGapInsight: {
    padding: '1.5rem',
    backgroundColor: '#dbeafe',
    borderRadius: '8px',
    borderLeft: '4px solid #1e40af',
  },
  insightText: {
    fontSize: '0.95rem',
    lineHeight: '1.6',
    color: '#1e293b',
    margin: 0,
  },
  sectorSection: {
    backgroundColor: '#fff',
    padding: '2rem',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
  },
  sectorStats: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '1.5rem',
  },
  sectorStat: {
    padding: '1.5rem',
    backgroundColor: '#f8fafc',
    borderRadius: '8px',
    textAlign: 'center',
  },
  sectorStatLabel: {
    fontSize: '0.875rem',
    color: '#64748b',
    marginBottom: '0.75rem',
  },
  sectorStatValue: {
    fontSize: '2rem',
    fontWeight: '700',
    color: '#1e40af',
    marginBottom: '0.5rem',
  },
  sectorStatSubtext: {
    fontSize: '0.75rem',
    color: '#94a3b8',
  },
};

export default RBIBenchmarks;