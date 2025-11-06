# Supabase Database Setup - Complete Guide

**Purpose:** Set up Supabase database for Gematria Hive ingestion and storage

**Last Updated:** November 6, 2025

---

## ✅ Prerequisites

- ✅ Supabase account created (free tier works)
- ✅ Python 3.12 environment set up
- ✅ All dependencies installed (`pip install -r requirements.txt`)
- ✅ Git synced across CLI, Replit, and Cursor

---

## 🚀 Step 1: Create Supabase Project

### In Supabase Dashboard

1. **Go to:** https://supabase.com
2. **Sign in** or create account
3. **Click:** "New Project"
4. **Fill in:**
   - Project Name: `gematria-hive`
   - Database Password: (save this securely)
   - Region: Choose closest to you
5. **Click:** "Create new project"
6. **Wait:** 2-3 minutes for project to initialize

---

## 🔑 Step 2: Get API Keys

### In Supabase Dashboard

1. **Go to:** Settings → API
2. **Copy these values:**
   - **Project URL** → `SUPABASE_URL`
   - **anon public** key → `SUPABASE_KEY`

### Set Environment Variables

#### Replit

**Option 1: Edit `.replit` file**
```toml
[env]
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key-here"
```

**Option 2: Use Replit Secrets** (Recommended)
1. Click lock icon in sidebar
2. Add `SUPABASE_URL` and `SUPABASE_KEY`
3. Access via `os.getenv()` in code

#### CLI/Cursor

**Create `.env` file:**
```bash
# In Cursor/CLI terminal
cd /Users/cooperladd/Desktop/gematria-hive/gematria-hive
nano .env  # or use Cursor editor
```

**Add to `.env`:**
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

**Verify:**
```bash
# In Cursor/CLI terminal (with venv activated)
source venv/bin/activate
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('URL:', os.getenv('SUPABASE_URL')[:30] + '...')"
```

---

## 🗄️ Step 3: Enable pgvector Extension

### In Supabase Dashboard

1. **Go to:** SQL Editor
2. **Click:** "New Query"
3. **Run this SQL:**
```sql
-- Enable pgvector extension for embeddings
CREATE EXTENSION IF NOT EXISTS vector;
```
4. **Click:** "Run" (or Cmd/Ctrl+Enter)
5. **Verify:** Should see "Success. No rows returned"

---

## 📊 Step 4: Create Tables

### In Supabase SQL Editor

**Run this complete SQL script:**

```sql
-- 1. Bookmarks Table (main data storage)
CREATE TABLE IF NOT EXISTS bookmarks (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  url TEXT,
  summary TEXT,
  embedding vector(384),  -- pgvector for similarity search
  tags TEXT[],
  phase TEXT,
  relevance_score FLOAT,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Hunches Table (for logging and tracking)
CREATE TABLE IF NOT EXISTS hunches (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  content TEXT,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  status TEXT DEFAULT 'pending',
  cost FLOAT DEFAULT 0.0,
  links TEXT[],
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Proofs Table (for future proof generation)
CREATE TABLE IF NOT EXISTS proofs (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  theorem TEXT,
  report TEXT,
  accuracy_metric FLOAT,
  efficiency_score FLOAT,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Create indexes for performance
CREATE INDEX IF NOT EXISTS bookmarks_phase_idx ON bookmarks(phase);
CREATE INDEX IF NOT EXISTS bookmarks_timestamp_idx ON bookmarks(timestamp);
CREATE INDEX IF NOT EXISTS bookmarks_relevance_idx ON bookmarks(relevance_score);

-- 5. Vector similarity search index (IVFFlat for pgvector)
CREATE INDEX IF NOT EXISTS bookmarks_embedding_idx ON bookmarks 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- 6. Dynamic view for recent updates
CREATE OR REPLACE VIEW dynamic_bookmarks AS 
SELECT * FROM bookmarks 
WHERE timestamp > NOW() - INTERVAL '1 day'
ORDER BY timestamp DESC;

-- 7. Enable Row Level Security (RLS) - Optional but recommended
ALTER TABLE bookmarks ENABLE ROW LEVEL SECURITY;
ALTER TABLE hunches ENABLE ROW LEVEL SECURITY;
ALTER TABLE proofs ENABLE ROW LEVEL SECURITY;

-- 8. Create policies for public access (adjust as needed)
CREATE POLICY "Allow public read access" ON bookmarks
  FOR SELECT USING (true);

CREATE POLICY "Allow public insert" ON bookmarks
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow public read access" ON hunches
  FOR SELECT USING (true);

CREATE POLICY "Allow public insert" ON hunches
  FOR INSERT WITH CHECK (true);
```

