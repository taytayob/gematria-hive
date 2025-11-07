# Navigation & Pages Guide

This document describes all the pages and navigation in the Gematria Hive webapp.

## Navigation Structure

The app uses a **sidebar navigation** with the following pages:

### 🏠 Dashboard (`/`)
- **Overview** of the entire system
- **Statistics cards** showing:
  - Total tasks
  - Pending tasks
  - In progress tasks
  - Total cost
- **Quick links** to other pages
- **Recent activity** feed

### 📋 Kanban Board (`/kanban`)
- **Drag-and-drop** task management
- **Four columns**: Pending, In Progress, Completed, Archived
- **Task cards** with:
  - Content preview
  - Cost information
  - Tags
  - Links
  - Edit/Delete actions
- **Statistics panel** at the top
- **Create/Edit task** dialog

### 🧮 Gematria Calculator (`/calculator`)
- **Text input** for calculating gematria values
- **Two calculation methods**:
  - **Standard Gematria**: A=1, B=2... Z=26
  - **Reduced Gematria**: A=1... I=9, J=1... R=9, S=1... Z=8
- **Real-time calculation** on input
- **Information** about gematria methods

### 📊 Statistics (`/statistics`)
- **Overview cards**:
  - Total tasks
  - Completed tasks with completion rate
  - Total cost
  - Average cost per task
- **Tabbed interface** with:
  - **Status Breakdown**: Visual distribution of tasks by status
  - **Cost Analysis**: Financial breakdown and metrics
  - **Timeline**: Recent task activity sorted by date

### 🤖 Agents (`/agents`)
- **Agent overview**:
  - Active agents count
  - Total tasks processed
  - System health status
- **Agent cards** showing:
  - Agent name and description
  - Status (active/idle)
  - Last run time
  - Tasks processed count
  - Action buttons
- **Recent activity** feed showing agent operations

### ⚙️ Settings (`/settings`)
- **Tabbed interface** with:
  - **General**: Theme, auto-refresh, refresh interval
  - **API**: API base URL configuration, connection status
  - **Display**: Items per page, date format
  - **Notifications**: Toggle notifications for various events
- **Save settings** button

## Navigation Features

### Sidebar Navigation
- **Fixed sidebar** on desktop (left side)
- **Mobile-responsive** with hamburger menu
- **Active route highlighting** - current page is highlighted
- **Icons** for each navigation item
- **Logo** and version number at top

### Mobile Navigation
- **Hamburger menu** button (top-left on mobile)
- **Overlay** when menu is open
- **Auto-close** when clicking outside or selecting a route

## Component Usage

All pages use **shadcn/ui components** consistently:
- `Card` - Container components
- `Button` - Action buttons
- `Input` - Text inputs
- `Select` - Dropdown selects
- `Tabs` - Tabbed interfaces
- `Badge` - Status indicators
- `Dialog` - Modals
- `Toast` - Notifications

## Data Fetching

All pages use **TanStack Query** for data fetching:
- `useStatistics()` - Fetch statistics
- `useTasks()` - Fetch all tasks
- `useTask(id)` - Fetch single task
- `useCreateTask()` - Create new task
- `useUpdateTask()` - Update task
- `useDeleteTask()` - Delete task

## Routing

The app uses **TanStack Router** for type-safe routing:
- File-based routing in `src/routes/`
- Type-safe navigation with `Link` component
- Active route detection for navigation highlighting

## Responsive Design

- **Desktop**: Sidebar always visible, full-width content
- **Tablet**: Sidebar can be toggled
- **Mobile**: Sidebar hidden by default, accessible via hamburger menu

## Theme

- **Light theme** by default (configurable in Settings)
- **Purple accent color** matching Gematria Hive brand
- **Consistent spacing** and typography throughout

