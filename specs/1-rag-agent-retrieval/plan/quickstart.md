# Quickstart Guide: RAG Agent with Retrieval Integration

## Prerequisites

- Python 3.9+
- OpenAI API key
- Qdrant Cloud account and API key
- Cohere API key (for embedding compatibility)

## Setup

### 1. Environment Configuration

Create a `.env` file with the following variables:

```bash
OPENAI_API_KEY='your-openai-api-key'
QDRANT_API_KEY='your-qdrant-api-key'
QDRANT_HOST='your-qdrant-host-url'
COHERE_API_KEY='your-cohere-api-key'
```

### 2. Install Dependencies

```bash
pip install openai qdrant-client cohere python-dotenv
```

### 3. Verify Qdrant Connection

Ensure your Qdrant instance has the book content vectors from the previous RAG pipeline.

## Usage

### Command Line Interface

```bash
# Run the agent with a query
python agent.py "What is Physical AI?"

# Run with verbose output
python agent.py --query "How do I create a humanoid robot?" --verbose

# Validate agent responses
python agent.py --validate "Sample query for validation"
```

### Library Usage

```python
from agent import create_rag_agent

# Create the agent
agent = create_rag_agent()

# Process a query
response = agent.process_query("What is Physical AI and Humanoid Robotics?")
print(response.content)
print(response.sources)
```

## Validation

### Test Sample Queries

The agent should respond to queries like:

- "What is Physical AI?"
- "Explain humanoid robotics"
- "How does the NVIDIA Isaac platform work?"
- "What are the key concepts in Module 3?"

### Expected Output

The agent should return responses that:

1. Are grounded in the retrieved content chunks
2. Include proper metadata attribution (source, section, module)
3. Cite specific information from the book content
4. Handle queries with no relevant results gracefully

## Troubleshooting

### Common Issues

- **API Key Errors**: Verify your API keys in the `.env` file
- **Qdrant Connection**: Check that your Qdrant instance is accessible and contains vectors
- **Embedding Mismatch**: Ensure Cohere embedding model matches the one used in ingestion
- **Rate Limits**: OpenAI and Qdrant may have rate limits that affect performance

### Debugging

Enable verbose logging with the `--verbose` flag to see detailed logs of the agent's interactions and retrieval process.