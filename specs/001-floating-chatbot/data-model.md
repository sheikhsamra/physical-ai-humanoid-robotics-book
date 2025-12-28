# Data Model: Floating RAG Chatbot UI

## Component State

### ChatbotUI State
- **isOpen** (boolean): Tracks whether the chat interface is currently open or closed
- **isLoading** (boolean): Tracks whether a query is currently being processed
- **messages** (array): List of message objects representing the chat history
- **inputValue** (string): Current value of the user input field

### Message Object
- **id** (string/number): Unique identifier for the message
- **content** (string): The text content of the message
- **sender** (string): Either "user" or "bot" to identify the sender
- **timestamp** (Date): When the message was created/sent

## API Request/Response Models

### Chat Request
- **query** (string): The user's query text to send to the backend
- **sessionId** (string, optional): Session identifier for conversation continuity

### Chat Response
- **content** (string): The response content from the RAG backend
- **sources** (array): List of source documents referenced in the response
- **query** (string): Echo of the original query
- **agentId** (string): Identifier of the agent that processed the request
- **timestamp** (string): ISO timestamp of the response

## UI Configuration
- **position** (object): Contains positioning properties (bottom, right) for the floating element
- **theme** (object): Theme variables for consistent styling with Docusaurus
- **apiEndpoint** (string): URL of the FastAPI chat endpoint