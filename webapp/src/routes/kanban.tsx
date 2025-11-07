import { createRoute } from '@tanstack/react-router'
import { rootRoute } from './__root'
import { KanbanBoard } from '@/components/kanban/KanbanBoard'

export const kanbanRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/kanban',
  component: KanbanPage,
})

function KanbanPage() {
  return <KanbanBoard />
}

