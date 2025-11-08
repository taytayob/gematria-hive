# Browser Setup Guide - Gematria Hive

**Date:** January 6, 2025  
**Status:** 🌐 Browser-Based Setup Instructions  
**Purpose:** Complete browser-based setup for all API keys

---

## ✅ Completed Automatically

### 1. INTERNAL_API_KEY ✅
- ✅ **Generated:** Secure random key created
- ✅ **Updated:** Added to `.env` file
- ⚠️ **Database:** Table needs to be created (see below)

**Key Generated:** `1xzBPnvGJtTLvKjQQrp8...` (truncated for security)

**Next Step:** Create `api_keys` table in Supabase:
1. Go to: https://supabase.com/dashboard
2. Click: SQL Editor
3. Run: `migrations/create_api_keys_table.sql`
4. Then run: `python scripts/apply_api_keys_migration.py` to log the key

---

## 🌐 Browser Setup - Step by Step

### 1. Google Gemini API Key (5 minutes) 🔴 HIGH PRIORITY

**Direct Link:** https://ai.google.dev

**Steps:**
1. **Open browser:** https://ai.google.dev
2. **Sign in** with your Google account
3. **Click:** "Get API Key" button (top right)
4. **Select/Create Project:**
   - Choose existing project or create new
   - Name: `Gematria Hive`
5. **Copy API Key:**
   - Click "Copy" button
   - Key starts with `AIza...`
6. **Add to `.env`:**
   ```bash
   GOOGLE_API_KEY=AIza...your-key-here
   ```
7. **Test:**
   ```bash
   python -c "from agents.gemini_research import GeminiResearchAgent; a = GeminiResearchAgent(); print('✅ OK' if a.model else '❌ Not configured')"
   ```

**Free Tier:** ✅ Available with generous limits

**Documentation:** https://ai.google.dev/docs

---

### 2. Google Drive OAuth Setup (15-20 minutes) 🔴 HIGH PRIORITY

#### Step 1: Create Google Cloud Project

**Direct Link:** https://console.cloud.google.com

**Steps:**
1. **Open:** https://console.cloud.google.com
2. **Sign in** with Google account
3. **Click:** "Select a project" (top bar)
4. **Click:** "New Project"
5. **Fill in:**
   - **Project name:** `Gematria Hive Drive Integration`
   - **Organization:** (optional)
   - **Location:** (optional)
6. **Click:** "Create"
7. **Wait:** 10-30 seconds for project creation

#### Step 2: Enable Google Drive API

**Direct Link:** https://console.cloud.google.com/apis/library/drive.googleapis.com

**Steps:**
1. **Go to:** https://console.cloud.google.com/apis/library
2. **Search:** "Google Drive API"
3. **Click:** "Google Drive API" result
4. **Click:** "Enable" button
5. **Wait:** API enabled (usually instant)

#### Step 3: Configure OAuth Consent Screen

**Direct Link:** https://console.cloud.google.com/apis/credentials/consent

**Steps:**
1. **Go to:** https://console.cloud.google.com/apis/credentials/consent
2. **Choose:** External (or Internal if using Google Workspace)
3. **Click:** "Create"
4. **Fill in:**
   - **App name:** `Gematria Hive`
   - **User support email:** Your email
   - **Developer contact:** Your email
5. **Click:** "Save and Continue"
6. **Scopes:** Click "Add or Remove Scopes"
   - Search: `drive.readonly`
   - Select: `.../auth/drive.readonly`
   - Click: "Update"
   - Click: "Save and Continue"
7. **Test users:** (if External)
   - Click: "Add Users"
   - Add: Your email address
   - Click: "Add"
   - Click: "Save and Continue"
8. **Summary:** Review and click "Back to Dashboard"

#### Step 4: Create OAuth 2.0 Credentials

**Direct Link:** https://console.cloud.google.com/apis/credentials

**Steps:**
1. **Go to:** https://console.cloud.google.com/apis/credentials
2. **Click:** "Create Credentials" → "OAuth client ID"
3. **Application type:** Desktop app
4. **Name:** `Gematria Hive Drive Integration`
5. **Click:** "Create"
6. **Copy credentials:**
   - **Client ID:** Copy this (long string)
   - **Client Secret:** Copy this (long string)
   - **Click:** "OK"

#### Step 5: Add to .env File

```bash
GOOGLE_DRIVE_CLIENT_ID=your-client-id-here
GOOGLE_DRIVE_CLIENT_SECRET=your-client-secret-here
```

#### Step 6: Run OAuth Flow

```bash
python scripts/setup_google_drive_oauth.py
```

This will:
- Open browser window
- Request Google Drive access
- Save refresh token to `.env`

**Test:**
```bash
python -c "from agents.google_drive_integrator import GoogleDriveIntegratorAgent; a = GoogleDriveIntegratorAgent(); print('✅ OK' if a.service else '❌ Not configured')"
```

---

### 3. Anthropic Claude API (Optional) 🟢 MEDIUM PRIORITY

**Direct Link:** https://console.anthropic.com

**Steps:**
1. **Open:** https://console.anthropic.com
2. **Sign in** or create account
3. **Go to:** API Keys
4. **Click:** "Create Key"
5. **Name:** `Gematria Hive`
6. **Copy:** API key (starts with `sk-ant-...`)
7. **Add to `.env`:**
   ```bash
   ANTHROPIC_API_KEY=sk-ant-...your-key-here
   ```

**Pricing:** Pay-as-you-go, check current rates

**Test:**
```bash
python -c "from agents.claude_integrator import ClaudeIntegratorAgent; a = ClaudeIntegratorAgent(); print('✅ OK' if a.client else '❌ Not configured')"
```

