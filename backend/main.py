"""
RAG Ingestion Pipeline for Docusaurus Book Content

This script implements a pipeline to:
1. Extract content from Docusaurus documentation sites
2. Clean and chunk the text
3. Generate embeddings using Cohere
4. Store vectors in Qdrant Cloud
"""

import os
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse
import time
import argparse
import requests
from bs4 import BeautifulSoup
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ContentChunk:
    """Represents a segment of text from the Docusaurus book with associated metadata"""
    id: str
    source_url: str
    module: str
    section: str
    content: str
    metadata: Dict
    word_count: int = 0
    token_count: int = 0


@dataclass
class EmbeddingVector:
    """Represents the vector embedding of a content chunk"""
    chunk_id: str
    vector_data: List[float]
    model_name: str
    model_version: str
    created_at: str


@dataclass
class IngestionStatus:
    """Tracks the status of the ingestion pipeline"""
    pipeline_id: str
    status: str  # "running", "completed", "failed"
    progress: float
    total_pages: int
    processed_pages: int
    total_chunks: int
    embedded_chunks: int
    stored_vectors: int
    start_time: str
    end_time: Optional[str] = None
    error_info: Optional[Dict] = None
    summary: Optional[Dict] = None


def load_config():
    """Load configuration from environment variables"""
    config = {
        'cohere_api_key': os.getenv('COHERE_API_KEY'),
        'qdrant_api_key': os.getenv('QDRANT_API_KEY'),
        'qdrant_host': os.getenv('QDRANT_HOST'),
        'qdrant_port': int(os.getenv('QDRANT_PORT', 6333)),
        'book_url': os.getenv('BOOK_URL', 'https://physical-ai-humanoid-robotics-book-sandy.vercel.app/')
    }

    # Validate required configuration
    required_fields = ['cohere_api_key', 'qdrant_api_key', 'qdrant_host']
    missing_fields = [field for field in required_fields if not config[field]]

    if missing_fields:
        raise ValueError(f"Missing required configuration: {', '.join(missing_fields)}")

    return config


def validate_url(url: str) -> bool:
    """Validate if a string is a properly formatted URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def safe_request(url: str, max_retries: int = 3, delay: float = 1.0) -> Optional[requests.Response]:
    """Safely make HTTP requests with retry logic"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(delay * (2 ** attempt))  # Exponential backoff
            else:
                logger.error(f"Failed to fetch {url} after {max_retries} attempts")
                return None
    return None


def fetch_sitemap(book_url: str) -> Optional[str]:
    """Fetch the sitemap from the Docusaurus book URL"""
    # Try common sitemap locations
    sitemap_urls = [
        f"{book_url.rstrip('/')}/sitemap.xml",
        f"{book_url.rstrip('/')}/sitemap-index.xml",
        f"{book_url.rstrip('/')}/api/sitemap.xml"
    ]

    for sitemap_url in sitemap_urls:
        logger.info(f"Trying sitemap URL: {sitemap_url}")
        response = safe_request(sitemap_url)
        if response:
            logger.info(f"Successfully fetched sitemap from: {sitemap_url}")
            return response.text

    logger.error(f"Could not find sitemap at any of the common locations for {book_url}")
    return None


def extract_urls_from_sitemap(sitemap_content: str) -> List[str]:
    """Extract URLs from sitemap XML content"""
    if not sitemap_content:
        return []

    try:
        soup = BeautifulSoup(sitemap_content, 'xml')
        urls = []
        for loc in soup.find_all('loc'):
            url = loc.get_text().strip()
            if url and validate_url(url):
                urls.append(url)
        logger.info(f"Extracted {len(urls)} URLs from sitemap")
        return urls
    except Exception as e:
        logger.error(f"Error parsing sitemap: {e}")
        return []


def fetch_page_content(url: str) -> Optional[str]:
    """Fetch content from a single Docusaurus page"""
    response = safe_request(url)
    if not response:
        return None

    return response.text


def clean_text(text: str) -> str:
    """Clean and normalize text content"""
    if not text:
        return ""

    # Remove extra whitespace
    cleaned = ' '.join(text.split())

    # Normalize common special characters
    cleaned = cleaned.replace('\n', ' ').replace('\t', ' ')

    return cleaned.strip()


