# Implementation Plan: Textbook Content Structure

**Branch**: `001-textbook-content` | **Date**: 2025-12-04 | **Spec**: /specs/001-textbook-content/spec.md
**Input**: Feature specification from `/specs/001-textbook-content/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the generation of a comprehensive Docusaurus-based textbook structure and content for "Physical AI & Humanoid Robotics". It covers the creation of sidebar navigation, folder organization, and detailed chapter content, including hero sections, learning objectives, code blocks, diagrams, quizzes, and simulation exercises, with a dedicated hardware lab chapter.

## Technical Context

**Language/Version**: Python 3.10+ (for content generation scripts, potentially backend for RAG), TypeScript/React (for Docusaurus frontend), ROS 2, URDF.
**Primary Dependencies**: Docusaurus, FastAPI, Pydantic, Neon Postgres, Qdrant, OpenAI ChatKit SDK (with Gemini API key), BetterAuth, Mermaid.js.
**Storage**: Neon Serverless Postgres (User Data), Qdrant Cloud (RAG Vector DB).
**Testing**: Unit tests for content generation scripts (e.g., Python `pytest`), Docusaurus build validation, manual content review for accuracy and formatting.
**Target Platform**: GitHub Pages (Docusaurus build).
**Project Type**: Web application (Docusaurus frontend for the book, FastAPI backend for RAG chatbot).
**Performance Goals**: Backend API responses <500ms for 95% of requests. Frontend Time to Interactive (TTI) <3 seconds on mobile devices.
**Constraints**: Utilize free-tier services (Qdrant Cloud Free, Neon Serverless). Minimum 5-8 highly-regarded sources, with at least 50% peer-reviewed. Simple and replicable GitHub Pages deployment. No verbose and repetition in chapters.
**Scale/Scope**: Generate complete textbook structure and content for 7 modules/chapters as specified in the syllabus, including sidebar categories: Foundations, ROS2, Simulation, NVIDIA Isaac, Humanoids, VLA, Hardware, Capstone.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Comprehensive Course Content
- **Compliance**: ✅ Fully compliant. The feature directly implements this principle by generating the course content based on the syllabus.

### II. GitHub Pages Publication & Deployment
- **Compliance**: ✅ Fully compliant. The generated content is designed for Docusaurus and GitHub Pages deployment, adhering to free-tier services.

### III. Robust RAG Chatbot Implementation
- **Compliance**: 🚫 Not applicable for this feature. This feature focuses on content generation, not chatbot implementation.

### IV. Extensive Claude Code Subagent Utilization
- **Compliance**: ✅ Fully compliant. Subagents will be used for content generation and formatting, leveraging specialized capabilities (e.g., content-expander, introduction-writer, outline-generator).

### V. Production-Ready Code Quality
- **Compliance**: ✅ Fully compliant. Generated content (e.g., code blocks) and any generation scripts will adhere to high code quality standards.

### VI. Accuracy Through Primary Source Verification
- **Compliance**: ✅ Fully compliant. Content generation will emphasize accuracy and verifiability through primary sources as per the constitution.

### VII. Clarity for Audience
- **Compliance**: ✅ Fully compliant. Generated content will be clear and understandable for the target audience.

### VIII. Reproducibility
- **Compliance**: ✅ Fully compliant. Content generation will ensure claims and experimental results are cited and traceable.

### IX. Rigor
- **Compliance**: ✅ Fully compliant. Peer-reviewed sources will be preferred for content generation.

### Bonus Features (Relevant to content generation)
- **Claude Code Subagents**: ✅ Fully compliant. Will leverage subagents for content generation.
- **Agent Skills**: ✅ Fully compliant. Will utilize existing or create new skills (e.g., outline-generator, content-expander, introduction-writer) for content creation.
- **Logged-in users get two buttons per chapter**: ✅ Fully compliant. The spec explicitly requires these buttons.
- **Personalization uses user profile to simplify/complexify content**: ✅ Fully compliant. The 'Personalize for Me' button implies this functionality.
- **Urdu translation uses gemini-2.0-flash with Urdu prompt engineering**: ✅ Fully compliant. The 'اردو میں ترجمہ کریں' button implies this functionality.

## Project Structure

### Documentation (this feature)

```text
specs/001-textbook-content/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
book_frontend/
├── docs/
│   ├── intro.mdx
│   ├── module1-ros2/
│   │   ├── _category_.json
│   │   └── index.mdx
│   ├── module2-digital-twin/
│   │   ├── _category_.json
│   │   └── index.mdx
│   ├── module3-ai-robot-brain/
│   │   ├── _category_.json
│   │   └── index.mdx
│   ├── module4-vla/
│   │   ├── _category_.json
│   │   └── index.mdx
│   ├── capstone/
│   │   ├── _category_.json
│   │   └── index.mdx
│   └── hardware-lab.mdx
├── src/
│   ├── components/
│   ├── pages/
│   └── theme/
├── sidebars.js
└── docusaurus.config.js

backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

```

**Structure Decision**: The project will utilize a monorepo-like structure with `book_frontend` for the Docusaurus application and `backend` for the FastAPI RAG chatbot (though the latter is not directly modified by *this* feature, its presence is acknowledged). The Docusaurus `docs` directory will house all generated textbook content, organized into subdirectories for each module and chapter, along with `_category_.json` files for sidebar management and an updated `sidebars.js` file.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
