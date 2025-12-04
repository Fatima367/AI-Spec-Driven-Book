---
id: 0001
title: Constitution Update with Bonus Features
stage: constitution
date: 2025-12-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: User provided constitution and then requested to add bonus features.
command: /sp.constitution
labels: ["constitution", "update"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- .specify/memory/constitution.md
tests:
- N/A
---

## Prompt

```
 ## **Physical AI & Humanoid Robotics Textbook Project Constitution**

## **Role**

You are the Chief Technology Officer and Lead Editor for the "Physical AI & Humanoid Robotics" textbook.

## **CORE RULES (never break):**

1.  Full course content based on the "Physical AI & Humanoid Robotics" course details from @Hackathon I_ Physical AI & Humanoid Robotics Textbook.md.
2. The book must be titled "Physical AI & Humanoid Robotics – From Digital Brain to Embodied Intelligence"
3. Publish book to GitHub Pages (docusaurus build → gh-pages).
4. Deploy to GitHub Pages (free).
5. Full RAG chatbot using FastAPI \+ Neon Postgres \+ Qdrant Free Tier \+ OpenAI ChatKit SDK (with Gemini API key). The chatbot must be able to answer user questions about the book's content, including answering questions based solely on text selected by the user.
6. Use Claude Code subagents extensively when needed.
7. All code must be production-ready, beautiful, and demo-ready in <90 seconds.
8. **Accuracy through primary source verification.**
9. **Clarity for audience.**
10. **Reproducibility (all claims cited and traceable).**
11. **Rigor (peer-reviewed sources preferred).**


## **Bonus Features:**
   1. Claude Code Subagents: Create specialized helper agents (e.g., summarizer, transformer, writing assistant).
   2. Agent Skills: Develop reusable intelligence modules (predefined knowledge or capabilities).
   3. Subagent \+ Skill Interaction: Show a Subagent dynamically loading and using a Skill (Matrix-style “load skill” analogy).
   4. Useful Integration: Subagents/Skills should support the book creation or the RAG chatbot.
   5. Implement Better-Auth with signup questions about software/hardware background
   6. Logged-in users get two buttons per chapter: "Personalize for Me" and "اردو میں ترجمہ کریں"
   7. Personalization uses user profile to simplify/complexify content
   8. Urdu translation uses gemini-2.0-flash with Urdu prompt engineering


## **Tech Stack**

1. **Frontend:** Docusaurus (React, TypeScript, CSS).
2. **Backend:** FastAPI (Python 3.10+), Pydantic.
3. **Database:** Neon (Serverless Postgres) for User Data.
4. **Vector DB:** Qdrant Cloud (Free Tier) for RAG.
5. **Auth:** BetterAuth (https://www.better-auth.com/) for handling Signups/Logins.
6. **AI:** OpenAI Agents SDK with Gemini API key / ChatKit.

## **Technical & Non-Functional Standards**

### **Performance and Scalability**

* **Response Time:** Backend API responses must target **<500ms** for 95% of requests.
* **Frontend Optimization:** Implement lazy loading for large components and images, and ensure the Time to Interactive (TTI) is **<3 seconds** on mobile devices.
* **Database:** Utilize Neon's indexing and connection pooling features effectively to prevent performance bottlenecks.

### **UI/UX & Accessibility Standards**

* **User Experience (UX):** The interface must be intuitive and professional. Navigation (chapters, search) and the RAG chatbot must be easily accessible and smooth.
* **UI Design:** Implement a clean, professional, and dark-mode-compatible design system using Tailwind CSS.
* **Responsiveness:** The entire interface must be fully responsive, providing an optimal viewing and interaction experience across **all devices (mobile, tablet, desktop)**.
* **Accessibility (A11y):** All interactive components must meet WCAG 2.1 AA standards, including full keyboard navigation support, sufficient color contrast, and descriptive ARIA labels.

### **Better Educational Experience**

* **Interactivity:** Content should feature interactive elements such as code sandboxes, glossary tooltips for technical terms, and embedded quizzes or self-assessment questions at the end of key sections.
* **Scaffolding:** Ensure content is clearly structured, with appropriate vocabulary and conceptual clarity suitable for a university-level audience with varied technical backgrounds.
* **Visualizers:** Integrate visual components (e.g., React components for demonstrating inverse kinematics or neural network structures) where appropriate to aid understanding.

### **RAG Chatbot Integrity Standards (No Web Search/Hallucination)**

* **Strict Grounding Mandate:** The RAG system **must** be configured to use **only** the indexed content of the "Physical AI & Humanoid Robotics" textbook documents. **The Google Search Tool is explicitly forbidden.**
* **Citation Mandate:** Every answer from the RAG chatbot must include a direct, verifiable citation (e.g., Chapter/Section link) to the source text within the book.
* **Failure Mode:** If the user's query cannot be answered based on the indexed book content, the chatbot **must** return a polite refusal message (e.g., "I can only answer questions based on the content of the textbook.") instead of attempting to generate an ungrounded, potentially hallucinatory response.

## **Coding Standards**

* **Strict Typing:** Use TypeScript interfaces for all React props. Use Pydantic models for all Python API bodies.
* **Modularity:** Backend logic must be separated from routes. Frontend components must be reusable.
* **Documentation:** All functions must have docstrings.
* **Error Handling:** Graceful degradation. If RAG fails, show a standard error.


## **Security \& Hardening**:

* **API Key Management:** DO NOT expose keys in the repository. All secrets (API keys, DB credentials) must be managed exclusively via environment variables (.env file for local development) and secured secrets management in the deployment pipeline.
* **Input Validation:** Implement strict Pydantic model validation on all FastAPI endpoints to prevent injection attacks and ensure data integrity.
* **CORS/CSRF:** Configure FastAPI with appropriate CORS policies and implement Cross-Site Request Forgery (CSRF) protection mechanisms where required (e.g., form submissions).
* **Dependency Scanning:** Regularly audit and scan all project dependencies (npm, pip) for known vulnerabilities.

## **Key Standards:**

* All factual claims must be traceable to sources.
* Source types: minimum 50% peer-reviewed articles.
* Writing clarity.


## **Success Criteria:**

* Book published to GH Pages
* RAG answers correctly, strictly based on book content, and includes document citations.
* All performance targets (API <500ms, TTI <3s) are met.
* All claims verified against sources.
* Zero plagiarism detected.
* Passes fact-checking review.
* Signup/login working with user profile saved in Neon.
* Personalization and Urdu toggle function per chapter.

## **Constraints:**
* **Infrastructure**: Use open/free tiers for prototype infra (Qdrant Cloud Free, Neon Serverless). Must adhere to their respective free-tier usage limits.
* **Source Count**: Minimum of 5-8 highly-regarded sources must be used, with at least 50% being peer-reviewed.
* **Deployment**: Deployment setup must be simple and replicable using standard GitHub  Pages configuration.

---
[Request interrupted by user]you didn't add bonus features in constitution
```

## Response snapshot

```
The constitution has been updated to version 0.1.1, incorporating the "Bonus Features" section. This was a patch bump as it involved adding new content.

The following template files require manual review and alignment with the updated constitution:
- `.specify/templates/plan-template.md`: Review for alignment with new constitution principles.
- `.specify/templates/spec-template.md`: Review for alignment with new constitution principles, especially regarding security, performance, UI/UX, and RAG chatbot integrity.
- `.specify/templates/tasks-template.md`: Review for alignment with new constitution principles, ensuring tasks reflect security, performance, UI/UX, and RAG chatbot integrity standards.

Suggested commit message:
`docs: amend constitution to v0.1.1 (bonus features added)`
```

## Outcome

- ✅ Impact: Constitution document updated with bonus features.
- 🧪 Tests: No tests run.
- 📁 Files: One file modified: `.specify/memory/constitution.md`
- 🔁 Next prompts: Review and update template files for alignment.
- 🧠 Reflection: The user identified a missing section in the initial constitution update, which was then corrected. This highlights the importance of thorough verification against user input.

## Evaluation notes (flywheel)

- Failure modes observed: Initial constitution update missed a section.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
