/**
 * Profile form component for updating user background information
 * Allows users to update their background data after registration
 */

import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';

const ProfileForm = () => {
  const { user, updateBackground, isLoading } = useAuth();
  const [formData, setFormData] = useState({
    softwareExperience: 'beginner',
    hardwareExperience: 'beginner',
    technicalBackground: 'other',
    primaryProgrammingLanguage: '',
  });
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    if (user) {
      setFormData({
        softwareExperience: user.softwareExperience || 'beginner',
        hardwareExperience: user.hardwareExperience || 'beginner',
        technicalBackground: user.technicalBackground || 'other',
        primaryProgrammingLanguage: user.primaryProgrammingLanguage || '',
      });
    }
  }, [user]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSuccessMessage('');

    try {
      const result = await updateBackground(formData);
      if (result.success) {
        setSuccessMessage('Profile updated successfully!');
        setTimeout(() => setSuccessMessage(''), 3000); // Clear message after 3 seconds
      } else {
        console.error('Update failed:', result.error);
      }
    } catch (err) {
      console.error('Update error:', err);
    }
  };

  if (!user) {
    return <div>Please sign in to view your profile.</div>;
  }

  return (
    <div className="auth-form-container">
      <h2>User Profile</h2>

      <div className="profile-info">
        <h3>Account Information</h3>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Name:</strong> {user.firstName} {user.lastName}</p>
      </div>

      <form onSubmit={handleSubmit} className="profile-form">
        <h3>Update Background Information</h3>

        {successMessage && <div className="success-message">{successMessage}</div>}

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

        <button type="submit" disabled={isLoading} className="submit-button">
          {isLoading ? 'Updating...' : 'Update Profile'}
        </button>
      </form>
    </div>
  );
};

export default ProfileForm;