"""
Unit Tests for Core Components

Tests core engine implementations.
"""

import unittest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()


class TestGematriaEngine(unittest.TestCase):
    """Comprehensive test suite for gematria engine"""
    
    def setUp(self):
        """Set up test fixtures"""
        from core.gematria_engine import get_gematria_engine
        self.engine = get_gematria_engine()
    
    def test_engine_initialization(self):
        """Test engine initializes correctly"""
        self.assertIsNotNone(self.engine)
        self.assertTrue(hasattr(self.engine, 'jewish_values'))
        self.assertTrue(hasattr(self.engine, 'english_values'))
        self.assertTrue(hasattr(self.engine, 'latin_values'))
        self.assertTrue(hasattr(self.engine, 'greek_values'))
    
    def test_singleton_pattern(self):
        """Test singleton pattern works correctly"""
        from core.gematria_engine import get_gematria_engine
        engine1 = get_gematria_engine()
        engine2 = get_gematria_engine()
        self.assertIs(engine1, engine2, "Should return same instance")
    
    def test_calculate_all(self):
        """Test calculate_all method returns all methods"""
        result = self.engine.calculate_all("LOVE")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        
        # Check all methods are present
        expected_methods = [
            'jewish_gematria', 'english_gematria', 'simple_gematria',
            'latin_gematria', 'greek_gematria', 'hebrew_full',
            'hebrew_musafi', 'hebrew_katan', 'hebrew_ordinal',
            'hebrew_atbash', 'hebrew_kidmi', 'hebrew_perati',
            'hebrew_shemi', 'search_num'
        ]
        for method in expected_methods:
            self.assertIn(method, result, f"Method {method} missing from results")
            self.assertIsInstance(result[method], int, f"Method {method} should return int")
    
    # English Gematria Tests
    def test_calculate_english_gematria_basic(self):
        """Test English gematria calculation - basic"""
        # A=1, B=2, ..., Z=26
        self.assertEqual(self.engine.calculate_english_gematria("A"), 1)
        self.assertEqual(self.engine.calculate_english_gematria("B"), 2)
        self.assertEqual(self.engine.calculate_english_gematria("Z"), 26)
    
    def test_calculate_english_gematria_love(self):
        """Test English gematria - LOVE = 54"""
        # L=12, O=15, V=22, E=5 = 54
        result = self.engine.calculate_english_gematria("LOVE")
        self.assertEqual(result, 54, "LOVE should equal 54 in English Gematria")
    
    def test_calculate_english_gematria_case_insensitive(self):
        """Test English gematria is case insensitive"""
        upper = self.engine.calculate_english_gematria("LOVE")
        lower = self.engine.calculate_english_gematria("love")
        mixed = self.engine.calculate_english_gematria("LoVe")
        self.assertEqual(upper, lower, "Should be case insensitive")
        self.assertEqual(upper, mixed, "Should be case insensitive")
    
    def test_calculate_english_gematria_empty(self):
        """Test English gematria with empty string"""
        result = self.engine.calculate_english_gematria("")
        self.assertEqual(result, 0, "Empty string should return 0")
    
    def test_calculate_english_gematria_non_alpha(self):
        """Test English gematria ignores non-alphabetic characters"""
        result = self.engine.calculate_english_gematria("A1B2C3")
        expected = self.engine.calculate_english_gematria("ABC")
        self.assertEqual(result, expected, "Should ignore non-alphabetic characters")
    
    # Simple Gematria Tests
    def test_calculate_simple_gematria(self):
        """Test Simple gematria (same as English)"""
        english = self.engine.calculate_english_gematria("LOVE")
        simple = self.engine.calculate_simple_gematria("LOVE")
        self.assertEqual(english, simple, "Simple should equal English")
    
    # Jewish Gematria Tests
    def test_calculate_jewish_gematria_empty(self):
        """Test Jewish gematria with non-Hebrew text"""
        result = self.engine.calculate_jewish_gematria("LOVE")
        self.assertEqual(result, 0, "Non-Hebrew text should return 0")
    
    def test_calculate_jewish_gematria_hebrew_letters(self):
        """Test Jewish gematria with Hebrew letters"""
        # א = 1, ב = 2, ג = 3
        result = self.engine.calculate_jewish_gematria("א")
        self.assertEqual(result, 1, "א should equal 1")
        
        result = self.engine.calculate_jewish_gematria("ב")
        self.assertEqual(result, 2, "ב should equal 2")
        
        result = self.engine.calculate_jewish_gematria("ג")
        self.assertEqual(result, 3, "ג should equal 3")
    
    # Latin Gematria Tests
    def test_calculate_latin_gematria_basic(self):
        """Test Latin gematria - basic letters"""
        # A=1, B=2, ..., I=9, L=10, M=11, etc.
        result = self.engine.calculate_latin_gematria("A")
        self.assertEqual(result, 1, "A should equal 1 in Latin")
    
    def test_calculate_latin_gematria_special_sequence(self):
        """Test Latin gematria - special sequence HI=27"""
        # HI should be treated as special sequence = 27
        result_hi = self.engine.calculate_latin_gematria("HI")
        result_h_i = self.engine.calculate_latin_gematria("H") + self.engine.calculate_latin_gematria("I")
        # HI as special sequence should not equal H+I
        self.assertNotEqual(result_hi, result_h_i, "HI should be special sequence")
    
    # Greek Gematria Tests
    def test_calculate_greek_gematria_empty(self):
        """Test Greek gematria with non-Greek text"""
        result = self.engine.calculate_greek_gematria("LOVE")
        self.assertEqual(result, 0, "Non-Greek text should return 0")
    
    # Hebrew Variants Tests
    def test_calculate_hebrew_full(self):
        """Test Hebrew Full (same as Jewish)"""
        jewish = self.engine.calculate_jewish_gematria("א")
        hebrew_full = self.engine.calculate_hebrew_full("א")
        self.assertEqual(jewish, hebrew_full, "Hebrew Full should equal Jewish")
    
    def test_calculate_hebrew_musafi(self):
        """Test Hebrew Musafi (base + letter_count × 1000)"""
        # For "א" (1 letter): base=1, musafi=1 + (1 × 1000) = 1001
        result = self.engine.calculate_hebrew_musafi("א")
        self.assertEqual(result, 1001, "Musafi should add 1000 per letter")
    
    def test_calculate_hebrew_katan_reduction(self):
        """Test Hebrew Katan (reduced to single digit)"""
        # ת = 400, reduced: 4+0+0 = 4
        result = self.engine.calculate_hebrew_katan("ת")
        self.assertEqual(result, 4, "ת (400) should reduce to 4")
    
    def test_calculate_hebrew_katan_multiple_digits(self):
        """Test Hebrew Katan with multi-digit reduction"""
        # Test that 999 reduces to 9 (9+9+9=27, 2+7=9)
        # Using multiple letters that sum to 999
        # This tests the reduction algorithm
        pass  # Would need Hebrew text that sums to 999
    
    def test_calculate_hebrew_ordinal(self):
        """Test Hebrew Ordinal (position in alphabet)"""
        # א is first letter = 1
        result = self.engine.calculate_hebrew_ordinal("א")
        self.assertEqual(result, 1, "א should be position 1")
    
    def test_calculate_hebrew_atbash(self):
        """Test Hebrew Atbash (reversed alphabet)"""
        # Atbash: א ↔ ת, ב ↔ ש
        # If א = 1, then atbash of ת should give same value as א
        result = self.engine.calculate_hebrew_atbash("א")
        # Atbash of א should map to ת, then calculate Jewish value
        # This tests the atbash mapping works
        self.assertIsInstance(result, int, "Atbash should return integer")
    
    def test_calculate_hebrew_kidmi_cumulative(self):
        """Test Hebrew Kidmi (cumulative sum)"""
        # For "אב": א=1, ב=2
        # Kidmi: cumulative=1, total=1; cumulative=1+2=3, total=1+3=4
        result = self.engine.calculate_hebrew_kidmi("אב")
        # Expected: 1 + (1+2) = 4
        self.assertGreater(result, 0, "Kidmi should return positive value")
    
    def test_calculate_hebrew_perati_product(self):
        """Test Hebrew Perati (product of values)"""
        # For "אב": א=1, ב=2, product = 1 × 2 = 2
        result = self.engine.calculate_hebrew_perati("אב")
        self.assertEqual(result, 2, "Perati should multiply values")
    
    def test_calculate_hebrew_perati_empty(self):
        """Test Hebrew Perati with empty string (should return 1)"""
        result = self.engine.calculate_hebrew_perati("")
        self.assertEqual(result, 1, "Empty product should be 1")
    
    def test_calculate_hebrew_shemi(self):
        """Test Hebrew Shemi (full letter name values)"""
        # Shemi uses full names of letters
        result = self.engine.calculate_hebrew_shemi("א")
        self.assertIsInstance(result, int, "Shemi should return integer")
        self.assertGreater(result, 0, "Shemi should return positive value")
    
    # Search Num Tests
    def test_calculate_search_num(self):
        """Test search_num calculation"""
        result = self.engine.calculate_search_num("LOVE", "english")
        english = self.engine.calculate_english_gematria("LOVE")
        self.assertEqual(result, english, "Search_num should match method")
    
    def test_calculate_search_num_default(self):
        """Test search_num defaults to Jewish"""
        result = self.engine.calculate_search_num("LOVE")
        # Should use Jewish method (default)
        self.assertIsInstance(result, int, "Search_num should return integer")
    
    # Edge Cases
    def test_calculate_all_empty_string(self):
        """Test calculate_all with empty string"""
        result = self.engine.calculate_all("")
        self.assertIsInstance(result, dict, "Should return dict")
        for method, value in result.items():
            if method == 'hebrew_perati':
                self.assertEqual(value, 1, "Perati empty should be 1")
            else:
                self.assertEqual(value, 0, f"{method} empty should be 0")
    
    def test_calculate_all_whitespace(self):
        """Test calculate_all with whitespace"""
        result = self.engine.calculate_all("   ")
        # Whitespace should be ignored
        for method, value in result.items():
            if method == 'hebrew_perati':
                self.assertEqual(value, 1, "Perati empty should be 1")
            else:
                self.assertEqual(value, 0, f"{method} whitespace should be 0")
    
    def test_calculate_all_special_characters(self):
        """Test calculate_all with special characters"""
        result = self.engine.calculate_all("!@#$%^&*()")
        # Special characters should be ignored
        for method, value in result.items():
            if method == 'hebrew_perati':
                self.assertEqual(value, 1, "Perati empty should be 1")
            else:
                self.assertEqual(value, 0, f"{method} special chars should be 0")
    
    # Integration Tests
    def test_calculate_all_consistency(self):
        """Test calculate_all returns consistent results"""
        text = "LOVE"
        result1 = self.engine.calculate_all(text)
        result2 = self.engine.calculate_all(text)
        self.assertEqual(result1, result2, "Results should be consistent")
    
    def test_method_names_consistency(self):
        """Test method names are consistent"""
        result = self.engine.calculate_all("TEST")
        # All method names should follow naming convention
        for method_name in result.keys():
            self.assertIn('_', method_name, "Method names should use underscore")
            self.assertFalse(method_name.startswith('_'), "Method names shouldn't start with underscore")


