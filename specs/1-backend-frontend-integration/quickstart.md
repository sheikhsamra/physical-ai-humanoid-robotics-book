# Quickstart Guide: Backend–Frontend Integration for RAG Chatbot

**Created**: 2025-12-27
**Feature**: 1-backend-frontend-integration

## Overview

This guide will help you quickly set up and run the integrated backend-frontend system for the RAG chatbot.

## Prerequisites

- Python 3.8+
- Node.js 16+
- Access to Qdrant vector database
- Cohere API key
- Groq API key

## Backend Setup

### 1. Install Dependencies

```bash
pip install fastapi uvicorn python-dotenv openai-agents groq cohere qdrant-client
```

### 2. Set Environment Variables

Create a `.env` file with the following variables:

```env
GROQ_API_KEY=your_groq_api_key
COHERE_API_KEY=your_cohere_api_key
QDRANT_HOST=your_qdrant_host
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=docusaurus_content
GROQ_MODEL=llama-3.1-8b-instant
```

### 3. Run the Backend Server

```bash
# Navigate to backend directory
cd backend

# Run the FastAPI server
uvicorn api:app --reload --port 8000
```

The server will be available at `http://localhost:8000`

## Frontend Setup

### 1. Navigate to Docusaurus Directory

```bash
cd my-book
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Run the Docusaurus Development Server

```bash
npm run start
```

The frontend will be available at `http://localhost:3000`

## Testing the Integration

### 1. Test the API Endpoint

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is Physical AI?"
  }'
```

### 2. Test via Frontend

1. Open your browser to `http://localhost:3000`
2. Use the integrated chat UI to ask questions
3. Verify responses appear correctly

## Frontend Integration Instructions

### Chat Component

The chat UI component is located at `my-book/src/components/Chatbot.jsx` and is integrated into the Docusaurus layout via `my-book/src/pages/index.js`.

The component handles:
- Query submission to the backend API
- Loading state display
- Error handling and display
- Response formatting with source attribution
- Responsive design that matches the Docusaurus theme

### API Connection

The frontend connects to the backend API at `http://localhost:8000/chat` using standard fetch API calls. CORS is configured to allow requests from the Docusaurus development server.

## API Usage Examples

### Query Request

```json
{
  "query": "What are the main components of a humanoid robot?",
  "sessionId": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Response Format

```json
{
  "content": "The main components of a humanoid robot include...",
  "sources": [
    {
      "id": "doc-001",
      "content": "Physical AI represents a paradigm shift...",
      "source_url": "https://example.com/book/components",
      "module": "robotics",
      "section": "components",
      "score": 0.87
    }
  ],
  "query": "What are the main components of a humanoid robot?",
  "agentId": "rag-agent-1",
  "timestamp": "2025-12-27T10:00:00Z"
}
```

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Verify environment variables are set correctly
   - Check that Qdrant database is accessible
   - Confirm API keys are valid

2. **CORS Issues**
   - Ensure the backend allows requests from the frontend origin
   - Check that both services are properly configured

3. **Agent Response Timeouts**
   - Verify Groq API is accessible
   - Check that the agent is properly initialized

4. **Frontend-Backend Connection**
   - Verify the backend server is running on port 8000
   - Check that the frontend is making requests to the correct API endpoint
   - Ensure the API endpoint is properly configured for CORS