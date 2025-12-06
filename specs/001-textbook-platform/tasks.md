# Tasks: Physical AI & Humanoid Robotics Textbook Platform

**Input**: Tasks for Physical AI & Humanoid Robotics Textbook Platform, using TDD, CLI automation, easy rollback, and traceability.
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: All tasks will follow a Test-Driven Development (TDD) approach, with tests being written and expected to fail *before* implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [TaskID] [P?] [Story?] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/`
- **Backend**: `backend/`
- **Tools**: `tools/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, basic structure, and essential tooling setup.

- [x] T001 Create project directories: `frontend/`, `backend/`, `tools/`
- [x] T002 Initialize frontend Docusaurus project in `frontend/`
- [x] T003 Initialize backend FastAPI project in backend/
- [x] T004 [P] Configure Git pre-commit hooks for linting/formatting (traceability & quality)
- [x] T005 [P] Setup Python virtual environment for backend in `backend/`
- [x] T006 [P] Create `backend/requirements.txt` for Python dependencies
- [x] T007 [P] Create `.env.example` in `backend/` for environment variables (API keys, DB connection)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented. Includes CI/CD, secret management, and core database setup.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### CI/CD, Deployment & Secret Management

- [x] T008 [P] Configure GitHub Actions workflow for Frontend Docusaurus build and deploy to GitHub Pages (`.github/workflows/frontend-deploy.yaml`)
- [x] T009 [P] Configure GitHub Actions workflow for Backend FastAPI Docker build and deploy to chosen serverless platform (`.github/workflows/backend-deploy.yaml`)
- [x] T010 [P] Document environment variable setup for deployment (GitHub Secrets, Cloud Platform Secrets)
- [x] T011 [P] Implement base API key management in backend/ (e.g., config loading from `.env` or secrets)

### Database Setup

- [x] T012 Configure Neon Serverless Postgres instance and connection string
- [x] T013 [P] Implement initial database connection and ORM setup in `backend/src/database/`
- [x] T014 Configure Qdrant Cloud instance and API key
- [x] T015 [P] Implement Qdrant client connection in `backend/src/services/`

### Observability & Error Handling

- [x] T016 Setup structured logging for FastAPI backend in `backend/src/main.py`
- [x] T017 Implement global error handling middleware for FastAPI in `backend/src/main.py`
- [x] T018 Define basic monitoring metrics for backend API (latency, error rates) in `backend/src/main.py`

### Core Data Models

- [x] T019 [P] Create Pydantic model for `Student` entity in `backend/src/models/student.py`
- [x] T020 [P] Create Pydantic model for `TextbookContent` (schema for embeddings) in `backend/src/models/content.py`
- [x] T021 Implement database schema for `Student` in Neon Postgres (e.g., using Alembic/SQLAlchemy) - *Manually created migration script. Requires valid NEON_DATABASE_URL to apply migration.*

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Access Textbook Content (P1) 🎯 MVP

**Goal**: Provide a publicly accessible and browsable Docusaurus textbook on GitHub Pages.

**Independent Test**: Successfully navigate to the deployed textbook URL and browse its chapters and sections.

### Tests for User Story 1 (TDD)

- [x] T022 [US1] Integration test: Verify Docusaurus builds successfully (e.g., `frontend/tests/integration/test_build.test.js`)
- [ ] T023 [US1] Integration test: Verify deployed site is accessible and displays content (e.g., `frontend/tests/integration/test_deployment_access.test.js`) - *Currently skipped, requires deployment.*
- [ ] T024 [US1] E2E test: Verify navigation between main pages/chapters (e.g., `frontend/tests/e2e/test_navigation.test.js`) - *Currently skipped, requires deployment and content.*

### Implementation for User Story 1

