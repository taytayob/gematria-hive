# Ingestion Pass #1 - Complete Guide

**Purpose:** Foundation for ingestion - Pulling data, understanding category/relevance, logging all steps, segmenting scope into phases.

**Last Updated:** November 6, 2025

---

## 📋 Overview

This script (`ingest_pass1.py`) provides the foundation for data ingestion:

- **Pulling data** from JSON exports (Dewey), manual files, photos (OCR), or URLs
- **Understanding category/relevance** via AI tagging using sentence-transformers similarity to vision keywords
- **Logging all steps** to hunches table and console/file
- **Segmenting scope into phases** (phase1: basic embed/ingest; phase2: deeper processing like proofs/unifications)
- **Optimized for efficiency** (chunking for large data, StringZilla for fast text ops)
- **Future-proofed** (modular functions for adding agents/MCP, master/dynamic DB copies)

---

## 🚀 Setup (Replit & CLI/Cursor)

### Replit

**Step 1: Set Environment Variables**

Edit `.replit` file or use Replit Secrets:

```bash
# In Replit Shell
# Or use Replit Secrets UI (lock icon in sidebar)
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_anon_key_here
```

**Step 2: Install Dependencies**

```bash
# In Replit Shell
pip install -r requirements.txt
```

**Step 3: Verify Installation**

```bash
# In Replit Shell
python -c "import supabase, sentence_transformers; print('✅ Core dependencies installed')"
```

### CLI/Cursor

**Step 1: Set Environment Variables**

Create `.env` file:

```bash
# In Cursor/CLI terminal
cd /Users/cooperladd/Desktop/gematria-hive/gematria-hive
cp .env.example .env
# Edit .env and add your Supabase credentials
nano .env  # or use Cursor to edit
```

**Step 2: Activate Venv and Install Dependencies**

```bash
# In Cursor/CLI terminal
source venv/bin/activate
pip install -r requirements.txt
```

**Step 3: Verify Installation**

```bash
# In Cursor/CLI terminal (with venv activated)
python -c "import supabase, sentence_transformers; print('✅ Core dependencies installed')"
```

---

## 📝 Environment Variables

### Required Variables

| Variable | Description | Where to Get |
|----------|-------------|--------------|
| `SUPABASE_URL` | Your Supabase project URL | Supabase Dashboard → Settings → API |
| `SUPABASE_KEY` | Your Supabase anon/public key | Supabase Dashboard → Settings → API |

### Setting in Replit

**Option 1: Edit `.replit` file**
```toml
[env]
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key-here"
```

**Option 2: Use Replit Secrets**
1. Click lock icon in sidebar
2. Add `SUPABASE_URL` and `SUPABASE_KEY`
3. Access via `os.getenv()` in code

### Setting in CLI/Cursor

**Create `.env` file:**
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

**Important:** `.env` is in `.gitignore` - never commit secrets!

---

## 🗄️ Database Setup

### Supabase Tables Required

**1. Bookmarks Table**

```sql
CREATE TABLE bookmarks (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  url TEXT,
  summary TEXT,
  embedding vector(384),  -- pgvector extension required
  tags TEXT[],
  phase TEXT,
  relevance_score FLOAT,
  timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create index for vector similarity search
CREATE INDEX ON bookmarks USING ivfflat (embedding vector_cosine_ops);
```

**2. Hunches Table**

```sql
CREATE TABLE hunches (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  content TEXT,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  status TEXT,
  cost FLOAT DEFAULT 0.0,
  links TEXT[]
);
```

**3. Dynamic View (Optional)**

```sql
-- Dynamic copy (view for recent updates)
CREATE VIEW dynamic_bookmarks AS 
SELECT * FROM bookmarks 
WHERE timestamp > NOW() - INTERVAL '1 day';
```

---

## 🔧 Usage (Replit & CLI/Cursor)

### Replit

**Basic Usage:**
```bash
# In Replit Shell
python ingest_pass1.py
```

**With Custom Source:**
```bash
# In Replit Shell
python ingest_pass1.py dewey_json.json
```

**With Custom Chunk Size:**
```bash
# In Replit Shell
python ingest_pass1.py dewey_json.json 100
```

**Run from Run Button:**
- Update `.replit` file:
```toml
run = "python ingest_pass1.py"
```

### CLI/Cursor

**Basic Usage:**
```bash
# In Cursor/CLI terminal (with venv activated)
cd /Users/cooperladd/Desktop/gematria-hive/gematria-hive
source venv/bin/activate
python ingest_pass1.py
```

**With Custom Source:**
```bash
# In Cursor/CLI terminal (with venv activated)
python ingest_pass1.py dewey_json.json
```

**With Custom Chunk Size:**
```bash
# In Cursor/CLI terminal (with venv activated)
python ingest_pass1.py dewey_json.json 100
```

---

## 📊 Data Sources

### 1. JSON Files (Dewey Export)

**Format:**
```json
[
  {
    "url": "https://example.com/article",
    "summary": "Article about gematria and numerology...",
    "tags": []
  },
  ...
]
```

**Usage:**
```bash
python ingest_pass1.py dewey_json.json
```

### 2. Image Files (OCR)

**Supported Formats:** `.jpg`, `.png`, `.jpeg`, `.gif`

**Usage:**
```bash
python ingest_pass1.py photo.jpg
```

**Requirements:**
- `opencv-python`
- `pytesseract`
- `pillow`
- Tesseract OCR installed on system

### 3. URLs (Web Scraping)

**Usage:**
```bash
python ingest_pass1.py https://example.com/article
```

