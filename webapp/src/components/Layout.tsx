import * as React from "react"
import { Outlet } from "@tanstack/react-router"
import { Sidebar } from "@/components/ui/sidebar"

export function Layout({ children }: { children?: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <main className="flex-1 overflow-auto lg:ml-64">
        <div className="container mx-auto p-6">
          {children || <Outlet />}
        </div>
      </main>
    </div>
  )
}

