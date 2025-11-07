# Complete Setup Guide - Gematria Hive

**Purpose:** Complete setup guide for all platforms with database, agents, and dependencies

**Last Updated:** November 7, 2025

---

## 🚀 Quick Start (All Platforms)

### 1. Install Dependencies

**CLI/Cursor:**
```bash
conda activate gematria_env
pip install -r requirements.txt
```

**Replit:**
```bash
./setup_replit.sh
# OR manually:
pip install -r requirements.txt
```

### 2. Set Up Database

**Create Supabase Project:**
1. Go to https://supabase.com
2. Create new project: `gematria-hive`
3. Save database password securely

**Get API Keys:**
1. Settings → API
2. Copy Project URL → `SUPABASE_URL`
3. Copy anon public key → `SUPABASE_KEY`

**Set Environment Variables:**

**CLI/Cursor:**
```bash
# Create .env file
cat > .env << EOF
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
EOF
```

**Replit:**
1. Click lock icon in sidebar
2. Add `SUPABASE_URL` and `SUPABASE_KEY` as secrets

### 3. Run Database Migrations

**In Supabase Dashboard SQL Editor:**
1. Run `migrations/create_gematria_tables.sql`
2. Run `migrations/create_complete_schema.sql`
3. Verify tables created in Table Editor

**Or use setup script:**
```bash
python setup_database.py
# Then run SQL in Supabase Dashboard as instructed
```

### 4. Test Setup

**CLI/Cursor:**
```bash
conda activate gematria_env
python -c "from agents import MCPOrchestrator; print('✅ Setup complete')"
```

**Replit:**
```bash
python -c "from agents import MCPOrchestrator; print('✅ Setup complete')"
```

### 5. Run Application

**CLI/Cursor:**
```bash
streamlit run app.py
```

**Replit:**
- Click Run button (uses .replit config)
- OR: `streamlit run app.py --server.port 5000`

---

## 📦 Dependencies

### Core Dependencies
- ✅ streamlit - Web UI
- ✅ pandas - Data manipulation
- ✅ numpy - Numerical computing
- ✅ python-dotenv - Environment variables

### Database
- ✅ supabase - Database client
- ✅ pgvector - Vector embeddings (enabled in Supabase)

### ML/AI
- ✅ sentence-transformers - Embeddings
- ✅ transformers - Hugging Face models
- ✅ langchain - Agent framework
- ✅ langgraph - State machine (optional)

### Data Pipelines
- ✅ pixeltable - Multimodal workflows
- ✅ stringzilla - Fast string operations
- ✅ simsimd - Fast vector operations

### Web Scraping
- ✅ requests - HTTP requests
- ✅ beautifulsoup4 - HTML parsing
- ✅ tqdm - Progress bars

### Image/OCR
- ✅ opencv-python - Image processing
- ✅ pytesseract - OCR
- ✅ pillow - Image handling

### Visualization
- ✅ plotly - Interactive charts
- ✅ matplotlib - Static charts

### Quantum (Future)
- ✅ qiskit - Quantum simulations

---

## 🗄️ Database Setup

### Step 1: Create Supabase Project
1. Go to https://supabase.com
2. Sign in or create account
3. Click "New Project"
4. Fill in:
   - Project Name: `gematria-hive`
   - Database Password: (save securely)
   - Region: Choose closest
5. Wait 2-3 minutes for initialization

### Step 2: Get API Keys
1. Go to Settings → API
2. Copy:
   - Project URL → `SUPABASE_URL`
   - anon public key → `SUPABASE_KEY`

### Step 3: Enable pgvector Extension
1. Go to SQL Editor
2. Run:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```
3. Verify: "Success. No rows returned"

### Step 4: Run Migrations
1. Go to SQL Editor
2. Run `migrations/create_gematria_tables.sql`
3. Run `migrations/create_complete_schema.sql`
4. Verify in Table Editor

### Step 5: Test Connection
```bash
python setup_database.py
```

---

## 🤖 Agent Framework Setup

### MCP Orchestrator
All agents are orchestrated by `MCPOrchestrator`:

```python
from agents import MCPOrchestrator

