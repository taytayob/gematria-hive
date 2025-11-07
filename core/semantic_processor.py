"""
Semantic Processor for Multi-Dimensional Word Associations
Purpose: Process words, roots, meanings, and build symmetry associations
- Understand word vs strings and roots
- Multi-dimensional meanings (orange = color/fruit/meaning/religious)
- Build symmetry and deeper associations
- Cross-language alphabet mappings
- Historical and frequency data
- Sacred geometry and esoteric connections

Author: Gematria Hive Team
Date: January 6, 2025
"""

import logging
import re
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
from collections import defaultdict
import json

logger = logging.getLogger(__name__)


class SemanticProcessor:
    """
    Processes words for multi-dimensional meanings and associations.
    Separates baseline gematria from enriched semantic data.
    """
    
    def __init__(self):
        """Initialize semantic processor."""
        # Layer types for multi-dimensional meanings
        self.layer_types = [
            'color', 'fruit', 'meaning', 'religious', 'symbolic',
            'esoteric', 'sacred_geometry', 'frequency', 'idiom', 'metaphor',
            'etymological', 'phonetic', 'cultural', 'historical'
        ]
        
        # Common word associations (example: orange)
        self.example_associations = {
            'orange': {
                'color': 'Orange color (wavelength ~590-620nm)',
                'fruit': 'Orange fruit (Citrus sinensis)',
                'meaning': 'Energy, enthusiasm, creativity',
                'religious': 'Associated with fire, transformation',
                'symbolic': 'Balance between red and yellow',
                'esoteric': 'Sacral chakra, creativity, sexuality',
                'frequency': 'Common word, high frequency',
                'idiom': 'Orange alert, orange is the new black'
            }
        }
        
        logger.info("Semantic processor initialized")
    
    def extract_word_roots(self, word: str) -> Dict:
        """
        Extract root word and etymology information.
        
        Args:
            word: Word to analyze
            
        Returns:
            Dictionary with root information
        """
        # This would integrate with etymology databases
        # For now, return structure
        return {
            'word': word,
            'root_word': None,  # Would be populated from etymology DB
            'root_language': None,
            'etymology': None,
            'phonetic_variants': [],
            'historical_forms': [],
            'language_family': None
        }
    
    def identify_semantic_layers(self, word: str) -> List[Dict]:
        """
        Identify multi-dimensional meanings for a word.
        Example: orange = color, fruit, meaning, religious, etc.
        
        Args:
            word: Word to analyze
            
        Returns:
            List of semantic layer dictionaries
        """
        layers = []
        word_lower = word.lower()
        
        # Check example associations
        if word_lower in self.example_associations:
            for layer_type, layer_value in self.example_associations[word_lower].items():
                layers.append({
                    'word': word,
                    'layer_type': layer_type,
                    'layer_value': layer_value,
                    'description': f"{word} as {layer_type}",
                    'frequency_score': 0.8,  # Would be calculated from data
                    'confidence_score': 0.9
                })
        
        # Add default layers if none found
        if not layers:
            layers.append({
                'word': word,
                'layer_type': 'meaning',
                'layer_value': word,
                'description': f"Basic meaning of {word}",
                'frequency_score': 0.5,
                'confidence_score': 0.5
            })
        
        return layers
    
    def find_word_associations(self, word: str, gematria_values: Dict) -> List[Dict]:
        """
        Find symmetry and deeper associations between words.
        
        Args:
            word: Word to find associations for
            gematria_values: Dictionary of gematria values for the word
            
        Returns:
            List of association dictionaries
        """
        associations = []
        
        # Find words with same gematria values (gematria_match)
        for method, value in gematria_values.items():
            if value and value > 0:
                associations.append({
                    'word1': word,
                    'word2': None,  # Would be populated from database
                    'association_type': 'gematria_match',
                    'strength': 0.8,
                    'gematria_values': {method: value},
                    'description': f"Words with same {method} value: {value}"
                })
        
        # Find semantic associations (would use embeddings/semantic search)
        associations.append({
            'word1': word,
            'word2': None,  # Would be populated from semantic search
            'association_type': 'semantic',
            'strength': 0.6,
            'description': f"Semantically related to {word}"
        })
        
        return associations
    
    def process_idiom_phrase(self, phrase: str) -> Dict:
        """
        Process idioms and phrases for multi-dimensional meanings.
        
        Args:
            phrase: Idiom or phrase to process
            
        Returns:
            Dictionary with idiom information
        """
        return {
            'phrase': phrase,
            'literal_meaning': None,  # Would be extracted
            'figurative_meaning': None,  # Would be extracted
            'cultural_context': None,
            'origin': None,
            'usage_examples': [],
            'semantic_layers': [],
            'gematria_values': {}
        }
    
    def build_master_blob(self, word: str, all_data: Dict) -> Dict:
        """
        Build master blob structure for a word without polluting baseline.
        
        Args:
            word: Word to build blob for
            all_data: All collected data for the word
            
        Returns:
            Master blob structure
        """
        return {
            'blob_type': 'word_complete',
            'blob_name': word,
            'blob_data': {
                'word': word,
                'baseline': {
                    'gematria_values': all_data.get('gematria_values', {}),
                    'source': all_data.get('source', 'unknown')
                },
                'semantic_layers': all_data.get('semantic_layers', []),
                'associations': all_data.get('associations', []),
                'roots': all_data.get('roots', {}),
                'frequency': all_data.get('frequency', {}),
                'symbols': all_data.get('symbols', []),
                'idioms': all_data.get('idioms', [])
            },
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'version': 1,
                'baseline_reference': all_data.get('baseline_id')
            }
        }


