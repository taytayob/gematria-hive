"""
Pattern Detector Agent
Purpose: Detect patterns and cross-domain inferences
- Key term frequency analysis
- Cross-domain pattern detection
- Temporal pattern analysis
- Symbolic pattern recognition
- Inference logic generation
- Pattern confidence scoring

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime
from collections import Counter, defaultdict

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


class PatternDetectorAgent:
    """
    Pattern Detector Agent - Detects patterns and cross-domain inferences
    """
    
    def __init__(self):
        """Initialize pattern detector agent"""
        self.name = "pattern_detector_agent"
        self.supabase = supabase if HAS_SUPABASE else None
        logger.info(f"Initialized {self.name}")
    
    def analyze_key_term_frequency(self, sources: List[Dict]) -> Dict[str, int]:
        """
        Analyze key term frequency across sources.
        
        Args:
            sources: List of source dictionaries
            
        Returns:
            Dictionary with term frequencies
        """
        term_frequencies = Counter()
        
        for source in sources:
            # Get key terms from source
            extracted_data = source.get('extracted_data', {})
            if isinstance(extracted_data, dict):
                # Symbols
                symbols = extracted_data.get('symbols', [])
                for symbol in symbols:
                    if isinstance(symbol, dict):
                        term_frequencies[symbol.get('symbol', '')] += 1
                
                # Esoteric terms
                esoteric_terms = extracted_data.get('esoteric_terms', [])
                for term in esoteric_terms:
                    if isinstance(term, dict):
                        term_frequencies[term.get('term', '')] += 1
            
            # Get tags
            tags = source.get('tags', [])
            if isinstance(tags, list):
                for tag in tags:
                    term_frequencies[tag] += 1
        
        return dict(term_frequencies)
    
    def detect_cross_domain_patterns(self, sources: List[Dict]) -> List[Dict]:
        """
        Detect cross-domain patterns across sources.
        
        Args:
            sources: List of source dictionaries
            
        Returns:
            List of pattern dictionaries
        """
        patterns = []
        
        # Group sources by domain/type
        domain_groups = defaultdict(list)
        for source in sources:
            source_type = source.get('source_type', 'unknown')
            domain_groups[source_type].append(source)
        
        # Find patterns across domains
        domain_list = list(domain_groups.keys())
        for i, domain1 in enumerate(domain_list):
            for domain2 in domain_list[i+1:]:
                # Find common terms between domains
                terms1 = set()
                terms2 = set()
                
                for source in domain_groups[domain1]:
                    extracted_data = source.get('extracted_data', {})
                    if isinstance(extracted_data, dict):
                        symbols = extracted_data.get('symbols', [])
                        for symbol in symbols:
                            if isinstance(symbol, dict):
                                terms1.add(symbol.get('symbol', ''))
                
                for source in domain_groups[domain2]:
                    extracted_data = source.get('extracted_data', {})
                    if isinstance(extracted_data, dict):
                        symbols = extracted_data.get('symbols', [])
                        for symbol in symbols:
                            if isinstance(symbol, dict):
                                terms2.add(symbol.get('symbol', ''))
                
                # Find common terms
                common_terms = terms1.intersection(terms2)
                
                if common_terms:
                    pattern = {
                        'pattern_name': f"Cross-domain pattern: {domain1} <-> {domain2}",
                        'pattern_type': 'cross_domain',
                        'description': f"Common terms between {domain1} and {domain2}",
                        'key_terms': list(common_terms),
                        'sources': [s.get('id') for s in domain_groups[domain1] + domain_groups[domain2] if s.get('id')],
                        'confidence_score': min(len(common_terms) / max(len(terms1), len(terms2), 1), 1.0),
                        'inference_logic': {
                            'domain1': domain1,
                            'domain2': domain2,
                            'common_terms_count': len(common_terms),
                            'terms1_count': len(terms1),
                            'terms2_count': len(terms2)
                        },
                        'cross_domain_connections': {
                            'domains': [domain1, domain2],
                            'common_terms': list(common_terms)
                        }
                    }
                    patterns.append(pattern)
        
        return patterns
    
    def detect_temporal_patterns(self, sources: List[Dict]) -> List[Dict]:
        """
        Detect temporal patterns in sources.
        
        Args:
            sources: List of source dictionaries
            
        Returns:
            List of temporal pattern dictionaries
        """
        patterns = []
        
        # Group sources by time
        time_groups = defaultdict(list)
        for source in sources:
            ingested_at = source.get('ingested_at') or source.get('created_at')
            if ingested_at:
                try:
                    # Group by date (day)
                    date_str = ingested_at.split('T')[0]
                    time_groups[date_str].append(source)
                except:
                    pass
        
        # Find patterns in time groups
        for date_str, date_sources in time_groups.items():
            if len(date_sources) > 1:
                # Find common terms in time group
                common_terms = set()
                all_terms = []
                
                for source in date_sources:
                    extracted_data = source.get('extracted_data', {})
                    if isinstance(extracted_data, dict):
                        symbols = extracted_data.get('symbols', [])
                        for symbol in symbols:
                            if isinstance(symbol, dict):
                                term = symbol.get('symbol', '')
                                if term:
                                    all_terms.append(term)
                
                # Find terms that appear in multiple sources
                term_counts = Counter(all_terms)
                common_terms = {term for term, count in term_counts.items() if count > 1}
                
                if common_terms:
                    pattern = {
                        'pattern_name': f"Temporal pattern: {date_str}",
                        'pattern_type': 'temporal',
                        'description': f"Common terms on {date_str}",
                        'key_terms': list(common_terms),
                        'sources': [s.get('id') for s in date_sources if s.get('id')],
                        'confidence_score': min(len(common_terms) / max(len(all_terms), 1), 1.0),
                        'inference_logic': {
                            'date': date_str,
                            'source_count': len(date_sources),
                            'common_terms_count': len(common_terms),
                            'total_terms': len(all_terms)
                        }
                    }
                    patterns.append(pattern)
        
        return patterns
    
    def detect_symbolic_patterns(self, sources: List[Dict]) -> List[Dict]:
        """
        Detect symbolic patterns in sources.
        
        Args:
            sources: List of source dictionaries
            
        Returns:
            List of symbolic pattern dictionaries
        """
        patterns = []
        
        # Group symbols by category
        category_groups = defaultdict(list)
        for source in sources:
            extracted_data = source.get('extracted_data', {})
            if isinstance(extracted_data, dict):
                symbols = extracted_data.get('symbols', [])
                for symbol in symbols:
                    if isinstance(symbol, dict):
                        category = symbol.get('category', 'unknown')
                        category_groups[category].append(symbol)
        
        # Find patterns within categories
        for category, symbols in category_groups.items():
            if len(symbols) > 1:
                # Find frequently co-occurring symbols
                symbol_pairs = defaultdict(int)
                for source in sources:
                    extracted_data = source.get('extracted_data', {})
                    if isinstance(extracted_data, dict):
                        source_symbols = extracted_data.get('symbols', [])
                        category_symbols = [s.get('symbol', '') for s in source_symbols 
                                          if isinstance(s, dict) and s.get('category') == category]
                        
                        # Count pairs
                        for i, symbol1 in enumerate(category_symbols):
                            for symbol2 in category_symbols[i+1:]:
                                pair = tuple(sorted([symbol1, symbol2]))
                                symbol_pairs[pair] += 1
                
                # Find strong pairs (appear together multiple times)
                strong_pairs = {pair: count for pair, count in symbol_pairs.items() if count > 1}
                
                if strong_pairs:
                    pattern = {
                        'pattern_name': f"Symbolic pattern: {category}",
                        'pattern_type': 'symbolic',
                        'description': f"Co-occurring symbols in {category}",
                        'key_terms': list(set([s for pair in strong_pairs.keys() for s in pair])),
                        'sources': [s.get('id') for s in sources if s.get('id')],
                        'confidence_score': min(max(strong_pairs.values()) / len(sources), 1.0),
                        'inference_logic': {
                            'category': category,
                            'strong_pairs_count': len(strong_pairs),
                            'total_symbols': len(symbols)
                        },
                        'cross_domain_connections': {
                            'category': category,
                            'strong_pairs': {f"{pair[0]}-{pair[1]}": count for pair, count in strong_pairs.items()}
                        }
                    }
                    patterns.append(pattern)
        
        return patterns
    
    def detect_phonetic_patterns(self, sources: List[Dict]) -> List[Dict]:
        """
        Detect phonetic patterns in sources.
        
        Args:
            sources: List of source dictionaries
            
        Returns:
            List of phonetic pattern dictionaries
        """
        patterns = []
        
        # Collect phonetic variants from all sources
        all_variants = defaultdict(list)
        for source in sources:
            extracted_data = source.get('extracted_data', {})
            if isinstance(extracted_data, dict):
                phonetic_analysis = extracted_data.get('phonetic_analysis', {})
                if isinstance(phonetic_analysis, dict):
                    variants = phonetic_analysis.get('phonetic_variants', [])
                    for variant in variants:
                        if isinstance(variant, dict):
                            pattern_group = variant.get('pattern_group', 'unknown')
                            word = variant.get('word', '')
                            if word:
                                all_variants[pattern_group].append(word)
        
        # Find patterns in phonetic groups
        for pattern_group, words in all_variants.items():
            if len(words) > 1:
                # Find frequently co-occurring words
                word_pairs = defaultdict(int)
                for source in sources:
                    extracted_data = source.get('extracted_data', {})
                    if isinstance(extracted_data, dict):
                        phonetic_analysis = extracted_data.get('phonetic_analysis', {})
                        if isinstance(phonetic_analysis, dict):
                            variants = phonetic_analysis.get('phonetic_variants', [])
                            group_words = [v.get('word', '') for v in variants 
                                         if isinstance(v, dict) and v.get('pattern_group') == pattern_group]
                            
                            # Count pairs
                            for i, word1 in enumerate(group_words):
                                for word2 in group_words[i+1:]:
                                    pair = tuple(sorted([word1, word2]))
                                    word_pairs[pair] += 1
                
                # Find strong pairs
                strong_pairs = {pair: count for pair, count in word_pairs.items() if count > 1}
                
                if strong_pairs:
                    pattern = {
                        'pattern_name': f"Phonetic pattern: {pattern_group}",
                        'pattern_type': 'phonetic',
                        'description': f"Co-occurring phonetic variants in {pattern_group}",
                        'key_terms': list(set([w for pair in strong_pairs.keys() for w in pair])),
                        'sources': [s.get('id') for s in sources if s.get('id')],
                        'confidence_score': min(max(strong_pairs.values()) / len(sources), 1.0),
                        'inference_logic': {
                            'pattern_group': pattern_group,
                            'strong_pairs_count': len(strong_pairs),
                            'total_words': len(words)
                        }
                    }
                    patterns.append(pattern)
        
        return patterns
    
    def detect_gematria_patterns(self, sources: List[Dict]) -> List[Dict]:
        """
        Detect gematria patterns in sources.
        
        Args:
            sources: List of source dictionaries
            
        Returns:
            List of gematria pattern dictionaries
        """
        patterns = []
        
        # Collect gematria values from all sources
        gematria_values = defaultdict(list)
        for source in sources:
            extracted_data = source.get('extracted_data', {})
            if isinstance(extracted_data, dict):
                gematria_data = extracted_data.get('gematria_values', {})
                if isinstance(gematria_data, dict):
                    for method, value in gematria_data.items():
                        if value:
                            gematria_values[method].append(value)
        
        # Find patterns in gematria values
        for method, values in gematria_values.items():
            if len(values) > 1:
                # Find frequently occurring values
                value_counts = Counter(values)
                frequent_values = {value: count for value, count in value_counts.items() if count > 1}
                
                if frequent_values:
                    pattern = {
                        'pattern_name': f"Gematria pattern: {method}",
                        'pattern_type': 'gematria',
                        'description': f"Frequently occurring gematria values in {method}",
                        'key_terms': list(frequent_values.keys()),
                        'sources': [s.get('id') for s in sources if s.get('id')],
                        'confidence_score': min(max(frequent_values.values()) / len(sources), 1.0),
                        'inference_logic': {
                            'method': method,
                            'frequent_values_count': len(frequent_values),
                            'total_values': len(values)
                        }
                    }
                    patterns.append(pattern)
        
        return patterns
    
    def calculate_confidence_score(self, pattern: Dict) -> float:
        """
        Calculate confidence score for a pattern.
        
        Args:
            pattern: Pattern dictionary
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        # Base confidence from pattern data
        base_confidence = pattern.get('confidence_score', 0.5)
        
        # Adjust based on number of sources
        source_count = len(pattern.get('sources', []))
        source_factor = min(source_count / 10.0, 1.0)  # Normalize to 10 sources
        
        # Adjust based on number of key terms
        term_count = len(pattern.get('key_terms', []))
        term_factor = min(term_count / 5.0, 1.0)  # Normalize to 5 terms
        
        # Combine factors
        confidence = (base_confidence * 0.5) + (source_factor * 0.25) + (term_factor * 0.25)
        
        return min(confidence, 1.0)
    
    def store_pattern(self, pattern: Dict) -> Optional[str]:
        """
        Store pattern in database.
        
        Args:
            pattern: Pattern dictionary
            
        Returns:
            Pattern ID or None
        """
        if not self.supabase:
            return None
        
        try:
            # Calculate confidence score
            pattern['confidence_score'] = self.calculate_confidence_score(pattern)
            
            # Store pattern
            result = self.supabase.table('patterns').insert(pattern).execute()
            
            if result.data:
                pattern_id = result.data[0]['id']
                logger.info(f"Stored pattern: {pattern.get('pattern_name')}")
                return pattern_id
            
            return None
        except Exception as e:
            logger.error(f"Error storing pattern: {e}")
            return None
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute pattern detection task.
        
        Args:
            state: Agent state with source data
            
        Returns:
            Updated state with detected patterns
        """
        data = state.get("data", [])
        
        if not data:
            logger.warning("No data provided for pattern detection")
            return state
        
        logger.info(f"Pattern detector agent: Processing {len(data)} sources")
        
        try:
            # Analyze key term frequency
            term_frequencies = self.analyze_key_term_frequency(data)
            
            # Detect patterns
            all_patterns = []
            
            # Cross-domain patterns
            cross_domain_patterns = self.detect_cross_domain_patterns(data)
            all_patterns.extend(cross_domain_patterns)
            
            # Temporal patterns
            temporal_patterns = self.detect_temporal_patterns(data)
            all_patterns.extend(temporal_patterns)
            
            # Symbolic patterns
            symbolic_patterns = self.detect_symbolic_patterns(data)
            all_patterns.extend(symbolic_patterns)
            
            # Phonetic patterns
            phonetic_patterns = self.detect_phonetic_patterns(data)
            all_patterns.extend(phonetic_patterns)
            
            # Gematria patterns
            gematria_patterns = self.detect_gematria_patterns(data)
            all_patterns.extend(gematria_patterns)
            
            # Store patterns
            stored_patterns = []
            for pattern in all_patterns:
                pattern_id = self.store_pattern(pattern)
                if pattern_id:
                    pattern['id'] = pattern_id
                    stored_patterns.append(pattern)
            
            # Update state
            state["context"]["detected_patterns"] = stored_patterns
            state["context"]["pattern_count"] = len(stored_patterns)
            state["context"]["term_frequencies"] = term_frequencies
            state["results"].append({
                "agent": self.name,
                "action": "detect_patterns",
                "patterns_detected": len(stored_patterns),
                "cross_domain": len(cross_domain_patterns),
                "temporal": len(temporal_patterns),
                "symbolic": len(symbolic_patterns),
                "phonetic": len(phonetic_patterns),
                "gematria": len(gematria_patterns)
            })
            
            logger.info(f"Pattern detection complete: {len(stored_patterns)} patterns detected")
            
        except Exception as e:
            logger.error(f"Pattern detection error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

