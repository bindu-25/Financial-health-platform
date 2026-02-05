import React from 'react';
import { Building2, CreditCard, TrendingUp, CheckCircle } from 'lucide-react';
import { t } from '../translations';

const BankProducts = ({ creditScore = 74.9, language = 'en' }) => {
  const products = [
    {
      id: 1,
      bank: 'ICICI Bank',
      product: 'Business Term Loan',
      icon: Building2,
      color: '#ff6b35',
      minScore: 70,
      loanAmount: '₹10L - ₹50L',
      interestRate: '9.5% - 11.5%',
      tenure: '12-60 months',
      features: [
        'Quick approval in 48 hours',
        'Minimal documentation',
        'Flexible repayment options',
        'No collateral up to ₹25L',
      ],
      eligibility: creditScore >= 70,
    },
    {
      id: 2,
      bank: 'HDFC Bank',
      product: 'Working Capital Loan',
      icon: TrendingUp,
      color: '#0066cc',
      minScore: 65,
      loanAmount: '₹5L - ₹30L',
      interestRate: '10% - 12%',
      tenure: '6-36 months',
      features: [
        'Overdraft facility available',
        'Interest only on utilized amount',
        'Digital application process',
        'Same-day disbursement',
      ],
      eligibility: creditScore >= 65,
    },
    {
      id: 3,
      bank: 'State Bank of India',
      product: 'MSME Loan',
      icon: Building2,
      color: '#1e3a8a',
      minScore: 60,
      loanAmount: '₹25L - ₹100L',
      interestRate: '8.5% - 10.5%',
      tenure: '24-84 months',
      features: [
        'Government-backed scheme',
        'Lower interest rates',
        'Extended repayment tenure',
        'Credit guarantee coverage',
      ],
      eligibility: creditScore >= 60,
    },
    {
      id: 4,
      bank: 'Razorpay Capital',
      product: 'Invoice Financing',
      icon: CreditCard,
      color: '#3395ff',
      minScore: 55,
      loanAmount: '₹1L - ₹20L',
      interestRate: '12% - 15%',
      tenure: '1-12 months',
      features: [
        '100% digital process',
        'Get 80% of invoice value instantly',
        'No hidden charges',
        'Automated collections',
      ],
      eligibility: creditScore >= 55,
    },
  ];

  const eligibleProducts = products.filter(p => p.eligibility);
  const ineligibleProducts = products.filter(p => !p.eligibility);

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div>
          <h2 style={styles.title}>Recommended Financial Products</h2>
          <p style={styles.subtitle}>
            Based on your credit score of <strong>{creditScore}/100</strong>, you qualify for these products
          </p>
        </div>
        <div style={styles.scoreBadge}>
          <span style={styles.scoreLabel}>Your Credit Score</span>
          <span style={styles.scoreValue}>{creditScore}</span>
        </div>
      </div>

      {/* Eligible Products */}
      {eligibleProducts.length > 0 && (
        <div style={styles.section}>
          <h3 style={styles.sectionTitle}>
            <CheckCircle size={20} style={{ color: '#10b981' }} />
            You're Eligible ({eligibleProducts.length} products)
          </h3>
          <div style={styles.productsGrid}>
            {eligibleProducts.map(product => (
              <ProductCard key={product.id} product={product} eligible={true} />
            ))}
          </div>
        </div>
      )}

      {/* Ineligible Products */}
      {ineligibleProducts.length > 0 && (
        <div style={styles.section}>
          <h3 style={styles.sectionTitle}>
            Build Your Score to Unlock ({ineligibleProducts.length} products)
          </h3>
          <div style={styles.productsGrid}>
            {ineligibleProducts.map(product => (
              <ProductCard key={product.id} product={product} eligible={false} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

const ProductCard = ({ product, eligible }) => {
  const Icon = product.icon;

  return (
    <div style={{
      ...styles.productCard,
      opacity: eligible ? 1 : 0.6,
      border: eligible ? `2px solid ${product.color}` : '1px solid #e2e8f0',
    }}>
      {!eligible && (
        <div style={styles.lockedBadge}>
          🔒 Min Score: {product.minScore}
        </div>
      )}

      <div style={styles.cardHeader}>
        <div style={{
          ...styles.iconWrapper,
          backgroundColor: product.color + '20',
        }}>
          <Icon size={24} style={{ color: product.color }} />
        </div>
        {eligible && (
          <span style={styles.eligibleBadge}>✓ Eligible</span>
        )}
      </div>

      <div style={styles.bankName}>{product.bank}</div>
      <h4 style={styles.productName}>{product.product}</h4>

      <div style={styles.productDetails}>
        <div style={styles.detailRow}>
          <span style={styles.detailLabel}>Loan Amount</span>
          <span style={styles.detailValue}>{product.loanAmount}</span>
        </div>
        <div style={styles.detailRow}>
          <span style={styles.detailLabel}>Interest Rate</span>
          <span style={styles.detailValue}>{product.interestRate}</span>
        </div>
        <div style={styles.detailRow}>
          <span style={styles.detailLabel}>Tenure</span>
          <span style={styles.detailValue}>{product.tenure}</span>
        </div>
      </div>

      <div style={styles.features}>
        <div style={styles.featuresTitle}>Key Benefits:</div>
        <ul style={styles.featuresList}>
          {product.features.map((feature, idx) => (
            <li key={idx} style={styles.featureItem}>
              <span style={styles.featureBullet}>•</span>
              {feature}
            </li>
          ))}
        </ul>
      </div>

      <button
        style={{
          ...styles.applyButton,
          backgroundColor: eligible ? product.color : '#cbd5e1',
          cursor: eligible ? 'pointer' : 'not-allowed',
        }}
        disabled={!eligible}
      >
        {eligible ? 'Apply Now' : `Improve Score by ${product.minScore - Math.floor(product.minScore)}`}
      </button>
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
  scoreBadge: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '1rem 1.5rem',
    backgroundColor: '#dbeafe',
    borderRadius: '12px',
    border: '2px solid #1e40af',
  },
  scoreLabel: {
    fontSize: '0.75rem',
    color: '#64748b',
    marginBottom: '0.25rem',
  },
  scoreValue: {
    fontSize: '2rem',
    fontWeight: '700',
    color: '#1e40af',
  },
  section: {
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
  productsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
    gap: '1.5rem',
  },
  productCard: {
    position: 'relative',
    backgroundColor: '#fff',
    padding: '1.75rem',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    transition: 'all 0.3s ease',
  },
  lockedBadge: {
    position: 'absolute',
    top: '1rem',
    right: '1rem',
    padding: '0.5rem 1rem',
    backgroundColor: '#fee2e2',
    color: '#ef4444',
    borderRadius: '6px',
    fontSize: '0.75rem',
    fontWeight: '600',
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
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  eligibleBadge: {
    padding: '0.5rem 1rem',
    backgroundColor: '#dcfce7',
    color: '#10b981',
    borderRadius: '6px',
    fontSize: '0.75rem',
    fontWeight: '600',
  },
  bankName: {
    fontSize: '0.875rem',
    color: '#64748b',
    marginBottom: '0.25rem',
  },
  productName: {
    fontSize: '1.25rem',
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: '1rem',
  },
  productDetails: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.75rem',
    marginBottom: '1rem',
    padding: '1rem',
    backgroundColor: '#f8fafc',
    borderRadius: '8px',
  },
  detailRow: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  detailLabel: {
    fontSize: '0.875rem',
    color: '#64748b',
  },
  detailValue: {
    fontSize: '0.875rem',
    fontWeight: '600',
    color: '#1e293b',
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
  applyButton: {
    width: '100%',
    padding: '0.875rem',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '0.95rem',
    fontWeight: '600',
    transition: 'all 0.2s',
  },
};

export default BankProducts;