"""
Unit tests for the RAG Agent with Retrieval Integration
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import os
from agent import (
    RAGAgent, RetrievalTool, Source, AgentResponse, ValidationResult,
    create_rag_agent_with_openai_sdk, validate_agent_response, create_sample_book_related_queries,
    format_human_readable_agent_output
)


class TestAgentDataModels(unittest.TestCase):
    """Test the core data models"""

    def test_rag_agent_creation(self):
        """Test creating a RAGAgent instance"""
        agent = RAGAgent()
        self.assertIsNotNone(agent.id)
        self.assertEqual(agent.model, os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant'))
        self.assertIn("helpful assistant", agent.instructions.lower())
        self.assertIsInstance(agent.tools, list)
        self.assertIsNotNone(agent.created_at)

    def test_retrieval_tool_creation(self):
        """Test creating a RetrievalTool instance"""
        tool = RetrievalTool()
        self.assertEqual(tool.name, "retrieve_content")
        self.assertIn("knowledge base", tool.description)
        self.assertIsInstance(tool.parameters, dict)
        self.assertIsNone(tool.function)

    def test_source_creation(self):
        """Test creating a Source instance"""
        source = Source(
            id="test-id",
            content="test content",
            source_url="https://example.com",
            module="test_module",
            section="test_section",
            score=0.8
        )
        self.assertEqual(source.id, "test-id")
        self.assertEqual(source.content, "test content")
        self.assertEqual(source.source_url, "https://example.com")
        self.assertEqual(source.module, "test_module")
        self.assertEqual(source.section, "test_section")
        self.assertEqual(source.score, 0.8)

    def test_agent_response_creation(self):
        """Test creating an AgentResponse instance"""
        import uuid
        test_agent_id = str(uuid.uuid4())
        source = Source(
            id="test-id",
            content="test content",
            source_url="https://example.com",
            module="test_module",
            section="test_section",
            score=0.8
        )
        response = AgentResponse(
            content="test response",
            sources=[source],
            query="test query",
            agent_id=test_agent_id
        )
        self.assertEqual(response.content, "test response")
        self.assertEqual(len(response.sources), 1)
        self.assertEqual(response.query, "test query")
        self.assertEqual(response.agent_id, test_agent_id)

    def test_validation_result_creation(self):
        """Test creating a ValidationResult instance"""
        validation = ValidationResult(
            response_id="test-response-id",
            is_grounded=True,
            grounding_score=0.8,
            metadata_accuracy=0.9
        )
        self.assertEqual(validation.response_id, "test-response-id")
        self.assertTrue(validation.is_grounded)
        self.assertEqual(validation.grounding_score, 0.8)
        self.assertEqual(validation.metadata_accuracy, 0.9)
        self.assertTrue(validation.is_valid)  # Should be valid based on thresholds


class TestAgentFunctions(unittest.TestCase):
    """Test the agent functions"""

    @patch('agent.OpenAIAgent')
    def test_create_rag_agent_with_openai_sdk(self, mock_openai_agent):
        """Test creating a RAG agent with OpenAI SDK"""
        # Mock the OpenAI Agent
        mock_agent_instance = Mock()
        mock_openai_agent.return_value = mock_agent_instance

        agent = create_rag_agent_with_openai_sdk()
        self.assertIsNotNone(agent)

    def test_validate_agent_response(self):
        """Test validating an agent response"""
        response_text = "This is a test response from the agent."

        validation_result = validate_agent_response(response_text)
        self.assertIsInstance(validation_result, ValidationResult)
        self.assertTrue(validation_result.is_valid)

    def test_create_sample_book_related_queries(self):
        """Test creating sample book-related queries"""
        queries = create_sample_book_related_queries()
        self.assertIsInstance(queries, list)
        self.assertGreater(len(queries), 0)
        self.assertIn("Physical AI", queries[0])

    def test_format_human_readable_agent_output(self):
        """Test formatting an agent response"""
        response_text = "This is a test response."

        formatted = format_human_readable_agent_output(response_text)
        self.assertIn("RAG Agent Response", formatted)
        self.assertIn("This is a test response.", formatted)
        self.assertIn("=" * 70, formatted)


class TestIntegration(unittest.TestCase):
    """Test integration between components"""

    @patch('agent.OpenAIAgent')
    def test_agent_creation_with_openai_sdk(self, mock_openai_agent):
        """Test the agent creation with OpenAI SDK"""
        # Setup mock
        mock_agent_instance = Mock()
        mock_agent_instance.name = "RAG Agent"
        mock_openai_agent.return_value = mock_agent_instance

        # Test that the agent can be created
        agent = create_rag_agent_with_openai_sdk()
        self.assertIsNotNone(agent)


if __name__ == '__main__':
    unittest.main()