# Agent Usage Guide

Complete guide for using Gematria Hive agents both standalone and as part of the MCP orchestrator.

## Overview

All agents in Gematria Hive are designed to be:
- **Modular**: Can be used independently without the full application
- **Standalone**: Have direct methods for direct usage
- **Orchestrated**: Work seamlessly with the MCP orchestrator
- **Well-documented**: Comprehensive docstrings and type hints

## Agent Architecture

Each agent follows this pattern:

```python
class Agent:
    def __init__(self):
        """Initialize agent"""
        pass
    
    def standalone_method(self, data):
        """Standalone method - use directly"""
        pass
    
    def execute(self, state):
        """Orchestrator method - called by MCP"""
        pass
```

## Standalone Usage

### Extraction Agent

```python
from agents.extraction import ExtractionAgent

# Initialize agent
agent = ExtractionAgent()

# Extract data directly
data = agent.extract_from_source("dewey_json.json")
print(f"Extracted {len(data)} items")
```

### Distillation Agent

```python
from agents.distillation import DistillationAgent

# Initialize agent
agent = DistillationAgent()

# Process data directly
processed = agent.process_data(extracted_data)
print(f"Processed {len(processed)} items")
```

### Ingestion Agent

```python
from agents.ingestion import IngestionAgent

# Initialize agent
agent = IngestionAgent()

# Ingest gematria words
count = agent.ingest_gematria_words(words, batch_size=1000)
print(f"Ingested {count} words")

# Ingest CSV file
results = agent.ingest_csv_file("data.csv", chunk_size=10000)
print(f"Results: {results}")
```

### Browser Agent

```python
from agents.browser import BrowserAgent

# Initialize agent
agent = BrowserAgent()

# Scrape URL directly
scraped = agent.scrape_url("https://example.com", max_depth=3)
print(f"Scraped {len(scraped)} pages")

# Find sitemap
sitemap = agent.find_sitemap("https://example.com")
print(f"Sitemap: {sitemap}")

# Parse sitemap
urls = agent.parse_sitemap(sitemap_url)
print(f"Found {len(urls)} URLs")
```

### Inference Agent

```python
from agents.inference import InferenceAgent

# Initialize agent
agent = InferenceAgent()

# Execute inference (orchestrator method)
# For standalone use, call execute() with minimal state
state = {
    "task": {"query": "gematria numerology"},
    "data": [],
    "context": {},
    "results": [],
    "cost": 0.0,
    "status": "pending"
}
result = agent.execute(state)
```

### Proof Agent

```python
from agents.proof import ProofAgent

# Initialize agent
agent = ProofAgent()

# Execute proof generation (orchestrator method)
state = {
    "task": {"theorem": "369 = 3+6+9 = 18 = 1+8 = 9"},
    "data": [],
    "context": {},
    "results": [],
    "cost": 0.0,
    "status": "pending"
}
result = agent.execute(state)
```

## Orchestrator Usage

### Full Workflow

```python
from agents import MCPOrchestrator

# Initialize orchestrator
orchestrator = MCPOrchestrator()

# Execute full workflow
task = {
    "type": "extraction",
    "source": "dewey_json.json",
    "query": "gematria numerology"
}

result = orchestrator.execute(task)
print(f"Status: {result['status']}")
print(f"Cost: ${result['cost']:.2f}")
print(f"Results: {len(result['results'])}")
```

### Browser Task

```python
from agents import MCPOrchestrator

orchestrator = MCPOrchestrator()

# Execute browser task directly
result = orchestrator.execute_browser_task(
    url="https://example.com",
    max_depth=3,
    delay=1.0,
    use_sitemap=True,
    respect_robots=True
)

print(f"Pages scraped: {result['pages_scraped']}")
print(f"Images found: {result['images_found']}")
```

### Log Hunches

```python
from agents import MCPOrchestrator

orchestrator = MCPOrchestrator()

# Log a hunch to database
orchestrator.log_hunch(
    content="High similarity found between 369 and sacred geometry",
    links=["bookmark_id_1", "bookmark_id_2"],
    cost=0.05
)
```

## CLI Scripts

See `scripts/README.md` for complete CLI usage examples.

Quick examples:

```bash
# Extract data
python scripts/extract.py --source dewey_json.json --output extracted.json

# Process data
python scripts/distill.py --input extracted.json --output processed.json

# Ingest data
python scripts/ingest.py --input processed.json

# Scrape website
python scripts/browser.py --url https://example.com --output scraped.json
```

## Task Manager

For task/hunch management:

```python
from task_manager import TaskManager, get_task_manager

# Get task manager
tm = get_task_manager()

# Create task
task = tm.create_task(
    content="Investigate 369 gematria connections",
    status="pending",
    cost=0.0,
    links=["bookmark_1", "bookmark_2"]
)

# Get tasks by status
pending = tm.get_tasks_by_status("pending")
in_progress = tm.get_tasks_by_status("in_progress")

# Update task
tm.update_task(
    task_id=task["id"],
    status="in_progress",
    cost=0.05
)

# Get statistics
stats = tm.get_task_statistics()
print(f"Total tasks: {stats['total']}")
print(f"Total cost: ${stats['total_cost']:.2f}")
```

## Best Practices

1. **Use standalone methods** when you only need one agent
2. **Use orchestrator** for full workflows
3. **Use CLI scripts** for quick operations
4. **Check dependencies** before using agents
5. **Handle errors** gracefully
6. **Log operations** for debugging

## Error Handling

All agents handle errors gracefully:

```python
from agents.extraction import ExtractionAgent

agent = ExtractionAgent()
data = agent.extract_from_source("nonexistent.json")

if not data:
    print("Extraction failed or returned no data")
```

## Dependencies

Some agents require optional dependencies:

- **Inference Agent**: Requires `sentence-transformers` and Supabase
- **Proof Agent**: Requires `sympy` for proof generation
- **Browser Agent**: Requires `scraper` module
- **Distillation Agent**: Requires `ingest_pass1` utilities

Agents will work without optional dependencies but with limited functionality.

## Examples

See `examples/` directory for complete usage examples (if available).

## Support

For issues or questions:
- Check agent docstrings: `help(Agent)`
- Review `AGENT_SETUP.md` for setup instructions
- Check `scripts/README.md` for CLI usage
- Review individual agent files for implementation details

