# Replit Browser Setup - Step by Step

## 🚀 Complete Setup in Your Browser

Follow these steps to set up Gematria Hive in Replit:

### Step 1: Go to Replit

1. **Open your browser**
2. **Go to:** https://replit.com
3. **Sign in** or create an account

### Step 2: Create New Repl

1. **Click "Create Repl"** (top right or main page)
2. **Choose import method:**

   **Option A: From GitHub (Recommended)**
   - Click "Import from GitHub"
   - Paste your repository URL: `https://github.com/your-username/gematria-hive`
   - Click "Import"
   - Replit will clone the repo

   **Option B: Upload Files**
   - Click "Create Repl"
   - Choose "Node.js" template
   - Name it: `gematria-hive-webapp`
   - Click "Create Repl"
   - Upload the `webapp/` directory contents

### Step 3: Install Dependencies

**In Replit shell (bottom panel):**

```bash
cd webapp
npm install
```

Wait for installation to complete (may take 1-2 minutes).

### Step 4: Configure Environment Variables (Optional)

**For Supabase integration (only needed for Kanban/Pipeline):**

1. **Click the lock icon** 🔒 in the left sidebar (Secrets)
2. **Click "New secret"**
3. **Add these secrets:**

   **Secret 1:**
   - Key: `VITE_SUPABASE_URL`
   - Value: `https://your-project-id.supabase.co`
   - Click "Add secret"

   **Secret 2:**
   - Key: `VITE_SUPABASE_ANON_KEY`
   - Value: `your-anon-key-here`
   - Click "Add secret"

**Note:** Gematria calculator works without these! They're only needed for:
- Kanban board (task management)
- Pipeline execution
- Research & Knowledge base

### Step 5: Run the App

**In Replit shell:**

```bash
cd webapp
npm run dev
```

**Replit will automatically:**
- Start the dev server
- Open the webview
- Show your app at the assigned URL

### Step 6: Test the Calculator

1. **Click the webview** that opened
2. **Navigate to:** `/calculator` or click "Gematria Calculator" in sidebar
3. **Try calculating:**
   - Enter "LOVE"
   - See all 13 methods calculate instantly!
   - No backend needed!

### Step 7: Deploy (Optional)

**When ready for production:**

1. **Click "Deploy"** button (top right)
2. **Configure settings:**
   - Name: `gematria-hive-webapp`
   - Description: `Gematria Hive - Frontend Calculator & Task Management`
3. **Click "Deploy"**
4. **Wait for deployment** (1-2 minutes)
5. **Get your public URL!**

## ✅ What Works Immediately

### 100% Frontend (No Backend Needed)
- ✅ **Gematria Calculator** - All 13 methods
- ✅ **Dashboard** - Overview page
- ✅ **Research & Knowledge Base** - Local state
- ✅ **Settings** - Configuration

### Needs Backend (Optional)
- ⚠️ **Kanban Board** - Needs Supabase or FastAPI
- ⚠️ **Pipeline & Phases** - Needs backend for agent execution
- ⚠️ **Statistics** - Needs Supabase for data

## 🐛 Troubleshooting

### "npm install" Fails
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### Port Already in Use
Replit handles ports automatically. If you see errors:
```bash
# Kill any existing process
pkill -f "vite"
# Then run again
npm run dev
```

### Environment Variables Not Working
1. Make sure secrets are named with `VITE_` prefix
2. Restart the Repl after adding secrets
3. Check `.replit` file exists

### Build Errors
```bash
# Check Node version
node --version  # Should be 18+

# Clear Vite cache
rm -rf node_modules/.vite

# Reinstall
rm -rf node_modules
npm install
```

## 🎉 Success!

Once you see the app running in the webview, you're done!

**Test the calculator:**
- Go to `/calculator`
- Enter "LOVE" or any text
- See all 13 methods calculate instantly!

**No backend needed for the calculator!** 🎉

