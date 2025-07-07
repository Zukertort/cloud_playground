import { Avatar, Menu, Portal } from "@chakra-ui/react"
import * as React from "react"
import { useNavigate } from '@tanstack/react-router'

const Demo = () => {
  const navigate = useNavigate()
  return (
    <Menu.Root positioning={{ placement: "right-end" }}>
      <Menu.Trigger rounded="full" focusRing="outside">
        <Avatar.Root size="sm">
          <Avatar.Fallback name="Segun Adebayo" />
          <Avatar.Image src="" />
        </Avatar.Root>
      </Menu.Trigger>
      <Portal>
        <Menu.Positioner>
          <Menu.Content>
            <Menu.Item value="account">Account</Menu.Item>
            <Menu.Item value="settings">Settings</Menu.Item>
            <Menu.Item value="logout">Logout</Menu.Item>
          </Menu.Content>
        </Menu.Positioner>
      </Portal>
    </Menu.Root>
  )
}