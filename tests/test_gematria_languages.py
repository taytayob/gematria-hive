"""
Comprehensive Language-Specific Gematria Tests

Tests all language calculations: English, Simple, Hebrew, Jewish, Kabbalah (Latin), Greek
Based on gematrix.org CSV database as baseline truth.

Author: Gematria Hive Team
Date: January 6, 2025
"""

import unittest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()


class TestEnglishGematria(unittest.TestCase):
    """Test English Gematria calculations"""
    
    def setUp(self):
        from core.gematria_engine import get_gematria_engine
        self.engine = get_gematria_engine()
    
    def test_english_basic_letters(self):
        """Test English Gematria - Basic letters (A=1, B=2, ..., Z=26)"""
        self.assertEqual(self.engine.calculate_english_gematria("A"), 1)
        self.assertEqual(self.engine.calculate_english_gematria("B"), 2)
        self.assertEqual(self.engine.calculate_english_gematria("Z"), 26)
    
    def test_english_love(self):
        """Test English Gematria - LOVE = 54 (baseline truth from gematrix789.csv)"""
        # L=12, O=15, V=22, E=5 = 54
        result = self.engine.calculate_english_gematria("LOVE")
        self.assertEqual(result, 54, "LOVE should equal 54 in English Gematria (baseline truth)")
    
    def test_english_hello(self):
        """Test English Gematria - HELLO"""
        # H=8, E=5, L=12, L=12, O=15 = 52
        result = self.engine.calculate_english_gematria("HELLO")
        self.assertEqual(result, 52, "HELLO should equal 52 in English Gematria")
    
    def test_english_case_insensitive(self):
        """Test English Gematria is case insensitive"""
        upper = self.engine.calculate_english_gematria("LOVE")
        lower = self.engine.calculate_english_gematria("love")
        mixed = self.engine.calculate_english_gematria("LoVe")
        self.assertEqual(upper, lower, "Should be case insensitive")
        self.assertEqual(upper, mixed, "Should be case insensitive")


class TestSimpleGematria(unittest.TestCase):
    """Test Simple Gematria calculations (same as English)"""
    
    def setUp(self):
        from core.gematria_engine import get_gematria_engine
        self.engine = get_gematria_engine()
    
    def test_simple_equals_english(self):
        """Test Simple Gematria equals English Gematria"""
        test_cases = ["LOVE", "HELLO", "TEST", "ABC"]
        for text in test_cases:
            english = self.engine.calculate_english_gematria(text)
            simple = self.engine.calculate_simple_gematria(text)
            self.assertEqual(english, simple, f"Simple should equal English for '{text}'")


class TestJewishGematria(unittest.TestCase):
    """Test Jewish Gematria calculations (Hebrew letter values)"""
    
    def setUp(self):
        from core.gematria_engine import get_gematria_engine
        self.engine = get_gematria_engine()
    
    def test_jewish_hebrew_letters(self):
        """Test Jewish Gematria - Hebrew letters (baseline truth from gematrix789.csv)"""
        # א = 1, ב = 2, ג = 3
        self.assertEqual(self.engine.calculate_jewish_gematria("א"), 1)
        self.assertEqual(self.engine.calculate_jewish_gematria("ב"), 2)
        self.assertEqual(self.engine.calculate_jewish_gematria("ג"), 3)
    
    def test_jewish_final_letters(self):
        """Test Jewish Gematria - Final letters"""
        # ך = 500, ם = 600, ן = 700, ף = 800, ץ = 900
        self.assertEqual(self.engine.calculate_jewish_gematria("ך"), 500)
        self.assertEqual(self.engine.calculate_jewish_gematria("ם"), 600)
        self.assertEqual(self.engine.calculate_jewish_gematria("ן"), 700)
        self.assertEqual(self.engine.calculate_jewish_gematria("ף"), 800)
        self.assertEqual(self.engine.calculate_jewish_gematria("ץ"), 900)
    
    def test_jewish_non_hebrew(self):
        """Test Jewish Gematria with non-Hebrew text returns 0"""
        result = self.engine.calculate_jewish_gematria("LOVE")
        self.assertEqual(result, 0, "Non-Hebrew text should return 0")


