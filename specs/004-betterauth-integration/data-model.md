# Data Model: BetterAuth Integration with User Background

## Overview
This document defines the data models for user authentication and background information collection for the Physical AI & Humanoid Robotics textbook application.

## User Entity

### User (Core Authentication Data)
**Source**: Extended from BetterAuth's default user model

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | String (UUID) | Primary Key, Not Null | Unique user identifier |
| email | String | Unique, Not Null, Email Format | User's email address |
| emailVerified | DateTime | Nullable | Timestamp when email was verified |
| firstName | String | Nullable, Max 50 chars | User's first name |
| lastName | String | Nullable, Max 50 chars | User's last name |
| createdAt | DateTime | Not Null | Account creation timestamp |
| updatedAt | DateTime | Not Null | Last update timestamp |
| image | String | Nullable, URL Format | Profile image URL |

### UserBackground (Extended Profile Data)
**Source**: Custom extension to BetterAuth user model for personalization

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| userId | String (UUID) | Foreign Key, Not Null, References User.id | Reference to user account |
| softwareExperience | String | Not Null, Enum: ["beginner", "intermediate", "advanced"] | User's software experience level |
| hardwareExperience | String | Not Null, Enum: ["beginner", "intermediate", "advanced"] | User's hardware experience level |
| technicalBackground | String | Not Null, Enum: ["computer_science", "electrical_engineering", "mechanical_engineering", "other"] | User's technical background |
| primaryProgrammingLanguage | String | Nullable, Enum: ["python", "cpp", "javascript", "other"] | Primary programming language familiarity |
| backgroundCompleted | Boolean | Not Null, Default: false | Whether user has completed background questions |

## Session Entity

### Session (Authentication Sessions)
**Source**: BetterAuth's default session model

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | String | Primary Key, Not Null | Unique session identifier |
| userId | String (UUID) | Foreign Key, Not Null, References User.id | Reference to user account |
| expiresAt | DateTime | Not Null | Session expiration timestamp |
| createdAt | DateTime | Not Null | Session creation timestamp |
| ipAddress | String | Nullable | IP address of session origin |
| userAgent | String | Nullable | User agent string of session origin |

## Database Schema

### Postgres Tables

```sql
-- BetterAuth handles the base user and session tables
-- We extend with our custom background data

-- User background information table
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

-- Index for faster lookups by user_id
CREATE INDEX idx_user_background_user_id ON user_background(user_id);

-- Trigger to update the updated_at timestamp
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

## Relationships

1. **User → UserBackground**: One-to-One relationship (each user has one background profile)
2. **User → Sessions**: One-to-Many relationship (each user can have multiple active sessions)

## Validation Rules

### User Registration Validation
- Email must be in valid format
- Password must meet minimum security requirements (8+ characters, mixed case, numbers)
- Background questions are optional during signup but encouraged

### UserBackground Validation
- softwareExperience must be one of: "beginner", "intermediate", "advanced"
- hardwareExperience must be one of: "beginner", "intermediate", "advanced"
- technicalBackground must be one of: "computer_science", "electrical_engineering", "mechanical_engineering", "other"
- primaryProgrammingLanguage must be one of: "python", "cpp", "javascript", "other" or null

## State Transitions

### User Background Completion
- Initial state: backgroundCompleted = false
- After user fills background info: backgroundCompleted = true
- User can update background info at any time, keeping backgroundCompleted = true

## API Data Transfer Objects (DTOs)

### User Registration DTO
```typescript
interface UserRegistrationRequest {
  email: string;
  password: string;
  firstName?: string;
  lastName?: string;
  softwareExperience?: 'beginner' | 'intermediate' | 'advanced';
  hardwareExperience?: 'beginner' | 'intermediate' | 'advanced';
  technicalBackground?: 'computer_science' | 'electrical_engineering' | 'mechanical_engineering' | 'other';
  primaryProgrammingLanguage?: 'python' | 'cpp' | 'javascript' | 'other';
}
```

### User Profile DTO
```typescript
interface UserProfileResponse {
  id: string;
  email: string;
  firstName?: string;
  lastName?: string;
  softwareExperience: 'beginner' | 'intermediate' | 'advanced';
  hardwareExperience: 'beginner' | 'intermediate' | 'advanced';
  technicalBackground: 'computer_science' | 'electrical_engineering' | 'mechanical_engineering' | 'other';
  primaryProgrammingLanguage?: 'python' | 'cpp' | 'javascript' | 'other';
  backgroundCompleted: boolean;
  createdAt: Date;
  updatedAt: Date;
}
```

### Update Background DTO
```typescript
interface UpdateBackgroundRequest {
  softwareExperience?: 'beginner' | 'intermediate' | 'advanced';
  hardwareExperience?: 'beginner' | 'intermediate' | 'advanced';
  technicalBackground?: 'computer_science' | 'electrical_engineering' | 'mechanical_engineering' | 'other';
  primaryProgrammingLanguage?: 'python' | 'cpp' | 'javascript' | 'other';
}
```