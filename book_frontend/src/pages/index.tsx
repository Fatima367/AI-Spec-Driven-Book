import React from 'react';
import Layout from '@theme/Layout';
import GlassmorphismCard from '../components/BookLanding/GlassmorphismCard';
import BackgroundSpheres from '../components/BookLanding/BackgroundSpheres';
import NavigationLinks from '../components/BookLanding/NavigationLinks';
import CTAButton from '../components/BookLanding/CTAButton';
import Chatbot from '../components/Chatbot/Chatbot';

/**
 * The main landing page for the book
 * Implements the glassmorphism aesthetic with background spheres
 */
const Home = () => {
  return (
    <Layout title="Physical AI & Humanoid Robotics" description="A book about the intersection of physical AI and humanoid robotics">
      <div style={{ position: 'relative', minHeight: '100vh', overflow: 'hidden' }}>
        {/* Background Spheres */}
        <BackgroundSpheres />

        {/* Main Content */}
        <div style={{
          position: 'relative',
          zIndex: 2,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '100vh',
          padding: '20px'
        }}>
          <GlassmorphismCard />
        </div>

        {/* Chatbot */}
        <Chatbot />
      </div>
    </Layout>
  );
};

export default Home;
