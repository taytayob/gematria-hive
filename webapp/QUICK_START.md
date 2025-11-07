# Quick Start Guide

Get the Gematria Hive webapp up and running in minutes!

## Prerequisites

- **Node.js** 18+ installed
- **npm**, **yarn**, or **pnpm** package manager
- Backend API running (optional for development)

## Installation

### 1. Install Dependencies

```bash
cd webapp
npm install
```

This will install all required dependencies including:
- React 18
- TypeScript
- Vite
- shadcn/ui components
- TanStack Query, Router, Table, Form
- Tailwind CSS
- And more...

### 2. Start Development Server

```bash
npm run dev
```

The app will start at `http://localhost:3000`

### 3. Start Backend API (Optional)

In a separate terminal, start the FastAPI backend:

```bash
# From project root
python kanban_api.py
```

The backend should run at `http://localhost:8000`

## Available Scripts

```bash
# Development
npm run dev          # Start dev server with hot reload

# Build
npm run build        # Build for production
npm run preview      # Preview production build

# Code Quality
npm run lint         # Run ESLint
```

## First Time Setup

1. **Install dependencies**: `npm install`
2. **Start dev server**: `npm run dev`
3. **Open browser**: Navigate to `http://localhost:3000`
4. **Explore pages**: Use the sidebar to navigate between pages

## Project Structure

```
webapp/
├── src/
│   ├── routes/          # TanStack Router routes
│   │   ├── __root.tsx   # Root layout
│   │   ├── index.tsx    # Dashboard
│   │   ├── kanban.tsx   # Kanban board
│   │   ├── calculator.tsx
│   │   ├── statistics.tsx
│   │   ├── agents.tsx
│   │   └── settings.tsx
│   ├── components/
│   │   ├── ui/          # shadcn/ui components
│   │   ├── kanban/      # Kanban board components
│   │   └── Layout.tsx   # Main layout
│   ├── lib/
│   │   ├── api.ts       # API client
│   │   ├── queries.ts   # TanStack Query hooks
│   │   └── utils.ts     # Utilities
│   ├── hooks/           # Custom React hooks
│   ├── App.tsx          # Main app component
│   ├── router.tsx        # Router configuration
│   └── main.tsx          # Entry point
├── package.json
├── vite.config.ts
└── tailwind.config.js
```

## Troubleshooting

### Port Already in Use

If port 3000 is in use, Vite will automatically try the next available port. Check the terminal output.

### API Connection Issues

1. Ensure backend is running: `python kanban_api.py`
2. Check CORS settings in `kanban_api.py`
3. Verify proxy in `vite.config.ts` points to correct backend URL

### Build Errors

1. Clear cache: `rm -rf node_modules/.vite`
2. Reinstall: `rm -rf node_modules && npm install`
3. Check TypeScript: `npm run build`

### TypeScript Errors

1. Check `tsconfig.json` configuration
2. Ensure all imports are correct
3. Run `npm run build` to see all errors

## Development Tips

1. **Hot Module Replacement**: Changes reflect immediately
2. **TypeScript**: Use strict mode for better type safety
3. **React DevTools**: Install browser extension for debugging
4. **TanStack Query DevTools**: Consider adding for query debugging

## Next Steps

- Explore all pages via sidebar navigation
- Check out `NAVIGATION.md` for page descriptions
- Read `ARCHITECTURE.md` for technical details
- Review `SETUP.md` for detailed setup instructions

## Need Help?

- Check `SETUP.md` for detailed setup
- Review `ARCHITECTURE.md` for architecture decisions
- See `NAVIGATION.md` for navigation structure
- Check console for errors

Happy coding! 🐝

