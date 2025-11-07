# Integration Coordination Plan - Replit, Supabase, Docker, MCP & Agents

**Date:** January 6, 2025  
**Status:** 🚀 **IN PROGRESS**

---

## 🎯 Objective

Coordinate and integrate:
1. **Replit** - Development and deployment platform
2. **Supabase** - Database and backend services
3. **Docker** - Containerization for services
4. **MCP** - Model Context Protocol for agent communication
5. **Agents** - 36+ autonomous agents with MCP integration

---

## 📊 Current State

### ✅ Completed
- ✅ **MCP Tool Registry:** Centralized tool registry implemented
- ✅ **MCP Orchestrator:** Agent workflow orchestration
- ✅ **Internal API:** Agent communication layer (port 8001)
- ✅ **Agents:** 36+ agents implemented
- ✅ **Docker:** Basic Docker configuration exists
- ✅ **Supabase:** Database schema and connection

### ⚠️ Needs Integration
- ⚠️ **Agents → MCP:** Some agents not using tool registry
- ⚠️ **Docker → Services:** Need to add internal API to Docker
- ⚠️ **Replit → Supabase:** Need to verify connection
- ⚠️ **MCP → Internal API:** Need to expose MCP via internal API

---

## 🚀 Integration Plan

### Phase 1: MCP & Agent Integration (Immediate)

#### 1.1 Ensure All Agents Use MCP Tool Registry
- [ ] **Update agents to register tools**
  - [ ] Pattern Detector Agent
  - [ ] Dark Matter Tracker Agent
  - [ ] Persona Manager Agent
  - [ ] Claude Integrator Agent
  - [ ] Affinity Agent
  - [ ] Other agents with tools

- [ ] **Update agents to use tool registry**
  - [ ] Allow agents to discover and use other agents' tools
  - [ ] Add tool discovery methods to agents
  - [ ] Update agent execution to use MCP tools

#### 1.2 Integrate MCP with Internal API
- [ ] **Expose MCP via Internal API**
  - [ ] Add MCP tool registry endpoints
  - [ ] Add tool execution endpoints
  - [ ] Add tool discovery endpoints

- [ ] **Update Internal API to use MCP**
  - [ ] Agent execution via MCP
  - [ ] Tool execution via MCP
  - [ ] Workflow orchestration via MCP

---

### Phase 2: Docker Integration (Short-term)

#### 2.1 Update Docker Configuration
- [ ] **Add Internal API Service**
  - [ ] Create Dockerfile for internal API
  - [ ] Add internal API to docker-compose.yml
  - [ ] Configure networking between services

- [ ] **Update Backend Service**
  - [ ] Include internal API in backend
  - [ ] Configure environment variables
  - [ ] Add health checks

#### 2.2 Docker Compose Services
- [ ] **Service Architecture**
  - [ ] `webapp` - React frontend (port 3000)
  - [ ] `backend` - Public API (port 8000)
  - [ ] `internal-api` - Internal API (port 8001)
  - [ ] `supabase` - Local Supabase (optional)

---

### Phase 3: Replit Integration (Short-term)

#### 3.1 Replit Configuration
- [ ] **Update .replit file**
  - [ ] Add internal API workflow
  - [ ] Configure environment variables
  - [ ] Add multiple port support

- [ ] **Replit Secrets**
  - [ ] SUPABASE_URL
  - [ ] SUPABASE_KEY
  - [ ] INTERNAL_API_KEY

#### 3.2 Replit Setup Script
- [ ] **Update setup_replit.sh**
  - [ ] Verify Supabase connection
  - [ ] Test internal API
  - [ ] Test MCP tool registry
  - [ ] Verify agent integration

---

### Phase 4: Supabase Integration (Short-term)

#### 4.1 Database Connection
- [ ] **Verify Supabase Connection**
  - [ ] Test connection from Replit
  - [ ] Test connection from Docker
  - [ ] Test connection from local

- [ ] **Environment Variables**
  - [ ] SUPABASE_URL
  - [ ] SUPABASE_KEY
  - [ ] Connection pooling

#### 4.2 Agent Memory & State
- [ ] **MCP State Persistence**
  - [ ] Store agent state in Supabase
  - [ ] Store tool registry state
  - [ ] Store workflow state

---

## 🔧 Implementation Steps

### Step 1: Update Agents to Use MCP Tool Registry

