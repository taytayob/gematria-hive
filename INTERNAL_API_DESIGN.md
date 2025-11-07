# Internal API Design - Gematria Hive

**Date:** January 6, 2025  
**Status:** 🚀 Design Proposal

---

## 🎯 Purpose

Design an internal API for agent-to-agent communication, system component interaction, and internal service coordination. This API would be separate from the public-facing kanban API and optimized for internal system operations.

---

## 📊 Current Architecture Analysis

### Current Communication Patterns

1. **MCP Protocol (AgentState):**
   - Agents communicate via shared `AgentState` TypedDict
   - Orchestrator manages state flow
   - Direct function calls between agents

2. **Public API (kanban_api.py):**
   - Port 8000: HTML kanban + REST API
   - Port 3000: React webapp (proxies to 8000)
   - Public-facing endpoints for task management

3. **Direct Database Access:**
   - Agents access Supabase directly
   - No standardized internal communication layer
   - Mixed patterns (direct calls, state passing, DB access)

### Gaps Identified

1. **No Internal API Layer:**
   - Agents communicate via direct calls or shared state
   - No RESTful internal communication
   - No service discovery
   - No internal-only endpoints

2. **Tight Coupling:**
   - Agents directly import each other
   - Hard to scale horizontally
   - Difficult to replace components
   - Testing challenges

3. **No Service Boundaries:**
   - All components access database directly
   - No clear service boundaries
   - Mixed concerns

---

## 🚀 Internal API Design

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│              Public API (Port 8000)                      │
│  - HTML Kanban                                           │
│  - Public REST API                                        │
│  - User-facing endpoints                                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│         Internal API (Port 8001)                        │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Agent Communication Layer                       │   │
│  │  - Agent-to-agent messaging                      │   │
│  │  - Service discovery                             │   │
│  │  - Internal task management                      │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │  System Component Layer                          │   │
│  │  - Orchestrator API                              │   │
│  │  - Tool Registry API                             │   │
│  │  - Cost Manager API                              │   │
│  │  - Memory Management API                         │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Data Access Layer                                │   │
│  │  - Internal database operations                   │   │
│  │  - Caching layer                                  │   │
│  │  - Query optimization                             │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              Agents & Components                         │
│  - 35+ Agents                                           │
│  - Orchestrator                                         │
│  - Tool Registry                                        │
│  - Cost Manager                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Internal API Endpoints

### 1. Agent Communication API

#### Agent Discovery
```python
GET /internal/agents
# List all available agents
Response: {
    "agents": [
        {
            "name": "extraction",
            "description": "Extract data from sources",
            "status": "active",
            "capabilities": ["json", "csv", "url"],
            "cost_per_call": 0.01
        },
        ...
    ]
}

GET /internal/agents/{agent_name}
# Get agent details
Response: {
    "name": "extraction",
    "description": "...",
    "status": "active",
    "capabilities": [...],
    "health": "healthy",
    "last_execution": "2025-01-06T12:00:00Z"
}
```

#### Agent Execution
```python
POST /internal/agents/{agent_name}/execute
# Execute agent with state
Request: {
    "state": {
        "task": {...},
        "data": [...],
        "context": {...}
    },
    "async": false
}
Response: {
    "result": {
        "state": {...},
        "execution_time": 0.5,
        "cost": 0.01
    }
}

POST /internal/agents/{agent_name}/execute-async
# Execute agent asynchronously
Request: {
    "state": {...},
    "callback_url": "http://internal:8001/internal/callbacks/{job_id}"
}
Response: {
    "job_id": "uuid",
    "status": "queued",
    "estimated_time": 5.0
}
```

#### Agent Status
```python
GET /internal/agents/{agent_name}/status
# Get agent status
Response: {
    "status": "active",
    "queue_length": 5,
    "current_executions": 2,
    "health": "healthy"
}

GET /internal/agents/{agent_name}/metrics
# Get agent metrics
Response: {
    "total_executions": 1000,
    "success_rate": 0.98,
    "avg_execution_time": 0.5,
    "total_cost": 10.0,
    "errors": 20
}
```

### 2. Orchestrator API

