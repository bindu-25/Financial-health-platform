import React, { useState } from 'react';
import { FileText, Download, Calendar, Filter, TrendingUp, DollarSign, PieChart } from 'lucide-react';

const ReportsSection = ({ language = 'en' }) => {
  const [dateRange, setDateRange] = useState('last-6-months');
  const [reportType, setReportType] = useState('all');

  const translations = {
    en: {
      title: 'Reports & Export',
      subtitle: 'Generate and download comprehensive financial reports',
      generate: 'Generate Report',
      download: 'Download',
      dateRange: 'Date Range',
      reportType: 'Report Type',
    },
    hi: {
      title: 'रिपोर्ट और निर्यात',
      subtitle: 'व्यापक वित्तीय रिपोर्ट तैयार और डाउनलोड करें',
      generate: 'रिपोर्ट बनाएं',
      download: 'डाउनलोड',
      dateRange: 'तिथि सीमा',
      reportType: 'रिपोर्ट प्रकार',
    },
  };

  const t = translations[language] || translations.en;

  const reportTemplates = [
    {
      id: 1,
      name: 'Executive Summary',
      description: 'High-level overview of financial performance for stakeholders',
      icon: TrendingUp,
      color: '#1e40af',
      pages: 5,
      lastGenerated: '2024-02-01',
    },
    {
      id: 2,
      name: 'Detailed P&L Statement',
      description: 'Complete profit and loss statement with variance analysis',
      icon: DollarSign,
      color: '#10b981',
      pages: 12,
      lastGenerated: '2024-02-01',
    },
    {
      id: 3,
      name: 'Cash Flow Analysis',
      description: 'Cash flow trends, working capital analysis, and projections',
      icon: FileText,
      color: '#f59e0b',
      pages: 8,
      lastGenerated: '2024-02-01',
    },
    {
      id: 4,
      name: 'Tax & Compliance Report',
      description: 'GST calculations, TDS summary, and regulatory compliance status',
      icon: PieChart,
      color: '#8b5cf6',
      pages: 6,
      lastGenerated: '2024-02-01',
    },
  ];

  const handleGenerateReport = (reportId) => {
    console.log(`Generating report ${reportId}`);
    alert(`Generating report... This would trigger backend PDF generation.`);
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div>
          <h2 style={styles.title}>{t.title}</h2>
          <p style={styles.subtitle}>{t.subtitle}</p>
        </div>
      </div>

      {/* Filters */}
      <div style={styles.filters}>
        <div style={styles.filterGroup}>
          <label style={styles.filterLabel}>
            <Calendar size={16} />
            {t.dateRange}
          </label>
          <select 
            value={dateRange} 
            onChange={(e) => setDateRange(e.target.value)}
            style={styles.select}
          >
            <option value="last-month">Last Month</option>
            <option value="last-3-months">Last 3 Months</option>
            <option value="last-6-months">Last 6 Months</option>
            <option value="last-year">Last Year</option>
            <option value="custom">Custom Range</option>
          </select>
        </div>

        <div style={styles.filterGroup}>
          <label style={styles.filterLabel}>
            <Filter size={16} />
            {t.reportType}
          </label>
          <select 
            value={reportType} 
            onChange={(e) => setReportType(e.target.value)}
            style={styles.select}
          >
            <option value="all">All Reports</option>
            <option value="financial">Financial Only</option>
            <option value="tax">Tax & Compliance</option>
            <option value="operational">Operational</option>
          </select>
        </div>
      </div>

      {/* Report Templates */}
      <div style={styles.reportGrid}>
        {reportTemplates.map((report) => {
          const IconComponent = report.icon;
          return (
            <div key={report.id} style={styles.reportCard}>
              <div style={styles.reportHeader}>
                <div 
                  style={{
                    ...styles.reportIcon,
                    backgroundColor: report.color + '20',
                  }}
                >
                  <IconComponent size={24} style={{ color: report.color }} />
                </div>
                <div style={styles.reportMeta}>
                  <span style={styles.reportPages}>{report.pages} pages</span>
                  <span style={styles.reportDate}>
                    Last: {new Date(report.lastGenerated).toLocaleDateString()}
                  </span>
                </div>
              </div>

              <h3 style={styles.reportName}>{report.name}</h3>
              <p style={styles.reportDescription}>{report.description}</p>

              <div style={styles.reportActions}>
                <button 
                  onClick={() => handleGenerateReport(report.id)}
                  style={styles.generateButton}
                >
                  <FileText size={16} />
                  {t.generate}
                </button>
                <button style={styles.downloadButton}>
                  <Download size={16} />
                  {t.download}
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Quick Export */}
      <div style={styles.quickExport}>
        <h3 style={styles.quickExportTitle}>Quick Export</h3>
        <div style={styles.quickExportButtons}>
          <button style={styles.exportButton}>
            <Download size={16} />
            Export to Excel
          </button>
          <button style={styles.exportButton}>
            <Download size={16} />
            Export to PDF
          </button>
          <button style={styles.exportButton}>
            <Download size={16} />
            Export to CSV
          </button>
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
  filters: {
    display: 'flex',
    gap: '1.5rem',
    marginBottom: '2rem',
    padding: '1.5rem',
    backgroundColor: '#fff',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
  },
  filterGroup: {
    flex: 1,
  },
  filterLabel: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    fontSize: '0.875rem',
    fontWeight: '600',
    color: '#475569',
    marginBottom: '0.5rem',
  },
  select: {
    width: '100%',
    padding: '0.75rem',
    fontSize: '0.95rem',
    border: '1px solid #e2e8f0',
    borderRadius: '8px',
    backgroundColor: '#fff',
    color: '#1e293b',
    cursor: 'pointer',
  },
  reportGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
    gap: '1.5rem',
    marginBottom: '2rem',
  },
  reportCard: {
    backgroundColor: '#fff',
    padding: '1.75rem',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    border: '1px solid #e2e8f0',
    transition: 'all 0.3s ease',
    cursor: 'pointer',
  },
  reportHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '1rem',
  },
  reportIcon: {
    width: '50px',
    height: '50px',
    borderRadius: '10px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  reportMeta: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-end',
    gap: '0.25rem',
  },
  reportPages: {
    fontSize: '0.75rem',
    color: '#64748b',
    fontWeight: '500',
  },
  reportDate: {
    fontSize: '0.7rem',
    color: '#94a3b8',
  },
  reportName: {
    fontSize: '1.125rem',
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: '0.5rem',
  },
  reportDescription: {
    fontSize: '0.875rem',
    color: '#64748b',
    lineHeight: '1.5',
    marginBottom: '1.5rem',
    minHeight: '3rem',
  },
  reportActions: {
    display: 'flex',
    gap: '0.75rem',
  },
  generateButton: {
    flex: 1,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '0.5rem',
    padding: '0.75rem',
    backgroundColor: '#1e40af',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '0.875rem',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  downloadButton: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '0.5rem',
    padding: '0.75rem',
    backgroundColor: '#f1f5f9',
    color: '#475569',
    border: 'none',
    borderRadius: '8px',
    fontSize: '0.875rem',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  quickExport: {
    backgroundColor: '#fff',
    padding: '1.75rem',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
  },
  quickExportTitle: {
    fontSize: '1.125rem',
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: '1rem',
  },
  quickExportButtons: {
    display: 'flex',
    gap: '1rem',
    flexWrap: 'wrap',
  },
  exportButton: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    padding: '0.75rem 1.5rem',
    backgroundColor: '#f8fafc',
    color: '#475569',
    border: '1px solid #e2e8f0',
    borderRadius: '8px',
    fontSize: '0.875rem',
    fontWeight: '500',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
};

export default ReportsSection;