#### 1.1 Create Agent Base Class with MCP Support
```python
# agents/base_agent.py
from agents.mcp_tool_registry import get_tool_registry

class BaseAgent:
    def __init__(self):
        self.tool_registry = get_tool_registry()
    
    def use_tool(self, tool_name: str, **kwargs):
        """Use a tool from the MCP registry"""
        return self.tool_registry.execute_tool(tool_name, **kwargs)
    
    def discover_tools(self, category: str = None):
        """Discover available tools"""
        return self.tool_registry.list_tools(category=category)
```

#### 1.2 Update Agents to Register Tools
- Update each agent to register its tools on initialization
- Ensure tools are accessible via MCP

### Step 2: Integrate MCP with Internal API

#### 2.1 Add MCP Endpoints to Internal API
```python
# internal_api.py
@app.get("/internal/mcp/tools")
async def list_mcp_tools(api_key: str = Depends(verify_internal_api_key)):
    """List all MCP tools"""
    return tool_registry.list_all_tools()

@app.post("/internal/mcp/tools/{tool_name}/execute")
async def execute_mcp_tool(tool_name: str, parameters: Dict, api_key: str = Depends(verify_internal_api_key)):
    """Execute an MCP tool"""
    result = tool_registry.execute_tool(tool_name, **parameters)
    return {"result": result}
```

### Step 3: Update Docker Configuration

#### 3.1 Add Internal API to docker-compose.yml
```yaml
services:
  internal-api:
    build:
      context: .
      dockerfile: Dockerfile.internal-api
    ports:
      - "8001:8001"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
      - INTERNAL_API_KEY=${INTERNAL_API_KEY}
    networks:
      - gematria-network
```

#### 3.2 Create Dockerfile for Internal API
```dockerfile
# Dockerfile.internal-api
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8001
CMD ["uvicorn", "internal_api:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Step 4: Update Replit Configuration

#### 4.1 Update .replit for Multiple Services
```toml
[workflows]
runButton = "All Services"

[[workflows.workflow]]
name = "All Services"
mode = "parallel"
author = "agent"

[[workflows.workflow.tasks]]
task = "shell.exec"
args = "python run_kanban.py"
waitForPort = 8000

[[workflows.workflow.tasks]]
task = "shell.exec"
args = "python run_internal_api.py"
waitForPort = 8001
```

---

## 📋 Integration Checklist

### MCP & Agent Integration
- [ ] All agents register tools with MCP registry
- [ ] All agents can discover and use other agents' tools
- [ ] MCP tool registry exposed via internal API
- [ ] Agent execution uses MCP tools
- [ ] Workflow orchestration uses MCP

### Docker Integration
- [ ] Internal API added to docker-compose.yml
- [ ] Dockerfile for internal API created
- [ ] Services can communicate via Docker network
- [ ] Environment variables configured
- [ ] Health checks added

### Replit Integration
- [ ] .replit updated for multiple services
- [ ] Replit Secrets configured
- [ ] Setup script updated
- [ ] Services can run in parallel
- [ ] Ports configured correctly

### Supabase Integration
- [ ] Connection verified from all environments
- [ ] Environment variables set
- [ ] Agent memory stored in Supabase
- [ ] Tool registry state persisted
- [ ] Workflow state persisted

---

## 🎯 Success Criteria

### MCP Integration
- ✅ All agents use MCP tool registry
- ✅ Tools discoverable via internal API
- ✅ Tools executable via internal API
- ✅ Agents can use other agents' tools

### Docker Integration
- ✅ All services containerized
- ✅ Services communicate via Docker network
- ✅ Environment variables configured
- ✅ Health checks working

### Replit Integration
- ✅ All services run in Replit
- ✅ Supabase connection working
- ✅ Internal API accessible
- ✅ MCP tools accessible

### Supabase Integration
- ✅ Connection verified
- ✅ Agent memory persisted
- ✅ Tool registry state persisted
- ✅ Workflow state persisted

---

## 🚀 Quick Start

### Local Development
```bash
# Start all services with Docker
docker-compose up

# Or start individually
python run_kanban.py &        # Port 8000
python run_internal_api.py &  # Port 8001
cd webapp && npm run dev &     # Port 3000
```

### Replit
```bash
# Run setup script
./setup_replit.sh

# Start services
python run_kanban.py &
python run_internal_api.py &
```

### Docker
```bash
# Build and start
docker-compose up --build

# Check services
docker-compose ps
```

---

## 📝 Next Steps

1. **Implement agent base class with MCP support**
2. **Update all agents to use MCP tool registry**
3. **Add MCP endpoints to internal API**
4. **Update Docker configuration**
5. **Update Replit configuration**
6. **Test integration end-to-end**

---

**Status:** 🚀 **READY FOR IMPLEMENTATION**

