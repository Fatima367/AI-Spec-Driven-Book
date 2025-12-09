# AI-Spec-Driven-Book

This project aims to create a comprehensive textbook on Physical AI & Humanoid Robotics using a Spec-Driven Development (SDD) approach. It includes a backend for content generation and management, and a frontend for displaying the book content.

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