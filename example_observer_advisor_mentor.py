"""
Example: Using Observer, Advisor, and Mentor Agents

This script demonstrates how to use the new observer, advisor, and mentor
agents for system monitoring, guidance, and learning.

Author: Gematria Hive Team
Date: January 6, 2025
"""

import logging
from agents import (
    ObserverAgent,
    AdvisorAgent,
    MentorAgent,
    NoteTakingSystem,
    get_note_system,
    MCPOrchestrator,
    get_orchestrator
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def example_observer():
    """Example: Using the Observer Agent"""
    print("\n=== Observer Agent Example ===")
    
    # Initialize observer
    observer = ObserverAgent()
    
    # Record some observations
    observer.observe("system_start", {"component": "example"}, "example_script")
    observer.observe("metric", {"metric_name": "cpu_usage", "value": 45.2}, "system")
    
    # Track a mock execution
    from agents.orchestrator import AgentState
    mock_state: AgentState = {
        "task": {"type": "example", "query": "test"},
        "data": [{"test": "data"}],
        "context": {},
        "results": [{"result": "success"}],
        "cost": 0.05,
        "status": "completed",
        "memory_id": None
    }
    
    observer.track_execution("example_agent", mock_state, execution_time=1.5)
    
    # Generate health report
    health_report = observer.generate_health_report()
    print(f"Health Report: {health_report}")
    
    # Save notes
    notes_path = observer.save_notes()
    print(f"Observer notes saved to: {notes_path}")


def example_advisor():
    """Example: Using the Advisor Agent"""
    print("\n=== Advisor Agent Example ===")
    
    # Initialize observer and advisor
    observer = ObserverAgent()
    advisor = AdvisorAgent(observer=observer)
    
    # Analyze and get recommendations
    recommendations = advisor.analyze_and_advise()
    print(f"Recommendations: {len(recommendations)} found")
    for rec in recommendations:
        print(f"  - {rec.get('title')}: {rec.get('recommendation')}")
    
    # Provide guidance on a question
    guidance = advisor.provide_guidance("How can I optimize performance?")
    print(f"\nGuidance on performance:")
    print(f"  Answer: {guidance['answer']}")
    
    # Save notes
    notes_path = advisor.save_notes()
    print(f"\nAdvisor notes saved to: {notes_path}")


def example_mentor():
    """Example: Using the Mentor Agent"""
    print("\n=== Mentor Agent Example ===")
    
    # Initialize observer, advisor, and mentor
    observer = ObserverAgent()
    advisor = AdvisorAgent(observer=observer)
    mentor = MentorAgent(observer=observer, advisor=advisor)
    
    # Identify patterns
    patterns = mentor.identify_patterns()
    print(f"Patterns identified: {len(patterns)}")
    for pattern in patterns:
        print(f"  - {pattern.get('title')}: {pattern.get('description')}")
    
    # Provide learning guidance
    guidance = mentor.provide_learning_guidance("agent architecture")
    print(f"\nLearning Guidance on 'agent architecture':")
    print(f"  Learning Objectives: {guidance['learning_objectives']}")
    print(f"  Best Practices: {guidance['best_practices'][:3]}")
    
    # Record a lesson learned
    lesson = mentor.record_lesson_learned({
        "topic": "Error Handling",
        "content": "Always implement comprehensive error handling with proper logging",
        "category": "best_practices"
    })
    print(f"\nLesson learned recorded: {lesson}")
    
    # Save notes
    notes_path = mentor.save_notes()
    print(f"\nMentor notes saved to: {notes_path}")


def example_note_system():
    """Example: Using the Note-Taking System"""
    print("\n=== Note-Taking System Example ===")
    
    # Get note-taking system
    note_system = get_note_system()
    
    # Take some notes
    note_system.take_note(
        "observation",
        {"content": "System is running smoothly", "metric": "health"},
        tags=["system", "health"],
        category="monitoring"
    )
    
    note_system.take_note(
        "advice",
        {"content": "Consider implementing caching for frequently accessed data"},
        tags=["optimization", "performance"],
        category="recommendation"
    )
    
    note_system.take_note(
        "mentoring",
        {"content": "Learned about agent communication patterns"},
        tags=["learning", "architecture"],
        category="knowledge"
    )
    
    # Search notes
    recent_notes = note_system.get_recent_notes(hours=1)
    print(f"Recent notes: {len(recent_notes)} found")
    
    # Get summary
    summary = note_system.get_note_summary(hours=24)
    print(f"\nNote Summary:")
    print(f"  Total notes: {summary['total_notes']}")
    print(f"  By type: {summary['by_type']}")
    print(f"  Top tags: {list(summary['top_tags'].keys())[:5]}")
    
    # Save summary
    summary_path = note_system.save_summary()
    print(f"\nSummary saved to: {summary_path}")


def example_integrated():
    """Example: Integrated usage with orchestrator"""
    print("\n=== Integrated Example with Orchestrator ===")
    
    # Get orchestrator (which now includes observer, advisor, mentor)
    orchestrator = get_orchestrator()
    
    # The orchestrator automatically has observer, advisor, and mentor
    print(f"Orchestrator has observer: {hasattr(orchestrator, 'observer')}")
    print(f"Orchestrator has advisor: {hasattr(orchestrator, 'advisor')}")
    print(f"Orchestrator has mentor: {hasattr(orchestrator, 'mentor')}")
    
    # Execute a task (observer will automatically track it)
    task = {
        "type": "extraction",
        "source": "example",
        "query": "test query"
    }
    
    print("\nExecuting task (observer will track automatically)...")
    # Note: This would execute the full workflow if agents are properly configured
    # result = orchestrator.execute(task)
    # print(f"Task completed: {result['status']}")
    
    # Get health report from observer
    if orchestrator.observer:
        health = orchestrator.observer.generate_health_report()
        print(f"\nSystem Health:")
        print(f"  Total tasks: {health['total_tasks']}")
        print(f"  Success rate: {health['success_rate']}%")
        print(f"  Total cost: ${health['total_cost']:.4f}")
    
    # Get recommendations from advisor
    if orchestrator.advisor:
        recommendations = orchestrator.advisor.analyze_and_advise()
        print(f"\nRecommendations: {len(recommendations)} found")
        for rec in recommendations[:3]:
            print(f"  - {rec.get('title')}")


if __name__ == "__main__":
    print("Observer, Advisor, and Mentor Agents - Examples")
    print("=" * 60)
    
    try:
        example_observer()
        example_advisor()
        example_mentor()
        example_note_system()
        example_integrated()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("\nNotes are being saved to the ./notes/ directory")
        
    except Exception as e:
        logger.error(f"Error running examples: {e}", exc_info=True)
        print(f"\nError: {e}")




