# Quick Database Setup Guide

**Purpose:** Fast database setup for Gematria Hive  
**Time:** 30 minutes  
**Status:** Ready to execute

---

## 🚀 5-Minute Setup

### Step 1: Create Supabase Project (5 min)

1. Go to https://supabase.com
2. Sign in or create account
3. Click **"New Project"**
4. Fill in:
   - **Name:** `gematria-hive`
   - **Database Password:** (save this securely!)
   - **Region:** Choose closest to you
5. Click **"Create new project"**
6. Wait 2-3 minutes for project to be created

---

### Step 2: Get API Keys (2 min)

1. In Supabase Dashboard, go to **Settings → API**
2. Copy **"Project URL"** → This is your `SUPABASE_URL`
   - Example: `https://abcdefghijklmnop.supabase.co`
3. Copy **"anon public"** key → This is your `SUPABASE_KEY`
   - Example: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

---

### Step 3: Set Environment Variables (1 min)

**CLI/Cursor:**
```bash
# Create .env file in project root
echo "SUPABASE_URL=https://your-project.supabase.co" > .env
echo "SUPABASE_KEY=your-anon-key-here" >> .env

# Verify
cat .env
```

**Replit:**
1. Click **lock icon** in sidebar (Secrets)
2. Add:
   - Key: `SUPABASE_URL`, Value: `https://your-project.supabase.co`
   - Key: `SUPABASE_KEY`, Value: `your-anon-key-here`
3. Click **"Add Secret"** for each

---

### Step 4: Run SQL Migrations (5 min)

1. In Supabase Dashboard, go to **SQL Editor**
2. Click **"New Query"**
3. Open `migrations/create_gematria_tables.sql` in your editor
4. Copy **ALL** SQL from that file
5. Paste into Supabase SQL Editor
6. Click **"Run"** (or Cmd/Ctrl+Enter)
7. Should see: **"Success. No rows returned"**

**Verify tables created:**
- Go to **Table Editor** in sidebar
- Should see: `bookmarks`, `hunches`, `proofs`, `gematria_words`

---

### Step 5: Verify Setup (2 min)

```bash
# Activate environment
conda activate gematria_env

# Run setup verification
python setup_database.py --verify-only
```

**Expected output:**
```
✅ Connection successful!
✅ Table 'bookmarks' exists
✅ Table 'hunches' exists
✅ Table 'proofs' exists
✅ Table 'gematria_words' exists
✅ pgvector extension appears to be enabled
✅ Database setup complete!
```

---

## ✅ Verification Checklist

After setup, verify:

- [ ] `python setup_database.py --verify-only` passes
- [ ] Tables visible in Supabase Table Editor
- [ ] Can query tables (test in SQL Editor)
- [ ] Environment variables set correctly
- [ ] pgvector extension enabled

---

## 🧪 Quick Test

```bash
# Test connection
python -c "
from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase = create_client(url, key)
result = supabase.table('bookmarks').select('*').limit(1).execute()
print('✅ Connection successful!')
print(f'Found {len(result.data)} rows')
"
```

---

## 🚀 Next Steps

Once database is set up:

1. **Run end-to-end tests:**
   ```bash
   python test_e2e.py --verbose
   ```

2. **Test kanban dashboard:**
   ```bash
   streamlit run app.py
   ```

3. **Test full pipeline:**
   ```bash
   python scripts/extract.py --source test_data.json --output extracted.json
   python scripts/distill.py --input extracted.json --output processed.json
   python scripts/ingest.py --input processed.json
   ```

---

## 📚 Full Documentation

- **SUPABASE_SETUP.md** - Detailed setup guide
- **setup_database.py** - Automated setup script
- **COMPLETION_CHECKLIST.md** - Complete checklist

---

**Ready to set up!** 🐝✨