- [x] T025 [US1] Initialize base Docusaurus configuration in `frontend/docusaurus.config.js`
- [x] T026 [US1] Add initial placeholder content for a few chapters in `frontend/docs/`
- [x] T027 [US1] Configure Docusaurus theme and styling in `frontend/src/theme/`
- [x] T028 [US1] Implement Docusaurus GitHub Pages deployment configuration (`frontend/docusaurus.config.js`)
- [x] T029 [US1] Trigger frontend CI/CD for initial deployment - *Requires user to push changes to trigger GitHub Actions workflow.*

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Interact with RAG Chatbot (P1) 🎯 MVP

**Goal**: Enable students to ask questions about textbook content and receive accurate, context-aware answers from an integrated RAG chatbot.

**Independent Test**: Query the chatbot and verify accuracy/relevance of responses, including snippet-based queries.

### Detailed Task Plan for User Story 2 (RAG Chatbot)

#### Part 1: Data Ingestion Pipeline
*   [ ] T030 [P] [US2] Test: Write test for Markdown file reader in `tools/embedding_generator.py`.
*   [ ] T031 [P] [US2] Implement: Markdown file reader to load content from `frontend/docs/` in `tools/embedding_generator.py`.
*   [ ] T032 [P] [US2] Test: Write test for text chunking logic in `tools/embedding_generator.py`.
*   [ ] T033 [P] [US2] Implement: Text chunking logic (e.g., recursive character splitter) in `tools/embedding_generator.py`.
*   [ ] T034 [P] [US2] Test: Write test for embedding generation (mocking OpenAI API) in `tools/embedding_generator.py`.
*   [ ] T035 [P] [US2] Implement: Embedding generation using OpenAI client in `tools/embedding_generator.py`.
*   [ ] T036 [P] [US2] Test: Write test for batch uploading to Qdrant (mocking Qdrant client) in `tools/embedding_generator.py`.
*   [ ] T037 [P] [US2] Implement: Batch upload of vectors and metadata to Qdrant in `tools/embedding_generator.py`.
*   [ ] T038 [US2] Execute: Run the completed `tools/embedding_generator.py` script to populate the Qdrant collection.

#### Part 2: Backend Implementation (FastAPI)
*   [ ] T039 [P] [US2] Test: Create Pydantic models for chat request/response and write validation tests in `backend/tests/api/test_chat_api.py`.
*   [ ] T040 [P] [US2] Implement: Pydantic models for the chat API in `backend/src/models/chat.py`.
*   [ ] T041 [P] [US2] Test: Write failing unit test for Qdrant search functionality in `backend/tests/services/test_qdrant_service.py`.
*   [ ] T042 [P] [US2] Implement: Qdrant search service to retrieve document chunks in `backend/src/services/qdrant_service.py`.
*   [ ] T043 [P] [US2] Test: Write failing unit test for prompt construction in `backend/tests/services/test_rag_service.py`.
*   [ ] T044 [P] [US2] Implement: Prompt construction logic in `backend/src/services/rag_service.py` that incorporates retrieved context and user query.
*   [ ] T045 [P] [US2] Test: Write failing unit test for calling the OpenAI API with the constructed prompt (mocking the API call) in `backend/tests/services/test_rag_service.py`.
*   [ ] T046 [P] [US2] Implement: Core RAG logic in `backend/src/services/rag_service.py` to call the language model and get a response.
*   [ ] T047 [US2] Test: Write failing integration test for the `/chat` endpoint in `backend/tests/api/test_chat_api.py`.
*   [ ] T048 [US2] Implement: The `/chat` streaming endpoint in `backend/src/api/chat.py`, orchestrating calls to the RAG service.

