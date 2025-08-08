import { useState, useEffect } from 'react';
// import { useNavigate } from '@tanstack/react-router';
import { Container } from './Container';

const SearchIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    className="h-5 w-5 text-gray-400"
    fill="none"
    viewBox="0 0 24 24"
    stroke="currentColor"
    strokeWidth={2}
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
    />
  </svg>
);

// Define the props our component will accept
interface SearchBarProps {
  initialQuery?: string;
  onSearch: (query: string) => void;
}

function Search_bar({ initialQuery = '', onSearch }: SearchBarProps) {
  const [query, setQuery] = useState(initialQuery);

  useEffect(() => {
    setQuery(initialQuery);
  }, [initialQuery]);

  const handleSearchSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSearch(query);
  };

  const isSearchEnabled = !!query.trim();

  return (
    <>  
      <Container>
        <form onSubmit={handleSearchSubmit}>
          <label htmlFor="search-input" className="sr-only">Search</label>

          <div className="relative flex items-center rounded-xl bg-white shadow-lg focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500">
            
            <button 
              type="submit" 
              disabled={!isSearchEnabled} 
              aria-label="Search" 
              className={`group rounded-l-xl p-3 transition-colors ${
              isSearchEnabled
                ? 'cursor-pointer hover:bg-blue-50'
                : 'cursor-not-allowed'
            }`}
            >
              <div className={isSearchEnabled ? "group-hover:text-blue-600" : ""}>
                <SearchIcon />
              </div>
            </button>

            <input
              type="search"
              name="search-input"
              id="search-input"
              placeholder="Search posts..."
              className="block w-full border-0 bg-transparent p-3 pr-4 text-gray-700 placeholder:text-gray-400 focus:ring-0 sm:text-sm"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>
        </form>
      </Container>
    </>
  )
}

export default Search_bar;