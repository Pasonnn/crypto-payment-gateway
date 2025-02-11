import React, { useState } from 'react';
import axios from 'axios';

const UserManagement = ({ users, onUserUpdate }) => {
  const [selectedUserId, setSelectedUserId] = useState(null);
  const [selectedUser, setSelectedUser] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleDeleteUser = async (userId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`http://localhost:5000/api/admin/users/${userId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSuccess('User deleted successfully');
      onUserUpdate();
    } catch (error) {
      setError('Failed to delete user');
    }
  };

  const viewUserDetails = async (userId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`http://localhost:5000/api/admin/users/${userId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSelectedUser(response.data.user);
      setSelectedUserId(userId);
    } catch (error) {
      setError('Failed to fetch user details');
    }
  };

  return (
    <div className="user-management">
      <h2>User Management</h2>
      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}
      
      <div className="users-table">
        <table>
          <thead>
            <tr>
              <th>Username</th>
              <th>Email</th>
              <th>Role</th>
              <th>Wallet Address</th>
              <th>Created At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(users).map(([userId, user]) => (
              <tr key={userId}>
                <td>{user.username || 'N/A'}</td>
                <td>{user.email || 'N/A'}</td>
                <td>{user.role}</td>
                <td>
                  {user.wallet_address ? 
                    `${user.wallet_address.slice(0, 6)}...${user.wallet_address.slice(-4)}` : 
                    'Not set'
                  }
                </td>
                <td>{new Date(user.created_at).toLocaleDateString()}</td>
                <td>
                  <button 
                    className="btn-view"
                    onClick={() => viewUserDetails(userId)}
                  >
                    View
                  </button>
                  <button 
                    className="btn-delete"
                    onClick={() => handleDeleteUser(userId)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedUser && (
        <div className="user-details-modal">
          <div className="modal-content">
            <h3>User Details</h3>
            <div className="user-info">
              <p><strong>ID:</strong> {selectedUserId}</p>
              <p><strong>Username:</strong> {selectedUser.username || 'N/A'}</p>
              <p><strong>Email:</strong> {selectedUser.email || 'N/A'}</p>
              <p><strong>Role:</strong> {selectedUser.role}</p>
              <p><strong>Wallet:</strong> {selectedUser.wallet_address || 'Not set'}</p>
              <p><strong>Created:</strong> {new Date(selectedUser.created_at).toLocaleString()}</p>
              <p><strong>Updated:</strong> {new Date(selectedUser.updated_at).toLocaleString()}</p>
            </div>
            <button onClick={() => setSelectedUser(null)}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserManagement;
