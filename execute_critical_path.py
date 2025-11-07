#!/usr/bin/env python3
"""
Critical Path Execution - Self-Scaffolding Gematria Hive

Purpose: Execute the critical path with maximum concurrency
- Pull all ingestions
- Run all agents concurrently
- Detect patterns
- Generate proofs
- Create unifications

Author: Gematria Hive Team
Date: November 7, 2025
"""

import sys
import os
import asyncio
import concurrent.futures
import logging
import copy
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import json

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
        logging.FileHandler('critical_path_execution.log')
    ]
)
logger = logging.getLogger(__name__)


def pull_all_ingestions() -> List[Dict]:
    """Pull all existing data from database"""
    logger.info("=" * 60)
    logger.info("PHASE 1: Pulling All Ingestions")
    logger.info("=" * 60)
    
    try:
        from supabase import create_client
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            logger.error("❌ Supabase credentials not configured")
            return []
        
        supabase = create_client(supabase_url, supabase_key)
        
        # Pull from all data sources concurrently
        results = {}
        
        # Pull bookmarks
        try:
            bookmarks = supabase.table('bookmarks').select('*').limit(1000).execute()
            results['bookmarks'] = bookmarks.data if bookmarks.data else []
            logger.info(f"✅ Pulled {len(results['bookmarks'])} bookmarks")
        except Exception as e:
            logger.warning(f"⚠️  Error pulling bookmarks: {e}")
            results['bookmarks'] = []
        
        # Pull gematria_words
        try:
            gematria_words = supabase.table('gematria_words').select('*').limit(1000).execute()
            results['gematria_words'] = gematria_words.data if gematria_words.data else []
            logger.info(f"✅ Pulled {len(results['gematria_words'])} gematria words")
        except Exception as e:
            logger.warning(f"⚠️  Error pulling gematria_words: {e}")
            results['gematria_words'] = []
        
        # Pull sources
        try:
            sources = supabase.table('sources').select('*').limit(1000).execute()
            results['sources'] = sources.data if sources.data else []
            logger.info(f"✅ Pulled {len(results['sources'])} sources")
        except Exception as e:
            logger.warning(f"⚠️  Error pulling sources: {e}")
            results['sources'] = []
        
        # Pull patterns
        try:
            patterns = supabase.table('patterns').select('*').limit(1000).execute()
            results['patterns'] = patterns.data if patterns.data else []
            logger.info(f"✅ Pulled {len(results['patterns'])} patterns")
        except Exception as e:
            logger.warning(f"⚠️  Error pulling patterns: {e}")
            results['patterns'] = []
        
        # Pull hunches
        try:
            hunches = supabase.table('hunches').select('*').limit(1000).execute()
            results['hunches'] = hunches.data if hunches.data else []
            logger.info(f"✅ Pulled {len(results['hunches'])} hunches")
        except Exception as e:
            logger.warning(f"⚠️  Error pulling hunches: {e}")
            results['hunches'] = []
        
        # Combine all data
        all_data = []
        for source, data in results.items():
            for item in data:
                item['_source'] = source
                all_data.append(item)
        
        logger.info(f"✅ Total data pulled: {len(all_data)} items")
        return all_data
        
    except Exception as e:
        logger.error(f"❌ Error pulling ingestions: {e}")
        import traceback
        traceback.print_exc()
        return []


