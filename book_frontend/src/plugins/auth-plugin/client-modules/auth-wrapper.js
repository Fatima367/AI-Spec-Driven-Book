// src/plugins/auth-plugin/client-modules/auth-wrapper.js
import React from 'react';
import { AuthProvider } from '../../../contexts/AuthContext';

export default function AuthWrapper({ children }) {
  return <AuthProvider>{children}</AuthProvider>;
}