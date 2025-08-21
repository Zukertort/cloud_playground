import { createFileRoute, Link, useLoaderData, redirect } from '@tanstack/react-router';
import { AxiosError } from 'axios';
import api from '../../lib/api';
import type { Post } from '../../lib/types';

const fetchPostById = async (postId: string): Promise<Post> => {
  const { data } = await api.get(`/posts/${postId}`)
  return data
}

export const Route = createFileRoute('/post/$postId')({
  loader: async ({ params }) => {
    return fetchPostById(params.postId)
  },
  onError: (error) => {
    if (error instanceof AxiosError && error.response?.status === 401) {
      throw redirect({
        to: '/login',
        search: {
          redirect: location.pathname,
        },
      });
    }
  },
  component: PostComponent,
  notFoundComponent: () => {
    return (
      <div>

        <div className='min-h-screen bg-violet-50 flex flex-col items-center justify-start gap-y-8 py-10 px-4'></div>
          <div className="p-4 text-center bg-white rounded-lg shadow-md max-w-lg w-full">
            <h2 className="text-2xl font-bold text-red-600">Post Not Found!</h2>
            <p className="text-gray-600 mt-2">We couldn't find the post you were looking for.</p>
            <Link to="/" className="mt-4 inline-block text-blue-500 hover:underline">
              &larr; Back to Home
            </Link>
          </div>
      </div>
    )
  },
})

function PostComponent() {
  // Use the useLoaderData hook to get the data fetched by the loader
  const post: Post = useLoaderData({ from: '/post/$postId' })

  return (

      <div className="mx-auto max-w-2xl w-full p-6 bg-white rounded-lg shadow-md">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">{post.title}</h1>
        <p className="text-gray-700 leading-relaxed">
          Posted by {post.user.username} on {new Date(post.created_at).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
            })}
        </p>
        <div className="prose max-w-none">
            <p className="text-gray-700 leading-relaxed">{post.content}</p>
        </div>

        <hr className="my-6" />

        <Link to="/" className="text-blue-500 hover:underline">
          &larr; Back to Home
        </Link>
      </div>

  )
}