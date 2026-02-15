import React, { useState, useEffect } from 'react';
import './App.css';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import AnalysisSection from './components/AnalysisSection';
import GSTDashboard from './components/GSTDashboard';
import ReportsSection from './components/ReportsSection';
import IntegrationsHub from './components/IntegrationsHub';
import FileUpload from './components/FileUpload';
import BankProducts from './components/BankProducts';
import RBIBenchmarks from './components/RBIBenchmarks';
import RoleBasedView from './components/RoleBasedView';

const API_URL = '';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [language, setLanguage] = useState('en');
  const [smeId] = useState(1);
  const [dashboardData, setDashboardData] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0); // Force component refresh

  useEffect(() => {
    loadDashboardData();
  }, [refreshKey]); // Reload when refreshKey changes

  const loadDashboardData = async () => {
    try {
      const res = await fetch(`${API_URL}/api/smes/${smeId}/dashboard`);
      const data = await res.json();
      console.log('App loaded dashboard data:', data);
      setDashboardData(data);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    }
  };

  const handleFileUploadSuccess = (result) => {
    console.log('File uploaded successfully:', result);
    // Increment refresh key to force reload
    setRefreshKey(prev => prev + 1);
    // Navigate to dashboard
    setCurrentView('dashboard');
  };

  const renderContent = () => {
    switch (currentView) {
      case 'dashboard':
        return <Dashboard key={refreshKey} smeId={smeId} language={language} />;
      
      case 'analysis':
        return (
          <RoleBasedView requiredRole="manager">
            <AnalysisSection language={language} />
          </RoleBasedView>
        );
      
      case 'gst':
        return <GSTDashboard language={language} />;
      
      case 'benchmarks':
        return <RBIBenchmarks language={language} />;
      
      case 'reports':
        return (
          <RoleBasedView requiredRole="manager">
            <ReportsSection language={language} />
          </RoleBasedView>
        );
      
      case 'integrations':
        return (
          <RoleBasedView requiredRole="admin">
            <IntegrationsHub language={language} />
          </RoleBasedView>
        );
      
      case 'upload':
        return (
          <RoleBasedView requiredRole="manager">
            <FileUpload onUploadSuccess={handleFileUploadSuccess} />
          </RoleBasedView>
        );
      
      case 'products':
        return (
          <BankProducts 
            creditScore={dashboardData?.credit_score?.score || 75} 
            language={language} 
          />
        );
      
      default:
        return <Dashboard key={refreshKey} smeId={smeId} language={language} />;
    }
  };

  return (
    <div className="App">
      <Navbar
        onNavigate={setCurrentView}
        currentView={currentView}
        onLanguageChange={setLanguage}
        currentLanguage={language}
      />
      {renderContent()}
    </div>
  );
}

export default App;