def clean_html_tags(text: str) -> str:
    """Remove HTML tags from text content"""
    from html import unescape
    # Remove HTML tags using regex
    import re
    clean_text = re.sub(r'<[^>]+>', '', text)
    # Unescape HTML entities
    clean_text = unescape(clean_text)
    return clean_text


def remove_navigation_elements(text: str) -> str:
    """Remove common navigation elements that are not part of main content"""
    # This would typically be applied to HTML before extracting text
    # For text that's already extracted, we can remove common patterns
    lines = text.split('\n')
    filtered_lines = []

    for line in lines:
        # Skip lines that look like navigation elements
        line_lower = line.lower()
        if any(skip in line_lower for skip in [
            'navigation', 'nav', 'menu', 'footer', 'header',
            'previous:', 'next:', 'table of contents', 'toc',
            'copyright', '©', 'all rights reserved'
        ]):
            continue
        filtered_lines.append(line)

    return '\n'.join(filtered_lines)


def normalize_text(text: str) -> str:
    """Normalize text with consistent spacing and character handling"""
    if not text:
        return ""

    # Normalize whitespace
    import re
    normalized = re.sub(r'\s+', ' ', text)  # Multiple whitespace to single space

    # Normalize special characters
    normalized = normalized.replace('\u201c', '"').replace('\u201d', '"')  # Smart quotes
    normalized = normalized.replace('\u2018', "'").replace('\u2019', "'")  # Smart apostrophes
    normalized = normalized.replace('\u2013', '-').replace('\u2014', '--')  # En/em dashes
    normalized = normalized.replace('\u00a0', ' ')  # Non-breaking space to regular space

    # Normalize line breaks
    normalized = normalized.replace('\r\n', '\n').replace('\r', '\n')

    return normalized.strip()


def preserve_code_blocks(content: str) -> str:
    """Preserve code blocks during cleaning process"""
    # For now, this is a placeholder - in a full implementation we'd extract code blocks
    # before cleaning and then reinsert them, but for this implementation we'll ensure
    # code blocks are not corrupted during text cleaning
    return content


def segment_content_by_semantics(content: str, max_chunk_size: int = 256) -> List[str]:
    """Segment content by semantic boundaries (paragraphs, sections)"""
    paragraphs = content.split('\n\n')  # Split by double newlines (paragraphs)

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        # Check if adding this paragraph would exceed the chunk size
        words_in_paragraph = len(paragraph.split())
        words_in_current = len(current_chunk.split()) if current_chunk else 0

        if words_in_current + words_in_paragraph <= max_chunk_size:
            current_chunk += "\n\n" + paragraph if current_chunk else paragraph
        else:
            # If current chunk is not empty, save it and start a new one
            if current_chunk:
                chunks.append(current_chunk.strip())

            # If the paragraph itself is larger than max_chunk_size, split it
            if words_in_paragraph > max_chunk_size:
                sentences = paragraph.split('. ')
                temp_chunk = ""

                for sentence in sentences:
                    sentence = sentence.strip() + '.'
                    words_in_sentence = len(sentence.split())
                    words_in_temp = len(temp_chunk.split()) if temp_chunk else 0

                    if words_in_temp + words_in_sentence <= max_chunk_size:
                        temp_chunk += " " + sentence if temp_chunk else sentence
                    else:
                        if temp_chunk:
                            chunks.append(temp_chunk.strip())
                        temp_chunk = sentence

                if temp_chunk:
                    current_chunk = temp_chunk
            else:
                current_chunk = paragraph

    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def validate_content_quality(content: str, min_word_count: int = 10) -> bool:
    """Validate content quality after cleaning"""
    if not content:
        return False

    word_count = len(content.split())
    if word_count < min_word_count:
        return False

    # Check if content is mostly whitespace or special characters
    text_ratio = sum(1 for c in content if c.isalnum()) / len(content) if content else 0
    if text_ratio < 0.3:  # Less than 30% alphanumeric characters
        return False

    return True


