import { createRootRoute, Link, Outlet } from '@tanstack/react-router'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { TanStackRouterDevtools } from '@tanstack/react-router-devtools'
import { AuthProvider } from '../contexts/AuthContext';

// Create a client
const queryClient = new QueryClient();

export const Route = createRootRoute({
  component: () => (
    <AuthProvider>
      <QueryClientProvider client={queryClient}>
      <Outlet />
      <TanStackRouterDevtools />
      </QueryClientProvider>
    </AuthProvider>
  ),
})