#### Part 3: Frontend Implementation (React)
*   [ ] T049 [P] [US2] Test: Create basic Jest snapshot test for the Chatbot UI component in `frontend/src/components/Chatbot/index.test.tsx`.
*   [ ] T050 [P] [US2] Implement: Basic UI structure for the chatbot window (message list, input box, send button) in `frontend/src/components/Chatbot/index.tsx`.
*   [ ] T051 [P] [US2] Test: Write tests for chat state management (adding messages, handling input) using React Testing Library.
*   [ ] T052 [P] [US2] Implement: State management for the chat component using React hooks in `frontend/src/components/Chatbot/index.tsx`.
*   [ ] T053 [P] [US2] Test: Write test for the API client service (mocking `fetch`) to call the backend in `frontend/src/services/api.test.ts`.
*   [ ] T054 [P] [US2] Implement: API client function in `frontend/src/services/api.ts` to send queries to the `/chat` endpoint.
*   [ ] T055 [US2] Implement: Logic in the Chatbot component to call the API service and display the streaming response.
*   [ ] T056 [US2] Integrate: Add the Chatbot component to the main Docusaurus layout in `frontend/src/theme/Layout/index.js` so it appears on all pages.
*   [ ] T057 [US2] E2E Test: Write a Playwright/Cypress test to simulate a user typing a question and receiving an answer in `frontend/tests/e2e/test_chatbot_interaction.test.js`.

**Checkpoint**: User Story 2 should be fully functional and testable independently

---

## Phase 5: User Story 3 - Personalized Content (P2 - Bonus)

**Goal**: Allow logged-in students to personalize chapter content based on their background.

**Independent Test**: Verify content adaptation after setting preferences, requires login.

### Tests for User Story 3 (TDD)

- [ ] T045 [P] [US3] Unit test: `better-auth.com` integration (mocking external service) (`backend/tests/services/test_auth_service.py`)
- [ ] T046 [P] [US3] Unit test: User profile update logic (`backend/tests/services/test_user_service.py`)
- [ ] T047 [P] [US3] Unit test: Content personalization logic (`backend/tests/services/test_personalization_service.py`)
- [ ] T048 [US3] Integration test: Full user signup/signin flow (`backend/tests/integration/test_auth_flow.py`)
- [ ] T049 [US3] E2E test: User can sign up, log in, update profile, and see personalized content (`frontend/tests/e2e/test_personalization.test.js`)

### Implementation for User Story 3

- [ ] T050 [P] [US3] Implement FastAPI endpoints for `/auth/signup` and `/auth/signin` in `backend/src/api/auth.py`
- [ ] T051 [P] [US3] Integrate `better-auth.com` for user management in `backend/src/services/auth_service.py`
- [ ] T052 [P] [US3] Implement user profile update endpoint `/user/{user_id}/profile` in `backend/src/api/user.py`
- [ ] T053 [US3] Develop content personalization logic in `backend/src/services/personalization_service.py`
- [ ] T054 [US3] Create Docusaurus UI components for Signup, Signin, and Profile management (`frontend/src/components/Auth/`)
- [ ] T055 [US3] Implement logic to dynamically adapt chapter content based on user preferences in `frontend/src/theme/Layout/index.js` or specific content components.

**Checkpoint**: User Story 3 should be fully functional and testable independently

---

## Phase 6: User Story 4 - Localized Content (P2 - Bonus)

**Goal**: Enable logged-in students to translate chapter content into Urdu.

**Independent Test**: Verify content translation after selecting Urdu language.

### Tests for User Story 4 (TDD)

- [ ] T056 [P] [US4] Unit test: Localization service logic (`backend/tests/services/test_localization_service.py`)
- [ ] T057 [P] [US4] Integration test: Localization API endpoint (`backend/tests/integration/test_localization_api.py`)
- [ ] T058 [US4] E2E test: User can select Urdu and content is translated correctly (`frontend/tests/e2e/test_localization.test.js`)

### Implementation for User Story 4

- [ ] T059 [P] [US4] Implement FastAPI endpoint for content translation `/translate/{chapter_id}` in `backend/src/api/localization.py`
- [ ] T060 [P] [US4] Develop localization service in `backend/src/services/localization_service.py` (e.g., using an LLM for translation)
- [ ] T061 [US4] Create Docusaurus UI component for language selection (`frontend/src/components/Localization/`)
- [ ] T062 [US4] Implement logic to display translated content in Docusaurus.

**Checkpoint**: User Story 4 should be fully functional and testable independently

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories, overall quality, and operational readiness.

