#!/usr/bin/env python3
"""
Run the Reviewer Agent to review all completed work.

Usage:
    python run_reviewer.py [autonomous_tasks.json]
"""

import sys
import json
from pathlib import Path
from agents.reviewer import ReviewerAgent


def main():
    """Run the reviewer agent."""
    # Try to load task status if provided
    task_status = None
    if len(sys.argv) > 1:
        task_file = Path(sys.argv[1])
        if task_file.exists():
            print(f"📋 Loading task status from: {task_file}")
            with open(task_file, 'r') as f:
                task_status = json.load(f)
        else:
            print(f"⚠️  Task file not found: {task_file}")
            print("   Running review without task status check...")
    else:
        # Try default location
        default_task_file = Path("autonomous_tasks.json")
        if default_task_file.exists():
            print(f"📋 Loading task status from: {default_task_file}")
            with open(default_task_file, 'r') as f:
                task_status = json.load(f)
        else:
            print("ℹ️  No task file provided, running review without task status check...")
    
    # Create and run reviewer
    print("\n" + "="*60)
    print("REVIEWER AGENT")
    print("="*60 + "\n")
    
    reviewer = ReviewerAgent()
    result = reviewer.run_review(task_status)
    
    # Print summary
    print("\n" + "="*60)
    print("REVIEW SUMMARY")
    print("="*60)
    
    if result.get("status") == "pending":
        print(f"⏳ Status: {result.get('message')}")
        return
    
    print(f"✅ Status: {result.get('status')}")
    print(f"📅 Timestamp: {result.get('timestamp')}")
    
    summary = result.get("work_summary", {})
    print(f"\n📊 Work Summary:")
    print(f"   - Agents: {summary.get('agents', 0)}")
    print(f"   - Core Modules: {summary.get('core_modules', 0)}")
    print(f"   - Documentation: {summary.get('documentation', 0)}")
    
    print(f"\n⭐ Quality Assessment: {result.get('quality_assessment', 'unknown')}")
    
    files = result.get("files_generated", {})
    if files:
        print(f"\n📄 Generated Files:")
        for name, path in files.items():
            print(f"   - {name}: {path}")
    
    print("\n" + "="*60)
    print("Review complete! Check the 'reviews/' directory for detailed reports.")
    print("="*60)
    
    return result


if __name__ == "__main__":
    main()




