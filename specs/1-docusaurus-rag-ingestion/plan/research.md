# Research Document: RAG Ingestion Pipeline

## Decision: Docusaurus URL Configuration
**Rationale**: The pipeline needs a specific URL to target for content extraction
**Alternatives considered**:
- Hardcoding the URL in the script
- Reading from environment variable
- Accepting as command-line argument
**Decision**: Use command-line argument with environment variable fallback for flexibility and security

## Decision: Cohere API Key Configuration
**Rationale**: API keys should be securely managed without being hardcoded
**Alternatives considered**:
- Hardcoding in the script (insecure)
- Reading from environment variable
- Reading from configuration file
**Decision**: Use environment variable with clear documentation for secure configuration

## Decision: Qdrant Cloud Configuration
**Rationale**: Vector database connection details need to be configurable and secure
**Alternatives considered**:
- Hardcoding connection details
- Using environment variables
- Reading from configuration file
**Decision**: Use environment variables for connection details with documentation

## Decision: Sitemap Location
**Rationale**: Need to discover all book pages systematically
**Alternatives considered**:
- Assuming standard location (/sitemap.xml)
- Accepting as parameter
- Auto-detection by checking common locations
**Decision**: Default to standard location with parameter override capability

## Decision: Optimal Chunk Size
**Rationale**: Need to balance embedding quality and token usage
**Research findings**:
- Cohere recommends chunks between 100-512 tokens for optimal performance
- Average English sentence is ~15-20 tokens
- For text, 200-300 words per chunk is typically optimal
**Decision**: Use 256-word chunks with overlap to preserve context

## Decision: Rate Limiting Strategy
**Rationale**: Prevent overwhelming external services and respect usage policies
**Research findings**:
- Web scraping should include delays between requests
- Cohere API has rate limits that vary by plan
- Qdrant Cloud may have ingestion rate limits
**Decision**: Implement configurable delays and exponential backoff for retries

## Decision: Content Extraction Strategy
**Rationale**: Need to extract main content while preserving structure and metadata
**Research findings**:
- Docusaurus sites typically use consistent class names for main content
- BeautifulSoup is effective for HTML parsing
- Need to handle navigation, headers, and footers appropriately
**Decision**: Use CSS selectors targeting Docusaurus-specific content containers

## Decision: Error Handling Approach
**Rationale**: Pipeline should be robust and provide clear feedback
**Decision**: Implement comprehensive error handling with specific error types for different failure modes