**Click:** "Run" to execute all statements

**Verify:** Check Table Editor to see all 3 tables created

---

## ✅ Step 5: Verify Setup

### Test Connection (Replit & CLI/Cursor)

#### Replit

```bash
# In Replit Shell
python -c "
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
    print(f'✅ Tables accessible: {len(result.data)} rows found')
else:
    print('❌ Environment variables not set')
"
```

#### CLI/Cursor

```bash
# In Cursor/CLI terminal (with venv activated)
source venv/bin/activate
python -c "
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
    print(f'✅ Tables accessible: {len(result.data)} rows found')
else:
    print('❌ Environment variables not set')
"
```

---

## 🧪 Step 6: Test Ingestion

### Create Test Data

**Create `test_data.json`:**
```json
[
  {
    "url": "https://example.com/gematria",
    "summary": "Article about gematria and numerology in ancient texts"
  },
  {
    "url": "https://example.com/sacred-geometry",
    "summary": "Exploring sacred geometry and its mathematical foundations"
  }
]
```

### Run Ingestion Test

#### Replit

```bash
# In Replit Shell
python ingest_pass1.py test_data.json
```

#### CLI/Cursor

```bash
# In Cursor/CLI terminal (with venv activated)
source venv/bin/activate
python ingest_pass1.py test_data.json
```

**Expected Output:**
```
============================================================
Gematria Hive - Ingestion Pass #1
============================================================
2025-11-06 08:00:00 - INFO - Starting ingestion pass #1 from source: test_data.json
2025-11-06 08:00:01 - INFO - Loaded 2 items from JSON file: test_data.json
2025-11-06 08:00:02 - INFO - Processing chunk 1 (2 items)
2025-11-06 08:00:03 - INFO - Item https://example.com/gematria: Relevance 0.750, phase phase1_basic, tags ['gematria', 'numerology']
...
============================================================
Ingestion Results:
============================================================
Source: test_data.json
Items Processed: 2
Items Ingested: 2
Success: True
============================================================

✅ Ingestion complete! Check ingestion_log.txt for details.
📊 Data exported to claude_export.json for Claude skills.
```

### Verify in Supabase

1. **Go to:** Supabase Dashboard → Table Editor
2. **Select:** `bookmarks` table
3. **Verify:** You should see 2 rows with:
   - URLs from test data
   - Summaries
   - Embeddings (vector data)
   - Tags (e.g., ['gematria', 'numerology'])
   - Phase (phase1_basic)
   - Relevance scores

---

## 🔄 Step 7: Sync Environment Variables

### Replit → CLI/Cursor

**In Replit:**
- Copy your Supabase credentials from `.replit` or Secrets

**In CLI/Cursor:**
- Add to `.env` file (see Step 2)

### CLI/Cursor → Replit

**In CLI/Cursor:**
- Copy from `.env` file

**In Replit:**
- Add to `.replit` file or Secrets

**Important:** Never commit `.env` file or real credentials to git!

---

## 📝 Step 8: Database Schema Reference

