import React, { useState, useEffect, useMemo } from 'react'
import ReactDOM from 'react-dom/client'
import { RouterProvider } from '@tanstack/react-router'
import { Provider } from "./components/ui/provider.tsx"
import { router } from './router.tsx'
import api from './lib/api.ts'
import type { AuthContextType } from './lib/types'
import { Spinner, Box } from '@chakra-ui/react'

function App() {
  const [user, setUser] = useState<AuthContextType['user']>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isAuthLoading, setIsAuthLoading] = useState(true);

  useEffect(() => {
    const verifyTokenOnLoad = async () => {
      const storedToken = localStorage.getItem('access_token');
      if (storedToken) {
        try {
          const response = await api.get('/auth/users/me');
          setUser(response.data);
          setIsAuthenticated(true);
        } catch (error) {
          console.error("Session expired or token is invalid.", error);
        }
      }
      setIsAuthLoading(false);
    };
    verifyTokenOnLoad();
  }, []);

  useEffect(() => {
    if (!isAuthLoading) {
      router.invalidate();
    }
  }, [isAuthenticated]);

  const auth = useMemo(() => ({
    isAuthenticated,
    user,
    login: async (formData: URLSearchParams) => {
      const response = await api.post('/auth/login', formData, {
         headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });

      const { access_token } = response.data;
      localStorage.setItem('access_token', access_token);
      
      const userResponse = await api.get('/auth/users/me');
      
      setUser(userResponse.data);
      setIsAuthenticated(true);
      await router.invalidate();
    },
    logout: async () => {
      setUser(null);
      setIsAuthenticated(false);
      localStorage.removeItem('access_token');
      await router.invalidate();
    },
  }), [isAuthenticated, user]);

  if (isAuthLoading) {
    return (
      <Provider>
        <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
          <Spinner size="xl" />
        </Box>
      </Provider>
    );
  }

  // Provide the reactive `auth` object to the router.
  return <RouterProvider router={router} context={{ auth }} />;
}


// Render the app
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Provider>
      <App />
    </Provider>
  </React.StrictMode>,
)