import { createFileRoute, Link, useLoaderData, redirect } from '@tanstack/react-router';
import { AxiosError } from 'axios';
import api from '../../lib/api';
import type { PostTitleAndDate } from '../../lib/types';

const fetchPostsByUserId = async (userId: string): Promise<PostTitleAndDate[]> => {
  const { data } = await api.get(`/posts/user/${userId}`);
  return data;
}

export const Route = createFileRoute('/my_work/$my_workid')({
    loader: async ({ params }) => {
    return fetchPostsByUserId(params.my_workid);
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
     // Add more error handling here, e.g., for 403 Forbidden
  },
  component: MyWorkComponent, // The component that will render the data
  notFoundComponent: () => {
    return (
      <div className='min-h-screen bg-violet-50 flex flex-col items-center justify-start gap-y-8 py-10 px-4'>
        <div className="p-4 text-center bg-white rounded-lg shadow-md max-w-lg w-full">
          <h2 className="text-2xl font-bold text-red-600">User Not Found or No Access</h2>
          <p className="text-gray-600 mt-2">We couldn't find the user you were looking for, or you don't have permission to view their work.</p>
          <Link to="/" className="mt-4 inline-block text-blue-500 hover:underline">
            &larr; Back to Home
          </Link>
        </div>
      </div>
    )
  },
});

function MyWorkComponent() {
  // Use the useLoaderData hook to get the array of posts fetched by the loader
  const posts = useLoaderData({ from: '/my_work/$my_workid' });

  return (
    <div className="mx-auto max-w-2xl w-full p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-3xl font-bold text-gray-900 mb-6 text-center">My Work</h1>
      
      {posts.length > 0 ? (
        <ul className="space-y-4">
          {posts.map((post: PostTitleAndDate, index: number) => (
            <li key={index} className="p-4 border rounded-lg hover:bg-gray-50">
              <h2 className="text-xl font-semibold text-gray-800">{post.title}</h2>
              <p className="text-sm text-gray-500 mt-1">
                Published on {new Date(post.created_at).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                })}
              </p>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-center text-gray-500">This user has not published any posts yet.</p>
      )}

      <div className="mt-8">
        <Link to="/" className="text-blue-500 hover:underline">
          &larr; Back to Home
        </Link>
      </div>
    </div>
  );
}