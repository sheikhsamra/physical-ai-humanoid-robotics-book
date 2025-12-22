# Quickstart Guide: Physical AI & Humanoid Robotics Book

## Prerequisites

- Node.js v18 or higher
- npm or yarn package manager
- Git for version control
- Text editor or IDE

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install Dependencies
```bash
npm install
# OR
yarn install
```

### 3. Start Local Development Server
```bash
npm run start
# OR
yarn start
```

This command starts a local development server and opens the documentation in your browser at `http://localhost:3000`.

### 4. Project Structure
```
docs/
├── intro.md                 # Introduction page
├── overview/                # Quarter overview content
│   ├── abstract.md          # Book abstract
│   ├── introduction.md      # Book introduction
│   └── literature-review.md # Background literature
├── module-1/                # Module 1: The Robotic Nervous System
│   ├── index.md             # Module 1 overview
│   ├── chapter-1-introduction-to-ros2.md
│   ├── chapter-2-nodes-topics-services.md
│   ├── chapter-3-bridging-ai-controllers.md
│   └── chapter-4-urdf-humanoid-robots.md
├── module-2/                # Module 2: Gazebo Simulation
├── module-3/                # Module 3: NVIDIA Isaac
├── module-4/                # Module 4: Vision-Language-Action Systems
└── sidebar.js               # Navigation configuration
```

## Creating New Content

### Adding a New Chapter
1. Create a new Markdown file in the appropriate module directory
2. Add the chapter to `sidebar.js` to make it accessible
3. Follow the established content format with proper citations

### Content Format Template
```markdown
---
title: Chapter Title
description: Brief description of chapter content
---

# Chapter Title

## Learning Objectives

- Objective 1
- Objective 2
- Objective 3

## Introduction

[Content introduction]

## Main Content

### Section Title

[Main content with appropriate citations]

## Summary

[Chapter summary]

## References

[APA-formatted citations]
```

## Building for Production

To build the static site for deployment:

```bash
npm run build
# OR
yarn build
```

The built site will be available in the `build/` directory and can be deployed to GitHub Pages.

## Validation

To validate your content before committing:

1. Check local build: `npm run build` (should complete without errors)
2. Verify navigation works properly
3. Confirm all citations follow APA format
4. Ensure content meets academic rigor standards