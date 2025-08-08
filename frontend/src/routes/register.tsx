import { useState } from 'react';
import { createFileRoute, Link, useNavigate } from '@tanstack/react-router';
import api from '../lib/api';
import { Spinner } from "@chakra-ui/react";

export const Route = createFileRoute('/register')({
  component: Register,
})

function Register() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [errors, setErrors] = useState<{ [key: string]: string | null }>({});
    const [success, setSuccess] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setErrors({});
        setSuccess(null);
        setIsLoading(true);

        // Client-side validation
        if (password !== confirmPassword) {
            setErrors({ 
                password: "Passwords do not match.", 
                confirmPassword: "Passwords do not match." 
            });
            setIsLoading(false);
            return;
        }

        try {
            const userData = { username, email, password };
            // The /auth/register endpoint expects a JSON body
            await api.post('/auth/register', userData);
            
            setSuccess("Registration successful! Redirecting to login...");

            // Redirect to the login page after a short delay
            setTimeout(() => {
                navigate({ to: '/login' });
            }, 2000);

        } catch (err: any) {
            const errorMessage = err.response?.data?.detail || "An unexpected error occurred. Please try again.";
            // Determine which field the error belongs to
            if (errorMessage.toLowerCase().includes('email')) {
                setErrors({ email: errorMessage });
            } else if (errorMessage.toLowerCase().includes('username')) {
                setErrors({ username: errorMessage });
            } else {
                // For generic errors
                setErrors({ general: errorMessage });
            }
        } finally {
            setIsLoading(false);
        }
    };

    const baseInputClass = "block w-full rounded-md border-0 bg-gray-50 px-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset placeholder:text-gray-400 focus:outline-none focus:ring-1 focus:ring-inset sm:text-sm";
    
    const getInputClass = (fieldName: 'username' | 'email' | 'password' | 'confirmPassword') => {
        const hasError = !!errors[fieldName];
        const errorClass = 'ring-red-500 focus:ring-red-500';
        const defaultClass = 'ring-gray-300 focus:ring-indigo-500';
        return `${baseInputClass} ${hasError ? errorClass : defaultClass}`;
    };



    return (
        <div className="min-h-screen flex items-center justify-center bg-blue-100 px-4">
            <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-lg sm:p-8">
                <div className="text-center">
                    <h2 className="text-2xl font-bold tracking-tight text-gray-900">
                        Create your account
                    </h2>
                </div>
                <div className="mt-8">
                    <form onSubmit={handleSubmit} className="space-y-4">
                        {/* Username Input */}
                        <div>
                            <label htmlFor="username" className="block text-sm font-medium text-gray-900">
                                Username
                            </label>
                            <div className="mt-2">
                                <input
                                    id="username"
                                    name="username"
                                    type="text"
                                    required
                                    autoComplete="username"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    className={getInputClass('username')}
                                    aria-invalid={!!errors.username}
                                />
                            </div>
                            {errors.username && <p className="mt-1 text-sm text-red-500">{errors.username}</p>}
                        </div>
                        
                        {/* Email Input */}
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
                                    className={getInputClass('email')}
                                    aria-invalid={!!errors.email}
                                />
                            </div>
                            {errors.email && <p className="mt-1 text-sm text-red-500">{errors.email}</p>}
                        </div>

                        {/* Password Input */}
                        <div>
                            <label htmlFor="password" className="block text-sm font-medium text-gray-900">
                                Password
                            </label>
                            <div className="mt-2">
                                <input
                                    id="password"
                                    name="password"
                                    type="password"
                                    required
                                    autoComplete="new-password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className={getInputClass('password')}
                                    aria-invalid={!!errors.password}
                                />
                            </div>
                            {errors.password && <p className="mt-1 text-sm text-red-500">{errors.password}</p>} 
                        </div>

                        {/* Confirm Password Input */}
                        <div>
                            <label htmlFor="confirm-password" className="block text-sm font-medium text-gray-900">
                                Confirm Password
                            </label>
                            <div className="mt-2">
                                <input
                                    id="confirm-password"
                                    name="confirm-password"
                                    type="password"
                                    required
                                    autoComplete="new-password"
                                    value={confirmPassword}
                                    onChange={(e) => setConfirmPassword(e.target.value)}
                                    className={getInputClass('confirmPassword')}
                                    aria-invalid={!!errors.confirmPassword}
                                />
                            </div>
                            {errors.confirmPassword && <p className="mt-1 text-sm text-red-500">{errors.confirmPassword}</p>}
                        </div>

                        {errors && <p className="text-sm text-red-500">{errors.general}</p>}
                        {success && <p className="text-sm text-green-500"><Spinner size='xs'/>{success}</p>}

                        <div>
                            <button
                                type="submit"
                                className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                            >
                                Create Account
                            </button>
                        </div>
                    </form>

                    <p className="mt-8 text-center text-sm text-gray-500">
                        Already a member?{' '}
                        <Link to="/login" className="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">
                            Sign in
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
}
