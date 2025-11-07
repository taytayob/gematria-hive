# Observer, Advisor, and Mentor Agents

This document describes the Observer, Advisor, and Mentor agents that are part of the Gematria Hive agent system.

## Overview

Three new agents have been added to provide system monitoring, guidance, and learning capabilities:

1. **Observer Agent** - Monitors system activity, tracks metrics, and maintains observational notes
2. **Advisor Agent** - Provides guidance, recommendations, and strategic advice
3. **Mentor Agent** - Offers learning guidance, improvement suggestions, and knowledge transfer

All agents are integrated with a centralized **Note-Taking System** for unified note management.

## Observer Agent

The Observer Agent monitors and tracks system activity.

### Features

- **Event Observation**: Records system events (execution_start, execution_end, errors, metrics)
- **Performance Tracking**: Tracks agent executions, costs, success rates, and execution times
- **Health Reporting**: Generates system health reports with metrics and statistics
- **Note Storage**: Saves observations to files and optionally to Supabase

### Usage

```python
from agents import ObserverAgent

# Initialize observer
observer = ObserverAgent()

# Record an observation
observer.observe("system_start", {"component": "example"}, "agent_name")

# Track an execution
observer.track_execution("agent_name", state, execution_time=1.5)

# Record an error
observer.record_error("agent_name", exception, context={})

# Generate health report
health_report = observer.generate_health_report()

# Save notes
observer.save_notes()
```

### Integration

The Observer Agent is automatically initialized in the Orchestrator and tracks all workflow executions.

## Advisor Agent

The Advisor Agent provides guidance and recommendations based on system observations.

### Features

- **System Analysis**: Analyzes metrics and observations to identify issues
- **Recommendations**: Provides actionable recommendations for optimization
- **Guidance**: Answers questions and provides best practice guidance
- **Strategic Advice**: Offers strategic advice based on system state

### Usage

```python
from agents import ObserverAgent, AdvisorAgent

# Initialize with observer
observer = ObserverAgent()
advisor = AdvisorAgent(observer=observer)

# Analyze and get recommendations
recommendations = advisor.analyze_and_advise()

# Provide guidance on a question
guidance = advisor.provide_guidance("How can I optimize performance?")

# Save notes
advisor.save_notes()
```

### Recommendation Types

- **Performance**: Success rate, execution time issues
- **Cost**: High cumulative costs, cost optimization
- **Error Handling**: Error patterns, error handling improvements
- **Agent-Specific**: Individual agent performance issues

## Mentor Agent

The Mentor Agent provides learning guidance and improvement suggestions.

### Features

- **Pattern Identification**: Identifies patterns from observations (errors, performance, costs)
- **Learning Guidance**: Provides structured learning guidance on topics
- **Lessons Learned**: Records and retrieves lessons learned
- **Improvement Suggestions**: Suggests improvements based on historical data

### Usage

```python
from agents import ObserverAgent, AdvisorAgent, MentorAgent

# Initialize with observer and advisor
observer = ObserverAgent()
advisor = AdvisorAgent(observer=observer)
mentor = MentorAgent(observer=observer, advisor=advisor)

# Identify patterns
patterns = mentor.identify_patterns()

# Provide learning guidance
guidance = mentor.provide_learning_guidance("agent architecture")

# Record a lesson learned
lesson_id = mentor.record_lesson_learned({
    "topic": "Error Handling",
    "content": "Always implement comprehensive error handling",
    "category": "best_practices"
})

# Save notes
mentor.save_notes()
```

### Learning Guidance Topics

- Agent architecture and design
- System architecture
- Performance optimization
- Error handling
- Best practices

## Note-Taking System

The Note-Taking System provides a unified interface for all note-taking activities.

### Features

- **Unified Interface**: Single interface for all note types
- **Search**: Search notes by query, type, tags, category, or date
- **Categorization**: Organize notes by type and category
- **Summarization**: Generate summaries of notes

### Usage

```python
from agents import get_note_system

# Get note-taking system
note_system = get_note_system()

# Take a note
note_id = note_system.take_note(
    "observation",
    {"content": "System is running smoothly"},
    tags=["system", "health"],
    category="monitoring"
)

# Search notes
notes = note_system.search_notes(
    query="performance",
    note_type="advice",
    tags=["optimization"]
)

# Get recent notes
recent = note_system.get_recent_notes(hours=24)

# Get summary
summary = note_system.get_note_summary(hours=168)

# Save summary
note_system.save_summary()
```

### Note Types

- **observation**: System observations and events
- **advice**: Recommendations and guidance
- **mentoring**: Learning guidance and lessons
- **general**: General notes

## Integration with Orchestrator

All three agents are automatically initialized in the Orchestrator:

```python
from agents import get_orchestrator

orchestrator = get_orchestrator()

# Access agents
observer = orchestrator.observer
advisor = orchestrator.advisor
mentor = orchestrator.mentor

# Observer automatically tracks all workflow executions
# Advisor and Mentor can be used for analysis and guidance
```

## File Structure

Notes are saved in the following directory structure:

```
./notes/
├── observations/
│   ├── observations_YYYYMMDD.jsonl
│   └── observations_summary_YYYYMMDD.json
├── advice/
│   ├── advice_YYYYMMDD.jsonl
│   └── advice_summary_YYYYMMDD.json
├── mentoring/
│   ├── lessons_YYYYMMDD.jsonl
│   ├── patterns_YYYYMMDD.jsonl
│   ├── mentoring_YYYYMMDD.jsonl
│   └── mentoring_summary_YYYYMMDD.json
├── general/
│   └── notes_YYYYMMDD.jsonl
└── summary_YYYYMMDD.json
```

## Database Integration

If Supabase is configured, notes are also saved to the database:

- `observations` table: Observation records
- `advice` table: Advice and recommendations
- `lessons_learned` table: Lessons learned
- `notes` table: General notes

## Example

See `example_observer_advisor_mentor.py` for complete examples of using all three agents.

## Best Practices

1. **Use Observer for Monitoring**: Always use the Observer Agent to track system activity
2. **Regular Analysis**: Periodically use the Advisor Agent to analyze system health
3. **Learn from Patterns**: Use the Mentor Agent to identify patterns and learn from them
4. **Take Notes**: Use the Note-Taking System to document important observations and decisions
5. **Review Summaries**: Regularly review note summaries to track system evolution

## Future Enhancements

- LLM integration for more intelligent recommendations
- Automated pattern detection and alerting
- Integration with external monitoring tools
- Advanced analytics and visualization
- Knowledge graph construction from notes




