"""
Integration Tests

Tests full system integration and workflows.
"""

import unittest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()


class TestIntegration(unittest.TestCase):
    """Test suite for system integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        from agents.orchestrator import get_orchestrator
        from core.gematria_engine import get_gematria_engine
        from core.conductor import get_unified_conductor
        
        self.orchestrator = get_orchestrator()
        self.gematria_engine = get_gematria_engine()
        self.conductor = get_unified_conductor()
    
    def test_full_pipeline(self):
        """Test full extraction -> distillation -> ingestion pipeline"""
        task = {
            "type": "extraction",
            "source": "test",
            "description": "Test pipeline"
        }
        
        result = self.orchestrator.execute(task)
        self.assertIsNotNone(result)
        self.assertIn('status', result)
    
    def test_gematria_calculation_integration(self):
        """Test gematria calculation integration"""
        result = self.gematria_engine.calculate_all("GEMATRIA")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
    
    def test_agent_orchestration(self):
        """Test agent orchestration"""
        task = {
            "type": "inference",
            "query": "test query",
            "description": "Test orchestration"
        }
        
        result = self.orchestrator.execute(task)
        self.assertIsNotNone(result)
        self.assertIn('status', result)
    
    def test_cost_tracking(self):
        """Test cost tracking integration"""
        if 'cost_manager' in self.orchestrator.agents:
            cost_manager = self.orchestrator.agents['cost_manager']
            cost_summary = cost_manager.get_cost_summary()
            self.assertIsNotNone(cost_summary)


if __name__ == '__main__':
    unittest.main()

