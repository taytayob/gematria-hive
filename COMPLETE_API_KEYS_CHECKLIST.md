# Complete API Keys & Configs Checklist - Gematria Hive

**Date:** January 6, 2025  
**Status:** 📋 Complete Checklist | 🔍 Current Status Check  
**Purpose:** Comprehensive list of all API keys and configs needed

---

## ✅ Currently Configured

| Variable | Status | Purpose |
|----------|--------|---------|
| `SUPABASE_URL` | ✅ SET | Database connection |
| `SUPABASE_KEY` | ✅ SET | Database authentication |

---

## 🔴 CRITICAL - Required for Core Functionality

### 1. Internal API Key (Security)

| Variable | Status | Priority | Purpose |
|----------|--------|----------|---------|
| `INTERNAL_API_KEY` | ⚠️ DEFAULT | 🔴 Critical | Internal API authentication |

**Current Status:** Using default value `internal-api-key-change-in-production`

**Action Required:**
```bash
# Generate a secure random key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Add to .env
INTERNAL_API_KEY=your-secure-random-key-here
```

**Why:** Security - prevents unauthorized access to internal API endpoints

**Impact:** ⚠️ Using default key is insecure for production

---

## 🟡 HIGH PRIORITY - Core Integrations

### 2. Google Gemini API (Deep Research)

| Variable | Status | Priority | Purpose | Agent |
|----------|--------|----------|---------|-------|
| `GOOGLE_API_KEY` | ❌ NOT SET | 🟡 High | Gemini Deep Research | `gemini_research.py` |
| `GEMINI_MODEL` | ⚠️ DEFAULT | 🟢 Low | Model selection | `gemini_research.py` |

**Current Status:** Not configured - agent disabled

**Get It:**
1. **Open:** https://ai.google.dev
2. **Click:** "Get API Key"
3. **Create/Select:** Project
4. **Copy:** API key
5. **Add to `.env`:**
   ```bash
   GOOGLE_API_KEY=your-api-key-here
   GEMINI_MODEL=gemini-2.0-flash-exp  # Optional, has default
   ```

**Free Tier:** ✅ Available with generous limits

**Impact:** Enables Gemini Deep Research agent for comprehensive research reports

**Agent:** `agents/gemini_research.py`

---

### 3. Google Drive OAuth (Drive Integration)

| Variable | Status | Priority | Purpose | Agent |
|----------|--------|----------|---------|-------|
| `GOOGLE_DRIVE_CLIENT_ID` | ❌ NOT SET | 🟡 High | OAuth client ID | `google_drive_integrator.py` |
| `GOOGLE_DRIVE_CLIENT_SECRET` | ❌ NOT SET | 🟡 High | OAuth client secret | `google_drive_integrator.py` |
| `GOOGLE_DRIVE_REFRESH_TOKEN` | ❌ NOT SET | 🟡 High | OAuth refresh token | `google_drive_integrator.py` |

**Current Status:** Not configured - agent disabled

**Get It:**
1. **Open:** https://console.cloud.google.com
2. **Create:** New project (or select existing)
3. **Enable:** Google Drive API
   - Go to: https://console.cloud.google.com/apis/library
   - Search: "Google Drive API"
   - Click: "Enable"
4. **Create OAuth Credentials:**
   - Go to: https://console.cloud.google.com/apis/credentials
   - Click: "Create Credentials" → "OAuth client ID"
   - Type: Desktop app
   - Name: "Gematria Hive Drive Integration"
   - Copy: Client ID and Client Secret
5. **Add to `.env`:**
   ```bash
   GOOGLE_DRIVE_CLIENT_ID=your-client-id
   GOOGLE_DRIVE_CLIENT_SECRET=your-client-secret
   ```
6. **Run OAuth Flow:**
   ```bash
   python scripts/setup_google_drive_oauth.py
   ```
   This will:
   - Open browser for authentication
   - Save refresh token to `.env`

**Impact:** Enables Google Drive integration for bookmark extraction

**Agent:** `agents/google_drive_integrator.py`

---

## 🟢 MEDIUM PRIORITY - Enhanced Features

### 4. Anthropic Claude API (Claude Integration)

