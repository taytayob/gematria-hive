"""
Phonetic Analyzer Agent
Purpose: Explore phonetic connections (I, eyes, ice, numerology, geometry, sacred)
- Phonetic similarity detection
- Sound-based pattern matching
- Homophone identification
- Phonetic variant tracking
- Cross-domain phonetic connections

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
import re
from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime
from difflib import SequenceMatcher

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


class PhoneticAnalyzerAgent:
    """
    Phonetic Analyzer Agent - Analyzes phonetic connections and patterns
    """
    
    def __init__(self):
        """Initialize phonetic analyzer agent"""
        self.name = "phonetic_analyzer_agent"
        self.supabase = supabase if HAS_SUPABASE else None
        
        # Phonetic patterns (I, eyes, ice, etc.)
        self.phonetic_patterns = {
            'i_eyes_ice': [
                'i', 'eye', 'eyes', 'ice', 'icy', 'aisle', 'isle', 'aisles', 'isles',
                'aye', 'ayes', 'ai', 'ay', 'ei', 'ey', 'ie', 'ye'
            ],
            'numerology': [
                'numerology', 'numerical', 'number', 'numbers', 'numeral', 'numerals',
                'numeric', 'num', 'nums', 'numeralogy', 'numerical'
            ],
            'geometry': [
                'geometry', 'geometric', 'geometrical', 'geometries', 'geometer',
                'geometrician', 'geometrical', 'geometrically'
            ],
            'sacred': [
                'sacred', 'sacredness', 'sacredly', 'sacred', 'sacral', 'sacrality',
                'sacred', 'sacred', 'sacred', 'sacred'
            ],
            'light': [
                'light', 'lights', 'lighting', 'lighted', 'lit', 'lighter', 'lightest',
                'lightness', 'lightly', 'lighten', 'lightening', 'enlighten', 'enlightened',
                'enlightenment', 'enlightening'
            ],
            'love': [
                'love', 'loves', 'loved', 'loving', 'lovely', 'lover', 'lovers',
                'lovable', 'loveable', 'beloved', 'unloved', 'loveless'
            ],
            'truth': [
                'truth', 'truths', 'truthful', 'truthfully', 'truthfulness', 'untruth',
                'untruthful', 'truthiness', 'truthy', 'truthier', 'truthiest'
            ],
            'eternal': [
                'eternal', 'eternally', 'eternity', 'eternities', 'eternalize', 'eternalized',
                'eternalizing', 'eternalization', 'eternalness'
            ]
        }
        
        # Phonetic similarity groups
        self.phonetic_groups = {
            'i_sound': ['i', 'eye', 'eyes', 'ice', 'icy', 'aisle', 'isle', 'aye', 'ai', 'ay', 'ei', 'ey', 'ie', 'ye'],
            'light_sound': ['light', 'lite', 'lyte', 'lyte', 'light', 'lite'],
            'love_sound': ['love', 'luv', 'luv', 'love'],
            'truth_sound': ['truth', 'trueth', 'trueth', 'truth'],
            'sacred_sound': ['sacred', 'sakred', 'sakred', 'sacred'],
            'number_sound': ['number', 'numbah', 'numbah', 'number'],
            'geometry_sound': ['geometry', 'geometree', 'geometree', 'geometry']
        }
        
        logger.info(f"Initialized {self.name}")
    
    def phonetic_similarity(self, word1: str, word2: str) -> float:
        """
        Calculate phonetic similarity between two words.
        
        Args:
            word1: First word
            word2: Second word
            
        Returns:
            Similarity score (0.0 to 1.0)
        """
        # Simple string similarity (can be enhanced with phonetic algorithms)
        return SequenceMatcher(None, word1.lower(), word2.lower()).ratio()
    
    def find_homophones(self, word: str, word_list: List[str], threshold: float = 0.8) -> List[str]:
        """
        Find homophones (words that sound similar) in a word list.
        
        Args:
            word: Word to find homophones for
            word_list: List of words to search
            threshold: Similarity threshold
            
        Returns:
            List of homophones
        """
        homophones = []
        word_lower = word.lower()
        
        for candidate in word_list:
            candidate_lower = candidate.lower()
            similarity = self.phonetic_similarity(word_lower, candidate_lower)
            if similarity >= threshold and word_lower != candidate_lower:
                homophones.append(candidate)
        
        return homophones
    
    def extract_phonetic_variants(self, text: str) -> List[Dict]:
        """
        Extract phonetic variants from text.
        
        Args:
            text: Text to extract variants from
            
        Returns:
            List of phonetic variant dictionaries
        """
        variants = []
        text_lower = text.lower()
        
        # Find all words matching phonetic patterns
        for pattern_group, words in self.phonetic_patterns.items():
            for word in words:
                pattern = r'\b' + re.escape(word) + r'\b'
                matches = re.finditer(pattern, text_lower, re.IGNORECASE)
                for match in matches:
                    variant = {
                        'word': match.group(0),
                        'pattern_group': pattern_group,
                        'start_pos': match.start(),
                        'end_pos': match.end(),
                        'context': text[max(0, match.start()-50):min(len(text), match.end()+50)]
                    }
                    variants.append(variant)
        
        # Find homophones within the text
        words_in_text = re.findall(r'\b\w+\b', text_lower)
        unique_words = list(set(words_in_text))
        
        for word in unique_words:
            # Check if word is in any phonetic group
            for group_name, group_words in self.phonetic_groups.items():
                if word in group_words:
                    # Find other words in the same group
                    homophones = [w for w in unique_words if w in group_words and w != word]
                    if homophones:
                        variant = {
                            'word': word,
                            'pattern_group': group_name,
                            'homophones': homophones,
                            'type': 'phonetic_group'
                        }
                        variants.append(variant)
        
        return variants
    
    def find_cross_domain_connections(self, text: str) -> List[Dict]:
        """
        Find cross-domain phonetic connections.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of cross-domain connection dictionaries
        """
        connections = []
        text_lower = text.lower()
        
        # Find connections between different phonetic groups
        found_groups = set()
        for group_name, group_words in self.phonetic_groups.items():
            for word in group_words:
                if word in text_lower:
                    found_groups.add(group_name)
                    break
        
        # Find connections between groups
        if len(found_groups) > 1:
            groups_list = list(found_groups)
            for i, group1 in enumerate(groups_list):
                for group2 in groups_list[i+1:]:
                    connection = {
                        'group1': group1,
                        'group2': group2,
                        'type': 'cross_domain_phonetic',
                        'strength': 1.0,
                        'context': text
                    }
                    connections.append(connection)
        
        # Find connections between phonetic patterns and other concepts
        # (e.g., I/eyes/ice with numerology, geometry, sacred)
        i_words = ['i', 'eye', 'eyes', 'ice', 'icy']
        concept_words = {
            'numerology': ['number', 'numerical', 'numerology'],
            'geometry': ['geometry', 'geometric', 'geometrical'],
            'sacred': ['sacred', 'sacredness', 'sacral']
        }
        
        has_i = any(word in text_lower for word in i_words)
        
        for concept, concept_word_list in concept_words.items():
            has_concept = any(word in text_lower for word in concept_word_list)
            if has_i and has_concept:
                connection = {
                    'group1': 'i_eyes_ice',
                    'group2': concept,
                    'type': 'phonetic_concept_connection',
                    'strength': 1.0,
                    'context': text
                }
                connections.append(connection)
        
        return connections
    
    def analyze_phonetic_patterns(self, text: str) -> Dict:
        """
        Analyze phonetic patterns in text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with phonetic pattern analysis
        """
        analysis = {
            'phonetic_variants': self.extract_phonetic_variants(text),
            'cross_domain_connections': self.find_cross_domain_connections(text),
            'pattern_groups_found': [],
            'homophone_groups': [],
            'phonetic_density': 0.0
        }
        
        # Count pattern groups found
        found_groups = set()
        for variant in analysis['phonetic_variants']:
            if 'pattern_group' in variant:
                found_groups.add(variant['pattern_group'])
        analysis['pattern_groups_found'] = list(found_groups)
        
        # Find homophone groups
        words_in_text = re.findall(r'\b\w+\b', text.lower())
        unique_words = list(set(words_in_text))
        
        homophone_groups = []
        processed_words = set()
        
        for word in unique_words:
            if word in processed_words:
                continue
            
            # Find homophones for this word
            homophones = self.find_homophones(word, unique_words, threshold=0.7)
            if homophones:
                group = {
                    'primary_word': word,
                    'homophones': homophones,
                    'group_size': len(homophones) + 1
                }
                homophone_groups.append(group)
                processed_words.add(word)
                processed_words.update(homophones)
        
        analysis['homophone_groups'] = homophone_groups
        
        # Calculate phonetic density (ratio of phonetic words to total words)
        total_words = len(words_in_text)
        phonetic_words = len(analysis['phonetic_variants'])
        if total_words > 0:
            analysis['phonetic_density'] = phonetic_words / total_words
        
        return analysis
    
    def store_phonetic_data(self, source_id: str, phonetic_data: Dict) -> bool:
        """
        Store phonetic analysis data in database.
        
        Args:
            source_id: Source ID
            phonetic_data: Phonetic analysis data
            
        Returns:
            True if stored successfully, False otherwise
        """
        if not self.supabase:
            return False
        
        try:
            # Store phonetic variants as key terms
            for variant in phonetic_data.get('phonetic_variants', []):
                if 'word' in variant:
                    term_data = {
                        'term': variant['word'],
                        'term_type': 'phonetic',
                        'phonetic_variants': variant.get('homophones', []),
                        'source_ids': [source_id] if source_id else [],
                        'context': variant.get('context', ''),
                        'first_seen_at': datetime.utcnow().isoformat(),
                        'last_seen_at': datetime.utcnow().isoformat()
                    }
                    
                    # Check if term already exists
                    existing = self.supabase.table('key_terms')\
                        .select('id')\
                        .eq('term', variant['word'])\
                        .eq('term_type', 'phonetic')\
                        .limit(1)\
                        .execute()
                    
                    if existing.data:
                        # Update existing term
                        term_id = existing.data[0]['id']
                        self.supabase.table('key_terms')\
                            .update({
                                'phonetic_variants': term_data['phonetic_variants'],
                                'last_seen_at': datetime.utcnow().isoformat(),
                                'frequency': existing.data[0].get('frequency', 0) + 1
                            })\
                            .eq('id', term_id)\
                            .execute()
                    else:
                        # Create new term
                        self.supabase.table('key_terms').insert(term_data).execute()
            
            logger.info(f"Stored phonetic data for source {source_id}")
            return True
        except Exception as e:
            logger.error(f"Error storing phonetic data: {e}")
            return False
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute phonetic analysis task.
        
        Args:
            state: Agent state with source data
            
        Returns:
            Updated state with phonetic analysis
        """
        data = state.get("data", [])
        
        if not data:
            logger.warning("No data provided for phonetic analysis")
            return state
        
        logger.info(f"Phonetic analyzer agent: Processing {len(data)} sources")
        
        try:
            all_phonetic_data = []
            
            for source in data:
                if not isinstance(source, dict):
                    continue
                
                source_id = source.get('id')
                content = source.get('content', '') or source.get('title', '') or source.get('description', '')
                
                if not content:
                    continue
                
                # Analyze phonetic patterns
                phonetic_analysis = self.analyze_phonetic_patterns(content)
                
                all_phonetic_data.append({
                    'source_id': source_id,
                    'phonetic_analysis': phonetic_analysis
                })
                
                # Store phonetic data
                if source_id:
                    self.store_phonetic_data(source_id, phonetic_analysis)
            
            # Update state
            state["context"]["phonetic_analysis"] = all_phonetic_data
            state["context"]["phonetic_variant_count"] = sum(
                len(p['phonetic_analysis']['phonetic_variants']) for p in all_phonetic_data
            )
            state["context"]["cross_domain_connections"] = sum(
                len(p['phonetic_analysis']['cross_domain_connections']) for p in all_phonetic_data
            )
            state["results"].append({
                "agent": self.name,
                "action": "analyze_phonetics",
                "sources_processed": len(all_phonetic_data),
                "total_variants": sum(len(p['phonetic_analysis']['phonetic_variants']) for p in all_phonetic_data),
                "total_connections": sum(len(p['phonetic_analysis']['cross_domain_connections']) for p in all_phonetic_data)
            })
            
            logger.info(f"Phonetic analysis complete: {len(all_phonetic_data)} sources processed")
            
        except Exception as e:
            logger.error(f"Phonetic analysis error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

