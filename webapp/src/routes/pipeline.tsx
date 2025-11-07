import { createRoute } from '@tanstack/react-router'
import { rootRoute } from './__root'
import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { useTasks, useCreateTask, useUpdateTask } from '@/lib/queries'
import { pipelineApi, type AgentExecutionRequest } from '@/lib/pipeline-api'
import { Play, Pause, CheckCircle2, Zap, Search, Bot } from 'lucide-react'
import { useToast } from '@/hooks/use-toast'

export const pipelineRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/pipeline',
  component: PipelinePage,
})

const PHASES = [
  { id: 'phase1_basic', name: 'Phase 1: Foundation', description: 'Basic extraction and ingestion' },
  { id: 'phase2_deep', name: 'Phase 2: Deep Analysis', description: 'Deep research and analysis' },
  { id: 'phase3_advanced', name: 'Phase 3: Advanced', description: 'Advanced processing and inference' },
  { id: 'phase4_scale', name: 'Phase 4: Scale', description: 'Scaling and optimization' },
] as const

const AGENTS = [
  { id: 'extraction', name: 'Extraction Agent', phase: 'phase1_basic', icon: Search },
  { id: 'distillation', name: 'Distillation Agent', phase: 'phase1_basic', icon: Zap },
  { id: 'ingestion', name: 'Ingestion Agent', phase: 'phase1_basic', icon: CheckCircle2 },
  { id: 'deep_research', name: 'Deep Research Agent', phase: 'phase2_deep', icon: Search },
  { id: 'inference', name: 'Inference Agent', phase: 'phase3_advanced', icon: Bot },
  { id: 'proof', name: 'Proof Agent', phase: 'phase3_advanced', icon: CheckCircle2 },
  { id: 'generative', name: 'Generative Agent', phase: 'phase4_scale', icon: Zap },
] as const

