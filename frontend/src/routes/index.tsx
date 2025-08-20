import { createFileRoute, useRouterState } from '@tanstack/react-router'
import Search_bar from '../components/Search_bar'
import Posts_index from '../components/Posts_index'

export const Route = createFileRoute('/')({
  component: Index,
})

function Index() {
  const navigate = Route.useNavigate(); // Use the route-specific hook
  const routerState = useRouterState();
  // Ensure search is an object before accessing properties
  const searchParams = new URLSearchParams(routerState.location.searchStr);
  const currentQuery = searchParams.get('q') || '';

  const handleIndexSearch = (query: string) => {
    navigate({
      to: '/posts',
      search: { q: query.trim() || undefined },
    });
  };

  return (
    <>
      <Search_bar 
        initialQuery={currentQuery}
        onSearch={handleIndexSearch}
      />
      <Posts_index />
    </>
  )
}