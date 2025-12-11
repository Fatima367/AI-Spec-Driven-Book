import React from 'react';
import { useLocation } from '@docusaurus/router';
import { usePluginData } from '@docusaurus/useGlobalData';
import OriginalProvider from '@theme-original/Layout';
import SkipToContent from '@theme/SkipToContent';
import AnnouncementBar from '@theme/AnnouncementBar';
import Chatbot from '../components/Chatbot/Chatbot';
import { AuthProvider } from '../contexts/AuthContext';

export default function Layout(props) {
  const { pathname } = useLocation();

  // Don't show chatbot on certain pages (like 404)
  const showChatbot = !pathname.includes('404');

  return (
    <AuthProvider>
    <OriginalProvider {...props}>
      <SkipToContent />
      <AnnouncementBar />
      <main className="main-wrapper">{props.children}</main>
      {showChatbot && <Chatbot />}
    </OriginalProvider>
    </AuthProvider>
  );
}