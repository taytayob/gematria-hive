# Gematria Hive Webapp

Modern React/TypeScript frontend for Gematria Hive, built with shadcn/ui and TanStack, integrated with Supabase and Replit.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

Visit **http://localhost:3000**

## ✨ Features

- **6 Pages** - Dashboard, Kanban, Calculator, Statistics, Agents, Settings
- **shadcn/ui** - Accessible component system
- **TanStack** - Query, Router, Table, Form
- **Supabase Integration** - Direct database access
- **Replit Support** - Ready for deployment
- **Responsive Design** - Mobile, tablet, desktop

## 📚 Documentation

- **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)** - Complete setup guide
- **[STACK_INTEGRATION.md](STACK_INTEGRATION.md)** - Supabase & Replit integration
- **[SUPABASE_INTEGRATION.md](SUPABASE_INTEGRATION.md)** - Supabase setup
- **[REPLIT_SETUP.md](REPLIT_SETUP.md)** - Replit deployment
- **[QUICK_START.md](QUICK_START.md)** - Quick start guide
- **[NAVIGATION.md](NAVIGATION.md)** - Navigation structure
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Architecture decisions

## 🔧 Configuration

### Supabase (Recommended)

Create `.env` file:
```env
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
```

### FastAPI (Fallback)

If Supabase not configured, app automatically uses FastAPI backend.

## 🎯 Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **shadcn/ui** - Component system
- **TanStack Query** - Data fetching
- **TanStack Router** - Navigation
- **Supabase** - Database (direct access)
- **Tailwind CSS** - Styling

## 📦 Scripts

```bash
npm run dev      # Start dev server
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Run ESLint
```

## 🚀 Deployment

### Replit
See [REPLIT_SETUP.md](REPLIT_SETUP.md)

### Other Platforms
- **Vercel** - `vercel deploy`
- **Netlify** - `netlify deploy`
- **Cloudflare Pages** - Connect Git repo

## 🐝 Ready to Use!

The app is fully integrated with your existing Supabase and Replit stack. Just add your Supabase credentials and start building!
