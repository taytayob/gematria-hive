# Replit Setup Guide

Deploy the Gematria Hive webapp to Replit with Supabase integration.

## Prerequisites

- Replit account
- Supabase project created
- Supabase URL and anon key

## Setup Steps

### 1. Create Replit Project

1. Go to https://replit.com
2. Click "Create Repl"
3. Choose "Node.js" template
4. Name it "gematria-hive-webapp"

### 2. Upload Project Files

**Option A: Git Import**
```bash
# In Replit shell
git clone https://github.com/your-username/gematria-hive.git
cd gematria-hive/webapp
```

**Option B: Manual Upload**
- Upload all files from `webapp/` directory
- Or use Replit's file upload feature

### 3. Install Dependencies

In Replit shell:
```bash
cd webapp
npm install
```

### 4. Configure Environment Variables

**In Replit:**

1. Click the **lock icon** 🔒 in the left sidebar (Secrets)
2. Add these secrets:

```
VITE_SUPABASE_URL = https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY = your-anon-key-here
```

**Get Supabase credentials:**
1. Go to https://supabase.com/dashboard
2. Select your project
3. Go to Settings → API
4. Copy:
   - **Project URL** → `VITE_SUPABASE_URL`
   - **anon public** key → `VITE_SUPABASE_ANON_KEY`

### 5. Create `.replit` File

Create `.replit` file in the `webapp/` directory:

```toml
run = "npm run dev"
entrypoint = "src/main.tsx"
language = "nodejs"

[env]
VITE_SUPABASE_URL = "@VITE_SUPABASE_URL"
VITE_SUPABASE_ANON_KEY = "@VITE_SUPABASE_ANON_KEY"

[deploy]
run = ["sh", "-c", "npm run build && npx serve dist"]
```

### 6. Configure Replit for Vite

**Create `replit.nix` (optional, for better Node.js support):**

```nix
{ pkgs }: {
  deps = [
    pkgs.nodejs-18_x
    pkgs.nodePackages.npm
  ];
}
```

### 7. Run the App

**Development:**
```bash
npm run dev
```

Replit will automatically open the webview.

**Production Build:**
```bash
npm run build
npx serve dist
```

### 8. Deploy (Optional)

**Using Replit Deploy:**
1. Click "Deploy" button
2. Configure deployment settings
3. Deploy to Replit hosting

**Or use other hosting:**
- Vercel
- Netlify
- Cloudflare Pages

## Environment Variables in Replit

Replit Secrets are automatically available as environment variables:

- `VITE_SUPABASE_URL` - Your Supabase project URL
- `VITE_SUPABASE_ANON_KEY` - Your Supabase anon key

These are automatically prefixed with `VITE_` for Vite to pick them up.

## Troubleshooting

### Port Issues

Replit uses dynamic ports. Vite will automatically use the correct port.

### Environment Variables Not Working

1. Make sure secrets are named correctly (with `VITE_` prefix)
2. Restart the Repl after adding secrets
3. Check `.replit` file configuration

### Build Errors

1. Check Node.js version: `node --version` (should be 18+)
2. Clear cache: `rm -rf node_modules/.vite`
3. Reinstall: `rm -rf node_modules && npm install`

## Benefits of Replit

- ✅ **Free hosting** for development
- ✅ **Built-in terminal** and editor
- ✅ **Automatic HTTPS**
- ✅ **Easy environment variable management**
- ✅ **Git integration**
- ✅ **Collaborative editing**

## Next Steps

1. Set up Supabase credentials
2. Run `npm run dev`
3. Open webview in Replit
4. Test the app!

## Production Deployment

For production, consider:
- **Vercel** - Great for Vite apps
- **Netlify** - Easy deployment
- **Cloudflare Pages** - Fast CDN
- **Replit Deploy** - Built-in hosting

All support environment variables and automatic deployments from Git.

