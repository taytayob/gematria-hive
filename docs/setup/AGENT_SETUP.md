# Agent Framework Setup & Usage

**Purpose:** Complete guide for setting up and using the Gematria Hive agent framework

**Last Updated:** November 6, 2025

---

## 🎯 Overview

The Gematria Hive agent framework is a self-scaffolding MCP-driven system that orchestrates multiple specialized agents to:
- Extract data from various sources
- Process and distill information
- Ingest into databases
- Generate insights and inferences
- Create mathematical proofs
- Generate media and games

---

## 🏗️ Architecture

### Agent Types

1. **Extraction Agent** - Extracts data (Dewey, OCR, URLs)
2. **Distillation Agent** - Processes and embeds data
3. **Ingestion Agent** - Stores data in database
4. **Inference Agent** - Generates insights and hunches
5. **Proof Agent** - Creates mathematical proofs
6. **Generative Agent** - Generates media/games

### MCP Orchestrator

The orchestrator manages:
- Agent workflow (LangGraph state machine)
- State management
- Task routing
- Cost tracking
- Memory persistence

---

## 🚀 Setup

### Prerequisites

```bash
# Activate conda environment
conda activate gematria_env

# Verify dependencies
python -c "import langchain, langgraph, supabase, sentence_transformers; print('✅ Dependencies ready')"
```

### Agent Structure

```
agents/
├── __init__.py          # Agent exports
├── orchestrator.py      # MCP orchestrator
├── extraction.py        # Extraction agent
├── distillation.py      # Distillation agent
├── ingestion.py         # Ingestion agent
├── inference.py         # Inference agent
├── proof.py             # Proof agent
└── generative.py        # Generative agent
```

---

## 📝 Usage

### Basic Workflow

```python
from agents import get_orchestrator

# Get orchestrator
orchestrator = get_orchestrator()

# Define task
task = {
    "type": "ingestion",
    "source": "test_data.json",
    "query": "gematria numerology"
}

# Execute workflow
result = orchestrator.execute(task)

# Check results
print(f"Status: {result['status']}")
print(f"Items processed: {len(result['data'])}")
print(f"Results: {result['results']}")
```

### Individual Agents

```python
from agents import ExtractionAgent, DistillationAgent, IngestionAgent

# Initialize agents
extraction = ExtractionAgent()
distillation = DistillationAgent()
ingestion = IngestionAgent()

# Create state
from agents.orchestrator import AgentState
state: AgentState = {
    "task": {"source": "test_data.json"},
    "data": [],
    "context": {},
    "results": [],
    "cost": 0.0,
    "status": "pending",
    "memory_id": None
}

# Execute sequentially
state = extraction.execute(state)
state = distillation.execute(state)
state = ingestion.execute(state)
```

---

## 🔧 Configuration

### Environment Variables

```bash
# .env file
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### Database Setup

Ensure Supabase tables exist:
- `bookmarks` - For ingested data
- `hunches` - For insights
- `proofs` - For mathematical proofs
- `agent_memory` - For agent state persistence

See `SUPABASE_SETUP.md` for database schema.

---

## 📊 Task Types

### 1. Ingestion Task

```python
task = {
    "type": "ingestion",
    "source": "dewey_json.json",  # or image path, or URL
    "chunk_size": 50
}
```

### 2. Inference Task

```python
task = {
    "type": "inference",
    "query": "gematria and sacred geometry",
    "threshold": 0.7
}
```

### 3. Proof Task

```python
task = {
    "type": "proof",
    "theorem": "369 triangle properties"
}
```

### 4. Generative Task

```python
task = {
    "type": "generative",
    "unification": "369 proof",
    "output_type": "game_level"
}
```

---

## 🧪 Testing

### Test Individual Agent

```python
from agents import ExtractionAgent
from agents.orchestrator import AgentState

agent = ExtractionAgent()
state: AgentState = {
    "task": {"source": "test_data.json"},
    "data": [],
    "context": {},
    "results": [],
    "cost": 0.0,
    "status": "pending",
    "memory_id": None
}

result = agent.execute(state)
print(result)
```

### Test Full Workflow

```python
from agents import get_orchestrator

orchestrator = get_orchestrator()

task = {
    "type": "ingestion",
    "source": "test_data.json"
}

result = orchestrator.execute(task)
print(f"Status: {result['status']}")
print(f"Cost: ${result['cost']:.2f}")
```

---

## 🔍 Monitoring

### Check Agent Memory

```python
from agents import get_orchestrator

orchestrator = get_orchestrator()
memory = orchestrator.get_memory("memory_id_here")
print(memory)
```

### Log Hunches

```python
from agents import get_orchestrator

orchestrator = get_orchestrator()
orchestrator.log_hunch(
    "High similarity found between gematria and numerology",
    links=["bookmark_id_1", "bookmark_id_2"],
    cost=0.05
)
```

---

## 🛠️ Troubleshooting

### Issue: "LangGraph not available"

**Solution:**
```bash
pip install langgraph langchain
```

### Issue: "Supabase connection failed"

**Solution:**
- Check environment variables
- Verify Supabase project is active
- Test connection: `python -c "from supabase import create_client; ..."`

### Issue: "Agent execution failed"

**Solution:**
- Check logs: `ingestion_log.txt`
- Verify data format
- Check database schema

---

## 📚 Related Documentation

- **MASTER_ARCHITECTURE.md** - Complete system architecture
- **SUPABASE_SETUP.md** - Database setup
- **INGESTION_GUIDE.md** - Ingestion script guide
- **PRD.md** - Product requirements

---

## 🎯 Next Steps

1. **Complete Supabase Setup** - Enable agent memory
2. **Test Agent Workflow** - Run full ingestion → inference → proof
3. **Expand Proof Agent** - Integrate SymPy for real proofs
4. **Add Cost Tracking** - Monitor API costs
5. **Implement Generative Agent** - Create media/games

---

**Agent framework ready! Start orchestrating!** 🐝✨

