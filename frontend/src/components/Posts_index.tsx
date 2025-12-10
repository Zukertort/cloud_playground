import { useQuery } from '@tanstack/react-query';
import { Link } from '@tanstack/react-router';
import { isAxiosError } from 'axios';
import api from '../lib/api';
import { Spinner } from "@chakra-ui/react";

import type { Post, PaginatedPostsResponse } from '../lib/types';

const fetchPosts = async (): Promise<PaginatedPostsResponse> => {
  const { data } = await api.get('/posts/', { params: { limit: 5, offset: 0 } });
  return data;
};

export function Posts_index() {
  // useQuery handles fetching, caching, loading states, and errors
  const { data: posts, isLoading, isError, error } = useQuery({
    queryKey: ['posts-latest'],
    queryFn: fetchPosts,
    retry: false,

    select: (data) => data.posts,
  });


  if (isLoading) {
    return <div className='text-blue-500'><Spinner size='xs'/> Loading posts...</div>;
  }

 
  if (isError) {
    if (isAxiosError(error) && error.response?.status === 401) {
      return (
        <div className="mx-auto flex w-full max-w-lg flex-col items-center gap-y-4 rounded-xl bg-white p-8 text-center shadow-lg">
          <h3 className="text-xl font-semibold text-gray-800">Authentication Required</h3>
          <p className="text-gray-500">
            You must be logged in to view posts.
          </p>
          <Link
            to="/login"
            className="mt-2 inline-block rounded-md bg-blue-600 px-6 py-2 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
          >
            Login
          </Link>
        </div>
      );
    }

    return <div className='text-red-500'>Error fetching posts. Please try again later.</div>;
  }


 return (
      <div className="mx-auto flex w-full max-w-4xl flex-col gap-y-4 rounded-xl bg-white p-6 shadow-lg">
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
      <div className="mt-4 border-t border-gray-200 pt-4 text-center">
        <Link
          to="/posts"
          className="inline-block rounded-md bg-cyan-600 px-5 py-2 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-cyan-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
        >
          View All Posts
        </Link>
      </div>
    </div>
  );
}

export default Posts_index;