/**
 * Signup form component with email/password fields and background questions
 * Implements the signup flow with background information collection
 */

import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';

const SignupForm = ({ onSignupSuccess }) => {
  const { signUp } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    firstName: '',
    lastName: '',
    softwareExperience: 'beginner',
    hardwareExperience: 'beginner',
    technicalBackground: 'other',
    primaryProgrammingLanguage: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const result = await signUp(formData);
      if (result.success) {
        if (onSignupSuccess) {
          onSignupSuccess(result.user);
        }
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError(err.message || 'An error occurred during signup');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-form-container">
      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit} className="signup-form">
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            minLength="8"
          />
          <small>Password must be at least 8 characters</small>
        </div>

        <div className="form-group">
          <label htmlFor="firstName">First Name:</label>
          <input
            type="text"
            id="firstName"
            name="firstName"
            value={formData.firstName}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="lastName">Last Name:</label>
          <input
            type="text"
            id="lastName"
            name="lastName"
            value={formData.lastName}
            onChange={handleChange}
          />
        </div>

        {/* Background Questions Section */}
        <div className="background-questions-section">
          <h3>Background Information</h3>

          <div className="form-group">
            <label htmlFor="softwareExperience">Software Experience:</label>
            <select
              id="softwareExperience"
              name="softwareExperience"
              value={formData.softwareExperience}
              onChange={handleChange}
            >
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="hardwareExperience">Hardware Experience:</label>
            <select
              id="hardwareExperience"
              name="hardwareExperience"
              value={formData.hardwareExperience}
              onChange={handleChange}
            >
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="technicalBackground">Technical Background:</label>
            <select
              id="technicalBackground"
              name="technicalBackground"
              value={formData.technicalBackground}
              onChange={handleChange}
            >
              <option value="computer_science">Computer Science</option>
              <option value="electrical_engineering">Electrical Engineering</option>
              <option value="mechanical_engineering">Mechanical Engineering</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="primaryProgrammingLanguage">Primary Programming Language:</label>
            <select
              id="primaryProgrammingLanguage"
              name="primaryProgrammingLanguage"
              value={formData.primaryProgrammingLanguage}
              onChange={handleChange}
            >
              <option value="">Select a language</option>
              <option value="python">Python</option>
              <option value="cpp">C++</option>
              <option value="javascript">JavaScript</option>
              <option value="other">Other</option>
            </select>
          </div>
        </div>

        <button type="submit" disabled={loading} className="submit-button">
          {loading ? 'Creating Account...' : 'Sign Up'}
        </button>
      </form>
    </div>
  );
};

export default SignupForm;