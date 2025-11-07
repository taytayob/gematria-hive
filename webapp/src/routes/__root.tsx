import { createRootRoute, Outlet } from '@tanstack/react-router'
import { Layout } from '@/components/Layout'
import { Toaster } from '@/components/ui/toaster'

export const rootRoute = createRootRoute({
  component: () => (
    <>
      <Layout>
        <Outlet />
      </Layout>
      <Toaster />
    </>
  ),
})

