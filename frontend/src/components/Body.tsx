import Header from './Header'
import Search_bar from './Search_bar'
import Posts_index from './Posts_index' 
import { useNavigate, useRouterState } from '@tanstack/react-router'

function Body() {
  const navigate = useNavigate();
  const routerState = useRouterState();
  const searchParams = new URLSearchParams(routerState.location.search);
  const currentQuery = searchParams.get('q') || '';

  const handleIndexSearch = (query: string) => {
    // navigate TO the /posts page with the query
    navigate({
      to: '/posts',
      search: { q: query.trim() || undefined },
    });
  };

  return (
    <>
        <div className='min-h-screen bg-violet-50 flex flex-col items-center justify-start gap-y-8 py-10 px-4'>
            <Header />
            <Search_bar 
              initialQuery={currentQuery}
              onSearch={handleIndexSearch}
            />
            <Posts_index />
        </div>
    </>
  )
}

export default Body;