def run_agents_concurrently(data: List[Dict]) -> Dict:
    """Run all agents concurrently on the data"""
    logger.info("=" * 60)
    logger.info("PHASE 2: Running All Agents Concurrently")
    logger.info("=" * 60)
    
    try:
        from agents.orchestrator import get_orchestrator
        orchestrator = get_orchestrator()
        
        if not orchestrator:
            logger.error("❌ Orchestrator not available")
            return {}
        
        # Create tasks for all agents
        tasks = []
        
        # Process data in batches
        batch_size = 100
        for i in range(0, len(data), batch_size):
            batch = data[i:i+batch_size]
            
            # Create task for each batch
            task = {
                "type": "processing",
                "data": batch,
                "batch_number": i // batch_size + 1,
                "total_batches": (len(data) + batch_size - 1) // batch_size
            }
            tasks.append(task)
        
        logger.info(f"📋 Created {len(tasks)} tasks for {len(data)} items")
        
        # Execute all tasks concurrently
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for task in tasks:
                future = executor.submit(orchestrator.execute, task)
                futures.append(future)
            
            # Collect results
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                try:
                    result = future.result()
                    results.append(result)
                    logger.info(f"✅ Task {i+1}/{len(tasks)} completed")
                except Exception as e:
                    logger.error(f"❌ Task {i+1} failed: {e}")
        
        logger.info(f"✅ All agents executed: {len(results)} results")
        return {"results": results, "total_tasks": len(tasks)}
        
    except Exception as e:
        logger.error(f"❌ Error running agents: {e}")
        import traceback
        traceback.print_exc()
        return {}


def detect_patterns_concurrently(data: List[Dict]) -> Dict:
    """Detect patterns across all data concurrently"""
    logger.info("=" * 60)
    logger.info("PHASE 3: Detecting Patterns Concurrently")
    logger.info("=" * 60)
    
    try:
        from agents.pattern_detector import PatternDetectorAgent
        from agents.affinity import AffinityAgent
        from agents.gematria_integrator import GematriaIntegratorAgent
        
        pattern_detector = PatternDetectorAgent()
        affinity = AffinityAgent()
        gematria_integrator = GematriaIntegratorAgent()
        
        # Create state for pattern detection
        from agents.orchestrator import AgentState
        
        # Base state template
        base_state: AgentState = {
            "task": {"type": "pattern_detection", "data": data},
            "data": data,
            "context": {},
            "results": [],
            "cost": 0.0,
            "status": "pending",
            "memory_id": None
        }
        
        # Run all pattern detectors concurrently
        # Each agent gets its own independent copy of the state to avoid race conditions
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(pattern_detector.execute, copy.deepcopy(base_state)): "pattern_detector",
                executor.submit(affinity.execute, copy.deepcopy(base_state)): "affinity",
                executor.submit(gematria_integrator.execute, copy.deepcopy(base_state)): "gematria_integrator"
            }
            
            results = {}
            for future in concurrent.futures.as_completed(futures):
                agent_name = futures[future]
                try:
                    result = future.result()
                    results[agent_name] = result
                    logger.info(f"✅ {agent_name} completed")
                except Exception as e:
                    logger.error(f"❌ {agent_name} failed: {e}")
        
        logger.info(f"✅ Pattern detection complete: {len(results)} agents")
        return results
        
    except Exception as e:
        logger.error(f"❌ Error detecting patterns: {e}")
        import traceback
        traceback.print_exc()
        return {}


def generate_proofs_concurrently(patterns: Dict) -> Dict:
    """Generate proofs for detected patterns concurrently"""
    logger.info("=" * 60)
    logger.info("PHASE 4: Generating Proofs Concurrently")
    logger.info("=" * 60)
    
    try:
        from agents.proof import ProofAgent
        from agents.validation_engine import ValidationEngineAgent
        
        proof_agent = ProofAgent()
        validation_engine = ValidationEngineAgent()
        
        # Extract patterns from results
        pattern_data = []
        for agent_result in patterns.values():
            if isinstance(agent_result, dict) and agent_result.get("results"):
                for result in agent_result["results"]:
                    if result.get("patterns"):
                        pattern_data.extend(result["patterns"])
        
        if not pattern_data:
            logger.warning("⚠️  No patterns found for proof generation")
            return {}
        
        logger.info(f"📋 Generating proofs for {len(pattern_data)} patterns")
        
        # Generate proofs concurrently
        from agents.orchestrator import AgentState
        
        proofs = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for pattern in pattern_data:
                state: AgentState = {
                    "task": {"type": "proof", "pattern": pattern},
                    "data": [pattern],
                    "context": {},
                    "results": [],
                    "cost": 0.0,
                    "status": "pending",
                    "memory_id": None
                }
                future = executor.submit(proof_agent.execute, state)
                futures.append(future)
            
            # Collect proofs
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                try:
                    result = future.result()
                    if result.get("results"):
                        proofs.extend(result["results"])
                    logger.info(f"✅ Proof {i+1}/{len(futures)} generated")
                except Exception as e:
                    logger.error(f"❌ Proof generation failed: {e}")
        
        logger.info(f"✅ Generated {len(proofs)} proofs")
        return {"proofs": proofs, "total": len(proofs)}
        
    except Exception as e:
        logger.error(f"❌ Error generating proofs: {e}")
        import traceback
        traceback.print_exc()
        return {}


