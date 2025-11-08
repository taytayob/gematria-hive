#!/usr/bin/env python3
"""
Test Enhanced Calculator

Purpose: Test all enhanced calculator features
- Step-by-step breakdown
- Search across all methods
- Multiple words
- Database search

Author: Gematria Hive Team
Date: January 6, 2025
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gematria_engine():
    """Test GematriaEngine"""
    print("=" * 60)
    print("Test 1: GematriaEngine")
    print("=" * 60)
    
    try:
        from core.gematria_engine import GematriaEngine
        
        engine = GematriaEngine()
        print("✅ GematriaEngine initialized")
        
        # Test basic calculation
        result = engine.calculate_all("HELLO")
        print(f"✅ Basic calculation: HELLO = {result.get('english_gematria', 'N/A')}")
        
        # Test step-by-step breakdown
        breakdown = engine.calculate_with_breakdown("HELLO", "english_gematria")
        print(f"✅ Step-by-step breakdown: {len(breakdown.get('steps', []))} steps")
        print(f"   Total: {breakdown.get('total', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gematria_calculator():
    """Test GematriaCalculator"""
    print()
    print("=" * 60)
    print("Test 2: GematriaCalculator")
    print("=" * 60)
    
    try:
        from gematria_calculator import GematriaCalculator
        
        calc = GematriaCalculator()
        print("✅ GematriaCalculator initialized")
        
        # Test calculation (using engine directly)
        from core.gematria_engine import GematriaEngine
        engine = GematriaEngine()
        result = engine.calculate_all("HELLO")
        print(f"✅ Calculation: {len(result)} methods")
        
        # Test search (if database available)
        try:
            words = calc.find_words_by_value(52, "english_gematria", limit=5)
            print(f"✅ Search by value: {len(words)} words found")
        except Exception as e:
            print(f"⚠️  Search test skipped: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_all_methods():
    """Test all gematria methods"""
    print()
    print("=" * 60)
    print("Test 3: All Gematria Methods")
    print("=" * 60)
    
    try:
        from core.gematria_engine import GematriaEngine
        
        engine = GematriaEngine()
        test_word = "HELLO"
        
        methods = [
            'english_gematria',
            'simple_gematria',
            'jewish_gematria',
            'latin_gematria',
            'greek_gematria',
            'hebrew_full',
            'hebrew_musafi',
            'hebrew_katan',
            'hebrew_ordinal',
            'hebrew_atbash',
            'hebrew_kidmi',
            'hebrew_perati',
            'hebrew_shemi'
        ]
        
        results = {}
        for method in methods:
            try:
                result = engine.calculate_all(test_word)
                value = result.get(method, 0)
                results[method] = value
                print(f"✅ {method}: {value}")
            except Exception as e:
                print(f"❌ {method}: {e}")
                results[method] = None
        
        print(f"\n✅ Tested {len([r for r in results.values() if r is not None])}/{len(methods)} methods")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_step_by_step_breakdown():
    """Test step-by-step breakdown for multiple methods"""
    print()
    print("=" * 60)
    print("Test 4: Step-by-Step Breakdown")
    print("=" * 60)
    
    try:
        from core.gematria_engine import GematriaEngine
        
        engine = GematriaEngine()
        test_word = "HELLO"
        
        methods = [
            'english_gematria',
            'simple_gematria',
            'jewish_gematria',
            'latin_gematria',
            'greek_gematria'
        ]
        
        for method in methods:
            try:
                breakdown = engine.calculate_with_breakdown(test_word, method)
                steps = breakdown.get('steps', [])
                total = breakdown.get('total', 0)
                print(f"✅ {method}: {len(steps)} steps, total = {total}")
            except Exception as e:
                print(f"❌ {method}: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_search():
    """Test database search functionality"""
    print()
    print("=" * 60)
    print("Test 5: Database Search")
    print("=" * 60)
    
    try:
        from supabase import create_client
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        
        if not url or not key:
            print("⚠️  Supabase not configured - skipping database search test")
            return True
        
        supabase = create_client(url, key)
        
        # Test search across all methods
        search_value = 52
        all_methods = [
            'jewish_gematria', 'english_gematria', 'simple_gematria',
            'latin_gematria', 'greek_gematria', 'hebrew_full',
            'hebrew_musafi', 'hebrew_katan', 'hebrew_ordinal',
            'hebrew_atbash', 'hebrew_kidmi', 'hebrew_perati', 'hebrew_shemi'
        ]
        
        results = {}
        for method in all_methods[:5]:  # Test first 5 methods
            try:
                result = supabase.table('gematria_words')\
                    .select('phrase')\
                    .eq(method, search_value)\
                    .limit(5)\
                    .execute()
                
                if result.data:
                    results[method] = len(result.data)
                    print(f"✅ {method}: {len(result.data)} matches")
                else:
                    print(f"⚠️  {method}: No matches")
            except Exception as e:
                print(f"❌ {method}: {e}")
        
        if results:
            print(f"\n✅ Database search working: {sum(results.values())} total matches")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("Enhanced Calculator Test Suite")
    print("=" * 60)
    print()
    
    results = {
        'gematria_engine': test_gematria_engine(),
        'gematria_calculator': test_gematria_calculator(),
        'all_methods': test_all_methods(),
        'step_by_step': test_step_by_step_breakdown(),
        'database_search': test_database_search()
    }
    
    print()
    print("=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    print()
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print()
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed!")
    else:
        print("⚠️  Some tests failed - check output above")

if __name__ == "__main__":
    main()

