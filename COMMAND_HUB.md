# Gematria Hive - Command Hub & Documentation

**Single Source of Truth for Commands, Documentation, and System Access**

**Last Updated:** January 6, 2025

---

## 🚀 Quick Start Commands

### Start Kanban Board (Standalone HTML)
```bash
# Start the API server
python run_kanban.py
# Or: python kanban_api.py

# Open in browser
# http://localhost:8000
```

### Start Internal API (Agent Communication)
```bash
# Set API key (optional, defaults to "internal-api-key-change-in-production")
export INTERNAL_API_KEY="your-secure-api-key"

# Start internal API
python run_internal_api.py

# Test internal API
python test_internal_api.py

# Internal API runs on http://localhost:8001
```

### Start Streamlit Dashboard
```bash
streamlit run app.py
```

### Run Agents
```bash
# Run all agents with default tasks
python run_agents.py

# Run specific task type
python run_agents.py --task-type inference --query "gematria patterns"

# Run browser task
python run_agents.py --task-type browser --url "https://example.com"
```

### Run Tests
```bash
# Run all tests
python run_tests.py

# Run integration tests
python integration_test.py

# Run E2E tests
python test_e2e.py
```

### Execute Critical Path
```bash
python execute_critical_path.py
```

---

## 📋 System Entry Points

### 1. Kanban Board (Recommended)
**File:** `kanban.html` + `kanban_api.py`  
**Command:** `python kanban_api.py`  
**URL:** http://localhost:8000  
**Features:**
- Standalone HTML/JS interface
- Drag-and-drop task management
- Real-time updates
- Full CRUD operations
- Cost tracking
- Statistics dashboard

### 2. Streamlit Dashboard
**File:** `app.py`  
**Command:** `streamlit run app.py`  
**Features:**
- Comprehensive dashboard
- All data visible simultaneously
- Interactive visualizations
- Real-time updates

### 3. Agent Runner
**File:** `run_agents.py`  
**Command:** `python run_agents.py [options]`  
**Features:**
- Automatic database verification
- Orchestrator initialization
- Task execution
- Results logging

### 4. Critical Path Execution
**File:** `execute_critical_path.py`  
**Command:** `python execute_critical_path.py`  
**Features:**
- Full pipeline execution
- Maximum concurrency
- Data → Agents → Patterns → Proofs → Unifications

---

## 🔧 Setup Commands

### Database Setup
```bash
# Verify database connection
python setup_database.py --verify-only

# Run migrations
python setup_database.py

# Test connection
python -c "from setup_database import test_connection; test_connection()"
```

### Environment Setup
```bash
# Activate conda environment
conda activate gematria_env

# Install dependencies
pip install -r requirements.txt

# Load environment variables
# Create .env file with:
# SUPABASE_URL=your_url
# SUPABASE_KEY=your_key
```

---

## 📚 Key Documentation

### Architecture & Vision
- **PRD:** `docs/architecture/PRD.md` - Product requirements
- **Master Architecture:** `docs/architecture/MASTER_ARCHITECTURE.md` - Complete architecture
- **Critical Path:** `docs/architecture/CRITICAL_PATH.md` - Execution plan
- **Master Review:** `MASTER_REVIEW_AND_CONSOLIDATION.md` - Comprehensive review

### Status & Roadmap
- **System Status:** `docs/STATUS.md` - Current system status
- **Next Phase Roadmap:** `NEXT_PHASE_ROADMAP.md` - Next phase priorities
- **Consolidation Complete:** `CONSOLIDATION_COMPLETE.md` - Consolidation summary

### Guides
- **Agent Usage:** `docs/guides/AGENT_USAGE.md` - How to use agents
- **Ingestion Guide:** `docs/guides/INGESTION_GUIDE.md` - Data ingestion
- **Quick Start:** `QUICK_START.md` - Quick start guide

---

## 🎯 Common Tasks

### Create a Task
```bash
# Via API
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"content": "Investigate 369 connections", "status": "pending"}'

# Via Python
python -c "from task_manager import create_task; create_task('Investigate 369 connections')"
```

### Run Specific Agent
```bash
# Via orchestrator
python -c "
from agents.orchestrator import get_orchestrator
orchestrator = get_orchestrator()
result = orchestrator.execute({'type': 'inference', 'query': 'gematria patterns'})
print(result)
"
```

### Check System Status
```bash
# Database status
python setup_database.py --verify-only

# Agent status
python run_agents.py --skip-verify --task-type inference --query "test"

# Cost status
python -c "from agents.cost_manager import CostManagerAgent; cm = CostManagerAgent(); print(cm.get_cost_summary())"
```

---

## 🔗 API Endpoints

### Kanban API (http://localhost:8000)

#### Tasks
- `GET /api/tasks` - Get all tasks
- `GET /api/tasks?status=pending` - Get tasks by status
- `GET /api/tasks/{task_id}` - Get single task
- `POST /api/tasks` - Create task
- `PUT /api/tasks/{task_id}` - Update task
- `PATCH /api/tasks/{task_id}/status?status=completed` - Update status
- `DELETE /api/tasks/{task_id}` - Delete task

