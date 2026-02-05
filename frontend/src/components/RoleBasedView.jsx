import React, { useState } from 'react';
import { Shield, User, Users, Lock, Settings } from 'lucide-react';

const RoleBasedView = ({ children, requiredRole = 'viewer' }) => {
  // Get role from localStorage or default to 'viewer'
  const [userRole, setUserRole] = useState(localStorage.getItem('userRole') || 'viewer');

  const roles = {
    viewer: {
      level: 1,
      permissions: ['view_dashboard', 'view_gst', 'view_benchmarks'],
      label: 'Viewer',
      icon: User,
      color: '#64748b',
      description: 'View-only access to dashboard, GST, and benchmarks',
    },
    manager: {
      level: 2,
      permissions: ['view_dashboard', 'view_reports', 'generate_reports', 'upload_data', 'view_analysis', 'view_gst', 'view_benchmarks'],
      label: 'Manager',
      icon: Users,
      color: '#3b82f6',
      description: 'Full analysis access + report generation',
    },
    admin: {
      level: 3,
      permissions: ['view_dashboard', 'view_reports', 'generate_reports', 'upload_data', 'manage_integrations', 'view_sensitive_data', 'view_analysis', 'view_gst', 'view_benchmarks'],
      label: 'Admin',
      icon: Shield,
      color: '#10b981',
      description: 'Full system access including integrations',
    },
  };

  const currentRole = roles[userRole];
  const requiredRoleData = roles[requiredRole];

  const hasAccess = currentRole.level >= requiredRoleData.level;

  if (!hasAccess) {
    return (
      <div style={styles.accessDenied}>
        <Lock size={48} style={{ color: '#ef4444' }} />
        <h3 style={styles.deniedTitle}>Access Restricted</h3>
        <p style={styles.deniedText}>
          This feature requires <strong>{requiredRoleData.label}</strong> access or higher.
        </p>
        <p style={styles.deniedSubtext}>
          Your current role: <strong>{currentRole.label}</strong>
        </p>
        <p style={styles.deniedSubtext}>
          {currentRole.description}
        </p>
        <p style={styles.deniedContact}>
          Contact your administrator to request access.
        </p>
      </div>
    );
  }

  return <>{children}</>;
};

// Role Badge Component with Selector
export const RoleBadge = () => {
  const [userRole, setUserRole] = useState(localStorage.getItem('userRole') || 'viewer');
  const [showSelector, setShowSelector] = useState(false);

  const roles = {
    viewer: { label: 'Viewer', icon: User, color: '#64748b' },
    manager: { label: 'Manager', icon: Users, color: '#3b82f6' },
    admin: { label: 'Admin', icon: Shield, color: '#10b981' },
  };

  const currentRole = roles[userRole];
  const RoleIcon = currentRole.icon;

  const changeRole = (newRole) => {
    setUserRole(newRole);
    localStorage.setItem('userRole', newRole);
    setShowSelector(false);
    window.location.reload(); // Reload to apply role changes
  };

  return (
    <div style={styles.roleBadgeContainer}>
      <button
        onClick={() => setShowSelector(!showSelector)}
        style={{
          ...styles.roleBadge,
          backgroundColor: currentRole.color + '20',
          border: `1px solid ${currentRole.color}`,
        }}
      >
        <RoleIcon size={16} style={{ color: currentRole.color }} />
        <span style={{ color: currentRole.color, fontWeight: '600' }}>
          {currentRole.label}
        </span>
        <Settings size={14} style={{ color: currentRole.color }} />
      </button>

      {showSelector && (
        <div style={styles.roleDropdown}>
          {Object.entries(roles).map(([key, role]) => {
            const Icon = role.icon;
            return (
              <button
                key={key}
                onClick={() => changeRole(key)}
                style={{
                  ...styles.roleOption,
                  ...(userRole === key && styles.roleOptionActive),
                }}
              >
                <Icon size={16} style={{ color: role.color }} />
                <span>{role.label}</span>
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
};

// Encryption Indicator Component
export const EncryptionIndicator = () => {
  return (
    <div style={styles.encryptionBadge}>
      <Shield size={16} style={{ color: '#10b981' }} />
      <span style={styles.encryptionText}>AES-256</span>
    </div>
  );
};

const styles = {
  accessDenied: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '400px',
    padding: '2rem',
    backgroundColor: '#fff',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    margin: '2rem',
  },
  deniedTitle: {
    fontSize: '1.5rem',
    fontWeight: '700',
    color: '#1e293b',
    marginTop: '1rem',
    marginBottom: '0.5rem',
  },
  deniedText: {
    fontSize: '1rem',
    color: '#64748b',
    textAlign: 'center',
    marginBottom: '0.5rem',
  },
  deniedSubtext: {
    fontSize: '0.875rem',
    color: '#94a3b8',
    textAlign: 'center',
    marginBottom: '0.25rem',
  },
  deniedContact: {
    fontSize: '0.875rem',
    color: '#64748b',
    textAlign: 'center',
    marginTop: '1rem',
    fontWeight: '600',
  },
  roleBadgeContainer: {
    position: 'relative',
  },
  roleBadge: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    padding: '0.5rem 1rem',
    borderRadius: '8px',
    fontSize: '0.875rem',
    cursor: 'pointer',
    border: 'none',
    backgroundColor: 'transparent',
  },
  roleDropdown: {
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
  roleOption: {
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
  roleOptionActive: {
    backgroundColor: '#dbeafe',
  },
  encryptionBadge: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    padding: '0.5rem 1rem',
    backgroundColor: '#dcfce7',
    borderRadius: '8px',
    border: '1px solid #10b981',
  },
  encryptionText: {
    fontSize: '0.75rem',
    fontWeight: '600',
    color: '#10b981',
  },
};

export default RoleBasedView;