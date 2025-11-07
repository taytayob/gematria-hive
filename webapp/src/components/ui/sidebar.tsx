import * as React from "react"
import { cn } from "@/lib/utils"
import { Link, useRouterState } from "@tanstack/react-router"
import { 
  LayoutDashboard, 
  KanbanSquare, 
  Calculator, 
  BarChart3, 
  Bot, 
  Settings,
  BookOpen,
  Menu,
  X
} from "lucide-react"
import { Button } from "./button"

interface SidebarProps {
  className?: string
}

const navigation = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Kanban Board", href: "/kanban", icon: KanbanSquare },
  { name: "Pipeline & Phases", href: "/pipeline", icon: Bot },
  { name: "Research & Knowledge", href: "/research", icon: BookOpen },
  { name: "Gematria Calculator", href: "/calculator", icon: Calculator },
  { name: "Statistics", href: "/statistics", icon: BarChart3 },
  { name: "Agents", href: "/agents", icon: Bot },
  { name: "Settings", href: "/settings", icon: Settings },
]

export function Sidebar({ className }: SidebarProps) {
  const router = useRouterState()
  const location = router.location
  const [isMobileOpen, setIsMobileOpen] = React.useState(false)

  return (
    <>
      {/* Mobile menu button */}
      <div className="lg:hidden fixed top-4 left-4 z-50">
        <Button
          variant="outline"
          size="icon"
          onClick={() => setIsMobileOpen(!isMobileOpen)}
        >
          {isMobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </Button>
      </div>

      {/* Mobile overlay */}
      {isMobileOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 z-40"
          onClick={() => setIsMobileOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          "fixed top-0 left-0 z-40 h-screen w-64 bg-card border-r transition-transform lg:translate-x-0",
          isMobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0",
          className
        )}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center gap-2 p-6 border-b">
            <div className="text-2xl">🐝</div>
            <div>
              <h1 className="font-bold text-lg">Gematria Hive</h1>
              <p className="text-xs text-muted-foreground">Webapp</p>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-1">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href
              const Icon = item.icon
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  onClick={() => setIsMobileOpen(false)}
                  className={cn(
                    "flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors",
                    isActive
                      ? "bg-primary text-primary-foreground"
                      : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                  )}
                >
                  <Icon className="h-5 w-5" />
                  {item.name}
                </Link>
              )
            })}
          </nav>

          {/* Footer */}
          <div className="p-4 border-t">
            <p className="text-xs text-muted-foreground text-center">
              v1.0.0
            </p>
          </div>
        </div>
      </aside>
    </>
  )
}

