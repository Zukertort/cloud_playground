import React from 'react'
import ReactDOM from 'react-dom'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBars, faUser } from '@fortawesome/free-solid-svg-icons'
import { Menu } from "@chakra-ui/react"

const bar = <FontAwesomeIcon icon={ faBars } />
const user = <FontAwesomeIcon icon={faUser} />

function Header() {
  return (
    <>
        <div className='w-full flex items-center justify-between gap-x-4 px-4 sm:px-6 py-4 bg-gradient-to-r from-cyan-400 to-violet-500 font-medium text-white text-xl shadow-lg'>
            <button className='btn-header rounded-full'>{bar}</button>
            <h1 className='select-none'>Cloud Playground</h1>
            <button className='btn-header rounded-full'>{user}</button>
        </div>
    </>
  )
}

export default Header
