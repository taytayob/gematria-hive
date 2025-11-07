# Webapp Setup Guide

This guide will help you set up and run the Gematria Hive webapp frontend.

## Prerequisites

- **Node.js** 18 or higher
- **npm**, **yarn**, or **pnpm** package manager
- Backend API running at `http://localhost:8000` (or configure proxy)

## Quick Start

### 1. Install Dependencies

```bash
cd webapp
npm install
```

### 2. Configure Environment (Optional)

Copy `.env.example` to `.env` and adjust if needed:

```bash
cp .env.example .env
```

By default, the app proxies API requests to `http://localhost:8000` via Vite's proxy configuration.

### 3. Start Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`.

### 4. Start Backend API

In a separate terminal, start the FastAPI backend:

```bash
# From project root
python kanban_api.py
```

The backend should be running at `http://localhost:8000`.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Tech Stack Overview

### shadcn/ui Components

We use shadcn/ui for all UI components. Components are located in `src/components/ui/`:

- **Button** - Primary action buttons
- **Card** - Container components
- **Dialog** - Modal dialogs
- **Input** - Text inputs
- **Label** - Form labels
- **Select** - Dropdown selects
- **Textarea** - Multi-line text inputs
- **Toast** - Notification toasts

### TanStack Query

Used for all data fetching and server state management:

- **useTasks** - Fetch all tasks
- **useTask** - Fetch single task
- **useCreateTask** - Create new task
- **useUpdateTask** - Update existing task
- **useUpdateTaskStatus** - Update task status (drag & drop)
- **useDeleteTask** - Delete task
- **useStatistics** - Fetch statistics

All queries are defined in `src/lib/queries.ts`.

### API Client

The API client is in `src/lib/api.ts` and provides type-safe methods for all backend endpoints.

## Project Structure

```
webapp/
├── src/
│   ├── components/
│   │   ├── ui/              # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dialog.tsx
│   │   │   └── ...
│   │   └── kanban/          # Kanban board components
│   │       ├── KanbanBoard.tsx
│   │       ├── KanbanColumn.tsx
│   │       ├── KanbanCard.tsx
│   │       ├── StatisticsPanel.tsx
│   │       └── TaskDialog.tsx
│   ├── lib/
│   │   ├── api.ts           # API client
│   │   ├── queries.ts        # TanStack Query hooks
│   │   └── utils.ts         # Utility functions
│   ├── hooks/
│   │   └── use-toast.ts     # Toast notification hook
│   ├── App.tsx              # Main app component
│   ├── main.tsx             # Entry point
│   └── index.css            # Global styles
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## Adding New Components

### Adding shadcn/ui Components

To add new shadcn/ui components, you can copy them from the [shadcn/ui documentation](https://ui.shadcn.com/) or use the CLI:

```bash
npx shadcn-ui@latest add [component-name]
```

### Creating Custom Components

1. Create component file in appropriate directory
2. Use existing shadcn/ui components as building blocks
3. Follow TypeScript best practices
4. Add proper prop types

## Styling

We use **Tailwind CSS** for all styling. The theme is configured in `tailwind.config.js` and uses CSS variables for theming (defined in `src/index.css`).

### Color Scheme

The app uses a purple gradient theme matching the Gematria Hive brand:
- Primary: Purple (`hsl(262.1 83.3% 57.8%)`)
- Background: White/Light
- Cards: White with shadows

## Type Safety

All API types are defined in `src/lib/api.ts`:
- `Task` - Task data structure
- `TaskCreate` - Task creation payload
- `TaskUpdate` - Task update payload
- `Statistics` - Statistics data structure

## Future Enhancements

- [ ] Add TanStack Router for multi-page navigation
- [ ] Use TanStack Table for advanced data tables
- [ ] Use TanStack Form for complex form validation
- [ ] Add more shadcn/ui components as needed
- [ ] Implement real-time updates with WebSockets
- [ ] Add filtering and search functionality
- [ ] Add dark mode support
- [ ] Add task filtering by phase, role, priority
- [ ] Add task tags and labels UI
- [ ] Add task dependencies visualization

## Troubleshooting

### Port Already in Use

If port 3000 is already in use, Vite will automatically try the next available port. Check the terminal output for the actual port.

### API Connection Issues

1. Ensure the backend is running at `http://localhost:8000`
2. Check CORS settings in `kanban_api.py`
3. Verify the proxy configuration in `vite.config.ts`

### Build Errors

1. Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
2. Clear Vite cache: `rm -rf node_modules/.vite`
3. Check TypeScript errors: `npm run build`

## Development Tips

1. **Hot Module Replacement (HMR)** - Changes should reflect immediately
2. **TypeScript** - Use strict mode for better type safety
3. **React DevTools** - Install browser extension for debugging
4. **TanStack Query DevTools** - Consider adding for query debugging

