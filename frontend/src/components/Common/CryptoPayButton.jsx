import React, { useState } from 'react';
import PaymentModal from './PaymentModal';

const CryptoPayButton = ({ 
  amount, // Amount in USD
  onSuccess, // Callback when payment is successful
  onError, // Callback when payment fails
  customStyle, // Optional custom styling
  buttonText = 'Pay with CryptoPay', // Customizable button text
  config = {} // Additional configuration
}) => {
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [error, setError] = useState(null);

  const defaultStyle = {
    padding: '12px 24px',
    fontSize: '16px',
    backgroundColor: '#00ff95',
    color: '#080808',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    fontWeight: '500',
    display: 'inline-flex',
    alignItems: 'center',
    gap: '8px'
  };

  const handleClick = () => {
    if (!amount || amount <= 0) {
      setError('Invalid amount');
      onError?.('Invalid amount');
      return;
    }
    setShowPaymentModal(true);
  };

  return (
    <>
      <button
        onClick={handleClick}
        style={{ ...defaultStyle, ...customStyle }}
        className="cryptopay-button"
      >
        <img 
          src="https://ibb.co/W4yRZM6b" 
          alt="CryptoPay" 
          style={{ width: '20px', height: '20px' }} 
        />
        {buttonText}
      </button>

      {showPaymentModal && (
        <PaymentModal
          amount={amount}
          config={config}
          onClose={() => {
            setShowPaymentModal(false);
            setError(null);
          }}
          onSuccess={() => {
            setShowPaymentModal(false);
            onSuccess?.();
          }}
          onError={(err) => {
            setError(err);
            onError?.(err);
          }}
        />
      )}
    </>
  );
};

export default CryptoPayButton; 