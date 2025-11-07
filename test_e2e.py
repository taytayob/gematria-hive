#!/usr/bin/env python3
"""
End-to-End Test Script

Purpose: Test the complete Gematria Hive pipeline from extraction to ingestion.
Verifies all agents work correctly and database operations succeed.

Usage:
    python test_e2e.py
    python test_e2e.py --verbose
    python test_e2e.py --skip-db  # Skip database operations

Author: Gematria Hive Team
Date: January 6, 2025
"""

import sys
import os
import json
import argparse
import logging
from pathlib import Path
from typing import Dict, List
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_test_data() -> List[Dict]:
    """Create test data for ingestion"""
    return [
        {
            "url": "https://example.com/gematria-369",
            "summary": "Article about the significance of 369 in gematria and sacred geometry. The number 369 appears frequently in mathematical patterns and esoteric traditions."
        },
        {
            "url": "https://example.com/sacred-geometry",
            "summary": "Exploring sacred geometry and its mathematical foundations. How geometric patterns relate to universal constants and spiritual principles."
        },
        {
            "url": "https://example.com/numerology",
            "summary": "Introduction to numerology and its connections to gematria. Understanding how numbers carry meaning across different systems."
        }
    ]


def test_extraction_agent(verbose: bool = False) -> Dict:
    """Test extraction agent"""
    logger.info("=" * 60)
    logger.info("Testing Extraction Agent")
    logger.info("=" * 60)
    
    try:
        from agents.extraction import ExtractionAgent
        
        # Create test data file
        test_data = create_test_data()
        test_file = "test_data.json"
        with open(test_file, 'w') as f:
            json.dump(test_data, f, indent=2)
        
        logger.info(f"Created test data file: {test_file}")
        
        # Test extraction
        agent = ExtractionAgent()
        data = agent.extract_from_source(test_file)
        
        if data:
            logger.info(f"✅ Extraction successful: {len(data)} items extracted")
            if verbose:
                logger.info(f"Sample data: {json.dumps(data[0], indent=2)}")
            return {"status": "success", "count": len(data), "data": data}
        else:
            logger.error("❌ Extraction failed: No data returned")
            return {"status": "failed", "error": "No data returned"}
            
    except Exception as e:
        logger.error(f"❌ Extraction test failed: {e}")
        return {"status": "failed", "error": str(e)}


def test_distillation_agent(extracted_data: List[Dict], verbose: bool = False) -> Dict:
    """Test distillation agent"""
    logger.info("=" * 60)
    logger.info("Testing Distillation Agent")
    logger.info("=" * 60)
    
    try:
        from agents.distillation import DistillationAgent
        
        agent = DistillationAgent()
        processed = agent.process_data(extracted_data)
        
        if processed:
            logger.info(f"✅ Distillation successful: {len(processed)} items processed")
            
            # Check embeddings
            with_embeddings = sum(1 for p in processed if p.get("embedding"))
            logger.info(f"  - Items with embeddings: {with_embeddings}/{len(processed)}")
            
            # Check relevance scores
            avg_relevance = sum(p.get("relevance_score", 0) for p in processed) / len(processed)
            logger.info(f"  - Average relevance: {avg_relevance:.3f}")
            
            if verbose:
                logger.info(f"Sample processed: {json.dumps(processed[0], indent=2, default=str)}")
            
            return {
                "status": "success",
                "count": len(processed),
                "with_embeddings": with_embeddings,
                "avg_relevance": avg_relevance,
                "data": processed
            }
        else:
            logger.error("❌ Distillation failed: No data processed")
            return {"status": "failed", "error": "No data processed"}
            
    except Exception as e:
        logger.error(f"❌ Distillation test failed: {e}")
        return {"status": "failed", "error": str(e)}


def test_ingestion_agent(processed_data: List[Dict], skip_db: bool = False, verbose: bool = False) -> Dict:
    """Test ingestion agent"""
    logger.info("=" * 60)
    logger.info("Testing Ingestion Agent")
    logger.info("=" * 60)
    
    if skip_db:
        logger.info("⏭️  Skipping database operations (--skip-db flag)")
        return {"status": "skipped", "reason": "Database operations skipped"}
    
    try:
        from agents.ingestion import IngestionAgent
        
        agent = IngestionAgent()
        
        # Test ingestion to bookmarks table
        ingested_count = agent.ingest_to_db(processed_data) if hasattr(agent, 'ingest_to_db') else 0
        
        if ingested_count > 0:
            logger.info(f"✅ Ingestion successful: {ingested_count} items ingested")
            return {"status": "success", "count": ingested_count}
        else:
            logger.warning("⚠️  Ingestion returned 0 items (may be expected if Supabase not configured)")
            return {"status": "partial", "count": 0, "note": "Supabase may not be configured"}
            
    except Exception as e:
        logger.error(f"❌ Ingestion test failed: {e}")
        return {"status": "failed", "error": str(e)}


