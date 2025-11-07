#!/usr/bin/env python3
"""
Run Agents - Focused Entry Point

Purpose: Wrangle the app to a focused point for interaction, sync database and app,
and run the agentic flow with all agents on their missions.

Usage:
    python run_agents.py [--task-type TYPE] [--query QUERY] [--url URL]

Author: Gematria Hive Team
Date: January 6, 2025
"""

import sys
import os
import argparse
import logging
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('agent_run.log')
    ]
)
logger = logging.getLogger(__name__)


def verify_database() -> bool:
    """Verify database connection and setup"""
    logger.info("=" * 60)
    logger.info("Verifying Database Connection")
    logger.info("=" * 60)
    
    try:
        from setup_database import test_connection, verify_tables, verify_pgvector
        
        # Test connection
        connection_result = test_connection()
        if connection_result.get("status") != "success":
            logger.error("❌ Database connection failed")
            return False
        
        logger.info("✅ Database connection successful")
        
        # Verify tables
        tables_result = verify_tables()
        if tables_result.get("status") not in ["success", "partial"]:
            logger.warning("⚠️  Some tables may be missing")
        
        # Verify pgvector
        pgvector_result = verify_pgvector()
        if pgvector_result.get("status") not in ["success", "partial"]:
            logger.warning("⚠️  pgvector may need to be enabled")
        
        logger.info("✅ Database verification complete")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database verification error: {e}")
        return False


def initialize_orchestrator():
    """Initialize the MCP orchestrator"""
    logger.info("=" * 60)
    logger.info("Initializing MCP Orchestrator")
    logger.info("=" * 60)
    
    try:
        from agents.orchestrator import get_orchestrator
        
        orchestrator = get_orchestrator()
        logger.info("✅ Orchestrator initialized")
        
        # Log available agents
        agents = list(orchestrator.agents.keys()) if hasattr(orchestrator, 'agents') else []
        logger.info(f"✅ Available agents: {len(agents)}")
        for agent_name in agents:
            logger.info(f"   - {agent_name}")
        
        return orchestrator
        
    except Exception as e:
        logger.error(f"❌ Orchestrator initialization error: {e}")
        import traceback
        traceback.print_exc()
        return None


def create_default_tasks() -> List[Dict]:
    """Create default tasks for agents to execute"""
    tasks = [
        {
            "type": "extraction",
            "source": "test",
            "description": "Extract data from test source"
        },
        {
            "type": "distillation",
            "description": "Process and distill extracted data"
        },
        {
            "type": "ingestion",
            "description": "Ingest processed data into database"
        },
        {
            "type": "inference",
            "query": "gematria numerology sacred geometry",
            "description": "Generate insights and hunches"
        },
        {
            "type": "affinity",
            "query": "synchronicities patterns",
            "description": "Detect synchronicities and patterns"
        },
        {
            "type": "pattern_detector",
            "query": "gematria patterns",
            "description": "Detect patterns in data"
        },
        {
            "type": "gematria_integrator",
            "query": "calculate gematria values",
            "description": "Integrate gematria calculations"
        }
    ]
    
    return tasks


def execute_task(orchestrator, task: Dict) -> Dict:
    """Execute a single task through the orchestrator"""
    logger.info("=" * 60)
    logger.info(f"Executing Task: {task.get('type', 'unknown')}")
    logger.info("=" * 60)
    logger.info(f"Description: {task.get('description', 'No description')}")
    
    try:
        start_time = datetime.now()
        
        # Execute task
        result = orchestrator.execute(task)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info(f"✅ Task completed in {duration:.2f} seconds")
        logger.info(f"Status: {result.get('status', 'unknown')}")
        logger.info(f"Results: {len(result.get('results', []))} agent outputs")
        logger.info(f"Cost: ${result.get('cost', 0):.4f}")
        
        if result.get('error'):
            logger.warning(f"⚠️  Task error: {result.get('error')}")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Task execution error: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "failed", "error": str(e)}


def run_agent_flow(orchestrator, tasks: List[Dict] = None):
    """Run the complete agentic flow with all agents"""
    logger.info("=" * 60)
    logger.info("Starting Agentic Flow")
    logger.info("=" * 60)
    
    if tasks is None:
        tasks = create_default_tasks()
    
    logger.info(f"📋 Executing {len(tasks)} tasks")
    logger.info("")
    
    results = []
    for i, task in enumerate(tasks, 1):
        logger.info(f"\n{'='*60}")
        logger.info(f"Task {i}/{len(tasks)}")
        logger.info(f"{'='*60}\n")
        
        result = execute_task(orchestrator, task)
        results.append({
            "task": task,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info("")
    
    # Summary
    logger.info("=" * 60)
    logger.info("Agentic Flow Summary")
    logger.info("=" * 60)
    
    successful = sum(1 for r in results if r["result"].get("status") == "completed")
    failed = len(results) - successful
    total_cost = sum(r["result"].get("cost", 0) for r in results)
    
    logger.info(f"✅ Successful tasks: {successful}/{len(results)}")
    logger.info(f"❌ Failed tasks: {failed}/{len(results)}")
    logger.info(f"💰 Total cost: ${total_cost:.4f}")
    logger.info("")
    
    return results


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Run Gematria Hive agents on their missions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run default tasks
  python run_agents.py
  
  # Run specific task type
  python run_agents.py --task-type inference --query "gematria patterns"
  
  # Run browser task
  python run_agents.py --task-type browser --url "https://example.com"
        """
    )
    
    parser.add_argument(
        "--task-type",
        type=str,
        help="Specific task type to run (extraction, distillation, ingestion, inference, etc.)"
    )
    
    parser.add_argument(
        "--query",
        type=str,
        help="Query string for inference/affinity tasks"
    )
    
    parser.add_argument(
        "--url",
        type=str,
        help="URL for browser/scraping tasks"
    )
    
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Skip database verification"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("=" * 60)
    logger.info("GEMATRIA HIVE - AGENT RUNNER")
    logger.info("=" * 60)
    logger.info("")
    
    # Step 1: Verify database
    if not args.skip_verify:
        if not verify_database():
            logger.error("❌ Database verification failed. Exiting.")
            logger.info("Run with --skip-verify to skip verification")
            return 1
        logger.info("")
    else:
        logger.info("⏭️  Skipping database verification")
        logger.info("")
    
    # Step 2: Initialize orchestrator
    orchestrator = initialize_orchestrator()
    if orchestrator is None:
        logger.error("❌ Orchestrator initialization failed. Exiting.")
        return 1
    logger.info("")
    
    # Step 3: Create tasks
    if args.task_type:
        # Single task
        task = {
            "type": args.task_type,
            "description": f"Execute {args.task_type} task"
        }
        
        if args.query:
            task["query"] = args.query
        
        if args.url:
            task["url"] = args.url
        
        tasks = [task]
    else:
        # Default tasks
        tasks = create_default_tasks()
    
    # Step 4: Run agent flow
    results = run_agent_flow(orchestrator, tasks)
    
    # Step 5: Save results
    results_file = f"agent_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        import json
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        logger.info(f"📄 Results saved to: {results_file}")
    except Exception as e:
        logger.warning(f"⚠️  Could not save results: {e}")
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("✅ Agent Run Complete!")
    logger.info("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

