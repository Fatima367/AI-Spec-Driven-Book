# Quickstart Guide: BetterAuth Integration

## Overview
This guide provides step-by-step instructions for setting up and using the BetterAuth integration with user background data collection for the Physical AI & Humanoid Robotics textbook application.

## Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.10+
- PostgreSQL database (Neon recommended for free tier)
- Basic knowledge of Docusaurus and FastAPI

## Installation

### 1. Backend Setup (FastAPI + BetterAuth)

First, install the required backend dependencies:

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install better-auth fastapi uvicorn python-multipart
```

### 2. Environment Configuration

Create a `.env` file in the backend directory with the following variables:

```env
# BetterAuth Configuration
BETTER_AUTH_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-super-secret-jwt-secret-key-here-make-it-long-and-random

# Database Configuration (Neon Postgres)
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname

# Session Configuration
BETTER_AUTH_TRUST_HOST=true
```

### 3. BetterAuth Configuration

Create a `src/auth/better_auth_config.py` file:

```python
from better_auth import auth, models
from better_auth import postgres
from pydantic import BaseModel
from typing import Optional

class UserBackground(BaseModel):
    software_experience: Optional[str] = "beginner"
    hardware_experience: Optional[str] = "beginner"
    technical_background: Optional[str] = "other"
    primary_programming_language: Optional[str] = None
    background_completed: bool = False

# Initialize BetterAuth with Neon Postgres
auth_client = auth(
    secret="your-super-secret-jwt-secret-key-here-make-it-long-and-random",
    database_url="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname",
    # Custom user data fields for background information
    additional_user_data={
        "software_experience": str,
        "hardware_experience": str,
        "technical_background": str,
        "primary_programming_language": str,
        "background_completed": bool
    }
)
```

### 4. Database Migration

Create the user_background table in your database:

```sql
CREATE TABLE user_background (
  user_id UUID PRIMARY KEY REFERENCES auth_user(id) ON DELETE CASCADE,
  software_experience VARCHAR(20) NOT NULL CHECK (software_experience IN ('beginner', 'intermediate', 'advanced')),
  hardware_experience VARCHAR(20) NOT NULL CHECK (hardware_experience IN ('beginner', 'intermediate', 'advanced')),
  technical_background VARCHAR(30) NOT NULL CHECK (technical_background IN ('computer_science', 'electrical_engineering', 'mechanical_engineering', 'other')),
  primary_programming_language VARCHAR(20) CHECK (primary_programming_language IN ('python', 'cpp', 'javascript', 'other')),
  background_completed BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_background_user_id ON user_background(user_id);

-- Trigger for updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_user_background_updated_at
    BEFORE UPDATE ON user_background
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### 5. Frontend Setup (Docusaurus)

Install the required frontend dependencies:

```bash
# Navigate to book_frontend directory
cd book_frontend

# Install BetterAuth client
npm install better-auth @better-auth/client
```

### 6. Frontend Configuration

Create a `src/contexts/AuthContext.tsx` file for authentication state management:

```tsx
import React, { createContext, useContext, useEffect, useState } from 'react';
import { useAuth } from '@better-auth/client/react';
import { authClient } from '../services/authService';

interface AuthContextType {
  user: any;
  signIn: (email: string, password: string) => Promise<any>;
  signUp: (userData: any) => Promise<any>;
  signOut: () => Promise<void>;
  updateProfile: (profileData: any) => Promise<any>;
  updateBackground: (backgroundData: any) => Promise<any>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const {
    session,
    signIn: authSignIn,
    signUp: authSignUp,
    signOut: authSignOut
  } = useAuth();

  // ... implementation for auth context
};

export const useAuthContext = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuthContext must be used within an AuthProvider');
  }
  return context;
};
```

## Running the Application

### 1. Start the Backend Server

```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

### 2. Start the Frontend Server

```bash
cd book_frontend
npm start
```

## API Usage Examples

### Register a New User

```javascript
// Example of registering a new user with background information
const registerUser = async () => {
  try {
    const response = await fetch('/api/auth/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: 'user@example.com',
        password: 'securePassword123',
        firstName: 'John',
        lastName: 'Doe',
        softwareExperience: 'intermediate',
        hardwareExperience: 'beginner',
        technicalBackground: 'computer_science',
        primaryProgrammingLanguage: 'python'
      }),
    });

    if (response.ok) {
      const data = await response.json();
      console.log('User registered:', data.user);
    } else {
      console.error('Registration failed:', await response.json());
    }
  } catch (error) {
    console.error('Error during registration:', error);
  }
};
```

### Login a User

```javascript
// Example of logging in a user
const loginUser = async () => {
  try {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: 'user@example.com',
        password: 'securePassword123',
      }),
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Login successful:', data.user);
    } else {
      console.error('Login failed:', await response.json());
    }
  } catch (error) {
    console.error('Error during login:', error);
  }
};
```

### Update User Background

```javascript
// Example of updating user background information
const updateBackground = async (userId, token) => {
  try {
    const response = await fetch('/api/auth/profile/background', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        softwareExperience: 'advanced',
        hardwareExperience: 'intermediate',
        technicalBackground: 'electrical_engineering',
        primaryProgrammingLanguage: 'cpp'
      }),
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Background updated:', data);
    } else {
      console.error('Update failed:', await response.json());
    }
  } catch (error) {
    console.error('Error updating background:', error);
  }
};
```

## Personalization Integration

The collected background information can be used to personalize content as follows:

```javascript
// Example of using background data for personalization
const getPersonalizedContent = (userBackground, originalContent) => {
  if (!userBackground) return originalContent;

  const { softwareExperience, hardwareExperience, technicalBackground } = userBackground;

  // Adjust content complexity based on user experience
  if (softwareExperience === 'beginner') {
    // Simplify code examples and add more explanations
    return simplifyContent(originalContent);
  } else if (softwareExperience === 'advanced') {
    // Add more complex examples and advanced concepts
    return enhanceContent(originalContent);
  }

  return originalContent;
};
```

## Testing

### Backend Tests

```bash
cd backend
pytest tests/api/test_auth.py
```

### Frontend Tests

```bash
cd book_frontend
npm test
```

## Deployment

### Environment Variables for Production

For production deployment, ensure these environment variables are set:

```env
BETTER_AUTH_URL=https://yourdomain.com
BETTER_AUTH_SECRET=your-production-jwt-secret
DATABASE_URL=your-production-database-url
BETTER_AUTH_COOKIE_DOMAIN=yourdomain.com
BETTER_AUTH_COOKIE_SECURE=true
```

## Troubleshooting

### Common Issues

1. **Session not persisting**: Ensure your domain and cookie settings are correct
2. **Database connection errors**: Verify your DATABASE_URL is properly formatted
3. **CORS issues**: Configure CORS settings in your FastAPI application
4. **Background data not saving**: Check that the user_background table exists and has proper permissions

### Debugging Tips

- Enable debug logging in BetterAuth configuration
- Check server logs for authentication-related errors
- Verify that the user_background table is properly created in your database
- Test API endpoints directly using tools like Postman or curl

## Next Steps

1. Implement the "Personalize for Me" button functionality using collected background data
2. Add the Urdu translation feature as specified in the bonus features
3. Implement the profile management UI components in Docusaurus
4. Add comprehensive error handling and user feedback mechanisms