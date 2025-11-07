import { Task } from '@/lib/api'
import { KanbanCard } from './KanbanCard'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface KanbanColumnProps {
  title: string
  status: string
  tasks: Task[]
  onDragEnd: (taskId: string, newStatus: string) => void
  onEditTask: (taskId: string) => void
}

export function KanbanColumn({ title, status, tasks, onDragEnd, onEditTask }: KanbanColumnProps) {
  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    const taskId = e.dataTransfer.getData('taskId')
    if (taskId) {
      onDragEnd(taskId, status)
    }
  }

  return (
    <Card className="bg-white shadow-lg min-h-[600px]">
      <CardHeader className="border-b pb-4">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-bold">{title}</CardTitle>
          <span className="bg-primary text-primary-foreground px-3 py-1 rounded-full text-sm font-semibold">
            {tasks.length}
          </span>
        </div>
      </CardHeader>
      <CardContent
        className="p-4 space-y-3 min-h-[500px]"
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        {tasks.map((task) => (
          <KanbanCard
            key={task.id}
            task={task}
            onEdit={onEditTask}
          />
        ))}
        {tasks.length === 0 && (
          <div className="text-center text-muted-foreground py-8">
            No tasks in this column
          </div>
        )}
      </CardContent>
    </Card>
  )
}

