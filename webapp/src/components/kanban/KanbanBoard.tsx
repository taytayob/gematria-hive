import { useTasks, useUpdateTaskStatus } from '@/lib/queries'
import { KanbanColumn } from './KanbanColumn'
import { StatisticsPanel } from './StatisticsPanel'
import { FilterPanel } from './FilterPanel'
import { Button } from '@/components/ui/button'
import { Plus } from 'lucide-react'
import { TaskDialog } from './TaskDialog'
import { useState, useMemo } from 'react'
import { Task } from '@/lib/api'

const COLUMNS = [
  { id: 'pending', title: '📝 Pending', status: 'pending' },
  { id: 'in_progress', title: '🔄 In Progress', status: 'in_progress' },
  { id: 'completed', title: '✅ Completed', status: 'completed' },
  { id: 'archived', title: '📦 Archived', status: 'archived' },
] as const

export function KanbanBoard() {
  const { data: tasks = [], isLoading } = useTasks()
  const updateStatus = useUpdateTaskStatus()
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [editingTaskId, setEditingTaskId] = useState<string | null>(null)
  const [phaseFilter, setPhaseFilter] = useState<string | null>(null)
  const [filters, setFilters] = useState<{
    phase?: string
    role?: string
    priority?: string
    tag?: string
  }>({})

  const filteredTasks = useMemo(() => {
    let filtered: Task[] = [...tasks]

    if (filters.phase) {
      filtered = filtered.filter((task) => task.phase === filters.phase)
    }

    if (filters.role) {
      filtered = filtered.filter((task) => task.role === filters.role)
    }

    if (filters.priority) {
      filtered = filtered.filter((task) => task.priority === filters.priority)
    }

    if (filters.tag) {
      filtered = filtered.filter(
        (task) => task.tags && task.tags.some((tag) => tag.toLowerCase().includes(filters.tag!.toLowerCase()))
      )
    }

    return filtered
  }, [tasks, filters])

  const handleDragEnd = (taskId: string, newStatus: string) => {
    updateStatus.mutate({ id: taskId, status: newStatus })
  }

  const handleEditTask = (taskId: string) => {
    setEditingTaskId(taskId)
    setIsDialogOpen(true)
  }

  const handleCreateTask = () => {
    setEditingTaskId(null)
    setIsDialogOpen(true)
  }

  const handleDialogClose = () => {
    setIsDialogOpen(false)
    setEditingTaskId(null)
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-muted-foreground">Loading tasks...</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold">Kanban Board</h1>
        <p className="text-muted-foreground mt-2">
          Manage and track your tasks with drag-and-drop
        </p>
      </div>

      {/* Header Actions */}
      <div className="flex items-center justify-end gap-3">
        <Button variant="outline" onClick={() => window.location.reload()}>
          🔄 Refresh
        </Button>
        <Button onClick={handleCreateTask}>
          <Plus className="mr-2 h-4 w-4" />
          New Task
        </Button>
      </div>

      {/* Statistics */}
      <StatisticsPanel />

      {/* Filter Panel */}
      <FilterPanel filters={filters} onFiltersChange={setFilters} />

      {/* Kanban Columns */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {COLUMNS.map((column) => {
          const columnTasks = filteredTasks.filter((task) => task.status === column.status)
          return (
            <KanbanColumn
              key={column.id}
              title={column.title}
              status={column.status}
              tasks={columnTasks}
              onDragEnd={handleDragEnd}
              onEditTask={handleEditTask}
            />
          )
        })}
      </div>

      {/* Task Dialog */}
      <TaskDialog
        open={isDialogOpen}
        onOpenChange={setIsDialogOpen}
        taskId={editingTaskId}
        onClose={handleDialogClose}
      />
    </div>
  )
}

