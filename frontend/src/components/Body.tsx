import React from 'react'
import Header from './Header'

function Body() {
  return (
    <>
        <div className='mx-auto flex-col max-w-screen min-h-screen sm:items-center justify-center gap-2 p-8 bg-white font-medium text-sky-600 text-xl'>
            <Header />
        </div>
    </>
  )
}

export default Body