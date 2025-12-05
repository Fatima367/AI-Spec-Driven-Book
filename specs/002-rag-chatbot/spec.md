# Feature Specification: RAG & Backend Architecture

**Feature Branch**: `001-rag-chatbot`
**Created**: 2025-12-02
**Status**: Draft
**Input**: User description: "RAG & Backend Architecture

Build a RAG chatbot embedded in every page of the Docusaurus book. that answers user queries using only the book content.

Tech stack:
- Backend: FastAPI + Python
- Vector DB: Qdrant Cloud (free tier)
- Embeddings: text-embedding-3-large
- LLM: gemini-2.5-flash
- SDK: OpenAI ChatKit + Open AI Agents SDK (with Gemini API Key)
- Frontend: React component using ChatKit UI


Features:
1. Global chatbot (bottom-right corner)
2. Context = entire book + selected text (user highlights text → "Ask about selection")
3. Shows sources with links to exact section
4. Works for logged-in and anonymous users

Requirements:
   - Ingest all docs/ markdown into chunked docs (<= 1200 tokens per chunk).
   - Store vectors in Qdrant Cloud (free cluster).
   - Provide REST endpoints: /ingest, /query, /chat.
   - Support "selected text" retrieval: the client can pass a selection; retrieval should constrain to that chunk.
   - Responses must include inline citations with doc id + chunk id.

## Fast API Service
Create a `backend/` folder containing a FastAPI app.

## Vector Database (Qdrant)
* **Collection:** `textbook_knowledge`
* **Payload:** `page_content`, `chapter_title`, `url_slug`.

## Endpoints
1.  `POST /ingest`: Scrapes the Docusaurus `docs/` folder, chunks text, generates embeddings (OpenAI `text-embedding-3-small`), and uploads to Qdrant.
2.  `POST /chat`:
    * Input: `query`, `user_id`, `selected_text` (optional).
    * Logic: Retrieve context from Qdrant + specific `selected_text`."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Global Chatbot Access (Priority: P1)

Users can find and interact with a chatbot consistently on every page of the Docusaurus book.

**Why this priority**: Essential for chatbot discoverability and core functionality.

**Independent Test**: Can be fully tested by navigating through various book pages and verifying the chatbot's presence and initial interaction availability.

**Acceptance Scenarios**:

1. **Given** a user is browsing any page of the Docusaurus book, **When** the page loads, **Then** a global chatbot interface is visible, typically in the bottom-right corner.
2. **Given** the chatbot interface is visible, **When** the user clicks on it, **Then** the chatbot expands, ready for input.

---

### User Story 2 - Contextual Q&A (Entire Book + Selected Text) (Priority: P1)

Users can ask questions to the chatbot, which provides answers based on the entire book content or specifically on text they have highlighted.

**Why this priority**: Core RAG functionality and enhanced user experience through contextual querying.

**Independent Test**: Can be fully tested by asking general questions about the book and then asking specific questions based on highlighted text, verifying the relevance of answers.

**Acceptance Scenarios**:

1. **Given** the chatbot is open, **When** the user types a query about the book's content, **Then** the chatbot provides an answer based on the entire indexed book content.
2. **Given** a user has highlighted text on a book page, **When** they activate an "Ask about selection" feature (e.g., via a right-click context menu or a dedicated button), **Then** the chatbot opens with the selected text pre-loaded as context for their query.
3. **Given** the chatbot is using selected text as context, **When** the user asks a question, **Then** the chatbot's answer is primarily informed by the selected text, falling back to the wider book context if necessary.

---

### User Story 3 - Source Citation (Priority: P2)

The chatbot provides verifiable sources (links to exact sections) for every answer, ensuring transparency and accuracy.

**Why this priority**: Critical for academic rigor and user trust as per constitution.

**Independent Test**: Can be fully tested by asking questions and verifying that each answer includes correctly formatted, clickable citations linking to specific book sections.

**Acceptance Scenarios**:

1. **Given** the chatbot provides an answer to a query, **When** the answer is displayed, **Then** it includes inline citations (e.g., "[1]", "[2]") linked to specific sections of the book.
2. **Given** a citation is provided, **When** the user clicks on it, **Then** they are navigated to the exact corresponding section within the Docusaurus book.

---

### User Story 4 - Anonymous and Authenticated Access (Priority: P3)

The RAG chatbot functions correctly for both users who are logged in and those browsing anonymously.

**Why this priority**: Ensures broad accessibility, though some personalized features might require authentication.

**Independent Test**: Can be fully tested by interacting with the chatbot as an unauthenticated user and then as an authenticated user, verifying consistent behavior.

**Acceptance Scenarios**:

1. **Given** an anonymous user interacts with the chatbot, **When** they ask a question, **Then** the chatbot provides an accurate answer with citations.
2. **Given** a logged-in user interacts with the chatbot, **When** they ask a question, **Then** the chatbot provides an accurate answer with citations, with no degradation in functionality compared to an anonymous user.

---

### Edge Cases

- What happens when a user's query cannot be answered based on the indexed book content? The chatbot MUST return a polite refusal message (e.g., "I can only answer questions based on the content of the textbook.") as per Constitution.
- How does the system handle selected text that is too short (e.g., a single word) or too long to be processed efficiently? It should default to full book context or intelligently truncate/summarize.
- What happens if the `docs/` folder contains empty, malformed, or unusually large Markdown files during ingestion? The ingestion process should handle errors gracefully, log issues, and skip problematic files without crashing.
- What if the Qdrant Cloud free tier limits are exceeded? The system should provide appropriate feedback and potentially queue ingestion or alert administrators.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a global RAG chatbot embedded in every page of the Docusaurus book.
- **FR-002**: Chatbot MUST answer user queries using only the indexed content of the textbook documents.
- **FR-003**: Chatbot MUST support retrieving context from the entire book content.
- **FR-004**: Chatbot MUST support retrieving context from user-selected text (client passes selection).
- **FR-005**: Chatbot responses MUST include inline citations (doc id + chunk id) with links to exact sections.
- **FR-006**: Chatbot MUST function correctly for logged-in users.
- **FR-007**: Chatbot MUST function correctly for anonymous users.
- **FR-008**: Backend MUST be a FastAPI application created in a `backend/` folder.
- **FR-009**: Backend MUST provide a `POST /ingest` endpoint that scrapes the Docusaurus `docs/` folder, chunks text (<= 1200 tokens), generates embeddings (OpenAI `text-embedding-3-large`), and uploads to Qdrant.
- **FR-010**: Backend MUST store vectors in a Qdrant Cloud collection named `textbook_knowledge` with `page_content`, `chapter_title`, and `url_slug` as payload fields.
- **FR-011**: Backend MUST provide a `POST /query` endpoint for direct retrieval.
- **FR-012**: Backend MUST provide a `POST /chat` endpoint that accepts `query`, `user_id` (optional), and `selected_text` (optional).
- **FR-013**: The `POST /chat` endpoint's logic MUST retrieve context from Qdrant, prioritizing specific `selected_text` if provided.
- **FR-014**: Embeddings for `POST /ingest` MUST use `Gemini embeddings`.
- **FR-015**: LLM for chat responses MUST be `gemini-2.5-flash`.

### Key Entities

-   **Document Chunk**: A segment of the textbook content, typically Markdown, tokenized and embedded.
    *   Attributes: `page_content` (text), `chapter_title` (metadata), `url_slug` (link), `embedding` (vector).
-   **User Query**: The natural language question submitted by the user to the chatbot.
-   **Selected Text**: A specific portion of the book's text highlighted by the user to narrow the query context.

## Constitution Compliance *(mandatory)*

*GATE: All aspects of the feature specification must align with the project's Constitution.*

- [x] Principle I: Full Course Content (Supports book content)
- [x] Principle II: Tech Stack Adherence (FastAPI, Qdrant, Docusaurus, Gemini API)
- [ ] Principle III: GitHub Pages Publication (Indirectly, as the chatbot will be on published pages)
- [ ] Principle IV: Free GitHub Pages Deployment (Indirectly)
- [x] Principle V: Full RAG Chatbot Implementation (Directly implementing)
- [x] Principle VI: Extensive Subagent Usage (Future consideration for RAG logic, will ensure)
- [x] Principle VII: Production-Ready Code (Implicit in all code)
- [x] Principle VIII: Accuracy through Primary Source Verification (RAG grounding)
- [x] Principle IX: Clarity for Audience (Chatbot purpose)
- [x] Principle X: Reproducibility (Citations from RAG)
- [x] Principle XI: Rigor (Peer-reviewed sources for RAG content)

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: 95% of user queries are answered accurately and solely from the indexed book content, as verified by human review.
-   **SC-002**: Chatbot responses for typical queries (average length, no selected text) are generated and displayed to the user within 3 seconds for 90% of requests.
-   **SC-003**: 100% of chatbot answers include at least one verifiable inline citation (doc id + chunk id) that links to the exact source section within the Docusaurus book.
-   **SC-004**: Users can successfully utilize the "Ask about selection" feature for 98% of valid text selections, leading to contextually relevant answers.
-   **SC-005**: The `POST /ingest` endpoint successfully processes and indexes all valid Markdown files within the `docs/` folder, with less than 0.1% failure rate for chunking or embedding generation.
-   **SC-006**: The chatbot politely refuses to answer queries that cannot be grounded in the book's content for 100% of such cases, without generating ungrounded responses.