| Variable | Status | Priority | Purpose | Agent |
|----------|--------|----------|---------|-------|
| `ANTHROPIC_API_KEY` | ❌ NOT SET | 🟢 Medium | Claude API access | `claude_integrator.py` |
| `CLAUDE_BROWSER_PLUGIN_ENABLED` | ⚠️ DEFAULT | 🟢 Low | Browser plugin | `claude_integrator.py` |

**Current Status:** Not configured - agent disabled

**Get It:**
1. **Open:** https://console.anthropic.com
2. **Sign in** or create account
3. **Go to:** API Keys
4. **Create:** New API key
5. **Copy:** API key
6. **Add to `.env`:**
   ```bash
   ANTHROPIC_API_KEY=your-api-key-here
   CLAUDE_BROWSER_PLUGIN_ENABLED=false  # Optional, default false
   ```

**Pricing:** Pay-as-you-go, check current rates

**Impact:** Enables Claude integration for advanced reasoning and analysis

**Agent:** `agents/claude_integrator.py`

---

### 5. Perplexity API (Enhanced Search)

| Variable | Status | Priority | Purpose | Agent |
|----------|--------|----------|---------|-------|
| `PERPLEXITY_API_KEY` | ❌ NOT SET | 🟢 Medium | Perplexity search | `perplexity_integrator.py` |

**Current Status:** Not configured - agent disabled

**Get It:**
1. **Open:** https://www.perplexity.ai
2. **Sign up** for API access
3. **Go to:** API settings
4. **Create:** API key
5. **Copy:** API key
6. **Add to `.env`:**
   ```bash
   PERPLEXITY_API_KEY=your-api-key-here
   ```

**Pricing:** Check current pricing at https://www.perplexity.ai

**Impact:** Enables Perplexity search for enhanced research capabilities

**Agent:** `agents/perplexity_integrator.py`

---

### 6. Grok/Twitter API (Twitter Integration)

| Variable | Status | Priority | Purpose | Agent |
|----------|--------|----------|---------|-------|
| `GROK_API_KEY` | ❌ NOT SET | 🟢 Medium | Grok/Twitter API | `twitter_fetcher.py` |

**Current Status:** Not configured - agent limited

**Get It:**
1. **Open:** https://x.ai
2. **Sign up** for API access
3. **Go to:** API settings
4. **Create:** API key
5. **Copy:** API key
6. **Add to `.env`:**
   ```bash
   GROK_API_KEY=your-api-key-here
   ```

**Pricing:** Check current pricing at https://x.ai

**Impact:** Enables Twitter/X thread fetching via Grok API

**Agent:** `agents/twitter_fetcher.py`

---

## 🔵 OPTIONAL - Additional Features

### 7. OpenAI API (OpenAI Integration)

| Variable | Status | Priority | Purpose | Agent |
|----------|--------|----------|---------|-------|
| `OPENAI_API_KEY` | ❌ NOT SET | 🔵 Optional | OpenAI GPT access | Future integration |

**Current Status:** Not implemented yet

**Get It:**
1. **Open:** https://platform.openai.com
2. **Sign in** or create account
3. **Go to:** API Keys
4. **Create:** New secret key
5. **Copy:** API key
6. **Add to `.env`:**
   ```bash
   OPENAI_API_KEY=your-api-key-here
   ```

**Pricing:** Pay-as-you-go, check current rates

**Impact:** Would enable OpenAI GPT integration (if implemented)

**Status:** ⚠️ Not currently used in codebase

---

### 8. Email Alerts (Cost Monitoring)

| Variable | Status | Priority | Purpose | Agent |
|----------|--------|----------|---------|-------|
| `COST_ALERT_EMAIL` | ❌ NOT SET | 🔵 Optional | Email for cost alerts | `cost_manager.py` |
| `SMTP_SERVER` | ⚠️ DEFAULT | 🔵 Optional | SMTP server | `cost_manager.py` |
| `SMTP_PORT` | ⚠️ DEFAULT | 🔵 Optional | SMTP port | `cost_manager.py` |
| `SMTP_USER` | ❌ NOT SET | 🔵 Optional | SMTP username | `cost_manager.py` |
| `SMTP_PASSWORD` | ❌ NOT SET | 🔵 Optional | SMTP password | `cost_manager.py` |

