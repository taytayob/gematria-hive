# Quick Start - Replit Setup

## 🚀 5-Minute Setup in Replit

### Step 1: Import to Replit

1. Go to https://replit.com
2. Click "Create Repl"
3. Choose "Import from GitHub" or "Upload files"
4. If GitHub: Paste repo URL
5. If Upload: Upload `webapp/` directory

### Step 2: Install

```bash
cd webapp
npm install
```

### Step 3: Run

```bash
npm run dev
```

**Done!** Replit will open the webview automatically.

### Step 4: Test Calculator

1. Click webview
2. Go to `/calculator`
3. Enter "LOVE"
4. See all 13 methods calculate!

## ✅ What Works

- ✅ **Gematria Calculator** - 100% frontend, no backend needed!
- ✅ **Dashboard** - Overview page
- ✅ **Research & Knowledge Base** - Local state
- ✅ **Settings** - Configuration

## ⚠️ Optional: Add Supabase

**Only needed for Kanban/Pipeline:**

1. Click lock icon 🔒 (Secrets)
2. Add:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`

**Calculator works without these!**

## 🐳 Docker (Optional)

**For production deployment:**

```bash
# Build
cd webapp
docker build -t gematria-webapp .

# Run
docker run -p 3000:80 gematria-webapp
```

## ☸️ Kubernetes

**Skip it** - Not needed for this project!

## 🎉 Ready!

Your app is ready to use in Replit. The calculator works immediately - no backend needed!