#### Statistics
- `GET /api/statistics` - Get task statistics

#### Health
- `GET /health` - Health check

### Internal API (http://localhost:8001)

**Note:** Internal API requires authentication via `Authorization: Bearer {INTERNAL_API_KEY}` header.

#### Health Check (No Auth Required)
- `GET /internal/health` - System health check
- `GET /internal/health/agents` - Agent health check

#### Agent Communication (Requires Auth)
- `GET /internal/agents` - List all agents
- `GET /internal/agents/{name}` - Get agent details
- `POST /internal/agents/{name}/execute` - Execute agent

#### Orchestrator (Requires Auth)
- `POST /internal/orchestrator/execute` - Execute workflow

#### Tool Registry (Requires Auth)
- `GET /internal/tools` - List all tools
- `GET /internal/tools/{name}` - Get tool details
- `POST /internal/tools/{name}/execute` - Execute tool

#### Cost Management (Requires Auth)
- `GET /internal/cost/current` - Get current cost

**Example Usage:**
```bash
# Health check (no auth)
curl http://localhost:8001/internal/health

# List agents (requires auth)
curl -H "Authorization: Bearer your-api-key" \
  http://localhost:8001/internal/agents

# Execute agent (requires auth)
curl -X POST \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"state": {"task": {}, "data": [], "context": {}}}' \
  http://localhost:8001/internal/agents/extraction/execute
```

---

## 📊 System Components

### Core Modules
- `core/gematria_engine.py` - Gematria calculations
- `core/conductor.py` - Database access
- `core/visualization_engine.py` - Visualizations
- `core/data_table.py` - Unified CRUD

### Agents (36+)
- `agents/orchestrator.py` - MCP orchestrator
- `agents/extraction.py` - Data extraction
- `agents/distillation.py` - Data processing
- `agents/ingestion.py` - Data ingestion
- `agents/inference.py` - Insights generation
- `agents/proof.py` - Proof generation
- `agents/cost_manager.py` - Cost tracking
- ... and 29+ more agents

### Utilities
- `utils/cache_manager.py` - Caching
- `utils/baseline_manager.py` - Baseline tracking
- `utils/floating_index.py` - Quick lookups

### Task Management
- `task_manager.py` - Task CRUD operations
- `kanban_api.py` - Kanban API server
- `kanban.html` - Standalone kanban UI

---

## 🧪 Testing Commands

### Unit Tests
```bash
# Run all unit tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_agents.py

# Run with coverage
python -m pytest tests/ --cov=agents --cov=core
```

### Integration Tests
```bash
# Run integration tests
python integration_test.py

# Run E2E tests
python test_e2e.py
```

---

## 🚀 Deployment Commands

### Development
```bash
# Start kanban API
python kanban_api.py

# Start Streamlit
streamlit run app.py

# Run agents
python run_agents.py
```

### Production (Future)
```bash
# Run with gunicorn
gunicorn kanban_api:app -w 4 -k uvicorn.workers.UvicornWorker

# Run with systemd (future)
sudo systemctl start gematria-hive
```

---

## 📝 Environment Variables

### Required
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

### Optional
```bash
# Email alerts
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password
COST_ALERT_EMAIL=alerts@example.com

# API keys
ANTHROPIC_API_KEY=your-claude-key
PERPLEXITY_API_KEY=your-perplexity-key
GROK_API_KEY=your-grok-key
```

---

## 🎯 Quick Reference

### Most Common Commands
```bash
# Start kanban board
python kanban_api.py

# Run agents
python run_agents.py

# Check status
python setup_database.py --verify-only

# Run tests
python run_tests.py
```

### Key Files
- `kanban.html` - Kanban UI
- `kanban_api.py` - Kanban API
- `run_agents.py` - Agent runner
- `app.py` - Streamlit dashboard
- `task_manager.py` - Task management

### Key Documentation
- `COMMAND_HUB.md` - This file (single source of truth)
- `MASTER_REVIEW_AND_CONSOLIDATION.md` - Master review
- `NEXT_PHASE_ROADMAP.md` - Next phase roadmap
- `docs/STATUS.md` - System status

---

## 🔄 Workflow Examples

### Daily Workflow
```bash
# 1. Start kanban board
python kanban_api.py

# 2. Create tasks in kanban UI
# http://localhost:8000

# 3. Run agents on tasks
python run_agents.py --task-type inference --query "your query"

# 4. Check results in kanban board
```

### Development Workflow
```bash
# 1. Make changes
# 2. Run tests
python run_tests.py

# 3. Test locally
python kanban_api.py

# 4. Commit changes
git add .
git commit -m "Description"
```

---

## 📞 Support & Resources

### Documentation
- All docs in `docs/` directory
- Architecture in `docs/architecture/`
- Guides in `docs/guides/`
- Status in `docs/status/`

### Key Contacts
- Issues: GitHub issues
- Documentation: See `docs/` directory
- Commands: This file

---

**This is your single source of truth for all commands and documentation!** 🐝✨

