# Quickstart Guide: RAG & Backend Architecture

This guide provides instructions to quickly set up and run the RAG chatbot backend and frontend.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.10+** (for the FastAPI backend)
*   **Node.js LTS** (for the Docusaurus frontend)
*   **Poetry** (Python package manager, `pip install poetry`)
*   **API Keys**:
    *   **Qdrant Cloud API Key**: For your vector database (free tier account at [qdrant.tech](https://qdrant.tech)).
    *   **Gemini API Key**: For embeddings and LLM (from [Google AI Studio](https://ai.google.dev/)).

## 1. Backend Setup (FastAPI)

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```
2.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```
3.  **Install dependencies using Poetry**:
    ```bash
    poetry install
    ```
4.  **Configure Environment Variables**: Create a `.env` file in the `backend/` directory with the following:
    ```dotenv
    QDRANT_API_KEY="your_qdrant_api_key"
    QDRANT_CLUSTER_URL="your_qdrant_cluster_url" # e.g., https://[cluster_id].qdrant.tech
    GEMINI_API_KEY="your_gemini_api_key"
    ```
    Replace the placeholder values with your actual API keys and Qdrant cluster URL.
5.  **Run the FastAPI application**:
    ```bash
    poetry run uvicorn src.main:app --reload
    ```
    The backend API will be accessible at `http://127.0.0.1:8000`.

## 2. Frontend Setup (Docusaurus/React)

1.  **Navigate to the frontend directory**:
    ```bash
    cd ../frontend # Assuming you are in the backend directory
    ```
2.  **Install Node.js dependencies**:
    ```bash
    npm install
    # or yarn install
    ```
3.  **Run the Docusaurus development server**:
    ```bash
    npm start
    # or yarn start
    ```
    The Docusaurus book with the embedded chatbot will be accessible at `http://localhost:3000`.

## 3. Ingestion Process

Once the backend is running, you can trigger the ingestion of the Docusaurus `docs/` content into Qdrant.

*   **Via cURL (example)**:
    ```bash
    curl -X POST http://127.0.0.1:8000/ingest
    ```
    This will scrape the `docs/` folder, chunk the content, generate embeddings, and upload them to your Qdrant Cloud instance.

## 4. Interaction with the Chatbot

### Via Frontend UI

Navigate to `http://localhost:3000` in your browser. The global chatbot interface should be visible (typically in the bottom-right corner). Click on it to expand and start asking questions related to the book content.

### Via API (example using cURL)

*   **Chat with general query**:
    ```bash
    curl -X POST http://127.0.0.1:8000/chat \
    -H "Content-Type: application/json" \
    -d '{"query": "What is the main topic of Chapter 3?", "user_id": "test_user"}'
    ```
*   **Chat with selected text context**:
    ```bash
    curl -X POST http://127.0.0.1:8000/chat \
    -H "Content-Type: application/json" \
    -d '{"query": "What does this mean for scalability?", "selected_text": "Retrieval-augmented generation (RAG) models combine ... to improve relevance.", "user_id": "test_user"}'
    ```
