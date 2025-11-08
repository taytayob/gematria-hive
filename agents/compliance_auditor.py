"""
Compliance Auditor - Planned vs Actual Execution Tracking

Purpose: Audits planned vs. actual execution, tracks missing parameters/tools/agents,
generates compliance reports, creates feedback loop for improvements, detects anomalies,
and tracks fibonacci/attention patterns.

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ComplianceAuditor:
    """
    Compliance Auditor - Tracks planned vs actual execution
    
    Operations:
    - Audits planned vs. actual execution
    - Tracks missing parameters, tools, agents
    - Generates compliance reports
    - Creates feedback loop for improvements
    - Detects anomalies (unknown unknowns)
    - Tracks fibonacci/attention patterns
    """
    
    def __init__(self, logs_dir: str = None):
        """
        Initialize compliance auditor
        
        Args:
            logs_dir: Directory for compliance logs
        """
        self.logs_dir = Path(logs_dir) if logs_dir else Path("./logs/compliance")
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Compliance tracking
        self.compliance_records = []
        self.violations = []
        self.patterns = []
        
        logger.info("Compliance Auditor initialized")
    
    def audit_execution(self, planned: Dict, actual: Dict, task_id: str = None) -> Dict:
        """
        Audit planned vs actual execution
        
        Args:
            planned: Planned execution dictionary
            actual: Actual execution dictionary
            task_id: Optional task ID
            
        Returns:
            Compliance audit result
        """
        audit_result = {
            "task_id": task_id or f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.utcnow().isoformat(),
            "compliant": True,
            "violations": [],
            "missing_items": {
                "tools": [],
                "agents": [],
                "parameters": []
            },
            "compliance_score": 1.0,
            "suggestions": []
        }
        
        # Check planned vs actual tools
        planned_tools = planned.get("tools", [])
        actual_tools = actual.get("tools_used", [])
        missing_tools = [tool for tool in planned_tools if tool not in actual_tools]
        
        if missing_tools:
            audit_result["violations"].append({
                "type": "missing_tools",
                "severity": "warning",
                "items": missing_tools,
                "message": f"Planned tools not used: {missing_tools}"
            })
            audit_result["missing_items"]["tools"] = missing_tools
            audit_result["compliance_score"] -= 0.1 * len(missing_tools)
        
        # Check planned vs actual agents
        planned_agents = planned.get("agents", [])
        actual_agents = actual.get("agents_used", [])
        missing_agents = [agent for agent in planned_agents if agent not in actual_agents]
        
        if missing_agents:
            audit_result["violations"].append({
                "type": "missing_agents",
                "severity": "warning",
                "items": missing_agents,
                "message": f"Planned agents not used: {missing_agents}"
            })
            audit_result["missing_items"]["agents"] = missing_agents
            audit_result["compliance_score"] -= 0.1 * len(missing_agents)
        
        # Check planned vs actual parameters
        planned_params = planned.get("parameters", {})
        actual_params = actual.get("parameters", {})
        missing_params = [param for param in planned_params.keys() if param not in actual_params]
        
        if missing_params:
            audit_result["violations"].append({
                "type": "missing_parameters",
                "severity": "info",
                "items": missing_params,
                "message": f"Planned parameters not used: {missing_params}"
            })
            audit_result["missing_items"]["parameters"] = missing_params
            audit_result["compliance_score"] -= 0.05 * len(missing_params)
        
        # Check for unexpected tools/agents (anomalies)
        unexpected_tools = [tool for tool in actual_tools if tool not in planned_tools]
        unexpected_agents = [agent for agent in actual_agents if agent not in planned_agents]
        
        if unexpected_tools or unexpected_agents:
            audit_result["violations"].append({
                "type": "unexpected_items",
                "severity": "info",
                "items": {
                    "tools": unexpected_tools,
                    "agents": unexpected_agents
                },
                "message": f"Unexpected items used (may indicate adaptation): tools={unexpected_tools}, agents={unexpected_agents}"
            })
            # Anomaly detection - unknown unknowns
            self._detect_anomaly(audit_result["task_id"], {
                "unexpected_tools": unexpected_tools,
                "unexpected_agents": unexpected_agents
            })
        
        # Ensure compliance score is between 0 and 1
        audit_result["compliance_score"] = max(0.0, min(1.0, audit_result["compliance_score"]))
        
        # Generate suggestions
        audit_result["suggestions"] = self._generate_suggestions(audit_result)
        
        # Record compliance
        self.compliance_records.append(audit_result)
        self._save_compliance_record(audit_result)
        
        # Track violations
        if audit_result["violations"]:
            self.violations.extend(audit_result["violations"])
        
        logger.info(f"Compliance audit completed for {audit_result['task_id']}: score={audit_result['compliance_score']:.2f}")
        
        return audit_result
    
    def _detect_anomaly(self, task_id: str, anomaly_data: Dict):
        """
        Detect anomaly (unknown unknowns)
        
        Args:
            task_id: Task ID
            anomaly_data: Anomaly data dictionary
        """
        anomaly = {
            "task_id": task_id,
            "timestamp": datetime.utcnow().isoformat(),
            "type": "unknown_unknown",
            "data": anomaly_data,
            "description": "Unexpected items detected - may indicate unknown unknowns"
        }
        
        self.patterns.append(anomaly)
        logger.warning(f"Anomaly detected in task {task_id}: {anomaly_data}")
    
    def _generate_suggestions(self, audit_result: Dict) -> List[str]:
        """Generate suggestions based on compliance audit"""
        suggestions = []
        
        # Suggest missing tools
        if audit_result["missing_items"]["tools"]:
            suggestions.append(f"Consider using planned tools: {', '.join(audit_result['missing_items']['tools'])}")
        
        # Suggest missing agents
        if audit_result["missing_items"]["agents"]:
            suggestions.append(f"Consider using planned agents: {', '.join(audit_result['missing_items']['agents'])}")
        
        # Suggest documentation
        if audit_result["compliance_score"] < 0.8:
            suggestions.append("Consider improving documentation of planned vs actual execution")
        
        # Suggest feedback loop
        if audit_result["violations"]:
            suggestions.append("Review violations and update planning process to improve compliance")
        
        return suggestions
    
    def _save_compliance_record(self, record: Dict):
        """Save compliance record to file"""
        date_str = datetime.now().strftime("%Y%m%d")
        filepath = self.logs_dir / f"compliance_{date_str}.jsonl"
        
        try:
            with open(filepath, 'a') as f:
                f.write(json.dumps(record) + '\n')
        except Exception as e:
            logger.error(f"Error saving compliance record: {e}")
    
    def generate_compliance_report(self, days: int = 7) -> Dict:
        """
        Generate compliance report
        
        Args:
            days: Number of days to include in report
            
        Returns:
            Compliance report dictionary
        """
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        recent_records = [
            record for record in self.compliance_records
            if datetime.fromisoformat(record["timestamp"]) >= cutoff
        ]
        
        if not recent_records:
            return {
                "period_days": days,
                "total_tasks": 0,
                "average_compliance_score": 0.0,
                "violations": [],
                "patterns": []
            }
        
        # Calculate statistics
        total_tasks = len(recent_records)
        avg_score = sum(record["compliance_score"] for record in recent_records) / total_tasks
        
        # Aggregate violations
        all_violations = []
        for record in recent_records:
            all_violations.extend(record.get("violations", []))
        
        # Group violations by type
        violation_types = {}
        for violation in all_violations:
            vtype = violation.get("type", "unknown")
            if vtype not in violation_types:
                violation_types[vtype] = []
            violation_types[vtype].append(violation)
        
        # Get recent patterns
        recent_patterns = [
            pattern for pattern in self.patterns
            if datetime.fromisoformat(pattern["timestamp"]) >= cutoff
        ]
        
        report = {
            "period_days": days,
            "generated_at": datetime.utcnow().isoformat(),
            "total_tasks": total_tasks,
            "average_compliance_score": round(avg_score, 2),
            "compliance_distribution": {
                "excellent": len([r for r in recent_records if r["compliance_score"] >= 0.9]),
                "good": len([r for r in recent_records if 0.7 <= r["compliance_score"] < 0.9]),
                "fair": len([r for r in recent_records if 0.5 <= r["compliance_score"] < 0.7]),
                "poor": len([r for r in recent_records if r["compliance_score"] < 0.5])
            },
            "violations": {
                "total": len(all_violations),
                "by_type": {k: len(v) for k, v in violation_types.items()},
                "details": violation_types
            },
            "patterns": recent_patterns,
            "suggestions": self._generate_report_suggestions(recent_records)
        }
        
        return report
    
    def _generate_report_suggestions(self, records: List[Dict]) -> List[str]:
        """Generate suggestions based on compliance report"""
        suggestions = []
        
        # Check average compliance score
        avg_score = sum(record["compliance_score"] for record in records) / len(records) if records else 0
        
        if avg_score < 0.7:
            suggestions.append("Consider improving planning process to better match actual execution")
        
        # Check for common violations
        all_violations = []
        for record in records:
            all_violations.extend(record.get("violations", []))
        
        violation_types = {}
        for violation in all_violations:
            vtype = violation.get("type", "unknown")
            violation_types[vtype] = violation_types.get(vtype, 0) + 1
        
        if violation_types.get("missing_tools", 0) > len(records) * 0.3:
            suggestions.append("Frequently missing planned tools - consider reviewing tool selection process")
        
        if violation_types.get("missing_agents", 0) > len(records) * 0.3:
            suggestions.append("Frequently missing planned agents - consider reviewing agent selection process")
        
        return suggestions
    
    def track_fibonacci_pattern(self, attention_data: List[float]) -> Dict:
        """
        Track fibonacci pattern in attention data
        
        Args:
            attention_data: List of attention values
            
        Returns:
            Pattern analysis dictionary
        """
        # Simple fibonacci pattern detection
        pattern = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": "fibonacci_pattern",
            "data": attention_data,
            "detected": False
        }
        
        # Check for fibonacci-like sequence
        if len(attention_data) >= 3:
            ratios = []
            for i in range(1, len(attention_data)):
                if attention_data[i-1] != 0:
                    ratio = attention_data[i] / attention_data[i-1]
                    ratios.append(ratio)
            
            # Fibonacci ratio is approximately 1.618
            fibonacci_ratio = 1.618
            tolerance = 0.1
            
            fibonacci_like = sum(1 for r in ratios if abs(r - fibonacci_ratio) < tolerance)
            
            if fibonacci_like > len(ratios) * 0.5:
                pattern["detected"] = True
                pattern["confidence"] = fibonacci_like / len(ratios)
                self.patterns.append(pattern)
                logger.info(f"Fibonacci pattern detected with confidence {pattern['confidence']:.2f}")
        
        return pattern


# Singleton instance
_compliance_auditor = None

def get_compliance_auditor() -> ComplianceAuditor:
    """Get or create compliance auditor singleton"""
    global _compliance_auditor
    if _compliance_auditor is None:
        _compliance_auditor = ComplianceAuditor()
    return _compliance_auditor

