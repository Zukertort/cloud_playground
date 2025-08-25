import { createFileRoute, redirect, useNavigate } from '@tanstack/react-router'
import { useState } from 'react'
import api from '../lib/api'
import { toaster } from '../components/ui/toaster'

// Chakra UI components
import {
  Button,
  Field,
  Fieldset,
  Input,
  Stack,
  Textarea,
} from '@chakra-ui/react'

export const Route = createFileRoute('/new_post')({
  component: RouteComponent,
  beforeLoad: ({ context }) => {
    if (!context.auth?.isAuthenticated) {
      throw redirect({
        to: '/login',
        search: {
          redirect: location.pathname,
        },
      })
    }
  }
})

function RouteComponent() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate({ from: '/new_post' });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim() || !content.trim()) {
      toaster.create({
        title: 'Validation Error',
        description: 'Title and content cannot be empty.',
        type: 'error',
      });
      return;
    }

    setIsLoading(true);

    try {
      await api.post('/posts/', { title, content });
      
      toaster.create({
        title: 'Post Created',
        description: 'Your post has been successfully created.',
        type: 'success',
      });

      // Navigate to home page on success
      navigate({ to: '/' });

    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "An unexpected error occurred. Please try again.";
      toaster.create({
        title: 'Error Creating Post',
        description: errorMessage,
        type: 'error',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-2xl w-full p-6 bg-white rounded-lg shadow-md">
      <form onSubmit={handleSubmit}>
        <Fieldset.Root>
          <Fieldset.Legend asChild>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Create a New Post</h1>
          </Fieldset.Legend>
          <p className="text-gray-600 mb-6">
            Share what's on your mind with the community.
          </p>

          <Fieldset.Content asChild>
            <Stack gap={5}>
              <Field.Root>
                <Field.Label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
                  Title
                </Field.Label>
                <Input
                  id="title"
                  name="title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Your post title"
                  color={'black'}
                />
              </Field.Root>

              <Field.Root>
                <Field.Label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-1">
                  Content
                </Field.Label>
                <Textarea
                  id="content"
                  name="content"
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  placeholder="Write your post content here..."
                  rows={8}
                  color={'black'}
                />
              </Field.Root>
            </Stack>
          </Fieldset.Content>

          <hr className="my-6" />
          <Stack direction="row" gap={4}>
            <Button
              type="submit"
              colorPalette="blue"
              variant="solid"
              loading={isLoading}
              loadingText="Creating..."
            >
              Create Post
            </Button>
            <Button
              variant="ghost"
              onClick={() => navigate({ to: '/' })}
              loading={isLoading}
            >
              Cancel
            </Button>
          </Stack>
        </Fieldset.Root>
      </form>
    </div>
  )
}
