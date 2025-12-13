# AI-Spec-Driven-Book

This project aims to create a comprehensive textbook on Physical AI & Humanoid Robotics using a Spec-Driven Development (SDD) approach. It includes a backend for RAG chatbot, and a frontend for displaying the book content.

## Textbook Content Overview

The Physical AI & Humanoid Robotics textbook is organized into several modules covering essential topics:

- **Foundations**: History and evolution of humanoids, biomechanics and actuation systems
- **ROS2**: Robot Operating System 2 fundamentals and node architecture
- **Simulation**: Digital twin concepts, Gazebo and Unity simulation environments
- **NVIDIA Isaac**: AI robot brain, Nav2 path planning, Isaac platform components
- **Humanoids**: Advanced humanoid-specific concepts and applications
- **VLA**: Vision-Language-Action models, Whisper integration, cognitive planning
- **Hardware**: Hardware lab specifications and requirements
- **Capstone**: Autonomous humanoid development project

Each module includes learning objectives, technical content, code examples, diagrams, and practical exercises to reinforce concepts.


## Project Structure

- `backend/`: Contains the backend services, likely for AI model integration and data processing.
- `book_frontend/`: Houses the Docusaurus-based frontend for the textbook.
- `specs/`: Holds the specifications, plans, and tasks for different features of the project following SDD principles.
- `history/`: Stores prompt history records and architectural decision records.
- `.specify/`: Contains templates and scripts for the SDD workflow.

## Getting Started

To set up and run the project locally, follow these steps:

### 1. Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    ./.venv/Scripts/activate  # On Windows
    source ./.venv/bin/activate # On macOS/Linux
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the backend server:**
    ```bash
    uvicorn main:app --reload --port 8000
    ```
    The backend API will be accessible at `http://127.0.0.1:8000`.

### 2. Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd book_frontend
    ```
2.  **Install dependencies:**
    ```bash
    yarn install
    ```
3.  **Start the development server:**
    ```bash
    yarn start
    ```
    This will open the book's frontend in your browser, typically at `http://localhost:3000`.


## Additional Setup Notes

- The frontend uses Docusaurus
- Personalization components allow content adaptation based on user preferences
- Urdu translation support is available through the translation component
- All content follows a consistent structure with hero sections, learning objectives, and practical exercises
- The sidebar navigation has been configured to include all textbook chapters for easy access

## Personalization and Urdu Translation Features

The textbook includes advanced personalization and Urdu translation capabilities that enhance the learning experience for users with diverse backgrounds and language preferences:

### Personalization
- **User Profile Integration**: Content is personalized based on user's software/hardware experience level, technical background, and learning preferences
- **Adaptive Content**: Users can click the "Personalize for Me" button on any chapter page to receive content adapted to their profile
- **Intelligent Adaptation**: The system adjusts complexity, explanations, and focus areas based on user preferences
- **Authentication Required**: Personalization features require user authentication for profile access
- **Session Management**: Proper session handling ensures personalization remains active during user sessions

### Urdu Translation
- **Bilingual Access**: Users can access Urdu translations via the "اردو میں ترجمہ کریں" button on chapter pages
- **File Management**: Urdu content files are stored as separate MDX files with 'urdu-' prefix (e.g., `urdu-chapter1.1.mdx`)
- **Navigation Control**: Urdu files are excluded from the main navigation sidebar to maintain clean organization
- **Synchronized Updates**: Content synchronization ensures Urdu translations stay updated with English content changes
- **Cultural Appropriateness**: Translations maintain technical accuracy while being culturally appropriate for Urdu-speaking audiences

### Technical Implementation
- **Backend API**: Personalization endpoints at `/api/v1/personalize/{chapter_id}` handle content adaptation
- **Authentication Middleware**: JWT-based authentication ensures secure access to personalization features
- **Content Synchronization**: Automated tools keep Urdu translations synchronized with source content
- **Error Handling**: Comprehensive error handling for session expiration and authentication failures
- **Performance Optimization**: Caching and efficient algorithms ensure fast response times for personalized content
