// src/components/Auth/RegisterForm.jsx
import React, { useState } from 'react';
import axios from 'axios';
import CryptoPayIcon from '../../assets/CryptoPayIcon.png';
import { useNavigate } from 'react-router-dom';

const RegisterForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleLogin = () => {
    navigate('/login');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Password validation
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    try {
      const response = await axios.post('http://localhost:5000/api/users/register', {
        username: formData.username,
        email: formData.email,
        password: formData.password
      });
      console.log('Registration successful:', response.data);
      // Handle successful registration (e.g., redirect to login)
      navigate('/login');
    } catch (err) {
      setError(err.response?.data?.message || 'Registration failed. Please try again.');
      console.error(err);
    }

  };

  return (
    <div className="auth-container">
      <form className="auth-form" onSubmit={handleSubmit}>
        <div className="logo">
          <img src={CryptoPayIcon} alt="Logo" />
          <h2>Create Account</h2>
        </div>
        <div className="content">
          {error && <p className="error-message">{error}</p>}
          <input
            type="text"
            name="username"
            placeholder="Username"
            value={formData.username}
            onChange={handleChange}
            required
            className="form-input"
          />
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            required
            className="form-input"
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
            className="form-input"
          />
          <input
            type="password"
            name="confirmPassword"
            placeholder="Confirm Password"
            value={formData.confirmPassword}
            onChange={handleChange}
            required
            className="form-input"
          />
          <button type="submit" className="btn-login action-button" onClick={handleSubmit}>
            Create Account
          </button>
          <div className="auth-switch">
            <p>Already have an account? <a href="/login" onClick={handleLogin}>Login</a></p>
          </div>
        </div>
      </form>

    </div>
  );
};

export default RegisterForm;