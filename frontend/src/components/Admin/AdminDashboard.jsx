// src/components/Admin/AdminDashboard.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import UserManagement from './UserManagement';
import AdminStats from './AdminStats';

const AdminDashboard = () => {
  const [activeTab, setActiveTab] = useState('users');
  const [users, setUsers] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`http://localhost:5000/api/admin/users`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUsers(response.data.users);
      setLoading(false);
    } catch (error) {
      setError('Failed to fetch users');
      setLoading(false);
    }
  };

  return (
    <div className="admin-dashboard">
      <nav className="admin-nav">
        <div className="nav-logo">
          <h1>CryptoPay Admin</h1>
        </div>
        <div className="nav-links">
          <button 
            className={activeTab === 'users' ? 'active' : ''} 
            onClick={() => setActiveTab('users')}
          >
            User Management
          </button>
          <button 
            className={activeTab === 'stats' ? 'active' : ''} 
            onClick={() => setActiveTab('stats')}
          >
            System Stats
          </button>
        </div>
      </nav>

      <main className="admin-main">
        {loading ? (
          <div className="loading">Loading...</div>
        ) : error ? (
          <div className="error">{error}</div>
        ) : (
          <>
            {activeTab === 'users' && (
              <UserManagement users={users} onUserUpdate={fetchUsers} />
            )}
            {activeTab === 'stats' && (
              <AdminStats users={users} />
            )}
          </>
        )}
      </main>
    </div>
  );
};

export default AdminDashboard;