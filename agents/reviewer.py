"""
Reviewer Agent - Final Quality Review and Documentation Generator

This agent reviews all completed work when all agents are finished,
provides critique, generates documentation, and creates status reports.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path


class ReviewerAgent:
    """
    Agent that performs final review, critique, and documentation generation
    when all other agents have completed their work.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the Reviewer Agent."""
        self.config_path = config_path or "autonomous_config.json"
        self.work_dir = Path(".")
        self.review_dir = Path("reviews")
        self.review_dir.mkdir(exist_ok=True)
        
    def check_all_agents_complete(self, task_status: Dict[str, Any]) -> bool:
        """
        Check if all agents have completed their work.
        
        Args:
            task_status: Dictionary containing task completion status
            
        Returns:
            True if all agents are complete, False otherwise
        """
        if not task_status:
            return False
            
        # Check for any pending or in-progress tasks
        for agent_name, status in task_status.items():
            if isinstance(status, dict):
                if status.get("status") in ["pending", "in_progress"]:
                    return False
            elif status not in ["completed", "done", "finished"]:
                return False
                
        return True
    
    def collect_all_work(self) -> Dict[str, Any]:
        """
        Collect all work artifacts from the project.
        
        Returns:
            Dictionary containing all work artifacts organized by category
        """
        work = {
            "timestamp": datetime.now().isoformat(),
            "agents": {},
            "code_artifacts": {},
            "data_artifacts": {},
            "documentation": {},
            "configurations": {},
            "database": {},
            "tasks": {}
        }
        
        # Collect agent files
        agents_dir = self.work_dir / "agents"
        if agents_dir.exists():
            work["agents"]["files"] = [
                str(f.relative_to(self.work_dir))
                for f in agents_dir.glob("*.py")
                if f.is_file()
            ]
            work["agents"]["count"] = len(work["agents"]["files"])
        
        # Collect core modules
        core_dir = self.work_dir / "core"
        if core_dir.exists():
            work["code_artifacts"]["core"] = [
                str(f.relative_to(self.work_dir))
                for f in core_dir.glob("*.py")
                if f.is_file()
            ]
        
        # Collect scripts
        scripts_dir = self.work_dir / "scripts"
        if scripts_dir.exists():
            work["code_artifacts"]["scripts"] = [
                str(f.relative_to(self.work_dir))
                for f in scripts_dir.glob("*.py")
                if f.is_file()
            ]
        
        # Collect migrations
        migrations_dir = self.work_dir / "migrations"
        if migrations_dir.exists():
            work["database"]["migrations"] = [
                str(f.relative_to(self.work_dir))
                for f in migrations_dir.glob("*.sql")
                if f.is_file()
            ]
        
        # Collect documentation
        doc_files = [
            "README.md", "PRD.md", "MASTER_ARCHITECTURE.md",
            "IMPLEMENTATION_ROADMAP.md", "NEXT_STEPS.md",
            "QUICK_START.md", "INGESTION_GUIDE.md"
        ]
        work["documentation"]["files"] = [
            f for f in doc_files
            if (self.work_dir / f).exists()
        ]
        
        # Collect configuration files
        config_files = [
            "autonomous_config.json", "autonomous_tasks.json",
            "requirements.txt", "environment.yml"
        ]
        work["configurations"]["files"] = [
            f for f in config_files
            if (self.work_dir / f).exists()
        ]
        
        # Try to load task status if available
        tasks_file = self.work_dir / "autonomous_tasks.json"
        if tasks_file.exists():
            try:
                with open(tasks_file, 'r') as f:
                    work["tasks"] = json.load(f)
            except Exception as e:
                work["tasks"]["error"] = str(e)
        
        return work
    
    def review_work_quality(self, work: Dict[str, Any]) -> Dict[str, Any]:
        """
        Review and critique the quality of completed work.
        
        Args:
            work: Dictionary containing all work artifacts
            
        Returns:
            Dictionary containing review findings and critiques
        """
        review = {
            "overall_quality": "good",
            "strengths": [],
            "concerns": [],
            "recommendations": [],
            "metrics": {}
        }
        
        # Review agent completeness
        agent_count = work.get("agents", {}).get("count", 0)
        if agent_count > 0:
            review["strengths"].append(
                f"Comprehensive agent framework with {agent_count} agents"
            )
            review["metrics"]["agent_count"] = agent_count
        else:
            review["concerns"].append("No agents found in agents directory")
        
        # Review code organization
        core_files = len(work.get("code_artifacts", {}).get("core", []))
        script_files = len(work.get("code_artifacts", {}).get("scripts", []))
        
        if core_files > 0:
            review["strengths"].append(
                f"Core modules organized ({core_files} files)"
            )
        if script_files > 0:
            review["strengths"].append(
                f"Utility scripts available ({script_files} files)"
            )
        
        # Review documentation
        doc_count = len(work.get("documentation", {}).get("files", []))
        if doc_count >= 5:
            review["strengths"].append(
                f"Comprehensive documentation ({doc_count} files)"
            )
        elif doc_count > 0:
            review["concerns"].append(
                f"Limited documentation ({doc_count} files) - consider adding more"
            )
        else:
            review["concerns"].append("No documentation files found")
        
        # Review database migrations
        migration_count = len(work.get("database", {}).get("migrations", []))
        if migration_count > 0:
            review["strengths"].append(
                f"Database migrations in place ({migration_count} files)"
            )
        else:
            review["concerns"].append("No database migrations found")
        
        # Review task completion
        tasks = work.get("tasks", {})
        if isinstance(tasks, dict) and tasks:
            completed = sum(
                1 for v in tasks.values()
                if isinstance(v, dict) and v.get("status") == "completed"
            )
            total = len(tasks)
            if total > 0:
                completion_rate = (completed / total) * 100
                review["metrics"]["task_completion_rate"] = completion_rate
                if completion_rate == 100:
                    review["strengths"].append("All tasks completed")
                elif completion_rate >= 80:
                    review["concerns"].append(
                        f"Some tasks incomplete ({completed}/{total})"
                    )
        
        # Generate recommendations
        if doc_count < 5:
            review["recommendations"].append(
                "Expand documentation with API references and usage examples"
            )
        
        if migration_count == 0:
            review["recommendations"].append(
                "Add database migrations for schema management"
            )
        
        review["recommendations"].append(
            "Consider adding unit tests for core functionality"
        )
        review["recommendations"].append(
            "Add integration tests for agent workflows"
        )
        
        return review
    
    def generate_synopsis(self, work: Dict[str, Any], review: Dict[str, Any]) -> str:
        """
        Generate a high-level synopsis of the project.
        
        Args:
            work: Dictionary containing all work artifacts
            review: Dictionary containing review findings
            
        Returns:
            Synopsis string
        """
        synopsis = f"""# Project Synopsis

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

