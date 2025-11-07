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

**Current Status:** ✅ **Operational**

- ✅ **Codebase:** Complete with 36+ agents
- ✅ **Database Schema:** 22 tables defined
- ✅ **Kanban Board:** Enhanced with phases, roles, tags, metadata
- ✅ **Internal API:** Agent communication layer ready
- ✅ **React Webapp:** Modern frontend with all enhanced features
- ✅ **Documentation:** Consolidated in `COMMAND_HUB.md`

**See [COMMAND_HUB.md](COMMAND_HUB.md) for complete system documentation.**

---

## 🎯 Main Entry Points

### 1. Kanban Board (Recommended)
```bash
# Start kanban board (HTML + API)
python run_kanban.py
# Open http://localhost:8000
```

**Features:**
- Standalone HTML/JS interface
- Enhanced task management (phases, roles, tags, metadata)
- Drag-and-drop functionality
- Real-time statistics
- Full CRUD operations

**See [COMMAND_HUB.md](COMMAND_HUB.md) for all commands.**

### 2. Modern Webapp Frontend (React/TypeScript)
```bash
# Start backend API
python run_kanban.py

# In another terminal, start frontend
cd webapp
npm install
npm run dev
```
Modern React/TypeScript frontend with shadcn/ui and TanStack Query. Available at `http://localhost:3000`.

**See [webapp/README.md](webapp/README.md) and [webapp/SETUP.md](webapp/SETUP.md) for details.**

### 3. Internal API (Agent Communication)
```bash
# Start internal API for agent-to-agent communication
python run_internal_api.py
# Runs on http://localhost:8001
```

**See [INTERNAL_API_DESIGN.md](INTERNAL_API_DESIGN.md) for details.**

### 4. Streamlit Dashboard
```bash
streamlit run app.py
```
Interactive web dashboard for viewing data and running analyses.

### 5. Agent Orchestrator
```bash
python run_agents.py
```
Runs the agent framework to process data through all agents.

### 6. Critical Path Execution
```bash
python execute_critical_path.py
```
Full pipeline: Data → Agents → Patterns → Proofs → Unifications.

---

## 📁 Project Structure

```
gematria-hive/
├── webapp/                   # Modern React/TypeScript frontend
│   ├── src/                 # Source code
│   │   ├── components/     # React components (shadcn/ui + custom)
│   │   ├── lib/            # API client, queries, utilities
│   │   └── hooks/          # Custom React hooks
│   ├── package.json        # Node.js dependencies
│   └── vite.config.ts      # Vite configuration
├── app.py                    # Streamlit dashboard
├── kanban_api.py            # FastAPI backend for webapp
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
└── requirements.txt         # Python dependencies
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
- **Modern Webapp Frontend** - React/TypeScript with shadcn/ui and TanStack
- **Streamlit Dashboard** - Legacy interactive web UI
- **Critical Path Execution** - Full pipeline with maximum concurrency

---

## 🛠️ Tech Stack

### Backend
- **Python 3.12+** - Core language
- **FastAPI** - REST API for webapp
- **Supabase** - PostgreSQL + pgvector
- **Streamlit** - Legacy web dashboard
- **LangChain/LangGraph** - Agent orchestration
- **Sentence-Transformers** - Embeddings

### Frontend (Webapp)
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **shadcn/ui** - Accessible component system (Radix UI + Tailwind CSS)
- **TanStack Query** - Server state management
- **TanStack Table** - Data tables (available)
- **TanStack Router** - Type-safe routing (available)
- **TanStack Form** - Form management (available)

---

## 📖 More Information

- **Product Requirements:** See `docs/architecture/PRD.md`
- **Master Architecture:** See `docs/architecture/MASTER_ARCHITECTURE.md`
- **Agent Usage:** See `docs/guides/AGENT_USAGE.md`

---

**Ready to explore the hive!** 🐝✨

