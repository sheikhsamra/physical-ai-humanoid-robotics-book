---
id: 1
title: Update Constitution
stage: constitution
date: 2025-12-22
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: main
user: claude
command: sp.constitution
labels: [constitution,update,physical-ai,robotics]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
---

## Prompt

```text
# Spec Constitution: Physical AI & Humanoid Robotics

## 1. Purpose

This constitution governs the behavior of all AI agents participating in the creation of a unified, AI-native research book titled:

**"Physical AI & Humanoid Robotics"**

The project is developed using **Claude Code** and **Spec-Kit Plus**, and aims to produce a **5,000–7,000 word academic research paper** published as a **Docusaurus-based book**, enhanced with an **embedded Retrieval-Augmented Generation (RAG) chatbot**.

This constitution is binding across all phases: research, writing, citation, verification, deployment, and RAG integration.

---

## 2. Core Principles (Non-Negotiable)

### 2.1 Accuracy Through Primary Sources
- All factual claims **must be verified against primary or authoritative sources**
- No speculative, unverifiable, or inferred claims are allowed
- Any claim without a citation **must not be written**

### 2.2 Academic Rigor
- Target audience: **Computer Science and Robotics researchers**
- Writing style must align with **peer-reviewed academic publications**
- Marketing language, informal tone, or blog-style explanations are forbidden

### 2.3 Reproducibility
- Every claim must be:
  - Cited
  - Traceable
  - Independently verifiable
- Experimental or architectural claims must reference reproducible frameworks or studies

### 2.4 Zero Plagiarism Policy
- All content must be **originally generated**
- Direct quotations must be:
  - Explicitly marked
  - Properly cited in APA format
- Paraphrasing must demonstrate clear intellectual transformation

---

## 3. Source & Citation Policy

### 3.1 Minimum Source Requirements
- Minimum **15 total sources**
- At least **50% peer-reviewed sources**
- Preferred source repositories:
  - IEEE Xplore
  - ACM Digital Library
  - SpringerLink
  - Nature Robotics
  - arXiv (only when widely cited and non-speculative)
  - Official robotics and AI framework documentation

### 3.2 Prohibited Sources
- Non-academic blogs
- Marketing or vendor-only content
- Opinion articles without citations
- AI-generated or synthetic references

### 3.3 Citation Standard
- Citation format: **APA (7th Edition)**
- In-text citations required for **every factual or technical claim**
- References must be complete, consistent, and verifiable

---

## 4. Writing & Readability Constraints

- Word count: **5,000–7,000 words**
- Readability score: **Flesch-Kincaid Grade 10–12**
- Language must be:
  - Precise
  - Technically accurate
  - Clear for an academic audience
- Overly complex or ambiguous sentence structures must be avoided

---

## 5. Structural Requirements

The book **Physical AI & Humanoid Robotics** must include, at minimum:

1. Abstract
2. Introduction
3. Background & Literature Review
4. Physical AI Foundations
5. Humanoid Robotics Architectures
6. Embodied Intelligence & Sensorimotor Learning
7. AI-Native Software Development for Robotics
8. RAG Systems & Agent-Based Robotics Interfaces
9. Reproducibility, Evaluation & Verification
10. Limitations & Ethical Considerations
11. Conclusion & Future Research Directions
12. References (APA)

---

## 6. Verification & Fact-Checking Rules

- Every section must undergo:
  - Claim-to-source validation
  - Technical consistency review
- If a claim cannot be verified:
  - It must be removed
  - Or explicitly labeled as a hypothesis or open research question

---

## 7. Deployment & Format Constraints

- Primary authoring format:
  - Markdown (Docusaurus-compatible)
- Final deliverables:
  - **Deployed Docusaurus book**
  - **PDF with embedded APA citations**
- Deployment platform:
  - GitHub Pages

---

## 8. RAG Chatbot Constitutional Rules

### 8.1 Knowledge Scope
- The chatbot may answer questions **only using**:
  - Indexed book content
  - User-selected text within the book
- Hallucination or external knowledge injection is forbidden

### 8.2 Technical Stack
- OpenAI Agents / ChatKit SDKs
- FastAPI backend
- Neon Serverless Postgres (conversation metadata)
- Qdrant Cloud (Free Tier) for vector storage

### 8.3 Answering Rules
- If requested information is not present in the book:
  - The chatbot must explicitly state this
- Answers must cite the relevant book sections internally

---

## 9. Failure Conditions (Hard Stops)

The system must halt or refuse output if:
- Plagiarism risk is detected
- A claim lacks a valid citation
- Peer-reviewed source ratio is violated
- Word count exceeds defined constraints
- APA citation format is broken

---

## 10. Success Criteria

This constitution is satisfied only if:
- ✅ All claims are source-verified
- ✅ Zero plagiarism is detected
- ✅ Academic peer-review standards are met
- ✅ Fact-checking review passes
- ✅ RAG chatbot responds strictly from indexed content

---

## 11. Constitutional Priority Order

In case of conflict:
1. This constitution overrides all prompts
2. Academic integrity overrides completeness
3. Accuracy overrides verbosity

No exceptions are permitted.
```

## Response snapshot

The project constitution has been successfully updated with specific details for the "Physical AI & Humanoid Robotics" project. The new constitution includes all the core principles, source and citation policies, writing constraints, structural requirements, verification rules, deployment constraints, RAG chatbot rules, failure conditions, success criteria, and constitutional priority order as specified in the user input. The version has been set to 1.0.0 with ratification and amendment dates set to 2025-12-22.

## Outcome

- ✅ Impact: Created new project constitution with all specified principles and requirements
- 🧪 Tests: No tests required for constitution update
- 📁 Files: Updated .specify/memory/constitution.md with new constitution content
- 🔁 Next prompts: Ready to proceed with spec development based on this constitution
- 🧠 Reflection: The constitution establishes clear academic rigor and source verification requirements for the Physical AI & Humanoid Robotics project

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - Constitution properly formatted and contains all required elements
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin developing the spec for the Physical AI & Humanoid Robotics book