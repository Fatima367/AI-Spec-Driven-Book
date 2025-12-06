import React from 'react';

/**
 * Background component with 3 large, glowing, iridescent spheres
 * Uses radial gradients and CSS animations to create the desired effect
 */
const BackgroundSpheres = () => {
  return (
    <div 
      data-testid="background-container"
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: 1,
        overflow: 'hidden',
        background: '#020510', // Deep void navy/black
      }}
    >
      {/* Sphere 1 - Top Left */}
      <div 
        data-testid="background-sphere"
        style={{
          position: 'absolute',
          width: '500px',
          height: '500px',
          borderRadius: '50%',
          background: 'radial-gradient(circle, #00E0FF 0%, #0066FF 30%, #000000 70%)',
          top: '10%',
          left: '5%',
          filter: 'blur(60px)',
          opacity: '0.7',
          animation: 'pulse 8s infinite alternate'
        }}
      />
      
      {/* Sphere 2 - Top Right */}
      <div 
        data-testid="background-sphere"
        style={{
          position: 'absolute',
          width: '400px',
          height: '400px',
          borderRadius: '50%',
          background: 'radial-gradient(circle, #D600FF 0%, #6600FF 30%, #000000 70%)',
          top: '15%',
          right: '10%',
          filter: 'blur(50px)',
          opacity: '0.6',
          animation: 'float 10s infinite ease-in-out'
        }}
      />
      
      {/* Sphere 3 - Bottom Center */}
      <div 
        data-testid="background-sphere"
        style={{
          position: 'absolute',
          width: '600px',
          height: '600px',
          borderRadius: '50%',
          background: 'radial-gradient(circle, #00E0FF 0%, #D600FF 40%, #000000 80%)',
          bottom: '10%',
          left: '50%',
          transform: 'translateX(-50%)',
          filter: 'blur(70px)',
          opacity: '0.5',
          animation: 'rotate 20s infinite linear'
        }}
      />
      
      {/* Keyframes for animations */}
      <style jsx>{`
        @keyframes pulse {
          0% {
            transform: scale(1) translate(0, 0);
            opacity: 0.6;
          }
          100% {
            transform: scale(1.1) translate(10px, -10px);
            opacity: 0.8;
          }
        }
        
        @keyframes float {
          0% {
            transform: translate(0, 0);
          }
          50% {
            transform: translate(-20px, 20px);
          }
          100% {
            transform: translate(0, 0);
          }
        }
        
        @keyframes rotate {
          0% {
            transform: translateX(-50%) rotate(0deg);
          }
          100% {
            transform: translateX(-50%) rotate(360deg);
          }
        }
      `}</style>
    </div>
  );
};

export default BackgroundSpheres;