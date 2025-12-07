import React from 'react';
import Layout from '@theme/Layout';
import GlassmorphismCard from '../components/BookLanding/GlassmorphismCard';
import BackgroundSpheres from '../components/BookLanding/BackgroundSpheres';
import Chatbot from '../components/Chatbot/Chatbot';
import './BookLandingPage.css';

/**
 * The main landing page for the book
 * Implements the glassmorphism aesthetic with background spheres
 */
const BookLandingPage = () => {
  // Features data
  const features = [
    {
      title: "ROS 2 Mastery",
      description: "Learn the middleware that enables robot control with ROS 2 Nodes, Topics, and Services",
      icon: "🤖"
    },
    {
      title: "Digital Twin Simulation",
      description: "Explore physics simulation and environment building with Gazebo and Unity",
      icon: "🎮"
    },
    {
      title: "AI-Robot Brain",
      description: "Dive into advanced perception and training with NVIDIA Isaac platform",
      icon: "🧠"
    },
    {
      title: "Vision-Language-Action",
      description: "Implement voice-to-action systems using VLA models and cognitive planning",
      icon: "👁️"
    }
  ];

  // Modules data
  const modules = [
    {
      title: "Module 1: The Robotic Nervous System (ROS 2)",
      description: "Master ROS 2 for robotic control and communication, bridging Python Agents to ROS controllers."
    },
    {
      title: "Module 2: The Digital Twin (Gazebo & Unity)",
      description: "Explore physics simulation with gravity, collisions, and sensors like LiDAR and depth cameras."
    },
    {
      title: "Module 3: The AI-Robot Brain (NVIDIA Isaac)",
      description: "Dive into advanced perception with Isaac Sim, Isaac ROS, and Nav2 for path planning."
    },
    {
      title: "Module 4: Vision-Language-Action (VLA)",
      description: "Explore the convergence of LLMs and robotics with voice-to-action systems."
    }
  ];

  return (
    <Layout
      title="Physical AI & Humanoid Robotics"
      description="A book about the intersection of physical AI and humanoid robotics"
      wrapperClassName="book-landing-page"
    >
      <div style={{ position: 'relative', minHeight: '100vh' }}>
        {/* Background Spheres */}
        <BackgroundSpheres />

        {/* Hero Section */}
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

        {/* Features Section */}
        <div style={{
          position: 'relative',
          zIndex: 2,
          padding: '80px 20px',
          backgroundColor: 'rgba(10, 10, 20, 0.7)',
          backdropFilter: 'blur(10px)',
          color: 'white'
        }}>
          <div style={{
            maxWidth: '1200px',
            margin: '0 auto',
            textAlign: 'center'
          }}>
            <h2 style={{ fontSize: '2.5rem', marginBottom: '50px', fontWeight: 'bold' }}>What You'll Learn</h2>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
              gap: '30px',
              marginTop: '40px'
            }}>
              {features.map((feature, index) => (
                <div
                  key={index}
                  style={{
                    padding: '30px',
                    borderRadius: '15px',
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    backdropFilter: 'blur(10px)',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    transition: 'transform 0.3s ease, box-shadow 0.3s ease'
                  }}
                  onMouseEnter={(e) => {
                    e.target.style.transform = 'translateY(-10px)';
                    e.target.style.boxShadow = '0 20px 40px rgba(0, 224, 255, 0.2)';
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.transform = 'translateY(0)';
                    e.target.style.boxShadow = 'none';
                  }}
                >
                  <div style={{ fontSize: '3rem', marginBottom: '20px' }}>{feature.icon}</div>
                  <h3 style={{ fontSize: '1.5rem', marginBottom: '15px', fontWeight: '600' }}>{feature.title}</h3>
                  <p style={{ fontSize: '1rem', opacity: 0.9 }}>{feature.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Modules Section */}
        <div style={{
          position: 'relative',
          zIndex: 2,
          padding: '80px 20px',
          backgroundColor: 'rgba(20, 20, 30, 0.8)',
          backdropFilter: 'blur(10px)',
          color: 'white'
        }}>
          <div style={{
            maxWidth: '1200px',
            margin: '0 auto',
            textAlign: 'center'
          }}>
            <h2 style={{ fontSize: '2.5rem', marginBottom: '50px', fontWeight: 'bold' }}>Course Modules</h2>
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '30px',
              marginTop: '40px'
            }}>
              {modules.map((module, index) => (
                <div
                  key={index}
                  style={{
                    padding: '30px',
                    borderRadius: '15px',
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    backdropFilter: 'blur(10px)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    textAlign: 'left',
                    transition: 'transform 0.3s ease, box-shadow 0.3s ease'
                  }}
                  onMouseEnter={(e) => {
                    e.target.style.transform = 'translateY(-5px)';
                    e.target.style.boxShadow = '0 15px 30px rgba(0, 224, 255, 0.15)';
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.transform = 'translateY(0)';
                    e.target.style.boxShadow = 'none';
                  }}
                >
                  <h3 style={{ fontSize: '1.5rem', marginBottom: '15px', fontWeight: '600', color: '#00E0FF' }}>{module.title}</h3>
                  <p style={{ fontSize: '1.1rem', opacity: 0.9 }}>{module.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Testimonials Section */}
        <div style={{
          position: 'relative',
          zIndex: 2,
          padding: '80px 20px',
          backgroundColor: 'rgba(10, 10, 20, 0.7)',
          backdropFilter: 'blur(10px)',
          color: 'white'
        }}>
          <div style={{
            maxWidth: '1200px',
            margin: '0 auto',
            textAlign: 'center'
          }}>
            <h2 style={{ fontSize: '2.5rem', marginBottom: '50px', fontWeight: 'bold' }}>What Students Say</h2>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
              gap: '30px',
              marginTop: '40px'
            }}>
              <div style={{
                padding: '30px',
                borderRadius: '15px',
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                textAlign: 'left'
              }}>
                <p style={{ fontStyle: 'italic', marginBottom: '20px', opacity: 0.9 }}>"This book transformed my understanding of Physical AI. The hands-on approach with ROS 2 and simulation made complex concepts accessible."</p>
                <p style={{ fontWeight: 'bold' }}>- Robotics Engineering Student</p>
              </div>
              <div style={{
                padding: '30px',
                borderRadius: '15px',
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                textAlign: 'left'
              }}>
                <p style={{ fontStyle: 'italic', marginBottom: '20px', opacity: 0.9 }}>"The VLA module opened my eyes to the future of human-robot interaction. The practical exercises were incredibly valuable."</p>
                <p style={{ fontWeight: 'bold' }}>- AI Researcher</p>
              </div>
              <div style={{
                padding: '30px',
                borderRadius: '15px',
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                textAlign: 'left'
              }}>
                <p style={{ fontStyle: 'italic', marginBottom: '20px', opacity: 0.9 }}>"Finally, a comprehensive resource that bridges the gap between digital AI and physical robotics. Highly recommended!"</p>
                <p style={{ fontWeight: 'bold' }}>- Mechatronics Engineer</p>
              </div>
            </div>
          </div>
        </div>

        {/* Chatbot */}
        <Chatbot />
      </div>

      {/* Custom Footer for Landing Page */}
      <footer style={{
        position: 'relative',
        zIndex: 2,
        backgroundColor: 'rgba(15, 15, 35, 0.95)',
        backdropFilter: 'blur(10px)',
        color: 'white',
        padding: '40px 20px',
        borderTop: '1px solid rgba(255, 255, 255, 0.1)'
      }}>
        <div style={{
          maxWidth: '1200px',
          margin: '0 auto',
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '40px'
        }}>
          <div>
            <h3 style={{ fontSize: '1.3rem', marginBottom: '20px', color: '#00E0FF' }}>Book Content</h3>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              <li style={{ marginBottom: '10px' }}><a href="/docs/intro" style={{ color: 'rgba(255, 255, 255, 0.8)', textDecoration: 'none' }}>Introduction</a></li>
              <li style={{ marginBottom: '10px' }}><a href="/docs/module1-ros2/" style={{ color: 'rgba(255, 255, 255, 0.8)', textDecoration: 'none' }}>Module 1: ROS2</a></li>
              <li style={{ marginBottom: '10px' }}><a href="/docs/module2-digital-twin/" style={{ color: 'rgba(255, 255, 255, 0.8)', textDecoration: 'none' }}>Module 2: Digital Twin</a></li>
              <li style={{ marginBottom: '10px' }}><a href="/docs/module3-ai-robot-brain/" style={{ color: 'rgba(255, 255, 255, 0.8)', textDecoration: 'none' }}>Module 3: AI Robot Brain</a></li>
              <li style={{ marginBottom: '10px' }}><a href="/docs/module4-vla/" style={{ color: 'rgba(255, 255, 255, 0.8)', textDecoration: 'none' }}>Module 4: VLA</a></li>
            </ul>
          </div>
          <div>
            <h3 style={{ fontSize: '1.3rem', marginBottom: '20px', color: '#00E0FF' }}>Resources</h3>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              <li style={{ marginBottom: '10px' }}><a href="/docs/" style={{ color: 'rgba(255, 255, 255, 0.8)', textDecoration: 'none' }}>Documentation</a></li>
              <li style={{ marginBottom: '10px' }}><a href="https://github.com/gemini-book/AI-Spec-Driven-Book" style={{ color: 'rgba(255, 255, 255, 0.8)', textDecoration: 'none' }}>GitHub</a></li>
            </ul>
          </div>
          <div>
            <h3 style={{ fontSize: '1.3rem', marginBottom: '20px', color: '#00E0FF' }}>Legal</h3>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              <li style={{ marginBottom: '10px' }}><a href="/privacy" style={{ color: 'rgba(255, 255, 255, 0.8)', textDecoration: 'none' }}>Privacy Policy</a></li>
              <li style={{ marginBottom: '10px' }}><a href="/terms" style={{ color: 'rgba(255, 255, 255, 0.8)', textDecoration: 'none' }}>Terms of Service</a></li>
            </ul>
          </div>
        </div>
        <div style={{
          maxWidth: '1200px',
          margin: '40px auto 0',
          paddingTop: '20px',
          borderTop: '1px solid rgba(255, 255, 255, 0.1)',
          textAlign: 'center',
          color: 'rgba(255, 255, 255, 0.6)'
        }}>
          <p>© {new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. Built with Docusaurus.</p>
        </div>
      </footer>
    </Layout>
  );
};

export default BookLandingPage;