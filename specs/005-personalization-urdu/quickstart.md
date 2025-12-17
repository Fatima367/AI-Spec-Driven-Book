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
- `POST /api/v1/personalize/{chapter_id}` - Personalizes content based on user profile
  - Uses Gemini 2.0 Flash for AI-powered content adaptation
  - Maintains syllabus compliance (ROS 2, Gazebo, Isaac, VLA concepts)
  - Simplifies for beginners or enhances for advanced users
  - Applies user preferences (learning mode, difficulty, focus area)

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
3. Click "Personalize for Me" button - content will be:
   - **Simplified** for users with beginner software/hardware experience (adds explanations, analogies, step-by-step breakdowns)
   - **Enhanced** for users with advanced experience (adds technical depth, best practices, research references)
   - **Adapted** based on learning preferences (visual, hands-on, theoretical)
4. Click "اردو میں ترجمہ کریں" button - should route to Urdu translated files if available

## How Personalization Works

### For Beginners (softwareExperience: "beginner" OR hardwareExperience: "beginner"):
- Simplifies technical jargon while keeping the terms
- Adds step-by-step explanations
- Includes beginner-friendly analogies and real-world examples
- Adds line-by-line code explanations
- **Maintains all ROS 2, Gazebo, Isaac, VLA concepts**

### For Advanced Users (softwareExperience: "advanced" OR hardwareExperience: "advanced"):
- Adds technical depth and implementation details
- Includes optimization techniques and best practices
- References research papers and cutting-edge developments
- Discusses architectural tradeoffs
- Adds performance and scalability considerations
- **Maintains all fundamental concepts while adding depth**

### Syllabus Compliance
All personalized content is validated to ensure:
- Core ROS 2 concepts maintained (nodes, topics, services, actions)
- Gazebo/Unity simulation concepts preserved (URDF, SDF, physics)
- NVIDIA Isaac platform concepts intact
- VLA (Vision-Language-Action) concepts maintained
- All code examples and practical exercises preserved
- Learning outcomes from course syllabus maintained