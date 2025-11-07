"""
Gematria Calculation Engine
Purpose: Exact gematrix.org calculation algorithms for all methods
- Jewish, English, Simple, Latin, Greek, Hebrew variants
- Search_num hierarchy implementation
- Cross-language matching

Author: Gematria Hive Team
Date: January 6, 2025
"""

import logging
import re
from typing import Dict, Optional, List, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class GematriaEngine:
    """
    Gematria calculation engine implementing exact gematrix.org algorithms.
    """
    
    def __init__(self):
        """Initialize gematria engine with all calculation methods."""
        # Jewish Gematria (Hebrew alphabet values)
        self.jewish_values = {
            'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9,
            'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60, 'ע': 70, 'פ': 80, 'צ': 90,
            'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,
            'ך': 500, 'ם': 600, 'ן': 700, 'ף': 800, 'ץ': 900
        }
        
        # English Gematria (A=1, B=2, ..., Z=26)
        self.english_values = {chr(i): i - 64 for i in range(65, 91)}  # A-Z
        
        # Simple Gematria (same as English for compatibility)
        self.simple_values = self.english_values.copy()
        
        # Latin Gematria (Qabala Simplex) - A=1, B=2, ..., Z=22
        # Based on 23-letter Latin alphabet, extended to 27 letters
        latin_base = 'ABCDEFGHILMNOPQRSTVXYZ'  # 23 letters
        self.latin_values = {}
        for i, char in enumerate(latin_base, 1):
            self.latin_values[char] = i
        # Additional letters: J, V, Hi, W (Hu) - mapped to 24-27
        self.latin_values['J'] = 24
        self.latin_values['V'] = 25
        self.latin_values['W'] = 26
        self.latin_values['HI'] = 27
        
        # Greek Gematria (classical Greek alphabet values)
        self.greek_values = {
            'Α': 1, 'Β': 2, 'Γ': 3, 'Δ': 4, 'Ε': 5, 'Ϝ': 6, 'Ζ': 7, 'Η': 8, 'Θ': 9,
            'Ι': 10, 'Κ': 20, 'Λ': 30, 'Μ': 40, 'Ν': 50, 'Ξ': 60, 'Ο': 70, 'Π': 80, 'Ϙ': 90,
            'Ρ': 100, 'Σ': 200, 'Τ': 300, 'Υ': 400, 'Φ': 500, 'Χ': 600, 'Ψ': 700, 'Ω': 800
        }
        
        # Hebrew variant values (for reference, actual calculation in methods)
        self.hebrew_variants = {
            'full': self.jewish_values.copy(),
            'musafi': {},  # Calculated separately
            'katan': {},   # Calculated separately
            'ordinal': {}, # Calculated separately
            'atbash': {},  # Calculated separately
            'kidmi': {},   # Calculated separately
            'perati': {},  # Calculated separately
            'shemi': {}    # Calculated separately
        }
        
        logger.info("Gematria engine initialized with all calculation methods")
    
    def calculate_jewish_gematria(self, text: str) -> int:
        """
        Calculate Jewish Gematria value.
        
        Args:
            text: Text to calculate (Hebrew or transliterated)
            
        Returns:
            Gematria value
        """
        total = 0
        for char in text.upper():
            if char in self.jewish_values:
                total += self.jewish_values[char]
        return total
    
    def calculate_english_gematria(self, text: str) -> int:
        """
        Calculate English Gematria value (A=1, B=2, ..., Z=26).
        
        Args:
            text: Text to calculate
            
        Returns:
            Gematria value
        """
        total = 0
        for char in text.upper():
            if char in self.english_values:
                total += self.english_values[char]
        return total
    
    def calculate_simple_gematria(self, text: str) -> int:
        """
        Calculate Simple Gematria value (same as English).
        
        Args:
            text: Text to calculate
            
        Returns:
            Gematria value
        """
        return self.calculate_english_gematria(text)
    
    def calculate_latin_gematria(self, text: str) -> int:
        """
        Calculate Latin Gematria (Qabala Simplex) value.
        A=1, B=2, ..., Z=22, with J, V, W, Hi mapped to 24-27.
        
        Args:
            text: Text to calculate
            
        Returns:
            Gematria value
        """
        total = 0
        text_upper = text.upper()
        i = 0
        while i < len(text_upper):
            char = text_upper[i]
            # Check for special sequences
            if i < len(text_upper) - 1 and text_upper[i:i+2] == 'HI':
                total += 27
                i += 2
            elif char in self.latin_values:
                total += self.latin_values[char]
                i += 1
            else:
                i += 1
        return total
    
    def calculate_greek_gematria(self, text: str) -> int:
        """
        Calculate Greek Gematria value.
        
        Args:
            text: Text to calculate (Greek alphabet)
            
        Returns:
            Gematria value
        """
        total = 0
        for char in text.upper():
            if char in self.greek_values:
                total += self.greek_values[char]
        return total
    
    def calculate_hebrew_full(self, text: str) -> int:
        """
        Calculate Hebrew Full Gematria (same as Jewish).
        
        Args:
            text: Text to calculate
            
        Returns:
            Gematria value
        """
        return self.calculate_jewish_gematria(text)
    
    def calculate_hebrew_musafi(self, text: str) -> int:
        """
        Calculate Hebrew Musafi Gematria.
        
        Args:
            text: Text to calculate
            
        Returns:
            Gematria value
        """
        # Musafi adds 1000 for each letter
        base = self.calculate_jewish_gematria(text)
        letter_count = sum(1 for c in text.upper() if c in self.jewish_values)
        return base + (letter_count * 1000)
    
    def calculate_hebrew_katan(self, text: str) -> int:
        """
        Calculate Hebrew Katan Gematria (reduced values).
        
        Args:
            text: Text to calculate
            
        Returns:
            Gematria value
        """
        total = 0
        for char in text.upper():
            if char in self.jewish_values:
                value = self.jewish_values[char]
                # Reduce to single digit (1-9)
                while value > 9:
                    value = sum(int(d) for d in str(value))
                total += value
        return total
    
    def calculate_hebrew_ordinal(self, text: str) -> int:
        """
        Calculate Hebrew Ordinal Gematria (position in alphabet).
        
        Args:
            text: Text to calculate
            
        Returns:
            Gematria value
        """
        hebrew_order = 'אבגדהוזחטיכסעפצקרשת'
        total = 0
        for char in text:
            if char in hebrew_order:
                total += hebrew_order.index(char) + 1
        return total
    
    def calculate_hebrew_atbash(self, text: str) -> int:
        """
        Calculate Hebrew Atbash Gematria (reversed alphabet).
        
        Args:
            text: Text to calculate
            
        Returns:
            Gematria value
        """
        # Atbash: א=ת, ב=ש, ג=ר, etc.
        atbash_map = {
            'א': 'ת', 'ב': 'ש', 'ג': 'ר', 'ד': 'ק', 'ה': 'צ', 'ו': 'פ', 'ז': 'ע', 'ח': 'ס', 'ט': 'נ',
            'י': 'מ', 'כ': 'ל', 'ל': 'כ', 'מ': 'י', 'נ': 'ט', 'ס': 'ח', 'ע': 'ז', 'פ': 'ו', 'צ': 'ה',
            'ק': 'ד', 'ר': 'ג', 'ש': 'ב', 'ת': 'א'
        }
        atbash_text = ''.join(atbash_map.get(c, c) for c in text)
        return self.calculate_jewish_gematria(atbash_text)
    
    def calculate_hebrew_kidmi(self, text: str) -> int:
        """
        Calculate Hebrew Kidmi Gematria (cumulative sum).
        
        Args:
            text: Text to calculate
            
        Returns:
            Gematria value
        """
        total = 0
        cumulative = 0
        for char in text.upper():
            if char in self.jewish_values:
                cumulative += self.jewish_values[char]
                total += cumulative
        return total
    
    def calculate_hebrew_perati(self, text: str) -> int:
        """
        Calculate Hebrew Perati Gematria (product of values).
        
        Args:
            text: Text to calculate
            
        Returns:
            Gematria value
        """
        product = 1
        for char in text.upper():
            if char in self.jewish_values:
                product *= self.jewish_values[char]
        return product
    
    def calculate_hebrew_shemi(self, text: str) -> int:
        """
        Calculate Hebrew Shemi Gematria (name values).
        
        Args:
            text: Text to calculate
            
        Returns:
            Gematria value
        """
        # Shemi uses full names of letters
        shemi_names = {
            'א': 'אלף', 'ב': 'בית', 'ג': 'גימל', 'ד': 'דלת', 'ה': 'הא',
            'ו': 'ואו', 'ז': 'זין', 'ח': 'חית', 'ט': 'טית', 'י': 'יוד',
            'כ': 'כף', 'ל': 'למד', 'מ': 'מם', 'נ': 'נון', 'ס': 'סמך',
            'ע': 'עין', 'פ': 'פא', 'צ': 'צדי', 'ק': 'קוף', 'ר': 'ריש',
            'ש': 'שין', 'ת': 'תיו'
        }
        total = 0
        for char in text:
            if char in shemi_names:
                name = shemi_names[char]
                total += self.calculate_jewish_gematria(name)
        return total
    
    def calculate_search_num(self, text: str, method: str = 'jewish') -> int:
        """
        Calculate search_num (hierarchy value) for cross-language matching.
        
        Args:
            text: Text to calculate
            method: Primary method ('jewish', 'english', 'simple', 'latin', 'greek')
            
        Returns:
            Search_num value
        """
        method_map = {
            'jewish': self.calculate_jewish_gematria,
            'english': self.calculate_english_gematria,
            'simple': self.calculate_simple_gematria,
            'latin': self.calculate_latin_gematria,
            'greek': self.calculate_greek_gematria
        }
        
        calc_func = method_map.get(method.lower(), self.calculate_jewish_gematria)
        return calc_func(text)
    
    def calculate_all(self, text: str) -> Dict[str, int]:
        """
        Calculate all gematria values for a given text.
        
        Args:
            text: Text to calculate
            
        Returns:
            Dictionary with all gematria values
        """
        return {
            'jewish_gematria': self.calculate_jewish_gematria(text),
            'english_gematria': self.calculate_english_gematria(text),
            'simple_gematria': self.calculate_simple_gematria(text),
            'latin_gematria': self.calculate_latin_gematria(text),
            'greek_gematria': self.calculate_greek_gematria(text),
            'hebrew_full': self.calculate_hebrew_full(text),
            'hebrew_musafi': self.calculate_hebrew_musafi(text),
            'hebrew_katan': self.calculate_hebrew_katan(text),
            'hebrew_ordinal': self.calculate_hebrew_ordinal(text),
            'hebrew_atbash': self.calculate_hebrew_atbash(text),
            'hebrew_kidmi': self.calculate_hebrew_kidmi(text),
            'hebrew_perati': self.calculate_hebrew_perati(text),
            'hebrew_shemi': self.calculate_hebrew_shemi(text),
            'search_num': self.calculate_search_num(text, 'jewish')
        }
    
    def calculate_with_breakdown(self, text: str, method: str = 'english_gematria') -> Dict:
        """
        Calculate gematria value with step-by-step breakdown showing how each letter contributes.
        
        Args:
            text: Text to calculate
            method: Gematria method to use
            
        Returns:
            Dictionary with total value and step-by-step breakdown
        """
        breakdown = {
            'text': text,
            'method': method,
            'total': 0,
            'steps': [],
            'formula': ''
        }
        
        text_upper = text.upper()
        
        # Map method to calculation function and values
        method_map = {
            'english_gematria': (self.english_values, 'English Gematria (A=1, B=2, ..., Z=26)'),
            'simple_gematria': (self.english_values, 'Simple Gematria (same as English)'),
            'jewish_gematria': (self.jewish_values, 'Jewish Gematria (Hebrew alphabet values)'),
            'latin_gematria': (self.latin_values, 'Latin Gematria (Qabala Simplex)'),
            'greek_gematria': (self.greek_values, 'Greek Gematria (Classical Greek alphabet)'),
        }
        
        if method in method_map:
            values_dict, formula_desc = method_map[method]
            breakdown['formula'] = formula_desc
            
            if method == 'latin_gematria':
                # Special handling for Latin (HI sequence)
                i = 0
                while i < len(text_upper):
                    char = text_upper[i]
                    if i < len(text_upper) - 1 and text_upper[i:i+2] == 'HI':
                        value = 27
                        breakdown['steps'].append({
                            'char': 'HI',
                            'value': value,
                            'running_total': breakdown['total'] + value
                        })
                        breakdown['total'] += value
                        i += 2
                    elif char in values_dict:
                        value = values_dict[char]
                        breakdown['steps'].append({
                            'char': char,
                            'value': value,
                            'running_total': breakdown['total'] + value
                        })
                        breakdown['total'] += value
                        i += 1
                    else:
                        breakdown['steps'].append({
                            'char': char,
                            'value': 0,
                            'running_total': breakdown['total'],
                            'note': 'Not in alphabet'
                        })
                        i += 1
            else:
                # Standard handling for other methods
                for char in text_upper:
                    if char in values_dict:
                        value = values_dict[char]
                        breakdown['steps'].append({
                            'char': char,
                            'value': value,
                            'running_total': breakdown['total'] + value
                        })
                        breakdown['total'] += value
                    else:
                        breakdown['steps'].append({
                            'char': char,
                            'value': 0,
                            'running_total': breakdown['total'],
                            'note': 'Not in alphabet'
                        })
        else:
            # For methods without simple letter mapping, calculate total
            method_func_map = {
                'hebrew_full': self.calculate_hebrew_full,
                'hebrew_musafi': self.calculate_hebrew_musafi,
                'hebrew_katan': self.calculate_hebrew_katan,
                'hebrew_ordinal': self.calculate_hebrew_ordinal,
                'hebrew_atbash': self.calculate_hebrew_atbash,
                'hebrew_kidmi': self.calculate_hebrew_kidmi,
                'hebrew_perati': self.calculate_hebrew_perati,
                'hebrew_shemi': self.calculate_hebrew_shemi,
            }
            
            if method in method_func_map:
                breakdown['total'] = method_func_map[method](text)
                breakdown['formula'] = f'{method.replace("_", " ").title()} (complex calculation)'
                # For complex methods, show character breakdown with Jewish values as reference
                for char in text_upper:
                    if char in self.jewish_values:
                        value = self.jewish_values[char]
                        breakdown['steps'].append({
                            'char': char,
                            'value': value,
                            'note': 'Hebrew letter (reference)'
                        })
                    else:
                        breakdown['steps'].append({
                            'char': char,
                            'value': 0,
                            'note': 'Not in Hebrew alphabet'
                        })
        
        return breakdown
    
    def find_matching_values(self, value: int, method: str = 'jewish') -> List[Dict]:
        """
        Find all phrases with matching gematria value (requires database).
        
        Args:
            value: Gematria value to search for
            method: Gematria method to search
            
        Returns:
            List of matching phrases
        """
        # This would query the database - placeholder for now
        # Actual implementation would use Supabase client
        return []
    
    def get_cross_language_matches(self, text: str) -> Dict[str, List[Dict]]:
        """
        Find matching values across all languages using search_num hierarchy.
        
        Args:
            text: Text to find matches for
            
        Returns:
            Dictionary with matches for each language
        """
        search_num = self.calculate_search_num(text)
        matches = {}
        
        # For each language, find phrases with same search_num
        for method in ['jewish', 'english', 'simple', 'latin', 'greek']:
            matches[method] = self.find_matching_values(search_num, method)
        
        return matches
    
    # ============================================================================
    # ADVANCED CALCULATION METHODS (Placeholders for Future Implementation)
    # These will be implemented based on ingestion data and research
    # ============================================================================
    
    def calculate_numerology(self, text: str, method: str = 'life_path') -> int:
        """
        Calculate numerology value.
        
        TODO: Implement based on ingestion data from CSV
        Planned methods:
        - life_path: Sum of birth date digits reduced to single digit
        - expression: Sum of full name reduced to single digit
        - soul: Sum of vowels reduced to single digit
        - personality: Sum of consonants reduced to single digit
        - birthday: Day of birth reduced to single digit
        
        Args:
            text: Text to calculate (or birth date/name)
            method: Numerology method ('life_path', 'expression', 'soul', 'personality', 'birthday')
            
        Returns:
            Numerology value
        """
        # Placeholder - will be implemented from CSV data
        logger.warning(f"Numerology calculation ({method}) not yet implemented - placeholder")
        return 0
    
    def calculate_orthogonal(self, text: str, method: str = 'sum') -> int:
        """
        Calculate orthogonal gematria value (perpendicular relationships).
        
        TODO: Implement based on geometric relationships from ingestion data
        Planned methods:
        - sum: Sum of values at right angles
        - product: Product of orthogonal values
        - distance: Distance between orthogonal points
        
        Args:
            text: Text to calculate
            method: Orthogonal method ('sum', 'product', 'distance')
            
        Returns:
            Orthogonal gematria value
        """
        # Placeholder - will be implemented from CSV data
        logger.warning(f"Orthogonal calculation ({method}) not yet implemented - placeholder")
        return 0
    
    def calculate_orthodontal(self, text: str, method: str = 'sum') -> int:
        """
        Calculate orthodontal gematria value (straight-line relationships).
        
        TODO: Implement based on linear relationships from ingestion data
        Planned methods:
        - sum: Sum along straight line
        - product: Product along straight line
        - sequence: Sequential values along line
        
        Args:
            text: Text to calculate
            method: Orthodontal method ('sum', 'product', 'sequence')
            
        Returns:
            Orthodontal gematria value
        """
        # Placeholder - will be implemented from CSV data
        logger.warning(f"Orthodontal calculation ({method}) not yet implemented - placeholder")
        return 0
    
    def calculate_mirror(self, text: str, method: str = 'sum') -> int:
        """
        Calculate mirror gematria value (beyond Atbash).
        
        TODO: Implement based on mirror relationships from ingestion data
        Planned methods:
        - sum: Sum of original + reversed
        - product: Product of original × reversed
        - difference: Difference between original and reversed
        - ratio: Ratio of original to reversed
        
        Args:
            text: Text to calculate
            method: Mirror method ('sum', 'product', 'difference', 'ratio')
            
        Returns:
            Mirror gematria value
        """
        # Placeholder - will be implemented from CSV data
        logger.warning(f"Mirror calculation ({method}) not yet implemented - placeholder")
        return 0
    
    def calculate_prime(self, text: str, method: str = 'sum') -> int:
        """
        Calculate prime-based gematria value.
        
        TODO: Implement based on prime number relationships from ingestion data
        Planned methods:
        - sum: Sum of prime factors
        - product: Product of prime factors
        - distance: Distance to nearest prime
        - sequence: Position in prime sequence
        
        Args:
            text: Text to calculate
            method: Prime method ('sum', 'product', 'distance', 'sequence')
            
        Returns:
            Prime-based gematria value
        """
        # Placeholder - will be implemented from CSV data
        logger.warning(f"Prime calculation ({method}) not yet implemented - placeholder")
        return 0
    
    def calculate_fibonacci(self, text: str, method: str = 'sum') -> int:
        """
        Calculate Fibonacci-based gematria value.
        
        TODO: Implement based on Fibonacci sequence relationships from ingestion data
        
        Args:
            text: Text to calculate
            method: Fibonacci method
            
        Returns:
            Fibonacci-based gematria value
        """
        # Placeholder - will be implemented from CSV data
        logger.warning(f"Fibonacci calculation ({method}) not yet implemented - placeholder")
        return 0
    
    def calculate_golden_ratio(self, text: str, method: str = 'sum') -> int:
        """
        Calculate golden ratio-based gematria value.
        
        TODO: Implement based on golden ratio relationships from ingestion data
        
        Args:
            text: Text to calculate
            method: Golden ratio method
            
        Returns:
            Golden ratio-based gematria value
        """
        # Placeholder - will be implemented from CSV data
        logger.warning(f"Golden ratio calculation ({method}) not yet implemented - placeholder")
        return 0
    
    def calculate_sacred_geometry(self, text: str, method: str = 'sum') -> int:
        """
        Calculate sacred geometry-based gematria value.
        
        TODO: Implement based on geometric relationships from ingestion data
        
        Args:
            text: Text to calculate
            method: Sacred geometry method
            
        Returns:
            Sacred geometry-based gematria value
        """
        # Placeholder - will be implemented from CSV data
        logger.warning(f"Sacred geometry calculation ({method}) not yet implemented - placeholder")
        return 0
    
    def calculate_wave(self, text: str, method: str = 'sum') -> int:
        """
        Calculate wave/harmonic-based gematria value.
        
        TODO: Implement based on wave/harmonic relationships from ingestion data
        
        Args:
            text: Text to calculate
            method: Wave method
            
        Returns:
            Wave-based gematria value
        """
        # Placeholder - will be implemented from CSV data
        logger.warning(f"Wave calculation ({method}) not yet implemented - placeholder")
        return 0
    
    def calculate_quantum(self, text: str, method: str = 'sum') -> int:
        """
        Calculate quantum state-based gematria value.
        
        TODO: Implement based on quantum relationships from ingestion data
        
        Args:
            text: Text to calculate
            method: Quantum method
            
        Returns:
            Quantum-based gematria value
        """
        # Placeholder - will be implemented from CSV data
        logger.warning(f"Quantum calculation ({method}) not yet implemented - placeholder")
        return 0
    
    def calculate_temporal(self, text: str, method: str = 'sum') -> int:
        """
        Calculate temporal/time-based gematria value.
        
        TODO: Implement based on temporal relationships from ingestion data
        
        Args:
            text: Text to calculate
            method: Temporal method
            
        Returns:
            Temporal-based gematria value
        """
        # Placeholder - will be implemented from CSV data
        logger.warning(f"Temporal calculation ({method}) not yet implemented - placeholder")
        return 0
    
    def calculate_spatial(self, text: str, method: str = 'sum') -> int:
        """
        Calculate spatial/3D-based gematria value.
        
        TODO: Implement based on spatial relationships from ingestion data
        
        Args:
            text: Text to calculate
            method: Spatial method
            
        Returns:
            Spatial-based gematria value
        """
        # Placeholder - will be implemented from CSV data
        logger.warning(f"Spatial calculation ({method}) not yet implemented - placeholder")
        return 0


# Singleton instance
_gematria_engine = None

def get_gematria_engine() -> GematriaEngine:
    """Get or create gematria engine singleton."""
    global _gematria_engine
    if _gematria_engine is None:
        _gematria_engine = GematriaEngine()
    return _gematria_engine

