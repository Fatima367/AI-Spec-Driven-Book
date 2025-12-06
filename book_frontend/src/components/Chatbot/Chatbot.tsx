import React, { useState, useEffect } from 'react';
import './Chatbot.css';
import { ChatKit, useChatKit } from '@openai/chatkit-react';

const Chatbot = () => {
  const [initialThread, setInitialThread] = useState<string | null>(null);
  const [isReady, setIsReady] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(false);

  useEffect(() => {
    const savedThread = localStorage.getItem('chatkit-thread-id');
    setInitialThread(savedThread);
    setIsReady(true);
  }, []);

  const { control } = useChatKit({
    api: {
      url: 'http://localhost:8000/chatkit', // Backend ChatKit endpoint
      domainKey: 'localhost', // Required for local development
    },
    initialThread: initialThread,
    theme: {
      colorScheme: 'dark',
      color: {
        grayscale: { hue: 220, tint: 6, shade: -1 },
        accent: { primary: '#4cc9f0', level: 1 },
      },
      radius: 'round',
    },
    startScreen: {
      greeting: 'Hello! I\'m your Physical AI & Humanoid Robotics book assistant. I\'m here to help you with questions about the book content. How can I assist you today?',
      prompts: [
        { label: 'Hello', prompt: 'Say hello and introduce yourself' },
        { label: 'Help', prompt: 'What can you help me with regarding the book?' },
        { label: 'Sources', prompt: 'Can you show me sources for your answers?' },
      ],
    },
    composer: {
      placeholder: 'Ask a question about the book content...',
    },
    onThreadChange: ({ threadId }) => {
      if (threadId) localStorage.setItem('chatkit-thread-id', threadId);
    },
    onError: ({ error }) => console.error('ChatKit error:', error),
  });

  if (!isReady) return <div className="chatbot-loading">Loading...</div>;

  return (
    <div className="chatbot-container">
      {/* Floating Chat Button (bottom-right) */}
      {!isChatOpen && (
        <button
          onClick={() => setIsChatOpen(true)}
          style={{
            position: 'fixed',
            bottom: '2rem',
            right: '2rem',
            width: '60px',
            height: '60px',
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #4361ee, #4cc9f0)',
            border: 'none',
            cursor: 'pointer',
            boxShadow: '0 4px 20px rgba(76, 201, 240, 0.4)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 100,
            fontSize: '24px'
          }}
        >
          <span role="img" aria-label="chat">💬</span>
        </button>
      )}

      {/* Chat Popup (bottom-right) */}
      {isChatOpen && (
        <>
          {/* Backdrop */}
          <div
            onClick={() => setIsChatOpen(false)}
            style={{
              position: 'fixed',
              inset: 0,
              background: 'rgba(0, 0, 0, 0.3)',
              zIndex: 999
            }}
          />

          {/* Popup Window */}
          <div style={{
            position: 'fixed',
            bottom: '2rem',
            right: '2rem',
            width: '420px',
            height: '600px',
            maxWidth: 'calc(100vw - 4rem)',
            maxHeight: 'calc(100vh - 4rem)',
            background: '#16213e',
            borderRadius: '1rem',
            boxShadow: '0 10px 50px rgba(0, 0, 0, 0.5)',
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden',
            zIndex: 1000,
          }}>
            {/* Header */}
            <div style={{
              padding: '1rem',
              background: '#0f3460',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}>
              <span style={{ color: '#4cc9f0', fontWeight: 'bold' }}>Book Assistant</span>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button
                  onClick={() => { localStorage.removeItem('chatkit-thread-id'); window.location.reload() }}
                  style={{ padding: '0.4rem 0.6rem', background: '#4361ee', color: 'white', border: 'none', borderRadius: '0.375rem', cursor: 'pointer', fontSize: '0.7rem' }}
                >
                  New Chat
                </button>
                <button
                  onClick={() => setIsChatOpen(false)}
                  style={{ padding: '0.4rem', background: 'transparent', color: '#a0a0a0', border: '1px solid #a0a0a0', borderRadius: '0.375rem', cursor: 'pointer' }}
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </button>
              </div>
            </div>

            {/* Chat Content */}
            <div style={{ flex: 1, overflow: 'hidden' }}>
              <ChatKit control={control} className="h-full w-full" />
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Chatbot;