### Bookmarks Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key (auto-generated) |
| `url` | TEXT | Source URL |
| `summary` | TEXT | Content summary |
| `embedding` | vector(384) | Sentence transformer embedding |
| `tags` | TEXT[] | Array of relevant tags |
| `phase` | TEXT | Processing phase (phase1_basic, phase2_deep) |
| `relevance_score` | FLOAT | Similarity score (0.0-1.0) |
| `timestamp` | TIMESTAMPTZ | When item was ingested |
| `created_at` | TIMESTAMPTZ | Record creation time |
| `updated_at` | TIMESTAMPTZ | Last update time |

### Hunches Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `content` | TEXT | Hunch/insight content |
| `timestamp` | TIMESTAMPTZ | When hunch was logged |
| `status` | TEXT | Status (pending, completed, etc.) |
| `cost` | FLOAT | Associated cost (for tracking) |
| `links` | TEXT[] | Related links/IDs |
| `created_at` | TIMESTAMPTZ | Record creation time |

### Proofs Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `theorem` | TEXT | Theorem statement |
| `report` | TEXT | Proof report |
| `accuracy_metric` | FLOAT | Accuracy score |
| `efficiency_score` | FLOAT | Efficiency score |
| `timestamp` | TIMESTAMPTZ | When proof was generated |
| `created_at` | TIMESTAMPTZ | Record creation time |

---

## 🛠️ Troubleshooting

### Issue: "Extension vector does not exist"

**Solution:**
```sql
-- Run in Supabase SQL Editor
CREATE EXTENSION IF NOT EXISTS vector;
```

### Issue: "Table does not exist"

**Solution:**
- Run the complete SQL script from Step 4
- Check Table Editor to verify tables exist

### Issue: "Permission denied" or RLS errors

**Solution:**
```sql
-- Disable RLS temporarily for testing (not recommended for production)
ALTER TABLE bookmarks DISABLE ROW LEVEL SECURITY;
ALTER TABLE hunches DISABLE ROW LEVEL SECURITY;
```

### Issue: "Invalid API key"

**Solution:**
- Verify you're using the **anon public** key (not service_role)
- Check environment variables are set correctly
- Restart Replit/Cursor after setting env vars

### Issue: "Connection timeout"

**Solution:**
- Check Supabase project is active (not paused)
- Verify network connectivity
- Check firewall settings

---

## ✅ Verification Checklist

### Database Setup
- [ ] Supabase project created
- [ ] pgvector extension enabled
- [ ] All 3 tables created (bookmarks, hunches, proofs)
- [ ] Indexes created
- [ ] Dynamic view created

### Environment Variables
- [ ] `SUPABASE_URL` set in Replit
- [ ] `SUPABASE_KEY` set in Replit
- [ ] `SUPABASE_URL` set in CLI/Cursor `.env`
- [ ] `SUPABASE_KEY` set in CLI/Cursor `.env`

### Connection Test
- [ ] Connection test successful in Replit
- [ ] Connection test successful in CLI/Cursor
- [ ] Can query tables from both platforms

### Ingestion Test
- [ ] Test data created
- [ ] Ingestion script runs successfully
- [ ] Data appears in Supabase Table Editor
- [ ] Embeddings generated correctly
- [ ] Tags assigned correctly

---

## 🚀 Next Steps

After Supabase setup is complete:

1. ✅ **Ready for Ingestion Pass #1**
   - Run `python ingest_pass1.py` with real data
   - Process Dewey exports, photos, URLs

2. ✅ **Ready for Phase 2**
   - Deeper processing for phase2_deep items
   - Proof generation
   - Unification analysis

3. ✅ **Ready for Agent Workflows**
   - MCP integration
   - Self-scaffolding agents
   - Automated insights

---

## 📚 Related Documentation

- **INGESTION_GUIDE.md** - Complete ingestion guide
- **CURSOR_SYNC_INSTRUCTIONS.md** - Sync setup
- **SYNC_WORKFLOW.md** - Workflow guide
- **README.md** - Project overview
- **PRD.md** - Product requirements

---

**Database setup complete! Ready for ingestion!** 🐝✨

