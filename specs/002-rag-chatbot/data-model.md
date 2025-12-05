# Data Model: RAG & Backend Architecture

## Entities

### 1. Document Chunk
*   **Description**: A segment of the textbook content, typically Markdown, tokenized and embedded.
*   **Attributes**:
    *   `page_content`: string (textual content of the chunk)
    *   `chapter_title`: string (title of the chapter the chunk belongs to)
    *   `url_slug`: string (URL slug for the exact section within the Docusaurus book)
    *   `embedding`: vector (numerical representation of the `page_content` for vector similarity search)
*   **Validation Rules**:
    *   `page_content` length MUST be `<= 1200 tokens`.

### 2. User Query
*   **Description**: The natural language question submitted by the user to the chatbot.
*   **Attributes**:
    *   `query`: string (the user's question)
    *   `user_id`: string (optional, identifier for the user)
*   **Relationships**:
    *   Used to retrieve relevant `Document Chunk`s from the Qdrant vector database.

### 3. Selected Text
*   **Description**: A specific portion of the book's text highlighted by the user to narrow the query context.
*   **Attributes**:
    *   `selected_text`: string (the text highlighted by the user)
*   **Relationships**:
    *   Prioritized as context for the `User Query` when provided, constraining retrieval to relevant `Document Chunk`s.
