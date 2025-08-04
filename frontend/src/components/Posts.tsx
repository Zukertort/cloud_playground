import { useQuery } from '@tanstack/react-query';
import api from '../lib/api';
import { Link } from '@tanstack/react-router';

interface Post {
    id: number
    title: string
    content: string
    created_at: string
}

const fetchPosts = async () => {
  const { data } = await api.get('/posts/');
  return data;
};

export function Posts() {
  // useQuery handles fetching, caching, loading states, and errors
  const { data: posts, isLoading, isError } = useQuery({
    queryKey: ['posts'],
    queryFn: fetchPosts,
  });


  if (isLoading) {
    return <div>Loading posts...</div>;
  }

 
  if (isError) {
    return <div>Error fetching posts.</div>;
  }


 return (
      <div className="mx-auto flex w-full max-w-lg flex-col gap-y-4 rounded-xl bg-white p-6 shadow-lg">
        <h2 className="text-2xl text-center text-gray-700 mb-4 select-none">Latest Posts</h2>

      <ul role="list" className="space-y-1">
        {posts?.map((post: Post) => (
          <li key={post.id}>
            {/* 1. The Link/anchor tag now wraps all content and gets the styling */}
            <Link
              to="/post/$postId"
              params={{ postId: post.id.toString() }}
              className="group flex items-center justify-between gap-x-4 rounded-md p-3 transition-colors hover:bg-gray-100"
            >
              <span className="text-gray-700 transition-colors group-hover:text-blue-600">
                {post.title}
              </span>
              
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                viewBox="0 0 20 20" 
                fill="currentColor" 
                className="h-5 w-5 text-gray-400 transition-transform group-hover:translate-x-1 group-hover:text-blue-600"
              >
                <path fillRule="evenodd" d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z" clipRule="evenodd" />
              </svg>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Posts