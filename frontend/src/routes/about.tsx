import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/about')({
  component: About,
})

function About() {
  return (
    <div className="mx-auto max-w-2xl w-full p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-3xl font-bold text-gray-900 mb-4 text-center">About</h1>
      <p className="text-gray-500 text-xs leading-relaxed text-center mb-10">
        Some info
      </p>
    </div>
  )
}