class AlphabetMapper:
    """
    Maps alphabets across languages (Greek, Roman, Hebrew, etc.)
    """
    
    def __init__(self):
        """Initialize alphabet mapper."""
        # Greek alphabet with values
        self.greek_alphabet = {
            'Α': {'name': 'alpha', 'value': 1, 'position': 1},
            'Β': {'name': 'beta', 'value': 2, 'position': 2},
            'Γ': {'name': 'gamma', 'value': 3, 'position': 3},
            'Δ': {'name': 'delta', 'value': 4, 'position': 4},
            'Ε': {'name': 'epsilon', 'value': 5, 'position': 5},
            'Ζ': {'name': 'zeta', 'value': 7, 'position': 6},
            'Η': {'name': 'eta', 'value': 8, 'position': 7},
            'Θ': {'name': 'theta', 'value': 9, 'position': 8},
            'Ι': {'name': 'iota', 'value': 10, 'position': 9},
            'Κ': {'name': 'kappa', 'value': 20, 'position': 10},
            'Λ': {'name': 'lambda', 'value': 30, 'position': 11, 'physics': 'wavelength'},
            'Μ': {'name': 'mu', 'value': 40, 'position': 12},
            'Ν': {'name': 'nu', 'value': 50, 'position': 13},
            'Ξ': {'name': 'xi', 'value': 60, 'position': 14},
            'Ο': {'name': 'omicron', 'value': 70, 'position': 15},
            'Π': {'name': 'pi', 'value': 80, 'position': 16, 'physics': 3.14159},
            'Ρ': {'name': 'rho', 'value': 100, 'position': 17},
            'Σ': {'name': 'sigma', 'value': 200, 'position': 18},
            'Τ': {'name': 'tau', 'value': 300, 'position': 19},
            'Υ': {'name': 'upsilon', 'value': 400, 'position': 20},
            'Φ': {'name': 'phi', 'value': 500, 'position': 21, 'physics': 'golden_ratio'},
            'Χ': {'name': 'chi', 'value': 600, 'position': 22},
            'Ψ': {'name': 'psi', 'value': 700, 'position': 23},
            'Ω': {'name': 'omega', 'value': 800, 'position': 24, 'physics': 'angular_frequency'}
        }
        
        # Roman numerals
        self.roman_numerals = {
            'I': 1, 'V': 5, 'X': 10, 'L': 50,
            'C': 100, 'D': 500, 'M': 1000
        }
        
        logger.info("Alphabet mapper initialized")
    
    def get_greek_letter_info(self, letter: str) -> Optional[Dict]:
        """Get information about a Greek letter."""
        return self.greek_alphabet.get(letter.upper())
    
    def map_cross_language(self, letter: str, from_lang: str, to_lang: str) -> Optional[str]:
        """
        Map letter from one language to another.
        
        Args:
            letter: Letter to map
            from_lang: Source language
            to_lang: Target language
            
        Returns:
            Equivalent letter in target language
        """
        # This would contain cross-language mappings
        # For now, return structure
        return None


class SymbolProcessor:
    """
    Processes symbols, sacred geometry, and esoteric associations.
    """
    
    def __init__(self):
        """Initialize symbol processor."""
        # Common symbols with meanings
        self.symbols = {
            'λ': {
                'name': 'lambda',
                'type': 'greek_letter',
                'numeric_value': 30,
                'physics_value': 'wavelength',
                'esoteric_meaning': 'Transformation, change',
                'sacred_geometry': None
            },
            'π': {
                'name': 'pi',
                'type': 'mathematical',
                'numeric_value': 80,
                'physics_value': 3.14159,
                'esoteric_meaning': 'Infinite, circular, cycles',
                'sacred_geometry': 'Circle, sphere'
            },
            'Ω': {
                'name': 'omega',
                'type': 'greek_letter',
                'numeric_value': 800,
                'physics_value': 'angular_frequency',
                'esoteric_meaning': 'End, completion, ultimate',
                'sacred_geometry': None
            },
            'φ': {
                'name': 'phi',
                'type': 'mathematical',
                'numeric_value': 500,
                'physics_value': 1.618,  # Golden ratio
                'esoteric_meaning': 'Divine proportion, harmony',
                'sacred_geometry': 'Golden ratio, pentagram'
            },
            '∞': {
                'name': 'infinity',
                'type': 'mathematical',
                'numeric_value': None,
                'physics_value': None,
                'esoteric_meaning': 'Eternal, infinite, boundless',
                'sacred_geometry': 'Lemniscate, ouroboros'
            }
        }
        
        logger.info("Symbol processor initialized")
    
    def get_symbol_info(self, symbol: str) -> Optional[Dict]:
        """Get information about a symbol."""
        return self.symbols.get(symbol)


def get_semantic_processor():
    """Get singleton semantic processor instance."""
    if not hasattr(get_semantic_processor, '_instance'):
        get_semantic_processor._instance = SemanticProcessor()
    return get_semantic_processor._instance


def get_alphabet_mapper():
    """Get singleton alphabet mapper instance."""
    if not hasattr(get_alphabet_mapper, '_instance'):
        get_alphabet_mapper._instance = AlphabetMapper()
    return get_alphabet_mapper._instance


def get_symbol_processor():
    """Get singleton symbol processor instance."""
    if not hasattr(get_symbol_processor, '_instance'):
        get_symbol_processor._instance = SymbolProcessor()
    return get_symbol_processor._instance

