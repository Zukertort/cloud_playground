import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBars, faUser } from '@fortawesome/free-solid-svg-icons'

// Import the necessary hooks and components
import { useNavigate } from '@tanstack/react-router';
import { useAuth } from '../contexts/AuthContext';
import { Avatar, Menu, Portal } from "@chakra-ui/react";

const bar = <FontAwesomeIcon icon={ faBars } />
const user = <FontAwesomeIcon icon={faUser} />

function Header() {

  const { isAuthenticated, user: authUser, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <>
        <div className='w-full flex items-center justify-between gap-x-4 px-4 sm:px-6 py-4 bg-gradient-to-r from-cyan-400 to-violet-500 font-medium text-white text-xl shadow-lg'>
            <button className='btn-header rounded-full'>{bar}</button>
            <h1 className='select-none'>Cloud Playground</h1>

            {isAuthenticated ? (
              
              <Menu.Root>
                <Menu.Trigger rounded="full" focusRing="outside">
                  <Avatar.Root size="sm" colorPalette="cyan">
                    <Avatar.Fallback name="Segun Adebayo" />
                    <Avatar.Image src="" />
                  </Avatar.Root>
                </Menu.Trigger>

                <Portal>
                  <Menu.Positioner>
                    <Menu.Content colorPalette="cyan">
                      <Menu.Item value="account">Account</Menu.Item>
                      <Menu.Item value="settings">Settings</Menu.Item>
                      <Menu.Item value="logout" onClick={logout}>Logout</Menu.Item>
                    </Menu.Content>
                  </Menu.Positioner>
                </Portal>

              </Menu.Root>
              
            ) : (
              <button className='btn-header rounded-full' onClick={() => navigate({ to: '/login' })}>{user}</button>
            )}
        </div>
    </>
  );
}

export default Header;
