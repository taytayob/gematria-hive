# Stack Integration Guide

The webapp now integrates with **Supabase** and **Replit** - your existing stack!

## ✅ What's Integrated

### 1. Supabase Integration
- ✅ **Direct database access** - Frontend connects directly to Supabase
- ✅ **Automatic fallback** - Falls back to FastAPI if Supabase not configured
- ✅ **Same database** - Uses your existing `hunches` table
- ✅ **Real-time ready** - Can enable real-time subscriptions

### 2. Replit Support
- ✅ **Environment variables** - Uses Replit Secrets
- ✅ **Deployment ready** - Can deploy to Replit hosting
- ✅ **Git integration** - Works with Replit Git

### 3. Existing Stack
- ✅ **Python backend** - Still works as fallback
- ✅ **FastAPI** - Available if Supabase not configured
- ✅ **Same database** - Uses your Supabase database

## 🚀 Quick Setup

### Option 1: Use Supabase Directly (Recommended)

**1. Get Supabase Credentials:**
```bash
# From Supabase Dashboard → Settings → API
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
```

**2. Configure Environment Variables:**

**Local (.env):**
```env
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
```

**Replit (Secrets):**
1. Click lock icon 🔒
2. Add:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`

**3. Install Dependencies:**
```bash
cd webapp
npm install
```

**4. Run:**
```bash
npm run dev
```

### Option 2: Use FastAPI Backend (Fallback)

If Supabase credentials are not set, the app automatically uses FastAPI:

```bash
# Start backend
python kanban_api.py

# Start frontend
cd webapp
npm run dev
```

## 📊 Architecture

### With Supabase (Recommended)
```
React App → Supabase Client → Supabase Database
```
- ✅ Faster (direct connection)
- ✅ No backend needed
- ✅ Real-time subscriptions available

### With FastAPI (Fallback)
```
React App → FastAPI → Supabase Database
```
- ✅ Works if Supabase not configured
- ✅ Backend validation
- ✅ Custom business logic

## 🔧 Configuration

### Environment Variables

**Supabase (Recommended):**
- `VITE_SUPABASE_URL` - Your Supabase project URL
- `VITE_SUPABASE_ANON_KEY` - Your Supabase anon key

**FastAPI (Fallback):**
- `VITE_API_BASE` - FastAPI base URL (default: `/api`)

### How It Works

1. **App checks for Supabase credentials**
2. **If found:** Uses Supabase directly
3. **If not found:** Falls back to FastAPI
4. **Automatic:** No code changes needed!

## 🎯 Benefits

### Using Supabase Directly
- ✅ **Faster** - Direct database connection
- ✅ **Real-time** - Can enable live updates
- ✅ **Simpler** - No backend needed
- ✅ **Scalable** - Supabase handles scaling

### Using FastAPI
- ✅ **Backend validation** - Custom business logic
- ✅ **API layer** - Additional security
- ✅ **Flexibility** - Custom endpoints

## 📚 Documentation

- **Supabase Integration:** See `SUPABASE_INTEGRATION.md`
- **Replit Setup:** See `REPLIT_SETUP.md`
- **Quick Start:** See `QUICK_START.md`

## 🚀 Deployment

### Replit
1. Upload project to Replit
2. Set environment variables (Secrets)
3. Run `npm run dev`
4. Deploy using Replit Deploy

### Other Platforms
- **Vercel** - Great for Vite apps
- **Netlify** - Easy deployment
- **Cloudflare Pages** - Fast CDN

All support environment variables!

## ✨ Next Steps

1. ✅ Add Supabase credentials
2. ✅ Test direct database access
3. ✅ Deploy to Replit (optional)
4. ✅ Enable real-time subscriptions (optional)

The app is now fully integrated with your existing stack! 🎉