**Current Status:** Not configured - email alerts disabled

**Configure:**
```bash
# For Gmail
COST_ALERT_EMAIL=your-email@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password  # Use app-specific password
```

**Impact:** Enables email alerts when cost threshold is reached

**Agent:** `agents/cost_manager.py`

**Note:** Defaults to Gmail SMTP if not set

---

### 9. ClickHouse (Phase 3+ Analytics)

| Variable | Status | Priority | Purpose |
|----------|--------|----------|---------|
| `CLICKHOUSE_HOST` | ❌ NOT SET | 🔵 Optional | ClickHouse host |
| `CLICKHOUSE_PASSWORD` | ❌ NOT SET | 🔵 Optional | ClickHouse password |

**Current Status:** Not implemented yet (Phase 3+)

**Impact:** Would enable ClickHouse analytics database (future feature)

**Status:** ⚠️ Not currently used in codebase

---

## 📊 Summary by Priority

### 🔴 Critical (Must Do)
- [ ] `INTERNAL_API_KEY` - Change from default (security)

### 🟡 High Priority (Core Features)
- [ ] `GOOGLE_API_KEY` - Gemini Deep Research (5 min)
- [ ] `GOOGLE_DRIVE_CLIENT_ID` - Drive integration (15-20 min)
- [ ] `GOOGLE_DRIVE_CLIENT_SECRET` - Drive integration
- [ ] `GOOGLE_DRIVE_REFRESH_TOKEN` - Run OAuth flow

### 🟢 Medium Priority (Enhanced Features)
- [ ] `ANTHROPIC_API_KEY` - Claude integration
- [ ] `PERPLEXITY_API_KEY` - Perplexity search
- [ ] `GROK_API_KEY` - Twitter integration

### 🔵 Optional (Nice to Have)
- [ ] `OPENAI_API_KEY` - OpenAI integration (not implemented)
- [ ] `COST_ALERT_EMAIL` - Email alerts
- [ ] `SMTP_*` - Email configuration
- [ ] `CLICKHOUSE_*` - Analytics (Phase 3+)

---

## 🚀 Quick Setup Order

### Step 1: Security (2 minutes)
```bash
# Generate secure key
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Add to .env
INTERNAL_API_KEY=generated-key-here
```

### Step 2: Gemini (5 minutes)
1. Get API key from https://ai.google.dev
2. Add `GOOGLE_API_KEY` to `.env`

### Step 3: Drive (15-20 minutes)
1. Set up Google Cloud project
2. Enable Drive API
3. Create OAuth credentials
4. Add `GOOGLE_DRIVE_CLIENT_ID` and `GOOGLE_DRIVE_CLIENT_SECRET` to `.env`
5. Run `python scripts/setup_google_drive_oauth.py`

### Step 4: Optional Integrations (as needed)
- Claude: https://console.anthropic.com
- Perplexity: https://www.perplexity.ai
- Grok: https://x.ai

---

## 🧪 Testing After Setup

### Test Each Integration
```bash
# Test Gemini
python -c "from agents.gemini_research import GeminiResearchAgent; a = GeminiResearchAgent(); print('✅ OK' if a.model else '❌ Need GOOGLE_API_KEY')"

# Test Drive
python -c "from agents.google_drive_integrator import GoogleDriveIntegratorAgent; a = GoogleDriveIntegratorAgent(); print('✅ OK' if a.service else '❌ Need OAuth credentials')"

# Test Claude
python -c "from agents.claude_integrator import ClaudeIntegratorAgent; a = ClaudeIntegratorAgent(); print('✅ OK' if a.client else '❌ Need ANTHROPIC_API_KEY')"

# Test Perplexity
python -c "from agents.perplexity_integrator import PerplexityIntegratorAgent; a = PerplexityIntegratorAgent(); print('✅ OK' if PERPLEXITY_API_KEY else '❌ Need PERPLEXITY_API_KEY')"

# Test Grok
python -c "from agents.twitter_fetcher import TwitterFetcherAgent; a = TwitterFetcherAgent(); print('✅ OK' if a.api_key else '❌ Need GROK_API_KEY')"
```

