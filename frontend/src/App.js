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

export default App;