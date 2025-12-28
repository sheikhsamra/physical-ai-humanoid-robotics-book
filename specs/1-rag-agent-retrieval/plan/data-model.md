# Data Model: RAG Agent with Retrieval Integration

## Entities

### Agent
**Description**: Core AI agent instance with tools and configuration

**Fields**:
- `id` (string): Unique identifier for the agent instance
- `model` (string): OpenAI model used by the agent (e.g., "gpt-4o")
- `instructions` (string): System instructions for the agent behavior
- `tools` (list): List of tools registered with the agent
- `created_at` (datetime): Timestamp when the agent was created

**Validation Rules**:
- `id` must be a valid UUID
- `model` must be a valid OpenAI model identifier
- `instructions` must not be empty
- `tools` must contain at least one tool

### RetrievalTool
**Description**: Tool function for retrieving content from Qdrant with parameters and results

**Fields**:
- `name` (string): Name of the tool function
- `description` (string): Description of what the tool does
- `parameters` (dict): JSON schema defining the input parameters
- `function` (callable): The actual function implementation
- `qdrant_client` (object): Client instance for Qdrant connection

**Validation Rules**:
- `name` must be a valid function name
- `description` must not be empty
- `parameters` must follow JSON schema format
- `function` must be callable
- `qdrant_client` must be a valid Qdrant client instance

### AgentResponse
**Description**: Response from the agent including content and metadata

**Fields**:
- `content` (string): The main response content from the agent
- `sources` (list[Source]): List of sources used in the response
- `query` (string): Original query that generated this response
- `created_at` (datetime): Timestamp when the response was generated
- `agent_id` (string): Reference to the agent that generated the response

**Validation Rules**:
- `content` must not be empty
- `sources` must contain valid source references if provided
- `query` must not be empty
- `agent_id` must be a valid agent identifier

### Source
**Description**: Information about a source used in an agent response

**Fields**:
- `id` (string): Unique identifier of the source content
- `content` (string): The actual content from the source
- `source_url` (string): URL where the content originated
- `module` (string): Module identifier from the original content
- `section` (string): Section identifier from the original content
- `score` (float): Similarity score of the content to the query (0.0-1.0)

**Validation Rules**:
- `id` must not be empty
- `content` must not be empty
- `source_url` must be a valid URL
- `module` must not be empty
- `section` must not be empty
- `score` must be between 0.0 and 1.0

### ValidationResult
**Description**: Assessment of response grounding and metadata accuracy

**Fields**:
- `response_id` (string): Reference to the agent response being validated
- `is_grounded` (bool): Whether the response is properly grounded in retrieved content
- `grounding_score` (float): Score indicating how well the response matches retrieved content (0.0-1.0)
- `metadata_accuracy` (float): Accuracy of metadata attribution (0.0-1.0)
- `details` (dict): Detailed breakdown of validation results
- `is_valid` (bool): Whether the response meets validation criteria

**Validation Rules**:
- `response_id` must be a valid response identifier
- `grounding_score` must be between 0.0 and 1.0
- `metadata_accuracy` must be between 0.0 and 1.0
- `is_valid` is true if `grounding_score` >= 0.7 and `metadata_accuracy` >= 0.8

## Relationships

### Agent → AgentResponse
- One-to-many relationship: One agent can generate multiple responses
- Reference: AgentResponse includes agent_id linking back to the original agent

### AgentResponse → Source
- One-to-many relationship: One response can reference multiple sources
- Reference: AgentResponse contains list of Source objects

### RetrievalTool → Source
- One-to-many relationship: One retrieval tool can return multiple sources
- Reference: RetrievalTool function returns list of Source objects

## State Transitions

### ValidationResult States
1. `created` → `validating`: When validation begins on an agent response
2. `validating` → `completed`: When validation finishes successfully
3. `validating` → `failed`: When validation encounters an error
4. `completed` → `validated`: When validation determines if response meets criteria

## Indexes

### AgentResponse
- Index on `agent_id` for efficient filtering by agent
- Index on `created_at` for chronological analysis of responses

### Source
- Index on `source_url` for efficient filtering by source
- Index on `module` and `section` for filtering by content hierarchy
- Index on `score` for ordering by relevance

### ValidationResult
- Index on `response_id` for finding specific response validations
- Index on `created_at` for chronological analysis of validation results
- Index on `is_valid` for filtering by validation status