// frontend/src/contexts/AuthContext.tsx
import { createContext, useState, useContext, useEffect } from 'react';
import type { ReactNode } from 'react';
import { useNavigate } from '@tanstack/react-router';
import api from '../lib/api';

interface AuthContextType {
  isAuthenticated: boolean;
  token: string | null;
  login: (token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('access_token'));
  const navigate = useNavigate();

  useEffect(() => {
    // Optional: Add a check here to verify the token with the backend
    // on initial load to ensure it's still valid.
  }, []);

  const login = (newToken: string) => {
    setToken(newToken);
    localStorage.setItem('access_token', newToken);
  };

  const logout = () => {
    setToken(null);
    localStorage.removeItem('access_token');
    // Navigate to login after logout
    navigate({ to: '/login' });
  };

  const value = {
    isAuthenticated: !!token,
    token,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};