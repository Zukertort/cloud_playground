import React from 'react';
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

function Search_bar() {
  return (
    <>  
      <Container>
        <label htmlFor="search-input" className="sr-only">Search</label>

        <div className="relative flex items-center rounded-xl bg-white shadow-lg focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500">
          
          <div className="pointer-events-none flex items-center justify-center p-3">
            <SearchIcon />
          </div>

          <input
            type="search"
            name="search-input"
            id="search-input"
            placeholder="Search..."
            className="block w-full border-0 bg-transparent p-3 pr-4 text-gray-700 placeholder:text-gray-400 focus:ring-0 sm:text-sm"
          />

        </div>

      </Container>
    </>
  )
}

export default Search_bar