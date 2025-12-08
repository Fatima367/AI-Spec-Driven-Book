import React, { useState, useEffect, useRef } from 'react';
import './Chatbot.css';
import { selectionService } from '../../services/selection_service'; // Import the selectionService
import { FaCommentAlt, FaTimes, FaPaperPlane, FaRobot } from 'react-icons/fa'; // Import icons

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { id: Date.now(), text: inputValue, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    // Get selected text from the selectionService
    const currentSelectedText = selectionService.getSelectedText();

    try {
      // Call the backend API to get chat response
      const response = await fetch('https://ai-spec-driven-book-production.up.railway.app/api/v1/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: inputValue,
          user_id: 'anonymous-user',
          selected_text: currentSelectedText // Use selected text from service
        }),
      });

      const data = await response.json();

      if (response.ok) {
        const botMessage = {
          id: Date.now() + 1,
          text: data.answer,
          sender: 'bot',
          citations: data.citations || []
        };
        setMessages(prev => [...prev, botMessage]);
      } else {
        const errorMessage = {
          id: Date.now() + 1,
          text: 'Sorry, I encountered an error processing your request. Please try again.',
          sender: 'bot'
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I\'m having trouble connecting to the server. Please try again later.',
        sender: 'bot'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="chatbot-container">
      {isOpen ? (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <FaRobot color="#00E0FF" />
              <h3>Book Assistant</h3>
            </div>
            <button className="chatbot-close" onClick={toggleChat}>
              <FaTimes />
            </button>
          </div>
          <div className="chatbot-messages">
            {messages.length === 0 ? (
              <div className="chatbot-welcome">
                <p>Hello! I'm your book assistant. Ask me anything about the content of this book, and I'll help you find the information you need.</p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`chatbot-message ${
                    message.sender === 'user' ? 'user-message' : 'bot-message'
                  }`}
                >
                  <div className="message-content">
                    {message.text}
                  </div>
                  {message.sender === 'bot' && message.citations && message.citations.length > 0 && (
                    <div className="citations">
                      <p>Sources:</p>
                      <ul>
                        {message.citations.map((citation, index) => (
                          <li key={index}>
                            <a href={citation.url} target="_blank" rel="noopener noreferrer">
                              {citation.doc_id || `Source ${index + 1}`}
                            </a>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))
            )}
            {isLoading && (
              <div className="chatbot-message bot-message">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <div className="chatbot-input-area">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask a question about the book content..."
              className="chatbot-input"
              rows="1"
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isLoading}
              className="chatbot-send-button"
            >
              <FaPaperPlane />
            </button>
          </div>
        </div>
      ) : (
        <button className="chatbot-button" onClick={toggleChat}>
          <span>Ask AI</span>
          <FaRobot style={{ marginLeft: '6px', fontSize: '0.9em' }} />
        </button>
      )}
    </div>
  );
};

export default Chatbot;