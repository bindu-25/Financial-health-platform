import React, { useState } from 'react';
import { BarChart3, Globe, Shield } from 'lucide-react';
import { t } from '../translations';
import { RoleBadge, EncryptionIndicator } from './RoleBasedView';

const Navbar = ({ onNavigate, currentView, onLanguageChange, currentLanguage }) => {
  const [showLanguages, setShowLanguages] = useState(false);

  const languages = [
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'hi', name: 'हिंदी', flag: '🇮🇳' },
    { code: 'ta', name: 'தமிழ்', flag: '🇮🇳' },
    { code: 'te', name: 'తెలుగు', flag: '🇮🇳' },
    { code: 'mr', name: 'मराठी', flag: '🇮🇳' },
  ];

  return (
    <nav style={styles.navbar}>
      <div style={styles.container}>
        <div style={styles.brand}>
          <BarChart3 size={32} style={styles.icon} />
          <div style={styles.brandText}>
            <span style={styles.brandTitle}>{t('brand', currentLanguage)}</span>
            <span style={styles.brandSubtitle}>{t('brandSubtitle', currentLanguage)}</span>
          </div>
        </div>
        
        <div style={styles.navLinks}>
          <button
            onClick={() => onNavigate('dashboard')}
            style={{
              ...styles.navButton,
              ...(currentView === 'dashboard' && styles.navButtonActive),
            }}
          >
            {t('dashboard', currentLanguage)}
          </button>
          <button
            onClick={() => onNavigate('analysis')}
            style={{
              ...styles.navButton,
              ...(currentView === 'analysis' && styles.navButtonActive),
            }}
          >
            {t('analysis', currentLanguage)}
          </button>
          <button
            onClick={() => onNavigate('reports')}
            style={{
              ...styles.navButton,
              ...(currentView === 'reports' && styles.navButtonActive),
            }}
          >
            {t('reports', currentLanguage)}
          </button>
        </div>

        <div style={styles.rightSection}>
          {/* Role Badge */}
          <RoleBadge />

          {/* Language Selector */}
          <div style={styles.languageSelector}>
            <button
              onClick={() => setShowLanguages(!showLanguages)}
              style={styles.languageButton}
            >
              <Globe size={18} />
              <span>{languages.find(l => l.code === currentLanguage)?.flag || '🇬🇧'}</span>
            </button>
            
            {showLanguages && (
              <div style={styles.languageDropdown}>
                {languages.map(lang => (
                  <button
                    key={lang.code}
                    onClick={() => {
                      onLanguageChange(lang.code);
                      setShowLanguages(false);
                    }}
                    style={{
                      ...styles.languageOption,
                      ...(currentLanguage === lang.code && styles.languageOptionActive),
                    }}
                  >
                    <span>{lang.flag}</span>
                    <span>{lang.name}</span>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Encryption Indicator */}
          <EncryptionIndicator />
        </div>
      </div>
    </nav>
  );
};

const styles = {
  navbar: {
    backgroundColor: '#1e40af',
    padding: '1rem 0',
    boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
    position: 'sticky',
    top: 0,
    zIndex: 1000,
  },
  container: {
    maxWidth: '1400px',
    margin: '0 auto',
    padding: '0 2rem',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: '1rem',
  },
  brand: {
    display: 'flex',
    alignItems: 'center',
    gap: '1rem',
  },
  icon: {
    color: '#fff',
  },
  brandText: {
    display: 'flex',
    flexDirection: 'column',
  },
  brandTitle: {
    color: '#fff',
    fontSize: '1.5rem',
    fontWeight: '700',
    letterSpacing: '-0.02em',
  },
  brandSubtitle: {
    color: '#93c5fd',
    fontSize: '0.7rem',
    fontWeight: '400',
    marginTop: '-0.2rem',
  },
  navLinks: {
    display: 'flex',
    gap: '0.5rem',
  },
  navButton: {
    padding: '0.625rem 1.25rem',
    backgroundColor: 'transparent',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '0.95rem',
    fontWeight: '500',
    cursor: 'pointer',
    transition: 'all 0.2s',
    whiteSpace: 'nowrap',
  },
  navButtonActive: {
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
  },
  rightSection: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem',
  },
  languageSelector: {
    position: 'relative',
  },
  languageButton: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    padding: '0.5rem 1rem',
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '1rem',
  },
  languageDropdown: {
    position: 'absolute',
    top: '110%',
    right: 0,
    backgroundColor: '#fff',
    borderRadius: '8px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
    minWidth: '150px',
    overflow: 'hidden',
    zIndex: 100,
  },
  languageOption: {
    width: '100%',
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem',
    padding: '0.75rem 1rem',
    backgroundColor: '#fff',
    border: 'none',
    cursor: 'pointer',
    fontSize: '0.9rem',
    transition: 'background-color 0.2s',
    textAlign: 'left',
  },
  languageOptionActive: {
    backgroundColor: '#dbeafe',
  },
};

export default Navbar;