---

### 4. Perplexity API (Optional) 🟢 MEDIUM PRIORITY

**Direct Link:** https://www.perplexity.ai

**Steps:**
1. **Open:** https://www.perplexity.ai
2. **Sign up** for API access
3. **Go to:** Account → API Settings
4. **Create:** API key
5. **Copy:** API key
6. **Add to `.env`:**
   ```bash
   PERPLEXITY_API_KEY=your-key-here
   ```

**Pricing:** Check current pricing

**Test:**
```bash
python -c "from agents.perplexity_integrator import PerplexityIntegratorAgent; a = PerplexityIntegratorAgent(); print('✅ OK' if a.api_key else '❌ Not configured')"
```

---

### 5. Grok/Twitter API (Optional) 🟢 MEDIUM PRIORITY

**Direct Link:** https://x.ai

**Steps:**
1. **Open:** https://x.ai
2. **Sign up** for API access
3. **Go to:** API settings
4. **Create:** API key
5. **Copy:** API key
6. **Add to `.env`:**
   ```bash
   GROK_API_KEY=your-key-here
   ```

**Pricing:** Check current pricing

**Test:**
```bash
python -c "from agents.twitter_fetcher import TwitterFetcherAgent; a = TwitterFetcherAgent(); print('✅ OK' if a.api_key else '❌ Not configured')"
```

---

## 📋 Quick Setup Checklist

### Immediate (2 minutes)
- [x] INTERNAL_API_KEY - Generated and set ✅
- [ ] Create `api_keys` table in Supabase SQL Editor
- [ ] Run `python scripts/apply_api_keys_migration.py` to log key

### High Priority (20-25 minutes)
- [ ] Get `GOOGLE_API_KEY` from https://ai.google.dev (5 min)
- [ ] Set up Google Drive OAuth (15-20 min)
  - [ ] Create Google Cloud project
  - [ ] Enable Drive API
  - [ ] Configure OAuth consent screen
  - [ ] Create OAuth credentials
  - [ ] Add to `.env`
  - [ ] Run OAuth flow

### Medium Priority (as needed)
- [ ] Get `ANTHROPIC_API_KEY` from https://console.anthropic.com
- [ ] Get `PERPLEXITY_API_KEY` from https://www.perplexity.ai
- [ ] Get `GROK_API_KEY` from https://x.ai

---

## 🔗 Quick Links

### API Keys
- **Google Gemini:** https://ai.google.dev
- **Google Cloud Console:** https://console.cloud.google.com
- **Google Drive API:** https://console.cloud.google.com/apis/library/drive.googleapis.com
- **OAuth Credentials:** https://console.cloud.google.com/apis/credentials
- **OAuth Consent Screen:** https://console.cloud.google.com/apis/credentials/consent
- **Anthropic Claude:** https://console.anthropic.com
- **Perplexity:** https://www.perplexity.ai
- **Grok/X.ai:** https://x.ai

### Database
- **Supabase Dashboard:** https://supabase.com/dashboard
- **Supabase SQL Editor:** https://supabase.com/dashboard → SQL Editor

---

## 🧪 Testing After Setup

### Test All Integrations
```bash
# Test Gemini
python -c "from agents.gemini_research import GeminiResearchAgent; a = GeminiResearchAgent(); print('✅ Gemini OK' if a.model else '❌ Need GOOGLE_API_KEY')"

# Test Drive
python -c "from agents.google_drive_integrator import GoogleDriveIntegratorAgent; a = GoogleDriveIntegratorAgent(); print('✅ Drive OK' if a.service else '❌ Need OAuth')"

# Test Claude
python -c "from agents.claude_integrator import ClaudeIntegratorAgent; a = ClaudeIntegratorAgent(); print('✅ Claude OK' if a.client else '❌ Need ANTHROPIC_API_KEY')"

# Test Perplexity
python -c "from agents.perplexity_integrator import PerplexityIntegratorAgent; a = PerplexityIntegratorAgent(); print('✅ Perplexity OK' if a.api_key else '❌ Need PERPLEXITY_API_KEY')"

# Test Grok
python -c "from agents.twitter_fetcher import TwitterFetcherAgent; a = TwitterFetcherAgent(); print('✅ Grok OK' if a.api_key else '❌ Need GROK_API_KEY')"
```

---

## 📊 Current Status

**✅ Completed:**
- INTERNAL_API_KEY generated and set in `.env`

**⚠️ Needs Database:**
- Create `api_keys` table in Supabase
- Log INTERNAL_API_KEY metadata

**❌ Not Set:**
- GOOGLE_API_KEY (High Priority)
- GOOGLE_DRIVE_CLIENT_ID (High Priority)
- GOOGLE_DRIVE_CLIENT_SECRET (High Priority)
- GOOGLE_DRIVE_REFRESH_TOKEN (High Priority - run OAuth flow)
- ANTHROPIC_API_KEY (Medium Priority)
- PERPLEXITY_API_KEY (Medium Priority)
- GROK_API_KEY (Medium Priority)

---

## 🚀 Next Steps

1. **Create API Keys Table:**
   - Go to: https://supabase.com/dashboard → SQL Editor
   - Run: `migrations/create_api_keys_table.sql`
   - Run: `python scripts/apply_api_keys_migration.py`

2. **Get Google Gemini API Key:**
   - Open: https://ai.google.dev
   - Get API key
   - Add to `.env`

3. **Set Up Google Drive OAuth:**
   - Follow steps above
   - Run OAuth flow

4. **Test Integrations:**
   - Run test commands above

---

**Last Updated:** January 6, 2025  
**Status:** ✅ INTERNAL_API_KEY Set | 🌐 Browser Setup Ready

