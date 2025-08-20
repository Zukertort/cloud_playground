import React, { useState, useEffect } from 'react'
import ReactDOM from 'react-dom/client'
import { RouterProvider } from '@tanstack/react-router'
import { Provider } from "./components/ui/provider.tsx"
import { router } from './router.tsx'
import api from './lib/api.ts'
import type { AuthContextType } from './lib/types'
import { Spinner, Box } from '@chakra-ui/react'

// This is the new Root component that will manage auth state
function App() {
  const [user, setUser] = useState<AuthContextType['user']>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('access_token'));
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isAuthLoading, setIsAuthLoading] = useState(true);

  // This effect runs once on app load to verify the token
  useEffect(() => {
    const verifyTokenOnLoad = async () => {
      const storedToken = localStorage.getItem('access_token');
      if (storedToken) {
        try {
          const response = await api.get('/auth/users/me');
          setUser(response.data);
          setToken(storedToken);
          setIsAuthenticated(true);
        } catch (error) {
          console.error("Session expired or token is invalid. Logging out.", error);
          localStorage.removeItem('access_token');
          setToken(null);
          setUser(null);
          setIsAuthenticated(false);
        } finally {
          setIsAuthLoading(false);
        }
      } else {
        setIsAuthLoading(false);
      }
    };

    verifyTokenOnLoad();
  }, []);

  // Login function
  const login = async (formData: URLSearchParams) => {
    const response = await api.post('/auth/login', formData.toString(), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });

    const { access_token } = response.data;
    localStorage.setItem('access_token', access_token);
    
    // After setting the token, fetch user info
    const userResponse = await api.get('/auth/users/me');
    setUser(userResponse.data);
    setToken(access_token);
    setIsAuthenticated(true);
    await router.invalidate(); // This tells the router to re-run all `beforeLoad` checks and re-render.
  };

  // Logout function
  const logout = async() => {
    setUser(null);
    setToken(null);
    setIsAuthenticated(false);
    localStorage.removeItem('access_token');
    await router.invalidate();
    // Navigation will be handled by the component that calls logout
  };
  
  // Assemble the auth object to pass to the router context
  const auth: AuthContextType = {
    isAuthenticated,
    user,
    token,
    login,
    logout,
  };

  if (isAuthLoading) {
    return (
      <Provider>
        <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
          <Spinner size="xl" />
        </Box>
      </Provider>
    )
  }

  return <RouterProvider router={router} context={{ auth }} />
}

// Render the app
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Provider>
      <App />
    </Provider>
  </React.StrictMode>,
)