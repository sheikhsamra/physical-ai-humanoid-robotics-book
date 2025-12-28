# Data Model: RAG Ingestion Pipeline

## Entities

### ContentChunk
**Description**: Represents a segment of text from the Docusaurus book with associated metadata

**Fields**:
- `id` (string): Unique identifier for the chunk
- `source_url` (string): Original URL where the content was found
- `module` (string): Module/section identifier from the book structure
- `section` (string): Specific section within the module
- `content` (string): The actual text content of the chunk
- `metadata` (dict): Additional metadata including creation timestamp, source details
- `word_count` (int): Number of words in the content
- `token_count` (int): Number of tokens in the content (for embedding models)

**Validation Rules**:
- `source_url` must be a valid URL
- `content` must not be empty
- `word_count` must be positive
- `token_count` must be positive

### EmbeddingVector
**Description**: Represents the vector embedding of a content chunk

**Fields**:
- `chunk_id` (string): Reference to the ContentChunk this embedding represents
- `vector_data` (list[float]): The numerical vector representation of the content
- `model_name` (string): Name of the embedding model used
- `model_version` (string): Version of the embedding model used
- `created_at` (datetime): Timestamp when the embedding was generated

**Validation Rules**:
- `chunk_id` must reference an existing ContentChunk
- `vector_data` must be a non-empty list of floats
- `model_name` must not be empty

### IngestionStatus
**Description**: Tracks the status of the ingestion pipeline

**Fields**:
- `pipeline_id` (string): Unique identifier for this pipeline run
- `status` (string): Current status (e.g., "running", "completed", "failed")
- `progress` (float): Progress percentage (0.0 to 1.0)
- `total_pages` (int): Total number of pages to process
- `processed_pages` (int): Number of pages processed so far
- `total_chunks` (int): Total number of chunks created
- `embedded_chunks` (int): Number of chunks that have embeddings generated
- `stored_vectors` (int): Number of vectors stored in the database
- `start_time` (datetime): When the pipeline started
- `end_time` (datetime): When the pipeline completed (null if still running)
- `error_info` (dict): Error details if the pipeline failed
- `summary` (dict): Summary statistics about the ingestion

**Validation Rules**:
- `progress` must be between 0.0 and 1.0
- `total_pages` must be non-negative
- `processed_pages` must not exceed `total_pages`
- `status` must be one of the allowed values

### PageMetadata
**Description**: Metadata about each page in the Docusaurus book

**Fields**:
- `url` (string): The URL of the page
- `title` (string): The title of the page
- `module` (string): The module this page belongs to
- `section` (string): The section within the module
- `hierarchy_level` (int): The depth in the site hierarchy
- `parent_url` (string): URL of the parent page (if applicable)
- `word_count` (int): Number of words in the page
- `last_modified` (datetime): When the page was last modified

**Validation Rules**:
- `url` must be a valid URL
- `title` must not be empty
- `hierarchy_level` must be non-negative

## Relationships

### ContentChunk → EmbeddingVector
- One-to-one relationship: Each ContentChunk has exactly one EmbeddingVector
- Foreign Key: EmbeddingVector.chunk_id references ContentChunk.id

### PageMetadata → ContentChunk
- One-to-many relationship: Each PageMetadata can have multiple ContentChunks
- Foreign Key: ContentChunk.source_url relates to PageMetadata.url

## State Transitions

### IngestionStatus States
1. `pending` → `running`: When the pipeline starts processing
2. `running` → `completed`: When all pages are processed successfully
3. `running` → `failed`: When an error occurs during processing
4. `failed` → `running`: When retrying after a failure (if implemented)

## Indexes

### ContentChunk
- Index on `source_url` for efficient lookups by URL
- Index on `module` and `section` for efficient filtering by book structure

### EmbeddingVector
- Index on `chunk_id` for efficient joins with ContentChunk
- Index on `model_name` for filtering by embedding model

### IngestionStatus
- Index on `pipeline_id` for unique identification
- Index on `status` for filtering by status

### PageMetadata
- Index on `url` for unique identification
- Index on `module` and `section` for hierarchical navigation