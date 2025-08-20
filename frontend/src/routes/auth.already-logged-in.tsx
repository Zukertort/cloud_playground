import { createFileRoute, useNavigate, useRouter } from '@tanstack/react-router'
import { z } from 'zod'
import type { AuthContextType } from '../lib/types';

// Validate that 'from' is a string, defaulting to '/' if not present
const alreadyLoggedInSearchSchema = z.object({
  from: z.string().optional().catch('/'),
});

export const Route = createFileRoute('/auth/already-logged-in')({
  validateSearch: alreadyLoggedInSearchSchema,
  component: AlreadyLoggedIn,
})

function AlreadyLoggedIn() {
  const { auth }: { auth: AuthContextType } = Route.useRouteContext();
  const { from } = Route.useSearch();
  const navigate = useNavigate();
  const router = useRouter();

  const handleLogoutAndRedirect = async () => {
    await auth.logout();
    // After logout, navigate to the page they were trying to access (login/register)
    navigate({ to: from });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-blue-100 px-4">
      <div className="w-full max-w-md rounded-xl bg-white p-6 text-center shadow-lg sm:p-8">
        <h2 className="text-2xl font-bold tracking-tight text-gray-900">
          You are already logged in
        </h2>
        <p className="mt-2 text-gray-600">
          You are signed in as <span className="font-medium">{auth.user?.username}</span>.
        </p>

        <div className="mt-8 flex flex-col gap-y-4 sm:flex-row sm:gap-x-4 sm:gap-y-0">
          <button
            onClick={() => router.history.back()}
            className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          >
            &larr; Go Back
          </button>
          <button
            onClick={handleLogoutAndRedirect}
            className="flex w-full justify-center rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-600"
          >
            Log Out
          </button>
        </div>
      </div>
    </div>
  );
  
}
