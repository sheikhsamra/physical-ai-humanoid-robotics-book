# Data Model: RAG Retrieval & Pipeline Validation

## Entities

### Query
**Description**: Represents a search query input for the RAG system

**Fields**:
- `text` (string): The query text to search for
- `id` (string): Unique identifier for the query
- `created_at` (datetime): Timestamp when the query was created

**Validation Rules**:
- `text` must not be empty
- `id` must be a valid UUID

### SearchResult
**Description**: Represents a result from the similarity search in Qdrant

**Fields**:
- `id` (string): Unique identifier of the matched vector
- `score` (float): Similarity score between query and result (0.0-1.0)
- `payload` (dict): Metadata associated with the vector
- `content` (string): The actual content of the retrieved chunk
- `source_url` (string): URL where the content originated
- `module` (string): Module identifier from the original content
- `section` (string): Section identifier from the original content

**Validation Rules**:
- `score` must be between 0.0 and 1.0
- `content` must not be empty
- `source_url` must be a valid URL
- Required fields in `payload`: `source_url`, `module`, `section`, `content`

### ValidationResult
**Description**: Assessment of retrieval relevance and metadata accuracy

**Fields**:
- `query_id` (string): Reference to the original query
- `search_results` (list[SearchResult]): List of retrieved results
- `relevance_score` (float): Overall relevance score for the results (0.0-1.0)
- `metadata_accuracy` (float): Accuracy of metadata preservation (0.0-1.0)
- `content_relevance` (float): Relevance of content to query (0.0-1.0)
- `is_valid` (bool): Whether the results meet validation criteria
- `threshold_used` (float): Threshold that was applied for validation
- `details` (dict): Detailed breakdown of validation scores

**Validation Rules**:
- `relevance_score` must be between 0.0 and 1.0
- `metadata_accuracy` must be between 0.0 and 1.0
- `content_relevance` must be between 0.0 and 1.0
- `is_valid` is true if `relevance_score` >= threshold_used

### ValidationReport
**Description**: Structured output containing validation metrics

**Fields**:
- `query_text` (string): Original query text
- `total_results` (int): Number of results returned
- `valid_results` (int): Number of results that met validation criteria
- `success_rate` (float): Percentage of valid results (0.0-1.0)
- `avg_similarity` (float): Average similarity score of results
- `metadata_accuracy_rate` (float): Percentage of results with valid metadata
- `validation_results` (list[ValidationResult]): Individual validation results
- `execution_time` (float): Time taken to execute and validate query (seconds)
- `timestamp` (datetime): When the validation was performed
- `errors` (list): List of errors encountered during validation

**Validation Rules**:
- `success_rate` must be between 0.0 and 1.0
- `avg_similarity` must be between 0.0 and 1.0
- `metadata_accuracy_rate` must be between 0.0 and 1.0
- `total_results` must be non-negative
- `valid_results` must be <= `total_results`

### QdrantConnectionConfig
**Description**: Configuration for connecting to Qdrant Cloud

**Fields**:
- `api_key` (string): Authentication key for Qdrant Cloud
- `host` (string): Host URL for the Qdrant Cloud instance
- `port` (int): Port number (usually 6333)
- `collection_name` (string): Name of the collection to query (default: "docusaurus_content")
- `https` (bool): Whether to use HTTPS (default: true)

**Validation Rules**:
- `api_key` must not be empty
- `host` must be a valid URL
- `port` must be between 1 and 65535
- `collection_name` must not be empty

## Relationships

### Query → SearchResult
- One-to-many relationship: One query can return multiple search results
- Reference: SearchResult includes query_id linking back to the original query

### SearchResult → ValidationResult
- One-to-many relationship: One validation result can validate multiple search results
- Reference: ValidationResult contains list of SearchResult objects

### ValidationResult → ValidationReport
- One-to-one relationship: Each validation run produces a single report
- Reference: ValidationReport contains list of ValidationResult objects

## State Transitions

### ValidationResult States
1. `created` → `validating`: When validation begins on search results
2. `validating` → `completed`: When validation finishes successfully
3. `validating` → `failed`: When validation encounters an error
4. `completed` → `validated`: When validation determines if results meet criteria

## Indexes

### SearchResult
- Index on `source_url` for efficient filtering by source
- Index on `module` and `section` for filtering by content hierarchy
- Index on `score` for ordering results by relevance

### ValidationReport
- Index on `query_text` for finding specific query validations
- Index on `timestamp` for chronological analysis of validation results
- Index on `success_rate` for filtering by validation quality

### Query
- Index on `text` for detecting duplicate queries
- Index on `id` for unique identification