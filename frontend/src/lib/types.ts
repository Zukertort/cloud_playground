export interface User {
  id: number;
  username: string;
}

export interface Post {
  id: number;
  title: string;
  content: string;
  created_at: string;
  user: User;
}