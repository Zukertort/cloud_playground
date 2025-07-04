import React from 'react'
import Header from './Header'
import Search_bar from './Search_bar'
import Posts from './Posts'

function Body() {
  return (
    <>
        <div className='min-h-screen bg-violet-50 flex flex-col items-center justify-start gap-y-8 py-10 px-4'>
            <Header />
            <Search_bar />
            <Posts />
        </div>
    </>
  )
}

export default Body