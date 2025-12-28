# RAG Ingestion Pipeline for Docusaurus Book Content

This pipeline extracts content from Docusaurus documentation sites, processes it, generates embeddings using Cohere, and stores the vectors in Qdrant Cloud for RAG (Retrieval-Augmented Generation) applications.

## Prerequisites

- Python 3.9+
- UV package manager
- Cohere API key
- Qdrant Cloud account and API key

## Setup

1. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

2. Create a `.env` file with your configuration:
   ```env
   # Cohere API configuration
   COHERE_API_KEY=your_cohere_api_key_here

   # Qdrant Cloud configuration
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_HOST=your_cluster_endpoint_here  # e.g., "https://your-cluster.us-east4-0.gcp.cloud.qdrant.io"
   QDRANT_PORT=6333  # Default port, change if different

   # Optional: Docusaurus book configuration
   BOOK_URL=https://your-docusaurus-book-url.com  # Default book URL if not provided as argument
   ```

## Usage

Run the pipeline with a Docusaurus book URL:

```bash
python main.py --book-url "https://your-docusaurus-book.com"
```

### Additional Options

- `--chunk-size`: Size of text chunks in words (default: 256)
- `--collection-name`: Name of the Qdrant collection (default: docusaurus_content)
- `--verbose`: Enable verbose logging

Example with all options:
```bash
python main.py --book-url "https://example-docusaurus-book.com" --chunk-size 300 --collection-name "my_book_content" --verbose
```

## How It Works

The pipeline performs the following steps:

1. **Fetch Sitemap**: Retrieves the sitemap from the Docusaurus book to discover all pages
2. **Extract Content**: Extracts main content from each page while preserving structure and metadata
3. **Clean & Process**: Cleans HTML, removes navigation elements, normalizes text, and segments content
4. **Generate Embeddings**: Creates semantic embeddings using Cohere's embedding models
5. **Store Vectors**: Stores embeddings in Qdrant Cloud with associated metadata
6. **Validate**: Validates the ingestion by checking vector counts and sample payloads

## Configuration

The pipeline can be configured through environment variables (in `.env`) or command-line arguments. The command-line arguments take precedence over environment variables.

## Output

The pipeline generates a comprehensive report showing:
- Number of pages processed
- Number of content chunks created
- Number of vectors stored
- Success rate
- Validation results

## Troubleshooting

- If you get rate limit errors, the pipeline has built-in retry logic with exponential backoff
- Make sure your Cohere and Qdrant credentials are valid
- Verify that the book URL is accessible and follows Docusaurus structure
- Use the `--verbose` flag for detailed logging during execution

## RAG Agent with Retrieval Integration

This backend also includes a RAG Agent that can answer questions using the ingested content.

### Setup for RAG Agent

1. **Add OpenAI API key** to your `.env` file:
   ```env
   # OpenAI API configuration
   OPENAI_API_KEY=your_openai_api_key_here
   ```

2. Make sure you have ingested content in Qdrant using the ingestion pipeline above.

### Usage

Run a query directly:
```bash
python agent.py "What is Physical AI?"
```

Or with the query flag:
```bash
python agent.py --query "How do I create a humanoid robot?" --verbose
```

### Validation

Run validation on sample queries:
```bash
python agent.py --validate
```

### Help

View all available options:
```bash
python agent.py --help
```

### Features

- **Retrieval-Augmented Generation (RAG)**: Combines OpenAI's language models with vector search capabilities
- **Multi-source Integration**: Uses Cohere for embeddings and Qdrant for vector storage
- **Metadata Attribution**: Responses include source citations and relevant metadata
- **Validation**: Built-in validation to ensure responses use retrieved content
- **CLI Interface**: Command-line interface for easy interaction