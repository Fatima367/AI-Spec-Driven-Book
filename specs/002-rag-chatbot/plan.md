# Implementation Plan: RAG & Backend Architecture

**Branch**: `001-rag-chatbot` | **Date**: 2025-12-02 | **Spec**: /specs/001-rag-chatbot/spec.md
**Input**: Feature specification from `/specs/001-rag-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a RAG chatbot embedded in every page of the Docusaurus book that answers user queries using only the book content. The technical approach involves a FastAPI + Python backend, Qdrant Cloud for vector database, `text-embedding-3-large` for embeddings, `gemini-2.5-flash` for the LLM, OpenAI ChatKit + OpenAI Agents SDK for the SDK, and a React component for the frontend UI.

## Technical Context

**Language/Version**: Python 3.10+, TypeScript, React
**Primary Dependencies**: FastAPI, Qdrant, OpenAI ChatKit SDK, OpenAI Agents SDK, Docusaurus, Tailwind CSS, Pydantic, Neon Postgres
**Storage**: Qdrant Cloud (Vector DB), Neon (Serverless Postgres)
**Testing**: pytest (backend), Jest/React Testing Library (frontend - NEEDS CLARIFICATION)
**Target Platform**: Linux server (backend), Web browser (frontend)
**Project Type**: Web application
**Performance Goals**: Backend API <500ms (95% of requests), Frontend TTI <3s (mobile)
**Constraints**: Qdrant Cloud Free Tier, Neon Serverless free tier, strictly book content for RAG, no web search.
**Scale/Scope**: Entire book content for RAG, global chatbot on every page.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Principle I: Full Course Content
- [x] Principle II: Tech Stack Adherence
- [x] Principle III: GitHub Pages Publication
- [x] Principle IV: Free GitHub Pages Deployment
- [x] Principle V: Full RAG Chatbot Implementation
- [x] Principle VI: Extensive Subagent Usage
- [x] Principle VII: Production-Ready Code
- [x] Principle VIII: Accuracy through Primary Source Verification
- [x] Principle IX: Clarity for Audience
- [x] Principle X: Reproducibility
- [x] Principle XI: Rigor

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/
```

**Structure Decision**: Web application structure with distinct `backend/` (FastAPI) and `frontend/` (Docusaurus/React) directories. This aligns with the specified tech stack and separation of concerns for a RAG chatbot integration into a Docusaurus book.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