class TestHebrewGematria(unittest.TestCase):
    """Test Hebrew Gematria calculations (all variants)"""
    
    def setUp(self):
        from core.gematria_engine import get_gematria_engine
        self.engine = get_gematria_engine()
    
    def test_hebrew_full_equals_jewish(self):
        """Test Hebrew Full equals Jewish Gematria (baseline truth from gimatria789.csv)"""
        test_cases = ["א", "ב", "ג", "אב"]
        for text in test_cases:
            jewish = self.engine.calculate_jewish_gematria(text)
            hebrew_full = self.engine.calculate_hebrew_full(text)
            self.assertEqual(jewish, hebrew_full, f"Hebrew Full should equal Jewish for '{text}'")
    
    def test_hebrew_musafi(self):
        """Test Hebrew Musafi (base + letter_count × 1000)"""
        # For "א" (1 letter): base=1, musafi=1 + (1 × 1000) = 1001
        result = self.engine.calculate_hebrew_musafi("א")
        self.assertEqual(result, 1001, "Musafi should add 1000 per letter")
    
    def test_hebrew_katan_reduction(self):
        """Test Hebrew Katan (reduced to single digit)"""
        # ת = 400, reduced: 4+0+0 = 4
        result = self.engine.calculate_hebrew_katan("ת")
        self.assertEqual(result, 4, "ת (400) should reduce to 4")
    
    def test_hebrew_ordinal(self):
        """Test Hebrew Ordinal (position in alphabet)"""
        # א is first letter = 1
        result = self.engine.calculate_hebrew_ordinal("א")
        self.assertEqual(result, 1, "א should be position 1")
    
    def test_hebrew_atbash_mirror(self):
        """Test Hebrew Atbash (mirror/reversed alphabet)"""
        # Atbash: א ↔ ת
        result = self.engine.calculate_hebrew_atbash("א")
        self.assertIsInstance(result, int, "Atbash should return integer")
        self.assertGreater(result, 0, "Atbash should return positive value")
    
    def test_hebrew_kidmi_cumulative(self):
        """Test Hebrew Kidmi (cumulative sum)"""
        # For "אב": א=1, ב=2
        # Kidmi: cumulative=1, total=1; cumulative=1+2=3, total=1+3=4
        result = self.engine.calculate_hebrew_kidmi("אב")
        self.assertEqual(result, 4, "Kidmi should calculate cumulative sum")
    
    def test_hebrew_perati_product(self):
        """Test Hebrew Perati (product of values)"""
        # For "אב": א=1, ב=2, product = 1 × 2 = 2
        result = self.engine.calculate_hebrew_perati("אב")
        self.assertEqual(result, 2, "Perati should multiply values")
    
    def test_hebrew_shemi_name_values(self):
        """Test Hebrew Shemi (full letter name values)"""
        # Shemi uses full names of letters
        result = self.engine.calculate_hebrew_shemi("א")
        self.assertIsInstance(result, int, "Shemi should return integer")
        self.assertGreater(result, 0, "Shemi should return positive value")


class TestKabbalahLatinGematria(unittest.TestCase):
    """Test Kabbalah/Latin Gematria (Qabala Simplex) calculations"""
    
    def setUp(self):
        from core.gematria_engine import get_gematria_engine
        self.engine = get_gematria_engine()
    
    def test_latin_basic_letters(self):
        """Test Latin Gematria - Basic letters"""
        # A=1, B=2, ..., I=9, L=10, M=11, etc.
        result = self.engine.calculate_latin_gematria("A")
        self.assertEqual(result, 1, "A should equal 1 in Latin")
    
    def test_latin_special_sequence_hi(self):
        """Test Latin Gematria - Special sequence HI=27"""
        # HI should be treated as special sequence = 27
        result_hi = self.engine.calculate_latin_gematria("HI")
        # HI as special sequence should not equal H+I
        result_h = self.engine.calculate_latin_gematria("H")
        result_i = self.engine.calculate_latin_gematria("I")
        self.assertNotEqual(result_hi, result_h + result_i, "HI should be special sequence")
        self.assertEqual(result_hi, 27, "HI should equal 27 as special sequence")
    
    def test_latin_extended_letters(self):
        """Test Latin Gematria - Extended letters (J, V, W)"""
        # J=24, V=25, W=26
        result_j = self.engine.calculate_latin_gematria("J")
        result_v = self.engine.calculate_latin_gematria("V")
        result_w = self.engine.calculate_latin_gematria("W")
        self.assertEqual(result_j, 24, "J should equal 24 in Latin")
        self.assertEqual(result_v, 25, "V should equal 25 in Latin")
        self.assertEqual(result_w, 26, "W should equal 26 in Latin")


