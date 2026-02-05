import React, { useState } from 'react';
import './App.css';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import FileUpload from './components/FileUpload';
import AnalysisSection from './components/AnalysisSection';
import ReportsSection from './components/ReportsSection';
import GSTDashboard from './components/GSTDashboard';
import RBIBenchmarks from './components/RBIBenchmarks';
import IntegrationsHub from './components/IntegrationsHub';
import RoleBasedView from './components/RoleBasedView';
import { t } from './translations';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [currentLanguage, setCurrentLanguage] = useState('en');
  const [uploadData, setUploadData] = useState(null);

  const handleUploadSuccess = (data) => {
    console.log('File uploaded successfully:', data);
    setUploadData(data);
    setCurrentView('dashboard');
  };

  const handleNavigate = (view) => {
    setCurrentView(view);
  };

  const handleLanguageChange = (lang) => {
    setCurrentLanguage(lang);
  };

  const renderContent = () => {
    switch (currentView) {
      case 'dashboard':
        return <Dashboard smeId={1} language={currentLanguage} />;
      
      case 'analysis':
        return (
          <RoleBasedView requiredRole="manager">
            <AnalysisSection language={currentLanguage} />
          </RoleBasedView>
        );
      
      case 'reports':
        return (
          <RoleBasedView requiredRole="manager">
            <ReportsSection language={currentLanguage} />
          </RoleBasedView>
        );
      
      case 'upload':
        return (
          <RoleBasedView requiredRole="manager">
            <FileUpload onUploadSuccess={handleUploadSuccess} language={currentLanguage} />
          </RoleBasedView>
        );
      
      case 'gst':
        return <GSTDashboard language={currentLanguage} />;
      
      case 'benchmarks':
        return <RBIBenchmarks language={currentLanguage} />;
      
      case 'integrations':
        return (
          <RoleBasedView requiredRole="admin">
            <IntegrationsHub language={currentLanguage} />
          </RoleBasedView>
        );
      
      default:
        return <Dashboard smeId={1} language={currentLanguage} />;
    }
  };

  return (
    <div className="App">
      <Navbar 
        onNavigate={handleNavigate}
        currentView={currentView}
        onLanguageChange={handleLanguageChange}
        currentLanguage={currentLanguage}
      />
      
      <div className="main-content">
        <div className="secondary-nav">
          <button 
            className={currentView === 'dashboard' ? 'nav-tab active' : 'nav-tab'}
            onClick={() => handleNavigate('dashboard')}
          >
            📊 {t('overview', currentLanguage)}
          </button>
          <button 
            className={currentView === 'analysis' ? 'nav-tab active' : 'nav-tab'}
            onClick={() => handleNavigate('analysis')}
          >
            📈 {t('analysis', currentLanguage)}
          </button>
          <button 
            className={currentView === 'gst' ? 'nav-tab active' : 'nav-tab'}
            onClick={() => handleNavigate('gst')}
          >
            🧾 {t('gst', currentLanguage)}
          </button>
          <button 
            className={currentView === 'benchmarks' ? 'nav-tab active' : 'nav-tab'}
            onClick={() => handleNavigate('benchmarks')}
          >
            🎯 {t('benchmarks', currentLanguage)}
          </button>
          <button 
            className={currentView === 'reports' ? 'nav-tab active' : 'nav-tab'}
            onClick={() => handleNavigate('reports')}
          >
            📄 {t('reports', currentLanguage)}
          </button>
          <button 
            className={currentView === 'integrations' ? 'nav-tab active' : 'nav-tab'}
            onClick={() => handleNavigate('integrations')}
          >
            🔗 {t('integrations', currentLanguage)}
          </button>
          <button 
            className={currentView === 'upload' ? 'nav-tab active' : 'nav-tab'}
            onClick={() => handleNavigate('upload')}
          >
            ⬆️ {t('upload', currentLanguage)}
          </button>
        </div>

        <div className="content-area">
          {renderContent()}
        </div>
      </div>
    </div>
  );
}

export default App;