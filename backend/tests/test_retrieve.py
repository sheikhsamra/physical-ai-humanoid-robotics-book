"""
Unit tests for the RAG retrieval system
"""
import unittest
import os
import sys
from unittest.mock import Mock, patch
from backend.retrieve import (
    QdrantConnectionConfig,
    Query,
    SearchResult,
    ValidationResult,
    ValidationReport,
    setup_cohere_client,
    connect_to_qdrant,
    generate_query_embedding,
    perform_similarity_search,
    map_to_search_result,
    process_sample_query,
    validate_content_relevance,
    validate_metadata_accuracy,
    generate_validation_result,
    generate_validation_report,
    rank_results_by_relevance,
    handle_qdrant_connection_errors,
    handle_no_results_query
)


class TestQdrantConnectionConfig(unittest.TestCase):
    """Test QdrantConnectionConfig dataclass"""

    def setUp(self):
        # Save original environment variables
        self.original_env = {
            'QDRANT_API_KEY': os.environ.get('QDRANT_API_KEY'),
            'QDRANT_HOST': os.environ.get('QDRANT_HOST'),
            'QDRANT_COLLECTION_NAME': os.environ.get('QDRANT_COLLECTION_NAME')
        }

    def tearDown(self):
        # Restore original environment variables
        for key, value in self.original_env.items():
            if value is not None:
                os.environ[key] = value
            elif key in os.environ:
                del os.environ[key]

    def test_config_creation_with_env_vars(self):
        """Test creating QdrantConnectionConfig with environment variables"""
        os.environ['QDRANT_API_KEY'] = 'test_key'
        os.environ['QDRANT_HOST'] = 'https://test.qdrant.com'
        os.environ['QDRANT_COLLECTION_NAME'] = 'test_collection'

        config = QdrantConnectionConfig()
        self.assertEqual(config.api_key, 'test_key')
        self.assertEqual(config.host, 'https://test.qdrant.com')
        self.assertEqual(config.collection_name, 'test_collection')

    def test_config_validation(self):
        """Test validation of QdrantConnectionConfig"""
        with self.assertRaises(ValueError):
            QdrantConnectionConfig(api_key='', host='https://test.com')


class TestQuery(unittest.TestCase):
    """Test Query dataclass"""

    def test_query_creation(self):
        """Test creating a Query object"""
        query = Query(text="Test query")
        self.assertEqual(query.text, "Test query")
        self.assertIsNotNone(query.id)
        self.assertIsNotNone(query.created_at)

    def test_query_validation(self):
        """Test validation of Query object"""
        with self.assertRaises(ValueError):
            Query(text="")


class TestSearchResult(unittest.TestCase):
    """Test SearchResult dataclass"""

    def test_search_result_creation(self):
        """Test creating a SearchResult object"""
        result = SearchResult(
            id="1",
            score=0.8,
            content="Test content",
            source_url="https://example.com",
            module="test_module",
            section="test_section"
        )
        self.assertEqual(result.id, "1")
        self.assertEqual(result.score, 0.8)
        self.assertEqual(result.content, "Test content")
        self.assertEqual(result.source_url, "https://example.com")
        self.assertEqual(result.module, "test_module")
        self.assertEqual(result.section, "test_section")

    def test_search_result_validation(self):
        """Test validation of SearchResult object"""
        with self.assertRaises(ValueError):
            SearchResult(
                id="1",
                score=1.5,  # Invalid score
                content="Test content",
                source_url="https://example.com",
                module="test_module",
                section="test_section"
            )


class TestValidationResult(unittest.TestCase):
    """Test ValidationResult dataclass"""

    def test_validation_result_creation(self):
        """Test creating a ValidationResult object"""
        search_result = SearchResult(
            id="1",
            score=0.8,
            content="Test content",
            source_url="https://example.com",
            module="test_module",
            section="test_section"
        )

        validation_result = ValidationResult(
            query_id="test_id",
            search_results=[search_result],
            relevance_score=0.8,
            metadata_accuracy=0.9,
            content_relevance=0.85,
            is_valid=True,
            threshold_used=0.7
        )

        self.assertEqual(validation_result.query_id, "test_id")
        self.assertEqual(len(validation_result.search_results), 1)
        self.assertEqual(validation_result.relevance_score, 0.8)


class TestValidationReport(unittest.TestCase):
    """Test ValidationReport dataclass"""

    def test_validation_report_creation(self):
        """Test creating a ValidationReport object"""
        search_result = SearchResult(
            id="1",
            score=0.8,
            content="Test content",
            source_url="https://example.com",
            module="test_module",
            section="test_section"
        )

        validation_result = ValidationResult(
            query_id="test_id",
            search_results=[search_result],
            relevance_score=0.8,
            metadata_accuracy=0.9,
            content_relevance=0.85,
            is_valid=True,
            threshold_used=0.7
        )

        report = ValidationReport(
            query_text="Test query",
            total_results=1,
            valid_results=1,
            success_rate=1.0,
            avg_similarity=0.8,
            metadata_accuracy_rate=0.9,
            validation_results=[validation_result],
            execution_time=0.5
        )

        self.assertEqual(report.query_text, "Test query")
        self.assertEqual(report.total_results, 1)


class TestValidationFunctions(unittest.TestCase):
    """Test validation functions"""

    def test_content_relevance_validation(self):
        """Test content relevance validation"""
        search_result = SearchResult(
            id="1",
            score=0.8,
            content="Test content",
            source_url="https://example.com",
            module="test_module",
            section="test_section"
        )

        relevance = validate_content_relevance([search_result], "test query")
        self.assertEqual(relevance, 0.8)

    def test_metadata_accuracy_validation(self):
        """Test metadata accuracy validation"""
        search_result = SearchResult(
            id="1",
            score=0.8,
            content="Test content",
            source_url="https://example.com",
            module="test_module",
            section="test_section"
        )

        accuracy = validate_metadata_accuracy([search_result])
        self.assertEqual(accuracy, 1.0)

    def test_ranking_by_relevance(self):
        """Test ranking results by relevance"""
        result1 = SearchResult(
            id="1",
            score=0.5,
            content="Test content 1",
            source_url="https://example.com",
            module="test_module",
            section="test_section"
        )

        result2 = SearchResult(
            id="2",
            score=0.8,
            content="Test content 2",
            source_url="https://example.com",
            module="test_module",
            section="test_section"
        )

        results = [result1, result2]
        ranked = rank_results_by_relevance(results)

        # Should be ranked by score in descending order
        self.assertEqual(ranked[0].score, 0.8)
        self.assertEqual(ranked[1].score, 0.5)


class TestNoResultsHandling(unittest.TestCase):
    """Test handling of queries with no results"""

    def test_no_results_handling(self):
        """Test handling of queries that return no results"""
        results = handle_no_results_query("test query", [])
        self.assertEqual(results, [])


if __name__ == '__main__':
    unittest.main()