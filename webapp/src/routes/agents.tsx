import { createRoute } from '@tanstack/react-router'
import { rootRoute } from './__root'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Bot, Activity, Zap, CheckCircle2 } from 'lucide-react'

export const agentsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/agents',
  component: AgentsPage,
})

const agents = [
  {
    id: 'extraction',
    name: 'Extraction Agent',
    description: 'Extracts data from various sources',
    status: 'active',
    lastRun: '2 minutes ago',
    tasksProcessed: 1247,
  },
  {
    id: 'distillation',
    name: 'Distillation Agent',
    description: 'Distills information into summaries',
    status: 'active',
    lastRun: '5 minutes ago',
    tasksProcessed: 892,
  },
  {
    id: 'ingestion',
    name: 'Ingestion Agent',
    description: 'Ingests processed data into database',
    status: 'active',
    lastRun: '1 minute ago',
    tasksProcessed: 2103,
  },
  {
    id: 'inference',
    name: 'Inference Agent',
    description: 'Makes inferences from data patterns',
    status: 'idle',
    lastRun: '15 minutes ago',
    tasksProcessed: 456,
  },
  {
    id: 'proof',
    name: 'Proof Agent',
    description: 'Generates proofs and validations',
    status: 'active',
    lastRun: '3 minutes ago',
    tasksProcessed: 678,
  },
  {
    id: 'generative',
    name: 'Generative Agent',
    description: 'Generates new content and insights',
    status: 'idle',
    lastRun: '20 minutes ago',
    tasksProcessed: 234,
  },
]

function AgentsPage() {
  const activeAgents = agents.filter(a => a.status === 'active').length
  const totalTasks = agents.reduce((sum, a) => sum + a.tasksProcessed, 0)

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Agents</h1>
        <p className="text-muted-foreground mt-2">
          Monitor and manage your AI agents
        </p>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Agents</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">{activeAgents}</div>
            <p className="text-xs text-muted-foreground">of {agents.length} total</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Tasks</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalTasks.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">Processed</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">System Health</CardTitle>
            <CheckCircle2 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">Healthy</div>
            <p className="text-xs text-muted-foreground">All systems operational</p>
          </CardContent>
        </Card>
      </div>

      {/* Agent List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {agents.map((agent) => (
          <Card key={agent.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Bot className="h-5 w-5 text-primary" />
                  <CardTitle className="text-lg">{agent.name}</CardTitle>
                </div>
                <Badge
                  variant={agent.status === 'active' ? 'default' : 'secondary'}
                  className={
                    agent.status === 'active'
                      ? 'bg-green-500'
                      : 'bg-gray-500'
                  }
                >
                  {agent.status}
                </Badge>
              </div>
              <CardDescription>{agent.description}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Last Run</span>
                <span className="font-medium">{agent.lastRun}</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Tasks Processed</span>
                <span className="font-medium">{agent.tasksProcessed.toLocaleString()}</span>
              </div>
              <div className="flex gap-2 pt-2">
                <button className="flex-1 px-3 py-2 text-sm bg-primary text-primary-foreground rounded-md hover:bg-primary/90">
                  View Details
                </button>
                <button className="px-3 py-2 text-sm border rounded-md hover:bg-accent">
                  <Zap className="h-4 w-4" />
                </button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Agent Activity */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
          <CardDescription>Latest agent operations</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[
              { agent: 'Extraction Agent', action: 'Processed 15 items', time: '2 min ago', status: 'success' },
              { agent: 'Distillation Agent', action: 'Completed batch', time: '5 min ago', status: 'success' },
              { agent: 'Ingestion Agent', action: 'Ingested 23 records', time: '1 min ago', status: 'success' },
              { agent: 'Inference Agent', action: 'Idle - waiting for data', time: '15 min ago', status: 'idle' },
            ].map((activity, idx) => (
              <div key={idx} className="flex items-center gap-4 p-4 border rounded-lg">
                <div className={`w-2 h-2 rounded-full ${
                  activity.status === 'success' ? 'bg-green-500' :
                  activity.status === 'idle' ? 'bg-yellow-500' :
                  'bg-red-500'
                }`} />
                <div className="flex-1">
                  <p className="text-sm font-medium">{activity.agent}</p>
                  <p className="text-xs text-muted-foreground">{activity.action}</p>
                </div>
                <span className="text-xs text-muted-foreground">{activity.time}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

