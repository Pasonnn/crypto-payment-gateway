import React, { useState, useEffect, useCallback } from 'react';
import { QRCodeSVG } from 'qrcode.react';
import axios from 'axios';
import CryptoPayConfig from '../../config/CryptoPayConfig';
import { API_URL } from '../../config/api';

const PaymentModal = ({ amount, config = {}, onClose, onSuccess, onError }) => {
  const [paymentAddress, setPaymentAddress] = useState('');
  const [timeLeft, setTimeLeft] = useState(600);
  const [status, setStatus] = useState('initializing');
  const [error, setError] = useState('');
  const [ethAmount, setEthAmount] = useState(null);

  // Move initializePayment to useCallback to prevent recreation
  const initializePayment = useCallback(async () => {
    try {
      const cryptoPayConfig = CryptoPayConfig.getConfig();
      
      const response = await axios.post(`${API_URL}/api/payments/create_payment`, {
        api_key: cryptoPayConfig.apiKey,
        amount: parseFloat(amount),
        currency: 'ETH'
      });

      if (response.data && response.data.payment_address) {
        setPaymentAddress(response.data.payment_address);
        setEthAmount(response.data.eth_amount);
        setStatus('pending');
      } else {
        throw new Error('Invalid response from server');
      }
    } catch (error) {
      const errorMessage = error.response?.data?.message || 
                          error.message || 
                          'Failed to initialize payment';
      setError(errorMessage);
      setStatus('failed');
      console.error('Payment initialization error:', error);
      onError?.(error);
    }
  }, [amount, onError]); // Add dependencies

  // Initialize payment only once when component mounts
  useEffect(() => {
    console.log("PaymentModal mounted");
    initializePayment();
  }, []); // Empty dependency array

  // Status checking effect
  useEffect(() => {
    let intervalId;
    if (status === 'pending' && paymentAddress) {
      intervalId = setInterval(checkPaymentStatus, 10000);
    }
    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [status, paymentAddress]);

  // Timer effect
  useEffect(() => {
    let timerId;
    if (timeLeft > 0 && status === 'pending') {
      timerId = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
    } else if (timeLeft === 0 && status === 'pending') {
      handlePaymentTimeout();
    }
    return () => {
      if (timerId) clearTimeout(timerId);
    };
  }, [timeLeft, status]);

  const checkPaymentStatus = async () => {
    if (!paymentAddress) return;

    try {
      // Check payment status first
      const statusResponse = await axios.get(
        `${API_URL}/api/payments/payment_status?payment_address=${paymentAddress}`
      );

      if (statusResponse.data.status === 'paid') {
        setStatus('completed');
        onSuccess();
        return; // Exit early if payment is confirmed
      }

      // If not paid, update payment status
      const cryptoPayConfig = CryptoPayConfig.getConfig();
      await axios.put(`${API_URL}/api/payments/update_payment_status`, {
        payment_address: paymentAddress,
        api_key: cryptoPayConfig.apiKey
      });

    } catch (error) {
      console.error('Payment status check error:', error);
    }
  };

  const handlePaymentTimeout = async () => {
    try {
      const cryptoPayConfig = CryptoPayConfig.getConfig();
      await axios.put(`${API_URL}/api/payments/timeout`, {
        payment_address: paymentAddress,
        api_key: cryptoPayConfig.apiKey
      });
      setStatus('timeout');
    } catch (error) {
      console.error('Error updating payment status:', error);
      setError('Failed to update payment status');
    }
  };

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className="payment-modal-overlay">
      <div className="payment-modal">
        <button className="close-button" onClick={onClose}>×</button>
        
        <div className="payment-content">
          <h2>Payment Details</h2>
          
          {status === 'initializing' && (
            <div className="payment-status">
              <p>Initializing payment...</p>
            </div>
          )}

          {status === 'pending' && paymentAddress && (
            <>
              <div className="payment-info">
                <p className="amount">{amount} USD</p>
                <p className="eth-amount">≈ {ethAmount} ETH</p>
                <p className="timer">Time remaining: {formatTime(timeLeft)}</p>
              </div>

              <div className="payment-address">
                <QRCodeSVG 
                  value={`ethereum:${paymentAddress}?amount=${ethAmount}`} 
                  size={200}
                  level="H"
                  includeMargin={true}
                />
                <p>Send exactly {ethAmount} ETH to:</p>
                <p className="address">{paymentAddress}</p>
              </div>

              <div className="payment-instructions">
                <p>Please send the payment within the time limit</p>
                <p>The payment will be confirmed automatically</p>
                <p>Network: Sepolia Testnet</p>
              </div>
            </>
          )}

          {status === 'completed' && (
            <div className="payment-status success">
              <h3>Payment Successful!</h3>
              <p>Thank you for your payment.</p>
              <button 
                className="btn-close-success"
                onClick={onClose}
              >
                Close Window
              </button>
            </div>
          )}

          {status === 'timeout' && (
            <div className="payment-status error">
              <h3>Payment Timeout</h3>
              <p>The payment session has expired.</p>
            </div>
          )}

          {status === 'failed' && (
            <div className="payment-status error">
              <h3>Payment Failed</h3>
              <p>{error}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PaymentModal; 