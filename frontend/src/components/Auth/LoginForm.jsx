// src/components/Auth/LoginForm.jsx
import React, { useState } from 'react';
import axios from 'axios';
import CryptoPayIcon from '../../assets/CryptoPayIcon.png';
import { useNavigate } from 'react-router-dom';


const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/api/users/login', {
        email,
        password,
      });
      console.log('Login successful:', response.data);
      // Handle successful login (e.g., store token, redirect)
      localStorage.setItem('token', response.data.token); // Store the token in local storage
      navigate('/dashboard'); // Redirect to the dashboard
    } catch (err) {
      setError('Login failed. Please check your credentials.');
      console.error(err);
    }
  };

  const handleSignup = () => {
    // Implement signup logic here
    navigate('/register');
    console.log('Signup button clicked');
  };




  const handleForgotPassword = () => {
    // Implement forgot password logic here
    console.log('Forgot password button clicked');
  };

  return (
    <div className="auth-container">
      <form className="auth-form" onSubmit={handleLogin}>
        <div className="logo">
          <img src={CryptoPayIcon} alt="Logo" />
          <h2>Login</h2>
        </div>
        <div className="content">
          {error && <p className="error-message">{error}</p>}
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="form-input"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="form-input"
          />
          <button type="submit" className="btn-login action-button">
            Log In
          </button>
          <div className="forgot-link">
            <a href="#">Forgot your email or password?</a>
          </div>
          <button type="button" className="btn-signup action-button" onClick={handleSignup}>
            Sign Up
          </button>
        </div>
      </form>
    </div>
  );
};

export default LoginForm;