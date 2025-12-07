---

description: "Task list template for feature implementation"
---

## Constitution Compliance *(mandatory)*

*GATE: All tasks must align with the project's Constitution.*

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

---

# Tasks: 001-rag-chatbot

**Input**: Design documents from `/specs/001-rag-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create `backend/` directory and use `book_frontend/` for frontend.
- [x] T002 Initialize Python backend with uv in `backend/`.
- [x] T003 Initialize Node.js frontend (Docusaurus/React) in `book_frontend/`.
- [x] T004 Create `.env` file structure in `backend/` for API keys.
- [x] T005 Add FastAPI, Qdrant, OpenAI SDK dependencies to `backend/requirements.txt`.
- [x] T006 Add Docusaurus, React, OpenAI ChatKit dependencies to `book_frontend/package.json`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Implement FastAPI application structure in `backend/src/main.py`.
- [x] T008 Define Pydantic models for Document Chunk, User Query, Selected Text in `backend/src/models/`.
- [x] T009 Implement Qdrant client initialization and connection in `backend/src/services/qdrant_service.py`.
- [x] T010 Implement embedding generation service using Gemini embeddings in `backend/src/services/embedding_service.py`.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Global Chatbot Access (Priority: P1) 🎯 MVP

**Goal**: Users can find and interact with a chatbot consistently on every page of the Docusaurus book.

**Independent Test**: Can be fully tested by navigating through various book pages and verifying the chatbot's presence and initial interaction availability.

### Implementation for User Story 1

- [x] T011 [US1] Create React Chatbot component in `frontend/src/components/Chatbot/Chatbot.tsx`.
- [x] T012 [P] [US1] Integrate Chatbot component into Docusaurus layout (e.g., `book_frontend/src/theme/Layout/index.tsx`).
- [x] T013 [US1] Implement basic Chatbot UI to expand/collapse.
- [x] T014 [US1] Ensure chatbot is visible in bottom-right corner on all pages.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Contextual Q&A (Entire Book + Selected Text) (Priority: P1)

**Goal**: Users can ask questions to the chatbot, which provides answers based on the entire book content or specifically on text they have highlighted.

**Independent Test**: Can be fully tested by asking general questions about the book and then asking specific questions based on highlighted text, verifying the relevance of answers.

### Implementation for User Story 2

- [x] T015 [US2] Implement `POST /ingest` endpoint in `backend/src/api/ingest.py`.
- [x] T016 [US2] Implement `POST /query` endpoint for direct retrieval in `backend/src/api/query.py`.
- [x] T017 [US2] Implement `POST /chat` endpoint in `backend/src/api/chat.py`.
- [x] T018 [US2] Frontend: Implement "Ask about selection" feature (e.g., context menu or button) in `book_frontend/src/services/selection_service.ts`.
- [x] T019 [US2] Frontend: Integrate `/chat` endpoint with Chatbot component for user queries in `book_frontend/src/components/Chatbot/Chatbot.tsx`.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Source Citation (Priority: P2)

**Goal**: The chatbot provides verifiable sources (links to exact sections) for every answer, ensuring transparency and accuracy.

**Independent Test**: Can be fully tested by asking questions and verifying that each answer includes correctly formatted, clickable citations linking to specific book sections.

### Implementation for User Story 3

- [x] T020 [US3] Modify `POST /chat` endpoint to include inline citations (doc id + chunk id) in responses.
- [x] T021 [US3] Frontend: Render inline citations as clickable links in Chatbot UI.

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Anonymous and Authenticated Access (Priority: P3)

**Goal**: The RAG chatbot functions correctly for both users who are logged in and those browsing anonymously.

**Independent Test**: Can be fully tested by interacting with the chatbot as an unauthenticated user and then as an authenticated user, verifying consistent behavior.

### Implementation for User Story 4

- [x] T022 [US4] Ensure `POST /chat` and other backend endpoints handle optional `user_id` gracefully.
- [x] T023 [US4] Frontend: Ensure Chatbot UI functions correctly without requiring authentication.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T024 Implement error handling for `POST /ingest` (empty/maldformed/large Markdown files).
- [x] T025 Implement polite refusal message for unanswerable queries.
- [x] T026 Add comprehensive unit/integration tests for backend services and API.
- [x] T027 Add unit/integration tests for book_frontend components and services.
- [x] T028 Document API endpoints using OpenAPI/Swagger.
- [x] T029 Update Quickstart Guide with final setup and usage instructions.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for [endpoint] in tests/contract/test_[name].py"
Task: "Integration test for [user journey] in tests/integration/test_[name].py"

# Launch all models for User Story 1 together:
Task: "Create React Chatbot component in book_frontend/src/components/Chatbot/Chatbot.tsx"
Task: "Integrate Chatbot component into Docusaurus layout (e.g., book_frontend/src/theme/Layout/index.tsx)"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
