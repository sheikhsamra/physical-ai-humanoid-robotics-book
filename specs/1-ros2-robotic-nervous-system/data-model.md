# Data Model: Physical AI & Humanoid Robotics Book

## Content Structure

### Book
- **title**: "Physical AI & Humanoid Robotics"
- **description**: Academic textbook covering physical AI and humanoid robotics concepts
- **wordCount**: 5000-7000 words (target range)
- **readabilityLevel**: Flesch-Kincaid Grade 10-12
- **citationStyle**: APA (7th Edition)
- **modules**: Array of Module entities

### Module
- **id**: Unique identifier (e.g., "module-1")
- **title**: Descriptive title (e.g., "The Robotic Nervous System (ROS 2)")
- **description**: Brief overview of module content
- **learningObjectives**: Array of learning objectives
- **chapters**: Array of Chapter entities
- **prerequisites**: Prerequisite knowledge requirements
- **targetAudience**: Intended reader profile

### Chapter
- **id**: Unique identifier (e.g., "chapter-1")
- **title**: Descriptive title
- **purpose**: Chapter objective
- **topics**: Array of topics covered
- **constraints**: Content limitations or exclusions
- **content**: Markdown content string
- **figures**: Array of figure references
- **citations**: Array of source citations

### Citation
- **id**: Unique identifier
- **type**: Source type (e.g., "journal", "book", "conference", "website")
- **authors**: Array of author names
- **title**: Publication title
- **journal**: Journal/publisher name
- **year**: Publication year
- **doi**: Digital object identifier (if available)
- **url**: Source URL (if applicable)
- **accessDate**: Date source was accessed
- **apaFormatted**: APA-formatted citation string

### Figure
- **id**: Unique identifier
- **title**: Figure title/caption
- **description**: Brief description of content
- **filePath**: Relative path to image file
- **altText**: Alternative text for accessibility
- **source**: Source attribution if applicable

## Navigation Structure

### Sidebar
- **items**: Array of navigation items (modules and chapters)
- **collapsible**: Whether sections can be collapsed
- **defaultCollapsed**: Default state for collapsible sections

### NavigationItem
- **type**: Item type ("category" for modules, "doc" for chapters)
- **label**: Display name
- **items**: Array of child items (for categories)
- **id**: Reference to document ID (for docs)

## Validation Rules

1. **Module Requirements**:
   - Each module must have 1-4 chapters
   - Module must have at least 3 learning objectives
   - Module content must be between 1,250-1,750 words

2. **Chapter Requirements**:
   - Each chapter must have a clear purpose statement
   - Chapter must include 3-7 main topics
   - Chapter must have 2-5 citations from peer-reviewed sources
   - Content must maintain academic tone

3. **Citation Requirements**:
   - At least 50% of sources must be peer-reviewed
   - All factual claims must have citations
   - Citations must follow APA (7th Edition) format
   - Minimum 15 total sources across the book

4. **Content Requirements**:
   - All content must be original (zero plagiarism)
   - Content must target Grade 10-12 reading level
   - Technical terminology must be consistent across modules
   - Content must prepare readers for subsequent modules

## State Transitions

### Chapter States
- **draft**: Initial state, content is being written
- **review**: Content is under review for accuracy and compliance
- **approved**: Content has passed review and is ready for publication
- **published**: Content is included in the final book

### Module States
- **planning**: Module structure and outline being defined
- **development**: Chapters are being written
- **integration**: Module is being integrated with book structure
- **complete**: Module is complete and ready for publication