---

## 📋 Complete .env Template

```bash
# ============================================
# CRITICAL - Database Configuration
# ============================================
SUPABASE_URL=https://your-project-id.supabase.co  # ✅ SET
SUPABASE_KEY=your-anon-key-here  # ✅ SET

# ============================================
# CRITICAL - Internal API Security
# ============================================
INTERNAL_API_KEY=your-secure-random-key-here  # ⚠️ CHANGE FROM DEFAULT

# ============================================
# HIGH PRIORITY - Google Gemini Integration
# ============================================
GOOGLE_API_KEY=your-gemini-api-key-here  # ❌ NOT SET
GEMINI_MODEL=gemini-2.0-flash-exp  # Optional, has default

# ============================================
# HIGH PRIORITY - Google Drive Integration
# ============================================
GOOGLE_DRIVE_CLIENT_ID=your-client-id  # ❌ NOT SET
GOOGLE_DRIVE_CLIENT_SECRET=your-client-secret  # ❌ NOT SET
GOOGLE_DRIVE_REFRESH_TOKEN=your-refresh-token  # ❌ NOT SET (run OAuth flow)

# ============================================
# MEDIUM PRIORITY - AI/ML API Keys
# ============================================
ANTHROPIC_API_KEY=your-claude-key  # ❌ NOT SET
PERPLEXITY_API_KEY=your-perplexity-key  # ❌ NOT SET
GROK_API_KEY=your-grok-key  # ❌ NOT SET
OPENAI_API_KEY=your-openai-key  # ❌ NOT SET (not implemented)

# ============================================
# OPTIONAL - Email Alerts
# ============================================
COST_ALERT_EMAIL=your-email@example.com  # ❌ NOT SET
SMTP_SERVER=smtp.gmail.com  # Optional, has default
SMTP_PORT=587  # Optional, has default
SMTP_USER=your-email@gmail.com  # ❌ NOT SET
SMTP_PASSWORD=your-app-password  # ❌ NOT SET

# ============================================
# OPTIONAL - ClickHouse (Phase 3+)
# ============================================
CLICKHOUSE_HOST=your-clickhouse-host  # ❌ NOT SET
CLICKHOUSE_PASSWORD=your-clickhouse-password  # ❌ NOT SET
```

---

## 📊 Current Status Summary

**✅ Configured (2/14):**
- SUPABASE_URL
- SUPABASE_KEY

**⚠️ Using Defaults (2/14):**
- INTERNAL_API_KEY (needs change for security)
- GEMINI_MODEL (has default, optional)

**❌ Not Set (10/14):**
- GOOGLE_API_KEY (High Priority)
- GOOGLE_DRIVE_CLIENT_ID (High Priority)
- GOOGLE_DRIVE_CLIENT_SECRET (High Priority)
- GOOGLE_DRIVE_REFRESH_TOKEN (High Priority)
- ANTHROPIC_API_KEY (Medium Priority)
- PERPLEXITY_API_KEY (Medium Priority)
- GROK_API_KEY (Medium Priority)
- OPENAI_API_KEY (Optional, not implemented)
- Email config (Optional)
- ClickHouse config (Optional, Phase 3+)

---

## 🎯 Recommended Setup Order

1. **Security First** (2 min)
   - Change `INTERNAL_API_KEY` from default

2. **High Priority** (20-25 min)
   - Get `GOOGLE_API_KEY` (5 min)
   - Set up Drive OAuth (15-20 min)

3. **Medium Priority** (as needed)
   - Add Claude, Perplexity, Grok keys when needed

4. **Optional** (as needed)
   - Email alerts, ClickHouse, etc.

---

## 📚 Documentation Links

- **Setup Guide:** `SETUP_COMPLETE_GUIDE.md` (with browser links)
- **Manual Setup:** `MANUAL_SETUP_REQUIRED.md`
- **Project Audit:** `PROJECT_AUDIT_AND_INSIGHTS.md`
- **This Checklist:** `COMPLETE_API_KEYS_CHECKLIST.md`

---

**Last Updated:** January 6, 2025  
**Status:** 📋 Complete Checklist Ready

