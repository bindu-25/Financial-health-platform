import React, { useState } from 'react';
import { Upload, FileSpreadsheet, AlertCircle, CheckCircle } from 'lucide-react';

const FileUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      const validTypes = ['.csv', '.xlsx', '.xls'];
      const fileExtension = selectedFile.name.substring(selectedFile.name.lastIndexOf('.')).toLowerCase();
      
      if (validTypes.includes(fileExtension)) {
        setFile(selectedFile);
        setError(null);
        setSuccess(false);
      } else {
        setError('Please upload a CSV or Excel file');
        setFile(null);
      }
    }
  };

  const handleUpload = async () => {
    // FIXED: Proper if block syntax
    if (!file) {
      alert('Please select a file');
      return;
    }

    setUploading(true);
    setError(null);
    setSuccess(false);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('sme_id', '1');

      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Upload failed');
      }

      const result = await response.json();
      
      setSuccess(true);
      setFile(null);
      
      // Clear file input
      document.getElementById('file-upload').value = '';
      
      // Notify parent component to refresh dashboard
      if (onUploadSuccess) {
        onUploadSuccess(result);
      }
      
      // Show success message for 3 seconds then redirect to dashboard
      setTimeout(() => {
        window.location.hash = '#dashboard';
        window.location.reload();
      }, 2000);

    } catch (err) {
      setError(err.message || 'Upload failed');
      console.error('Upload error:', err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.uploadBox}>
        <FileSpreadsheet size={48} style={styles.icon} />
        <h3 style={styles.title}>Upload Financial Data</h3>
        <p style={styles.description}>
          Upload your CSV or Excel file containing financial data (date, revenue, expenses)
        </p>

        <input
          type="file"
          accept=".csv,.xlsx,.xls"
          onChange={handleFileChange}
          style={styles.fileInput}
          id="file-upload"
        />
        
        <label htmlFor="file-upload" style={styles.fileLabel}>
          <Upload size={20} />
          Choose File
        </label>

        {file && (
          <div style={styles.fileInfo}>
            <p style={styles.fileName}>{file.name}</p>
            <p style={styles.fileSize}>
              {(file.size / 1024).toFixed(2)} KB
            </p>
          </div>
        )}

        {error && (
          <div style={styles.error}>
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        {success && (
          <div style={styles.success}>
            <CheckCircle size={16} />
            <span>File uploaded successfully! Redirecting to dashboard...</span>
          </div>
        )}

        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          style={{
            ...styles.uploadButton,
            ...((!file || uploading) && styles.uploadButtonDisabled),
          }}
        >
          {uploading ? 'Analyzing...' : 'Upload & Analyze'}
        </button>

        {uploading && (
          <div style={styles.loadingBar}>
            <div style={styles.loadingBarFill}></div>
          </div>
        )}
      </div>
    </div>
  );
};

const styles = {
  container: {
    padding: '2rem',
    maxWidth: '600px',
    margin: '0 auto',
  },
  uploadBox: {
    border: '2px dashed #cbd5e1',
    borderRadius: '12px',
    padding: '3rem 2rem',
    textAlign: 'center',
    backgroundColor: '#f8fafc',
  },
  icon: {
    color: '#64748b',
    margin: '0 auto 1rem',
  },
  title: {
    fontSize: '1.5rem',
    fontWeight: '600',
    marginBottom: '0.5rem',
    color: '#1e293b',
  },
  description: {
    color: '#64748b',
    marginBottom: '2rem',
    fontSize: '0.95rem',
  },
  fileInput: {
    display: 'none',
  },
  fileLabel: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '0.5rem',
    padding: '0.75rem 1.5rem',
    backgroundColor: '#fff',
    border: '1px solid #cbd5e1',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '1rem',
    fontWeight: '500',
    transition: 'all 0.2s',
  },
  fileInfo: {
    marginTop: '1rem',
    padding: '1rem',
    backgroundColor: '#fff',
    borderRadius: '8px',
    border: '1px solid #e2e8f0',
  },
  fileName: {
    fontWeight: '500',
    color: '#1e293b',
    marginBottom: '0.25rem',
  },
  fileSize: {
    fontSize: '0.875rem',
    color: '#64748b',
  },
  error: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '0.5rem',
    marginTop: '1rem',
    padding: '0.75rem',
    backgroundColor: '#fef2f2',
    color: '#dc2626',
    borderRadius: '8px',
    fontSize: '0.875rem',
  },
  success: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '0.5rem',
    marginTop: '1rem',
    padding: '0.75rem',
    backgroundColor: '#dcfce7',
    color: '#16a34a',
    borderRadius: '8px',
    fontSize: '0.875rem',
  },
  uploadButton: {
    marginTop: '1.5rem',
    padding: '0.875rem 2rem',
    backgroundColor: '#1e40af',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '1rem',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  },
  uploadButtonDisabled: {
    backgroundColor: '#cbd5e1',
    cursor: 'not-allowed',
  },
  loadingBar: {
    marginTop: '1rem',
    height: '4px',
    backgroundColor: '#e2e8f0',
    borderRadius: '2px',
    overflow: 'hidden',
  },
  loadingBarFill: {
    height: '100%',
    width: '100%',
    backgroundColor: '#1e40af',
    animation: 'loading 1.5s ease-in-out infinite',
  },
};

export default FileUpload;