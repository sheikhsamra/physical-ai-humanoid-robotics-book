"""
Mock Agent Service for API Integration

This module provides a mock service layer that returns quick responses when the real agent is unavailable.
It simulates the RAG agent functionality with predefined responses for common queries.
"""
import logging
import time
from typing import Optional
from datetime import datetime

from ..models.agent_response import AgentResponse
from ..models.source import Source as SourceModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockAgentService:
    """
    Mock service class to handle agent functionality when real agent is unavailable
    """

    def __init__(self):
        self.responses = {
            "what is physical ai": "Physical AI is a field that bridges artificial intelligence with embodied systems, enabling intelligent algorithms to interact with the real world in meaningful ways. It represents a paradigm shift toward intelligence that is embodied, situated, and grounded in physical reality, recognizing that true intelligence emerges from the interaction between an agent and its environment.",

            "humanoid robot": "A humanoid robot is a robot with a human-like body structure, typically featuring a head, torso, two arms, and two legs. These robots are designed to mimic human appearance and behavior, making them ideal for human-robot interaction in various applications.",

            "ai robotics": "AI robotics combines artificial intelligence with robotics to create machines capable of performing tasks that require intelligence. This includes perception, decision-making, learning, and adaptation to dynamic environments.",

            "machine learning": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It focuses on developing algorithms that can access data and use it to learn for themselves.",

            "deep learning": "Deep learning is a subset of machine learning based on artificial neural networks with multiple layers. It enables computers to recognize patterns and make predictions based on large amounts of data.",

            "neural network": "A neural network is a series of algorithms that endeavors to recognize underlying relationships in a set of data through a process that mimics the way the human brain operates.",

            "computer vision": "Computer vision is an interdisciplinary scientific field that deals with how computers can gain high-level understanding from digital images or videos.",

            "natural language processing": "Natural Language Processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language.",

            "reinforcement learning": "Reinforcement learning is an area of machine learning concerned with how intelligent agents ought to take actions in an environment to maximize the notion of cumulative reward.",

            "embodied ai": "Embodied AI refers to artificial intelligence systems that interact with the physical world through a body or robot, learning from physical experiences and sensorimotor interactions.",

            "robotics": "Robotics is an interdisciplinary branch of engineering and science that includes mechanical engineering, electrical engineering, computer science, and others. It deals with the design, construction, operation, and use of robots, as well as computer systems for their control, sensory feedback, and information processing.",
        }

    def query_agent(self, query_text: str) -> AgentResponse:
        """
        Query the mock agent and return a formatted response

        Args:
            query_text: The user's query

        Returns:
            AgentResponse: Formatted response with content, sources, and metadata
        """
        start_time = time.time()
        logger.info(f"Processing query through mock agent service: '{query_text[:50]}{'...' if len(query_text) > 50 else ''}'")

        # Normalize the query for matching
        normalized_query = query_text.lower().strip()

        # Look for matching responses
        response_content = "I'm sorry, I don't have specific information about that topic in my knowledge base. However, I can provide general information about Physical AI and Humanoid Robotics. Physical AI represents a paradigm shift toward intelligence that is embodied in physical systems, such as humanoid robots, to create intelligent agents that can interact with the real world in meaningful ways. Humanoid robotics serves as a compelling platform for Physical AI research, as human-like form factors provide natural interfaces for human-robot interaction and complex sensorimotor challenges that drive innovation in AI algorithms."

        # Check for exact matches first
        for key, value in self.responses.items():
            if key in normalized_query:
                response_content = value
                break

        # Check for partial matches
        if response_content.startswith("I'm sorry"):
            for key, value in self.responses.items():
                if any(word in normalized_query for word in key.split()):
                    response_content = value
                    break

        # Create and return the formatted response
        formatted_response = AgentResponse(
            content=response_content,
            sources=[
                SourceModel(
                    id="mock-source-1",
                    content="Physical AI and Humanoid Robotics book content",
                    source_url="https://physical-ai-humanoid-robotics-book-sandy.vercel.app/",
                    module="Introduction",
                    section="Overview",
                    score=0.8
                )
            ],
            query=query_text,
            agentId="mock-rag-agent",
        )

        processing_time = time.time() - start_time
        logger.info(f"Processed query through mock agent service in {processing_time:.2f}s")
        return formatted_response

    def health_check(self) -> bool:
        """
        Check if the mock agent service is healthy and operational

        Returns:
            bool: True if the service is operational, False otherwise
        """
        try:
            # Perform a simple test
            test_response = self.query_agent("Hello")
            return bool(test_response and len(test_response.content) > 0)
        except Exception as e:
            logger.error(f"Mock agent health check failed: {str(e)}")
            return False

# Global mock agent service instance
mock_agent_service = MockAgentService()

def get_mock_agent_service() -> MockAgentService:
    """
    Get the global mock agent service instance

    Returns:
        MockAgentService: The global mock agent service instance
    """
    return mock_agent_service