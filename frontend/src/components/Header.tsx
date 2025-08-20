// frontend/src/components/Header.tsx

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBars, faUser, faHouse } from '@fortawesome/free-solid-svg-icons'
import { useNavigate } from '@tanstack/react-router';
import { Avatar, Menu, Portal } from "@chakra-ui/react";
// Import the root route to access its context
import { Route } from '../routes/__root.tsx';
import type { AuthContextType } from '../lib/types';

// ... (icon and style definitions are unchanged)
const bar = <FontAwesomeIcon icon={ faBars } />
const user_icon = <FontAwesomeIcon icon={faUser} />
const home_icon = <FontAwesomeIcon icon={faHouse} />

const menuItemHoverStyle = {
  bg: 'cyan.500',
  cursor: 'pointer',
};

const barItemHoverStyle = {
  cursor: 'pointer',
  opacity: '0.8',
};

const logoutItemHoverStyle = {
  bg: 'red.500',
  cursor: 'pointer',
};

const loginItemHoverStyle = {
  cursor: 'pointer',
  opacity: '0.8',
};


function Header() {
  // Get auth context from the root route
  const { auth }: { auth: AuthContextType } = Route.useRouteContext()
  const navigate = useNavigate();

  const handleLogout = async () => {
    await auth.logout();
    // After logging out, navigate to the home page or login page
    navigate({ to: '/' });
  };

  return (
    <>
        <div className='relative w-full flex items-center justify-between gap-x-4 px-4 sm:px-6 py-4 bg-gradient-to-r from-cyan-400 to-violet-500 font-medium text-white text-xl shadow-lg'>
          {/* ... Left side menu and home icon are unchanged ... */}
          <div className="flex items-center gap-x-4">
            <Menu.Root>
                <Menu.Trigger rounded="full" focusRing="outside" _hover={barItemHoverStyle} className="bg-transparent px-3 py-1.5">
                  {bar}
                </Menu.Trigger>

                <Portal>
                  <Menu.Positioner>
                    <Menu.Content bg="cyan.600" color="white" borderWidth="1px" borderColor="gray.200">
                      <Menu.Item value="about" onClick={() => navigate({ to: '/about' })} _hover={menuItemHoverStyle}>About</Menu.Item>
                    </Menu.Content>
                  </Menu.Positioner>
                </Portal>
              </Menu.Root>

            {location.pathname !== '/' && (
                <div 
                  onClick={() => navigate({ to: '/' })} 
                  className="cursor-pointer hover:opacity-80"
                  title="Go to Homepage"
                >
                  {home_icon}
                </div>
              )}
           </div> 

            <h1 className='select-none absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2'>
              Cloud Playground
            </h1>

            {/* Right side user menu */}
            {auth.isAuthenticated ? (
              <Menu.Root>
                <Menu.Trigger rounded="full" focusRing="outside">
                  <Avatar.Root size="sm" colorPalette="cyan" _hover={loginItemHoverStyle}>
                    {/* Use optional chaining in case user is null briefly */}
                    <Avatar.Fallback name={auth.user?.username} />
                    <Avatar.Image src="" />
                  </Avatar.Root>
                </Menu.Trigger>

                <Portal>
                  <Menu.Positioner>
                    <Menu.Content bg="cyan.600" color="white" borderWidth="1px" borderColor="gray.200">
                      <Menu.Item value="account" _hover={menuItemHoverStyle}>Account</Menu.Item>
                      <Menu.Item value="settings" _hover={menuItemHoverStyle}>Settings</Menu.Item>
                      <Menu.Item value="logout" onClick={handleLogout} _hover={logoutItemHoverStyle}>Logout</Menu.Item>
                    </Menu.Content>
                  </Menu.Positioner>
                </Portal>
              </Menu.Root>
            ) : (
              // ... Unauthenticated menu is unchanged ...
              <Menu.Root>
                <Menu.Trigger rounded="full" focusRing="outside" _hover={barItemHoverStyle} className="bg-transparent px-3 py-1.5">
                  {user_icon}
                </Menu.Trigger>

                <Portal>
                  <Menu.Positioner>
                    <Menu.Content bg="cyan.600" color="white" borderWidth="1px" borderColor="gray.200">
                      <Menu.Item value="login" onClick={() => navigate({ to: '/login' })} _hover={menuItemHoverStyle}>Login</Menu.Item>
                      <Menu.Item value="register" onClick={() => navigate({ to: '/register' })} _hover={menuItemHoverStyle}>Register</Menu.Item>
                    </Menu.Content>
                  </Menu.Positioner>
                </Portal>
              </Menu.Root>
            )}
        </div>
    </>
  );
}

export default Header;