# Autonomous Agent

**Purpose:** Autonomous agent that can commit changes and proceed with work while you're away, with configurable milestones to stop at reasonable points.

**Author:** Gematria Hive Team  
**Date:** January 6, 2025

---

## Overview

The Autonomous Agent is designed to work autonomously, automatically committing changes and processing tasks while you're away. It includes safety features with configurable milestones to ensure it stops at reasonable points.

### Features

- ✅ **Automatic Git Commits**: Monitors git status and commits changes automatically
- ✅ **Task Queue Processing**: Processes a queue of tasks autonomously
- ✅ **Milestone-Based Stopping**: Stops at configurable milestones (max commits, time, tasks)
- ✅ **Activity Logging**: Logs all activities for review
- ✅ **Safe Operation**: Configurable settings for safe autonomous operation
- ✅ **Auto-Push Option**: Optional automatic pushing of commits

---

## Quick Start

### Basic Usage

```bash
# Run with default settings (10 commits max, 8 hours max, 50 tasks max)
python run_autonomous.py

# Run with custom milestones
python run_autonomous.py --max-commits 20 --max-time 12.0 --max-tasks 100

# Run with auto-push enabled
python run_autonomous.py --auto-push

# Run with custom config file
python run_autonomous.py --config autonomous_config.json
```

### Configuration File

Create `autonomous_config.json` (copy from `autonomous_config.json.example`):

```json
{
  "max_commits": 10,
  "max_time_hours": 8.0,
  "max_tasks": 50,
  "commit_interval_seconds": 300,
  "auto_push": false,
  "branch": null,
  "work_dir": null
}
```

### Task File

Create `autonomous_tasks.json` (copy from `autonomous_tasks.json.example`):

```json
[
  {
    "type": "commit",
    "action": "commit",
    "description": "Commit current changes"
  },
  {
    "type": "wait",
    "action": "wait",
    "seconds": 60,
    "description": "Wait 60 seconds"
  }
]
```

---

## Configuration Options

### Milestones

| Option | Default | Description |
|--------|---------|-------------|
| `max_commits` | 10 | Maximum number of commits before stopping |
| `max_time_hours` | 8.0 | Maximum hours to run before stopping |
| `max_tasks` | 50 | Maximum number of tasks to process before stopping |

### Commit Settings

| Option | Default | Description |
|--------|---------|-------------|
| `commit_interval_seconds` | 300 | Minimum seconds between commits (5 minutes) |
| `auto_push` | false | Automatically push commits to remote |
| `branch` | null | Git branch to work on (default: current branch) |

### Other Settings

| Option | Default | Description |
|--------|---------|-------------|
| `work_dir` | null | Working directory (default: current directory) |

---

## Command-Line Options

```bash
python run_autonomous.py [OPTIONS]

Options:
  --max-commits N          Maximum number of commits (default: 10)
  --max-time HOURS         Maximum hours to run (default: 8.0)
  --max-tasks N            Maximum number of tasks (default: 50)
  --commit-interval SEC    Minimum seconds between commits (default: 300)
  --auto-push              Automatically push commits
  --branch BRANCH          Git branch to work on
  --work-dir DIR           Working directory
  --config FILE            Path to JSON configuration file
  --tasks FILE             Path to JSON file with tasks
```

---

## Usage Examples

### Example 1: Overnight Work Session

Run for 8 hours with auto-commit every 5 minutes, max 20 commits:

```bash
python run_autonomous.py \
  --max-time 8.0 \
  --max-commits 20 \
  --commit-interval 300
```

### Example 2: Short Session with Auto-Push

Run for 2 hours, auto-push commits:

```bash
python run_autonomous.py \
  --max-time 2.0 \
  --max-commits 5 \
  --auto-push
```

### Example 3: Process Specific Tasks

Process tasks from a file:

```bash
python run_autonomous.py \
  --tasks autonomous_tasks.json \
  --max-tasks 100
```

### Example 4: Using Config File

```bash
# Create config file
cp autonomous_config.json.example autonomous_config.json
# Edit autonomous_config.json as needed

# Run with config
python run_autonomous.py --config autonomous_config.json
```

---

## How It Works

### Main Loop

1. **Check Milestones**: Stop if any milestone is reached
2. **Process Tasks**: If tasks are in queue, process next task
3. **Check Git Status**: If no tasks, check for changes
4. **Commit Changes**: If changes exist and enough time has passed, commit
5. **Sleep**: Small sleep to avoid tight loop
6. **Repeat**: Continue until milestone reached

### Commit Logic

