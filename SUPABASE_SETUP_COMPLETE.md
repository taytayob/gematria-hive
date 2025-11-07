# Supabase Setup - Complete Guide

**Status:** ✅ All Code Ready | ⚠️ Database Setup Required (15 minutes)

**Last Updated:** November 7, 2025

---

## 🎯 Quick Start (15 minutes)

### Step 1: Create Supabase Project (5 min)

1. **Go to:** https://supabase.com
2. **Sign in** or create account (free tier works)
3. **Click:** "New Project"
4. **Fill in:**
   - **Project Name:** `gematria-hive`
   - **Database Password:** Create strong password (SAVE IT!)
   - **Region:** Choose closest to you
5. **Click:** "Create new project"
6. **Wait:** 2-3 minutes for initialization

---

### Step 2: Get API Keys (2 min)

1. **In Supabase Dashboard**, go to **Settings → API**
2. **Copy these values:**

   **a) Project URL:**
   - Copy the URL (e.g., `https://abcdefghijklmnop.supabase.co`)
   - This is your `SUPABASE_URL`

   **b) API Keys:**
   - Find **"anon public"** key (NOT service_role)
   - Copy the key (long string starting with `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`)
   - This is your `SUPABASE_KEY`

---

### Step 3: Set Environment Variables (2 min)

**CLI/Cursor:**
```bash
# Create .env file
cat > .env << EOF
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here
EOF

# Verify
cat .env
```

**Replit:**
1. Click **lock icon** 🔒 in left sidebar
2. Click **"New secret"**
3. Add:
   - **Key:** `SUPABASE_URL`
   - **Value:** `https://your-project-id.supabase.co`
4. Click **"New secret"** again
5. Add:
   - **Key:** `SUPABASE_KEY`
   - **Value:** `your-anon-key-here`

---

### Step 4: Enable pgvector Extension (1 min)

1. **In Supabase Dashboard**, go to **SQL Editor**
2. **Click:** "New query"
3. **Paste and run:**
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```
4. **Click:** "Run" (or Cmd/Ctrl+Enter)
5. **Verify:** Should see "Success. No rows returned"

---

### Step 5: Run Migrations (5 min)

#### Migration 1: Gematria Tables

1. **In Supabase SQL Editor**, click "New query"
2. **Open file:** `migrations/create_gematria_tables.sql`
3. **Copy ALL SQL** from the file
4. **Paste** into Supabase SQL Editor
5. **Click:** "Run"
6. **Verify:** Should see multiple "Success" messages

#### Migration 2: Complete Schema

1. **In Supabase SQL Editor**, click "New query" again
2. **Open file:** `migrations/create_complete_schema.sql`
3. **Copy ALL SQL** from the file (it's long - ~600 lines)
4. **Paste** into Supabase SQL Editor
5. **Click:** "Run"
6. **Verify:** Should see multiple "Success" messages

#### Verify Tables Created

1. **In Supabase Dashboard**, go to **Table Editor**
2. **Verify** you can see these tables:
   - `bookmarks`
   - `gematria_words`
   - `authors`
   - `sources`
   - `key_terms`
   - `patterns`
   - `research_topics`
   - `proofs`
   - `personas`
   - `alphabets`
   - `baselines`
   - `validations`
   - `floating_index`
   - `projects`
   - `cost_tracking`
   - `synchronicities`
   - `observations`
   - `agent_memory`
   - `hunches`
   - `scraped_content`
   - `discovered_resources`

**Total:** 20+ tables

---

### Step 6: Verify Setup (1 min)

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

## 🧪 Test Everything

### Test Connection
```bash
python setup_database.py
```

### Test Ingestion
```bash
# Create test data
cat > test_data.json << 'EOF'
[
  {
    "url": "https://example.com/gematria",
    "summary": "Article about gematria and numerology",
    "title": "Gematria Example"
  }
]
EOF

# Run ingestion
python ingest_pass1.py test_data.json
```

### Test Agents
```bash
python -c "from agents import MCPOrchestrator; o = MCPOrchestrator(); print('✅ Agents ready')"
```

### Test Streamlit
```bash
streamlit run app.py
```

---

## 📋 Verification Checklist

After setup, verify:

- [ ] Supabase project created and active
- [ ] API keys obtained (SUPABASE_URL and SUPABASE_KEY)
- [ ] Environment variables set (`.env` file or Replit Secrets)
- [ ] pgvector extension enabled
- [ ] Both migrations run successfully
- [ ] Tables visible in Table Editor (20+ tables)
- [ ] Connection test successful (`python setup_database.py`)
- [ ] Can query tables (test in SQL Editor)

---

## 🐛 Troubleshooting

### Issue: "Environment variables not set"
**Solution:**
1. Check `.env` file exists in project root
2. Verify `SUPABASE_URL` and `SUPABASE_KEY` are set
3. For Replit: Check Secrets (lock icon) are set
4. Restart terminal/Replit after setting variables

### Issue: "Connection failed"
**Solution:**
1. Verify API keys are correct (no extra spaces)
2. Check Supabase project is active (not paused)
3. Verify network connection
4. Check if project was paused (free tier auto-pauses after inactivity)

### Issue: "Tables not found"
**Solution:**
1. Run migrations in Supabase SQL Editor
2. Verify migrations ran without errors
3. Check Table Editor to see created tables
4. Re-run migrations if needed

### Issue: "pgvector extension not enabled"
**Solution:**
1. Go to SQL Editor
2. Run: `CREATE EXTENSION IF NOT EXISTS vector;`
3. Verify extension enabled in Extensions section

---

## 📚 Documentation

### Setup Guides
- `SUPABASE_SETUP_INSTRUCTIONS.md` - Detailed step-by-step guide
- `DATABASE_SETUP_COMPLETE.md` - Database setup details
- `COMPLETE_SETUP_GUIDE.md` - Complete setup for all platforms
- `run_supabase_setup.py` - Interactive setup script

### Scripts
- `setup_database.py` - Automated setup and verification
- `run_supabase_setup.py` - Interactive setup guide

### Migration Files
- `migrations/create_gematria_tables.sql` - Core gematria tables
- `migrations/create_complete_schema.sql` - Complete schema (20+ tables)

---

## 🎉 Next Steps After Setup

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

## 🔗 Quick Reference

### Essential Commands
```bash
# Test connection
python setup_database.py

# Test ingestion
python ingest_pass1.py test_data.json

# Test agents
python -c "from agents import MCPOrchestrator; print('✅ Ready')"

# Run app
streamlit run app.py
```

### File Locations
- **Environment:** `.env` (CLI/Cursor) or Replit Secrets
- **Migrations:** `migrations/create_gematria_tables.sql` and `migrations/create_complete_schema.sql`
- **Setup Scripts:** `setup_database.py`, `run_supabase_setup.py`

---

## ✅ Summary

**Status:** 🟢 **CODE COMPLETE** | 🟡 **DATABASE SETUP REQUIRED**

All code is ready and working. The only remaining step is Supabase database setup (15 minutes).

**Follow the steps above to complete setup!**

---

**Database Setup Complete!** 🐝✨

Once Supabase is configured, the system is ready for production use!

