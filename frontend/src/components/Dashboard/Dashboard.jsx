// src/components/Dashboard/Dashboard.jsx
import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import axios from 'axios';
import CryptoPayIcon from '../../assets/CryptoPayIcon.png';
import { useNavigate } from 'react-router-dom';
import UserProfile from './UserProfile';
import Notification from '../Common/Notification'
import WalletConnect from './WalletConnect';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const Dashboard = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [transactions, setTransactions] = useState([]);
  const [apiKey, setApiKey] = useState('');
  const [walletAddress, setWalletAddress] = useState('');
  const [userProfile, setUserProfile] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);
  const [notification, setNotification] = useState(null);
  const [revenueData, setRevenueData] = useState({
    labels: [],
    datasets: [{
      label: 'Revenue (ETH)',
      data: [],
      fill: false,
      borderColor: 'rgb(0, 255, 149)',
      tension: 0.1
    }]
  });

  // Chart options
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(255, 255, 255, 0.1)'
        },
        ticks: {
          color: '#ffffff'
        }
      },
      x: {
        grid: {
          color: 'rgba(255, 255, 255, 0.1)'
        },
        ticks: {
          color: '#ffffff'
        }
      }
    },
    plugins: {
      legend: {
        labels: {
          color: '#ffffff'
        }
      }
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    fetchDashboardData();
    fetchUserProfile();
    fetchTransactions();
    fetchApiKey();
    fetchWalletAddress();
  }, [navigate]);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:5000/api/users/dashboard', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setDashboardData(response.data.dashboard);
      
      // Update revenue chart with dashboard data
      if (response.data.revenue_data) {
        setRevenueData({
          labels: response.data.revenue_data.map(item => new Date(item.date).toLocaleDateString()),
          datasets: [{
            label: 'Revenue (ETH)',
            data: response.data.revenue_data.map(item => item.amount),
            fill: false,
            borderColor: 'rgb(0, 255, 149)',
            tension: 0.1
          }]
        });
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      if (error.response?.status === 401) navigate('/login');
    }
  };

  const fetchUserProfile = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:5000/api/users/profile', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUserProfile(response.data);
      localStorage.setItem('userRole', response.data.user.role); // Store user role
    } catch (error) {
      console.error('Error fetching user profile:', error);
    }
  };

  const fetchTransactions = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:5000/api/users/transactions', {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      // Process transactions for the chart
      const transactionsData = response.data.transactions;
      const processedData = processTransactionsForChart(transactionsData);
      
      setTransactions(transactionsData);
      setRevenueData(processedData);
    } catch (error) {
      console.error('Error fetching transactions:', error);
    }
  };

  const fetchApiKey = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:5000/api/users/api_key', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setApiKey(response.data.api_key || 'No API key generated');
    } catch (error) {
      console.error('Error fetching API key:', error);
      setApiKey('Error fetching API key');
    }
  };

  const regenerateApiKey = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('http://localhost:5000/api/users/regenerate_api_key', {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setApiKey(response.data.api_key);
    } catch (error) {
      console.error('Error regenerating API key:', error);
    }
  };

  const updateWallet = async (address) => {
    try {
      const token = localStorage.getItem('token');
      await axios.put('http://localhost:5000/api/users/update_wallet', 
        { wallet_address: address },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setWalletAddress(address);
    } catch (error) {
      console.error('Error updating wallet:', error);
    }
  };

  const fetchWalletAddress = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:5000/api/users/profile', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setWalletAddress(response.data.user.wallet_address || 'No wallet bound');
    } catch (error) {
      console.error('Error fetching wallet address:', error);
    }
  };

  // Add this helper function to process transactions for the chart
  const processTransactionsForChart = (transactions) => {
    // Create a map to store daily totals
    const dailyTotals = {};
    
    Object.values(transactions).forEach(transaction => {
      const date = new Date(transaction.created_at).toLocaleDateString();
      if (!dailyTotals[date]) {
        dailyTotals[date] = 0;
      }
      if (transaction.status === 'paid') {
        dailyTotals[date] += parseFloat(transaction.amount);
      }
    });

    // Sort dates and create chart data
    const sortedDates = Object.keys(dailyTotals).sort((a, b) => new Date(a) - new Date(b));
    
    return {
      labels: sortedDates,
      datasets: [{
        label: 'Daily Revenue (ETH)',
        data: sortedDates.map(date => dailyTotals[date].toFixed(5)),
        fill: false,
        borderColor: 'rgb(0, 255, 149)',
        tension: 0.1
      }]
    };
  };

  const handleCopyPrivateKey = (key) => {
    navigator.clipboard.writeText(key);
    setNotification('Private key copied to clipboard!'); // Set notification message
    setTimeout(() => setNotification(null), 3000); // Clear notification after 3 seconds
  };

  return (
    <div className="dashboard-container">
      {notification && (
        <Notification message={notification} onClose={() => setNotification(null)} />
      )}
      <nav className="dashboard-nav">
        <div className="nav-logo">
          <img src={CryptoPayIcon} alt="CryptoPay Logo" />
          <h1>CryptoPay</h1>
        </div>
        <div className="nav-links">
          <button 
            className={activeTab === 'dashboard' ? 'active' : ''} 
            onClick={() => setActiveTab('dashboard')}
          >
            Dashboard
          </button>
          <button 
            className={activeTab === 'transactions' ? 'active' : ''} 
            onClick={() => setActiveTab('transactions')}
          >
            Transactions
          </button>
          <button 
            className={activeTab === 'wallet' ? 'active' : ''} 
            onClick={() => setActiveTab('wallet')}
          >
            Wallet
          </button>
          <button 
            className={activeTab === 'api' ? 'active' : ''} 
            onClick={() => setActiveTab('api')}
          >
            API Key
          </button>
          <button 
            className={activeTab === 'profile' ? 'active' : ''} 
            onClick={() => setActiveTab('profile')}
          >
            Profile
          </button>
          {userProfile?.user?.role === 'admin' && (
            <button 
              className="nav-button"
              onClick={() => navigate('/admin')}
            >
              Management
            </button>
          )}
        </div>
      </nav>

      <main className="dashboard-main">
        {activeTab === 'dashboard' && (
          <>
            <div className="dashboard-overview">
              <div className="overview-card">
                <h3>Total Revenue</h3>
                <p>{(dashboardData?.revenue || 0).toFixed(5)} ETH</p>
              </div>
              <div className="overview-card">
                <h3>Total Transactions</h3>
                <p>{dashboardData?.transactions || '0'}</p>
              </div>
              <div className="overview-card">
                <h3>Fee</h3>
                <p>{(dashboardData?.fee || 0).toFixed(5)} ETH</p>
              </div>
            </div>
            <div className="revenue-chart">
              <h2>Revenue Overview</h2>
              <div className="chart-container">
                <Line data={revenueData} options={chartOptions} />
              </div>
            </div>
            <div className="recent-transactions">
              <h2>Recent Transactions</h2>
              <div className="transactions-list">
                {Object.keys(transactions).length > 0 ? (
                  Object.entries(transactions)
                    .sort((a, b) => new Date(b[1].created_at) - new Date(a[1].created_at))
                    .slice(0, 5)
                    .map(([id, transaction]) => (
                      <div key={id} className="transaction-item">
                        <div className="transaction-info">
                          <span className="amount">{parseFloat(transaction.amount).toFixed(5)} ETH</span>
                          <span className="date">
                            {new Date(transaction.created_at).toLocaleDateString()}
                            <span className="separator"> | </span>
                            {new Date(transaction.created_at).toLocaleTimeString()}
                          </span>
                        </div>
                        <span className={`status ${transaction.status.toLowerCase()}`}>
                          {transaction.status}
                        </span>
                      </div>
                    ))
                ) : (
                  <p className="no-data">No transactions yet</p>
                )}
              </div>
            </div>
          </>
        )}

        {activeTab === 'transactions' && (
          <div className="transactions-table">
            <h2>All Transactions</h2>
            {Object.keys(transactions).length > 0 ? (
              <table>
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Amount (ETH)</th>
                    <th>Fee (ETH)</th>
                    <th>Status</th>
                    <th>Address</th>
                    <th>Private Key</th>
                    <th>Transaction ID</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(transactions)
                    .sort((a, b) => new Date(b[1].created_at) - new Date(a[1].created_at))
                    .map(([id, transaction]) => (
                      <tr key={id}>
                        <td>
                          {new Date(transaction.updated_at).toLocaleDateString()} 
                          {' '}
                          {new Date(transaction.updated_at).toLocaleTimeString()}
                        </td>
                        <td>{parseFloat(transaction.amount).toFixed(5)}</td>
                        <td>{parseFloat(transaction.fee).toFixed(5)}</td>
                        <td className={`status ${transaction.status.toLowerCase()}`}>
                          {transaction.status}
                        </td>
                        <td>
                          <a href={`https://sepolia.etherscan.io/address/${transaction.payment_address}`} target="_blank" rel="noopener noreferrer">
                            {`${transaction.payment_address.slice(0, 5)}...${transaction.payment_address.slice(-5)}`}
                          </a>
                        </td>
                        <td>
                          <span 
                            onClick={() => handleCopyPrivateKey(transaction.payment_address_private_key)}
                          >
                            {`${transaction.payment_address_private_key.slice(0, 5)}...${transaction.payment_address_private_key.slice(-5)}`}
                          </span>
                        </td>
                        <td>{id}</td>
                      </tr>
                    ))}
                </tbody>
              </table>
            ) : (
              <p className="no-data">No transactions available</p>
            )}
          </div>
        )}

        {activeTab === 'wallet' && (
          <WalletConnect 
            walletAddress={walletAddress}
            fetchWalletAddress={fetchWalletAddress}
          />
        )}

        {activeTab === 'api' && (
          <div className="api-section">
            <h2>API Key Management</h2>
            <div className="current-api">
              <h3>Your API Key:</h3>
              <p>{apiKey || 'No API key generated'}</p>
            </div>
            <div className="api-key-display">
              <button onClick={regenerateApiKey}>Regenerate API Key</button>
            </div>
          </div>
        )}

        {activeTab === 'profile' && (
          <UserProfile 
            userProfile={userProfile}
            fetchUserProfile={fetchUserProfile}
          />
        )}
      </main>
    </div>
  );
};

export default Dashboard;