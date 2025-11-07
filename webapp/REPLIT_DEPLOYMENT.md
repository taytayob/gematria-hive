# Replit Deployment Guide

## ✅ Gematria Calculator is Now 100% Frontend!

The gematria calculator now works **completely in the browser** - no backend needed! All 13 calculation methods are implemented in TypeScript and run client-side.

## 🚀 Quick Start on Replit

### 1. Import Project to Replit

1. Go to https://replit.com
2. Click "Create Repl"
3. Choose "Import from GitHub" or "Upload files"
4. If using GitHub, paste your repo URL
5. If uploading, upload the entire `webapp/` directory

### 2. Install Dependencies

In Replit shell:
```bash
cd webapp
npm install
```

### 3. Configure Environment Variables (Optional)

**For Supabase integration (optional):**

1. Click the **lock icon** 🔒 in Replit sidebar (Secrets)
2. Add these secrets:
   - `VITE_SUPABASE_URL` = your Supabase project URL
   - `VITE_SUPABASE_ANON_KEY` = your Supabase anon key

**Note:** The gematria calculator works without Supabase! It's only needed for:
- Kanban board (task management)
- Pipeline execution
- Research & Knowledge base

### 4. Run the App

**Development:**
```bash
cd webapp
npm run dev
```

Replit will automatically open the webview.

**Production Build:**
```bash
cd webapp
npm run build
npx serve dist
```

## 📁 Project Structure

```
webapp/
├── .replit              # Replit configuration
├── replit.nix           # Nix packages
├── src/
│   ├── lib/
│   │   └── gematria.ts  # ✅ Full gematria engine (frontend-only!)
│   ├── routes/
│   │   └── calculator.tsx  # ✅ Enhanced calculator UI
│   └── ...
└── package.json
```

## ✨ What Works Without Backend

### ✅ Gematria Calculator
- **All 13 calculation methods** work 100% in browser
- No API calls needed
- Instant calculations
- Works offline!

**Methods:**
- English Gematria
- Simple Gematria
- Jewish Gematria
- Latin Gematria
- Greek Gematria
- Hebrew Full
- Hebrew Musafi
- Hebrew Katan (Reduced)
- Hebrew Ordinal
- Hebrew Atbash
- Hebrew Kidmi
- Hebrew Perati
- Hebrew Shemi

### ✅ Other Frontend Features
- Dashboard
- Statistics (if using Supabase)
- Research & Knowledge Base (local state)
- Settings

## 🔧 What Needs Backend (Optional)

These features work better with a backend, but have fallbacks:

### Kanban Board
- **With Supabase:** Full task management
- **Without Supabase:** Shows error message (can be enhanced with local storage)

### Pipeline & Phases
- **With Backend:** Execute agents
- **Without Backend:** UI works, but agent execution needs backend

## 🎯 Replit Configuration

### `.replit` File
```toml
run = "cd webapp && npm run dev"
entrypoint = "webapp/src/main.tsx"
language = "nodejs"

[env]
NODE_ENV = "development"

[deploy]
run = ["sh", "-c", "cd webapp && npm run build && npx serve dist"]
```

### `replit.nix` File
```nix
{ pkgs }: {
  deps = [
    pkgs.nodejs-18_x
    pkgs.nodePackages.npm
    pkgs.nodePackages.typescript
  ];
}
```

## 🌐 Deployment Options

### Replit Deploy
1. Click "Deploy" button in Replit
2. Configure deployment settings
3. Deploy to Replit hosting

### Other Platforms
- **Vercel:** `vercel deploy`
- **Netlify:** `netlify deploy`
- **Cloudflare Pages:** Connect Git repo

All support environment variables and automatic deployments!

## 🐛 Troubleshooting

### Port Issues
Replit uses dynamic ports. Vite automatically uses the correct port.

### Environment Variables
1. Make sure secrets are named correctly (with `VITE_` prefix)
2. Restart the Repl after adding secrets
3. Check `.replit` file configuration

### Build Errors
1. Check Node.js version: `node --version` (should be 18+)
2. Clear cache: `rm -rf node_modules/.vite`
3. Reinstall: `rm -rf node_modules && npm install`

## 🎉 Benefits

### ✅ Frontend-Only Calculator
- No backend needed for calculations
- Works offline
- Instant results
- No API costs

### ✅ Replit Integration
- Free hosting for development
- Built-in terminal and editor
- Automatic HTTPS
- Easy environment variable management
- Git integration
- Collaborative editing

## 📝 Next Steps

1. **Import to Replit** - Upload or clone the project
2. **Install dependencies** - `cd webapp && npm install`
3. **Run the app** - `npm run dev`
4. **Test calculator** - Try calculating "LOVE" or any text!
5. **Optional:** Add Supabase secrets for full features

## 🚀 Ready to Deploy!

The gematria calculator is now **100% frontend** and ready for Replit deployment. No backend needed for calculations!

