"""
Mentor Agent

Purpose: Provide learning guidance, improvement suggestions, and knowledge
transfer based on system patterns, best practices, and historical performance.

Author: Gematria Hive Team
Date: January 6, 2025
"""

import logging
import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path
from agents.orchestrator import AgentState
from dotenv import load_dotenv

load_dotenv()

try:
    from supabase import create_client, Client
    HAS_SUPABASE = True
except ImportError:
    HAS_SUPABASE = False
    print("Warning: supabase not installed, mentor will use file-based storage")

logger = logging.getLogger(__name__)


class MentorAgent:
    """
    Mentor Agent - Provides learning and improvement guidance
    
    Operations:
    - Analyze patterns and trends
    - Provide learning recommendations
    - Suggest improvements based on historical data
    - Maintain mentoring notes and lessons learned
    - Track knowledge transfer
    """
    
    def __init__(self, notes_dir: str = None, observer = None, 
                 advisor = None):
        """
        Initialize mentor agent
        
        Args:
            notes_dir: Directory for storing mentoring notes (default: ./notes/mentoring)
            observer: Optional observer agent for accessing metrics
            advisor: Optional advisor agent for accessing recommendations
        """
        self.name = "mentor_agent"
        self.notes_dir = Path(notes_dir) if notes_dir else Path("./notes/mentoring")
        self.notes_dir.mkdir(parents=True, exist_ok=True)
        self.observer = observer
        self.advisor = advisor
        
        # Mentoring knowledge base
        self.lessons_learned = []
        self.improvement_suggestions = []
        self.mentoring_notes = []
        self.patterns = []
        
        # Supabase for persistent storage
        if HAS_SUPABASE:
            supabase_url = os.getenv('SUPABASE_URL')
            supabase_key = os.getenv('SUPABASE_KEY')
            if supabase_url and supabase_key:
                self.supabase = create_client(supabase_url, supabase_key)
                logger.info("Mentor: Supabase connected for persistent storage")
            else:
                self.supabase = None
        else:
            self.supabase = None
        
        logger.info(f"Initialized {self.name} with notes directory: {self.notes_dir}")
    
    def identify_patterns(self, observations: List[Dict] = None) -> List[Dict[str, Any]]:
        """
        Identify patterns from observations and metrics
        
        Args:
            observations: Optional list of observations (uses observer if available)
            
        Returns:
            List of identified patterns
        """
        patterns = []
        
        # Get observations from observer if available
        if not observations and self.observer:
            observations = self.observer.get_recent_observations(hours=168)  # Last week
        
        if not observations:
            return patterns
        
        # Analyze error patterns
        error_events = [obs for obs in observations if obs.get("event_type") == "error"]
        if error_events:
            error_agents = {}
            for event in error_events:
                agent = event.get("agent_name", "unknown")
                error_agents[agent] = error_agents.get(agent, 0) + 1
            
            if error_agents:
                most_errors = max(error_agents.items(), key=lambda x: x[1])
                patterns.append({
                    "type": "error_pattern",
                    "title": f"Error Pattern: {most_errors[0]}",
                    "description": f"{most_errors[0]} has {most_errors[1]} errors in recent observations",
                    "recommendation": f"Focus improvement efforts on {most_errors[0]}. Review error logs and implement better error handling.",
                    "timestamp": datetime.utcnow().isoformat(),
                    "severity": "high" if most_errors[1] > 10 else "medium"
                })
        
        # Analyze performance patterns
        execution_events = [obs for obs in observations if obs.get("event_type") == "execution_complete"]
        if execution_events:
            execution_times = []
            for event in execution_events:
                exec_time = event.get("data", {}).get("execution_time")
                if exec_time:
                    execution_times.append(exec_time)
            
            if execution_times:
                avg_time = sum(execution_times) / len(execution_times)
                max_time = max(execution_times)
                
                if max_time > avg_time * 2:
                    patterns.append({
                        "type": "performance_pattern",
                        "title": "Performance Variability Detected",
                        "description": f"Execution times vary significantly (avg: {avg_time:.1f}s, max: {max_time:.1f}s)",
                        "recommendation": "Investigate causes of performance variability. Consider caching, optimization, or parallel processing.",
                        "timestamp": datetime.utcnow().isoformat(),
                        "severity": "medium"
                    })
        
        # Analyze cost patterns
        cost_events = [obs for obs in observations if obs.get("event_type") == "execution_complete"]
        if cost_events:
            costs = [event.get("data", {}).get("cost", 0) for event in cost_events]
            total_cost = sum(costs)
            avg_cost = total_cost / len(costs) if costs else 0
            
            if avg_cost > 0.1:  # High average cost per execution
                patterns.append({
                    "type": "cost_pattern",
                    "title": "High Cost Pattern Detected",
                    "description": f"Average cost per execution is ${avg_cost:.4f}",
                    "recommendation": "Review cost optimization strategies. Consider using cheaper models or caching results.",
                    "timestamp": datetime.utcnow().isoformat(),
                    "severity": "medium"
                })
        
        # Save patterns
        for pattern in patterns:
            self.record_pattern(pattern)
        
        return patterns
    
    def provide_learning_guidance(self, topic: str, context: Dict = None) -> Dict[str, Any]:
        """
        Provide learning guidance on a specific topic
        
        Args:
            topic: Topic to learn about
            context: Optional context dictionary
            
        Returns:
            Learning guidance dictionary
        """
        guidance = {
            "topic": topic,
            "timestamp": datetime.utcnow().isoformat(),
            "learning_objectives": [],
            "key_concepts": [],
            "best_practices": [],
            "common_pitfalls": [],
            "improvement_suggestions": [],
            "related_lessons": []
        }
        
        topic_lower = topic.lower()
        
        # Agent-specific learning guidance
        if "agent" in topic_lower:
            guidance["learning_objectives"] = [
                "Understand agent architecture and responsibilities",
                "Learn agent communication patterns",
                "Master state management in agent workflows"
            ]
            guidance["key_concepts"] = [
                "Agent separation of concerns",
                "State machine orchestration",
                "Error handling and recovery",
                "Cost and performance optimization"
            ]
            guidance["best_practices"] = [
                "Keep agents focused on single responsibilities",
                "Implement comprehensive error handling",
                "Log all important events",
                "Monitor performance and costs",
                "Document agent behavior and interfaces"
            ]
            guidance["common_pitfalls"] = [
                "Tight coupling between agents",
                "Insufficient error handling",
                "Lack of observability",
                "Ignoring cost implications",
                "Poor state management"
            ]
        
        # System architecture learning
        elif "architecture" in topic_lower or "system" in topic_lower:
            guidance["learning_objectives"] = [
                "Understand system architecture",
                "Learn workflow orchestration",
                "Master data flow patterns"
            ]
            guidance["key_concepts"] = [
                "MCP (Model Context Protocol) patterns",
                "State machine design",
                "Data triangulation and unification",
                "Observability and monitoring"
            ]
            guidance["best_practices"] = [
                "Design for scalability",
                "Implement comprehensive logging",
                "Use state machines for workflows",
                "Separate concerns properly",
                "Plan for failure and recovery"
            ]
        
        # Performance optimization learning
        elif "performance" in topic_lower or "optimization" in topic_lower:
            guidance["learning_objectives"] = [
                "Identify performance bottlenecks",
                "Learn optimization techniques",
                "Master profiling and monitoring"
            ]
            guidance["key_concepts"] = [
                "Execution time analysis",
                "Caching strategies",
                "Parallel processing",
                "Resource optimization"
            ]
            guidance["best_practices"] = [
                "Profile before optimizing",
                "Cache frequently accessed data",
                "Use parallel processing where possible",
                "Monitor resource usage",
                "Set performance targets"
            ]
        
        # Get related lessons learned
        related_lessons = [
            lesson for lesson in self.lessons_learned
            if topic_lower in lesson.get("topic", "").lower() or
               any(keyword in lesson.get("content", "").lower() 
                   for keyword in topic_lower.split())
        ]
        guidance["related_lessons"] = related_lessons[-5:]  # Last 5 related
        
        # Get improvement suggestions from advisor
        if self.advisor:
            recent_recs = self.advisor.get_recent_recommendations(hours=168)
            guidance["improvement_suggestions"] = recent_recs[:5]
        
        # Save guidance
        self.record_mentoring_note(guidance)
        
        return guidance
    
    def record_lesson_learned(self, lesson: Dict[str, Any]) -> str:
        """
        Record a lesson learned
        
        Args:
            lesson: Lesson dictionary with topic, content, etc.
            
        Returns:
            Lesson ID
        """
        lesson_id = f"lesson_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        lesson["id"] = lesson_id
        
        if "timestamp" not in lesson:
            lesson["timestamp"] = datetime.utcnow().isoformat()
        
        self.lessons_learned.append(lesson)
        
        # Save to file
        self._save_lesson(lesson)
        
        # Save to Supabase if available
        if self.supabase:
            try:
                self.supabase.table("lessons_learned").insert({
                    "lesson_id": lesson_id,
                    "timestamp": lesson["timestamp"],
                    "topic": lesson.get("topic", ""),
                    "content": json.dumps(lesson)
                }).execute()
            except Exception as e:
                logger.error(f"Error saving lesson to Supabase: {e}")
        
        logger.info(f"Lesson learned recorded: {lesson.get('topic', lesson_id)}")
        return lesson_id
    
    def record_pattern(self, pattern: Dict[str, Any]) -> str:
        """
        Record an identified pattern
        
        Args:
            pattern: Pattern dictionary
            
        Returns:
            Pattern ID
        """
        pattern_id = f"pattern_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        pattern["id"] = pattern_id
        
        if "timestamp" not in pattern:
            pattern["timestamp"] = datetime.utcnow().isoformat()
        
        self.patterns.append(pattern)
        
        # Save to file
        self._save_pattern(pattern)
        
        logger.debug(f"Pattern recorded: {pattern.get('title', pattern_id)}")
        return pattern_id
    
    def record_mentoring_note(self, note: Dict[str, Any]) -> str:
        """
        Record a mentoring note
        
        Args:
            note: Note dictionary
            
        Returns:
            Note ID
        """
        note_id = f"mentor_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        note["id"] = note_id
        
        if "timestamp" not in note:
            note["timestamp"] = datetime.utcnow().isoformat()
        
        self.mentoring_notes.append(note)
        
        # Save to file
        self._save_mentoring_note(note)
        
        logger.debug(f"Mentoring note recorded: {note.get('topic', note_id)}")
        return note_id
    
    def _save_lesson(self, lesson: Dict) -> None:
        """Save lesson to file"""
        date_str = datetime.now().strftime("%Y%m%d")
        filepath = self.notes_dir / f"lessons_{date_str}.jsonl"
        
        with open(filepath, 'a') as f:
            f.write(json.dumps(lesson) + '\n')
    
    def _save_pattern(self, pattern: Dict) -> None:
        """Save pattern to file"""
        date_str = datetime.now().strftime("%Y%m%d")
        filepath = self.notes_dir / f"patterns_{date_str}.jsonl"
        
        with open(filepath, 'a') as f:
            f.write(json.dumps(pattern) + '\n')
    
    def _save_mentoring_note(self, note: Dict) -> None:
        """Save mentoring note to file"""
        date_str = datetime.now().strftime("%Y%m%d")
        filepath = self.notes_dir / f"mentoring_{date_str}.jsonl"
        
        with open(filepath, 'a') as f:
            f.write(json.dumps(note) + '\n')
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute mentor task
        
        Args:
            state: Agent state
            
        Returns:
            Updated state with mentoring guidance
        """
        task = state.get("task", {})
        task_type = task.get("type", "analyze")
        
        logger.info(f"Mentor agent: {task_type}")
        
        if task_type == "identify_patterns":
            # Identify patterns from observations
            patterns = self.identify_patterns()
            state["results"].append({
                "agent": self.name,
                "action": "identify_patterns",
                "patterns": patterns
            })
        
        elif task_type == "learning_guidance":
            # Provide learning guidance
            topic = task.get("topic", "")
            guidance = self.provide_learning_guidance(topic, state.get("context", {}))
            state["results"].append({
                "agent": self.name,
                "action": "learning_guidance",
                "guidance": guidance
            })
        
        elif task_type == "lessons":
            # Get lessons learned
            recent_lessons = self.get_recent_lessons(hours=168)
            state["results"].append({
                "agent": self.name,
                "action": "lessons",
                "lessons": recent_lessons
            })
        
        return state
    
    def get_recent_lessons(self, hours: int = 168, limit: int = 50) -> List[Dict]:
        """
        Get recent lessons learned
        
        Args:
            hours: Number of hours to look back
            limit: Maximum number of lessons to return
            
        Returns:
            List of lesson dictionaries
        """
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        
        recent = [
            lesson for lesson in self.lessons_learned
            if datetime.fromisoformat(lesson.get("timestamp", datetime.utcnow().isoformat())) >= cutoff
        ]
        
        return recent[-limit:]
    
    def save_notes(self, filepath: str = None) -> str:
        """
        Save all mentoring notes to a file
        
        Args:
            filepath: Optional filepath (default: notes/mentoring_summary_YYYYMMDD.json)
            
        Returns:
            Path to saved file
        """
        if not filepath:
            date_str = datetime.now().strftime("%Y%m%d")
            filepath = self.notes_dir / f"mentoring_summary_{date_str}.json"
        
        notes_data = {
            "generated_at": datetime.utcnow().isoformat(),
            "total_lessons": len(self.lessons_learned),
            "total_patterns": len(self.patterns),
            "recent_lessons": self.get_recent_lessons(hours=168),
            "recent_patterns": [
                p for p in self.patterns
                if datetime.fromisoformat(p.get("timestamp", datetime.utcnow().isoformat())) >= 
                   (datetime.utcnow() - timedelta(hours=168))
            ][-50:],
            "mentoring_notes": self.mentoring_notes[-100:]
        }
        
        with open(filepath, 'w') as f:
            json.dump(notes_data, f, indent=2)
        
        logger.info(f"Mentor notes saved to: {filepath}")
        return str(filepath)

