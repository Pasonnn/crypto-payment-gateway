import React, { useState } from 'react';
import axios from 'axios';
import PaymentModal from '../Common/PaymentModal';
import CryptoPayButton from '../Common/CryptoPayButton';

const UserProfile = ({ userProfile, fetchUserProfile }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    username: userProfile?.user?.username || '',
    email: userProfile?.user?.email || '',
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [donationAmount, setDonationAmount] = useState('');
  const [finalAmount, setFinalAmount] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (formData.newPassword !== formData.confirmPassword) {
      setError('New passwords do not match');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      await axios.put('http://localhost:5000/api/users/edit', 
        {
          username: formData.username,
          current_password: formData.currentPassword,
          new_password: formData.newPassword || undefined // Only send if there's a new password
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      setSuccess('Profile updated successfully');
      setIsEditing(false);
      fetchUserProfile();
    } catch (error) {
      setError(error.response?.data?.message || 'Error updating profile');
    }
  };

  const handleOpenPaymentModal = () => {
    setFinalAmount(donationAmount); // Lock the current donation amount
    setShowPaymentModal(true);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="profile-section">
      <h2>User Profile</h2>
      {!isEditing ? (
        <div className="profile-info">
          <div className="info-group">
            <label>Username</label>
            <p>{userProfile?.user?.username}</p>
          </div>
          <div className="info-group">
            <label>Email</label>
            <p>{userProfile?.user?.email}</p>
          </div>
          <div className="info-group">
            <label>Role</label>
            <p>{userProfile?.user?.role}</p>
          </div>
          <div className="info-group">
            <label>Wallet Address</label>
            <p>{userProfile?.user?.wallet_address || 'No wallet bound'}</p>
          </div>
          <div className="info-group">
            <label>Account Created</label>
            <p>{formatDate(userProfile?.user?.created_at)}</p>
          </div>
          <div className="info-group">
            <label>Last Updated</label>
            <p>{formatDate(userProfile?.user?.updated_at)}</p>
          </div>
          <button 
            className="btn-edit-profile"
            onClick={() => setIsEditing(true)}
          >
            Edit Profile
          </button>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="profile-form">
          {error && <p className="error-message">{error}</p>}
          {success && <p className="success-message">{success}</p>}
          
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={formData.email}
              disabled
            />
          </div>
          
          <div className="form-group">
            <label>Current Password</label>
            <input
              type="password"
              name="currentPassword"
              value={formData.currentPassword}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label>New Password (optional)</label>
            <input
              type="password"
              name="newPassword"
              value={formData.newPassword}
              onChange={handleChange}
            />
          </div>
          
          <div className="form-group">
            <label>Confirm New Password</label>
            <input
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
            />
          </div>
          
          <div className="profile-actions">
            <button type="submit" className="btn-save">
              Save Changes
            </button>
            <button 
              type="button" 
              className="btn-cancel"
              onClick={() => setIsEditing(false)}
            >
              Cancel
            </button>
          </div>
        </form>
      )}
      <div className="donation-section">
        <h2>Donate ETH</h2>
        <div className="donation-form">
          <div className="form-group">
            <label>Amount (USD)</label>
            <input
              type="number"
              step="0.01"
              min="0"
              value={donationAmount}
              onChange={(e) => setDonationAmount(e.target.value)}
              placeholder="Enter USD amount"
            />
          </div>
          <CryptoPayButton
            amount={donationAmount}
            buttonText="Pay with CryptoPay"
            onClick={handleOpenPaymentModal}
            onSuccess={() => {
              setSuccess('Thank you for your donation!');
              setDonationAmount('');
            }}
            onError={(error) => {
              setError(error.message || 'Payment failed');
            }}
            config={{
              currency: 'USD',
              callbackUrl: `${window.location.origin}/payment/callback`
            }}
          />
        </div>
        {error && <p className="error-message">{error}</p>}
        {success && <p className="success-message">{success}</p>}
      </div>
      {showPaymentModal && (
        <PaymentModal
          amount={finalAmount}
          apiKey={userProfile?.user?.api_key}
          onClose={() => {
            setShowPaymentModal(false);
            setError('');
          }}
          onSuccess={() => {
            setShowPaymentModal(false);
            setSuccess('Thank you for your donation!');
            setDonationAmount('');
          }}
        />
      )}
    </div>
  );
};

export default UserProfile;
