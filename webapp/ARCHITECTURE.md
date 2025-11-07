# Webapp Architecture

## Decision: Use shadcn/ui and TanStack

After research, we've decided to use **shadcn/ui** and **TanStack** for the frontend. Here's why:

### shadcn/ui
- ✅ **Accessible by default** - Built on Radix UI primitives
- ✅ **Customizable** - Copy components into your project, full control
- ✅ **Modern design** - Beautiful, consistent components
- ✅ **TypeScript-first** - Full type safety
- ✅ **Tailwind CSS** - Utility-first styling
- ✅ **No runtime dependencies** - Components are part of your codebase

### TanStack Suite
- ✅ **TanStack Query** - Industry-standard server state management
  - Automatic caching, refetching, background updates
  - Optimistic updates
  - Error handling and retries
- ✅ **TanStack Table** - Powerful data tables (available for future use)
  - Headless, fully customizable
  - Sorting, filtering, pagination
- ✅ **TanStack Router** - Type-safe routing (available for future use)
  - File-based routing
  - Type-safe navigation
- ✅ **TanStack Form** - Headless form management (available for future use)
  - Type-safe forms
  - Validation with Zod

## Architecture Overview

```
┌─────────────────────────────────────────┐
│         React App (App.tsx)             │
│  ┌───────────────────────────────────┐  │
│  │   QueryClientProvider             │  │
│  │  ┌─────────────────────────────┐ │  │
│  │  │  KanbanBoard Component      │ │  │
│  │  │  ┌───────────────────────┐   │ │  │
│  │  │  │  TanStack Query      │   │ │  │
│  │  │  │  Hooks (useTasks,    │   │ │  │
│  │  │  │   useCreateTask, etc)│   │ │  │
│  │  │  └───────────────────────┘   │ │  │
│  │  │  ┌───────────────────────┐   │ │  │
│  │  │  │  shadcn/ui Components │   │ │  │
│  │  │  │  (Button, Card,       │   │ │  │
│  │  │  │   Dialog, etc)        │   │ │  │
│  │  │  └───────────────────────┘   │ │  │
│  │  └─────────────────────────────┘ │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│         API Client (lib/api.ts)          │
│  - Type-safe API methods                │
│  - Task CRUD operations                 │
│  - Statistics fetching                  │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│      FastAPI Backend (kanban_api.py)    │
│  - REST API endpoints                   │
│  - Task management                      │
│  - Statistics                           │
└─────────────────────────────────────────┘
```

## Component Structure

### UI Components (shadcn/ui)
Located in `src/components/ui/`:
- **Button** - Primary action buttons with variants
- **Card** - Container components
- **Dialog** - Modal dialogs
- **Input** - Text inputs
- **Label** - Form labels
- **Select** - Dropdown selects
- **Textarea** - Multi-line text inputs
- **Toast** - Notification toasts

### Feature Components
Located in `src/components/kanban/`:
- **KanbanBoard** - Main board container
- **KanbanColumn** - Individual column (Pending, In Progress, etc.)
- **KanbanCard** - Task card with drag & drop
- **StatisticsPanel** - Statistics display
- **TaskDialog** - Create/Edit task modal

## Data Flow

1. **Component renders** → Calls TanStack Query hook (e.g., `useTasks()`)
2. **Query hook** → Checks cache, fetches if needed
3. **API client** → Makes HTTP request to FastAPI backend
4. **Backend** → Returns data
5. **Query hook** → Updates cache, triggers re-render
6. **Component** → Displays data

### Mutations (Create/Update/Delete)

1. **User action** → Calls mutation hook (e.g., `useCreateTask()`)
2. **Mutation hook** → Optimistically updates cache
3. **API client** → Makes HTTP request
4. **Backend** → Processes request
5. **Mutation hook** → Invalidates queries, refetches data
6. **Component** → Updates with new data

## State Management

### Server State (TanStack Query)
- Tasks list
- Individual tasks
- Statistics
- All managed by TanStack Query with automatic caching

### Local State (React useState)
- Dialog open/close state
- Form data
- UI interactions

## Styling

- **Tailwind CSS** - Utility-first CSS
- **CSS Variables** - Theming (defined in `index.css`)
- **shadcn/ui** - Pre-styled components with Tailwind

## Type Safety

- **TypeScript** - Full type coverage
- **API Types** - Defined in `lib/api.ts`
- **Component Props** - Typed with TypeScript interfaces
- **Query Hooks** - Fully typed with generics

## Future Enhancements

### TanStack Router
- Add file-based routing
- Type-safe navigation
- Route-based code splitting

### TanStack Table
- Advanced task tables
- Sorting, filtering, pagination
- Export functionality

### TanStack Form
- Complex form validation
- Multi-step forms
- Field-level validation

### Additional shadcn/ui Components
- Data tables
- Charts
- Date pickers
- Dropdown menus
- Tooltips
- Popovers

## Consistency Across Frontend

All frontend code follows these patterns:

1. **shadcn/ui components** - Use for all UI elements
2. **TanStack Query** - Use for all data fetching
3. **TypeScript** - Strict typing everywhere
4. **Tailwind CSS** - Consistent styling
5. **Component composition** - Build complex UIs from simple components

This ensures:
- ✅ Consistent look and feel
- ✅ Reusable components
- ✅ Type safety
- ✅ Maintainable codebase
- ✅ Easy to extend

