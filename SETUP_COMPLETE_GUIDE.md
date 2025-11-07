# Setup Complete Guide - Gematria Hive

**Date:** January 6, 2025  
**Status:** ✅ Dependencies Installed | ⚠️ API Keys Required  
**Purpose:** Complete setup guide with browser links

---

## ✅ Completed Automatically

### 1. Dependencies Installed ✅
- ✅ `google-generativeai` - Gemini API
- ✅ `google-api-python-client` - Drive API
- ✅ `google-auth-httplib2` - OAuth HTTP
- ✅ `google-auth-oauthlib` - OAuth flow

### 2. Agents Initialized ✅
- ✅ Gemini Research Agent - Ready (needs API key)
- ✅ Google Drive Integrator Agent - Ready (needs OAuth)
- ✅ Orchestrator - All agents loaded

### 3. Code Integration ✅
- ✅ All agents integrated into orchestrator
- ✅ MCP tool registry updated
- ✅ Parallel execution configured

---

## ⚠️ Manual Setup Required (Use Browser)

### 1. Get Google Gemini API Key 🔴 HIGH PRIORITY

**Steps:**
1. **Open browser:** https://ai.google.dev
2. **Sign in** with your Google account
3. **Click "Get API Key"** button
4. **Create new project** or select existing
5. **Copy the API key**
6. **Add to `.env` file:**
   ```bash
   GOOGLE_API_KEY=your-api-key-here
   ```

**Direct Link:** https://ai.google.dev

**Documentation:** https://ai.google.dev/docs

**Free Tier:** Available with generous limits

---

### 2. Set Up Google Drive OAuth 🔴 HIGH PRIORITY

**Steps:**

#### Step 1: Create Google Cloud Project
1. **Open browser:** https://console.cloud.google.com
2. **Sign in** with your Google account
3. **Click "Select a project"** → **"New Project"**
4. **Name:** `Gematria Hive Drive Integration`
5. **Click "Create"**

#### Step 2: Enable Google Drive API
1. **Go to:** https://console.cloud.google.com/apis/library
2. **Search for:** "Google Drive API"
3. **Click "Google Drive API"**
4. **Click "Enable"**

#### Step 3: Create OAuth 2.0 Credentials
1. **Go to:** https://console.cloud.google.com/apis/credentials
2. **Click "Create Credentials"** → **"OAuth client ID"**
3. **If prompted, configure OAuth consent screen:**
   - **User Type:** External (or Internal if using Google Workspace)
   - **App name:** `Gematria Hive`
   - **User support email:** Your email
   - **Developer contact:** Your email
   - **Click "Save and Continue"**
   - **Scopes:** Click "Add or Remove Scopes" → Search "drive.readonly" → Select → Save
   - **Test users:** Add your email (if External)
   - **Click "Save and Continue"** → **"Back to Dashboard"**
4. **Application type:** Desktop app
5. **Name:** `Gematria Hive Drive Integration`
6. **Click "Create"**
7. **Copy Client ID and Client Secret**

#### Step 4: Add to .env File
```bash
GOOGLE_DRIVE_CLIENT_ID=your-client-id-here
GOOGLE_DRIVE_CLIENT_SECRET=your-client-secret-here
```

#### Step 5: Run OAuth Flow
```bash
python scripts/setup_google_drive_oauth.py
```

This will:
- Open a browser window for authentication
- Request Google Drive read-only access
- Save refresh token to `.env` file

**Direct Links:**
- **Google Cloud Console:** https://console.cloud.google.com
- **APIs Library:** https://console.cloud.google.com/apis/library
- **Credentials:** https://console.cloud.google.com/apis/credentials
- **OAuth Consent Screen:** https://console.cloud.google.com/apis/credentials/consent

---

### 3. Verify Supabase Configuration ✅

