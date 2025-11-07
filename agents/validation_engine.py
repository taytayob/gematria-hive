"""
Validation Engine Agent
Purpose: Implement proofs and validation system with baseline checking and accuracy tracking
- Proof building engine
- Validation scoring
- Baseline checking
- Self-validation
- Accuracy tracking
- Alert on 100% accuracy achievement

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from agents.orchestrator import AgentState
from core.data_table import DataTable

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

try:
    from supabase import create_client, Client
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    if SUPABASE_URL and SUPABASE_KEY:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        HAS_SUPABASE = True
    else:
        HAS_SUPABASE = False
        supabase = None
except Exception:
    HAS_SUPABASE = False
    supabase = None

logger = logging.getLogger(__name__)


class ValidationEngineAgent(DataTable):
    """
    Validation Engine Agent - Validates proofs and tracks accuracy
    """
    
    def __init__(self):
        """Initialize validation engine agent"""
        super().__init__('validations')
        self.name = "validation_engine_agent"
        self.proofs_table = DataTable('proofs')
        self.baselines_table = DataTable('baselines')
        logger.info(f"Initialized {self.name}")
    
    def check_baseline(self, entity_type: str, entity_id: str, value: Dict) -> Tuple[bool, Optional[str], float]:
        """
        Check entity against baseline.
        
        Args:
            entity_type: Entity type
            entity_id: Entity ID
            value: Value to check
            
        Returns:
            Tuple of (matches, baseline_id, similarity_score)
        """
        if not self.supabase:
            return (False, None, 0.0)
        
        try:
            # Get baselines for entity type
            result = self.supabase.table('baselines')\
                .select('*')\
                .eq('baseline_type', entity_type)\
                .execute()
            
            if result.data:
                best_match = None
                best_score = 0.0
                
                for baseline in result.data:
                    baseline_value = baseline.get('value', {})
                    if isinstance(baseline_value, dict):
                        # Calculate similarity
                        similarity = self._calculate_similarity(value, baseline_value)
                        if similarity > best_score:
                            best_score = similarity
                            best_match = baseline
                
                if best_match and best_score >= 0.8:  # 80% similarity threshold
                    return (True, best_match['id'], best_score)
            
            return (False, None, 0.0)
        except Exception as e:
            logger.error(f"Error checking baseline: {e}")
            return (False, None, 0.0)
    
    def _calculate_similarity(self, value1: Dict, value2: Dict) -> float:
        """
        Calculate similarity between two values.
        
        Args:
            value1: First value dictionary
            value2: Second value dictionary
            
        Returns:
            Similarity score (0.0 to 1.0)
        """
        if not isinstance(value1, dict) or not isinstance(value2, dict):
            return 0.0
        
        # Simple similarity calculation
        # Count matching keys
        keys1 = set(value1.keys())
        keys2 = set(value2.keys())
        common_keys = keys1.intersection(keys2)
        
        if not common_keys:
            return 0.0
        
        # Count matching values
        matches = 0
        for key in common_keys:
            if value1[key] == value2[key]:
                matches += 1
        
        # Calculate similarity
        similarity = matches / max(len(keys1), len(keys2), 1)
        
        return similarity
    
    def validate_entity(self, entity_type: str, entity_id: str, entity_data: Dict) -> Dict:
        """
        Validate an entity.
        
        Args:
            entity_type: Entity type
            entity_id: Entity ID
            entity_data: Entity data
            
        Returns:
            Validation result dictionary
        """
        if not self.supabase:
            return {
                'valid': False,
                'score': 0.0,
                'passed': False,
                'notes': 'Supabase not available'
            }
        
        try:
            # Check baseline
            matches_baseline, baseline_id, similarity = self.check_baseline(entity_type, entity_id, entity_data)
            
            # Calculate validation score
            score = similarity if matches_baseline else 0.5  # Default score if no baseline match
            
            # Determine if passed
            passed = score >= 0.7  # 70% threshold
            
            # Create validation record
            validation_data = {
                'validation_type': entity_type,
                'entity_id': entity_id,
                'entity_type': entity_type,
                'score': score,
                'passed': passed,
                'baseline_id': baseline_id,
                'notes': f"Baseline match: {matches_baseline}, Similarity: {similarity:.2f}"
            }
            
            result = self.create(validation_data)
            
            if result:
                logger.info(f"Validated {entity_type} {entity_id}: score={score:.2f}, passed={passed}")
                return {
                    'valid': True,
                    'score': score,
                    'passed': passed,
                    'baseline_id': baseline_id,
                    'validation_id': result['id']
                }
            
            return {
                'valid': False,
                'score': score,
                'passed': passed,
                'notes': 'Validation record not created'
            }
        except Exception as e:
            logger.error(f"Error validating entity: {e}")
            return {
                'valid': False,
                'score': 0.0,
                'passed': False,
                'notes': f"Error: {str(e)}"
            }
    
    def create_proof(self, proof_name: str, proof_type: str, theorem: str, 
                     evidence: Dict, sources: List[str] = None, 
                     research_topic_id: Optional[str] = None) -> Optional[str]:
        """
        Create a proof.
        
        Args:
            proof_name: Proof name
            proof_type: Proof type ('gematria', 'phonetic', 'symbolic', etc.)
            theorem: Theorem statement
            evidence: Evidence dictionary
            sources: List of source IDs
            research_topic_id: Research topic ID
            
        Returns:
            Proof ID or None
        """
        if not self.supabase:
            return None
        
        try:
            # Calculate accuracy metric
            accuracy = self._calculate_accuracy(evidence)
            
            # Calculate efficiency score
            efficiency = self._calculate_efficiency(evidence)
            
            proof_data = {
                'proof_name': proof_name,
                'proof_type': proof_type,
                'theorem': theorem,
                'evidence': evidence,
                'accuracy_metric': accuracy,
                'efficiency_score': efficiency,
                'sources': sources or [],
                'research_topic_id': research_topic_id
            }
            
            result = self.proofs_table.create(proof_data)
            
            if result:
                proof_id = result['id']
                logger.info(f"Created proof: {proof_name} (accuracy: {accuracy:.2f}, efficiency: {efficiency:.2f})")
                
                # Check if accuracy is 100%
                if accuracy >= 1.0:
                    logger.warning(f"🎉 100% ACCURACY ACHIEVED: {proof_name}")
                    self._alert_100_percent_accuracy(proof_name, proof_id, accuracy)
                
                return proof_id
            
            return None
        except Exception as e:
            logger.error(f"Error creating proof: {e}")
            return None
    
    def _calculate_accuracy(self, evidence: Dict) -> float:
        """
        Calculate accuracy metric from evidence.
        
        Args:
            evidence: Evidence dictionary
            
        Returns:
            Accuracy score (0.0 to 1.0)
        """
        if not isinstance(evidence, dict):
            return 0.0
        
        # Simple accuracy calculation
        # Count valid evidence points
        valid_points = 0
        total_points = 0
        
        for key, value in evidence.items():
            total_points += 1
            if value:
                if isinstance(value, (int, float)):
                    if value > 0:
                        valid_points += 1
                elif isinstance(value, (str, list, dict)):
                    if value:
                        valid_points += 1
                elif isinstance(value, bool):
                    if value:
                        valid_points += 1
        
        if total_points == 0:
            return 0.0
        
        accuracy = valid_points / total_points
        return accuracy
    
    def _calculate_efficiency(self, evidence: Dict) -> float:
        """
        Calculate efficiency score from evidence.
        
        Args:
            evidence: Evidence dictionary
            
        Returns:
            Efficiency score (0.0 to 1.0)
        """
        if not isinstance(evidence, dict):
            return 0.0
        
        # Simple efficiency calculation
        # Based on evidence density and quality
        evidence_keys = len(evidence.keys())
        evidence_values = sum(1 for v in evidence.values() if v)
        
        if evidence_keys == 0:
            return 0.0
        
        efficiency = evidence_values / evidence_keys
        return efficiency
    
    def _alert_100_percent_accuracy(self, proof_name: str, proof_id: str, accuracy: float):
        """
        Alert on 100% accuracy achievement.
        
        Args:
            proof_name: Proof name
            proof_id: Proof ID
            accuracy: Accuracy score
        """
        logger.warning(f"🎉 100% ACCURACY ACHIEVED: {proof_name} (ID: {proof_id}, Accuracy: {accuracy:.2f})")
        
        # Log to hunches table
        if self.supabase:
            try:
                self.supabase.table('hunches').insert({
                    'content': f"🎉 100% ACCURACY ACHIEVED: {proof_name} (ID: {proof_id}, Accuracy: {accuracy:.2f})",
                    'timestamp': datetime.utcnow().isoformat(),
                    'status': 'completed',
                    'cost': 0.0
                }).execute()
            except Exception as e:
                logger.error(f"Error logging 100% accuracy alert: {e}")
    
    def validate_proof(self, proof_id: str) -> Dict:
        """
        Validate a proof.
        
        Args:
            proof_id: Proof ID
            
        Returns:
            Validation result dictionary
        """
        if not self.supabase:
            return {
                'valid': False,
                'score': 0.0,
                'passed': False,
                'notes': 'Supabase not available'
            }
        
        try:
            # Get proof
            proof = self.proofs_table.read(proof_id)
            
            if not proof:
                return {
                    'valid': False,
                    'score': 0.0,
                    'passed': False,
                    'notes': 'Proof not found'
                }
            
            # Validate proof
            evidence = proof.get('evidence', {})
            accuracy = proof.get('accuracy_metric', 0.0)
            efficiency = proof.get('efficiency_score', 0.0)
            
            # Calculate validation score
            score = (accuracy * 0.7) + (efficiency * 0.3)
            
            # Determine if passed
            passed = score >= 0.7  # 70% threshold
            
            # Create validation record
            validation_data = {
                'validation_type': 'proof',
                'entity_id': proof_id,
                'entity_type': 'proof',
                'score': score,
                'passed': passed,
                'notes': f"Proof validation: accuracy={accuracy:.2f}, efficiency={efficiency:.2f}"
            }
            
            result = self.create(validation_data)
            
            if result:
                logger.info(f"Validated proof {proof_id}: score={score:.2f}, passed={passed}")
                return {
                    'valid': True,
                    'score': score,
                    'passed': passed,
                    'validation_id': result['id']
                }
            
            return {
                'valid': False,
                'score': score,
                'passed': passed,
                'notes': 'Validation record not created'
            }
        except Exception as e:
            logger.error(f"Error validating proof: {e}")
            return {
                'valid': False,
                'score': 0.0,
                'passed': False,
                'notes': f"Error: {str(e)}"
            }
    
    def get_validation_stats(self) -> Dict:
        """
        Get validation statistics.
        
        Returns:
            Dictionary with validation statistics
        """
        if not self.supabase:
            return {}
        
        try:
            # Get all validations
            result = self.supabase.table('validations')\
                .select('*')\
                .execute()
            
            if result.data:
                total = len(result.data)
                passed = sum(1 for v in result.data if v.get('passed', False))
                failed = total - passed
                avg_score = sum(v.get('score', 0.0) for v in result.data) / total if total > 0 else 0.0
                
                return {
                    'total_validations': total,
                    'passed': passed,
                    'failed': failed,
                    'pass_rate': passed / total if total > 0 else 0.0,
                    'average_score': avg_score
                }
            
            return {
                'total_validations': 0,
                'passed': 0,
                'failed': 0,
                'pass_rate': 0.0,
                'average_score': 0.0
            }
        except Exception as e:
            logger.error(f"Error getting validation stats: {e}")
            return {}
    
    def validate(self, data: Dict, record_id: Optional[str] = None) -> Dict:
        """Validate validation data."""
        errors = []
        
        # Required fields
        if 'validation_type' not in data or not data['validation_type']:
            errors.append("validation_type is required")
        
        if 'entity_id' not in data or not data['entity_id']:
            errors.append("entity_id is required")
        
        if 'entity_type' not in data or not data['entity_type']:
            errors.append("entity_type is required")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute validation task.
        
        Args:
            state: Agent state with task information
            
        Returns:
            Updated state with validation results
        """
        task = state.get("task", {})
        action = task.get("action", "validate")
        
        logger.info(f"Validation engine agent: Executing action {action}")
        
        try:
            if action == "validate_entity":
                # Validate entity
                entity_type = task.get("entity_type")
                entity_id = task.get("entity_id")
                entity_data = task.get("entity_data", {})
                
                if entity_type and entity_id:
                    validation_result = self.validate_entity(entity_type, entity_id, entity_data)
                    state["context"]["validation_result"] = validation_result
                    state["results"].append({
                        "agent": self.name,
                        "action": "validate_entity",
                        "result": validation_result
                    })
            
            elif action == "create_proof":
                # Create proof
                proof_name = task.get("proof_name")
                proof_type = task.get("proof_type")
                theorem = task.get("theorem")
                evidence = task.get("evidence", {})
                sources = task.get("sources", [])
                research_topic_id = task.get("research_topic_id")
                
                if proof_name and proof_type and theorem:
                    proof_id = self.create_proof(proof_name, proof_type, theorem, evidence, sources, research_topic_id)
                    state["context"]["proof_id"] = proof_id
                    state["results"].append({
                        "agent": self.name,
                        "action": "create_proof",
                        "proof_id": proof_id
                    })
            
            elif action == "validate_proof":
                # Validate proof
                proof_id = task.get("proof_id")
                
                if proof_id:
                    validation_result = self.validate_proof(proof_id)
                    state["context"]["validation_result"] = validation_result
                    state["results"].append({
                        "agent": self.name,
                        "action": "validate_proof",
                        "result": validation_result
                    })
            
            elif action == "get_stats":
                # Get validation statistics
                stats = self.get_validation_stats()
                state["context"]["validation_stats"] = stats
                state["results"].append({
                    "agent": self.name,
                    "action": "get_stats",
                    "stats": stats
                })
            
            logger.info(f"Validation complete: {action}")
            
        except Exception as e:
            logger.error(f"Validation error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