def create_unifications(proofs: Dict) -> Dict:
    """Create unifications from proofs"""
    logger.info("=" * 60)
    logger.info("PHASE 5: Creating Unifications")
    logger.info("=" * 60)
    
    try:
        from agents.inference import InferenceAgent
        
        inference_agent = InferenceAgent()
        
        # Extract proofs
        proof_data = proofs.get("proofs", [])
        
        if not proof_data:
            logger.warning("⚠️  No proofs found for unification")
            return {}
        
        logger.info(f"📋 Creating unifications from {len(proof_data)} proofs")
        
        # Create unifications
        from agents.orchestrator import AgentState
        
        state: AgentState = {
            "task": {"type": "unification", "proofs": proof_data},
            "data": proof_data,
            "context": {},
            "results": [],
            "cost": 0.0,
            "status": "pending",
            "memory_id": None
        }
        
        result = inference_agent.execute(state)
        
        unifications = result.get("results", [])
        logger.info(f"✅ Created {len(unifications)} unifications")
        
        return {"unifications": unifications, "total": len(unifications)}
        
    except Exception as e:
        logger.error(f"❌ Error creating unifications: {e}")
        import traceback
        traceback.print_exc()
        return {}


def main():
    """Main execution function"""
    logger.info("=" * 60)
    logger.info("CRITICAL PATH EXECUTION - SELF-SCAFFOLDING GEMATRIA HIVE")
    logger.info("=" * 60)
    logger.info("")
    
    start_time = datetime.now()
    
    # Phase 1: Pull all ingestions
    data = pull_all_ingestions()
    logger.info("")
    
    if not data:
        logger.warning("⚠️  No data found. Running with empty dataset.")
        data = []
    
    # Phase 2: Run all agents concurrently
    agent_results = run_agents_concurrently(data)
    logger.info("")
    
    # Phase 3: Detect patterns concurrently
    pattern_results = detect_patterns_concurrently(data)
    logger.info("")
    
    # Phase 4: Generate proofs concurrently
    proof_results = generate_proofs_concurrently(pattern_results)
    logger.info("")
    
    # Phase 5: Create unifications
    unification_results = create_unifications(proof_results)
    logger.info("")
    
    # Summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    logger.info("=" * 60)
    logger.info("CRITICAL PATH EXECUTION SUMMARY")
    logger.info("=" * 60)
    logger.info(f"⏱️  Total Duration: {duration:.2f} seconds")
    logger.info(f"📊 Data Items: {len(data)}")
    logger.info(f"🤖 Agent Tasks: {agent_results.get('total_tasks', 0)}")
    logger.info(f"🔍 Patterns Detected: {len(pattern_results)}")
    logger.info(f"✅ Proofs Generated: {proof_results.get('total', 0)}")
    logger.info(f"🔗 Unifications Created: {unification_results.get('total', 0)}")
    logger.info("")
    
    # Save results
    results_file = f"critical_path_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        results = {
            "execution_time": duration,
            "data_count": len(data),
            "agent_results": agent_results,
            "pattern_results": pattern_results,
            "proof_results": proof_results,
            "unification_results": unification_results,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"📄 Results saved to: {results_file}")
    except Exception as e:
        logger.warning(f"⚠️  Could not save results: {e}")
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("✅ CRITICAL PATH EXECUTION COMPLETE!")
    logger.info("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())