class TestGreekGematria(unittest.TestCase):
    """Test Greek Gematria calculations"""
    
    def setUp(self):
        from core.gematria_engine import get_gematria_engine
        self.engine = get_gematria_engine()
    
    def test_greek_basic_letters(self):
        """Test Greek Gematria - Basic letters"""
        # Α = 1, Β = 2, Γ = 3, etc.
        result = self.engine.calculate_greek_gematria("Α")
        self.assertEqual(result, 1, "Α should equal 1 in Greek")
        
        result = self.engine.calculate_greek_gematria("Β")
        self.assertEqual(result, 2, "Β should equal 2 in Greek")
    
    def test_greek_non_greek(self):
        """Test Greek Gematria with non-Greek text returns 0"""
        result = self.engine.calculate_greek_gematria("LOVE")
        self.assertEqual(result, 0, "Non-Greek text should return 0")


class TestSearchNum(unittest.TestCase):
    """Test Search Num (hierarchy value) for cross-language matching"""
    
    def setUp(self):
        from core.gematria_engine import get_gematria_engine
        self.engine = get_gematria_engine()
    
    def test_search_num_default_jewish(self):
        """Test search_num defaults to Jewish Gematria"""
        result = self.engine.calculate_search_num("LOVE")
        # Should use Jewish method (default)
        self.assertIsInstance(result, int, "Search_num should return integer")
    
    def test_search_num_english(self):
        """Test search_num with English method"""
        result = self.engine.calculate_search_num("LOVE", "english")
        english = self.engine.calculate_english_gematria("LOVE")
        self.assertEqual(result, english, "Search_num should match method")
    
    def test_search_num_simple(self):
        """Test search_num with Simple method"""
        result = self.engine.calculate_search_num("LOVE", "simple")
        simple = self.engine.calculate_simple_gematria("LOVE")
        self.assertEqual(result, simple, "Search_num should match method")
    
    def test_search_num_latin(self):
        """Test search_num with Latin method"""
        result = self.engine.calculate_search_num("LOVE", "latin")
        latin = self.engine.calculate_latin_gematria("LOVE")
        self.assertEqual(result, latin, "Search_num should match method")
    
    def test_search_num_greek(self):
        """Test search_num with Greek method"""
        result = self.engine.calculate_search_num("LOVE", "greek")
        greek = self.engine.calculate_greek_gematria("LOVE")
        self.assertEqual(result, greek, "Search_num should match method")
    
    def test_search_num_cross_language_matching(self):
        """Test search_num enables cross-language matching"""
        # Calculate search_num for "LOVE" using English
        search_num = self.engine.calculate_search_num("LOVE", "english")
        # This search_num can be used to find matching values across all languages
        # (requires database implementation)
        self.assertIsInstance(search_num, int, "Search_num should be integer for cross-language matching")


class TestAllLanguagesComprehensive(unittest.TestCase):
    """Comprehensive tests for all languages"""
    
    def setUp(self):
        from core.gematria_engine import get_gematria_engine
        self.engine = get_gematria_engine()
    
    def test_all_languages_calculate_all(self):
        """Test calculate_all returns values for all languages"""
        result = self.engine.calculate_all("LOVE")
        
        # Check all language methods are present
        language_methods = [
            'english_gematria',
            'simple_gematria',
            'jewish_gematria',
            'hebrew_full',
            'latin_gematria',
            'greek_gematria'
        ]
        
        for method in language_methods:
            self.assertIn(method, result, f"Method {method} missing from results")
            self.assertIsInstance(result[method], int, f"Method {method} should return int")
    
    def test_all_languages_consistency(self):
        """Test all languages return consistent results"""
        text = "LOVE"
        result1 = self.engine.calculate_all(text)
        result2 = self.engine.calculate_all(text)
        self.assertEqual(result1, result2, "Results should be consistent across calls")
    
    def test_language_specific_values(self):
        """Test language-specific values match expected formulas"""
        text = "LOVE"
        result = self.engine.calculate_all(text)
        
        # English = 54 (verified baseline truth)
        self.assertEqual(result['english_gematria'], 54, "English Gematria should equal 54")
        
        # Simple = English
        self.assertEqual(result['simple_gematria'], result['english_gematria'], "Simple should equal English")
        
        # Jewish = 0 (no Hebrew letters)
        self.assertEqual(result['jewish_gematria'], 0, "Jewish Gematria should be 0 for non-Hebrew text")
        
        # Greek = 0 (no Greek letters)
        self.assertEqual(result['greek_gematria'], 0, "Greek Gematria should be 0 for non-Greek text")


if __name__ == '__main__':
    unittest.main()

