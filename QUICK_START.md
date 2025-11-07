# Gematria Hive - Quick Start

**Get up and running in 5 minutes**

---

## 🚀 Prerequisites

- Python 3.12+
- Supabase account (free tier works)
- Git

---

## ⚡ Quick Setup

### 1. Clone and Install (2 min)

```bash
# Clone repo (if not already)
git clone <repo-url>
cd gematria-hive

# Create virtual environment
python -m venv gematria_env
source gematria_env/bin/activate  # On Windows: gematria_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Database (2 min)

```bash
# Create .env file
cat > .env << EOF
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
EOF

# Get credentials from:
# 1. Go to https://supabase.com
# 2. Create project: gematria-hive
# 3. Settings → API → Copy URL and anon key
```

### 3. Setup Database (1 min)

```bash
# Verify connection
python setup_database.py --verify-only

# If tables don't exist, run migrations in Supabase SQL Editor:
# - migrations/create_gematria_tables.sql
# - migrations/create_complete_schema.sql
```

### 4. Run Application (30 sec)

```bash
# Option 1: Streamlit Dashboard
streamlit run app.py

# Option 2: Run Agents
python run_agents.py

# Option 3: Critical Path
python execute_critical_path.py
```

---

## 🎯 What Each Command Does

### `streamlit run app.py`
- Launches web dashboard
- View data, run analyses
- Interactive UI

### `python run_agents.py`
- Runs agent orchestrator
- Processes data through agents
- Generates insights

### `python execute_critical_path.py`
- Full pipeline execution
- Data → Agents → Patterns → Proofs → Unifications
- Maximum concurrency

---

## ✅ Verification

```bash
# Test database connection
python setup_database.py --verify-only

# Test imports
python -c "from agents import MCPOrchestrator; print('✅ Agents OK')"

# Test Streamlit
streamlit --version
```

---

## 🐛 Troubleshooting

### "SUPABASE_URL not set"
- Create `.env` file with credentials
- Or set environment variables directly

### "Table does not exist"
- Run migrations in Supabase SQL Editor
- Check `migrations/` folder

### "Module not found"
- Activate virtual environment
- Run `pip install -r requirements.txt`

---

## 📚 Next Steps

1. **Ingest Data:** Use `execute_ingestions.py` or `scripts/ingest.py`
2. **Run Agents:** Use `run_agents.py` for agent workflows
3. **View Dashboard:** Use `streamlit run app.py` for UI
4. **Read Docs:** Check `docs/` folder (after consolidation)

---

**Ready to go!** 🐝✨
