import { useState } from 'react';
import { createFileRoute, useNavigate, useSearch, Link } from '@tanstack/react-router';
import { z } from 'zod';
import { useAuth } from '../contexts/AuthContext';

const loginSearchSchema = z.object({
    redirect: z.string().optional(),
});

export const Route = createFileRoute('/login')({
  validateSearch: (search) => loginSearchSchema.parse(search),
  component: Login,
})

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState<string | null>(null);
    const { login } = useAuth();
    const navigate = useNavigate();

    const { redirect } = useSearch({ from:Route.id});

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);

        // FastAPI's OAuth2PasswordRequestForm expects 'username' and 'password' fields
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        try {
            await login(formData);
            navigate({ to: redirect || '/' });
            
        } catch (err: any) {
            const errorMessage = err.response?.data?.detail || "An unexpected error occurred. Please try again.";
            setError(errorMessage);
        }
    };

  return (
  <>
        <div className="min-h-screen flex items-center justify-center bg-blue-100 px-4">
            <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-lg sm:p-8">
                <div className="text-center">
                    <h2 className="text-2xl font-bold tracking-tight text-gray-900">
                        Sign in to your account
                    </h2>
                </div>
                <div className="mt-8">
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-gray-900">
                                Email address
                            </label>
                            <div className="mt-2">
                                <input
                                id="email"
                                name="email"
                                type="email"
                                required
                                autoComplete="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="block w-full rounded-md border-0 bg-gray-50 px-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:outline-none focus:ring-1 focus:ring-inset focus:ring-indigo-500 sm:text-sm"
                                />
                            </div>
                        </div>

                        <div>
                            <div className="flex items-center justify-between">
                                <label htmlFor="password" className="block text-sm font-medium text-gray-900">
                                Password
                                </label>
                                <div className="text-sm">
                                <a href="#" className="font-semibold text-indigo-600 hover:text-indigo-500">
                                    Forgot password?
                                </a>
                                </div>
                            </div>
                            <div className="mt-2">
                                <input
                                    id="password"
                                    name="password"
                                    type="password"
                                    required
                                    autoComplete="current-password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="block w-full rounded-md border-0 bg-gray-50 px-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:outline-none focus:ring-1 focus:ring-inset focus:ring-indigo-500 sm:text-sm"
                                />
                            </div>  
                        </div>

                        {error && <p className="text-sm text-red-500">{error}</p>}

                        <div>
                            <button
                                type="submit"
                                className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                            >
                                Sign in
                            </button>
                        </div>
                    </form>

                    <p className="mt-8 text-center text-sm text-gray-500">
                        Not a member?{' '}
                        <Link to="/register" className="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">
                                Start a 14 day free trial
                        </Link>
                    </p>
                </div>
            </div>
        </div>
  </>
  )
}