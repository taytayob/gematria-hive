# Manual Setup Required - Gematria Hive

**Date:** January 6, 2025  
**Status:** ⚠️ Action Required  
**Purpose:** Document all items that require manual setup

---

## 🔴 CRITICAL - Must Do Now

### 1. Create `.env` File

**Action:** Copy `.env.example` to `.env` and fill in your values

```bash
cp .env.example .env
# Then edit .env with your actual API keys
```

**Required Variables:**
- `SUPABASE_URL` - Get from https://supabase.com/dashboard → Settings → API
- `SUPABASE_KEY` - Get from https://supabase.com/dashboard → Settings → API
- `INTERNAL_API_KEY` - Change to a secure random string

**Optional but Recommended:**
- `GOOGLE_API_KEY` - Get from https://ai.google.dev (for Gemini Deep Research)
- `GOOGLE_DRIVE_CLIENT_ID` - Get from https://console.cloud.google.com (for Drive integration)
- `GOOGLE_DRIVE_CLIENT_SECRET` - Get from https://console.cloud.google.com

---

## 🟡 HIGH PRIORITY - Google Gemini Setup

### 1. Get Google Gemini API Key

**Steps:**
1. Go to https://ai.google.dev
2. Sign in with your Google account
3. Click "Get API Key"
4. Create a new API key or use existing
5. Copy the API key
6. Add to `.env` file: `GOOGLE_API_KEY=your-key-here`

**Documentation:** https://ai.google.dev/docs

---

## 🟡 HIGH PRIORITY - Google Drive Setup

### 1. Create Google Cloud Project

**Steps:**
1. Go to https://console.cloud.google.com
2. Create a new project or select existing
3. Enable Google Drive API:
   - Go to "APIs & Services" → "Library"
   - Search for "Google Drive API"
   - Click "Enable"

### 2. Create OAuth 2.0 Credentials

**Steps:**
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Choose "Desktop app" as application type
4. Name it "Gematria Hive Drive Integration"
5. Click "Create"
6. Copy the Client ID and Client Secret
7. Add to `.env` file:
   ```
   GOOGLE_DRIVE_CLIENT_ID=your-client-id
   GOOGLE_DRIVE_CLIENT_SECRET=your-client-secret
   ```

### 3. Run OAuth Flow to Get Refresh Token

**Steps:**
1. Install dependencies: `pip install -r requirements.txt`
2. Run OAuth flow:
   ```python
   from utils.google_drive_auth import run_oauth_flow, save_refresh_token
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   
   client_id = os.getenv('GOOGLE_DRIVE_CLIENT_ID')
   client_secret = os.getenv('GOOGLE_DRIVE_CLIENT_SECRET')
   
   creds = run_oauth_flow(client_id, client_secret)
   if creds:
       save_refresh_token(creds)
   ```
3. This will open a browser window for authentication
4. After authentication, the refresh token will be saved to `.env`

**Alternative:** Use the setup script:
```bash
python scripts/setup_google_drive_oauth.py
```

---

## 🟢 MEDIUM PRIORITY - Optional API Keys

### 1. Anthropic Claude API

**Steps:**
1. Go to https://console.anthropic.com
2. Sign up or sign in
3. Create an API key
4. Add to `.env`: `ANTHROPIC_API_KEY=your-key-here`

### 2. Perplexity API

**Steps:**
1. Go to https://perplexity.ai
2. Sign up for API access
3. Get your API key
4. Add to `.env`: `PERPLEXITY_API_KEY=your-key-here`

### 3. Grok/Twitter API

**Steps:**
1. Go to https://x.ai
2. Sign up for API access
3. Get your API key
4. Add to `.env`: `GROK_API_KEY=your-key-here`

---

## 📋 Setup Checklist

### Critical (Required for Core Functionality)
- [ ] Create `.env` file from `.env.example`
- [ ] Set `SUPABASE_URL` in `.env`
- [ ] Set `SUPABASE_KEY` in `.env`
- [ ] Set `INTERNAL_API_KEY` in `.env` (change from default)
- [ ] Test database connection: `python setup_database.py --verify-only`

### High Priority (Gemini & Drive Integration)
- [ ] Get `GOOGLE_API_KEY` from https://ai.google.dev
- [ ] Add `GOOGLE_API_KEY` to `.env`
- [ ] Create Google Cloud project
- [ ] Enable Google Drive API
- [ ] Create OAuth 2.0 credentials
- [ ] Add `GOOGLE_DRIVE_CLIENT_ID` to `.env`
- [ ] Add `GOOGLE_DRIVE_CLIENT_SECRET` to `.env`
- [ ] Run OAuth flow to get refresh token
- [ ] Add `GOOGLE_DRIVE_REFRESH_TOKEN` to `.env`
- [ ] Test Gemini integration: `python -c "from agents.gemini_research import GeminiResearchAgent; a = GeminiResearchAgent(); print('Gemini OK' if a.model else 'Gemini not configured')"`
- [ ] Test Drive integration: `python -c "from agents.google_drive_integrator import GoogleDriveIntegratorAgent; a = GoogleDriveIntegratorAgent(); print('Drive OK' if a.service else 'Drive not configured')"`

### Optional (Enhance Features)
- [ ] Get `ANTHROPIC_API_KEY` and add to `.env`
- [ ] Get `PERPLEXITY_API_KEY` and add to `.env`
- [ ] Get `GROK_API_KEY` and add to `.env`
- [ ] Get `OPENAI_API_KEY` and add to `.env`

---

## 🚀 Quick Start Commands

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create .env File
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Test Database Connection
```bash
python setup_database.py --verify-only
```

### 4. Test Gemini Integration
```bash
python -c "from agents.gemini_research import GeminiResearchAgent; a = GeminiResearchAgent(); print('✅ Gemini OK' if a.model else '❌ Gemini not configured')"
```

### 5. Test Drive Integration
```bash
python -c "from agents.google_drive_integrator import GoogleDriveIntegratorAgent; a = GoogleDriveIntegratorAgent(); print('✅ Drive OK' if a.service else '❌ Drive not configured')"
```

---

## 📚 Documentation Links

- **Supabase Setup:** `docs/setup/SUPABASE_SETUP_INSTRUCTIONS.md`
- **Gemini Integration:** `staging/gemini-deep-research-integration.md`
- **Drive Integration:** `staging/gemini-deep-research-integration.md` (includes Drive)
- **Project Audit:** `PROJECT_AUDIT_AND_INSIGHTS.md`

---

## ❓ Questions?

If you need help with setup:
1. Check the documentation files listed above
2. Review `PROJECT_AUDIT_AND_INSIGHTS.md` for detailed information
3. Check error logs for specific issues

---

**Last Updated:** January 6, 2025  
**Next Review:** After completing setup

