import React, { useState, useRef, useEffect } from 'react';
import './FloatingChatbot.css';

const FloatingChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the backend API
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: inputValue }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const botMessage = {
        id: Date.now() + 1,
        content: data.content,
        sender: 'bot',
        timestamp: new Date(),
        sources: data.sources || [],
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      console.error('Error fetching response:', err);
      const errorMessage = {
        id: Date.now() + 1,
        content: `Sorry, I encountered an error: ${err.message}`,
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatSources = (sources) => {
    if (!sources || sources.length === 0) return null;

    return (
      <div className="sources">
        <h4>Sources:</h4>
        <ul>
          {sources.map((source, index) => (
            <li key={index}>
              <a href={source.source_url} target="_blank" rel="noopener noreferrer">
                {source.module} - {source.section}
              </a>
            </li>
          ))}
        </ul>
      </div>
    );
  };

  return (
    <div className="floating-chatbot">
      {/* Floating Icon */}
      {!isOpen && (
        <div
          className="floating-chatbot-icon"
          onClick={() => setIsOpen(true)}
          title="Open Chat"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 8C21 5.23858 16.7614 3 12 3C7.23858 3 3 5.23858 3 8C3 10.7614 5.76142 13 12 13C13.8604 13 15.5786 12.633 17.0064 12.0329C17.386 12.5001 17.8647 12.8976 18.4089 13.2179C18.6887 13.3843 19 13.281 19 12.9671V9.5C19 8.11929 20.1193 7 21.5 7C21.8041 7 22 7.19589 22 7.5C22 7.80411 21.8041 8 21 8Z" fill="currentColor"/>
            <path d="M12 15C7.23858 15 3 17.2386 3 20C3 20.5523 3.44772 21 4 21H20C20.5523 21 21 20.5523 21 20C21 17.2386 16.7614 15 12 15Z" fill="currentColor"/>
          </svg>
        </div>
      )}

      {/* Chat Interface */}
      {isOpen && (
        <div className="floating-chatbot-container">
          <div className="floating-chatbot-header">
            <h3>Physical AI Assistant</h3>
            <button
              className="close-button"
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
            >
              ×
            </button>
          </div>

          <div className="floating-chatbot-messages">
            {messages.length === 0 ? (
              <div className="welcome-message">
                <p>Hello! I'm your assistant for the Physical AI and Humanoid Robotics book. Ask me anything about the content!</p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`message ${message.sender}-message`}
                >
                  <div className="message-content">{message.content}</div>
                  {message.sender === 'bot' && message.sources && formatSources(message.sources)}
                </div>
              ))
            )}
            {isLoading && (
              <div className="message bot-message">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSubmit} className="floating-chatbot-input-form">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask a question about Physical AI or Humanoid Robotics..."
              disabled={isLoading}
              className="floating-chatbot-input"
            />
            <button type="submit" disabled={isLoading || !inputValue.trim()} className="floating-chatbot-send-button">
              {isLoading ? '...' : '→'}
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default FloatingChatbot;