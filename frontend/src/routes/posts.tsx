import { createFileRoute, Link, redirect, useLoaderData, useNavigate } from '@tanstack/react-router'
import { AxiosError } from 'axios'
import { z } from 'zod'
import api from '../lib/api'
import type { Post } from '../lib/types';
import Header from '../components/Header';
import Search_bar from '../components/Search_bar';

// Validation schema for search params
const postsSearchSchema = z.object({
  q: z.string().optional(),
})

// API function to fetch posts with an optional search query
const fetchPosts = async (query?: string): Promise<Post[]> => {
  const { data } = await api.get('/posts/', {
    params: { q: query },
  })
  return data
}

export const Route = createFileRoute('/posts')({
  validateSearch: (search) => postsSearchSchema.parse(search),
  loaderDeps: ({ search: { q } }) => ({ q }),
  loader: async ({ deps: { q } }) => {
    return fetchPosts(q)
  },
  onError: (error) => {
    if (error instanceof AxiosError && error.response?.status === 401) {
      throw redirect({
        to: '/login',
        search: {
          redirect: location.pathname + location.search,
        },
      })
    }
  },
  component: PostsComponent,
})

function PostsComponent() {
  const posts: Post[] = useLoaderData({ from: '/posts' });
  const { q } = Route.useSearch();
  const navigate = useNavigate({ from: Route.id });

  const handleSearch = (query: string) => {
    navigate({
      search: { q: query.trim() || undefined }, // Use undefined to remove the param
    });
  };

  return (
    <>

      <Search_bar 
        initialQuery={q}
        onSearch={handleSearch}
      />
      
      <div className="mx-auto flex w-full max-w-2xl flex-col gap-y-4 rounded-xl bg-white p-6 shadow-lg">
        <h2 className="text-2xl text-center text-gray-700 mb-4 select-none">
          {q ? `Search Results for "${q}"` : 'All Posts'}
        </h2>
        
        {posts.length > 0 ? (
          <ul role="list" className="space-y-3">
            {posts.map((post: Post) => (
              <li key={post.id}>
                <Link
                  to="/post/$postId"
                  params={{ postId: post.id.toString() }}
                  className="group block rounded-md p-4 transition-colors hover:bg-gray-100"
                >
                  <div className="flex items-center justify-between gap-x-4">
                    <h3 className="text-lg font-semibold text-gray-800 transition-colors group-hover:text-blue-600">
                      {post.title}
                    </h3>
                    <svg 
                      xmlns="http://www.w3.org/2000/svg" 
                      viewBox="0 0 20 20" 
                      fill="currentColor" 
                      className="h-5 w-5 text-gray-400 transition-transform group-hover:translate-x-1 group-hover:text-blue-600"
                    >
                      <path fillRule="evenodd" d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <p className="text-sm text-gray-500 mt-1">
                    Posted by {post.user.username} on {new Date(post.created_at).toLocaleDateString()}
                  </p>
                </Link>
              </li>
            ))}
          </ul>
        ) : (
          <div className="text-center text-gray-500 py-8">
              {q ? (
              <>
                <p>No posts found matching your search for "{q}".</p>
                <Link to="/posts" search={{}} className="mt-4 inline-block text-blue-500 hover:underline">
                    &larr; Search all posts
                </Link>
              </>
              ) : (
                <p>It looks like there are no posts here yet.</p>
              )}
          </div>
        )}
      </div>
    </>
  )
}