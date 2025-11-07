import { createRoute } from '@tanstack/react-router'
import { rootRoute } from './__root'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { useStatistics } from '@/lib/queries'
import { LayoutDashboard, KanbanSquare, Calculator, BarChart3, Bot } from 'lucide-react'
import { Link } from '@tanstack/react-router'

export const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  component: Dashboard,
})

function Dashboard() {
  const { data: stats } = useStatistics()

  const quickLinks = [
    {
      title: 'Kanban Board',
      description: 'Manage tasks and track progress',
      href: '/kanban',
      icon: KanbanSquare,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      title: 'Gematria Calculator',
      description: 'Calculate gematria values',
      href: '/calculator',
      icon: Calculator,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
    },
    {
      title: 'Statistics',
      description: 'View detailed analytics',
      href: '/statistics',
      icon: BarChart3,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      title: 'Agents',
      description: 'Monitor agent activity',
      href: '/agents',
      icon: Bot,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100',
    },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground mt-2">
          Welcome to Gematria Hive. Overview of your system.
        </p>
      </div>

      {/* Statistics Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Tasks</CardTitle>
              <LayoutDashboard className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.total}</div>
              <p className="text-xs text-muted-foreground">All tasks</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Pending</CardTitle>
              <KanbanSquare className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">
                {stats.by_status?.pending || 0}
              </div>
              <p className="text-xs text-muted-foreground">Awaiting action</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">In Progress</CardTitle>
              <Bot className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-yellow-600">
                {stats.by_status?.in_progress || 0}
              </div>
              <p className="text-xs text-muted-foreground">Active work</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Cost</CardTitle>
              <BarChart3 className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">
                ${(stats.total_cost || 0).toFixed(2)}
              </div>
              <p className="text-xs text-muted-foreground">Cumulative</p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Quick Links */}
      <div>
        <h2 className="text-2xl font-semibold mb-4">Quick Links</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickLinks.map((link) => {
            const Icon = link.icon
            return (
              <Link key={link.href} to={link.href}>
                <Card className="hover:shadow-lg transition-shadow cursor-pointer h-full">
                  <CardHeader>
                    <div className={`w-12 h-12 rounded-lg ${link.bgColor} flex items-center justify-center mb-2`}>
                      <Icon className={`h-6 w-6 ${link.color}`} />
                    </div>
                    <CardTitle>{link.title}</CardTitle>
                    <CardDescription>{link.description}</CardDescription>
                  </CardHeader>
                </Card>
              </Link>
            )
          })}
        </div>
      </div>

      {/* Recent Activity */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
          <CardDescription>Latest updates from your system</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center gap-4 p-4 border rounded-lg">
              <div className="w-2 h-2 bg-green-500 rounded-full" />
              <div className="flex-1">
                <p className="text-sm font-medium">System operational</p>
                <p className="text-xs text-muted-foreground">All services running normally</p>
              </div>
              <span className="text-xs text-muted-foreground">Just now</span>
            </div>
            <div className="flex items-center gap-4 p-4 border rounded-lg">
              <div className="w-2 h-2 bg-blue-500 rounded-full" />
              <div className="flex-1">
                <p className="text-sm font-medium">Tasks synced</p>
                <p className="text-xs text-muted-foreground">All tasks up to date</p>
              </div>
              <span className="text-xs text-muted-foreground">2 min ago</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

