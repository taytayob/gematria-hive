# Supabase Database Setup - Step by Step

**Purpose:** Complete step-by-step instructions to set up Supabase database

**Time Required:** 15 minutes

**Last Updated:** November 7, 2025

---

## 🚀 Quick Setup (15 minutes)

### Step 1: Create Supabase Project (5 minutes)

1. **Go to:** https://supabase.com
2. **Sign in** or create account (free tier works perfectly)
3. **Click:** "New Project" button
4. **Fill in the form:**
   - **Project Name:** `gematria-hive`
   - **Database Password:** Create a strong password (SAVE THIS - you'll need it!)
   - **Region:** Choose the region closest to you
5. **Click:** "Create new project"
6. **Wait:** 2-3 minutes for project initialization (you'll see a progress indicator)

---

### Step 2: Get API Keys (2 minutes)

1. **In Supabase Dashboard**, go to **Settings** → **API**
2. **Copy these two values:**

   **a) Project URL:**
   - Look for "Project URL" section
   - Copy the URL (looks like: `https://abcdefghijklmnop.supabase.co`)
   - This is your `SUPABASE_URL`

   **b) API Keys:**
   - Look for "Project API keys" section
   - Find the **"anon public"** key (NOT the service_role key)
   - Copy the key (long string starting with `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`)
   - This is your `SUPABASE_KEY`

---

### Step 3: Set Environment Variables (2 minutes)

**CLI/Cursor (Mac Terminal):**
```bash
# Navigate to project directory
cd /Users/cooperladd/Desktop/gematria-hive/gematria-hive

# Create .env file
cat > .env << EOF
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here
EOF

# Verify it was created
cat .env
```

**Replit:**
1. Click the **lock icon** 🔒 in the left sidebar
2. Click **"New secret"**
3. Add first secret:
   - **Key:** `SUPABASE_URL`
   - **Value:** `https://your-project-id.supabase.co`
4. Click **"New secret"** again
5. Add second secret:
   - **Key:** `SUPABASE_KEY`
   - **Value:** `your-anon-key-here`

---

### Step 4: Enable pgvector Extension (1 minute)

1. **In Supabase Dashboard**, go to **SQL Editor** (left sidebar)
2. **Click:** "New query" button
3. **Copy and paste this SQL:**
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```
4. **Click:** "Run" button (or press Cmd/Ctrl+Enter)
5. **Verify:** Should see "Success. No rows returned" message

---

### Step 5: Run Migrations (5 minutes)

#### Migration 1: Gematria Tables

1. **In Supabase SQL Editor**, click "New query"
2. **Open file:** `migrations/create_gematria_tables.sql` (in your project)
3. **Copy ALL the SQL content** from the file
4. **Paste** into Supabase SQL Editor
5. **Click:** "Run"
6. **Verify:** Should see multiple "Success" messages

#### Migration 2: Complete Schema

1. **In Supabase SQL Editor**, click "New query" again
2. **Open file:** `migrations/create_complete_schema.sql` (in your project)
3. **Copy ALL the SQL content** from the file
4. **Paste** into Supabase SQL Editor
5. **Click:** "Run"
6. **Verify:** Should see multiple "Success" messages

#### Verify Tables Created

1. **In Supabase Dashboard**, go to **Table Editor** (left sidebar)
2. **Verify** you can see these tables:
   - `bookmarks`
   - `gematria_words`
   - `authors`
   - `sources`
   - `key_terms`
   - `patterns`
   - And many more...

---

### Step 6: Test Connection (1 minute)

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

## ✅ Verification Checklist

After setup, verify:

- [ ] Supabase project created and active
- [ ] API keys obtained (SUPABASE_URL and SUPABASE_KEY)
- [ ] Environment variables set (`.env` file or Replit Secrets)
- [ ] pgvector extension enabled
- [ ] Both migrations run successfully
- [ ] Tables visible in Table Editor
- [ ] Connection test successful (`python setup_database.py`)

---

## 🧪 Test Database Connection

### Quick Test
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

if url and key:
    supabase = create_client(url, key)
    result = supabase.table('bookmarks').select('*').limit(1).execute()
    print('✅ Connection successful!')
else:
    print('❌ Environment variables not set')
```

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

## 📚 Next Steps After Setup

1. **Test Ingestion**
   ```bash
   # Create test data
   cat > test_data.json << 'EOF'
   [
     {
       "url": "https://example.com/gematria",
       "summary": "Article about gematria and numerology"
     }
   ]
   EOF
   
   # Run ingestion
   python ingest_pass1.py test_data.json
   ```

2. **Test Agents**
   ```bash
   python -c "from agents import MCPOrchestrator; o = MCPOrchestrator(); print('✅ Agents ready')"
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
- `DATABASE_SETUP_COMPLETE.md` - Detailed database setup
- `setup_database.py` - Automated setup script
- `SUPABASE_SETUP.md` - Original Supabase setup guide

---

## 📋 Quick Reference

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
- **Setup Script:** `setup_database.py`

---

**Database Setup Complete!** 🐝✨

Once Supabase is configured, the system is ready for production use!

