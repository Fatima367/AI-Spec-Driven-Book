# Skills and Subagents for Physical AI & Humanoid Robotics Textbook

This directory contains specialized skills and subagents created to support the development of the "Physical AI & Humanoid Robotics – From Digital Brain to Embodied Intelligence" textbook project.

## Skills

### 1. BetterAuth Integration
- **Purpose**: Handles user authentication, profile management, and personalized features using BetterAuth
- **Key Features**:
  - User signup with background questions (software/hardware experience)
  - Profile management with preferences
  - Integration with Neon Postgres
  - Security best practices implementation

### 2. Docusaurus Customization
- **Purpose**: Customizes Docusaurus for the textbook with specialized UI/UX features
- **Key Features**:
  - Dark-mode compatible design system
  - Interactive robotics visualizers
  - Glossary tooltips for technical terms
  - Embedded quizzes and assessments
  - Accessibility compliance (WCAG 2.1 AA)

### 3. Physical AI Expert
- **Purpose**: Provides specialized knowledge for Physical AI and robotics content
- **Key Features**:
  - Creates content based on peer-reviewed sources
  - Provides mathematical formulations
  - Explains complex robotics concepts
  - Maintains scientific accuracy

### 4. Urdu Translation
- **Purpose**: Translates educational content from English to Urdu with technical accuracy
- **Key Features**:
  - Uses gemini-2.0-flash with Urdu prompt engineering
  - Maintains technical terminology consistency
  - Preserves mathematical formulations
  - Ensures cultural appropriateness

### 5. Content Personalization
- **Purpose**: Adapts content complexity based on user's technical background
- **Key Features**:
  - Adjusts explanations based on user profile
  - Modifies examples for different experience levels
  - Maintains content accuracy at all complexity levels
  - Provides appropriate analogies for user background

### 6. RAG Chatbot Enhancement
- **Purpose**: Improves the RAG chatbot for textbook Q&A with strict grounding
- **Key Features**:
  - Strictly grounded to textbook content only
  - Includes direct citations to source material
  - Handles out-of-scope queries appropriately
  - Optimized for performance (<500ms response time)

## Subagents

### 1. BetterAuth Subagent
- **Purpose**: Handles authentication workflows and personalized content delivery
- **Key Functions**:
  - Complex authentication flows
  - User profile management
  - Personalization engine
  - Localization features

### 2. Physical AI Expert Subagent
- **Purpose**: Creates and verifies advanced robotics content with scientific accuracy
- **Key Functions**:
  - Complex technical content creation
  - Scientific accuracy verification
  - Mathematical formulation generation
  - Educational content adaptation

## Usage Guidelines

- Use the appropriate skill when you need specific functionality (e.g., `betterauth-integration` for auth features)
- Use subagents for complex, multi-step tasks that require specialized knowledge
- All skills and subagents follow the project's constitution and technical standards
- Skills are reusable across different parts of the project
- Subagents can work together and utilize multiple skills when needed

## Integration with Project Goals

These skills and subagents directly support the project's bonus features:
- ✅ Claude Code Subagents: Specialized helper agents
- ✅ Agent Skills: Reusable intelligence modules
- ✅ Subagent + Skill Interaction: Dynamic skill loading
- ✅ Useful Integration: Supports book creation and RAG chatbot
- ✅ Better-Auth with signup questions
- ✅ "Personalize for Me" and "اردو میں ترجمہ کریں" features
- ✅ Content personalization based on user profile
- ✅ Urdu translation using gemini-2.0-flash