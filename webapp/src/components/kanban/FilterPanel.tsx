import { useState } from 'react'
import { Card } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { usePhases, useRoles, usePriorities } from '@/lib/queries'
import { X } from 'lucide-react'

interface FilterPanelProps {
  filters: {
    phase?: string
    role?: string
    priority?: string
    tag?: string
  }
  onFiltersChange: (filters: {
    phase?: string
    role?: string
    priority?: string
    tag?: string
  }) => void
}

export function FilterPanel({ filters, onFiltersChange }: FilterPanelProps) {
  const { data: phases = [] } = usePhases()
  const { data: roles = [] } = useRoles()
  const { data: priorities = [] } = usePriorities()
  const [tagInput, setTagInput] = useState(filters.tag || '')

  const handleFilterChange = (key: 'phase' | 'role' | 'priority' | 'tag', value: string) => {
    onFiltersChange({
      ...filters,
      [key]: value || undefined,
    })
    if (key === 'tag') {
      setTagInput(value)
    }
  }

  const clearFilters = () => {
    onFiltersChange({})
    setTagInput('')
  }

  const hasActiveFilters = filters.phase || filters.role || filters.priority || filters.tag

  return (
    <Card className="p-4">
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold">Filters</h3>
          {hasActiveFilters && (
            <Button
              variant="ghost"
              size="sm"
              onClick={clearFilters}
              className="text-xs"
            >
              <X className="h-3 w-3 mr-1" />
              Clear
            </Button>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Phase Filter */}
          <div className="space-y-2">
            <Label htmlFor="filter-phase" className="text-xs">Phase</Label>
            <Select
              value={filters.phase || ''}
              onValueChange={(value) => handleFilterChange('phase', value)}
            >
              <SelectTrigger id="filter-phase" className="h-9">
                <SelectValue placeholder="All phases" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">All phases</SelectItem>
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

          {/* Role Filter */}
          <div className="space-y-2">
            <Label htmlFor="filter-role" className="text-xs">Role</Label>
            <Select
              value={filters.role || ''}
              onValueChange={(value) => handleFilterChange('role', value)}
            >
              <SelectTrigger id="filter-role" className="h-9">
                <SelectValue placeholder="All roles" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">All roles</SelectItem>
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

          {/* Priority Filter */}
          <div className="space-y-2">
            <Label htmlFor="filter-priority" className="text-xs">Priority</Label>
            <Select
              value={filters.priority || ''}
              onValueChange={(value) => handleFilterChange('priority', value)}
            >
              <SelectTrigger id="filter-priority" className="h-9">
                <SelectValue placeholder="All priorities" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">All priorities</SelectItem>
                {priorities.length > 0 ? (
                  priorities.map((priority) => (
                    <SelectItem key={priority} value={priority}>
                      {priority.charAt(0).toUpperCase() + priority.slice(1)}
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

          {/* Tag Filter */}
          <div className="space-y-2">
            <Label htmlFor="filter-tag" className="text-xs">Tag</Label>
            <Input
              id="filter-tag"
              value={tagInput}
              onChange={(e) => {
                setTagInput(e.target.value)
                handleFilterChange('tag', e.target.value)
              }}
              placeholder="Filter by tag"
              className="h-9"
            />
          </div>
        </div>
      </div>
    </Card>
  )
}

