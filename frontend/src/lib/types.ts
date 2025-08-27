export interface User {
  id: number;
  username: string;
  email?: string;
}

export interface Post {
  id: number;
  title: string;
  content: string;
  created_at: string;
  user: User;
}

export interface PaginatedPostsResponse {
  total: number;
  posts: Post[];
}

export interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  token?: string | null;
  login: (formData: URLSearchParams) => Promise<void>;
  logout: () => Promise<void>;
}