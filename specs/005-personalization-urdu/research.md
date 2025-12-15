# Research: Personalization and Urdu Translation Implementation

## Decision: Complete Implementation of Personalization and Translation Features
- The buttons are already added to chapters but are not fully functional
- Need to implement backend API endpoints and connect them to frontend components

## Rationale:
- The frontend components exist but only show alerts (mock functionality)
- Need to implement actual API calls to backend services
- Need to create Urdu content files with 'urdu' prefix as specified in requirements

## Alternatives considered:
1. Keep current mock implementation - rejected as it doesn't provide actual functionality
2. Replace with different UI approach - rejected as current UI is already integrated
3. Implement full functionality as planned - accepted as it meets requirements

## Technical Research Findings:

### 1. Current State
- PersonalizeButton and UrduTranslationButton components exist in `/src/components/PersonalizationButtons/index.tsx`
- CSS styling is implemented in `/src/components/PersonalizationButtons/PersonalizationButtons.css`
- Components are imported and used in MDX files (e.g., `import { PersonalizeButton, UrduTranslationButton } from '@site/src/components/PersonalizationButtons';`)
- Components currently only show alerts and have TODO comments for API integration
- No Urdu content files with 'urdu' prefix currently exist in the docs directory

### 2. Backend API Requirements
- Need `/api/personalize/{chapterId}` endpoint for personalization
- Personalization endpoint needs authentication validation

### 3. Content Management
- Need to generate duplicate MDX files with 'urdu' prefix for all existing MDX files
- Urdu files must not appear in sidebar navigation (handled in sidebars.ts)
- When Urdu button is clicked, it should route to the corresponding Urdu file if it exists
- Need to implement proper file path resolution for Urdu content

### 4. Authentication Integration
- Both features require logged-in users
- Must validate authentication before processing requests
- BetterAuth integration is already in place

### 5. Implementation Approach
- Create backend API endpoints in FastAPI for personalization and Urdu file management
- Connect frontend buttons to backend APIs
- Implement Urdu content generation process that creates files with 'urdu' prefix
- Update frontend to properly route to Urdu content when available
- Ensure proper error handling and loading states