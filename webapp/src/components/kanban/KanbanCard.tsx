import { Task } from '@/lib/api'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { useDeleteTask } from '@/lib/queries'
import { format } from 'date-fns'
import { Edit, Trash2 } from 'lucide-react'

interface KanbanCardProps {
  task: Task
  onEdit: (taskId: string) => void
}

const getPhaseColor = (phase?: string) => {
  if (!phase) return 'bg-gray-100 text-gray-700'
  if (phase.includes('phase1')) return 'bg-blue-100 text-blue-700'
  if (phase.includes('phase2')) return 'bg-green-100 text-green-700'
  if (phase.includes('phase3')) return 'bg-yellow-100 text-yellow-700'
  if (phase.includes('phase4')) return 'bg-purple-100 text-purple-700'
  return 'bg-gray-100 text-gray-700'
}

const getPriorityColor = (priority?: string) => {
  if (!priority) return 'bg-gray-100 text-gray-700'
  if (priority === 'low') return 'bg-gray-100 text-gray-700'
  if (priority === 'medium') return 'bg-blue-100 text-blue-700'
  if (priority === 'high') return 'bg-orange-100 text-orange-700'
  if (priority === 'critical') return 'bg-red-100 text-red-700'
  return 'bg-gray-100 text-gray-700'
}

const getRoleColor = (role?: string) => {
  if (!role) return 'bg-gray-100 text-gray-700'
  const colors: Record<string, string> = {
    project_manager: 'bg-purple-100 text-purple-700',
    product_manager: 'bg-indigo-100 text-indigo-700',
    developer: 'bg-blue-100 text-blue-700',
    designer: 'bg-pink-100 text-pink-700',
    qa: 'bg-green-100 text-green-700',
  }
  return colors[role] || 'bg-gray-100 text-gray-700'
}

export function KanbanCard({ task, onEdit }: KanbanCardProps) {
  const deleteTask = useDeleteTask()

  const handleDragStart = (e: React.DragEvent) => {
    e.dataTransfer.setData('taskId', task.id)
    e.dataTransfer.effectAllowed = 'move'
  }

  const handleDelete = async (e: React.MouseEvent) => {
    e.stopPropagation()
    if (window.confirm('Are you sure you want to delete this task?')) {
      deleteTask.mutate(task.id)
    }
  }

  return (
    <Card
      draggable
      onDragStart={handleDragStart}
      className="cursor-move hover:border-primary hover:shadow-md transition-all bg-white"
    >
      <div className="p-4 space-y-3">
        {/* Content */}
        <p className="text-sm text-gray-800 leading-relaxed">{task.content}</p>
        
        {/* Badges Row */}
        <div className="flex flex-wrap gap-1 items-center">
          {task.phase && (
            <Badge variant="outline" className={`text-xs ${getPhaseColor(task.phase)}`}>
              {task.phase.replace('phase', 'P').replace('_', ' ')}
            </Badge>
          )}
          {task.role && (
            <Badge variant="outline" className={`text-xs ${getRoleColor(task.role)}`}>
              {task.role.replace('_', ' ')}
            </Badge>
          )}
          {task.priority && (
            <Badge variant="outline" className={`text-xs ${getPriorityColor(task.priority)}`}>
              {task.priority}
            </Badge>
          )}
        </div>

        {/* Progress Bar */}
        {task.progress !== undefined && task.progress > 0 && (
          <div className="space-y-1">
            <div className="flex items-center justify-between text-xs text-gray-600">
              <span>Progress</span>
              <span>{task.progress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all"
                style={{ width: `${task.progress}%` }}
              />
            </div>
          </div>
        )}

        {/* Tags */}
        {task.tags && task.tags.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {task.tags.slice(0, 3).map((tag, idx) => (
              <span
                key={idx}
                className="px-2 py-0.5 bg-purple-100 text-purple-700 rounded text-xs"
              >
                #{tag}
              </span>
            ))}
            {task.tags.length > 3 && (
              <span className="px-2 py-0.5 bg-gray-100 text-gray-600 rounded text-xs">
                +{task.tags.length - 3}
              </span>
            )}
          </div>
        )}

        {/* Metadata Row */}
        <div className="flex items-center justify-between text-xs text-gray-600 pt-2 border-t">
          <div className="flex items-center gap-3">
            <span>{format(new Date(task.timestamp), 'MMM d, yyyy')}</span>
            {task.assigned_to && (
              <span className="text-gray-500">@{task.assigned_to}</span>
            )}
          </div>
          {task.cost > 0 && (
            <span className="text-green-600 font-semibold">${task.cost.toFixed(2)}</span>
          )}
        </div>

        {/* Resources and Links Count */}
        {(task.resources?.length > 0 || task.links?.length > 0) && (
          <div className="flex items-center gap-3 text-xs text-gray-500">
            {task.resources && task.resources.length > 0 && (
              <span>📎 {task.resources.length} resource(s)</span>
            )}
            {task.links && task.links.length > 0 && (
              <span>🔗 {task.links.length} link(s)</span>
            )}
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-2 pt-2 border-t">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => onEdit(task.id)}
            className="flex-1"
          >
            <Edit className="h-3 w-3 mr-1" />
            Edit
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleDelete}
            className="text-destructive hover:text-destructive"
          >
            <Trash2 className="h-3 w-3" />
          </Button>
        </div>
      </div>
    </Card>
  )
}
