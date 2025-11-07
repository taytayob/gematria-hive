# Agent/MCP Navigation Guide - Gematria Hive

**Purpose:** Guide for agents and MCP tools to navigate the platform efficiently using phases, metadata, resources, tags, and roles.

**Date:** January 6, 2025

---

## 🎯 Navigation Layers

### Layer 1: Phases
**Purpose:** Organize tasks by project phase

**Phases:**
- `phase1_basic` - Foundation: Basic setup, core features
- `phase2_deep` - Deep Analysis: Advanced features, optimization
- `phase3_advanced` - Advanced: Enterprise features
- `phase4_scale` - Scale: Scaling, performance

**Usage:**
```python
# Get tasks by phase
tasks = task_manager.get_tasks_by_phase("phase1_basic")

# Filter by phase in API
GET /api/tasks/phase/phase1_basic
```

### Layer 2: Roles
**Purpose:** Organize tasks by role assignment

**Roles:**
- `project_manager` - Manages phases, timelines, resources
- `product_manager` - Manages PRD, features, roadmap
- `developer` - Develops features, fixes bugs
- `designer` - Creates designs, mockups
- `qa` - Tests features, validates quality

**Usage:**
```python
# Get tasks by role
tasks = task_manager.get_tasks_by_role("developer")

# Filter by role in API
GET /api/tasks/role/developer
```

### Layer 3: Tags
**Purpose:** Categorize tasks with flexible tags

**Usage:**
```python
# Get tasks by tag
tasks = task_manager.get_tasks_by_tag("gematria")

# Filter by tag in API
GET /api/tasks/tag/gematria
```

### Layer 4: Resources
**Purpose:** Link resources to tasks

**Resource Types:**
- `url` - Web URLs
- `file` - File paths
- `document` - Documents
- `code` - Code snippets
- `image` - Images
- `video` - Videos
- `audio` - Audio files
- `data` - Data files
- `other` - Other resources

**Usage:**
```python
# Add resource to task
resource = task_manager.add_resource_to_task(
    task_id="...",
    resource_type="url",
    resource_name="Documentation",
    resource_url="https://example.com/docs"
)
```

### Layer 5: Metadata
**Purpose:** Flexible JSONB metadata for any additional data

**Usage:**
```python
# Create task with metadata
task = task_manager.create_task(
    content="...",
    metadata={
        "agent_context": "inference",
        "mcp_tool": "pattern_detector",
        "related_patterns": ["pattern1", "pattern2"],
        "cost_estimate": 0.05
    }
)
```

---

## 🔍 Agent Navigation Patterns

### Pattern 1: Phase-Based Navigation
```python
# Agent workflow by phase
def agent_workflow_by_phase():
    # Phase 1: Foundation tasks
    phase1_tasks = task_manager.get_tasks_by_phase("phase1_basic")
    for task in phase1_tasks:
        if task.status == "pending":
            process_task(task)
    
    # Phase 2: Deep analysis tasks
    phase2_tasks = task_manager.get_tasks_by_phase("phase2_deep")
    for task in phase2_tasks:
        if task.status == "pending":
            process_task(task)
```

### Pattern 2: Role-Based Navigation
```python
# Agent workflow by role
def agent_workflow_by_role():
    # Developer tasks
    dev_tasks = task_manager.get_tasks_by_role("developer")
    for task in dev_tasks:
        if task.status == "pending":
            process_developer_task(task)
    
    # Product manager tasks
    pm_tasks = task_manager.get_tasks_by_role("product_manager")
    for task in pm_tasks:
        if task.status == "pending":
            process_pm_task(task)
```

### Pattern 3: Tag-Based Navigation
```python
# Agent workflow by tag
def agent_workflow_by_tag():
    # Gematria-related tasks
    gematria_tasks = task_manager.get_tasks_by_tag("gematria")
    for task in gematria_tasks:
        process_gematria_task(task)
    
    # Pattern detection tasks
    pattern_tasks = task_manager.get_tasks_by_tag("pattern")
    for task in pattern_tasks:
        process_pattern_task(task)
```

### Pattern 4: Metadata-Based Navigation
```python
# Agent workflow by metadata
def agent_workflow_by_metadata():
    all_tasks = task_manager.get_all_tasks()
    
    # Tasks for inference agent
    inference_tasks = [
        task for task in all_tasks
        if task.get("metadata", {}).get("agent_context") == "inference"
    ]
    
    # Tasks using specific MCP tool
    mcp_tool_tasks = [
        task for task in all_tasks
        if task.get("metadata", {}).get("mcp_tool") == "pattern_detector"
    ]
```

---

## 🛠️ MCP Tool Integration

### Tool 1: Task Query Tool
```python
# MCP tool for querying tasks
def query_tasks(phase=None, role=None, tag=None, status=None):
    """Query tasks with filters"""
    tasks = task_manager.get_all_tasks()
    
    if phase:
        tasks = [t for t in tasks if t.get("phase") == phase]
    if role:
        tasks = [t for t in tasks if t.get("role") == role]
    if tag:
        tasks = [t for t in tasks if tag in (t.get("tags") or [])]
    if status:
        tasks = [t for t in tasks if t.get("status") == status]
    
    return tasks
```

