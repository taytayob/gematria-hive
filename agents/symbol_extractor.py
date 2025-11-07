"""
Symbol & Esoteric Extractor Agent
Purpose: Extract symbols, arcane/esoteric content, narratives, events
- Pattern matching for symbols (geometric, alchemical, astrological, etc.)
- Esoteric terminology detection
- Narrative structure analysis
- Event extraction (dates, locations, significance)
- Symbol relationships and connections

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime

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


class SymbolExtractorAgent:
    """
    Symbol & Esoteric Extractor Agent - Extracts symbols and esoteric content
    """
    
    def __init__(self):
        """Initialize symbol extractor agent"""
        self.name = "symbol_extractor_agent"
        self.supabase = supabase if HAS_SUPABASE else None
        
        # Symbol patterns
        self.symbol_patterns = {
            'geometric': [
                r'metatron\'?s?\s+cube',
                r'tree\s+of\s+life',
                r'flower\s+of\s+life',
                r'seed\s+of\s+life',
                r'vesica\s+piscis',
                r'sacred\s+geometry',
                r'platonic\s+solids?',
                r'torus',
                r'merkaba',
                r'star\s+of\s+david',
                r'pentagram',
                r'hexagram',
                r'octagram',
                r'enneagram',
                r'mandala',
                r'yantra'
            ],
            'alchemical': [
                r'alchemy',
                r'philosopher\'?s?\s+stone',
                r'elixir',
                r'transmutation',
                r'prima\s+materia',
                r'quintessence',
                r'four\s+elements',
                r'fire\s+water\s+earth\s+air',
                r'alchemical\s+symbols?',
                r'caduceus',
                r'ouroboros'
            ],
            'astrological': [
                r'zodiac',
                r'astrology',
                r'planets?',
                r'constellations?',
                r'horoscope',
                r'ascendant',
                r'descendant',
                r'houses?',
                r'aspects?',
                r'conjunction',
                r'opposition',
                r'trine',
                r'sextile'
            ],
            'numerological': [
                r'numerology',
                r'life\s+path',
                r'expression\s+number',
                r'soul\s+number',
                r'personality\s+number',
                r'birth\s+number',
                r'master\s+numbers?',
                r'angel\s+numbers?',
                r'369',
                r'111',
                r'222',
                r'333',
                r'444',
                r'555',
                r'666',
                r'777',
                r'888',
                r'999'
            ],
            'kabbalistic': [
                r'kabbalah',
                r'qabalah',
                r'cabala',
                r'sephiroth',
                r'sefirot',
                r'kabbalistic\s+tree',
                r'paths?',
                r'hebrew\s+letters?',
                r'gematria',
                r'notarikon',
                r'temurah',
                r'zohar',
                r'sefer\s+yetzirah'
            ],
            'hermetic': [
                r'hermetic',
                r'hermeticism',
                r'emerald\s+tablets?',
                r'thoth',
                r'hermes\s+trismegistus',
                r'as\s+above\s+so\s+below',
                r'seven\s+principles?',
                r'kybalion',
                r'corpus\s+hermeticum'
            ],
            'other_esoteric': [
                r'occult',
                r'esoteric',
                r'arcane',
                r'mysticism',
                r'gnostic',
                r'gnosticism',
                r'rosicrucian',
                r'freemasonry',
                r'illuminati',
                r'secret\s+societies?',
                r'initiation',
                r'adept',
                r'master',
                r'guru',
                r'sage'
            ]
        }
        
        # Esoteric terminology - literal terms
        self.esoteric_terms = [
            'vibration', 'frequency', 'resonance', 'harmonics', 'oscillation',
            'quantum', 'consciousness', 'awareness', 'enlightenment', 'awakening',
            'chakra', 'kundalini', 'prana', 'chi', 'qi', 'energy', 'aura',
            'meditation', 'contemplation', 'transcendence', 'unity', 'oneness',
            'duality', 'polarity', 'balance', 'harmony', 'equilibrium',
            'synchronicity', 'coincidence', 'meaning', 'purpose', 'destiny',
            'karma', 'dharma', 'samsara', 'nirvana', 'moksha',
            'reincarnation', 'rebirth', 'transmigration', 'soul', 'spirit',
            'divine', 'sacred', 'holy', 'blessed', 'anointed',
            'prophecy', 'revelation', 'apocalypse', 'eschatology',
            'messiah', 'savior', 'redeemer', 'christ'
        ]
        
        # Esoteric terminology - regex patterns (handled separately)
        self.esoteric_regex_patterns = [
            r'end\s+times',
            r'anointed\s+one'
        ]
        
        logger.info(f"Initialized {self.name}")
    
    def extract_symbols(self, text: str) -> List[Dict]:
        """
        Extract symbols from text using pattern matching.
        
        Args:
            text: Text to extract symbols from
            
        Returns:
            List of symbol dictionaries
        """
        symbols = []
        text_lower = text.lower()
        
        for category, patterns in self.symbol_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text_lower, re.IGNORECASE)
                for match in matches:
                    symbol = {
                        'symbol': match.group(0),
                        'category': category,
                        'start_pos': match.start(),
                        'end_pos': match.end(),
                        'context': text[max(0, match.start()-50):min(len(text), match.end()+50)]
                    }
                    symbols.append(symbol)
        
        # Remove duplicates
        seen = set()
        unique_symbols = []
        for symbol in symbols:
            key = (symbol['symbol'], symbol['category'])
            if key not in seen:
                seen.add(key)
                unique_symbols.append(symbol)
        
        return unique_symbols
    
    def extract_esoteric_terms(self, text: str) -> List[Dict]:
        """
        Extract esoteric terminology from text.
        
        Args:
            text: Text to extract terms from
            
        Returns:
            List of esoteric term dictionaries
        """
        terms = []
        text_lower = text.lower()
        
        # Handle literal terms with word boundaries
        for term in self.esoteric_terms:
            pattern = r'\b' + re.escape(term) + r'\b'
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                term_dict = {
                    'term': match.group(0),
                    'type': 'esoteric',
                    'start_pos': match.start(),
                    'end_pos': match.end(),
                    'context': text[max(0, match.start()-50):min(len(text), match.end()+50)]
                }
                terms.append(term_dict)
        
        # Handle regex patterns directly (without re.escape)
        for pattern in self.esoteric_regex_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                term_dict = {
                    'term': match.group(0),
                    'type': 'esoteric',
                    'start_pos': match.start(),
                    'end_pos': match.end(),
                    'context': text[max(0, match.start()-50):min(len(text), match.end()+50)]
                }
                terms.append(term_dict)
        
        # Remove duplicates
        seen = set()
        unique_terms = []
        for term in terms:
            key = term['term']
            if key not in seen:
                seen.add(key)
                unique_terms.append(term)
        
        return unique_terms
    
    def extract_events(self, text: str) -> List[Dict]:
        """
        Extract events (dates, locations, significance) from text.
        
        Args:
            text: Text to extract events from
            
        Returns:
            List of event dictionaries
        """
        events = []
        
        # Date patterns
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY
            r'\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s+\d{4}\b',  # Month DD, YYYY
            r'\b\d{4}\b'  # Year
        ]
        
        for pattern in date_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                event = {
                    'type': 'date',
                    'value': match.group(0),
                    'start_pos': match.start(),
                    'end_pos': match.end(),
                    'context': text[max(0, match.start()-50):min(len(text), match.end()+50)]
                }
                events.append(event)
        
        # Location patterns (simple - can be enhanced with NLP)
        location_keywords = ['eclipse', 'solstice', 'equinox', 'full moon', 'new moon',
                            'conjunction', 'alignment', 'event', 'ceremony', 'ritual']
        
        for keyword in location_keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            matches = re.finditer(pattern, text.lower(), re.IGNORECASE)
            for match in matches:
                event = {
                    'type': 'celestial_event',
                    'value': match.group(0),
                    'start_pos': match.start(),
                    'end_pos': match.end(),
                    'context': text[max(0, match.start()-50):min(len(text), match.end()+50)]
                }
                events.append(event)
        
        return events
    
    def analyze_narrative_structure(self, text: str) -> Dict:
        """
        Analyze narrative structure of text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with narrative structure analysis
        """
        narrative = {
            'has_beginning': False,
            'has_middle': False,
            'has_end': False,
            'has_conflict': False,
            'has_resolution': False,
            'themes': [],
            'characters': [],
            'locations': []
        }
        
        text_lower = text.lower()
        
        # Beginning indicators
        beginning_keywords = ['once', 'long ago', 'in the beginning', 'first', 'started', 'began']
        narrative['has_beginning'] = any(keyword in text_lower for keyword in beginning_keywords)
        
        # Middle indicators
        middle_keywords = ['then', 'next', 'after', 'during', 'meanwhile', 'while']
        narrative['has_middle'] = any(keyword in text_lower for keyword in middle_keywords)
        
        # End indicators
        end_keywords = ['finally', 'in the end', 'conclusion', 'ended', 'finished', 'last']
        narrative['has_end'] = any(keyword in text_lower for keyword in end_keywords)
        
        # Conflict indicators
        conflict_keywords = ['conflict', 'struggle', 'battle', 'war', 'fight', 'opposition', 'challenge']
        narrative['has_conflict'] = any(keyword in text_lower for keyword in conflict_keywords)
        
        # Resolution indicators
        resolution_keywords = ['resolved', 'solved', 'overcome', 'victory', 'triumph', 'success', 'peace']
        narrative['has_resolution'] = any(keyword in text_lower for keyword in resolution_keywords)
        
        # Extract themes (simple keyword matching)
        theme_keywords = ['love', 'hate', 'good', 'evil', 'light', 'dark', 'truth', 'lie', 'freedom', 'bondage']
        for keyword in theme_keywords:
            if keyword in text_lower:
                narrative['themes'].append(keyword)
        
        return narrative
    
    def find_symbol_relationships(self, symbols: List[Dict]) -> List[Dict]:
        """
        Find relationships between symbols.
        
        Args:
            symbols: List of symbol dictionaries
            
        Returns:
            List of relationship dictionaries
        """
        relationships = []
        
        # Group symbols by category
        by_category = {}
        for symbol in symbols:
            category = symbol['category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(symbol)
        
        # Find relationships within categories
        for category, category_symbols in by_category.items():
            if len(category_symbols) > 1:
                for i, symbol1 in enumerate(category_symbols):
                    for symbol2 in category_symbols[i+1:]:
                        relationship = {
                            'symbol1': symbol1['symbol'],
                            'symbol2': symbol2['symbol'],
                            'category': category,
                            'type': 'same_category',
                            'strength': 1.0
                        }
                        relationships.append(relationship)
        
        # Find cross-category relationships (can be enhanced with knowledge graph)
        # For now, simple proximity-based relationships
        for i, symbol1 in enumerate(symbols):
            for symbol2 in symbols[i+1:]:
                # Check if symbols are close in text
                distance = abs(symbol1['start_pos'] - symbol2['start_pos'])
                if distance < 200:  # Within 200 characters
                    relationship = {
                        'symbol1': symbol1['symbol'],
                        'symbol2': symbol2['symbol'],
                        'category1': symbol1['category'],
                        'category2': symbol2['category'],
                        'type': 'proximity',
                        'distance': distance,
                        'strength': 1.0 / (1.0 + distance / 100.0)
                    }
                    relationships.append(relationship)
        
        return relationships
    
    def store_extracted_data(self, source_id: str, extracted_data: Dict) -> bool:
        """
        Store extracted symbol/esoteric data in database.
        
        Args:
            source_id: Source ID
            extracted_data: Extracted data dictionary
            
        Returns:
            True if stored successfully, False otherwise
        """
        if not self.supabase:
            return False
        
        try:
            # Update source with extracted data
            self.supabase.table('sources')\
                .update({
                    'extracted_data': extracted_data,
                    'processed_at': datetime.utcnow().isoformat()
                })\
                .eq('id', source_id)\
                .execute()
            
            logger.info(f"Stored extracted data for source {source_id}")
            return True
        except Exception as e:
            logger.error(f"Error storing extracted data: {e}")
            return False
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute symbol extraction task.
        
        Args:
            state: Agent state with source data
            
        Returns:
            Updated state with extracted symbols
        """
        data = state.get("data", [])
        
        if not data:
            logger.warning("No data provided for symbol extraction")
            return state
        
        logger.info(f"Symbol extractor agent: Processing {len(data)} sources")
        
        try:
            all_extracted = []
            
            for source in data:
                if not isinstance(source, dict):
                    continue
                
                source_id = source.get('id')
                content = source.get('content', '') or source.get('title', '') or source.get('description', '')
                
                if not content:
                    continue
                
                # Extract symbols
                symbols = self.extract_symbols(content)
                
                # Extract esoteric terms
                esoteric_terms = self.extract_esoteric_terms(content)
                
                # Extract events
                events = self.extract_events(content)
                
                # Analyze narrative structure
                narrative = self.analyze_narrative_structure(content)
                
                # Find symbol relationships
                relationships = self.find_symbol_relationships(symbols)
                
                extracted_data = {
                    'symbols': symbols,
                    'esoteric_terms': esoteric_terms,
                    'events': events,
                    'narrative': narrative,
                    'relationships': relationships,
                    'extracted_at': datetime.utcnow().isoformat()
                }
                
                all_extracted.append({
                    'source_id': source_id,
                    'extracted_data': extracted_data
                })
                
                # Store extracted data
                if source_id:
                    self.store_extracted_data(source_id, extracted_data)
            
            # Update state
            state["context"]["extracted_symbols"] = all_extracted
            state["context"]["symbol_count"] = sum(len(e['extracted_data']['symbols']) for e in all_extracted)
            state["results"].append({
                "agent": self.name,
                "action": "extract_symbols",
                "sources_processed": len(all_extracted),
                "total_symbols": sum(len(e['extracted_data']['symbols']) for e in all_extracted),
                "total_terms": sum(len(e['extracted_data']['esoteric_terms']) for e in all_extracted)
            })
            
            logger.info(f"Symbol extraction complete: {len(all_extracted)} sources processed")
            
        except Exception as e:
            logger.error(f"Symbol extraction error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

