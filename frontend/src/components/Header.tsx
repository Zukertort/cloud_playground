import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBars, faUser } from '@fortawesome/free-solid-svg-icons'

// Import the necessary hooks and components
import { useNavigate } from '@tanstack/react-router';
import { useAuth } from '../contexts/AuthContext';
import { Avatar, Menu, Portal } from "@chakra-ui/react";

const bar = <FontAwesomeIcon icon={ faBars } />
const user = <FontAwesomeIcon icon={faUser} />

// Styling
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

  const { isAuthenticated, user: authUser, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <>
        <div className='w-full flex items-center justify-between gap-x-4 px-4 sm:px-6 py-4 bg-gradient-to-r from-cyan-400 to-violet-500 font-medium text-white text-xl shadow-lg'>
            
            <Menu.Root>
                <Menu.Trigger rounded="full" focusRing="outside" _hover={barItemHoverStyle} className="bg-transparent px-3 py-1.5">
                  {bar}
                </Menu.Trigger>

                <Portal>
                  <Menu.Positioner>
                    <Menu.Content bg="cyan.600" color="white" borderWidth="1px" borderColor="gray.200">
                      <Menu.Item value="">Unavailable</Menu.Item>
                    </Menu.Content>
                  </Menu.Positioner>
                </Portal>
              </Menu.Root>

            <h1 className='select-none'>Cloud Playground</h1>

            {isAuthenticated ? (
              
              <Menu.Root>
                <Menu.Trigger rounded="full" focusRing="outside">
                  <Avatar.Root size="sm" colorPalette="cyan" _hover={loginItemHoverStyle}>
                    <Avatar.Fallback name="Segun Adebayo" />
                    <Avatar.Image src="" />
                  </Avatar.Root>
                </Menu.Trigger>

                <Portal>
                  <Menu.Positioner>
                    <Menu.Content bg="cyan.600" color="white" borderWidth="1px" borderColor="gray.200">
                      <Menu.Item value="account" _hover={menuItemHoverStyle}>Account</Menu.Item>
                      <Menu.Item value="settings" _hover={menuItemHoverStyle}>Settings</Menu.Item>
                      <Menu.Item value="logout" onClick={logout} _hover={logoutItemHoverStyle}>Logout</Menu.Item>
                    </Menu.Content>
                  </Menu.Positioner>
                </Portal>

              </Menu.Root>
              
            ) : (
              <Menu.Root>
                <Menu.Trigger rounded="full" focusRing="outside" _hover={barItemHoverStyle} className="bg-transparent px-3 py-1.5">
                  {user}
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
