import { createContext, useState, useContext, useEffect } from 'react';
import type { ReactNode } from 'react';
import { useNavigate } from '@tanstack/react-router';
import api from '../lib/api';

interface User {
  id: number;
  username: string;
  email: string;
}
interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  login: (formData: URLSearchParams) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('access_token'));
  const navigate = useNavigate();

  useEffect(() => {
    const verifyTokenOnLoad = async () => {
      if (token) {
        try {
          // The interceptor in api.ts will add the token to the header
          const response = await api.get<User>('/auth/users/me');
          setUser(response.data); // Set user data if token is valid
        } catch (error) {
          console.error("Session expired or token is invalid. Logging out.", error);
          // If token is invalid, clear it
          logout();
        }
      }
    };

    verifyTokenOnLoad();
  }, [token]); // Rerun effect if token changes

  const login = async (formData: URLSearchParams) => {
    const response = await api.post('/auth/login', formData.toString(), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });

    const { access_token } = response.data;
    localStorage.setItem('access_token', access_token);
    setToken(access_token); // This will trigger the useEffect to fetch user data

  };

  const logout = () => { 
    setUser(null);
    setToken(null);
    localStorage.removeItem('access_token');
    // Navigate to login after logout
    navigate({ to: '/login' });
  };

  const value = {
    isAuthenticated: !!user, // Authenticated if we have user data
    user,
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