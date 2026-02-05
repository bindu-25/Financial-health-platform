import React, { useState } from 'react';
import { Lightbulb, TrendingUp, DollarSign, AlertCircle, ChevronDown, ChevronUp } from 'lucide-react';

const RecommendationsList = ({ recommendations, language = 'en' }) => {
  const [expandedIndex, setExpandedIndex] = useState(null);

  const translations = {
    en: {
      title: 'AI-Powered Recommendations',
      subtitle: 'Actionable insights to improve your financial health',
      timeline: 'Timeline',
      impact: 'Expected Impact',
      steps: 'Action Steps',
      resources: 'Resources Needed',
    },
    hi: {
      title: 'AI-संचालित सिफारिशें',
      subtitle: 'आपके वित्तीय स्वास्थ्य में सुधार के लिए कार्रवाई योग्य अंतर्दृष्टि',
      timeline: 'समयरेखा',
      impact: 'अपेक्षित प्रभाव',
      steps: 'कार्य चरण',
      resources: 'आवश्यक संसाधन',
    },
  };

  const t = translations[language] || translations.en;

  const items = [
    {
      category: 'Revenue Growth',
      title: 'Expand Product Lines',
      description: 'Introduce complementary products to increase average transaction value and customer lifetime value.',
      priority: 'high',
      icon: TrendingUp,
      timeline: '3-6 months',
      impact: '+15-20% revenue increase',
      steps: [
        'Conduct market research on complementary products',
        'Identify top 3 high-margin product categories',
        'Negotiate supplier agreements',
        'Launch pilot program with 5 products',
        'Analyze sales data and scale successful items',
      ],
      resources: [
        'Budget: ₹5-10 lakhs for initial inventory',
        'Team: 1 product manager, 1 analyst',
        'Time: 20 hours/week for 3 months',
        'Tools: Inventory management software',
      ],
    },
    {
      category: 'Cost Optimization',
      title: 'Negotiate with Suppliers',
      description: 'Leverage your purchasing volume to negotiate better rates. Consider bulk purchasing for frequently used items.',
      priority: 'high',
      icon: DollarSign,
      timeline: '1-2 months',
      impact: '5-8% cost reduction',
      steps: [
        'Analyze top 10 suppliers by spend',
        'Calculate annual purchase volumes',
        'Prepare negotiation strategy with competitive quotes',
        'Schedule meetings with key suppliers',
        'Implement new pricing agreements',
      ],
      resources: [
        'Team: Procurement manager',
        'Time: 10 hours/week for 2 months',
        'Tools: Spend analysis software',
        'Support: Legal review for contracts',
      ],
    },
    {
      category: 'Cash Flow',
      title: 'Optimize Working Capital',
      description: 'Review inventory turnover rates and reduce excess stock. Implement just-in-time inventory practices.',
      priority: 'medium',
      icon: AlertCircle,
      timeline: '2-4 months',
      impact: '₹20-30 lakhs cash release',
      steps: [
        'Audit current inventory levels',
        'Identify slow-moving items (>90 days)',
        'Implement discount strategy for excess stock',
        'Set up automated reorder points',
        'Negotiate payment terms with suppliers',
      ],
      resources: [
        'Budget: ₹2 lakhs for software',
        'Team: Operations manager',
        'Time: 15 hours/week for 3 months',
        'Tools: ERP system integration',
      ],
    },
    {
      category: 'Profitability',
      title: 'Improve Profit Margins',
      description: 'Focus on high-margin products and services. Analyze your product mix and consider discontinuing low-margin items.',
      priority: 'medium',
      icon: Lightbulb,
      timeline: '1-3 months',
      impact: '+2-3% margin improvement',
      steps: [
        'Calculate profit margin for each product',
        'Identify bottom 20% low-margin products',
        'Develop exit strategy for unprofitable items',
        'Increase marketing for high-margin products',
        'Adjust pricing strategy quarterly',
      ],
      resources: [
        'Team: Financial analyst, Marketing',
        'Time: 8 hours/week for 2 months',
        'Tools: Product profitability dashboard',
        'Budget: ₹3 lakhs for marketing push',
      ],
    },
  ];

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return '#ef4444';
      case 'medium': return '#f59e0b';
      case 'low': return '#10b981';
      default: return '#64748b';
    }
  };

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>{t.title}</h3>
      <p style={styles.subtitle}>{t.subtitle}</p>

      <div style={styles.list}>
        {items.map((item, index) => {
          const IconComponent = item.icon;
          const isExpanded = expandedIndex === index;

          return (
            <div 
              key={index} 
              style={{
                ...styles.card,
                ...(isExpanded && styles.cardExpanded),
              }}
              onMouseEnter={() => setExpandedIndex(index)}
              onMouseLeave={() => setExpandedIndex(null)}
            >
              <div style={styles.cardHeader}>
                <div style={styles.iconWrapper}>
                  <IconComponent size={20} style={{ color: '#1e40af' }} />
                </div>
                <span style={{
                  ...styles.priority,
                  backgroundColor: getPriorityColor(item.priority) + '20',
                  color: getPriorityColor(item.priority),
                }}>
                  {item.priority.toUpperCase()}
                </span>
              </div>
              
              <div style={styles.category}>{item.category}</div>
              <h4 style={styles.cardTitle}>{item.title}</h4>
              <p style={styles.description}>{item.description}</p>

              {/* Expanded Content */}
              {isExpanded && (
                <div style={styles.expandedContent}>
                  <div style={styles.expandedDivider}></div>
                  
                  <div style={styles.expandedGrid}>
                    <div style={styles.expandedItem}>
                      <div style={styles.expandedLabel}>{t.timeline}:</div>
                      <div style={styles.expandedValue}>{item.timeline}</div>
                    </div>
                    <div style={styles.expandedItem}>
                      <div style={styles.expandedLabel}>{t.impact}:</div>
                      <div style={styles.expandedValue}>{item.impact}</div>
                    </div>
                  </div>

                  <div style={styles.expandedSection}>
                    <div style={styles.expandedSectionTitle}>{t.steps}:</div>
                    <ol style={styles.stepsList}>
                      {item.steps.map((step, idx) => (
                        <li key={idx} style={styles.stepItem}>{step}</li>
                      ))}
                    </ol>
                  </div>

                  <div style={styles.expandedSection}>
                    <div style={styles.expandedSectionTitle}>{t.resources}:</div>
                    <ul style={styles.resourcesList}>
                      {item.resources.map((resource, idx) => (
                        <li key={idx} style={styles.resourceItem}>{resource}</li>
                      ))}
                    </ul>
                  </div>

                  <div style={styles.expandIndicator}>
                    <ChevronUp size={20} style={{ color: '#64748b' }} />
                  </div>
                </div>
              )}

              {!isExpanded && (
                <div style={styles.hoverHint}>
                  <ChevronDown size={16} style={{ color: '#94a3b8' }} />
                  <span style={styles.hoverHintText}>Hover for details</span>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

const styles = {
  container: {
    padding: '2rem',
  },
  title: {
    fontSize: '1.5rem',
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: '0.25rem',
  },
  subtitle: {
    fontSize: '0.875rem',
    color: '#64748b',
    marginBottom: '1.5rem',
  },
  list: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
    gap: '1.5rem',
  },
  card: {
    backgroundColor: '#fff',
    padding: '1.5rem',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    border: '1px solid #e2e8f0',
    transition: 'all 0.3s ease',
    cursor: 'pointer',
    position: 'relative',
  },
  cardExpanded: {
    boxShadow: '0 8px 16px rgba(0,0,0,0.15)',
    transform: 'translateY(-4px)',
  },
  cardHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '1rem',
  },
  iconWrapper: {
    width: '40px',
    height: '40px',
    borderRadius: '8px',
    backgroundColor: '#dbeafe',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  priority: {
    padding: '0.25rem 0.75rem',
    borderRadius: '12px',
    fontSize: '0.75rem',
    fontWeight: '600',
  },
  category: {
    fontSize: '0.75rem',
    color: '#64748b',
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
    marginBottom: '0.5rem',
  },
  cardTitle: {
    fontSize: '1.125rem',
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: '0.5rem',
  },
  description: {
    fontSize: '0.875rem',
    color: '#64748b',
    lineHeight: '1.5',
    marginBottom: '1rem',
  },
  hoverHint: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '0.5rem',
    paddingTop: '0.75rem',
    borderTop: '1px solid #e2e8f0',
  },
  hoverHintText: {
    fontSize: '0.75rem',
    color: '#94a3b8',
  },
  expandedContent: {
    marginTop: '1rem',
    animation: 'fadeIn 0.3s ease',
  },
  expandedDivider: {
    height: '1px',
    backgroundColor: '#e2e8f0',
    marginBottom: '1rem',
  },
  expandedGrid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '1rem',
    marginBottom: '1rem',
  },
  expandedItem: {
    backgroundColor: '#f8fafc',
    padding: '0.75rem',
    borderRadius: '6px',
  },
  expandedLabel: {
    fontSize: '0.75rem',
    color: '#64748b',
    marginBottom: '0.25rem',
  },
  expandedValue: {
    fontSize: '0.875rem',
    fontWeight: '600',
    color: '#1e293b',
  },
  expandedSection: {
    marginBottom: '1rem',
  },
  expandedSectionTitle: {
    fontSize: '0.875rem',
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: '0.5rem',
  },
  stepsList: {
    paddingLeft: '1.25rem',
    margin: 0,
  },
  stepItem: {
    fontSize: '0.8rem',
    color: '#64748b',
    marginBottom: '0.5rem',
    lineHeight: '1.4',
  },
  resourcesList: {
    paddingLeft: '1.25rem',
    margin: 0,
  },
  resourceItem: {
    fontSize: '0.8rem',
    color: '#64748b',
    marginBottom: '0.5rem',
  },
  expandIndicator: {
    display: 'flex',
    justifyContent: 'center',
    paddingTop: '0.5rem',
  },
};

export default RecommendationsList;