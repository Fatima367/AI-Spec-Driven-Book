---
id: 0001
title: Create Spec for RAG Backend Architecture
stage: spec
date: 2025-12-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-rag-chatbot
branch: 001-rag-chatbot
user: user
command: /sp.specify RAG & Backend Architecture\n\nBuild a RAG chatbot embedded in every page of the Docusaurus book. that answers user queries using only the book content.\n\nTech stack:\n- Backend: FastAPI + Python\n- Vector DB: Qdrant Cloud (free tier)\n- Embeddings: text-embedding-3-large\n- LLM: gemini-2.5-flash\n- SDK: OpenAI ChatKit + Open AI Agents SDK (with Gemini API Key)\n- Frontend: React component using ChatKit UI\n\n\nFeatures:\n1. Global chatbot (bottom-right corner)\n2. Context = entire book + selected text (user highlights text → "Ask about selection")\n3. Shows sources with links to exact section\n4. Works for logged-in and anonymous users\n\nRequirements:\n   - Ingest all docs/ markdown into chunked docs (<= 1200 tokens per chunk).\n   - Store vectors in Qdrant Cloud (free cluster).\n   - Provide REST endpoints: /ingest, /query, /chat.\n   - Support "selected text" retrieval: the client can pass a selection; retrieval should constrain to that chunk.\n   - Responses must include inline citations with doc id + chunk id.\n\n## Fast API Service\nCreate a `backend/` folder containing a FastAPI app.\n\n## Vector Database (Qdrant)\n* **Collection:** `textbook_knowledge`\n* **Payload:** `page_content`, `chapter_title`, `url_slug`.\n\n## Endpoints\n1.  `POST /ingest`: Scrapes the Docusaurus `docs/` folder, chunks text, generates embeddings (OpenAI `text-embedding-3-small`), and uploads to Qdrant.\n2.  `POST /chat`:\n    * Input: `query`, `user_id`, `selected_text` (optional).\n    * Logic: Retrieve context from Qdrant + specific `selected_text`.\n    * System Prompt: "You are a TA for a Robotics course..."
labels: ["spec", "rag-chatbot", "backend-architecture"]
links:
  spec: /specs/001-rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-rag-chatbot/spec.md
  - specs/001-rag-chatbot/checklists/requirements.md
tests:
  - N/A
---

## Prompt

RAG & Backend Architecture

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
    * Logic: Retrieve context from Qdrant + specific `selected_text`.
    * System Prompt: "You are a TA for a Robotics course..."


## Response snapshot

The specification for the "RAG & Backend Architecture" feature has been created and validated. The `spec.md` file has been updated to reflect this. The quality checklist `requirements.md` has also been updated, with all items marked as complete.

## Outcome

- ✅ Impact: Feature specification created successfully.
- 🧪 Tests: No tests run during spec creation.
- 📁 Files: Created spec.md and requirements.md checklist.
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: Successfully generated feature specification and checklist.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
