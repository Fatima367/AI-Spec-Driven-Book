# AI-Spec-Driven-Book

This project aims to create a comprehensive textbook on Physical AI & Humanoid Robotics using a Spec-Driven Development (SDD) approach. It includes a backend for RAG chatbot, and a frontend for displaying the book content.

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