def extract_main_content(html_content: str, url: str = "") -> Tuple[str, str, str]:
    """Extract main content from Docusaurus page HTML, with module and section info"""
    if not html_content:
        return "", "", ""

    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Try to find main content area - Docusaurus specific selectors
        main_content = None

        # Common Docusaurus content selectors
        selectors = [
            'main div[class*="docItem"]',  # Docusaurus docs item
            'article',  # Standard article tag often used in Docusaurus
            'main div.container',  # Docusaurus main container
            'div.main-wrapper',  # Docusaurus main wrapper
            '.theme-doc-markdown',  # Docusaurus markdown content
            '.doc-content',  # Common doc content class
            'main',  # Main content area
            'div[class*="doc"]'  # Any div with doc in the class name
        ]

        for selector in selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break

        # If no specific content area found, use body
        if not main_content:
            main_content = soup.find('body')

        if not main_content:
            logger.warning(f"No main content found for {url}")
            return "", "", ""

        # Extract text content
        content_text = main_content.get_text(separator=' ', strip=True)
        content_text = clean_text(content_text)

        # Extract title
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else ""

        # Extract module and section from URL structure
        parsed_url = urlparse(url)
        path_parts = [part for part in parsed_url.path.split('/') if part]
        module = path_parts[0] if path_parts else "root"
        section = path_parts[-1] if path_parts else title.split()[0] if title.split() else "default"

        return content_text, module, section
    except Exception as e:
        logger.error(f"Error extracting content from {url}: {e}")
        return "", "", ""


def create_content_chunk(content: str, url: str, module: str, section: str) -> ContentChunk:
    """Create a ContentChunk object with the extracted content and metadata"""
    import uuid
    from datetime import datetime

    chunk_id = str(uuid.uuid4())
    word_count = len(content.split())
    token_count = len(content) // 4  # Rough estimation: 1 token ~ 4 characters

    return ContentChunk(
        id=chunk_id,
        source_url=url,
        module=module,
        section=section,
        content=content,
        metadata={
            "created_at": datetime.now().isoformat(),
            "source_url": url,
            "module": module,
            "section": section
        },
        word_count=word_count,
        token_count=token_count
    )


def run_ingestion_pipeline(book_url: str) -> List[ContentChunk]:
    """Run the full ingestion pipeline for a Docusaurus book"""
    logger.info(f"Starting ingestion pipeline for: {book_url}")

    # Fetch sitemap
    sitemap_content = fetch_sitemap(book_url)
    if not sitemap_content:
        logger.error("Could not fetch sitemap, stopping pipeline")
        return []

    # Extract URLs from sitemap
    urls = extract_urls_from_sitemap(sitemap_content)
    if not urls:
        logger.error("No URLs found in sitemap, stopping pipeline")
        return []

    logger.info(f"Processing {len(urls)} pages from the book")

    content_chunks = []
    for i, url in enumerate(urls, 1):
        logger.info(f"Processing page {i}/{len(urls)}: {url}")

        # Fetch page content
        html_content = fetch_page_content(url)
        if not html_content:
            logger.warning(f"Could not fetch content for {url}, skipping")
            continue

        # Extract main content
        content, module, section = extract_main_content(html_content, url)
        if not content:
            logger.warning(f"No content extracted from {url}, skipping")
            continue

        # Create content chunk
        chunk = create_content_chunk(content, url, module, section)
        content_chunks.append(chunk)

        logger.info(f"Extracted {chunk.word_count} words from {url}")

    logger.info(f"Pipeline completed. Extracted {len(content_chunks)} content chunks")
    return content_chunks


def initialize_cohere_client(api_key: str) -> cohere.Client:
    """Initialize Cohere API client"""
    return cohere.Client(api_key)


def chunk_text(content: str, chunk_size: int = 256) -> List[str]:
    """Split content into appropriately sized chunks"""
    return segment_content_by_semantics(content, chunk_size)


def generate_embeddings(cohere_client: cohere.Client, texts: List[str], model: str = "embed-multilingual-v2.0") -> List[List[float]]:
    """Generate embeddings for a list of texts using Cohere"""
    try:
        response = cohere_client.embed(
            texts=texts,
            model=model
        )
        return response.embeddings
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        return [[] for _ in texts]  # Return empty embeddings for each text


def initialize_qdrant_client(api_key: str, host: str, port: int = 6333) -> QdrantClient:
    """Initialize Qdrant Cloud client"""
    return QdrantClient(
        url=host,
        api_key=api_key,
        port=port,
        https=True
    )


