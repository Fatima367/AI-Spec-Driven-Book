import React, { useEffect } from 'react';
import { useHistory } from '@docusaurus/router';
import { AuthProvider, useAuth } from '../contexts/AuthContext'; // Import AuthProvider
import AuthModal from '../components/Auth/AuthModal';

/**
 * Login page that opens the auth modal and redirects after login
 */
const LoginPage = () => {
  const history = useHistory();
  const { user, isLoading } = useAuth();
  const [showModal, setShowModal] = React.useState(true);

  // If user is already logged in, redirect to home
  useEffect(() => {
    if (user && !isLoading) {
      history.push('/');
    }
  }, [user, isLoading, history]);

  const handleLoginSuccess = (user) => {
    history.push('/'); // Redirect to home after successful login
  };

  const handleClose = () => {
    history.push('/'); // Redirect to home when modal is closed
  };

  if (isLoading) {
    return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>Loading...</div>;
  }

  if (user) {
    // User is already logged in, redirecting...
    history.push('/');
    return null;
  }

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)' }}>
      <AuthModal
        isOpen={showModal}
        onClose={handleClose}
        initialView="login"
        onLoginSuccess={handleLoginSuccess}
      />
    </div>
  );
};

export default function WrappedLoginPage() {
  return (
    <AuthProvider>
      <LoginPage />
    </AuthProvider>
  );
}