### Tool 2: Resource Access Tool
```python
# MCP tool for accessing resources
def get_task_resources(task_id):
    """Get all resources for a task"""
    task = task_manager.get_task(task_id)
    if not task:
        return []
    
    resources = task.get("resources", [])
    # Fetch resource details from task_resources table
    return resources
```

### Tool 3: Metadata Query Tool
```python
# MCP tool for querying metadata
def query_by_metadata(key, value):
    """Query tasks by metadata key-value"""
    all_tasks = task_manager.get_all_tasks()
    return [
        task for task in all_tasks
        if task.get("metadata", {}).get(key) == value
    ]
```

---

## 📊 Database Views for Navigation

### View: tasks_by_phase_role
```sql
SELECT * FROM tasks_by_phase_role
WHERE phase = 'phase1_basic' AND role = 'developer';
```

### View: task_resources_view
```sql
SELECT * FROM task_resources_view
WHERE task_phase = 'phase1_basic';
```

### View: task_stats_by_phase
```sql
SELECT * FROM task_stats_by_phase
WHERE phase = 'phase1_basic';
```

### View: task_stats_by_role
```sql
SELECT * FROM task_stats_by_role
WHERE role = 'developer';
```

---

## 🔗 API Endpoints for Navigation

### Phase Navigation
- `GET /api/tasks/phase/{phase}` - Get tasks by phase
- `GET /api/phases` - Get all phases

### Role Navigation
- `GET /api/tasks/role/{role}` - Get tasks by role
- `GET /api/roles` - Get all roles

### Tag Navigation
- `GET /api/tasks/tag/{tag}` - Get tasks by tag

### Resource Navigation
- `POST /api/tasks/{task_id}/resources` - Add resource to task
- `GET /api/tasks/{task_id}` - Get task with resources

### Metadata Navigation
- Use task metadata field for flexible queries
- Filter in application layer based on metadata content

---

## 📝 Best Practices

### 1. Use Phases for Project Organization
- Assign tasks to appropriate phases
- Use phase filters for agent workflows
- Track phase progress

### 2. Use Roles for Task Assignment
- Assign tasks to appropriate roles
- Use role filters for role-specific workflows
- Track role workload

### 3. Use Tags for Flexible Categorization
- Tag tasks with relevant keywords
- Use tags for cross-cutting concerns
- Enable multi-dimensional filtering

### 4. Use Resources for Task Context
- Link relevant resources to tasks
- Use resources for agent context
- Track resource usage

### 5. Use Metadata for Agent Context
- Store agent-specific context in metadata
- Use metadata for MCP tool routing
- Enable flexible querying

---

## 🎯 Example Agent Workflows

### Inference Agent Workflow
```python
# 1. Get tasks tagged with "inference"
inference_tasks = task_manager.get_tasks_by_tag("inference")

# 2. Filter by phase
phase1_inference = [t for t in inference_tasks if t.get("phase") == "phase1_basic"]

# 3. Process tasks
for task in phase1_inference:
    if task.status == "pending":
        # Get resources
        resources = task.get("resources", [])
        
        # Get metadata context
        metadata = task.get("metadata", {})
        agent_context = metadata.get("agent_context", "inference")
        
        # Process task
        result = process_inference_task(task, resources, metadata)
        
        # Update task
        task_manager.update_task(
            task["id"],
            status="in_progress",
            progress=50,
            metadata={**metadata, "processing": True}
        )
```

### Pattern Detector Agent Workflow
```python
# 1. Get tasks with pattern metadata
all_tasks = task_manager.get_all_tasks()
pattern_tasks = [
    t for t in all_tasks
    if t.get("metadata", {}).get("mcp_tool") == "pattern_detector"
]

# 2. Process by phase
for phase in ["phase1_basic", "phase2_deep"]:
    phase_tasks = [t for t in pattern_tasks if t.get("phase") == phase]
    for task in phase_tasks:
        process_pattern_task(task)
```

---

## 🔄 Integration with Orchestrator

### Orchestrator Task Creation
```python
# Create task from orchestrator
def create_orchestrator_task(task_type, phase, metadata):
    task = task_manager.create_task(
        content=f"Process {task_type} task",
        phase=phase,
        role="developer",
        priority="medium",
        tags=[task_type],
        metadata={
            "task_type": task_type,
            "orchestrator": True,
            **metadata
        }
    )
    return task
```

### Agent Task Updates
```python
# Update task from agent
def update_agent_task(task_id, result, cost):
    task_manager.update_task(
        task_id=task_id,
        status="completed",
        progress=100,
        cost=cost,
        metadata={
            **task.get("metadata", {}),
            "agent_result": result,
            "completed_at": datetime.utcnow().isoformat()
        }
    )
```

---

**This navigation system enables efficient agent and MCP tool navigation through the platform!** 🐝✨

