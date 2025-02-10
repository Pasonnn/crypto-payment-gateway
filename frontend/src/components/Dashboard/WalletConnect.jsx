import React, { useState } from 'react';
import axios from 'axios';
import detectEthereumProvider from '@metamask/detect-provider';

const WalletConnect = ({ walletAddress, fetchWalletAddress }) => {
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const connectWallet = async () => {
    try {
      setIsConnecting(true);
      setError('');

      // Check if MetaMask is installed
      const provider = await detectEthereumProvider();
      
      if (!provider) {
        setError('Please install MetaMask to connect your wallet!');
        return;
      }

      // Request account access
      const accounts = await window.ethereum.request({ 
        method: 'eth_requestAccounts' 
      });
      
      if (accounts.length === 0) {
        setError('No accounts found! Please create an account in MetaMask.');
        return;
      }

      const address = accounts[0];
      
      // Update wallet address in backend
      const token = localStorage.getItem('token');
      await axios.put('http://localhost:5000/api/users/update_wallet',
        { wallet_address: address },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setSuccess('Wallet connected successfully!');
      fetchWalletAddress();

    } catch (error) {
      if (error.code === 4001) {
        // User rejected the connection
        setError('Please connect your wallet to continue.');
      } else {
        setError(error.message || 'Failed to connect wallet');
      }
    } finally {
      setIsConnecting(false);
    }
  };

  return (
    <div className="wallet-section">
      <h2>Connect Wallet</h2>
      <div className="current-wallet">
        <h3>Current Wallet Address:</h3>
        <p>{walletAddress || 'No wallet connected'}</p>
      </div>
      
      {error && <p className="error-message">{error}</p>}
      {success && <p className="success-message">{success}</p>}
      
      <div className="wallet-actions">
        <button 
          onClick={connectWallet} 
          disabled={isConnecting}
          className="btn-connect-wallet"
        >
          {isConnecting ? 'Connecting...' : walletAddress ? 'Change Wallet' : 'Connect MetaMask'}
        </button>
      </div>
    </div>
  );
};

export default WalletConnect; 