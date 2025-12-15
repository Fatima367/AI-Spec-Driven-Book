import React from 'react';
import './LoadingStates.css';

interface LoadingStateProps {
  isLoading: boolean;
  message?: string;
}

export const LoadingSpinner: React.FC = () => {
  return (
    <div className="loading-spinner">
      <div className="spinner"></div>
    </div>
  );
};

export const LoadingState: React.FC<LoadingStateProps> = ({ isLoading, message = "Processing..." }) => {
  if (!isLoading) return null;

  return (
    <div className="loading-overlay">
      <div className="loading-content">
        <div className="spinner"></div>
        <p>{message}</p>
      </div>
    </div>
  );
};

export const ErrorMessage: React.FC<{ message: string, onClose?: () => void }> = ({ message, onClose }) => {
  return (
    <div className="error-message">
      <span className="error-text">{message}</span>
      {onClose && (
        <button className="close-btn" onClick={onClose}>×</button>
      )}
    </div>
  );
};