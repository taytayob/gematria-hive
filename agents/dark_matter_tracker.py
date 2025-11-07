"""
Dark Matter Tracker Agent

Purpose: Track hidden patterns, latent connections, and implicit knowledge (dark matter)
- Track patterns that exist but aren't explicitly recognized
- Monitor implicit connections between domains
- Detect latent knowledge and hidden structures
- Quantum inference of unseen patterns
- Multi-perspective dark matter analysis

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
from typing import Dict, List, Optional, Set
from datetime import datetime
from collections import defaultdict

from agents.orchestrator import AgentState

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


class DarkMatterTrackerAgent:
    """
    Dark Matter Tracker Agent - Tracks hidden patterns and latent knowledge
    
    Dark Matter Definition:
    - Patterns that exist but aren't explicitly recognized
    - Implicit connections between domains
    - Latent knowledge structures
    - Hidden relationships in data
    - Quantum-like superposition states of meaning
    """
    
    def __init__(self):
        """Initialize dark matter tracker agent"""
        self.name = "dark_matter_tracker_agent"
        self.supabase = supabase if HAS_SUPABASE else None
        
        # Dark matter patterns cache
        self.dark_matter_patterns: Dict[str, List[Dict]] = defaultdict(list)
        
        # Latent connections graph
        self.latent_connections: Dict[str, Set[str]] = defaultdict(set)
        
        logger.info(f"Initialized {self.name}")
    
    def track_dark_matter_pattern(self, pattern: Dict) -> Optional[str]:
        """
        Track a dark matter pattern (hidden pattern)
        
        Args:
            pattern: Pattern dictionary with:
                - pattern_name: Name of the pattern
                - pattern_type: Type (latent, implicit, hidden, quantum)
                - description: Description
                - elements: List of connected elements
                - confidence: Confidence score (0.0 to 1.0)
                - perspectives: Multi-perspective analysis
                - quantum_state: Quantum-like superposition state
        
        Returns:
            Pattern ID or None
        """
        if not self.supabase:
            # Cache locally if no database
            pattern_id = f"dm_{datetime.utcnow().timestamp()}"
            pattern['id'] = pattern_id
            pattern['created_at'] = datetime.utcnow().isoformat()
            self.dark_matter_patterns[pattern.get('pattern_type', 'unknown')].append(pattern)
            return pattern_id
        
        try:
            # Store in dark_matter_patterns table
            result = self.supabase.table('dark_matter_patterns').insert({
                'pattern_name': pattern.get('pattern_name', ''),
                'pattern_type': pattern.get('pattern_type', 'latent'),
                'description': pattern.get('description', ''),
                'elements': pattern.get('elements', []),
                'confidence': pattern.get('confidence', 0.5),
                'perspectives': pattern.get('perspectives', {}),
                'quantum_state': pattern.get('quantum_state', {}),
                'inference_logic': pattern.get('inference_logic', {}),
                'cross_domain_connections': pattern.get('cross_domain_connections', {}),
                'first_principles': pattern.get('first_principles', []),
                'persona_insights': pattern.get('persona_insights', {}),
                'created_at': datetime.utcnow().isoformat()
            }).execute()
            
            if result.data:
                pattern_id = result.data[0]['id']
                logger.info(f"Tracked dark matter pattern: {pattern.get('pattern_name')}")
                return pattern_id
            
            return None
        except Exception as e:
            logger.error(f"Error tracking dark matter pattern: {e}")
            return None
    
    def detect_latent_connections(self, data: List[Dict]) -> List[Dict]:
        """
        Detect latent connections (dark matter) in data
        
        Args:
            data: List of data dictionaries
            
        Returns:
            List of latent connection patterns
        """
        latent_patterns = []
        
        # 1. Cross-domain implicit connections
        implicit_cross_domain = self._detect_implicit_cross_domain(data)
        latent_patterns.extend(implicit_cross_domain)
        
        # 2. Hidden gematria connections
        hidden_gematria = self._detect_hidden_gematria(data)
        latent_patterns.extend(hidden_gematria)
        
        # 3. Temporal dark matter (patterns that occur together but aren't obvious)
        temporal_dark_matter = self._detect_temporal_dark_matter(data)
        latent_patterns.extend(temporal_dark_matter)
        
        # 4. Semantic shadows (semantically related but not obviously)
        semantic_shadows = self._detect_semantic_shadows(data)
        latent_patterns.extend(semantic_shadows)
        
        # 5. Quantum superposition patterns
        quantum_patterns = self._detect_quantum_superposition(data)
        latent_patterns.extend(quantum_patterns)
        
        return latent_patterns
    
    def _detect_implicit_cross_domain(self, data: List[Dict]) -> List[Dict]:
        """Detect implicit cross-domain connections"""
        patterns = []
        
        # Group by domain
        domain_groups = defaultdict(list)
        for item in data:
            domain = item.get('domain', item.get('source_type', 'unknown'))
            domain_groups[domain].append(item)
        
        # Find implicit connections between domains
        domains = list(domain_groups.keys())
        for i, domain1 in enumerate(domains):
            for domain2 in domains[i+1:]:
                # Find implicit connections (not explicit in data)
                implicit_terms = self._find_implicit_connections(
                    domain_groups[domain1],
                    domain_groups[domain2]
                )
                
                if implicit_terms:
                    pattern = {
                        'pattern_name': f"Implicit cross-domain: {domain1} <-> {domain2}",
                        'pattern_type': 'implicit_cross_domain',
                        'description': f"Hidden connections between {domain1} and {domain2}",
                        'elements': implicit_terms,
                        'confidence': 0.6,  # Lower confidence for implicit patterns
                        'cross_domain_connections': {
                            'domains': [domain1, domain2],
                            'implicit_terms': implicit_terms
                        }
                    }
                    patterns.append(pattern)
        
        return patterns
    
    def _find_implicit_connections(self, group1: List[Dict], group2: List[Dict]) -> List[str]:
        """Find implicit connections between two groups"""
        # Extract terms from both groups
        terms1 = set()
        terms2 = set()
        
        for item in group1:
            # Extract terms from various fields
            if 'extracted_data' in item:
                extracted = item['extracted_data']
                if isinstance(extracted, dict):
                    # Symbols
                    for symbol in extracted.get('symbols', []):
                        if isinstance(symbol, dict):
                            terms1.add(symbol.get('symbol', ''))
                    # Esoteric terms
                    for term in extracted.get('esoteric_terms', []):
                        if isinstance(term, dict):
                            terms1.add(term.get('term', ''))
            
            # Tags
            for tag in item.get('tags', []):
                terms1.add(tag)
        
        for item in group2:
            if 'extracted_data' in item:
                extracted = item['extracted_data']
                if isinstance(extracted, dict):
                    for symbol in extracted.get('symbols', []):
                        if isinstance(symbol, dict):
                            terms2.add(symbol.get('symbol', ''))
                    for term in extracted.get('esoteric_terms', []):
                        if isinstance(term, dict):
                            terms2.add(term.get('term', ''))
            
            for tag in item.get('tags', []):
                terms2.add(tag)
        
        # Find implicit connections (phonetic, gematria, semantic)
        implicit = []
        for term1 in terms1:
            for term2 in terms2:
                # Check for implicit connections
                if self._is_implicitly_connected(term1, term2):
                    implicit.append(f"{term1} <-> {term2}")
        
        return implicit
    
    def _is_implicitly_connected(self, term1: str, term2: str) -> bool:
        """Check if two terms are implicitly connected"""
        # Phonetic similarity
        if self._phonetic_similarity(term1, term2) > 0.7:
            return True
        
        # Gematria similarity (if both have gematria values)
        # This would require gematria calculation
        
        # Semantic similarity (would require embeddings)
        
        return False
    
    def _phonetic_similarity(self, term1: str, term2: str) -> float:
        """Calculate phonetic similarity between two terms"""
        # Simple phonetic similarity check
        # In production, use phonetic algorithms like Soundex, Metaphone, etc.
        term1_lower = term1.lower()
        term2_lower = term2.lower()
        
        if term1_lower == term2_lower:
            return 1.0
        
        # Check for common substrings
        common_chars = set(term1_lower) & set(term2_lower)
        if not common_chars:
            return 0.0
        
        similarity = len(common_chars) / max(len(set(term1_lower)), len(set(term2_lower)), 1)
        return similarity
    
    def _detect_hidden_gematria(self, data: List[Dict]) -> List[Dict]:
        """Detect hidden gematria connections"""
        patterns = []
        
        # Collect gematria values
        gematria_map = defaultdict(list)
        for item in data:
            if 'extracted_data' in item:
                extracted = item['extracted_data']
                if isinstance(extracted, dict):
                    gematria_data = extracted.get('gematria_values', {})
                    if isinstance(gematria_data, dict):
                        for method, value in gematria_data.items():
                            if value:
                                gematria_map[method].append({
                                    'value': value,
                                    'source': item.get('id', 'unknown'),
                                    'term': item.get('title', item.get('url', ''))
                                })
        
        # Find hidden connections (same gematria values across different contexts)
        for method, values in gematria_map.items():
            value_groups = defaultdict(list)
            for val_data in values:
                value_groups[val_data['value']].append(val_data)
            
            # Find values that appear in multiple contexts (hidden connection)
            for value, contexts in value_groups.items():
                if len(contexts) > 1:
                    pattern = {
                        'pattern_name': f"Hidden gematria connection: {method} = {value}",
                        'pattern_type': 'hidden_gematria',
                        'description': f"Same gematria value ({value}) in {len(contexts)} different contexts",
                        'elements': [c['term'] for c in contexts],
                        'confidence': 0.7,
                        'inference_logic': {
                            'method': method,
                            'value': value,
                            'context_count': len(contexts)
                        }
                    }
                    patterns.append(pattern)
        
        return patterns
    
    def _detect_temporal_dark_matter(self, data: List[Dict]) -> List[Dict]:
        """Detect temporal dark matter (patterns that occur together but aren't obvious)"""
        patterns = []
        
        # Group by time
        time_groups = defaultdict(list)
        for item in data:
            timestamp = item.get('ingested_at') or item.get('created_at')
            if timestamp:
                try:
                    # Group by day
                    date_str = timestamp.split('T')[0]
                    time_groups[date_str].append(item)
                except:
                    pass
        
        # Find patterns in time groups
        for date_str, items in time_groups.items():
            if len(items) > 2:  # Multiple items on same day
                # Find common themes (not explicit in data)
                common_themes = self._find_common_themes(items)
                
                if common_themes:
                    pattern = {
                        'pattern_name': f"Temporal dark matter: {date_str}",
                        'pattern_type': 'temporal_dark_matter',
                        'description': f"Hidden patterns on {date_str}",
                        'elements': common_themes,
                        'confidence': 0.6,
                        'inference_logic': {
                            'date': date_str,
                            'item_count': len(items),
                            'themes': common_themes
                        }
                    }
                    patterns.append(pattern)
        
        return patterns
    
    def _find_common_themes(self, items: List[Dict]) -> List[str]:
        """Find common themes across items"""
        themes = []
        
        # Extract themes from various fields
        all_themes = []
        for item in items:
            # Tags
            all_themes.extend(item.get('tags', []))
            
            # Categories
            if 'category' in item:
                all_themes.append(item['category'])
        
        # Find frequently occurring themes
        theme_counts = defaultdict(int)
        for theme in all_themes:
            theme_counts[theme] += 1
        
        # Themes that appear in multiple items
        for theme, count in theme_counts.items():
            if count > 1:
                themes.append(theme)
        
        return themes
    
    def _detect_semantic_shadows(self, data: List[Dict]) -> List[Dict]:
        """Detect semantic shadows (semantically related but not obviously)"""
        patterns = []
        
        # This would use embeddings to find semantic similarity
        # For now, placeholder implementation
        
        return patterns
    
    def _detect_quantum_superposition(self, data: List[Dict]) -> List[Dict]:
        """Detect quantum superposition patterns (multiple meanings simultaneously)"""
        patterns = []
        
        # Find items with multiple interpretations
        for item in data:
            interpretations = []
            
            # Check for multiple gematria values
            if 'extracted_data' in item:
                extracted = item['extracted_data']
                if isinstance(extracted, dict):
                    gematria_data = extracted.get('gematria_values', {})
                    if isinstance(gematria_data, dict) and len(gematria_data) > 1:
                        interpretations.append('multiple_gematria_values')
            
            # Check for multiple symbols
            if 'extracted_data' in item:
                extracted = item['extracted_data']
                if isinstance(extracted, dict):
                    symbols = extracted.get('symbols', [])
                    if len(symbols) > 1:
                        interpretations.append('multiple_symbols')
            
            if interpretations:
                pattern = {
                    'pattern_name': f"Quantum superposition: {item.get('title', item.get('id', 'unknown'))}",
                    'pattern_type': 'quantum_superposition',
                    'description': f"Multiple simultaneous interpretations",
                    'elements': [item.get('id', 'unknown')],
                    'confidence': 0.7,
                    'quantum_state': {
                        'interpretations': interpretations,
                        'superposition': True
                    }
                }
                patterns.append(pattern)
        
        return patterns
    
    def analyze_with_personas(self, pattern: Dict, persona_manager) -> Dict:
        """
        Analyze dark matter pattern from multiple persona perspectives
        
        Args:
            pattern: Dark matter pattern
            persona_manager: PersonaManagerAgent instance
            
        Returns:
            Pattern with persona insights added
        """
        if not persona_manager:
            return pattern
        
        persona_insights = {}
        
        # Get relevant personas
        pattern_type = pattern.get('pattern_type', 'unknown')
        if 'gematria' in pattern_type:
            personas = persona_manager.get_personas_by_tag('gematria')
        elif 'quantum' in pattern_type:
            personas = persona_manager.get_personas_by_tag('physics')
        else:
            personas = persona_manager.get_personas_by_domain('physics')  # Default
        
        # Analyze from each persona perspective
        for persona in personas:
            persona_name = persona.get('name', 'unknown')
            # In production, use LLM to get persona insights
            # For now, placeholder
            persona_insights[persona_name] = {
                'perspective': f"{persona_name} perspective on {pattern.get('pattern_name')}",
                'insight': f"Analysis from {persona_name}'s framework"
            }
        
        pattern['persona_insights'] = persona_insights
        return pattern
    
    def apply_first_principles(self, pattern: Dict) -> Dict:
        """
        Apply first principles thinking to dark matter pattern
        
        Args:
            pattern: Dark matter pattern
            
        Returns:
            Pattern with first principles analysis added
        """
        first_principles = []
        
        # Break down pattern to fundamental components
        pattern_name = pattern.get('pattern_name', '')
        pattern_type = pattern.get('pattern_type', '')
        elements = pattern.get('elements', [])
        
        # First principles analysis
        first_principles.append(f"Fundamental observation: {pattern_type} pattern detected")
        first_principles.append(f"Core elements: {len(elements)} connected elements")
        first_principles.append(f"Pattern confidence: {pattern.get('confidence', 0.0)}")
        
        # Add to pattern
        pattern['first_principles'] = first_principles
        return pattern
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute dark matter tracking task
        
        Args:
            state: Agent state with source data
            
        Returns:
            Updated state with dark matter patterns
        """
        data = state.get("data", [])
        
        if not data:
            logger.warning("No data provided for dark matter tracking")
            return state
        
        logger.info(f"Dark matter tracker: Processing {len(data)} sources")
        
        try:
            # Detect latent connections (dark matter)
            dark_matter_patterns = self.detect_latent_connections(data)
            
            # Get persona manager for multi-perspective analysis
            persona_manager = None
            if 'persona_manager' in state.get('context', {}):
                persona_manager = state['context']['persona_manager']
            else:
                # Try to get from orchestrator
                try:
                    from .persona_manager import PersonaManagerAgent
                    persona_manager = PersonaManagerAgent()
                except:
                    pass
            
            # Process each pattern
            processed_patterns = []
            for pattern in dark_matter_patterns:
                # Apply first principles
                pattern = self.apply_first_principles(pattern)
                
                # Analyze with personas
                if persona_manager:
                    pattern = self.analyze_with_personas(pattern, persona_manager)
                
                # Track pattern
                pattern_id = self.track_dark_matter_pattern(pattern)
                if pattern_id:
                    pattern['id'] = pattern_id
                    processed_patterns.append(pattern)
            
            # Update state
            state["context"]["dark_matter_patterns"] = processed_patterns
            state["context"]["dark_matter_count"] = len(processed_patterns)
            state["results"].append({
                "agent": self.name,
                "action": "track_dark_matter",
                "patterns_tracked": len(processed_patterns),
                "pattern_types": list(set(p.get('pattern_type', 'unknown') for p in processed_patterns))
            })
            
            logger.info(f"Dark matter tracking complete: {len(processed_patterns)} patterns tracked")
            
        except Exception as e:
            logger.error(f"Dark matter tracking error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

