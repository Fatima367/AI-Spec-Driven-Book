# Quickstart: Personalization and Urdu Translation

## Overview
This feature adds personalization and Urdu translation capabilities to the Physical AI & Humanoid Robotics textbook. Users can click "Personalize for Me" to adapt content to their learning preferences, or "اردو میں ترجمہ کریں" to read content in Urdu.

## Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.10+
- BetterAuth configured with user profiles
- Gemini API key for translation
- Access to the textbook MDX content files

## Setup

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### 2. Frontend Setup
```bash
cd book_frontend
npm install
```

### 3. Environment Variables
Create `.env` file in the backend directory:
```env
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=your_neon_postgres_url
BETTER_AUTH_URL=your_auth_url
```

## Implementation Steps

### 1. Generate Urdu Content Files
Create Urdu translations of all MDX files by duplicating existing files with 'urdu-' prefix:
```bash
# Create duplicate files with 'urdu' prefix for all MDX files
# This can be done manually or with a script that copies each .mdx file to urdu-*.mdx
```

### 2. Update Frontend Components
The PersonalizationButtons component is already integrated into chapter MDX files:
```md
import { PersonalizeButton, UrduTranslationButton } from '@site/src/components/PersonalizationButtons';

<PersonalizeButton />
<UrduTranslationButton />
```

### 3. Run the Application
```bash
# Start backend
cd backend
python main.py

# Start frontend
cd book_frontend
npm run start
```

## API Endpoints

### Personalization
- `POST /api/personalize/{chapter_id}` - Personalizes content based on user profile

## File Structure
```
book_frontend/
├── docs/                    # Original MDX files
├── docs/urdu-*/            # Generated Urdu MDX files (not in sidebar)
├── src/components/PersonalizationButtons/  # Button components
└── sidebars.ts             # Navigation (excludes Urdu files)
```

## Testing
1. Login with an authenticated user
2. Navigate to any chapter
3. Click "Personalize for Me" button - content should adapt to user preferences
4. Click "اردو میں ترجمہ کریں" button - should route to Urdu translated files if available