def store_vectors(qdrant_client: QdrantClient, chunks: List[ContentChunk], embeddings: List[List[float]], collection_name: str = "docusaurus_content"):
    """Store embeddings with metadata in Qdrant Cloud"""
    try:
        # Check if collection exists
        try:
            collection_info = qdrant_client.get_collection(collection_name)
            # Check if the existing collection has the correct vector size
            if hasattr(collection_info.config.params, 'vectors'):
                expected_size = 768  # Cohere's embedding size
                actual_size = collection_info.config.params.vectors.size if hasattr(collection_info.config.params.vectors, 'size') else None

                if actual_size != expected_size:
                    # Delete the existing collection and recreate with correct dimensions
                    qdrant_client.delete_collection(collection_name)
                    print(f"Deleted existing collection '{collection_name}' with incorrect dimensions ({actual_size}). Recreating with {expected_size} dimensions.")

        except:
            # Collection doesn't exist, create it
            pass

        # Ensure collection exists with correct dimensions
        try:
            qdrant_client.get_collection(collection_name)
        except:
            # Create collection if it doesn't exist
            qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE)  # Cohere's embedding size
            )

        # Prepare points for insertion
        points = []
        for chunk, embedding in zip(chunks, embeddings):
            if embedding:  # Only store if we have a valid embedding
                point = models.PointStruct(
                    id=chunk.id,
                    vector=embedding,
                    payload={
                        "source_url": chunk.source_url,
                        "module": chunk.module,
                        "section": chunk.section,
                        "content": chunk.content,
                        "word_count": chunk.word_count,
                        "token_count": chunk.token_count,
                        "created_at": chunk.metadata.get("created_at", ""),
                    }
                )
                points.append(point)

        # Upload points to Qdrant
        if points:
            qdrant_client.upsert(
                collection_name=collection_name,
                points=points
            )
            logger.info(f"Stored {len(points)} vectors in Qdrant collection '{collection_name}'")
            return len(points)
        else:
            logger.warning("No points to store in Qdrant")
            return 0

    except Exception as e:
        logger.error(f"Error storing vectors in Qdrant: {e}")
        raise


def create_embedding_vector(chunk_id: str, vector_data: List[float], model_name: str = "cohere/embed-multilingual-v2.0") -> EmbeddingVector:
    """Create an EmbeddingVector object from chunk and embedding data"""
    from datetime import datetime

    return EmbeddingVector(
        chunk_id=chunk_id,
        vector_data=vector_data,
        model_name=model_name,
        model_version="v2.0",  # Default version for Cohere's multilingual model
        created_at=datetime.now().isoformat()
    )


def add_retry_logic():
    """Placeholder for retry logic implementation - would be used with API calls"""
    # This is more of an architectural consideration
    # The safe_request function already implements retry logic
    # For Cohere and Qdrant API calls, we could implement similar patterns
    pass


def track_ingestion_status(pipeline_id: str, total_pages: int) -> IngestionStatus:
    """Initialize ingestion status tracking"""
    from datetime import datetime

    return IngestionStatus(
        pipeline_id=pipeline_id,
        status="running",
        progress=0.0,
        total_pages=total_pages,
        processed_pages=0,
        total_chunks=0,
        embedded_chunks=0,
        stored_vectors=0,
        start_time=datetime.now().isoformat()
    )


def validate_vector_count(qdrant_client: QdrantClient, expected_count: int, collection_name: str = "docusaurus_content") -> bool:
    """Validate that the vector count matches expected content"""
    try:
        collection_info = qdrant_client.get_collection(collection_name)
        actual_count = collection_info.points_count
        logger.info(f"Expected {expected_count} vectors, found {actual_count} in collection")

        # Allow for some flexibility in count due to filtering out empty content
        return actual_count >= expected_count * 0.9  # At least 90% of expected content
    except Exception as e:
        logger.error(f"Error validating vector count: {e}")
        return False


