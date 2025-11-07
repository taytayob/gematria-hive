import { createRoute } from '@tanstack/react-router'
import { rootRoute } from './__root'
import { useStatistics, useTasks } from '@/lib/queries'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { BarChart3, TrendingUp, DollarSign, CheckCircle2 } from 'lucide-react'

export const statisticsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/statistics',
  component: StatisticsPage,
})

function StatisticsPage() {
  const { data: stats, isLoading: statsLoading } = useStatistics()
  const { data: tasks = [], isLoading: tasksLoading } = useTasks()

  const statusCounts = {
    pending: tasks.filter(t => t.status === 'pending').length,
    in_progress: tasks.filter(t => t.status === 'in_progress').length,
    completed: tasks.filter(t => t.status === 'completed').length,
    archived: tasks.filter(t => t.status === 'archived').length,
  }

  const totalCost = tasks.reduce((sum, task) => sum + (task.cost || 0), 0)

  if (statsLoading || tasksLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-muted-foreground">Loading statistics...</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Statistics</h1>
        <p className="text-muted-foreground mt-2">
          Detailed analytics and insights
        </p>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Tasks</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.total || 0}</div>
            <p className="text-xs text-muted-foreground">All tasks</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Completed</CardTitle>
            <CheckCircle2 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {statusCounts.completed}
            </div>
            <p className="text-xs text-muted-foreground">
              {stats?.total ? ((statusCounts.completed / stats.total) * 100).toFixed(1) : 0}% completion rate
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Cost</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-purple-600">
              ${totalCost.toFixed(2)}
            </div>
            <p className="text-xs text-muted-foreground">Cumulative</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Cost/Task</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${stats?.total ? (totalCost / stats.total).toFixed(2) : '0.00'}
            </div>
            <p className="text-xs text-muted-foreground">Per task</p>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Statistics */}
      <Tabs defaultValue="status" className="w-full">
        <TabsList>
          <TabsTrigger value="status">Status Breakdown</TabsTrigger>
          <TabsTrigger value="cost">Cost Analysis</TabsTrigger>
          <TabsTrigger value="timeline">Timeline</TabsTrigger>
        </TabsList>

        <TabsContent value="status" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Tasks by Status</CardTitle>
              <CardDescription>Distribution of tasks across different statuses</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {Object.entries(statusCounts).map(([status, count]) => {
                const percentage = stats?.total ? (count / stats.total) * 100 : 0
                return (
                  <div key={status} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="capitalize">{status.replace('_', ' ')}</span>
                      <span className="font-medium">{count} ({percentage.toFixed(1)}%)</span>
                    </div>
                    <div className="w-full bg-muted rounded-full h-2">
                      <div
                        className="bg-primary h-2 rounded-full transition-all"
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                  </div>
                )
              })}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="cost" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Cost Analysis</CardTitle>
              <CardDescription>Financial breakdown of tasks</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 border rounded-lg">
                  <div className="text-sm text-muted-foreground">Total Cost</div>
                  <div className="text-2xl font-bold">${totalCost.toFixed(2)}</div>
                </div>
                <div className="p-4 border rounded-lg">
                  <div className="text-sm text-muted-foreground">Tasks with Cost</div>
                  <div className="text-2xl font-bold">
                    {tasks.filter(t => (t.cost || 0) > 0).length}
                  </div>
                </div>
                <div className="p-4 border rounded-lg">
                  <div className="text-sm text-muted-foreground">Average Cost</div>
                  <div className="text-2xl font-bold">
                    ${stats?.total ? (totalCost / stats.total).toFixed(2) : '0.00'}
                  </div>
                </div>
                <div className="p-4 border rounded-lg">
                  <div className="text-sm text-muted-foreground">Highest Cost</div>
                  <div className="text-2xl font-bold">
                    ${tasks.length > 0 ? Math.max(...tasks.map(t => t.cost || 0)).toFixed(2) : '0.00'}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="timeline" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Task Timeline</CardTitle>
              <CardDescription>Recent task activity</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {tasks
                  .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
                  .slice(0, 10)
                  .map((task) => (
                    <div key={task.id} className="flex items-center gap-4 p-4 border rounded-lg">
                      <div className={`w-2 h-2 rounded-full ${
                        task.status === 'completed' ? 'bg-green-500' :
                        task.status === 'in_progress' ? 'bg-yellow-500' :
                        'bg-blue-500'
                      }`} />
                      <div className="flex-1">
                        <p className="text-sm font-medium">{task.content.substring(0, 50)}...</p>
                        <p className="text-xs text-muted-foreground">
                          {new Date(task.timestamp).toLocaleString()}
                        </p>
                      </div>
                      <span className="text-xs text-muted-foreground capitalize">
                        {task.status.replace('_', ' ')}
                      </span>
                    </div>
                  ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

