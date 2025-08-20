export interface User {
  id: number;
  username: string;
  email?: string; // Add email as optional since it's in your old context
}

// Post interface remains the same
export interface Post {
  id: number;
  title: string;
  content: string;
  created_at: string;
  user: User;
}

// Add the AuthContextType here
export interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  token?: string | null;
  login: (formData: URLSearchParams) => Promise<void>;
  logout: () => Promise<void>;
}