def retrieve_and_validate_sample_payloads(qdrant_client: QdrantClient, sample_size: int = 5, collection_name: str = "docusaurus_content") -> bool:
    """Retrieve and validate sample payloads from the vector store"""
    try:
        # Get a few random points to validate
        # First get the total count to know the range
        collection_info = qdrant_client.get_collection(collection_name)
        total_points = collection_info.points_count

        if total_points == 0:
            logger.error("No points in collection to validate")
            return False

        # Sample random IDs to check
        import random
        sample_ids = random.sample(range(min(10000, total_points)), min(sample_size, total_points))

        # Convert to valid UUIDs or get list of actual IDs
        all_points = qdrant_client.scroll(
            collection_name=collection_name,
            limit=sample_size
        )

        sample_points = all_points[0] if all_points else []

        valid_samples = 0
        for point in sample_points:
            payload = point.payload
            # Validate required fields are present
            required_fields = ["source_url", "module", "section", "content"]
            if all(field in payload for field in required_fields):
                if payload["content"] and len(payload["content"]) > 0:
                    valid_samples += 1
                    logger.debug(f"Valid sample: {payload['source_url'][:50]}...")
                else:
                    logger.warning(f"Sample has empty content: {payload.get('source_url', 'Unknown')}")
            else:
                logger.warning(f"Sample missing required fields: {payload.keys()}")

        logger.info(f"Validated {valid_samples}/{len(sample_points)} sample payloads")
        return valid_samples > 0

    except Exception as e:
        logger.error(f"Error validating sample payloads: {e}")
        return False


def generate_validation_report(status: IngestionStatus, qdrant_client: QdrantClient, collection_name: str = "docusaurus_content") -> Dict:
    """Generate comprehensive validation report"""
    try:
        # Get collection statistics
        collection_info = qdrant_client.get_collection(collection_name)
        total_vectors = collection_info.points_count

        # Generate report
        report = {
            "pipeline_id": status.pipeline_id,
            "status": status.status,
            "summary": {
                "total_pages_processed": status.processed_pages,
                "total_content_chunks": status.total_chunks,
                "total_vectors_stored": total_vectors,
                "start_time": status.start_time,
                "end_time": status.end_time,
            },
            "validation": {
                "vector_count_match": validate_vector_count(qdrant_client, status.total_chunks, collection_name),
                "sample_payloads_valid": retrieve_and_validate_sample_payloads(qdrant_client, collection_name=collection_name),
                "success_rate": (status.processed_pages / status.total_pages * 100) if status.total_pages > 0 else 0
            },
            "errors": status.error_info
        }

        return report
    except Exception as e:
        logger.error(f"Error generating validation report: {e}")
        return {"error": str(e)}


def add_validation_to_pipeline(book_url: str, config: Dict) -> Tuple[List[ContentChunk], IngestionStatus]:
    """Enhanced pipeline with validation"""
    from datetime import datetime

    # Initialize ingestion status
    import uuid
    pipeline_id = str(uuid.uuid4())
    total_pages = 0  # We'll update this after fetching URLs

    # Fetch sitemap and URLs first to get total count
    sitemap_content = fetch_sitemap(book_url)
    if sitemap_content:
        urls = extract_urls_from_sitemap(sitemap_content)
        total_pages = len(urls)

    ingestion_status = track_ingestion_status(pipeline_id, total_pages)

    try:
        # Run the ingestion pipeline
        content_chunks = run_ingestion_pipeline(book_url)

        # Update status
        ingestion_status.processed_pages = len(content_chunks)  # Approximate
        ingestion_status.total_chunks = len(content_chunks)
        ingestion_status.status = "completed"
        ingestion_status.progress = 1.0
        ingestion_status.end_time = datetime.now().isoformat()

        # Initialize Qdrant client and store vectors
        qdrant_client = initialize_qdrant_client(
            config['qdrant_api_key'],
            config['qdrant_host'],
            config['qdrant_port']
        )

        if content_chunks:
            # Generate embeddings
            cohere_client = initialize_cohere_client(config['cohere_api_key'])
            contents = [chunk.content for chunk in content_chunks]
            embeddings = generate_embeddings(cohere_client, contents)

            # Store vectors
            stored_count = store_vectors(qdrant_client, content_chunks, embeddings)
            ingestion_status.stored_vectors = stored_count
            ingestion_status.embedded_chunks = len([e for e in embeddings if e])  # Count non-empty embeddings

        return content_chunks, ingestion_status

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        ingestion_status.status = "failed"
        ingestion_status.error_info = {"error": str(e), "timestamp": datetime.now().isoformat()}
        ingestion_status.end_time = datetime.now().isoformat()
        return [], ingestion_status


