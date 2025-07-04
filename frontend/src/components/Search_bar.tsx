import React from 'react'

function Search_bar() {
  return (
    <>  
      <div className="mx-auto flex w-full max-w-lg flex-col gap-y-4 rounded-xl bg-white p-6 shadow-lg">
          <p className="text-center text-gray-700 select-none"> Find posts, users, and applications with the search bar.</p>
          <input
            className="w-full rounded-md border border-blue-100 p-2 placeholder:italic placeholder:text-grey-100 focus:outline-none focus:ring-2 focus:ring-blue-200"
            placeholder="Search for anything..."
            type="text"
            name="search"
          />
      </div>
    </>
  )
}

export default Search_bar