import { createRouter } from '@tanstack/react-router'
import { rootRoute } from './routes/__root'
import { indexRoute } from './routes/index'
import { kanbanRoute } from './routes/kanban'
import { pipelineRoute } from './routes/pipeline'
import { researchRoute } from './routes/research'
import { calculatorRoute } from './routes/calculator'
import { statisticsRoute } from './routes/statistics'
import { agentsRoute } from './routes/agents'
import { settingsRoute } from './routes/settings'

// Create the route tree
const routeTree = rootRoute.addChildren([
  indexRoute,
  kanbanRoute,
  pipelineRoute,
  researchRoute,
  calculatorRoute,
  statisticsRoute,
  agentsRoute,
  settingsRoute,
])

// Create the router
export const router = createRouter({ routeTree })

// Register the router instance for type safety
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}

