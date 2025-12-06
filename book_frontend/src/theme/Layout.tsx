import React from 'react';
import { useLocation } from '@docusaurus/router';
import { usePluginData } from '@docusaurus/useGlobalData';
import OriginalLayout from '@theme-original/Layout';
import SkipToContent from '@theme/SkipToContent';
import AnnouncementBar from '@theme/AnnouncementBar';
import Navbar from '@theme/Navbar';
import Footer from '@theme/Footer';
import Chatbot from '../components/Chatbot/Chatbot';

export default function Layout(props) {
  const { pathname } = useLocation();

  // Don't show chatbot on certain pages (like 404)
  const showChatbot = !pathname.includes('404');

  return (
    <OriginalLayout {...props}>
      <SkipToContent />
      <AnnouncementBar />
      <main className="main-wrapper">{props.children}</main>
      {showChatbot && <Chatbot />}
    </OriginalLayout>
  );
}