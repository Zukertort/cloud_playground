import { createFileRoute } from '@tanstack/react-router'
import Body from '../components/Body'
import Footer from '../components/Footer'

export const Route = createFileRoute('/')({
  component: Index,
})

function Index() {
  return (
    <>
      <Body />
      <Footer />
    </>
  )
}