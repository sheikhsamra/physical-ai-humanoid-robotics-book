# Quickstart Guide: RAG Ingestion Pipeline

## Prerequisites

- Python 3.9 or higher
- UV package manager
- Access to Cohere API (API key)
- Qdrant Cloud account and connection details

## Setup

### 1. Clone and Navigate to Project
```bash
# If you haven't already, create the backend directory
mkdir backend
cd backend
```

### 2. Initialize Project with UV
```bash
# Create a new Python project
uv init
# Or if starting fresh in the backend directory
uv venv  # Creates virtual environment
source .venv/bin/activate  # Activate virtual environment (Linux/Mac)
# or
source .venv/Scripts/activate  # Activate virtual environment (Windows)
```

### 3. Install Dependencies
The pipeline will require the following packages:
- `requests` - for fetching web content
- `beautifulsoup4` - for HTML parsing
- `cohere` - for embedding generation
- `qdrant-client` - for vector storage
- `python-dotenv` - for environment variable management

Install with:
```bash
uv pip install requests beautifulsoup4 cohere qdrant-client python-dotenv
```

## Configuration

### Environment Variables
Create a `.env` file in the backend directory with the following:

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

## Running the Pipeline

### 1. Place the main.py file
Put the `main.py` file containing the ingestion pipeline in the backend directory.

### 2. Run the Pipeline
```bash
cd backend
python main.py --book-url "https://your-docusaurus-book-url.com"
```

### Optional Parameters
```bash
# Specify custom sitemap location
python main.py --book-url "https://your-book.com" --sitemap-path "/custom-sitemap.xml"

# Specify custom chunk size
python main.py --book-url "https://your-book.com" --chunk-size 300

# Enable verbose logging
python main.py --book-url "https://your-book.com" --verbose
```

## Expected Output

The pipeline will:
1. Fetch the sitemap from the book URL
2. Extract content from all pages
3. Clean and chunk the text
4. Generate embeddings using Cohere
5. Store vectors in Qdrant Cloud
6. Validate the ingestion by checking vector count

You'll see progress indicators as the pipeline processes:
```
[INFO] Starting ingestion pipeline for: https://your-book.com
[INFO] Found 45 pages in sitemap
[INFO] Processing page 1/45: Introduction
[INFO] Extracted 1200 words from Introduction
[INFO] Created 5 chunks from Introduction
[INFO] Generated embeddings for 5 chunks
[INFO] Stored 5 vectors in Qdrant Cloud
...
[SUCCESS] Pipeline completed successfully
[SUMMARY] Processed 45 pages, created 150 chunks, stored 150 vectors
```

## Troubleshooting

### Common Issues

1. **Cohere API Error**: Check that your API key is valid and has sufficient quota
2. **Qdrant Connection Error**: Verify your cluster endpoint and API key
3. **Content Extraction Error**: Some pages might have different structures; the pipeline should continue with other pages
4. **Rate Limiting**: If you encounter rate limits, the pipeline includes backoff logic but you may need to adjust delays

### Verifying Installation

Run this command to verify all dependencies are installed:
```bash
python -c "import requests, bs4, cohere, qdrant_client; print('All dependencies available')"
```

## Next Steps

After successful execution:
1. The vectors are stored in Qdrant Cloud and ready for RAG queries
2. You can use the stored vectors with any RAG application
3. Check the Qdrant Cloud dashboard to verify vector storage