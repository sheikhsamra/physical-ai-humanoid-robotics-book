import React from 'react';
import FloatingChatbot from '../components/FloatingChatbot';

// Custom Root component to add the floating chatbot to all pages
function Root({children}) {
  return (
    <>
      {children}
      <FloatingChatbot />
    </>
  );
}

export default Root;