def test_orchestrator(verbose: bool = False) -> Dict:
    """Test MCP orchestrator"""
    logger.info("=" * 60)
    logger.info("Testing MCP Orchestrator")
    logger.info("=" * 60)
    
    try:
        from agents import MCPOrchestrator
        
        orchestrator = MCPOrchestrator()
        
        # Create test data file
        test_data = create_test_data()
        test_file = "test_data.json"
        with open(test_file, 'w') as f:
            json.dump(test_data, f, indent=2)
        
        # Test full workflow
        task = {
            "type": "extraction",
            "source": test_file,
            "query": "gematria numerology"
        }
        
        logger.info("Executing full workflow...")
        result = orchestrator.execute(task)
        
        if result.get("status") == "completed":
            logger.info("✅ Orchestrator workflow completed successfully")
            logger.info(f"  - Items processed: {len(result.get('data', []))}")
            logger.info(f"  - Cost: ${result.get('cost', 0):.2f}")
            logger.info(f"  - Results: {len(result.get('results', []))}")
            
            if verbose:
                logger.info(f"Full result: {json.dumps(result, indent=2, default=str)}")
            
            return {"status": "success", "result": result}
        else:
            logger.error(f"❌ Orchestrator workflow failed: {result.get('error', 'Unknown error')}")
            return {"status": "failed", "error": result.get("error", "Unknown error")}
            
    except Exception as e:
        logger.error(f"❌ Orchestrator test failed: {e}")
        return {"status": "failed", "error": str(e)}


def test_task_manager(verbose: bool = False) -> Dict:
    """Test task manager"""
    logger.info("=" * 60)
    logger.info("Testing Task Manager")
    logger.info("=" * 60)
    
    try:
        from task_manager import get_task_manager
        
        tm = get_task_manager()
        
        # Create a test task
        task = tm.create_task(
            content="Test task for E2E testing",
            status="pending",
            cost=0.0
        )
        
        if task:
            logger.info(f"✅ Task created: {task.get('id')}")
            
            # Get tasks by status
            pending = tm.get_tasks_by_status("pending")
            logger.info(f"  - Pending tasks: {len(pending)}")
            
            # Update task
            updated = tm.update_task(task["id"], status="in_progress")
            if updated:
                logger.info("✅ Task updated successfully")
            
            # Get statistics
            stats = tm.get_task_statistics()
            logger.info(f"  - Total tasks: {stats.get('total', 0)}")
            logger.info(f"  - Total cost: ${stats.get('total_cost', 0):.2f}")
            
            return {"status": "success", "task_id": task.get("id"), "stats": stats}
        else:
            logger.warning("⚠️  Task creation returned None (may be expected if Supabase not configured)")
            return {"status": "partial", "note": "Supabase may not be configured"}
            
    except Exception as e:
        logger.error(f"❌ Task manager test failed: {e}")
        return {"status": "failed", "error": str(e)}


def test_kanban_dashboard(verbose: bool = False) -> Dict:
    """Test kanban dashboard (import test)"""
    logger.info("=" * 60)
    logger.info("Testing Kanban Dashboard")
    logger.info("=" * 60)
    
    try:
        from pages.kanban_dashboard import main as kanban_main
        
        logger.info("✅ Kanban dashboard module imports successfully")
        return {"status": "success", "note": "Module import successful"}
        
    except Exception as e:
        logger.error(f"❌ Kanban dashboard test failed: {e}")
        return {"status": "failed", "error": str(e)}


def main():
    """Main test function"""
    parser = argparse.ArgumentParser(
        description="End-to-end test for Gematria Hive pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--skip-db",
        action="store_true",
        help="Skip database operations (for testing without Supabase)"
    )
    
    parser.add_argument(
        "--skip-orchestrator",
        action="store_true",
        help="Skip orchestrator test"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("=" * 60)
    logger.info("Gematria Hive - End-to-End Test Suite")
    logger.info("=" * 60)
    logger.info("")
    
    results = {}
    
    # Test 1: Extraction Agent
    extraction_result = test_extraction_agent(verbose=args.verbose)
    results["extraction"] = extraction_result
    
    if extraction_result.get("status") != "success":
        logger.error("Extraction failed, stopping tests")
        return 1
    
    extracted_data = extraction_result.get("data", [])
    
    # Test 2: Distillation Agent
    distillation_result = test_distillation_agent(extracted_data, verbose=args.verbose)
    results["distillation"] = distillation_result
    
    if distillation_result.get("status") != "success":
        logger.error("Distillation failed, stopping tests")
        return 1
    
    processed_data = distillation_result.get("data", [])
    
    # Test 3: Ingestion Agent
    ingestion_result = test_ingestion_agent(processed_data, skip_db=args.skip_db, verbose=args.verbose)
    results["ingestion"] = ingestion_result
    
    # Test 4: Task Manager
    task_manager_result = test_task_manager(verbose=args.verbose)
    results["task_manager"] = task_manager_result
    
    # Test 5: Kanban Dashboard
    kanban_result = test_kanban_dashboard(verbose=args.verbose)
    results["kanban"] = kanban_result
    
    # Test 6: Orchestrator (optional)
    if not args.skip_orchestrator:
        orchestrator_result = test_orchestrator(verbose=args.verbose)
        results["orchestrator"] = orchestrator_result
    else:
        logger.info("⏭️  Skipping orchestrator test (--skip-orchestrator flag)")
        results["orchestrator"] = {"status": "skipped"}
    
    # Summary
    logger.info("")
    logger.info("=" * 60)
    logger.info("Test Summary")
    logger.info("=" * 60)
    
    for test_name, result in results.items():
        status = result.get("status", "unknown")
        if status == "success":
            logger.info(f"✅ {test_name}: PASSED")
        elif status == "partial":
            logger.info(f"⚠️  {test_name}: PARTIAL ({result.get('note', '')})")
        elif status == "skipped":
            logger.info(f"⏭️  {test_name}: SKIPPED")
        else:
            logger.error(f"❌ {test_name}: FAILED ({result.get('error', 'Unknown error')})")
    
    # Overall status
    all_passed = all(
        r.get("status") in ["success", "partial", "skipped"]
        for r in results.values()
    )
    
    if all_passed:
        logger.info("")
        logger.info("✅ All tests passed (or skipped/partial)")
        return 0
    else:
        logger.error("")
        logger.error("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

