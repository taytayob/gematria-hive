# Gematria Hive 🐝

**Self-scaffolding AI ecosystem for gematria unification**

A comprehensive system that unifies gematria, numerology, sacred geometry, and esoteric knowledge with rigorous mathematics, physics, and AI/ML.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
# Create .env file with SUPABASE_URL and SUPABASE_KEY

# 3. Check status
python run_all.py --status

# 4. Run application
python run_all.py --run streamlit  # Web dashboard
python run_all.py --run agents     # Agent orchestrator
python run_all.py --run critical   # Critical path execution
```

**See [QUICK_START.md](QUICK_START.md) for detailed setup instructions.**

---

## 📊 System Status

**Current Status:** 🟡 Partially Operational

- ✅ **Codebase:** Complete with 36+ agents
- ✅ **Database Schema:** 22 tables defined
- ⚠️ **Environment:** Needs SUPABASE_URL and SUPABASE_KEY
- ✅ **Documentation:** Organized in `docs/` folder

**See [STATUS.md](STATUS.md) for full system status.**

---

## 🎯 Main Entry Points

### 1. Streamlit Dashboard
```bash
streamlit run app.py
```
Interactive web dashboard for viewing data and running analyses.

### 2. Agent Orchestrator
```bash
python run_agents.py
```
Runs the agent framework to process data through all agents.

### 3. Critical Path Execution
```bash
python execute_critical_path.py
```
Full pipeline: Data → Agents → Patterns → Proofs → Unifications.

### 4. Master Run Script
```bash
python run_all.py --status    # Show system status
python run_all.py --setup     # Setup database
python run_all.py --run <component>  # Run specific component
```

---

## 📁 Project Structure

```
gematria-hive/
├── app.py                    # Streamlit dashboard
├── run_all.py               # Master run script
├── run_agents.py            # Agent orchestrator
├── execute_critical_path.py  # Critical path execution
├── agents/                   # 36+ agent modules
├── core/                     # Core engines
├── scripts/                  # CLI scripts
├── docs/                     # Organized documentation
│   ├── setup/               # Setup guides
│   ├── status/              # Status reports
│   ├── guides/              # Usage guides
│   └── architecture/        # Architecture docs
├── migrations/              # Database migrations
└── requirements.txt         # Dependencies
```

---

## 📚 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Get started in 5 minutes
- **[STATUS.md](STATUS.md)** - Current system status
- **[docs/](docs/)** - Organized documentation
  - `docs/setup/` - Setup guides
  - `docs/guides/` - Usage guides
  - `docs/architecture/` - Architecture docs
  - `docs/status/` - Status reports

---

## 🔧 Configuration

### Environment Variables

Create `.env` file:
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

### Database Setup

1. Create Supabase project at https://supabase.com
2. Run migrations from `migrations/` folder
3. Set environment variables
4. Verify: `python setup_database.py --verify-only`

---

## 🎯 Features

- **36+ Modular Agents** - Extraction, distillation, ingestion, inference, proofs
- **MCP Orchestrator** - Coordinate agents with LangGraph
- **Database Integration** - Supabase with pgvector for embeddings
- **Streamlit Dashboard** - Interactive web UI
- **Critical Path Execution** - Full pipeline with maximum concurrency

---

## 🛠️ Tech Stack

- **Python 3.12+** - Core language
- **Supabase** - PostgreSQL + pgvector
- **Streamlit** - Web dashboard
- **LangChain/LangGraph** - Agent orchestration
- **Sentence-Transformers** - Embeddings

---

## 📖 More Information

- **Product Requirements:** See `docs/architecture/PRD.md`
- **Master Architecture:** See `docs/architecture/MASTER_ARCHITECTURE.md`
- **Agent Usage:** See `docs/guides/AGENT_USAGE.md`

---

**Ready to explore the hive!** 🐝✨

