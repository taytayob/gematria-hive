# Internal API Implementation Guide

**Date:** January 6, 2025  
**Status:** 🚀 Implementation Ready

---

## 🎯 Quick Start

### 1. Start Internal API
```bash
# Set internal API key (optional, defaults to "internal-api-key-change-in-production")
export INTERNAL_API_KEY="your-secure-api-key"

# Set port (optional, defaults to 8001)
export INTERNAL_API_PORT=8001

# Start internal API
python internal_api.py
```

### 2. Test Internal API
```bash
# Health check (no auth required)
curl http://localhost:8001/internal/health

# List agents (requires auth)
curl -H "Authorization: Bearer your-secure-api-key" \
  http://localhost:8001/internal/agents

# Execute agent
curl -X POST \
  -H "Authorization: Bearer your-secure-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "state": {
      "task": {"source": "test"},
      "data": [],
      "context": {}
    }
  }' \
  http://localhost:8001/internal/agents/extraction/execute
```

---

## 📊 Architecture

### Port Configuration
- **Port 8000:** Public API (kanban_api.py) - User-facing
- **Port 8001:** Internal API (internal_api.py) - Agent communication
- **Port 3000:** React Webapp - Frontend

### API Separation
- **Public API:** Task management, user interactions
- **Internal API:** Agent communication, system operations
- **Clear boundaries:** Each serves specific purpose

---

## 🔐 Security

### Authentication
- **API Key:** Required for all endpoints except `/internal/health`
- **Header:** `Authorization: Bearer {api_key}`
- **Environment Variable:** `INTERNAL_API_KEY`

### Access Control
- **Internal-only:** Not exposed to public internet
- **IP Whitelisting:** Can be configured via CORS
- **Rate Limiting:** Can be added per endpoint

---

## 🚀 Usage Examples

### Agent Discovery
```python
import requests

# List all agents
response = requests.get(
    "http://localhost:8001/internal/agents",
    headers={"Authorization": "Bearer your-api-key"}
)
agents = response.json()["agents"]
print(f"Available agents: {[a['name'] for a in agents]}")
```

### Agent Execution
```python
# Execute extraction agent
response = requests.post(
    "http://localhost:8001/internal/agents/extraction/execute",
    headers={"Authorization": "Bearer your-api-key"},
    json={
        "state": {
            "task": {"source": "https://example.com/data.json"},
            "data": [],
            "context": {}
        }
    }
)
result = response.json()
print(f"Execution time: {result['execution_time']}s")
print(f"Cost: ${result['cost']}")
```

### Tool Execution
```python
# Execute pattern detection tool
response = requests.post(
    "http://localhost:8001/internal/tools/detect_patterns/execute",
    headers={"Authorization": "Bearer your-api-key"},
    json={
        "parameters": {"data": [...]},
        "context": {}
    }
)
result = response.json()
print(f"Patterns detected: {result['result']}")
```

### Workflow Execution
```python
# Execute workflow via orchestrator
response = requests.post(
    "http://localhost:8001/internal/orchestrator/execute",
    headers={"Authorization": "Bearer your-api-key"},
    json={
        "task": {"type": "extract_and_process"},
        "agents": ["extraction", "distillation", "ingestion"],
        "parallel": True
    }
)
workflow = response.json()
print(f"Workflow ID: {workflow['workflow_id']}")
```

---

## 📝 Next Steps

1. **Add More Endpoints:**
   - Memory management
   - Task management (internal)
   - Metrics and monitoring

2. **Enhance Security:**
   - Service-to-service authentication
   - Rate limiting
   - IP whitelisting

3. **Add Features:**
   - Async execution
   - Webhooks
   - Event streaming

4. **Migration:**
   - Migrate agents to use internal API
   - Replace direct calls with API calls

---

**Internal API is ready for use!** 🐝✨

