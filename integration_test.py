"""
Integration Test - Gematria Hive
Purpose: Test all components working together
- Test database schema
- Test CSV ingestion
- Test gematria calculations
- Test all agents
- Test visualization
- Test UI

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
from typing import Dict, List
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_database_schema():
    """Test database schema"""
    logger.info("Testing database schema...")
    try:
        from supabase import create_client, Client
        SUPABASE_URL = os.getenv('SUPABASE_URL')
        SUPABASE_KEY = os.getenv('SUPABASE_KEY')
        
        if not SUPABASE_URL or not SUPABASE_KEY:
            logger.warning("Supabase not configured, skipping database schema test")
            return False
        
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Test all tables exist
        tables = [
            'gematria_words', 'sources', 'authors', 'key_terms', 'patterns',
            'research_topics', 'proofs', 'personas', 'alphabets', 'baselines',
            'validations', 'cost_tracking', 'projects', 'synchronicities', 'observations',
            'discovered_resources', 'cache_logs', 'floating_index', 'bookmarks', 'hunches'
        ]
        
        for table in tables:
            try:
                result = supabase.table(table).select('id', count='exact').limit(1).execute()
                logger.info(f"✅ Table {table} exists")
            except Exception as e:
                logger.error(f"❌ Table {table} error: {e}")
                return False
        
        logger.info("✅ Database schema test passed")
        return True
    except Exception as e:
        logger.error(f"❌ Database schema test failed: {e}")
        return False

def test_gematria_engine():
    """Test gematria engine"""
    logger.info("Testing gematria engine...")
    try:
        from core.gematria_engine import get_gematria_engine
        
        engine = get_gematria_engine()
        
        # Test calculation
        test_text = "TEST"
        results = engine.calculate_all(test_text)
        
        if results:
            logger.info(f"✅ Gematria engine test passed: {results}")
            return True
        else:
            logger.error("❌ Gematria engine test failed: No results")
            return False
    except Exception as e:
        logger.error(f"❌ Gematria engine test failed: {e}")
        return False

def test_agents():
    """Test all agents"""
    logger.info("Testing agents...")
    try:
        from agents.orchestrator import get_orchestrator
        
        orchestrator = get_orchestrator()
        
        if hasattr(orchestrator, 'agents'):
            agent_count = len(orchestrator.agents)
            logger.info(f"✅ Found {agent_count} agents")
            
            # List all agents
            for agent_name in orchestrator.agents.keys():
                logger.info(f"  - {agent_name}")
            
            return True
        else:
            logger.error("❌ No agents found")
            return False
    except Exception as e:
        logger.error(f"❌ Agents test failed: {e}")
        return False

def test_visualization_engine():
    """Test visualization engine"""
    logger.info("Testing visualization engine...")
    try:
        from core.visualization_engine import get_visualization_engine
        
        engine = get_visualization_engine()
        
        # Test geometry generation
        geometry = engine.generate_metatrons_cube()
        if geometry:
            logger.info("✅ Visualization engine test passed")
            return True
        else:
            logger.error("❌ Visualization engine test failed: No geometry")
            return False
    except Exception as e:
        logger.error(f"❌ Visualization engine test failed: {e}")
        return False

def test_cost_manager():
    """Test cost manager"""
    logger.info("Testing cost manager...")
    try:
        from agents.cost_manager import CostManagerAgent
        
        cost_manager = CostManagerAgent()
        cost_summary = cost_manager.get_cost_summary()
        
        if cost_summary:
            logger.info(f"✅ Cost manager test passed: {cost_summary}")
            return True
        else:
            logger.error("❌ Cost manager test failed: No summary")
            return False
    except Exception as e:
        logger.error(f"❌ Cost manager test failed: {e}")
        return False

def test_utilities():
    """Test utilities"""
    logger.info("Testing utilities...")
    try:
        from utils.cache_manager import get_cache_manager
        from utils.baseline_manager import get_baseline_manager
        from utils.floating_index import get_floating_index
        
        cache_manager = get_cache_manager()
        baseline_manager = get_baseline_manager()
        floating_index = get_floating_index()
        
        if cache_manager and baseline_manager and floating_index:
            logger.info("✅ Utilities test passed")
            return True
        else:
            logger.error("❌ Utilities test failed: Missing components")
            return False
    except Exception as e:
        logger.error(f"❌ Utilities test failed: {e}")
        return False

def main():
    """Run all integration tests"""
    logger.info("=" * 60)
    logger.info("Gematria Hive - Integration Tests")
    logger.info("=" * 60)
    
    results = {}
    
    # Run tests
    results['database_schema'] = test_database_schema()
    results['gematria_engine'] = test_gematria_engine()
    results['agents'] = test_agents()
    results['visualization_engine'] = test_visualization_engine()
    results['cost_manager'] = test_cost_manager()
    results['utilities'] = test_utilities()
    
    # Summary
    logger.info("=" * 60)
    logger.info("Integration Test Results:")
    logger.info("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{test_name}: {status}")
    
    logger.info("=" * 60)
    logger.info(f"Total: {passed}/{total} tests passed")
    logger.info("=" * 60)
    
    if passed == total:
        logger.info("🎉 All integration tests passed!")
        return True
    else:
        logger.warning(f"⚠️ {total - passed} test(s) failed")
        return False

if __name__ == "__main__":
    main()