### Documentation & Traceability

- [ ] T063 [P] Review and update project `README.md` with setup, run, and deployment instructions.
- [ ] T064 [P] Generate/update OpenAPI specification documentation in `docs/api/` (CLI automation).
- [ ] T065 [P] Document API key management procedures and secure storage guidelines.
- [ ] T066 [P] Update `quickstart.md` with any refined steps.

### Security Hardening

- [ ] T067 Conduct a basic security review of API endpoints and data handling.
- [ ] T068 Implement helmet-like security headers for FastAPI response.
- [ ] T069 Configure CORS policies for FastAPI backend.

### Observability & Monitoring

- [ ] T070 Setup basic dashboard for API performance and error rates in chosen cloud monitoring tool.
- [ ] T071 Configure alerts for critical errors or performance degradation.
- [ ] T072 Implement tracing for key API calls (e.g., using OpenTelemetry if time permits).

### Performance Optimization

- [ ] T073 Review critical API endpoints for performance bottlenecks.
- [ ] T074 Implement caching for frequently accessed data (e.g., textbook content, RAG results).

### AI Content Generation Workflow Automation

- [ ] T075 Develop CLI tool/script to automate content generation using Spec-Kit Plus and Claude Code (`tools/content_automator.py`).
- [ ] T076 Integrate automated content generation into CI pipeline (if applicable).

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Foundational phase completion.
  - User stories can then proceed in parallel (if staffed) or sequentially in priority order (P1 → P2 → P3).
- **Polish (Final Phase)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories.
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories.
- **User Story 3 (P2)**: Depends on User Story 1 (for content) and Foundational (Phase 2) - Can integrate with US1 but should be independently testable.
- **User Story 4 (P2)**: Depends on User Story 1 (for content) and Foundational (Phase 2) - Can integrate with US1 but should be independently testable.

### Within Each User Story

- Tests MUST be written and FAIL before implementation.
- Models before services.
- Services before endpoints.
- Core implementation before integration.
- Story complete before moving to next priority.

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel.
- All Foundational tasks marked [P] can run in parallel (within Phase 2).
- Once Foundational phase completes, User Stories 1 and 2 can be developed in parallel.
- User Stories 3 and 4 can also be developed in parallel, but will likely depend on the core content from US1 and user management from Foundational phase.
- Within each user story, tasks marked [P] can run in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 & 2)

1.  Complete Phase 1: Setup.
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories).
3.  Complete Phase 3: User Story 1 (Deploy basic Docusaurus site).
4.  Complete Phase 4: User Story 2 (Implement core RAG Chatbot functionality and integration).
5.  **STOP and VALIDATE**: Test User Stories 1 & 2 independently.
6.  Deploy/demo if ready (Core MVP).

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready.
2.  Add User Story 1 → Test independently → Deploy/Demo (Basic Textbook MVP).
3.  Add User Story 2 → Test independently → Deploy/Demo (Interactive Textbook MVP).
4.  Add User Story 3 → Test independently → Deploy/Demo (Personalized Textbook).
5.  Add User Story 4 → Test independently → Deploy/Demo (Localized Textbook).
6.  Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together.
2.  Once Foundational is done:
    *   Developer A: User Story 1 (Frontend Docusaurus, deployment).
    *   Developer B: User Story 2 (Backend FastAPI, RAG logic).
    *   Developer C: User Story 3 (Authentication, personalization).
    *   Developer D: User Story 4 (Localization).
3.  Stories complete and integrate independently.

---

## Notes

-   [P] tasks = different files, no dependencies.
-   [Story] label maps task to specific user story for traceability.
-   Each user story should be independently completable and testable.
-   Verify tests fail before implementing.
-   Commit after each task or logical group (easy rollback and traceability).
-   CLI automation will be preferred for development tasks (e.g., content embedding, deployment).
-   Context7 MCP server will be used for documentation lookups during development to ensure accuracy and best practices.