This project represents a comprehensive agent-based framework for gematria research and analysis. The system consists of multiple specialized agents working together to ingest, process, analyze, and generate insights from gematria-related data.

## Current State

### Agents Implemented
- **Agent Count:** {work.get('agents', {}).get('count', 0)} specialized agents
- **Core Modules:** {len(work.get('code_artifacts', {}).get('core', []))} core components
- **Utility Scripts:** {len(work.get('code_artifacts', {}).get('scripts', []))} utility scripts

### Documentation
- **Documentation Files:** {len(work.get('documentation', {}).get('files', []))} comprehensive guides
- **Configuration Files:** {len(work.get('configurations', {}).get('files', []))} configuration files

### Database
- **Migrations:** {len(work.get('database', {}).get('migrations', []))} database migration files

## Quality Assessment

**Overall Quality:** {review.get('overall_quality', 'unknown').title()}

### Strengths
"""
        for strength in review.get("strengths", []):
            synopsis += f"- {strength}\n"
        
        synopsis += "\n### Areas for Improvement\n"
        for concern in review.get("concerns", []):
            synopsis += f"- {concern}\n"
        
        return synopsis
    
    def generate_abstract(self, work: Dict[str, Any]) -> str:
        """
        Generate an abstract summarizing the project.
        
        Args:
            work: Dictionary containing all work artifacts
            
        Returns:
            Abstract string
        """
        agent_count = work.get('agents', {}).get('count', 0)
        
        abstract = f"""# Project Abstract