function PipelinePage() {
  const { data: tasks = [] } = useTasks()
  const createTask = useCreateTask()
  const updateTask = useUpdateTask()
  const { toast } = useToast()
  
  const [selectedPhase, setSelectedPhase] = useState<string>('phase1_basic')
  const [executing, setExecuting] = useState<string | null>(null)
  const [newTask, setNewTask] = useState({
    content: '',
    phase: 'phase1_basic',
    priority: 'medium',
    agent: 'extraction',
  })

  const phaseTasks = tasks.filter(t => t.phase === selectedPhase)
  const phaseAgents = AGENTS.filter(a => a.phase === selectedPhase)

  const handleExecuteAgent = async (agentId: string) => {
    setExecuting(agentId)
    
    try {
      // Create task for agent execution
      const task = await createTask.mutateAsync({
        content: `Execute ${AGENTS.find(a => a.id === agentId)?.name || agentId}`,
        phase: selectedPhase,
        status: 'in_progress',
        priority: 'high',
        metadata: {
          agent: agentId,
          execution_type: 'pipeline',
          started_at: new Date().toISOString(),
        },
      })

      // Execute agent via backend API
      try {
        const agentRequest: AgentExecutionRequest = {
          agent: agentId,
          phase: selectedPhase,
          task_type: agentId === 'deep_research' ? 'deep_research' : 'general',
          metadata: {
            task_id: task.id,
            phase: selectedPhase,
          },
        }

        // For deep research, add topic_name if available
        if (agentId === 'deep_research') {
          agentRequest.topic_name = 'Deep Research Task'
          agentRequest.query = 'Research topic'
        }

        const executionResult = await pipelineApi.executeAgent(agentRequest)

        // Update task with results
        await updateTask.mutateAsync({
          id: task.id,
          task: {
            status: executionResult.success ? 'completed' : 'failed',
            progress: executionResult.success ? 100 : 0,
            metadata: {
              ...task.metadata,
              completed_at: new Date().toISOString(),
              execution_time: executionResult.execution_time,
              execution_result: executionResult,
            },
          },
        })
        
        setExecuting(null)
        toast({
          title: executionResult.success ? 'Agent executed' : 'Execution failed',
          description: executionResult.success
            ? `${AGENTS.find(a => a.id === agentId)?.name} completed successfully.`
            : executionResult.error || 'Agent execution failed',
          variant: executionResult.success ? 'default' : 'destructive',
        })
      } catch (apiError) {
        // If API call fails, still update task
        await updateTask.mutateAsync({
          id: task.id,
          task: {
            status: 'failed',
            progress: 0,
            metadata: {
              ...task.metadata,
              error: apiError instanceof Error ? apiError.message : 'API call failed',
            },
          },
        })
        
        setExecuting(null)
        toast({
          title: 'Execution failed',
          description: apiError instanceof Error ? apiError.message : 'Failed to execute agent',
          variant: 'destructive',
        })
      }
    } catch (error) {
      setExecuting(null)
      toast({
        title: 'Execution failed',
        description: error instanceof Error ? error.message : 'Failed to execute agent',
        variant: 'destructive',
      })
    }
  }

  const handleCreatePipelineTask = async () => {
    if (!newTask.content.trim()) {
      toast({
        title: 'Error',
        description: 'Task content is required',
        variant: 'destructive',
      })
      return
    }

    try {
      await createTask.mutateAsync({
        content: newTask.content,
        phase: newTask.phase,
        priority: newTask.priority,
        status: 'pending',
        metadata: {
          agent: newTask.agent,
          pipeline_task: true,
        },
      })

      setNewTask({ content: '', phase: 'phase1_basic', priority: 'medium', agent: 'extraction' })
      toast({
        title: 'Task created',
        description: 'Pipeline task created successfully.',
      })
    } catch (error) {
      toast({
        title: 'Error',
        description: error instanceof Error ? error.message : 'Failed to create task',
        variant: 'destructive',
      })
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Pipeline & Phases</h1>
        <p className="text-muted-foreground mt-2">
          Execute agentic work through phases with Google Deep Research integration
        </p>
      </div>

      {/* Phase Selection */}
      <Card>
        <CardHeader>
          <CardTitle>Work Phases</CardTitle>
          <CardDescription>Select a phase to view agents and tasks</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {PHASES.map((phase) => (
              <button
                key={phase.id}
                onClick={() => setSelectedPhase(phase.id)}
                className={`p-4 border rounded-lg text-left transition-all ${
                  selectedPhase === phase.id
                    ? 'border-primary bg-primary/5'
                    : 'hover:border-primary/50'
                }`}
              >
                <div className="font-semibold">{phase.name}</div>
                <div className="text-sm text-muted-foreground mt-1">{phase.description}</div>
                <div className="text-xs text-muted-foreground mt-2">
                  {phaseTasks.filter(t => t.phase === phase.id).length} tasks
                </div>
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Agents for Selected Phase */}
        <Card>
          <CardHeader>
            <CardTitle>Agents - {PHASES.find(p => p.id === selectedPhase)?.name}</CardTitle>
            <CardDescription>Execute agents in this phase</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {phaseAgents.map((agent) => {
              const Icon = agent.icon
              const isExecuting = executing === agent.id
              const agentTasks = tasks.filter(
                t => t.metadata?.agent === agent.id && t.phase === selectedPhase
              )
              
              return (
                <div
                  key={agent.id}
                  className="flex items-center justify-between p-4 border rounded-lg"
                >
                  <div className="flex items-center gap-3">
                    <Icon className="h-5 w-5 text-primary" />
                    <div>
                      <div className="font-medium">{agent.name}</div>
                      <div className="text-xs text-muted-foreground">
                        {agentTasks.length} task(s)
                      </div>
                    </div>
                  </div>
                  <Button
                    onClick={() => handleExecuteAgent(agent.id)}
                    disabled={isExecuting || createTask.isPending}
                    size="sm"
                  >
                    {isExecuting ? (
                      <>
                        <Pause className="mr-2 h-4 w-4 animate-spin" />
                        Executing...
                      </>
                    ) : (
                      <>
                        <Play className="mr-2 h-4 w-4" />
                        Execute
                      </>
                    )}
                  </Button>
                </div>
              )
            })}
          </CardContent>
        </Card>

        {/* Tasks for Selected Phase */}
        <Card>
          <CardHeader>
            <CardTitle>Tasks - {PHASES.find(p => p.id === selectedPhase)?.name}</CardTitle>
            <CardDescription>Tasks in this phase</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3 max-h-[400px] overflow-y-auto">
              {phaseTasks.length === 0 ? (
                <div className="text-center text-muted-foreground py-8">
                  No tasks in this phase
                </div>
              ) : (
                phaseTasks.map((task) => (
                  <div
                    key={task.id}
                    className="p-4 border rounded-lg space-y-2"
                  >
                    <div className="flex items-start justify-between">
                      <p className="text-sm flex-1">{task.content}</p>
                      <Badge
                        variant={
                          task.status === 'completed' ? 'default' :
                          task.status === 'in_progress' ? 'default' :
                          'secondary'
                        }
                        className={
                          task.status === 'completed' ? 'bg-green-500' :
                          task.status === 'in_progress' ? 'bg-yellow-500' :
                          ''
                        }
                      >
                        {task.status.replace('_', ' ')}
                      </Badge>
                    </div>
                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                      {task.metadata?.agent && (
                        <span>Agent: {task.metadata.agent}</span>
                      )}
                      {task.progress > 0 && (
                        <span>Progress: {task.progress}%</span>
                      )}
                    </div>
                    {task.progress > 0 && (
                      <div className="w-full bg-muted rounded-full h-2">
                        <div
                          className="bg-primary h-2 rounded-full transition-all"
                          style={{ width: `${task.progress}%` }}
                        />
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Create Pipeline Task */}
      <Card>
        <CardHeader>
          <CardTitle>Create Pipeline Task</CardTitle>
          <CardDescription>Create a new task for agent execution</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="task-content">Task Content</Label>
            <Textarea
              id="task-content"
              value={newTask.content}
              onChange={(e) => setNewTask({ ...newTask, content: e.target.value })}
              placeholder="Describe the task..."
              rows={3}
            />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label htmlFor="task-phase">Phase</Label>
              <Select
                value={newTask.phase}
                onValueChange={(value) => setNewTask({ ...newTask, phase: value })}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {PHASES.map((phase) => (
                    <SelectItem key={phase.id} value={phase.id}>
                      {phase.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="task-agent">Agent</Label>
              <Select
                value={newTask.agent}
                onValueChange={(value) => setNewTask({ ...newTask, agent: value })}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {AGENTS.filter(a => a.phase === newTask.phase).map((agent) => (
                    <SelectItem key={agent.id} value={agent.id}>
                      {agent.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="task-priority">Priority</Label>
              <Select
                value={newTask.priority}
                onValueChange={(value) => setNewTask({ ...newTask, priority: value })}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="low">Low</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                  <SelectItem value="critical">Critical</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <Button
            onClick={handleCreatePipelineTask}
            disabled={createTask.isPending}
            className="w-full"
          >
            {createTask.isPending ? 'Creating...' : 'Create Pipeline Task'}
          </Button>
        </CardContent>
      </Card>

      {/* Pipeline Flow Visualization */}
      <Card>
        <CardHeader>
          <CardTitle>Pipeline Flow</CardTitle>
          <CardDescription>Visual representation of the agent pipeline</CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="flow" className="w-full">
            <TabsList>
              <TabsTrigger value="flow">Flow</TabsTrigger>
              <TabsTrigger value="status">Status</TabsTrigger>
              <TabsTrigger value="deep-research">Deep Research</TabsTrigger>
            </TabsList>

            <TabsContent value="flow" className="space-y-4">
              <div className="space-y-4">
                {PHASES.map((phase, idx) => {
                  const phaseAgents = AGENTS.filter(a => a.phase === phase.id)
                  return (
                    <div key={phase.id} className="space-y-2">
                      <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold">
                          {idx + 1}
                        </div>
                        <div>
                          <div className="font-semibold">{phase.name}</div>
                          <div className="text-sm text-muted-foreground">{phase.description}</div>
                        </div>
                      </div>
                      <div className="ml-10 grid grid-cols-1 md:grid-cols-3 gap-2">
                        {phaseAgents.map((agent) => {
                          const Icon = agent.icon
                          const agentTasks = tasks.filter(
                            t => t.metadata?.agent === agent.id && t.phase === phase.id
                          )
                          return (
                            <div
                              key={agent.id}
                              className="p-3 border rounded-lg bg-muted/50"
                            >
                              <div className="flex items-center gap-2">
                                <Icon className="h-4 w-4" />
                                <span className="text-sm font-medium">{agent.name}</span>
                              </div>
                              <div className="text-xs text-muted-foreground mt-1">
                                {agentTasks.length} task(s)
                              </div>
                            </div>
                          )
                        })}
                      </div>
                      {idx < PHASES.length - 1 && (
                        <div className="ml-4 flex items-center gap-2 text-muted-foreground">
                          <div className="h-8 w-px bg-border" />
                          <span className="text-xs">↓ Next Phase</span>
                        </div>
                      )}
                    </div>
                  )
                })}
              </div>
            </TabsContent>

            <TabsContent value="status" className="space-y-4">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {PHASES.map((phase) => {
                  const phaseTasks = tasks.filter(t => t.phase === phase.id)
                  const completed = phaseTasks.filter(t => t.status === 'completed').length
                  const inProgress = phaseTasks.filter(t => t.status === 'in_progress').length
                  const pending = phaseTasks.filter(t => t.status === 'pending').length
                  
                  return (
                    <div key={phase.id} className="p-4 border rounded-lg">
                      <div className="text-sm font-medium mb-2">{phase.name}</div>
                      <div className="space-y-1 text-xs">
                        <div className="flex justify-between">
                          <span>Total:</span>
                          <span className="font-medium">{phaseTasks.length}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-green-600">Completed:</span>
                          <span className="font-medium">{completed}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-yellow-600">In Progress:</span>
                          <span className="font-medium">{inProgress}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-blue-600">Pending:</span>
                          <span className="font-medium">{pending}</span>
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>
            </TabsContent>

            <TabsContent value="deep-research" className="space-y-4">
              <div className="p-4 border rounded-lg bg-blue-50 dark:bg-blue-950">
                <div className="flex items-center gap-2 mb-2">
                  <Search className="h-5 w-5 text-blue-600" />
                  <div className="font-semibold">Google Deep Research Integration</div>
                </div>
                <p className="text-sm text-muted-foreground mb-4">
                  Deep Research Agent uses Google Gemini Deep Research to generate comprehensive
                  research reports with multi-source synthesis.
                </p>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-green-600" />
                    <span>Multi-source research synthesis</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-green-600" />
                    <span>Google Workspace integration (Drive, Gmail, Chat)</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-green-600" />
                    <span>Enhanced bookmark context generation</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-green-600" />
                    <span>Cross-reference discovery</span>
                  </div>
                </div>
                <Button
                  onClick={() => handleExecuteAgent('deep_research')}
                  disabled={executing === 'deep_research'}
                  className="mt-4"
                  variant="outline"
                >
                  {executing === 'deep_research' ? (
                    <>
                      <Pause className="mr-2 h-4 w-4 animate-spin" />
                      Executing Deep Research...
                    </>
                  ) : (
                    <>
                      <Search className="mr-2 h-4 w-4" />
                      Execute Deep Research
                    </>
                  )}
                </Button>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}

