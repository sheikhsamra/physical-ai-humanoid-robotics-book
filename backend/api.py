from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import logging

# Import the models
try:
    # When running as a module within the package
    from .models.query_request import QueryRequest
    from .models.agent_response import AgentResponse
    from .models.error_response import ErrorResponse
    from .services.agent_service import agent_service
    from .services.rate_limiter import rate_limiter
except ImportError:
    # When running directly as a script
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from backend.models.query_request import QueryRequest
    from backend.models.agent_response import AgentResponse
    from backend.models.error_response import ErrorResponse
    from backend.services.agent_service import agent_service
    from backend.services.rate_limiter import rate_limiter

app = FastAPI(
    title="RAG Chatbot API",
    description="API for interacting with the RAG agent in the Physical AI and Humanoid Robotics book",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:8000", "http://localhost:3002"],  # Docusaurus dev server and API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose headers that the frontend can read
    expose_headers=["Access-Control-Allow-Origin"]
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
def read_root():
    return {"message": "RAG Chatbot API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/chat", response_model=AgentResponse)
def chat_endpoint(request: QueryRequest):
    """
    Chat endpoint that accepts user queries and returns agent responses.
    """
    logger.info(f"Received query: {request.query}")

    # Rate limiting check (using a simple IP-based identifier for now)
    client_ip = "default_client"  # In a real implementation, you'd extract the actual client IP
    if not rate_limiter.is_allowed(client_ip):
        error_response = ErrorResponse(
            error="Rate limit exceeded. Please try again later.",
            code="RATE_LIMIT_EXCEEDED",
            details={
                "message": "Too many requests from this IP address",
                "retry_after": rate_limiter.get_reset_time(client_ip)
            }
        )
        raise HTTPException(status_code=429, detail=error_response.model_dump())

    try:
        # Validate the query is not empty after stripping whitespace
        if not request.query or not request.query.strip():
            error_response = ErrorResponse(
                error="Query cannot be empty",
                code="EMPTY_QUERY",
                details={"message": "The query field is required and cannot be empty"}
            )
            raise HTTPException(status_code=400, detail=error_response.model_dump())

        # Use the agent service to process the query with fallback for knowledge base unavailability
        agent_response = agent_service.query_agent_with_fallback(request.query)
        return agent_response
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        error_response = ErrorResponse(
            error="An error occurred while processing your query",
            code="PROCESSING_ERROR",
            details={"message": str(e)},
        )
        raise HTTPException(status_code=500, detail=error_response.model_dump())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)