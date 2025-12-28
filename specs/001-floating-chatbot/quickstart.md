# Quickstart Guide: Floating RAG Chatbot UI for Docusaurus Book

## Overview

This guide will help you quickly set up and run the floating RAG chatbot UI component for the Docusaurus book.

## Prerequisites

- Node.js 16+ (for Docusaurus)
- npm or yarn package manager
- Access to the existing FastAPI RAG backend
- Running backend server at the configured endpoint

## Setup Instructions

### 1. Install the Floating Chatbot Component

The floating chatbot component is integrated directly into the Docusaurus site:

1. The component is located at `my-book/src/components/FloatingChatbot.jsx`
2. The styling is located at `my-book/src/components/FloatingChatbot.css`
3. The component is integrated globally via `my-book/src/theme/Root.js` to appear on all pages

### 2. Configure API Endpoint

The chatbot connects to the existing FastAPI RAG backend. Ensure the API endpoint is properly configured:

```javascript
// In FloatingChatbot.jsx, update the API endpoint if needed
const API_ENDPOINT = process.env.REACT_APP_CHAT_API_URL || 'http://localhost:8000/chat';
```

### 3. Run the Docusaurus Development Server

1. Navigate to the my-book directory:
   ```bash
   cd my-book
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run start
   ```

The Docusaurus site will be available at `http://localhost:3000` with the floating chatbot component visible on all pages.

## Usage

1. Visit any page in the Docusaurus book
2. Locate the floating chatbot icon in the bottom-right corner
3. Click the icon to open the chat interface
4. Type your question about the book content in the input field
5. Submit your query to receive a response from the RAG backend
6. Click the icon again or the close button to hide the chat interface

## Testing the Integration

### 1. Test Component Visibility
- Verify the floating icon appears on all pages
- Confirm the icon remains visible during scrolling
- Check that the icon is positioned in the bottom-right corner

### 2. Test UI Functionality
- Click the icon to open the chat interface
- Verify the UI overlays content without shifting layout
- Test that the input field is functional
- Submit a test query and verify response display

### 3. Test API Connection
- Submit a query about book content
- Verify that responses are received from the backend
- Test error handling when the backend is unavailable

## Troubleshooting

### Common Issues

1. **Floating icon not visible**
   - Verify the component is properly integrated into the layout
   - Check that the component file exists and has no syntax errors

2. **API connection errors**
   - Confirm the backend server is running
   - Verify the API endpoint URL is correctly configured
   - Check that CORS is properly configured on the backend

3. **Styling inconsistencies**
   - Ensure CSS properly imports and applies Docusaurus theme variables
   - Verify that component styles don't conflict with existing styles

4. **Performance issues**
   - Check that the component doesn't block the main thread
   - Verify that initial load impact is minimal