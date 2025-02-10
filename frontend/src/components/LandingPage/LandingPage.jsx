import React from 'react';
import { useNavigate } from 'react-router-dom';
import CryptoPayIcon from '../../assets/CryptoPayIcon.png';
import HeroImage from '../../assets/HeroImage.png'
import FastImage from '../../assets/Fast.png'
import SecureImage from '../../assets/Secure.png'
import CheapImage from '../../assets/Cheap.png'
import StepOneImage from '../../assets/Step1.png';
import StepTwoImage from '../../assets/Step2.png';
import StepThreeImage from '../../assets/Step3.png';

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="landing-container">
      <header className="landing-header">
        <div className="logo">
          <img src={CryptoPayIcon} alt="CryptoPay Logo" />
          <h1>CryptoPay</h1>
        </div>
        <div className="header-buttons">
          <button onClick={() => navigate('/login')} className="btn-login">Login</button>
          <button onClick={() => navigate('/register')} className="btn-signup">Sign Up</button>
        </div>
      </header>

      <main className="landing-main">
        <section className="hero-section">
          <h1>Next-Gen Crypto Payment Solution</h1>
          <p>Fast, secure, and seamless cryptocurrency transactions for everyone</p>
          <img src={HeroImage} alt="Hero Image" />
          <button onClick={() => navigate('/register')} className="btn-get-started">
            Get Started
          </button>
        </section>

        <section className="features-section">
          <h2>Why Choose CryptoPay?</h2>
          <div className="features-grid">
            <div className="feature-card">
              <img src={SecureImage} alt="Secure Image" />
              <h3>Secure Transactions</h3>
              <p>Our advanced security protocols ensuring your transactions are safe and protected.</p>
            </div>
            <div className="feature-card">
            <img src={FastImage} alt="Fast Image" />
            <h3>Lightning Fast</h3>
              <p>Enjoy rapid transaction speeds that allow you to send and receive cryptocurrencies in seconds.</p>
            </div>
            <div className="feature-card">
            <img src={CheapImage} alt="Cheap Image" />
            <h3>Low Fees</h3>
              <p>We offer competitive rates, ensuring that you pay less for every transaction you make.</p>
            </div>
          </div>
        </section>

        <section className="how-it-works">
          <h2>How It Works</h2>
          <div className="steps-container">
            <div className="step-card">
              <img src={StepOneImage} alt="Create Account" />
              <h3>Create Account</h3>
              <p>Sign up for a CryptoPay account in minutes. All you need is your email</p>
            </div>
            <div className="step-card">
              <img src={StepTwoImage} alt="Connect Wallet" />
              <h3>Bind Wallet</h3>
              <p>Link your crypto wallet to start receiving payments securely.</p>
            </div>
            <div className="step-card">
              <img src={StepThreeImage} alt="Start Transacting" />
              <h3>Start Transacting</h3>
              <p>Get API key and receive crypto payments instantly with minimal fees.</p>
            </div>
          </div>
        </section>
      </main>

      <footer className="landing-footer">
        <p>© 2024 CryptoPay. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default LandingPage; 