import { createRootRouteWithContext, Outlet } from '@tanstack/react-router'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { TanStackRouterDevtools } from '@tanstack/react-router-devtools'
import type { AuthContextType } from '../lib/types';
import Header from '../components/Header';
import Footer from '../components/Footer';

interface RouterContext {
  auth: AuthContextType;
}

// Create a client
const queryClient = new QueryClient();

export const Route = createRootRouteWithContext<RouterContext>()({
  component: RootComponent,
})

function RootComponent() {

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-violet-50 flex flex-col">
        <Header />
        <main className="flex-grow flex flex-col items-center justify-start gap-y-8 py-10 px-4">
          <Outlet />
        </main>
        <Footer />
      </div>
      <TanStackRouterDevtools />
    </QueryClientProvider>
  )
}