- Checks git status for changes
- Respects `commit_interval_seconds` (won't commit too frequently)
- Generates descriptive commit messages
- Optionally pushes to remote if `auto_push` is enabled
- Tracks commit count against `max_commits` milestone

### Milestone Checking

The agent stops when ANY of these conditions are met:
- `max_commits` reached
- `max_time_hours` elapsed
- `max_tasks` processed

---

## Activity Logging

All activities are logged to:
- **Console**: Real-time logging
- **File**: `autonomous_agent.log`
- **JSON Log**: `autonomous_log_YYYYMMDD_HHMMSS.json`

### Log Format

```json
{
  "agent": "autonomous_agent",
  "settings": {
    "max_commits": 10,
    "max_time_hours": 8.0,
    "max_tasks": 50,
    "commit_interval_seconds": 300,
    "auto_push": false
  },
  "activity_log": [
    {
      "timestamp": "2025-01-06T12:00:00",
      "action": "commit",
      "commit_number": 1,
      "message": "Autonomous commit: 3 modified file(s)..."
    }
  ]
}
```

---

## Safety Features

### Milestone Limits

The agent **always stops** when milestones are reached, preventing:
- Infinite loops
- Excessive commits
- Running too long
- Processing too many tasks

### Commit Interval

Prevents too-frequent commits with `commit_interval_seconds`:
- Default: 300 seconds (5 minutes)
- Ensures reasonable commit frequency
- Prevents commit spam

### Activity Logging

All activities are logged for review:
- See what was committed
- Review task processing
- Check milestone triggers

---

## Integration with Other Agents

The autonomous agent can be integrated with the orchestrator:

```python
from agents.autonomous import AutonomousAgent
from agents.orchestrator import MCPOrchestrator

# Create autonomous agent
autonomous = AutonomousAgent(
    max_commits=10,
    max_time_hours=8.0,
    max_tasks=50
)

# Create orchestrator
orchestrator = MCPOrchestrator()

# Add tasks that use orchestrator
tasks = [
    {
        'type': 'orchestrator_task',
        'action': 'execute',
        'task': {
            'type': 'browser',
            'url': 'https://example.com'
        }
    }
]

# Run autonomous agent with tasks
autonomous.run(tasks=tasks)
```

---

## Best Practices

### Before Running

1. **Review Settings**: Check milestones are reasonable
2. **Check Git Status**: Ensure working tree is clean or ready
3. **Set Branch**: Specify branch if not on main/master
4. **Test First**: Run with small milestones first

### During Run

1. **Monitor Logs**: Check `autonomous_agent.log` periodically
2. **Review Commits**: Check git log to see commits
3. **Check Milestones**: Verify agent stops at milestones

### After Run

1. **Review Activity Log**: Check JSON log file
2. **Review Commits**: `git log` to see what was committed
3. **Verify Changes**: Ensure changes are correct
4. **Push Manually**: If `auto_push` was false, push manually

---

## Troubleshooting

### Issue: Agent doesn't commit

**Possible causes:**
- No changes detected
- Commit interval not elapsed
- Max commits reached

**Solution:**
- Check git status: `git status`
- Check last commit time in logs
- Check milestone status

### Issue: Agent stops immediately

**Possible causes:**
- Milestone already reached
- No tasks in queue
- Git errors

**Solution:**
- Check milestone settings
- Add tasks to queue
- Check git configuration

### Issue: Commits too frequent

**Solution:**
- Increase `commit_interval_seconds`
- Check commit logic in logs

### Issue: Agent runs too long

**Solution:**
- Reduce `max_time_hours`
- Check milestone logic
- Verify time calculation

---

## Example Workflow

### Overnight Development Session

```bash
# 1. Create config for overnight session
cat > overnight_config.json << EOF
{
  "max_commits": 20,
  "max_time_hours": 8.0,
  "max_tasks": 100,
  "commit_interval_seconds": 600,
  "auto_push": false
}
EOF

# 2. Create tasks file
cat > overnight_tasks.json << EOF
[
  {
    "type": "process",
    "action": "process",
    "description": "Process development tasks"
  }
]
EOF

# 3. Run autonomous agent
python run_autonomous.py \
  --config overnight_config.json \
  --tasks overnight_tasks.json

# 4. In the morning, review results
git log --oneline -20
cat autonomous_log_*.json
```

---

## Summary

The Autonomous Agent provides a safe way to work autonomously while you're away:

✅ **Automatic commits** with configurable intervals  
✅ **Milestone-based stopping** for safety  
✅ **Activity logging** for review  
✅ **Task queue processing** for structured work  
✅ **Configurable settings** for different use cases  

**Remember**: Always review commits and logs after the agent runs!




