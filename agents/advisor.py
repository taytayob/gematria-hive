"""
Advisor Agent

Purpose: Provide guidance, recommendations, and strategic advice based on
system observations, metrics, and best practices.

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
    print("Warning: supabase not installed, advisor will use file-based storage")

logger = logging.getLogger(__name__)


class AdvisorAgent:
    """
    Advisor Agent - Provides guidance and recommendations
    
    Operations:
    - Analyze system metrics and observations
    - Provide strategic recommendations
    - Suggest optimizations
    - Offer best practice guidance
    - Maintain advisory notes
    """
    
    def __init__(self, notes_dir: str = None, observer = None):
        """
        Initialize advisor agent
        
        Args:
            notes_dir: Directory for storing advisory notes (default: ./notes/advice)
            observer: Optional observer agent for accessing metrics
        """
        self.name = "advisor_agent"
        self.notes_dir = Path(notes_dir) if notes_dir else Path("./notes/advice")
        self.notes_dir.mkdir(parents=True, exist_ok=True)
        self.observer = observer
        
        # Advisory knowledge base
        self.recommendations = []
        self.advice_history = []
        
        # Supabase for persistent storage
        if HAS_SUPABASE:
            supabase_url = os.getenv('SUPABASE_URL')
            supabase_key = os.getenv('SUPABASE_KEY')
            if supabase_url and supabase_key:
                self.supabase = create_client(supabase_url, supabase_key)
                logger.info("Advisor: Supabase connected for persistent storage")
            else:
                self.supabase = None
        else:
            self.supabase = None
        
        # Initialize MCP tool registry access
        try:
            from agents.mcp_tool_registry import get_tool_registry
            self.tool_registry = get_tool_registry()
            logger.info(f"Agent {self.name} initialized with MCP tool registry access")
        except Exception as e:
            logger.warning(f"Could not initialize MCP tool registry for {self.name}: {e}")
            self.tool_registry = None
        
        # Initialize compliance auditor for compliance-based recommendations
        try:
            from agents.compliance_auditor import get_compliance_auditor
            self.compliance_auditor = get_compliance_auditor()
            logger.info(f"Agent {self.name} initialized with compliance auditor access")
        except Exception as e:
            logger.warning(f"Could not initialize compliance auditor for {self.name}: {e}")
            self.compliance_auditor = None
        
        logger.info(f"Initialized {self.name} with notes directory: {self.notes_dir}")
    
    def analyze_and_advise(self, context: Dict = None) -> List[Dict[str, Any]]:
        """
        Analyze current system state and provide recommendations
        
        Args:
            context: Optional context dictionary
            
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        # Get metrics from observer if available
        if self.observer:
            metrics = self.observer.get_metrics_summary()
            health = self.observer.generate_health_report()
            
            # Analyze success rate
            if health.get("success_rate", 100) < 80:
                recommendations.append({
                    "type": "performance",
                    "priority": "high",
                    "title": "Low Success Rate Detected",
                    "description": f"Success rate is {health['success_rate']:.1f}%, below optimal threshold of 80%",
                    "recommendation": "Review failed tasks and error logs. Consider improving error handling and retry logic.",
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            # Analyze cost
            total_cost = metrics.get("total_cost", 0.0)
            if total_cost > 100.0:  # Threshold for cost concern
                recommendations.append({
                    "type": "cost",
                    "priority": "medium",
                    "title": "High Cumulative Cost",
                    "description": f"Total cost has reached ${total_cost:.2f}",
                    "recommendation": "Review cost optimization strategies. Consider caching, batching, or using cheaper models where appropriate.",
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            # Analyze execution time
            avg_time = health.get("average_execution_time", 0.0)
            if avg_time > 60.0:  # More than 60 seconds average
                recommendations.append({
                    "type": "performance",
                    "priority": "medium",
                    "title": "Slow Execution Times",
                    "description": f"Average execution time is {avg_time:.1f} seconds",
                    "recommendation": "Optimize agent workflows. Consider parallel processing, caching, or reducing unnecessary operations.",
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            # Analyze agent-specific performance
            agent_perf = health.get("agent_performance", {})
            for agent_name, perf in agent_perf.items():
                if perf.get("success_rate", 100) < 70:
                    recommendations.append({
                        "type": "agent_specific",
                        "priority": "high",
                        "title": f"{agent_name} Performance Issues",
                        "description": f"{agent_name} has success rate of {perf['success_rate']:.1f}%",
                        "recommendation": f"Review {agent_name} implementation. Check for error handling, input validation, and edge cases.",
                        "timestamp": datetime.utcnow().isoformat()
                    })
        
        # Add context-specific recommendations
        if context:
            if context.get("high_error_rate"):
                recommendations.append({
                    "type": "error_handling",
                    "priority": "high",
                    "title": "Error Handling Improvement Needed",
                    "description": "High error rate detected in recent operations",
                    "recommendation": "Implement comprehensive error handling, logging, and retry mechanisms.",
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            if context.get("resource_constraints"):
                recommendations.append({
                    "type": "resource",
                    "priority": "medium",
                    "title": "Resource Optimization Recommended",
                    "description": "Resource constraints detected",
                    "recommendation": "Review resource usage patterns. Consider implementing rate limiting, batching, or resource pooling.",
                    "timestamp": datetime.utcnow().isoformat()
                })
        
        # Add compliance-based recommendations
        if self.compliance_auditor:
            try:
                compliance_report = self.compliance_auditor.generate_compliance_report(days=7)
                
                # Check average compliance score
                avg_score = compliance_report.get("average_compliance_score", 1.0)
                if avg_score < 0.7:
                    recommendations.append({
                        "type": "compliance",
                        "priority": "high",
                        "title": "Low Compliance Score Detected",
                        "description": f"Average compliance score is {avg_score:.2f}, below threshold of 0.7",
                        "recommendation": "Review planned vs actual execution. Improve planning process to better match actual execution.",
                        "timestamp": datetime.utcnow().isoformat()
                    })
                
                # Check for common violations
                violations = compliance_report.get("violations", {})
                violation_types = violations.get("by_type", {})
                
                if violation_types.get("missing_tools", 0) > compliance_report.get("total_tasks", 0) * 0.3:
                    recommendations.append({
                        "type": "compliance",
                        "priority": "medium",
                        "title": "Frequently Missing Planned Tools",
                        "description": f"Missing tools in {violation_types.get('missing_tools', 0)} cases",
                        "recommendation": "Review tool selection process. Consider improving tool planning or tool availability.",
                        "timestamp": datetime.utcnow().isoformat()
                    })
                
                if violation_types.get("missing_agents", 0) > compliance_report.get("total_tasks", 0) * 0.3:
                    recommendations.append({
                        "type": "compliance",
                        "priority": "medium",
                        "title": "Frequently Missing Planned Agents",
                        "description": f"Missing agents in {violation_types.get('missing_agents', 0)} cases",
                        "recommendation": "Review agent selection process. Consider improving agent planning or agent availability.",
                        "timestamp": datetime.utcnow().isoformat()
                    })
            except Exception as e:
                logger.warning(f"Error generating compliance-based recommendations: {e}")
        
        # Save recommendations
        for rec in recommendations:
            self.record_advice(rec)
        
        return recommendations
    
    def provide_guidance(self, question: str, context: Dict = None) -> Dict[str, Any]:
        """
        Provide guidance on a specific question
        
        Args:
            question: Question or topic for guidance
            context: Optional context dictionary
            
        Returns:
            Guidance dictionary with answer and recommendations
        """
        guidance = {
            "question": question,
            "timestamp": datetime.utcnow().isoformat(),
            "answer": "",
            "recommendations": [],
            "related_advice": []
        }
        
        # Simple rule-based guidance (can be enhanced with LLM)
        question_lower = question.lower()
        
        if "cost" in question_lower or "expensive" in question_lower:
            guidance["answer"] = "Cost optimization strategies: 1) Use caching for repeated operations, 2) Batch similar requests, 3) Use cheaper models for simple tasks, 4) Monitor and log all costs, 5) Set cost thresholds and alerts."
            guidance["recommendations"].append({
                "action": "Implement cost tracking",
                "priority": "high"
            })
        
        elif "performance" in question_lower or "slow" in question_lower:
            guidance["answer"] = "Performance optimization strategies: 1) Profile agent execution times, 2) Implement parallel processing where possible, 3) Cache frequently accessed data, 4) Optimize database queries, 5) Review and optimize agent workflows."
            guidance["recommendations"].append({
                "action": "Profile system performance",
                "priority": "medium"
            })
        
        elif "error" in question_lower or "failure" in question_lower:
            guidance["answer"] = "Error handling best practices: 1) Implement comprehensive try-catch blocks, 2) Log all errors with context, 3) Implement retry logic with exponential backoff, 4) Validate inputs before processing, 5) Provide meaningful error messages."
            guidance["recommendations"].append({
                "action": "Review error logs and improve error handling",
                "priority": "high"
            })
        
        elif "architecture" in question_lower or "design" in question_lower:
            guidance["answer"] = "Architecture recommendations: 1) Follow agent separation of concerns, 2) Use state machine for workflow orchestration, 3) Implement proper logging and observability, 4) Design for scalability and maintainability, 5) Document all design decisions."
            guidance["recommendations"].append({
                "action": "Review architecture documentation",
                "priority": "medium"
            })
        
        else:
            guidance["answer"] = "General guidance: Focus on observability, maintainability, and following best practices. Monitor system health regularly and iterate based on observations."
        
        # Get related advice from history
        if self.advice_history:
            guidance["related_advice"] = self.advice_history[-5:]
        
        # Save guidance
        self.record_advice(guidance)
        
        return guidance
    
    def record_advice(self, advice: Dict[str, Any]) -> str:
        """
        Record an advice or recommendation
        
        Args:
            advice: Advice dictionary
            
        Returns:
            Advice ID
        """
        advice_id = f"adv_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        advice["id"] = advice_id
        
        if "timestamp" not in advice:
            advice["timestamp"] = datetime.utcnow().isoformat()
        
        self.advice_history.append(advice)
        self.recommendations.append(advice)
        
        # Save to file
        self._save_advice(advice)
        
        # Save to Supabase if available
        if self.supabase:
            try:
                self.supabase.table("advice").insert({
                    "advice_id": advice_id,
                    "timestamp": advice["timestamp"],
                    "type": advice.get("type", "general"),
                    "priority": advice.get("priority", "medium"),
                    "title": advice.get("title", ""),
                    "content": json.dumps(advice)
                }).execute()
            except Exception as e:
                logger.error(f"Error saving advice to Supabase: {e}")
        
        logger.debug(f"Advice recorded: {advice.get('title', advice_id)}")
        return advice_id
    
    def _save_advice(self, advice: Dict) -> None:
        """Save advice to file"""
        date_str = datetime.now().strftime("%Y%m%d")
        filepath = self.notes_dir / f"advice_{date_str}.jsonl"
        
        with open(filepath, 'a') as f:
            f.write(json.dumps(advice) + '\n')
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute advisor task
        
        Args:
            state: Agent state
            
        Returns:
            Updated state with advice and recommendations
        """
        task = state.get("task", {})
        task_type = task.get("type", "analyze")
        
        logger.info(f"Advisor agent: {task_type}")
        
        if task_type == "analyze":
            # Analyze and provide recommendations
            recommendations = self.analyze_and_advise(state.get("context", {}))
            state["results"].append({
                "agent": self.name,
                "action": "analyze",
                "recommendations": recommendations
            })
        
        elif task_type == "guidance":
            # Provide guidance on a question
            question = task.get("question", "")
            guidance = self.provide_guidance(question, state.get("context", {}))
            state["results"].append({
                "agent": self.name,
                "action": "guidance",
                "guidance": guidance
            })
        
        elif task_type == "recommendations":
            # Get recent recommendations
            recent_recs = self.get_recent_recommendations(hours=24)
            state["results"].append({
                "agent": self.name,
                "action": "recommendations",
                "recommendations": recent_recs
            })
        
        return state
    
    def get_recent_recommendations(self, hours: int = 24, limit: int = 50) -> List[Dict]:
        """
        Get recent recommendations
        
        Args:
            hours: Number of hours to look back
            limit: Maximum number of recommendations to return
            
        Returns:
            List of recommendation dictionaries
        """
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        
        recent = [
            rec for rec in self.recommendations
            if datetime.fromisoformat(rec.get("timestamp", datetime.utcnow().isoformat())) >= cutoff
        ]
        
        return recent[-limit:]
    
    def save_notes(self, filepath: str = None) -> str:
        """
        Save all advice to a file
        
        Args:
            filepath: Optional filepath (default: notes/advice_summary_YYYYMMDD.json)
            
        Returns:
            Path to saved file
        """
        if not filepath:
            date_str = datetime.now().strftime("%Y%m%d")
            filepath = self.notes_dir / f"advice_summary_{date_str}.json"
        
        notes_data = {
            "generated_at": datetime.utcnow().isoformat(),
            "total_recommendations": len(self.recommendations),
            "recent_recommendations": self.get_recent_recommendations(hours=168),  # Last week
            "advice_history": self.advice_history[-100:]  # Last 100 items
        }
        
        with open(filepath, 'w') as f:
            json.dump(notes_data, f, indent=2)
        
        logger.info(f"Advisor notes saved to: {filepath}")
        return str(filepath)