#### Workflow Management
```python
POST /internal/orchestrator/execute
# Execute workflow
Request: {
    "task": {...},
    "agents": ["extraction", "distillation", "ingestion"],
    "parallel": true
}
Response: {
    "workflow_id": "uuid",
    "status": "running",
    "estimated_completion": "2025-01-06T12:05:00Z"
}

GET /internal/orchestrator/workflows/{workflow_id}
# Get workflow status
Response: {
    "workflow_id": "uuid",
    "status": "completed",
    "progress": 100,
    "results": {...},
    "cost": 0.15,
    "execution_time": 5.0
}

GET /internal/orchestrator/workflows
# List workflows
Response: {
    "workflows": [
        {
            "workflow_id": "uuid",
            "status": "completed",
            "created_at": "2025-01-06T12:00:00Z",
            "cost": 0.15
        },
        ...
    ]
}
```

#### State Management
```python
GET /internal/orchestrator/state/{state_id}
# Get workflow state
Response: {
    "state_id": "uuid",
    "state": {
        "task": {...},
        "data": [...],
        "context": {...},
        "results": [...],
        "cost": 0.15
    }
}

PUT /internal/orchestrator/state/{state_id}
# Update workflow state
Request: {
    "state": {
        "data": [...],
        "context": {...}
    }
}
```

### 3. Tool Registry API

#### Tool Discovery
```python
GET /internal/tools
# List all tools
Response: {
    "tools": [
        {
            "name": "detect_patterns",
            "description": "Detect patterns in data",
            "category": "analysis",
            "agent": "pattern_detector",
            "cost_per_call": 0.02
        },
        ...
    ]
}

GET /internal/tools/{tool_name}
# Get tool details
Response: {
    "name": "detect_patterns",
    "description": "...",
    "category": "analysis",
    "agent": "pattern_detector",
    "parameters": {...},
    "returns": "Dict",
    "cost_per_call": 0.02
}

GET /internal/tools/category/{category}
# Get tools by category
Response: {
    "category": "analysis",
    "tools": [...]
}
```

#### Tool Execution
```python
POST /internal/tools/{tool_name}/execute
# Execute tool
Request: {
    "parameters": {...},
    "context": {...}
}
Response: {
    "result": {...},
    "execution_time": 0.1,
    "cost": 0.02
}
```

### 4. Cost Management API

#### Cost Tracking
```python
GET /internal/cost/current
# Get current cost
Response: {
    "total_cost": 8.50,
    "daily_cost": 2.30,
    "remaining_budget": 1.50,
    "budget_cap": 10.00,
    "alerts": []
}

GET /internal/cost/history
# Get cost history
Response: {
    "history": [
        {
            "date": "2025-01-06",
            "cost": 2.30,
            "operations": 150
        },
        ...
    ]
}

GET /internal/cost/by-agent
# Get cost by agent
Response: {
    "by_agent": {
        "extraction": 1.50,
        "distillation": 2.00,
        "inference": 1.80,
        ...
    }
}
```

#### Budget Management
```python
POST /internal/cost/budget
# Set budget
Request: {
    "daily_budget": 5.00,
    "total_budget": 10.00
}
Response: {
    "daily_budget": 5.00,
    "total_budget": 10.00,
    "alerts_enabled": true
}
```

### 5. Memory Management API

#### Memory Operations
```python
POST /internal/memory/store
# Store memory
Request: {
    "agent": "inference",
    "context": {...},
    "data": {...},
    "ttl": 3600
}
Response: {
    "memory_id": "uuid",
    "stored_at": "2025-01-06T12:00:00Z"
}

GET /internal/memory/{memory_id}
# Get memory
Response: {
    "memory_id": "uuid",
    "agent": "inference",
    "context": {...},
    "data": {...},
    "stored_at": "2025-01-06T12:00:00Z",
    "expires_at": "2025-01-06T13:00:00Z"
}

GET /internal/memory/agent/{agent_name}
# Get memories by agent
Response: {
    "agent": "inference",
    "memories": [
        {
            "memory_id": "uuid",
            "context": {...},
            "stored_at": "..."
        },
        ...
    ]
}
```

### 6. Task Management API (Internal)

#### Internal Task Operations
```python
POST /internal/tasks/create
# Create internal task
Request: {
    "content": "Process data extraction",
    "phase": "phase1_basic",
    "role": "developer",
    "metadata": {
        "agent_context": "extraction",
        "internal": true
    }
}
Response: {
    "task_id": "uuid",
    "status": "pending"
}

GET /internal/tasks/by-agent/{agent_name}
# Get tasks by agent
Response: {
    "agent": "extraction",
    "tasks": [...]
}

GET /internal/tasks/by-phase/{phase}
# Get tasks by phase
Response: {
    "phase": "phase1_basic",
    "tasks": [...]
}

PUT /internal/tasks/{task_id}/update
# Update internal task
Request: {
    "status": "completed",
    "progress": 100,
    "metadata": {...}
}
```

