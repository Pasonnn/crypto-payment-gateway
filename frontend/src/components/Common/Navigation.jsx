import React from 'react';
import { useNavigate } from 'react-router-dom';
import CryptoPayIcon from '../../assets/CryptoPayIcon.png';

const Navigation = ({ userProfile }) => {
  const navigate = useNavigate();
  const isAdmin = userProfile?.user?.role === 'admin';

  return (
    <nav className="dashboard-nav">
      <div className="nav-logo">
        <img src={CryptoPayIcon} alt="CryptoPay Logo" />
        <h1>CryptoPay</h1>
      </div>
      <div className="nav-links">
        <button onClick={() => navigate('/dashboard')}>Dashboard</button>
        <button onClick={() => navigate('/transactions')}>Transactions</button>
        <button onClick={() => navigate('/wallet')}>Wallet</button>
        <button onClick={() => navigate('/api')}>API Key</button>
        <button onClick={() => navigate('/profile')}>Profile</button>
        {isAdmin && (
          <button 
            onClick={() => navigate('/admin')}
            className="admin-link"
          >
            Admin Dashboard
          </button>
        )}
      </div>
    </nav>
  );
};

export default Navigation; 