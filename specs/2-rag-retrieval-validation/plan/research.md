# Research Document: RAG Retrieval & Pipeline Validation

## Decision: Collection Name
**Rationale**: Need to connect to the correct Qdrant collection where vectors are stored
**Alternatives considered**:
- Using default collection name "docusaurus_content" (from ingestion pipeline)
- Discovering collection names dynamically
- Reading from configuration
**Decision**: Use "docusaurus_content" as it matches the ingestion pipeline collection name

## Decision: Query Examples
**Rationale**: Need sample queries to test the retrieval functionality
**Alternatives considered**:
- Using generic queries like "What is ROS2?"
- Creating queries based on actual content from the book
- Reading queries from a file
**Decision**: Create relevant queries based on the actual content from the Physical AI Humanoid Robotics book

## Decision: Relevance Threshold
**Rationale**: Need to define what similarity score constitutes a "relevant" result
**Research findings**:
- Qdrant cosine similarity scores range from -1 to 1, with higher scores indicating greater similarity
- Common practice is to use threshold of 0.7-0.8 for high relevance
- For RAG applications, 0.6-0.7 is often acceptable
**Decision**: Use 0.65 as the default relevance threshold, configurable via parameter

## Decision: Validation Criteria
**Rationale**: Need to establish what constitutes acceptable validation results
**Research findings**:
- Validation should check both content relevance and metadata accuracy
- Metadata accuracy means source_url, module, and section match the original
- Content relevance means the retrieved chunk is semantically related to the query
**Decision**: Validation will check both content relevance (via similarity score) and metadata accuracy (via field comparison)

## Decision: Cohere Model Compatibility
**Rationale**: Ensure query embeddings are compatible with stored vector embeddings
**Research findings**:
- The ingestion pipeline used Cohere's multilingual embedding model
- Query embeddings must use the same model for compatibility
- Need to use the same embedding dimension (likely 768 or 1024)
**Decision**: Use the same Cohere embedding model as the ingestion pipeline (multilingual-v2.0)

## Decision: Error Handling Approach
**Rationale**: Pipeline should be robust and provide clear feedback
**Decision**: Implement comprehensive error handling with specific error types for different failure modes