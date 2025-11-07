# Supabase Integration Guide

The webapp now supports **direct Supabase integration** for better performance and real-time capabilities.

## Architecture

### Option 1: Direct Supabase (Recommended)
```
React App → Supabase Client → Supabase Database
```
- ✅ Faster (direct connection)
- ✅ Real-time subscriptions
- ✅ Better performance
- ✅ No backend needed

### Option 2: FastAPI Backend (Fallback)
```
React App → FastAPI → Supabase Database
```
- ✅ Works if Supabase not configured
- ✅ Backend validation
- ✅ Custom business logic

## Setup

### 1. Get Supabase Credentials

1. Go to https://supabase.com/dashboard
2. Select your project
3. Go to **Settings → API**
4. Copy:
   - **Project URL** → `VITE_SUPABASE_URL`
   - **anon public** key → `VITE_SUPABASE_ANON_KEY`

### 2. Configure Environment Variables

**Local Development (.env):**
```env
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
```

**Replit (Secrets):**
1. Click lock icon 🔒
2. Add:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`

### 3. Verify Connection

The app will automatically:
- ✅ Use Supabase if credentials are available
- ✅ Fall back to FastAPI if not configured
- ✅ Show warnings in console if Supabase not configured

## Features

### Direct Database Access
- All CRUD operations go directly to Supabase
- No backend proxy needed
- Faster response times

### Real-time Subscriptions (Future)
```typescript
// Subscribe to task changes
supabase
  .channel('tasks')
  .on('postgres_changes', 
    { event: '*', schema: 'public', table: 'hunches' },
    (payload) => {
      // Update UI in real-time
    }
  )
  .subscribe()
```

### Row Level Security (RLS)
- Configure RLS policies in Supabase
- Secure data access
- User-based permissions

## Database Schema

The app uses the `hunches` table (matching your existing schema):

```sql
CREATE TABLE hunches (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content TEXT NOT NULL,
  status TEXT DEFAULT 'pending',
  phase TEXT,
  role TEXT,
  priority TEXT,
  cost DECIMAL DEFAULT 0,
  tags TEXT[],
  resources TEXT[],
  labels TEXT[],
  assigned_to TEXT,
  project_id TEXT,
  parent_task_id TEXT,
  due_date TIMESTAMP,
  estimated_hours DECIMAL,
  actual_hours DECIMAL,
  progress INTEGER DEFAULT 0,
  dependencies TEXT[],
  metadata JSONB,
  links TEXT[],
  timestamp TIMESTAMP DEFAULT NOW(),
  created_at TIMESTAMP DEFAULT NOW()
);
```

## Benefits

### Performance
- ✅ Direct database connection
- ✅ No backend latency
- ✅ Faster queries

### Real-time
- ✅ Live updates (with subscriptions)
- ✅ Instant UI updates
- ✅ Collaborative features

### Scalability
- ✅ Supabase handles scaling
- ✅ Built-in CDN
- ✅ Global edge network

### Security
- ✅ Row Level Security (RLS)
- ✅ API key authentication
- ✅ Secure by default

## Migration from FastAPI

The app automatically detects Supabase credentials and uses them if available. No code changes needed!

1. Add Supabase credentials to `.env`
2. Restart dev server
3. App automatically uses Supabase

## Troubleshooting

### "Supabase credentials not found"
- Check `.env` file exists
- Verify variable names: `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY`
- Restart dev server after adding variables

### "Failed to connect to Supabase"
- Check Supabase URL is correct
- Verify anon key is correct
- Check Supabase project is active

### Still using FastAPI
- App falls back to FastAPI if Supabase not configured
- Check console for warnings
- Verify environment variables are loaded

## Next Steps

1. ✅ Add Supabase credentials
2. ✅ Test direct database access
3. ✅ Enable real-time subscriptions (optional)
4. ✅ Configure RLS policies (optional)
5. ✅ Deploy to production

The app is now fully integrated with Supabase! 🎉

