# API Contract: Floating Chatbot UI Integration

## Overview

This document defines the API contract between the floating chatbot UI component and the backend services.

## Backend API Integration

### Chat Endpoint
- **Method**: POST
- **URL**: `/chat` (relative to backend base URL)
- **Description**: Send user queries to the RAG backend and receive contextual responses

#### Request
```json
{
  "query": "string (required)",
  "sessionId": "string (optional)"
}
```

**Headers**:
- `Content-Type`: `application/json`

#### Response
**Success (200 OK)**:
```json
{
  "content": "string",
  "sources": [
    {
      "id": "string",
      "content": "string",
      "source_url": "string",
      "module": "string",
      "section": "string",
      "score": "number"
    }
  ],
  "query": "string",
  "agentId": "string",
  "timestamp": "string (ISO 8601 format)"
}
```

**Error (400, 429, 500)**:
```json
{
  "error": "string",
  "code": "string",
  "details": "object (optional)",
  "timestamp": "string (ISO 8601 format)"
}
```

### Health Check Endpoint
- **Method**: GET
- **URL**: `/health` (relative to backend base URL)
- **Description**: Check the health status of the backend API

#### Response
**Success (200 OK)**:
```json
{
  "status": "healthy"
}
```

## Frontend Component API

### Component Props
The FloatingChatbot component accepts the following properties:

- **apiEndpoint** (string, optional): The URL of the backend chat API
  - Default: `http://localhost:8000/chat`
- **initialOpen** (boolean, optional): Whether the chat interface should start open
  - Default: `false`
- **theme** (object, optional): Theme configuration object to match Docusaurus styling
  - Default: Uses Docusaurus CSS variables

### Component Events
The component may emit the following events:

- **onQuerySubmit**: Triggered when a user submits a query
- **onResponseReceived**: Triggered when a response is received from the backend
- **onError**: Triggered when an error occurs during query processing

## Error Handling

### Client-Side Errors
- Network errors during API communication
- Invalid input validation errors
- Component rendering errors

### Server-Side Errors
- 400: Bad request (malformed query)
- 429: Rate limiting exceeded
- 500: Internal server error
- 503: Service unavailable