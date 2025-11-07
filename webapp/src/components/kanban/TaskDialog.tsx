import { useState, useEffect } from 'react'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { MetadataEditor } from '@/components/ui/metadata-editor'
import { useTask, useCreateTask, useUpdateTask, usePhases, useRoles, usePriorities } from '@/lib/queries'
import { TaskCreate, TaskUpdate } from '@/lib/api'

interface TaskDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  taskId: string | null
  onClose: () => void
}

export function TaskDialog({ open, onOpenChange, taskId, onClose }: TaskDialogProps) {
  const { data: task } = useTask(taskId || '')
  const { data: phases = [] } = usePhases()
  const { data: roles = [] } = useRoles()
  const { data: priorities = [] } = usePriorities()
  const createTask = useCreateTask()
  const updateTask = useUpdateTask()

  const [formData, setFormData] = useState({
    content: '',
    status: 'pending',
    phase: 'phase1_basic',
    role: 'developer',
    priority: 'medium',
    cost: 0,
    tags: [] as string[],
    resources: [] as string[],
    labels: [] as string[],
    assigned_to: '',
    project_id: '',
    due_date: '',
    estimated_hours: '',
    progress: 0,
    dependencies: [] as string[],
    metadata: {} as Record<string, any>,
    links: '',
  })
  const [tagInput, setTagInput] = useState('')

  useEffect(() => {
    if (task) {
      setFormData({
        content: task.content || '',
        status: task.status || 'pending',
        phase: task.phase || 'phase1_basic',
        role: task.role || 'developer',
        priority: task.priority || 'medium',
        cost: task.cost || 0,
        tags: task.tags || [],
        resources: task.resources || [],
        labels: task.labels || [],
        assigned_to: task.assigned_to || '',
        project_id: task.project_id || '',
        due_date: task.due_date ? task.due_date.split('T')[0] : '',
        estimated_hours: task.estimated_hours?.toString() || '',
        progress: task.progress || 0,
        dependencies: task.dependencies || [],
        metadata: task.metadata || {},
        links: (task.links || []).join('\n'),
      })
    } else {
      setFormData({
        content: '',
        status: 'pending',
        phase: 'phase1_basic',
        role: 'developer',
        priority: 'medium',
        cost: 0,
        tags: [],
        resources: [],
        labels: [],
        assigned_to: '',
        project_id: '',
        due_date: '',
        estimated_hours: '',
        progress: 0,
        dependencies: [],
        metadata: {},
        links: '',
      })
    }
    setTagInput('')
  }, [task, open])

  const handleAddTag = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && tagInput.trim()) {
      e.preventDefault()
      setFormData({
        ...formData,
        tags: [...formData.tags, tagInput.trim()],
      })
      setTagInput('')
    }
  }

  const handleRemoveTag = (index: number) => {
    setFormData({
      ...formData,
      tags: formData.tags.filter((_, i) => i !== index),
    })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    const links = formData.links
      .split('\n')
      .map((link) => link.trim())
      .filter((link) => link.length > 0)

    const resources = formData.resources
      .map((r) => r.trim())
      .filter((r) => r.length > 0)

    const dependencies = formData.dependencies
      .map((d) => d.trim())
      .filter((d) => d.length > 0)

    if (taskId) {
      const update: TaskUpdate = {
        content: formData.content,
        status: formData.status,
        phase: formData.phase,
        role: formData.role,
        priority: formData.priority,
        cost: formData.cost,
        tags: formData.tags,
        resources,
        labels: formData.labels,
        assigned_to: formData.assigned_to || undefined,
        project_id: formData.project_id || undefined,
        due_date: formData.due_date || undefined,
        estimated_hours: formData.estimated_hours ? parseFloat(formData.estimated_hours) : undefined,
        progress: formData.progress,
        dependencies,
        metadata: formData.metadata,
        links,
      }
      updateTask.mutate({ id: taskId, task: update }, { onSuccess: onClose })
    } else {
      const create: TaskCreate = {
        content: formData.content,
        status: formData.status,
        phase: formData.phase,
        role: formData.role,
        priority: formData.priority,
        cost: formData.cost,
        tags: formData.tags,
        resources,
        labels: formData.labels,
        assigned_to: formData.assigned_to || undefined,
        project_id: formData.project_id || undefined,
        due_date: formData.due_date || undefined,
        estimated_hours: formData.estimated_hours ? parseFloat(formData.estimated_hours) : undefined,
        progress: formData.progress,
        dependencies,
        metadata: formData.metadata,
        links,
      }
      createTask.mutate(create, { onSuccess: onClose })
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[700px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{taskId ? 'Edit Task' : 'Create Task'}</DialogTitle>
          <DialogDescription>
            {taskId ? 'Update the task details below.' : 'Fill in the details to create a new task.'}
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="space-y-4 py-4">
            {/* Basic Fields */}
            <div className="space-y-2">
              <Label htmlFor="content">Content *</Label>
              <Textarea
                id="content"
                value={formData.content}
                onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                required
                rows={4}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="status">Status</Label>
                <Select
                  value={formData.status}
                  onValueChange={(value) => setFormData({ ...formData, status: value })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="pending">Pending</SelectItem>
                    <SelectItem value="in_progress">In Progress</SelectItem>
                    <SelectItem value="completed">Completed</SelectItem>
                    <SelectItem value="archived">Archived</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="priority">Priority</Label>
                <Select
                  value={formData.priority}
                  onValueChange={(value) => setFormData({ ...formData, priority: value })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {priorities.length > 0 ? (
                      priorities.map((p) => (
                        <SelectItem key={p} value={p}>
                          {p.charAt(0).toUpperCase() + p.slice(1)}
                        </SelectItem>
                      ))
                    ) : (
                      <>
                        <SelectItem value="low">Low</SelectItem>
                        <SelectItem value="medium">Medium</SelectItem>
                        <SelectItem value="high">High</SelectItem>
                        <SelectItem value="critical">Critical</SelectItem>
                      </>
                    )}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="phase">Phase</Label>
                <Select
                  value={formData.phase}
                  onValueChange={(value) => setFormData({ ...formData, phase: value })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {phases.length > 0 ? (
                      phases.map((phase) => (
                        <SelectItem key={phase.name} value={phase.name}>
                          {phase.display}
                        </SelectItem>
                      ))
                    ) : (
                      <>
                        <SelectItem value="phase1_basic">Phase 1: Foundation</SelectItem>
                        <SelectItem value="phase2_deep">Phase 2: Deep Analysis</SelectItem>
                        <SelectItem value="phase3_advanced">Phase 3: Advanced</SelectItem>
                        <SelectItem value="phase4_scale">Phase 4: Scale</SelectItem>
                      </>
                    )}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="role">Role</Label>
                <Select
                  value={formData.role}
                  onValueChange={(value) => setFormData({ ...formData, role: value })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {roles.length > 0 ? (
                      roles.map((role) => (
                        <SelectItem key={role.name} value={role.name}>
                          {role.display}
                        </SelectItem>
                      ))
                    ) : (
                      <>
                        <SelectItem value="project_manager">Project Manager</SelectItem>
                        <SelectItem value="product_manager">Product Manager</SelectItem>
                        <SelectItem value="developer">Developer</SelectItem>
                        <SelectItem value="designer">Designer</SelectItem>
                        <SelectItem value="qa">QA Engineer</SelectItem>
                      </>
                    )}
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Tags */}
            <div className="space-y-2">
              <Label htmlFor="tags">Tags</Label>
              <Input
                id="tags"
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyDown={handleAddTag}
                placeholder="Add tag and press Enter"
              />
              {formData.tags.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-2">
                  {formData.tags.map((tag, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-purple-100 text-purple-700 rounded text-sm flex items-center gap-1"
                    >
                      {tag}
                      <button
                        type="button"
                        onClick={() => handleRemoveTag(index)}
                        className="text-purple-700 hover:text-purple-900"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              )}
            </div>

            {/* Progress */}
            <div className="space-y-2">
              <Label htmlFor="progress">Progress: {formData.progress}%</Label>
              <Input
                id="progress"
                type="range"
                min="0"
                max="100"
                value={formData.progress}
                onChange={(e) => setFormData({ ...formData, progress: parseInt(e.target.value) })}
              />
            </div>

            {/* Additional Fields */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="assigned_to">Assigned To</Label>
                <Input
                  id="assigned_to"
                  value={formData.assigned_to}
                  onChange={(e) => setFormData({ ...formData, assigned_to: e.target.value })}
                  placeholder="User name or email"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="due_date">Due Date</Label>
                <Input
                  id="due_date"
                  type="date"
                  value={formData.due_date}
                  onChange={(e) => setFormData({ ...formData, due_date: e.target.value })}
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="estimated_hours">Estimated Hours</Label>
                <Input
                  id="estimated_hours"
                  type="number"
                  step="0.5"
                  min="0"
                  value={formData.estimated_hours}
                  onChange={(e) => setFormData({ ...formData, estimated_hours: e.target.value })}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="cost">Cost</Label>
                <Input
                  id="cost"
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.cost}
                  onChange={(e) => setFormData({ ...formData, cost: parseFloat(e.target.value) || 0 })}
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="project_id">Project ID</Label>
              <Input
                id="project_id"
                value={formData.project_id}
                onChange={(e) => setFormData({ ...formData, project_id: e.target.value })}
                placeholder="Project identifier"
              />
            </div>

            {/* Resources */}
            <div className="space-y-2">
              <Label htmlFor="resources">Resources (one per line)</Label>
              <Textarea
                id="resources"
                value={formData.resources.join('\n')}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    resources: e.target.value.split('\n').map((r) => r.trim()),
                  })
                }
                rows={3}
                placeholder="https://example.com/resource"
              />
            </div>

            {/* Links */}
            <div className="space-y-2">
              <Label htmlFor="links">Links (one per line)</Label>
              <Textarea
                id="links"
                value={formData.links}
                onChange={(e) => setFormData({ ...formData, links: e.target.value })}
                rows={3}
                placeholder="https://example.com"
              />
            </div>

            {/* Dependencies */}
            <div className="space-y-2">
              <Label htmlFor="dependencies">Dependencies (task IDs, one per line)</Label>
              <Textarea
                id="dependencies"
                value={formData.dependencies.join('\n')}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    dependencies: e.target.value.split('\n').map((d) => d.trim()),
                  })
                }
                rows={2}
                placeholder="task-id-1"
              />
            </div>

            {/* Metadata Editor */}
            <MetadataEditor
              value={formData.metadata}
              onChange={(value) => setFormData({ ...formData, metadata: value })}
            />
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" disabled={createTask.isPending || updateTask.isPending}>
              {taskId ? 'Update' : 'Create'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
