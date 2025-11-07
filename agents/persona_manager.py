"""
Persona Manager Agent
Purpose: Create master personas system for Einstein, Tesla, Pythagoras, etc. with contributions and frameworks
- Create persona tables for different domains
- Store contributions, models, frameworks
- Link personas to knowledge domains
- Create persona index

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
from typing import Dict, List, Optional
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


class PersonaManagerAgent(DataTable):
    """
    Persona Manager Agent - Manages master personas
    """
    
    def __init__(self):
        """Initialize persona manager agent"""
        super().__init__('personas')
        self.name = "persona_manager_agent"
        
        # Master personas data
        self.master_personas = {
            # Physics
            'einstein': {
                'name': 'Albert Einstein',
                'domain': 'physics',
                'contributions': [
                    'Theory of Relativity',
                    'E=mc²',
                    'Photoelectric Effect',
                    'Brownian Motion',
                    'Mass-Energy Equivalence',
                    'Space-Time Continuum',
                    'Quantum Mechanics'
                ],
                'models': [
                    'Special Relativity',
                    'General Relativity',
                    'Einstein Field Equations',
                    'Einstein-Maxwell Equations'
                ],
                'frameworks': [
                    'Relativistic Physics',
                    'Quantum Theory',
                    'Unified Field Theory'
                ],
                'knowledge': {
                    'theories': ['Relativity', 'Quantum Mechanics', 'Unified Field Theory'],
                    'equations': ['E=mc²', 'Gμν = 8πG/c⁴ Tμν'],
                    'concepts': ['Space-Time', 'Mass-Energy Equivalence', 'Photoelectric Effect']
                },
                'subject_tags': ['physics', 'relativity', 'quantum', 'mathematics', 'cosmology']
            },
            'tesla': {
                'name': 'Nikola Tesla',
                'domain': 'physics',
                'contributions': [
                    'Alternating Current (AC)',
                    'Tesla Coil',
                    'Wireless Power Transmission',
                    'Radio Technology',
                    'Electric Motor',
                    'Resonance',
                    'Frequency'
                ],
                'models': [
                    'AC Power System',
                    'Tesla Coil',
                    'Wireless Transmission',
                    'Resonant Frequency'
                ],
                'frameworks': [
                    'Electrical Engineering',
                    'Wireless Communication',
                    'Resonance Theory'
                ],
                'knowledge': {
                    'theories': ['AC Power', 'Resonance', 'Wireless Transmission'],
                    'inventions': ['Tesla Coil', 'AC Motor', 'Radio'],
                    'concepts': ['Frequency', 'Resonance', 'Vibration', '369']
                },
                'subject_tags': ['physics', 'engineering', 'electricity', 'resonance', 'frequency', '369']
            },
            # Mathematics
            'pythagoras': {
                'name': 'Pythagoras',
                'domain': 'mathematics',
                'contributions': [
                    'Pythagorean Theorem',
                    'Pythagorean Tuning',
                    'Sacred Geometry',
                    'Number Theory',
                    'Harmonic Ratios',
                    'Golden Ratio',
                    'Mathematical Mysticism'
                ],
                'models': [
                    'Pythagorean Theorem',
                    'Pythagorean Tuning',
                    'Sacred Geometry',
                    'Number Theory'
                ],
                'frameworks': [
                    'Pythagorean Mathematics',
                    'Sacred Geometry',
                    'Harmonic Theory'
                ],
                'knowledge': {
                    'theories': ['Pythagorean Theorem', 'Sacred Geometry', 'Harmonic Ratios'],
                    'theorems': ['a² + b² = c²'],
                    'concepts': ['Golden Ratio', 'Harmonic Ratios', 'Sacred Numbers', '369']
                },
                'subject_tags': ['mathematics', 'geometry', 'sacred geometry', 'harmonics', '369']
            },
            # Gematria
            'agrippa': {
                'name': 'Heinrich Cornelius Agrippa',
                'domain': 'gematria',
                'contributions': [
                    'Three Books of Occult Philosophy',
                    'Latin Gematria',
                    'Qabala Simplex',
                    'Gematria Methods',
                    'Occult Philosophy'
                ],
                'models': [
                    'Latin Gematria',
                    'Qabala Simplex',
                    'Gematria Calculation Methods'
                ],
                'frameworks': [
                    'Occult Philosophy',
                    'Gematria',
                    'Kabbalah'
                ],
                'knowledge': {
                    'theories': ['Latin Gematria', 'Qabala Simplex', 'Gematria Methods'],
                    'books': ['Three Books of Occult Philosophy'],
                    'concepts': ['Gematria', 'Kabbalah', 'Occult Philosophy']
                },
                'subject_tags': ['gematria', 'kabbalah', 'occult', 'philosophy', 'latin']
            },
            # Hermetic
            'thoth': {
                'name': 'Thoth / Hermes Trismegistus',
                'domain': 'hermetic',
                'contributions': [
                    'Emerald Tablets',
                    'Hermetic Principles',
                    'As Above So Below',
                    'Alchemy',
                    'Sacred Knowledge'
                ],
                'models': [
                    'Hermetic Principles',
                    'Emerald Tablets',
                    'Alchemy'
                ],
                'frameworks': [
                    'Hermeticism',
                    'Alchemy',
                    'Sacred Knowledge'
                ],
                'knowledge': {
                    'theories': ['Hermetic Principles', 'As Above So Below', 'Alchemy'],
                    'texts': ['Emerald Tablets', 'Corpus Hermeticum'],
                    'concepts': ['Hermeticism', 'Alchemy', 'Sacred Knowledge']
                },
                'subject_tags': ['hermetic', 'alchemy', 'sacred', 'philosophy', 'ancient']
            },
            # Schumann Resonance
            'schumann': {
                'name': 'Winfried Otto Schumann',
                'domain': 'physics',
                'contributions': [
                    'Schumann Resonance',
                    'Earth Resonance Frequency',
                    '7.83 Hz Frequency',
                    'Electromagnetic Resonance'
                ],
                'models': [
                    'Schumann Resonance',
                    'Earth Resonance Model'
                ],
                'frameworks': [
                    'Electromagnetic Resonance',
                    'Earth Frequency'
                ],
                'knowledge': {
                    'theories': ['Schumann Resonance', 'Earth Frequency'],
                    'frequencies': ['7.83 Hz', '14.3 Hz', '20.8 Hz', '27.3 Hz', '33.8 Hz'],
                    'concepts': ['Earth Resonance', 'Electromagnetic Resonance', 'Frequency']
                },
                'subject_tags': ['physics', 'resonance', 'frequency', 'earth', 'electromagnetic']
            }
        }
        
        logger.info(f"Initialized {self.name}")
    
    def initialize_personas(self):
        """Initialize master personas in database."""
        if not self.supabase:
            logger.warning("Supabase not available, personas not initialized")
            return
        
        try:
            for persona_key, persona_data in self.master_personas.items():
                # Check if persona already exists
                existing = self.supabase.table('personas')\
                    .select('id')\
                    .eq('name', persona_data['name'])\
                    .limit(1)\
                    .execute()
                
                if existing.data:
                    # Update existing
                    self.supabase.table('personas')\
                        .update({
                            'domain': persona_data['domain'],
                            'contributions': persona_data['contributions'],
                            'models': persona_data['models'],
                            'frameworks': persona_data['frameworks'],
                            'knowledge': persona_data['knowledge'],
                            'subject_tags': persona_data['subject_tags']
                        })\
                        .eq('name', persona_data['name'])\
                        .execute()
                    
                    logger.info(f"Updated persona: {persona_data['name']}")
                else:
                    # Create new
                    self.supabase.table('personas').insert({
                        'name': persona_data['name'],
                        'domain': persona_data['domain'],
                        'contributions': persona_data['contributions'],
                        'models': persona_data['models'],
                        'frameworks': persona_data['frameworks'],
                        'knowledge': persona_data['knowledge'],
                        'subject_tags': persona_data['subject_tags']
                    }).execute()
                    
                    logger.info(f"Created persona: {persona_data['name']}")
            
            logger.info("Master personas initialized in database")
        except Exception as e:
            logger.error(f"Error initializing personas: {e}")
    
    def get_persona(self, name: str) -> Optional[Dict]:
        """
        Get persona by name.
        
        Args:
            name: Persona name
            
        Returns:
            Persona dictionary or None
        """
        if not self.supabase:
            return None
        
        try:
            result = self.supabase.table('personas')\
                .select('*')\
                .eq('name', name)\
                .limit(1)\
                .execute()
            
            if result.data:
                return result.data[0]
            
            return None
        except Exception as e:
            logger.error(f"Error getting persona: {e}")
            return None
    
    def get_personas_by_domain(self, domain: str) -> List[Dict]:
        """
        Get personas by domain.
        
        Args:
            domain: Domain name (e.g., 'physics', 'mathematics', 'gematria')
            
        Returns:
            List of persona dictionaries
        """
        if not self.supabase:
            return []
        
        try:
            result = self.supabase.table('personas')\
                .select('*')\
                .eq('domain', domain)\
                .execute()
            
            if result.data:
                return result.data
            
            return []
        except Exception as e:
            logger.error(f"Error getting personas by domain: {e}")
            return []
    
    def get_personas_by_tag(self, tag: str) -> List[Dict]:
        """
        Get personas by subject tag.
        
        Args:
            tag: Subject tag
            
        Returns:
            List of persona dictionaries
        """
        if not self.supabase:
            return []
        
        try:
            result = self.supabase.table('personas')\
                .select('*')\
                .contains('subject_tags', [tag])\
                .execute()
            
            if result.data:
                return result.data
            
            return []
        except Exception as e:
            logger.error(f"Error getting personas by tag: {e}")
            return []
    
    def validate(self, data: Dict, record_id: Optional[str] = None) -> Dict:
        """Validate persona data."""
        errors = []
        
        # Required fields
        if 'name' not in data or not data['name']:
            errors.append("name is required")
        
        if 'domain' not in data or not data['domain']:
            errors.append("domain is required")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def apply_highest_persona_thinking(self, query: str, context: Dict = None) -> Dict:
        """
        Apply highest persona thinking to a query
        
        Uses first principles and highest-level thinking from relevant personas
        
        Args:
            query: Query string
            context: Optional context dictionary
            
        Returns:
            Dictionary with persona insights
        """
        insights = {}
        
        # Get relevant personas based on query
        relevant_personas = self._get_relevant_personas(query)
        
        # Apply first principles from each persona
        for persona_name in relevant_personas:
            persona = self.get_persona(persona_name)
            if persona:
                # Apply first principles thinking
                first_principles = self._extract_first_principles(persona, query)
                
                # Get persona framework insights
                framework_insights = self._apply_persona_framework(persona, query)
                
                insights[persona_name] = {
                    'persona': persona,
                    'first_principles': first_principles,
                    'framework_insights': framework_insights,
                    'perspective': f"{persona.get('name', persona_name)} perspective"
                }
        
        return {
            'query': query,
            'personas_used': relevant_personas,
            'insights': insights,
            'synthesis': self._synthesize_persona_insights(insights)
        }
    
    def _get_relevant_personas(self, query: str) -> List[str]:
        """Get relevant personas for a query"""
        query_lower = query.lower()
        relevant = []
        
        # Check for domain keywords
        if any(kw in query_lower for kw in ['physics', 'relativity', 'quantum', 'einstein']):
            relevant.append('einstein')
        
        if any(kw in query_lower for kw in ['electricity', 'resonance', 'frequency', '369', 'tesla']):
            relevant.append('tesla')
        
        if any(kw in query_lower for kw in ['geometry', 'mathematics', 'pythagoras', 'theorem', '369']):
            relevant.append('pythagoras')
        
        if any(kw in query_lower for kw in ['gematria', 'kabbalah', 'occult', 'agrippa']):
            relevant.append('agrippa')
        
        if any(kw in query_lower for kw in ['hermetic', 'alchemy', 'thoth', 'hermes']):
            relevant.append('thoth')
        
        if any(kw in query_lower for kw in ['schumann', 'resonance', 'frequency', 'earth']):
            relevant.append('schumann')
        
        # Default to all personas if none match
        if not relevant:
            relevant = ['einstein', 'tesla', 'pythagoras']
        
        return relevant
    
    def _extract_first_principles(self, persona: Dict, query: str) -> List[str]:
        """Extract first principles from persona for query"""
        principles = []
        
        # Get persona frameworks
        frameworks = persona.get('frameworks', [])
        contributions = persona.get('contributions', [])
        models = persona.get('models', [])
        
        # Build first principles
        principles.append(f"Core domain: {persona.get('domain', 'unknown')}")
        principles.append(f"Key frameworks: {', '.join(frameworks[:3])}")
        principles.append(f"Fundamental contributions: {', '.join(contributions[:3])}")
        principles.append(f"Core models: {', '.join(models[:3])}")
        
        return principles
    
    def _apply_persona_framework(self, persona: Dict, query: str) -> Dict:
        """Apply persona framework to query"""
        return {
            'domain': persona.get('domain', 'unknown'),
            'frameworks': persona.get('frameworks', []),
            'models': persona.get('models', []),
            'contributions': persona.get('contributions', []),
            'knowledge': persona.get('knowledge', {})
        }
    
    def _synthesize_persona_insights(self, insights: Dict) -> str:
        """Synthesize insights from multiple personas"""
        synthesis_parts = []
        synthesis_parts.append("Synthesis of highest persona thinking:")
        
        for persona_name, insight in insights.items():
            synthesis_parts.append(f"\n{persona_name}:")
            synthesis_parts.append(f"  First principles: {', '.join(insight.get('first_principles', [])[:2])}")
        
        return "\n".join(synthesis_parts)
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute persona management task.
        
        Args:
            state: Agent state with task information
            
        Returns:
            Updated state with persona data
        """
        task = state.get("task", {})
        action = task.get("action", "initialize")
        
        logger.info(f"Persona manager agent: Executing action {action}")
        
        try:
            if action == "initialize":
                # Initialize personas
                self.initialize_personas()
                
                state["context"]["personas_initialized"] = True
                state["results"].append({
                    "agent": self.name,
                    "action": "initialize_personas",
                    "status": "completed"
                })
            
            elif action == "get_persona":
                # Get persona by name
                name = task.get("name")
                
                if name:
                    persona = self.get_persona(name)
                    state["context"]["persona"] = persona
                    state["results"].append({
                        "agent": self.name,
                        "action": "get_persona",
                        "persona": persona
                    })
            
            elif action == "get_by_domain":
                # Get personas by domain
                domain = task.get("domain")
                
                if domain:
                    personas = self.get_personas_by_domain(domain)
                    state["context"]["personas"] = personas
                    state["results"].append({
                        "agent": self.name,
                        "action": "get_by_domain",
                        "personas": personas
                    })
            
            elif action == "get_by_tag":
                # Get personas by tag
                tag = task.get("tag")
                
                if tag:
                    personas = self.get_personas_by_tag(tag)
                    state["context"]["personas"] = personas
                    state["results"].append({
                        "agent": self.name,
                        "action": "get_by_tag",
                        "personas": personas
                    })
            
            elif action == "apply_highest_persona_thinking":
                # Apply highest persona thinking to query
                query = task.get("query", "")
                context = state.get("context", {})
                
                if query:
                    insights = self.apply_highest_persona_thinking(query, context)
                    state["context"]["persona_insights"] = insights
                    state["results"].append({
                        "agent": self.name,
                        "action": "apply_highest_persona_thinking",
                        "insights": insights
                    })
            
            logger.info(f"Persona management complete: {action}")
            
        except Exception as e:
            logger.error(f"Persona management error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

