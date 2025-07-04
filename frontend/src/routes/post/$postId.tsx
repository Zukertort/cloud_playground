import { createFileRoute, Link, useLoaderData } from '@tanstack/react-router'
import axios from 'axios'

// Define the shape of a single post for type safety
interface Post {
    post_id: number
    title: string
    content: string
    author_id: number
    published_date: string
}

const fetchPostById = async (postId: string): Promise<Post> => {
  const { data } = await axios.get(`http://127.0.0.1:8000/posts/${postId}`)
  return data
}

export const Route = createFileRoute('/post/$postId')({
  loader: async ({ params }) => {
    return fetchPostById(params.postId)
  },
  component: PostComponent,
  notFoundComponent: () => {
    return (
      <div className="p-4 text-center">
        <h2 className="text-2xl font-bold text-red-600">Post Not Found!</h2>
        <p className="text-gray-600 mt-2">We couldn't find the post you were looking for.</p>
        <Link to="/" className="mt-4 inline-block text-blue-500 hover:underline">
          &larr; Back to Home
        </Link>
      </div>
    )
  },
})

function PostComponent() {
  // Use the useLoaderData hook to get the data fetched by the loader
  const post: Post = useLoaderData({ from: '/post/$postId' })

  return (
    <div className="mx-auto max-w-2xl p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-3xl font-bold text-gray-900 mb-4">{post.title}</h1>
      <h2 className="text-gray-700 leading-relaxed">{post.published_date}</h2>
      <p className="text-gray-700 leading-relaxed">{post.content}</p>

      <hr className="my-6" />

      <Link to="/" className="text-blue-500 hover:underline">
        &larr; Back to Home
      </Link>
    </div>
  )
}