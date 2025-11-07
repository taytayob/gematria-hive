"""
Unit Tests for Agents

Tests all agent implementations for correctness and integration.
"""

import unittest
import os
import sys
from typing import Dict

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from agents.orchestrator import AgentState, get_orchestrator


class TestAgents(unittest.TestCase):
    """Test suite for all agents"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.orchestrator = get_orchestrator()
        self.test_state: AgentState = {
            "task": {"type": "test"},
            "data": [],
            "context": {},
            "results": [],
            "cost": 0.0,
            "status": "pending",
            "memory_id": None
        }
    
    def test_orchestrator_initialization(self):
        """Test orchestrator initializes correctly"""
        self.assertIsNotNone(self.orchestrator)
        self.assertIsNotNone(self.orchestrator.agents)
        self.assertGreater(len(self.orchestrator.agents), 0)
    
    def test_extraction_agent(self):
        """Test extraction agent"""
        if 'extraction' in self.orchestrator.agents:
            agent = self.orchestrator.agents['extraction']
            state = agent.execute(self.test_state.copy())
            self.assertIsNotNone(state)
            self.assertIn('status', state)
    
    def test_distillation_agent(self):
        """Test distillation agent"""
        if 'distillation' in self.orchestrator.agents:
            agent = self.orchestrator.agents['distillation']
            state = agent.execute(self.test_state.copy())
            self.assertIsNotNone(state)
            self.assertIn('status', state)
    
    def test_ingestion_agent(self):
        """Test ingestion agent"""
        if 'ingestion' in self.orchestrator.agents:
            agent = self.orchestrator.agents['ingestion']
            state = agent.execute(self.test_state.copy())
            self.assertIsNotNone(state)
            self.assertIn('status', state)
    
    def test_inference_agent(self):
        """Test inference agent"""
        if 'inference' in self.orchestrator.agents:
            agent = self.orchestrator.agents['inference']
            state = agent.execute(self.test_state.copy())
            self.assertIsNotNone(state)
            self.assertIn('status', state)
    
    def test_proof_agent(self):
        """Test proof agent"""
        if 'proof' in self.orchestrator.agents:
            agent = self.orchestrator.agents['proof']
            test_state = self.test_state.copy()
            test_state['task'] = {"type": "proof", "theorem": "test theorem"}
            state = agent.execute(test_state)
            self.assertIsNotNone(state)
            self.assertIn('status', state)
    
    def test_affinity_agent(self):
        """Test affinity agent"""
        if 'affinity' in self.orchestrator.agents:
            agent = self.orchestrator.agents['affinity']
            state = agent.execute(self.test_state.copy())
            self.assertIsNotNone(state)
            self.assertIn('status', state)
    
    def test_pattern_detector(self):
        """Test pattern detector agent"""
        if 'pattern_detector' in self.orchestrator.agents:
            agent = self.orchestrator.agents['pattern_detector']
            state = agent.execute(self.test_state.copy())
            self.assertIsNotNone(state)
            self.assertIn('status', state)
    
    def test_gematria_integrator(self):
        """Test gematria integrator agent"""
        if 'gematria_integrator' in self.orchestrator.agents:
            agent = self.orchestrator.agents['gematria_integrator']
            state = agent.execute(self.test_state.copy())
            self.assertIsNotNone(state)
            self.assertIn('status', state)
    
    def test_cost_manager(self):
        """Test cost manager agent"""
        if 'cost_manager' in self.orchestrator.agents:
            agent = self.orchestrator.agents['cost_manager']
            # Test cost tracking
            cost_summary = agent.get_cost_summary()
            self.assertIsNotNone(cost_summary)
    
    def test_all_agents_registered(self):
        """Test all expected agents are registered"""
        expected_agents = [
            'extraction', 'distillation', 'ingestion', 'inference',
            'proof', 'browser', 'affinity', 'pattern_detector',
            'gematria_integrator', 'cost_manager'
        ]
        
        for agent_name in expected_agents:
            self.assertIn(agent_name, self.orchestrator.agents,
                         f"Agent {agent_name} not registered")


if __name__ == '__main__':
    unittest.main()