orchestrator = MCPOrchestrator()
result = orchestrator.execute({
    "type": "ingestion",
    "source": "data.json"
})
```

### Parallel Execution
All analysis agents run in parallel:
- Extraction (runs first)
- Distillation, Ingestion, Author Indexer, Symbol Extractor, etc. (run simultaneously)

### Agent Documentation
See `MCP_AGENT_TRACKER.md` for complete agent list and documentation.

---

## 🔧 Platform-Specific Setup

### CLI (Mac Terminal)
```bash
# Activate conda environment
conda activate gematria_env

# Install dependencies
pip install -r requirements.txt

# Set environment variables
echo "SUPABASE_URL=..." > .env
echo "SUPABASE_KEY=..." >> .env

# Test
python -c "from agents import MCPOrchestrator; print('✅ Ready')"
```

### Cursor IDE
1. Set Python interpreter: `Cmd+Shift+P` → "Python: Select Interpreter"
2. Choose: `/Users/cooperladd/anaconda3/envs/gematria_env/bin/python`
3. Terminal auto-activates conda environment
4. Follow CLI setup steps

### Replit
1. Pull latest: `git pull origin feat-agent-framework-9391b --rebase`
2. Run setup: `./setup_replit.sh`
3. Set secrets: Lock icon → Add `SUPABASE_URL` and `SUPABASE_KEY`
4. Click Run button (uses .replit config)

---

## ✅ Verification Checklist

### Dependencies
- [ ] Python 3.12+ installed
- [ ] All packages from requirements.txt installed
- [ ] pixeltable installed
- [ ] langchain installed
- [ ] langgraph installed (optional)

### Database
- [ ] Supabase project created
- [ ] API keys obtained
- [ ] Environment variables set
- [ ] pgvector extension enabled
- [ ] Migrations run
- [ ] Tables created and verified

### Agents
- [ ] All agents importable
- [ ] MCPOrchestrator works
- [ ] Parallel execution working
- [ ] Cost tracking active

### Application
- [ ] Streamlit runs without errors
- [ ] App accessible in browser
- [ ] Database connection works
- [ ] Ingestion script works

---

## 🐛 Troubleshooting

### Issue: "pixeltable not installed"
**Solution:**
```bash
pip install pixeltable
```

### Issue: "langchain not installed"
**Solution:**
```bash
pip install langchain langgraph
```

### Issue: "Supabase connection failed"
**Solution:**
1. Check environment variables are set
2. Verify API keys are correct
3. Check Supabase project is active
4. Test connection: `python setup_database.py`

### Issue: "Import errors"
**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: "Database tables not found"
**Solution:**
1. Run migrations in Supabase Dashboard SQL Editor
2. Verify tables in Table Editor
3. Check RLS policies if needed

---

## 📚 Documentation

### Setup Guides
- `COMPLETE_SETUP_GUIDE.md` - This file
- `REPLIT_SETUP_COMPLETE.md` - Replit-specific setup
- `SUPABASE_SETUP.md` - Database setup details
- `QUICK_START.md` - 5-minute quick start

### Agent Documentation
- `MCP_AGENT_TRACKER.md` - Complete agent list and tracking
- `AGENT_USAGE.md` - Agent usage guide
- `AGENT_SETUP.md` - Agent framework setup

### Architecture
- `MASTER_ARCHITECTURE.md` - Complete system architecture
- `PRD.md` - Product requirements
- `IMPLEMENTATION_ROADMAP.md` - Implementation plan

---

## 🎯 Next Steps After Setup

1. **Test Ingestion**
   ```bash
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

4. **Verify Database**
   - Go to Supabase Dashboard → Table Editor
   - Check bookmarks table has data

---

## 🔗 Quick Reference

### Essential Commands
```bash
# Setup
./setup_replit.sh  # Replit only
python setup_database.py  # Database setup

# Test
python -c "from agents import MCPOrchestrator; print('✅ Ready')"

# Run
streamlit run app.py

# Ingestion
python ingest_pass1.py data.json
```

### File Locations
- **Config:** `.replit` (Replit), `.env` (CLI/Cursor)
- **Migrations:** `migrations/`
- **Agents:** `agents/`
- **Core:** `core/`
- **Utils:** `utils/`

---

**Setup Complete! Ready to use Gematria Hive!** 🐝✨