### 7. System Health API

#### Health Checks
```python
GET /internal/health
# System health
Response: {
    "status": "healthy",
    "components": {
        "orchestrator": "healthy",
        "database": "healthy",
        "agents": "healthy"
    },
    "timestamp": "2025-01-06T12:00:00Z"
}

GET /internal/health/agents
# Agent health
Response: {
    "agents": {
        "extraction": "healthy",
        "distillation": "healthy",
        ...
    }
}

GET /internal/health/database
# Database health
Response: {
    "status": "healthy",
    "connection": "active",
    "latency": 0.05
}
```

---

## 🔐 Security & Access Control

### Authentication
```python
# Internal API uses API keys or service tokens
Authorization: Bearer {internal_api_key}

# Or service-to-service authentication
X-Service-Name: orchestrator
X-Service-Token: {service_token}
```

### Access Control
- **Internal-only:** Not exposed to public
- **Service authentication:** Services authenticate with tokens
- **Rate limiting:** Per-service rate limits
- **IP whitelisting:** Only allow internal IPs

---

## 📊 Benefits

### 1. Separation of Concerns
- **Public API:** User-facing, task management
- **Internal API:** Agent communication, system operations
- **Clear boundaries:** Each API has specific purpose

### 2. Scalability
- **Horizontal scaling:** Agents can run on different machines
- **Service discovery:** Agents can discover each other
- **Load balancing:** Distribute agent execution

### 3. Testability
- **Mock services:** Easy to mock internal services
- **Integration tests:** Test agent communication
- **Isolated testing:** Test components independently

### 4. Flexibility
- **Replace components:** Easy to swap implementations
- **Add new agents:** Register via API
- **Dynamic routing:** Route to available agents

### 5. Observability
- **Metrics:** Track agent performance
- **Logging:** Centralized logging
- **Tracing:** Track request flow

---

## 🚀 Implementation Plan

### Phase 1: Core Internal API
1. Create `internal_api.py` (FastAPI)
2. Implement agent discovery endpoints
3. Implement agent execution endpoints
4. Add authentication/authorization

### Phase 2: Orchestrator Integration
1. Expose orchestrator via internal API
2. Add workflow management endpoints
3. Add state management endpoints

### Phase 3: Tool Registry Integration
1. Expose tool registry via internal API
2. Add tool discovery endpoints
3. Add tool execution endpoints

### Phase 4: Cost & Memory Management
1. Expose cost manager via internal API
2. Expose memory management via internal API
3. Add monitoring endpoints

### Phase 5: Agent Migration
1. Migrate agents to use internal API
2. Replace direct calls with API calls
3. Add service discovery

---

## 📝 Example Usage

### Agent-to-Agent Communication
```python
# Agent A wants to use Agent B
import requests

# Discover available agents
response = requests.get(
    "http://internal:8001/internal/agents",
    headers={"Authorization": "Bearer {api_key}"}
)
agents = response.json()["agents"]

# Execute Agent B
response = requests.post(
    "http://internal:8001/internal/agents/extraction/execute",
    headers={"Authorization": "Bearer {api_key}"},
    json={
        "state": {
            "task": {"source": "https://example.com/data.json"},
            "data": [],
            "context": {}
        }
    }
)
result = response.json()["result"]
```

### Orchestrator Workflow
```python
# Create workflow via internal API
response = requests.post(
    "http://internal:8001/internal/orchestrator/execute",
    headers={"Authorization": "Bearer {api_key}"},
    json={
        "task": {"type": "extract_and_process"},
        "agents": ["extraction", "distillation", "ingestion"],
        "parallel": True
    }
)
workflow_id = response.json()["workflow_id"]

# Check workflow status
response = requests.get(
    f"http://internal:8001/internal/orchestrator/workflows/{workflow_id}",
    headers={"Authorization": "Bearer {api_key}"}
)
status = response.json()["status"]
```

---

## 🎯 Next Steps

1. **Review Design:** Validate architecture with team
2. **Create Prototype:** Implement basic internal API
3. **Test Integration:** Test with existing agents
4. **Migrate Gradually:** Migrate agents one by one
5. **Monitor Performance:** Track API performance

---

**This internal API would provide a clean, scalable foundation for agent communication!** 🐝✨

