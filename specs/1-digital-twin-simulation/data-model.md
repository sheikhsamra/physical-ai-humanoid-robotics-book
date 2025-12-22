# Data Model: Module 2 - The Digital Twin (Gazebo & Unity)

## Content Structure

### Module
- **id**: "module-2"
- **title**: "The Digital Twin (Gazebo & Unity)"
- **description**: Module focusing on digital twin concepts, physics simulation, and environment building for humanoid robots using Gazebo and Unity
- **learningObjectives**: Array of learning objectives
- **chapters**: Array of Chapter entities
- **prerequisites**: ["Module 1: The Robotic Nervous System (ROS 2)"]
- **targetAudience**: "Robotics and AI students with basic ROS 2 knowledge"

### Chapter
- **id**: Unique identifier (e.g., "chapter-2-1", "chapter-2-2", etc.)
- **title**: Descriptive title
- **filename**: File name with numeric prefix (e.g., "01-introduction-to-digital-twins.md")
- **purpose**: Chapter objective
- **topics**: Array of topics covered
- **constraints**: Content limitations or exclusions
- **content**: Markdown content string
- **figures**: Array of figure references
- **citations**: Array of source citations
- **moduleId**: Reference to parent module

### Citation
- **id**: Unique identifier
- **type**: Source type (e.g., "journal", "book", "conference", "website", "documentation")
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

### Digital Twin Concept
- **id**: Unique identifier
- **name**: Name of the concept (e.g., "Digital Twin", "Physics Simulation", "Sensor Simulation")
- **definition**: Clear definition of the concept
- **application**: How the concept applies to humanoid robotics
- **relatedConcepts**: Array of related concepts
- **references**: Array of related citations

### Simulation Environment
- **id**: Unique identifier
- **name**: Name of the environment (e.g., "Gazebo", "Unity")
- **purpose**: Purpose of the environment in digital twin implementation
- **capabilities**: List of key capabilities
- **integrationPoints**: How it integrates with ROS2 and other tools
- **configurationRequirements**: Setup requirements for humanoid robotics

## Validation Rules

1. **Module Requirements**:
   - Module must have exactly 4 chapters
   - Module must have at least 3 learning objectives
   - Module content must be between 1,250-1,750 words

2. **Chapter Requirements**:
   - Each chapter must have a clear purpose statement
   - Chapter must include 3-7 main topics
   - Chapter must have 2-5 citations from peer-reviewed sources
   - Content must maintain academic tone
   - Chapter must properly link to Module 1 concepts where applicable

3. **Citation Requirements**:
   - At least 50% of sources must be peer-reviewed
   - All factual claims must have citations
   - Citations must follow APA (7th Edition) format
   - Minimum 3 unique sources per chapter

4. **Content Requirements**:
   - All content must be original (zero plagiarism)
   - Content must target Grade 10-12 reading level
   - Technical terminology must be consistent across chapters
   - Content must prepare readers for Module 3 (NVIDIA Isaac) and Module 4 (Vision-Language-Action systems)
   - Content must demonstrate clear connection to Module 1 (ROS 2 control) concepts

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