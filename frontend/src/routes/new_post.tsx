import { createFileRoute, redirect } from '@tanstack/react-router'


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
  return <div>Hello from "/new_post"!</div>
}