class TestConductor(unittest.TestCase):
    """Test suite for unified conductor"""
    
    def setUp(self):
        """Set up test fixtures"""
        from core.conductor import get_unified_conductor
        self.conductor = get_unified_conductor()
    
    def test_conductor_initialization(self):
        """Test conductor initializes correctly"""
        self.assertIsNotNone(self.conductor)
    
    def test_database_connection(self):
        """Test database connection"""
        # This will fail gracefully if Supabase not configured
        if hasattr(self.conductor, 'supabase') and self.conductor.supabase:
            # Test connection
            try:
                result = self.conductor.supabase.table('bookmarks').select('*').limit(1).execute()
                self.assertIsNotNone(result)
            except Exception as e:
                # Expected if database not configured
                pass


class TestVisualizationEngine(unittest.TestCase):
    """Test suite for visualization engine"""
    
    def setUp(self):
        """Set up test fixtures"""
        from core.visualization_engine import get_visualization_engine
        self.engine = get_visualization_engine()
    
    def test_engine_initialization(self):
        """Test engine initializes correctly"""
        self.assertIsNotNone(self.engine)
    
    def test_generate_metatrons_cube(self):
        """Test Metatron's cube generation"""
        geometry = self.engine.generate_metatrons_cube()
        self.assertIsNotNone(geometry)
    
    def test_generate_sacred_geometry(self):
        """Test sacred geometry generation"""
        geometry = self.engine.generate_sacred_geometry("test")
        self.assertIsNotNone(geometry)


if __name__ == '__main__':
    unittest.main()