**Requirements:**
- `requests`
- `beautifulsoup4`

---

## 🎯 Vision Keywords

The script uses these keywords to categorize relevance:

- gematria, numerology, sacred geometry
- vibration, harmonics, quantum, duality
- 369, Pi, esoteric, consciousness
- DNA, frequencies, light, love
- synchronicity, ancient wisdom, occult
- mysticism, spirituality, mathematics, physics

**Customization:**
Edit `VISION_KEYWORDS` in `ingest_pass1.py` to add/remove keywords.

---

## 📈 Relevance Scoring

### How It Works

1. **Embedding:** Each item's summary is embedded using `all-MiniLM-L6-v2`
2. **Similarity:** Cosine similarity computed against vision keyword embeddings
3. **Scoring:** Maximum similarity score determines relevance
4. **Phase Assignment:**
   - `phase1_basic`: Score > 0.5 (basic processing)
   - `phase2_deep`: Score ≤ 0.5 (deeper processing needed)

### Threshold Adjustment

Edit the threshold in `categorize_relevance()` function:

```python
phase = 'phase1_basic' if max_score > 0.5 else 'phase2_deep'  # Adjust 0.5 as needed
```

---

## 📝 Logging

### Log Files

**Location:** `ingestion_log.txt` (in project root)

**Format:**
```
2025-11-06 08:00:00 - INFO - Pulled 100 items from dewey_json.json
2025-11-06 08:00:01 - INFO - Item https://example.com: Relevance 0.750, phase phase1_basic, tags ['gematria', 'numerology']
...
```

### Console Output

All logs also print to console for real-time monitoring.

### Database Logging

Hunches are logged to `hunches` table in Supabase for tracking and future analysis.

---

## 🔄 Chunking

### Why Chunking?

For large datasets, processing in chunks:
- Prevents memory issues
- Allows progress tracking
- Enables error recovery

### Default Chunk Size

**Default:** 50 items per chunk

**Customize:**
```bash
python ingest_pass1.py source.json 100  # Process 100 items per chunk
```

---

## 📤 Export for Claude Skills

After ingestion, data is exported to `claude_export.json` for use with Claude skills.

**Usage:**
1. Run ingestion: `python ingest_pass1.py`
2. Export created: `claude_export.json`
3. Upload to Claude for queries

**Claude Skill Prompt Template:**
```
System: Unify gematria/esoteric with math—log leaps, measure costs.

MCP: Triangulate data, segment phases, update master DB.

Task: From uploaded json, query 'best vector libs'—return summaries/tags/relevance; flag for phase2 if score <0.5.
```

---

## 🛠️ Troubleshooting (Replit & CLI/Cursor)

### Issue: "SUPABASE_URL and SUPABASE_KEY must be set"

**Replit:**
```bash
# Check .replit file has [env] section
# Or set in Replit Secrets
```

**CLI/Cursor:**
```bash
# Check .env file exists and has correct values
cat .env
# Or create from .env.example
cp .env.example .env
```

### Issue: "Module not found"

**Replit:**
```bash
# In Replit Shell
pip install -r requirements.txt
```

**CLI/Cursor:**
```bash
# In Cursor/CLI terminal (with venv activated)
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Error inserting to Supabase"

**Check:**
1. Supabase tables exist (see Database Setup)
2. pgvector extension enabled
3. API keys are correct
4. Network connectivity

**Debug:**
```python
# Add to script for debugging
print(f"Supabase URL: {SUPABASE_URL}")
print(f"Supabase Key: {SUPABASE_KEY[:10]}...")  # First 10 chars only
```

### Issue: OCR Not Working

**Requirements:**
- Tesseract OCR installed on system
- For Mac: `brew install tesseract`
- For Linux: `sudo apt-get install tesseract-ocr`
- For Windows: Download from GitHub

**Verify:**
```bash
tesseract --version
```

---

## 📊 Verification

### Check Ingestion Results

**In Supabase Dashboard:**
1. Go to Table Editor
2. Check `bookmarks` table
3. Verify items were inserted

**In Logs:**
```bash
# Check ingestion_log.txt
tail -f ingestion_log.txt
```

**In Python:**
```python
# Query Supabase
result = supabase.table('bookmarks').select('*').limit(10).execute()
print(result.data)
```

---

## 🚀 Next Steps

### Phase 1 Complete

After running `ingest_pass1.py`:
- ✅ Data pulled and processed
- ✅ Relevance scored
- ✅ Items tagged and phased
- ✅ Data in Supabase
- ✅ Export created for Claude

### Phase 2 (Future)

- Deeper processing for `phase2_deep` items
- Proof generation
- Unification analysis
- Agent workflows
- MCP integration

---

## 📚 Related Documentation

- **CURSOR_SYNC_INSTRUCTIONS.md** - Setup and sync guide
- **CURSOR_STREAMLIT_SETUP.md** - Streamlit setup
- **SYNC_WORKFLOW.md** - Complete workflow guide
- **README.md** - Project overview
- **PRD.md** - Product requirements

---

## ❓ Questions for Clarification

1. **Dewey exports:** Specific tags/filters needed? (e.g., only "repo" related)
2. **Photo count/format:** How many photos? Batch OCR limits?
3. **Supabase keys:** Ready to share, or need mock for testing?
4. **Kanban preference:** Trello (free) or Replit built-in?
5. **Relevance threshold:** 0.5 OK, or adjust for esoteric sensitivity?
6. **Test URLs:** Any specific X/Instagram bookmark examples?
7. **Mac CLI installs:** Any missing libraries to address?

---

**Ready for ingestion!** 🐝✨

