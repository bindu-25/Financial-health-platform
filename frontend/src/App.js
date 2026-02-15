import React, { useState, useEffect } from 'react';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [smeId, setSmeId] = useState(1);
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Load dashboard data
  const loadData = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/smes/${smeId}/dashboard`);
      const data = await res.json();
      setDashboardData(data);
    } catch (error) {
      setMessage('Error loading data: ' + error.message);
    }
    setLoading(false);
  };

  // Handle file upload
  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('sme_id', smeId);

    setLoading(true);
    setMessage('Uploading...');

    try {
      const res = await fetch(`${API_URL}/api/analyze`, {
        method: 'POST',
        body: formData,
      });
      
      if (!res.ok) throw new Error('Upload failed');
      
      setMessage('Upload successful! Refreshing dashboard...');
      await loadData(); // Auto-refresh after upload
      setMessage('Dashboard updated!');
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage('Upload error: ' + error.message);
    }
    setLoading(false);
  };

  // Load on mount
  useEffect(() => {
    loadData();
  }, [smeId]);

  return (
    <div className="App">
      <header>
        <h1>Financial Dashboard</h1>
        <div className="controls">
          <input
            type="file"
            accept=".xlsx,.xls,.csv"
            onChange={handleUpload}
            disabled={loading}
            id="fileInput"
            style={{display: 'none'}}
          />
          <label htmlFor="fileInput" className="btn">
            📤 Upload Excel
          </label>
          <button onClick={loadData} disabled={loading} className="btn">
            🔄 Refresh
          </button>
        </div>
      </header>

      {message && <div className="message">{message}</div>}
      
      {loading && <div className="loading">Loading...</div>}
      
      {dashboardData && !loading && (
        <div className="dashboard">
          <div className="metrics">
            <div className="card">
              <h3>Credit Score</h3>
              <div className="value">{dashboardData.credit_score?.score || 'N/A'}</div>
            </div>
            <div className="card">
              <h3>Revenue</h3>
              <div className="value">₹{(dashboardData.profit_loss?.revenue || 0).toLocaleString()}</div>
            </div>
            <div className="card">
              <h3>Net Profit</h3>
              <div className="value">₹{(dashboardData.profit_loss?.net_profit || 0).toLocaleString()}</div>
            </div>
          </div>
          <div className="timestamp">Last updated: {new Date().toLocaleString()}</div>
        </div>
      )}
    </div>
  );
}

export default App;import React, { useState, useEffect } from 'react';
import './App.css';

// Use empty string for Railway deployment (relative URLs on same domain)
const API_URL = '';

function App() {
  const [smeId, setSmeId] = useState(1);
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Load dashboard data
  const loadData = async () => {
    setLoading(true);
    setMessage('');
    try {
      const res = await fetch(`${API_URL}/api/smes/${smeId}/dashboard`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setDashboardData(data);
    } catch (error) {
      setMessage('Error loading data: ' + error.message);
      console.error('Load error:', error);
    }
    setLoading(false);
  };

  // Handle file upload
  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('sme_id', smeId);

    setLoading(true);
    setMessage('Uploading...');

    try {
      const res = await fetch(`${API_URL}/api/analyze`, {
        method: 'POST',
        body: formData,
      });
      
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Upload failed');
      }
      
      setMessage('Upload successful! Refreshing dashboard...');
      await loadData(); // Auto-refresh after upload
      setMessage('Dashboard updated!');
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage('Upload error: ' + error.message);
      console.error('Upload error:', error);
    }
    setLoading(false);
    
    // Reset file input
    e.target.value = '';
  };

  // Load on mount
  useEffect(() => {
    loadData();
  }, [smeId]);

  return (
    <div className="App">
      <header>
        <h1>💰 Financial Dashboard</h1>
        <div className="controls">
          <input
            type="file"
            accept=".xlsx,.xls,.csv"
            onChange={handleUpload}
            disabled={loading}
            id="fileInput"
            style={{display: 'none'}}
          />
          <label htmlFor="fileInput" className={`btn ${loading ? 'disabled' : ''}`}>
            📤 Upload Excel
          </label>
          <button onClick={loadData} disabled={loading} className="btn">
            🔄 {loading ? 'Loading...' : 'Refresh'}
          </button>
        </div>
      </header>

      {message && (
        <div className={`message ${message.includes('error') || message.includes('Error') ? 'error' : 'success'}`}>
          {message}
        </div>
      )}
      
      {loading && <div className="loading">Loading...</div>}
      
      {dashboardData && !loading && (
        <div className="dashboard">
          <div className="metrics">
            <div className="card">
              <h3>Credit Score</h3>
              <div className="value">{dashboardData.credit_score?.score || 'N/A'}</div>
              <div className="label">Rating: {dashboardData.credit_score?.rating || 'N/A'}</div>
            </div>
            <div className="card">
              <h3>Revenue</h3>
              <div className="value">₹{(dashboardData.profit_loss?.revenue || 0).toLocaleString()}</div>
              <div className="label">Total Revenue</div>
            </div>
            <div className="card">
              <h3>Net Profit</h3>
              <div className="value">₹{(dashboardData.profit_loss?.net_profit || 0).toLocaleString()}</div>
              <div className="label">Margin: {dashboardData.profit_loss?.margin || 0}%</div>
            </div>
            <div className="card">
              <h3>GST Balance</h3>
              <div className="value">₹{(dashboardData.gst?.net || 0).toLocaleString()}</div>
              <div className="label">Compliance: {dashboardData.gst?.compliance_score || 0}%</div>
            </div>
          </div>
          <div className="timestamp">Last updated: {new Date(dashboardData.last_updated).toLocaleString()}</div>
        </div>
      )}
    </div>
  );
}

export default App;