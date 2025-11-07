# Database Setup - Complete Guide

**Purpose:** Step-by-step guide to set up Supabase database for Gematria Hive

**Last Updated:** November 7, 2025

---

## 🚀 Quick Setup (15 minutes)

### Step 1: Create Supabase Project (5 minutes)

1. **Go to:** https://supabase.com
2. **Sign in** or create account (free tier works)
3. **Click:** "New Project"
4. **Fill in:**
   - **Project Name:** `gematria-hive`
   - **Database Password:** (create a strong password and **SAVE IT**)
   - **Region:** Choose closest to you
5. **Click:** "Create new project"
6. **Wait:** 2-3 minutes for project initialization

---

### Step 2: Get API Keys (2 minutes)

1. **Go to:** Settings → API (in Supabase Dashboard)
2. **Copy these values:**
   - **Project URL** → This is your `SUPABASE_URL`
     - Example: `https://abcdefghijklmnop.supabase.co`
   - **anon public** key → This is your `SUPABASE_KEY`
     - Example: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

---

### Step 3: Set Environment Variables (2 minutes)

**CLI/Cursor:**
```bash
# Create .env file
cat > .env << EOF
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
EOF
```

**Replit:**
1. Click **lock icon** in sidebar
2. Add secrets:
   - `SUPABASE_URL` = `https://your-project.supabase.co`
   - `SUPABASE_KEY` = `your-anon-key-here`

---

### Step 4: Enable pgvector Extension (1 minute)

1. **Go to:** Supabase Dashboard → SQL Editor
2. **Click:** "New Query"
3. **Run this SQL:**
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```
4. **Click:** "Run" (or Cmd/Ctrl+Enter)
5. **Verify:** Should see "Success. No rows returned"

---

### Step 5: Run Migrations (5 minutes)

1. **Go to:** Supabase Dashboard → SQL Editor
2. **Click:** "New Query"

#### Migration 1: Gematria Tables
1. **Open:** `migrations/create_gematria_tables.sql`
2. **Copy** all SQL content
3. **Paste** into SQL Editor
4. **Click:** "Run"
5. **Verify:** Should see "Success" messages

#### Migration 2: Complete Schema
1. **Open:** `migrations/create_complete_schema.sql`
2. **Copy** all SQL content
3. **Paste** into SQL Editor
4. **Click:** "Run"
5. **Verify:** Should see "Success" messages

---

### Step 6: Verify Setup (1 minute)

**CLI/Cursor:**
```bash
conda activate gematria_env
python setup_database.py
```

**Replit:**
```bash
python setup_database.py
```

**Expected Output:**
```
✅ Connection successful!
✅ Table 'bookmarks' exists
✅ Table 'gematria_words' exists
✅ All required tables exist!
✅ pgvector extension appears to be enabled
✅ Database setup complete!
```

---

## 📋 Verification Checklist

After setup, verify:

- [ ] Supabase project created
- [ ] API keys obtained
- [ ] Environment variables set (`.env` file or Replit Secrets)
- [ ] pgvector extension enabled
- [ ] Migrations run successfully
- [ ] Tables created (check in Table Editor)
- [ ] Connection test successful

---

## 🗄️ Tables Created

After running migrations, you should have:

### Core Tables
- ✅ `bookmarks` - Main bookmark storage
- ✅ `gematria_words` - Gematria calculations
- ✅ `scraped_content` - Web scraped content

### Analysis Tables
- ✅ `authors` - Author tracking
- ✅ `sources` - Source repository
- ✅ `key_terms` - Key terms and gematria values
- ✅ `patterns` - Pattern detection results
- ✅ `research_topics` - Research topics
- ✅ `proofs` - Mathematical proofs

### System Tables
- ✅ `personas` - Master personas
- ✅ `alphabets` - Character values
- ✅ `baselines` - Validation baselines
- ✅ `validations` - Proof validations
- ✅ `floating_index` - Quick lookup cache
- ✅ `projects` - Sandbox projects
- ✅ `cost_tracking` - API cost tracking
- ✅ `synchronicities` - Pattern connections
- ✅ `observations` - Observer agent data
- ✅ `cache_logs` - Caching system
- ✅ `hunches` - Hunches and insights
- ✅ `agent_memory` - Agent memory storage

**Total:** 20+ tables

---

## 🧪 Test Database Connection

### Test Script
```bash
python setup_database.py
```

### Manual Test
```python
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')

supabase = create_client(url, key)

# Test connection
result = supabase.table('bookmarks').select('*').limit(1).execute()
print('✅ Connection successful!')
```

---

## 🐛 Troubleshooting

### Issue: "Environment variables not set"
**Solution:**
1. Check `.env` file exists in project root
2. Verify `SUPABASE_URL` and `SUPABASE_KEY` are set
3. For Replit: Check Secrets (lock icon)

### Issue: "Connection failed"
**Solution:**
1. Verify API keys are correct
2. Check Supabase project is active
3. Verify network connection
4. Check if project was paused (free tier)

### Issue: "Tables not found"
**Solution:**
1. Run migrations in Supabase SQL Editor
2. Verify migrations ran successfully
3. Check Table Editor to see created tables

### Issue: "pgvector extension not enabled"
**Solution:**
1. Go to SQL Editor
2. Run: `CREATE EXTENSION IF NOT EXISTS vector;`
3. Verify extension enabled

---

## 📚 Next Steps

After database setup:

1. **Test Ingestion**
   ```bash
   python ingest_pass1.py test_data.json
   ```

2. **Test Agents**
   ```bash
   python -c "from agents import MCPOrchestrator; o = MCPOrchestrator(); print('✅ Ready')"
   ```

3. **Run Streamlit**
   ```bash
   streamlit run app.py
   ```

4. **Verify Data**
   - Go to Supabase Dashboard → Table Editor
   - Check `bookmarks` table has data

---

## 🔗 Related Documentation

- `COMPLETE_SETUP_GUIDE.md` - Complete setup guide
- `SUPABASE_SETUP.md` - Detailed Supabase setup
- `setup_database.py` - Automated setup script

---

**Database Setup Complete!** 🐝✨