The Gematria Hive project is an advanced, agent-based research and analysis platform designed to process, analyze, and generate insights from gematria-related data. The system employs a multi-agent architecture with {agent_count} specialized agents, each responsible for distinct aspects of the workflow including data ingestion, extraction, distillation, generation, and orchestration.

The platform features a modular design with core engine components, comprehensive database migrations, and extensive documentation. It supports autonomous task execution, real-time monitoring, and collaborative agent interactions to deliver sophisticated gematria analysis capabilities.

Key features include:
- Multi-agent orchestration framework
- Automated data ingestion and processing
- Knowledge registry and management
- Autonomous task execution
- Real-time monitoring and observation
- Comprehensive documentation and configuration management

The system is designed for extensibility, allowing new agents and capabilities to be integrated seamlessly while maintaining code quality and architectural integrity.
"""
        return abstract
    
    def generate_status_report(
        self,
        work: Dict[str, Any],
        review: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive status report.
        
        Args:
            work: Dictionary containing all work artifacts
            review: Dictionary containing review findings
            
        Returns:
            Status report dictionary
        """
        report = {
            "generated_at": datetime.now().isoformat(),
            "project_status": "active",
            "achievements": {
                "agents_implemented": work.get('agents', {}).get('count', 0),
                "core_modules": len(work.get('code_artifacts', {}).get('core', [])),
                "scripts_available": len(work.get('code_artifacts', {}).get('scripts', [])),
                "documentation_files": len(work.get('documentation', {}).get('files', [])),
                "database_migrations": len(work.get('database', {}).get('migrations', []))
            },
            "whats_available": {
                "agents": work.get('agents', {}).get('files', []),
                "core_modules": work.get('code_artifacts', {}).get('core', []),
                "scripts": work.get('code_artifacts', {}).get('scripts', []),
                "documentation": work.get('documentation', {}).get('files', []),
                "migrations": work.get('database', {}).get('migrations', [])
            },
            "quality_review": {
                "overall_quality": review.get('overall_quality'),
                "strengths": review.get('strengths', []),
                "concerns": review.get('concerns', []),
                "metrics": review.get('metrics', {})
            },
            "next_steps": review.get('recommendations', [])
        }
        
        return report
    
    def save_review_artifacts(
        self,
        synopsis: str,
        abstract: str,
        status_report: Dict[str, Any],
        review: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Save all review artifacts to files.
        
        Args:
            synopsis: Synopsis text
            abstract: Abstract text
            status_report: Status report dictionary
            review: Review findings dictionary
            
        Returns:
            Dictionary with paths to saved files
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        saved_files = {}
        
        # Save synopsis
        synopsis_path = self.review_dir / f"synopsis_{timestamp}.md"
        with open(synopsis_path, 'w') as f:
            f.write(synopsis)
        saved_files["synopsis"] = str(synopsis_path)
        
        # Save abstract
        abstract_path = self.review_dir / f"abstract_{timestamp}.md"
        with open(abstract_path, 'w') as f:
            f.write(abstract)
        saved_files["abstract"] = str(abstract_path)
        
        # Save status report
        status_path = self.review_dir / f"status_report_{timestamp}.json"
        with open(status_path, 'w') as f:
            json.dump(status_report, f, indent=2)
        saved_files["status_report"] = str(status_path)
        
        # Save review findings
        review_path = self.review_dir / f"review_{timestamp}.json"
        with open(review_path, 'w') as f:
            json.dump(review, f, indent=2)
        saved_files["review"] = str(review_path)
        
        # Save comprehensive report
        comprehensive_path = self.review_dir / f"comprehensive_report_{timestamp}.md"
        comprehensive = f"""# Comprehensive Project Review

{abstract}

---

{synopsis}

---

## Detailed Status Report

### Achievements
"""
        for key, value in status_report.get("achievements", {}).items():
            comprehensive += f"- **{key.replace('_', ' ').title()}:** {value}\n"
        
        comprehensive += "\n### What's Available\n"
        for category, items in status_report.get("whats_available", {}).items():
            comprehensive += f"\n#### {category.replace('_', ' ').title()}\n"
            if isinstance(items, list):
                for item in items:
                    comprehensive += f"- {item}\n"
            else:
                comprehensive += f"- {items}\n"
        
        comprehensive += "\n### Quality Review\n"
        comprehensive += f"- **Overall Quality:** {review.get('overall_quality', 'unknown')}\n"
        comprehensive += "\n#### Strengths\n"
        for strength in review.get('strengths', []):
            comprehensive += f"- {strength}\n"
        comprehensive += "\n#### Concerns\n"
        for concern in review.get('concerns', []):
            comprehensive += f"- {concern}\n"
        
        comprehensive += "\n### Next Steps\n"
        for step in status_report.get("next_steps", []):
            comprehensive += f"- {step}\n"
        
        with open(comprehensive_path, 'w') as f:
            f.write(comprehensive)
        saved_files["comprehensive"] = str(comprehensive_path)
        
        return saved_files
    
    def run_review(self, task_status: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the complete review process.
        
        Args:
            task_status: Optional task status dictionary
            
        Returns:
            Dictionary containing review results and file paths
        """
        print("🔍 Reviewer Agent: Starting comprehensive review...")
        
        # Check if all agents are complete
        if task_status:
            if not self.check_all_agents_complete(task_status):
                return {
                    "status": "pending",
                    "message": "Not all agents have completed their work yet"
                }
        
        # Collect all work
        print("📦 Collecting all work artifacts...")
        work = self.collect_all_work()
        
        # Review work quality
        print("🔎 Reviewing work quality...")
        review = self.review_work_quality(work)
        
        # Generate documentation
        print("📝 Generating documentation...")
        synopsis = self.generate_synopsis(work, review)
        abstract = self.generate_abstract(work)
        status_report = self.generate_status_report(work, review)
        
        # Save artifacts
        print("💾 Saving review artifacts...")
        saved_files = self.save_review_artifacts(
            synopsis, abstract, status_report, review
        )
        
        result = {
            "status": "completed",
            "timestamp": datetime.now().isoformat(),
            "work_summary": {
                "agents": work.get('agents', {}).get('count', 0),
                "core_modules": len(work.get('code_artifacts', {}).get('core', [])),
                "documentation": len(work.get('documentation', {}).get('files', []))
            },
            "quality_assessment": review.get('overall_quality'),
            "files_generated": saved_files,
            "synopsis_preview": synopsis[:500] + "..." if len(synopsis) > 500 else synopsis,
            "abstract_preview": abstract[:500] + "..." if len(abstract) > 500 else abstract
        }
        
        print("✅ Review complete!")
        print(f"📄 Files saved to: {self.review_dir}")
        for name, path in saved_files.items():
            print(f"   - {name}: {path}")
        
        return result


def main():
    """Main entry point for the Reviewer Agent."""
    import sys
    
    # Try to load task status if provided
    task_status = None
    if len(sys.argv) > 1:
        task_file = sys.argv[1]
        if os.path.exists(task_file):
            with open(task_file, 'r') as f:
                task_status = json.load(f)
    
    # Create and run reviewer
    reviewer = ReviewerAgent()
    result = reviewer.run_review(task_status)
    
    # Print summary
    print("\n" + "="*60)
    print("REVIEW SUMMARY")
    print("="*60)
    print(json.dumps(result, indent=2))
    
    return result


if __name__ == "__main__":
    main()