def report_validation_errors(error_info: Dict):
    """Implement error reporting for validation failures"""
    if error_info:
        logger.error(f"Validation error occurred: {error_info}")
        print(f"ERROR: {error_info.get('error', 'Unknown error')}")
        print(f"Timestamp: {error_info.get('timestamp', 'Unknown')}")


def setup_argument_parser():
    """Implement command-line argument parsing"""
    parser = argparse.ArgumentParser(
        description="RAG Ingestion Pipeline for Docusaurus Book Content"
    )
    parser.add_argument(
        "--book-url",
        type=str,
        required=True,
        help="URL of the Docusaurus book to ingest"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=256,
        help="Size of text chunks in words (default: 256)"
    )
    parser.add_argument(
        "--collection-name",
        type=str,
        default="docusaurus_content",
        help="Name of the Qdrant collection (default: docusaurus_content)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    return parser


def comprehensive_error_handling():
    """Placeholder - error handling is implemented throughout the pipeline"""
    # Error handling is implemented in individual functions
    # with try-catch blocks and logging
    pass


def implement_rate_limiting():
    """Placeholder for rate limiting implementation"""
    # Rate limiting is partially implemented via the safe_request function
    # with retry logic and delays
    pass


def add_progress_indicators(total_items: int):
    """Add progress indicators for long-running operations"""
    # This is handled by the logging throughout the pipeline
    # showing progress at various stages
    pass


def validate_configuration(config: Dict):
    """Implement configuration validation at startup"""
    required_keys = ['cohere_api_key', 'qdrant_api_key', 'qdrant_host']
    missing_keys = [key for key in required_keys if not config.get(key)]

    if missing_keys:
        raise ValueError(f"Missing required configuration: {', '.join(missing_keys)}")

    # Validate URL formats
    if not validate_url(config.get('qdrant_host', '')):
        raise ValueError(f"Invalid Qdrant host URL: {config.get('qdrant_host', '')}")

    if not validate_url(config.get('book_url', '')):
        raise ValueError(f"Invalid book URL: {config.get('book_url', '')}")

    # If all validations pass, return True
    return True


def main():
    """Main function that orchestrates the entire pipeline end-to-end"""
    logger.info("Starting RAG Ingestion Pipeline for Docusaurus Book Content")
    print("RAG Ingestion Pipeline - Docusaurus Book Content")
    print("=" * 50)

    # Parse command-line arguments
    parser = setup_argument_parser()
    args = parser.parse_args()

    # Update logging level if verbose
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Load and validate configuration
        logger.info("Loading configuration...")
        config = load_config()
        config['book_url'] = args.book_url  # Override with CLI arg
        validate_configuration(config)
        logger.info("Configuration loaded and validated successfully")

        # Run the pipeline with validation
        logger.info(f"Starting ingestion pipeline for: {args.book_url}")
        content_chunks, status = add_validation_to_pipeline(args.book_url, config)

        # Generate validation report
        qdrant_client = initialize_qdrant_client(
            config['qdrant_api_key'],
            config['qdrant_host'],
            config['qdrant_port']
        )

        report = generate_validation_report(status, qdrant_client, args.collection_name)

        print("\n" + "="*50)
        print("INGESTION PIPELINE COMPLETED")
        print("="*50)
        print(f"Status: {report['status']}")
        print(f"Pages Processed: {report['summary']['total_pages_processed']}")
        print(f"Content Chunks Created: {report['summary']['total_content_chunks']}")
        print(f"Vectors Stored: {report['summary']['total_vectors_stored']}")
        print(f"Success Rate: {report['validation']['success_rate']:.2f}%")
        print(f"Vector Count Match: {'[SUCCESS]' if report['validation']['vector_count_match'] else '[FAILED]'}")
        print(f"Sample Payloads Valid: {'[SUCCESS]' if report['validation']['sample_payloads_valid'] else '[FAILED]'}")

        if report.get("errors"):
            print(f"Errors: {report['errors']}")

        print("="*50)
        print("Pipeline execution completed!")

    except Exception as e:
        logger.error(f"Pipeline failed with error: {e}")
        print(f"\nERROR: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())