**Check if set:**
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('SUPABASE_URL:', '✅ SET' if os.getenv('SUPABASE_URL') else '❌ NOT SET'); print('SUPABASE_KEY:', '✅ SET' if os.getenv('SUPABASE_KEY') else '❌ NOT SET')"
```

**If not set:**
1. **Open browser:** https://supabase.com
2. **Sign in** or create account
3. **Create new project** or select existing
4. **Go to:** Settings → API
5. **Copy:**
   - **Project URL** → `SUPABASE_URL`
   - **anon public key** → `SUPABASE_KEY`
6. **Add to `.env` file**

**Direct Link:** https://supabase.com/dashboard

---

## 🧪 Testing After Setup

### Test Gemini Integration
```bash
python -c "from agents.gemini_research import GeminiResearchAgent; a = GeminiResearchAgent(); print('✅ Gemini OK' if a.model else '❌ Need GOOGLE_API_KEY')"
```

### Test Drive Integration
```bash
python -c "from agents.google_drive_integrator import GoogleDriveIntegratorAgent; a = GoogleDriveIntegratorAgent(); print('✅ Drive OK' if a.service else '❌ Need OAuth credentials')"
```

### Test Full Orchestrator
```python
from agents.orchestrator import get_orchestrator

orchestrator = get_orchestrator()
result = orchestrator.execute({
    "type": "browser",
    "url": "https://example.com"
})
print("✅ Orchestrator working" if result.get("status") == "completed" else "❌ Error")
```

---

## 📋 Quick Setup Checklist

### Immediate (5 minutes)
- [ ] Get Google Gemini API key from https://ai.google.dev
- [ ] Add `GOOGLE_API_KEY` to `.env`
- [ ] Test Gemini: `python -c "from agents.gemini_research import GeminiResearchAgent; a = GeminiResearchAgent(); print('OK' if a.model else 'Not configured')"`

### Google Drive Setup (15-20 minutes)
- [ ] Create Google Cloud project at https://console.cloud.google.com
- [ ] Enable Google Drive API
- [ ] Create OAuth 2.0 credentials (Desktop app)
- [ ] Add `GOOGLE_DRIVE_CLIENT_ID` to `.env`
- [ ] Add `GOOGLE_DRIVE_CLIENT_SECRET` to `.env`
- [ ] Run `python scripts/setup_google_drive_oauth.py`
- [ ] Test Drive: `python -c "from agents.google_drive_integrator import GoogleDriveIntegratorAgent; a = GoogleDriveIntegratorAgent(); print('OK' if a.service else 'Not configured')"`

### Verify Supabase (if needed)
- [ ] Check if `SUPABASE_URL` and `SUPABASE_KEY` are set
- [ ] If not, get from https://supabase.com/dashboard → Settings → API

---

## 🔗 Quick Links

### API Keys & Setup
- **Google Gemini:** https://ai.google.dev
- **Google Cloud Console:** https://console.cloud.google.com
- **Google Drive API:** https://console.cloud.google.com/apis/library/drive.googleapis.com
- **OAuth Credentials:** https://console.cloud.google.com/apis/credentials
- **Supabase Dashboard:** https://supabase.com/dashboard

### Documentation
- **Gemini API Docs:** https://ai.google.dev/docs
- **Drive API Docs:** https://developers.google.com/drive/api
- **OAuth 2.0 Guide:** https://developers.google.com/identity/protocols/oauth2

---

## 🚀 After Setup

### Run Full Pipeline
```python
from agents.orchestrator import get_orchestrator

orchestrator = get_orchestrator()

# Browser + Gemini research in parallel
result = orchestrator.execute({
    "type": "browser",
    "url": "https://example.com"
})

print(f"Status: {result.get('status')}")
print(f"Data items: {len(result.get('data', []))}")
print(f"Results: {len(result.get('results', []))}")
```

### Use Drive Integration
```python
from agents.google_drive_integrator import GoogleDriveIntegratorAgent

drive = GoogleDriveIntegratorAgent()

# List files in folder
files = drive.list_files(folder_id="your-folder-id")

# Extract from file
data = drive._extract_from_file(file_id="your-file-id")
```

---

## 📊 Current Status

**✅ Completed:**
- Dependencies installed
- Agents initialized
- Code integrated
- Orchestrator ready

**⚠️ Needs Manual Setup:**
- Google Gemini API key (5 min)
- Google Drive OAuth (15-20 min)
- Supabase credentials (if not set)

**🎯 Next Steps:**
1. Get Gemini API key → Add to `.env`
2. Set up Drive OAuth → Run setup script
3. Test integrations
4. Start using the platform!

---

**Last Updated:** January 6, 2025  
**Status:** ✅ Ready for API Key Setup

