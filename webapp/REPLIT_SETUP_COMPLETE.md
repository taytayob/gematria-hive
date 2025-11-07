# Replit Setup - Complete Guide

## ✅ Ready for Replit Deployment!

Your Gematria Hive webapp is now configured for Replit with:
- ✅ Frontend-only gematria calculator (no backend needed!)
- ✅ Docker support (optional)
- ✅ Full Replit configuration
- ✅ Production-ready setup

## 🚀 Quick Start in Replit

### Step 1: Import to Replit

**Option A: From GitHub**
1. Go to https://replit.com
2. Click "Create Repl"
3. Choose "Import from GitHub"
4. Paste your repository URL
5. Click "Import"

**Option B: Upload Files**
1. Go to https://replit.com
2. Click "Create Repl"
3. Choose "Node.js" template
4. Name it "gematria-hive-webapp"
5. Upload the `webapp/` directory contents

### Step 2: Install Dependencies

In Replit shell:
```bash
cd webapp
npm install
```

### Step 3: Configure Environment Variables (Optional)

**For Supabase integration (only needed for Kanban/Pipeline):**

1. Click the **lock icon** 🔒 in Replit sidebar (Secrets)
2. Add these secrets:
   ```
   VITE_SUPABASE_URL = https://your-project-id.supabase.co
   VITE_SUPABASE_ANON_KEY = your-anon-key-here
   ```

**Note:** Gematria calculator works without these!

### Step 4: Run the App

**Development:**
```bash
cd webapp
npm run dev
```

Replit will automatically:
- Start the dev server
- Open the webview
- Show the app at the assigned URL

**Production Build:**
```bash
cd webapp
npm run build
npx serve dist -p 3000
```

## 📁 Project Structure in Replit

```
gematria-hive-webapp/
├── .replit              # ✅ Replit configuration
├── replit.nix           # ✅ Nix packages
├── webapp/
│   ├── src/
│   │   ├── lib/
│   │   │   └── gematria.ts  # ✅ Full frontend calculator
│   │   ├── routes/
│   │   │   └── calculator.tsx  # ✅ Enhanced UI
│   │   └── ...
│   ├── package.json
│   └── ...
└── ...
```

## 🐳 Docker Support (Optional)

### Why Docker?

**Use Docker if:**
- ✅ You want consistent development environments
- ✅ You need to deploy to multiple platforms
- ✅ You want easy production deployment
- ✅ You need to run both frontend and backend together

**Skip Docker if:**
- ✅ You're only using Replit (it handles this)
- ✅ You're deploying to Vercel/Netlify (they handle builds)
- ✅ You only need the frontend calculator (no backend needed)

### Using Docker

**Build and run:**
```bash
# Frontend only
cd webapp
docker build -t gematria-webapp .
docker run -p 3000:80 gematria-webapp

# Full stack (frontend + backend)
docker-compose up
```

**Docker Compose includes:**
- Frontend (Nginx serving React app)
- Backend (FastAPI - optional)
- Network configuration
- Health checks

## ☸️ Kubernetes (Not Recommended for This Project)

### Why NOT Kubernetes?

**Skip Kubernetes because:**
- ❌ Overkill for a frontend React app
- ❌ Adds unnecessary complexity
- ❌ Higher operational overhead
- ❌ Not needed unless scaling to 100+ instances

**Use Kubernetes if:**
- ✅ You're building a large-scale system
- ✅ You need auto-scaling
- ✅ You have multiple microservices
- ✅ You need advanced orchestration

**For this project:**
- ✅ **Replit** - Perfect for development and simple deployment
- ✅ **Docker** - Good for production deployment
- ❌ **Kubernetes** - Unnecessary complexity

## 🎯 Recommended Deployment Strategy

### Development
- **Replit** - Best for development and testing
- Free hosting, built-in editor, easy collaboration

### Production Options

**Option 1: Replit Deploy (Easiest)**
1. Click "Deploy" in Replit
2. Configure settings
3. Deploy to Replit hosting
4. Done!

**Option 2: Docker + Cloud Platform**
- **Vercel** - `vercel deploy` (handles Docker automatically)
- **Netlify** - `netlify deploy` (handles Docker automatically)
- **Railway** - `railway up` (Docker support)
- **Fly.io** - `fly deploy` (Docker support)

**Option 3: Docker Compose (Self-hosted)**
- Run on your own server
- Full control
- Requires server management

## 📝 Replit Configuration Files

### `.replit` - Main Configuration
- Sets run command: `cd webapp && npm run dev`
- Configures language: Node.js
- Sets up TypeScript language server
- Configures ports

### `replit.nix` - Package Dependencies
- Node.js 18
- npm
- TypeScript

## 🔧 Troubleshooting

### Port Already in Use
Replit handles ports automatically. If you see errors:
```bash
# Check what's using the port
lsof -ti:3000

# Kill the process
kill -9 $(lsof -ti:3000)
```

### Environment Variables Not Working
1. Make sure secrets are named with `VITE_` prefix
2. Restart the Repl after adding secrets
3. Check `.replit` file configuration

### Build Errors
```bash
# Clear cache
rm -rf node_modules/.vite

# Reinstall
rm -rf node_modules && npm install
```

## ✅ What Works in Replit

### 100% Frontend (No Backend Needed)
- ✅ **Gematria Calculator** - All 13 methods
- ✅ **Dashboard** - Static content
- ✅ **Research & Knowledge Base** - Local state
- ✅ **Settings** - Local configuration

### Needs Backend (Optional)
- ⚠️ **Kanban Board** - Needs Supabase or FastAPI
- ⚠️ **Pipeline & Phases** - Needs backend for agent execution
- ⚠️ **Statistics** - Needs Supabase for data

## 🎉 Next Steps

1. **Import to Replit** - Follow Step 1 above
2. **Install dependencies** - `cd webapp && npm install`
3. **Run the app** - `npm run dev`
4. **Test calculator** - Try "LOVE" or any text!
5. **Optional:** Add Supabase secrets for full features
6. **Deploy:** Click "Deploy" when ready!

## 🚀 Ready to Go!

Your app is configured for Replit. Just import and run!

**For Docker:** Use `docker-compose up` if you need full stack
**For Kubernetes:** Skip it - not needed for this project

