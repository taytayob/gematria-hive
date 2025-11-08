#!/usr/bin/env python3
"""
Populate Semantic Data

Purpose: Populate alphabet mappings and symbol database after migration
- Populate alphabet mappings (Greek, Roman, Hebrew)
- Populate symbol database (Lambda, Pi, Omega, Phi, etc.)

Author: Gematria Hive Team
Date: January 6, 2025
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def populate_alphabet_mappings(supabase) -> Dict:
    """Populate alphabet mappings for Greek, Roman, Hebrew alphabets"""
    print("📝 Populating alphabet mappings...")
    
    # Greek alphabet mappings
    greek_alphabet = {
        'Α': {'name': 'Alpha', 'value': 1, 'roman': 'A'},
        'Β': {'name': 'Beta', 'value': 2, 'roman': 'B'},
        'Γ': {'name': 'Gamma', 'value': 3, 'roman': 'C'},
        'Δ': {'name': 'Delta', 'value': 4, 'roman': 'D'},
        'Ε': {'name': 'Epsilon', 'value': 5, 'roman': 'E'},
        'Ζ': {'name': 'Zeta', 'value': 7, 'roman': 'Z'},
        'Η': {'name': 'Eta', 'value': 8, 'roman': 'H'},
        'Θ': {'name': 'Theta', 'value': 9, 'roman': 'Th'},
        'Ι': {'name': 'Iota', 'value': 10, 'roman': 'I'},
        'Κ': {'name': 'Kappa', 'value': 20, 'roman': 'K'},
        'Λ': {'name': 'Lambda', 'value': 30, 'roman': 'L'},
        'Μ': {'name': 'Mu', 'value': 40, 'roman': 'M'},
        'Ν': {'name': 'Nu', 'value': 50, 'roman': 'N'},
        'Ξ': {'name': 'Xi', 'value': 60, 'roman': 'X'},
        'Ο': {'name': 'Omicron', 'value': 70, 'roman': 'O'},
        'Π': {'name': 'Pi', 'value': 80, 'roman': 'P'},
        'Ρ': {'name': 'Rho', 'value': 100, 'roman': 'R'},
        'Σ': {'name': 'Sigma', 'value': 200, 'roman': 'S'},
        'Τ': {'name': 'Tau', 'value': 300, 'roman': 'T'},
        'Υ': {'name': 'Upsilon', 'value': 400, 'roman': 'U'},
        'Φ': {'name': 'Phi', 'value': 500, 'roman': 'Ph'},
        'Χ': {'name': 'Chi', 'value': 600, 'roman': 'Ch'},
        'Ψ': {'name': 'Psi', 'value': 700, 'roman': 'Ps'},
        'Ω': {'name': 'Omega', 'value': 800, 'roman': 'O'}
    }
    
    # Roman alphabet mappings
    roman_alphabet = {
        'A': {'value': 1, 'greek': 'Α', 'hebrew': 'א'},
        'B': {'value': 2, 'greek': 'Β', 'hebrew': 'ב'},
        'C': {'value': 3, 'greek': 'Γ', 'hebrew': 'ג'},
        'D': {'value': 4, 'greek': 'Δ', 'hebrew': 'ד'},
        'E': {'value': 5, 'greek': 'Ε', 'hebrew': 'ה'},
        'F': {'value': 6, 'greek': None, 'hebrew': None},
        'G': {'value': 7, 'greek': None, 'hebrew': 'ז'},
        'H': {'value': 8, 'greek': 'Η', 'hebrew': 'ח'},
        'I': {'value': 9, 'greek': 'Ι', 'hebrew': 'י'},
        'J': {'value': 10, 'greek': None, 'hebrew': None},
        'K': {'value': 11, 'greek': 'Κ', 'hebrew': 'כ'},
        'L': {'value': 12, 'greek': 'Λ', 'hebrew': 'ל'},
        'M': {'value': 13, 'greek': 'Μ', 'hebrew': 'מ'},
        'N': {'value': 14, 'greek': 'Ν', 'hebrew': 'נ'},
        'O': {'value': 15, 'greek': 'Ο', 'hebrew': None},
        'P': {'value': 16, 'greek': 'Π', 'hebrew': 'פ'},
        'Q': {'value': 17, 'greek': None, 'hebrew': 'ק'},
        'R': {'value': 18, 'greek': 'Ρ', 'hebrew': 'ר'},
        'S': {'value': 19, 'greek': 'Σ', 'hebrew': 'ש'},
        'T': {'value': 20, 'greek': 'Τ', 'hebrew': 'ת'},
        'U': {'value': 21, 'greek': 'Υ', 'hebrew': None},
        'V': {'value': 22, 'greek': None, 'hebrew': None},
        'W': {'value': 23, 'greek': None, 'hebrew': None},
        'X': {'value': 24, 'greek': 'Ξ', 'hebrew': None},
        'Y': {'value': 25, 'greek': None, 'hebrew': None},
        'Z': {'value': 26, 'greek': 'Ζ', 'hebrew': None}
    }
    
    # Hebrew alphabet mappings
    hebrew_alphabet = {
        'א': {'name': 'Aleph', 'value': 1, 'roman': 'A', 'greek': 'Α'},
        'ב': {'name': 'Bet', 'value': 2, 'roman': 'B', 'greek': 'Β'},
        'ג': {'name': 'Gimel', 'value': 3, 'roman': 'G', 'greek': 'Γ'},
        'ד': {'name': 'Dalet', 'value': 4, 'roman': 'D', 'greek': 'Δ'},
        'ה': {'name': 'He', 'value': 5, 'roman': 'E', 'greek': 'Ε'},
        'ו': {'name': 'Vav', 'value': 6, 'roman': 'V', 'greek': None},
        'ז': {'name': 'Zayin', 'value': 7, 'roman': 'Z', 'greek': 'Ζ'},
        'ח': {'name': 'Het', 'value': 8, 'roman': 'H', 'greek': 'Η'},
        'ט': {'name': 'Tet', 'value': 9, 'roman': 'T', 'greek': 'Θ'},
        'י': {'name': 'Yod', 'value': 10, 'roman': 'I', 'greek': 'Ι'},
        'כ': {'name': 'Kaf', 'value': 20, 'roman': 'K', 'greek': 'Κ'},
        'ל': {'name': 'Lamed', 'value': 30, 'roman': 'L', 'greek': 'Λ'},
        'מ': {'name': 'Mem', 'value': 40, 'roman': 'M', 'greek': 'Μ'},
        'נ': {'name': 'Nun', 'value': 50, 'roman': 'N', 'greek': 'Ν'},
        'ס': {'name': 'Samekh', 'value': 60, 'roman': 'S', 'greek': 'Ξ'},
        'ע': {'name': 'Ayin', 'value': 70, 'roman': None, 'greek': 'Ο'},
        'פ': {'name': 'Pe', 'value': 80, 'roman': 'P', 'greek': 'Π'},
        'צ': {'name': 'Tsadi', 'value': 90, 'roman': 'Ts', 'greek': None},
        'ק': {'name': 'Qof', 'value': 100, 'roman': 'Q', 'greek': None},
        'ר': {'name': 'Resh', 'value': 200, 'roman': 'R', 'greek': 'Ρ'},
        'ש': {'name': 'Shin', 'value': 300, 'roman': 'S', 'greek': 'Σ'},
        'ת': {'name': 'Tav', 'value': 400, 'roman': 'T', 'greek': 'Τ'}
    }
    
    results = {
        'greek': 0,
        'roman': 0,
        'hebrew': 0,
        'errors': []
    }
    
    try:
        # Insert Greek alphabet
        for letter, data in greek_alphabet.items():
            try:
                supabase.table('alphabet_mappings').insert({
                    'source_language': 'greek',
                    'source_letter': letter,
                    'target_language': 'roman',
                    'target_letter': data['roman'],
                    'gematria_value': data['value'],
                    'letter_name': data['name'],
                    'metadata': {'greek_name': data['name']}
                }).execute()
                results['greek'] += 1
            except Exception as e:
                results['errors'].append(f"Greek {letter}: {e}")
        
        # Insert Roman alphabet
        for letter, data in roman_alphabet.items():
            try:
                supabase.table('alphabet_mappings').insert({
                    'source_language': 'roman',
                    'source_letter': letter,
                    'target_language': 'greek',
                    'target_letter': data.get('greek'),
                    'gematria_value': data['value'],
                    'metadata': {'roman_value': data['value']}
                }).execute()
                results['roman'] += 1
            except Exception as e:
                results['errors'].append(f"Roman {letter}: {e}")
        
        # Insert Hebrew alphabet
        for letter, data in hebrew_alphabet.items():
            try:
                supabase.table('alphabet_mappings').insert({
                    'source_language': 'hebrew',
                    'source_letter': letter,
                    'target_language': 'roman',
                    'target_letter': data.get('roman'),
                    'gematria_value': data['value'],
                    'letter_name': data['name'],
                    'metadata': {'hebrew_name': data['name']}
                }).execute()
                results['hebrew'] += 1
            except Exception as e:
                results['errors'].append(f"Hebrew {letter}: {e}")
        
        print(f"✅ Alphabet mappings populated:")
        print(f"   Greek: {results['greek']} letters")
        print(f"   Roman: {results['roman']} letters")
        print(f"   Hebrew: {results['hebrew']} letters")
        
        if results['errors']:
            print(f"⚠️  Errors: {len(results['errors'])}")
            for error in results['errors'][:5]:
                print(f"   {error}")
        
    except Exception as e:
        print(f"❌ Error populating alphabet mappings: {e}")
        results['errors'].append(str(e))
    
    return results

def populate_symbols(supabase) -> Dict:
    """Populate symbols and sacred geometry database"""
    print("📝 Populating symbols database...")
    
    symbols = {
        'λ': {
            'symbol': 'λ',
            'name': 'Lambda',
            'type': 'greek_letter',
            'gematria_value': 30,
            'physics_value': 'wavelength',
            'description': 'Greek letter Lambda, represents wavelength in physics',
            'sacred_geometry': 'Golden ratio connection',
            'esoteric_meaning': 'Transformation, change'
        },
        'π': {
            'symbol': 'π',
            'name': 'Pi',
            'type': 'greek_letter',
            'gematria_value': 80,
            'physics_value': 3.14159,
            'description': 'Mathematical constant Pi, ratio of circle circumference to diameter',
            'sacred_geometry': 'Circle, perfection, infinity',
            'esoteric_meaning': 'Divine proportion, eternal cycles'
        },
        'Ω': {
            'symbol': 'Ω',
            'name': 'Omega',
            'type': 'greek_letter',
            'gematria_value': 800,
            'physics_value': 'ohms (resistance)',
            'description': 'Greek letter Omega, represents resistance in physics',
            'sacred_geometry': 'Completion, finality',
            'esoteric_meaning': 'End, completion, ultimate truth'
        },
        'φ': {
            'symbol': 'φ',
            'name': 'Phi',
            'type': 'greek_letter',
            'gematria_value': 500,
            'physics_value': 1.618,
            'description': 'Golden ratio Phi, divine proportion',
            'sacred_geometry': 'Golden ratio, Fibonacci sequence',
            'esoteric_meaning': 'Divine proportion, beauty, harmony'
        },
        '∞': {
            'symbol': '∞',
            'name': 'Infinity',
            'type': 'mathematical',
            'gematria_value': None,
            'physics_value': 'infinity',
            'description': 'Mathematical symbol for infinity',
            'sacred_geometry': 'Eternal, boundless',
            'esoteric_meaning': 'Eternity, infinite potential'
        },
        '∑': {
            'symbol': '∑',
            'name': 'Sigma (Summation)',
            'type': 'mathematical',
            'gematria_value': 200,
            'physics_value': 'summation',
            'description': 'Mathematical symbol for summation',
            'sacred_geometry': 'Accumulation, totality',
            'esoteric_meaning': 'Unity, completeness'
        },
        '√': {
            'symbol': '√',
            'name': 'Square Root',
            'type': 'mathematical',
            'gematria_value': None,
            'physics_value': 'square root',
            'description': 'Mathematical symbol for square root',
            'sacred_geometry': 'Foundation, root',
            'esoteric_meaning': 'Origin, source, foundation'
        }
    }
    
    results = {
        'inserted': 0,
        'errors': []
    }
    
    try:
        for symbol_key, data in symbols.items():
            try:
                supabase.table('symbols_sacred_geometry').insert({
                    'symbol': data['symbol'],
                    'symbol_name': data['name'],
                    'symbol_type': data['type'],
                    'gematria_value': data.get('gematria_value'),
                    'physics_value': str(data.get('physics_value', '')),
                    'description': data['description'],
                    'sacred_geometry_meaning': data.get('sacred_geometry', ''),
                    'esoteric_meaning': data.get('esoteric_meaning', ''),
                    'metadata': {
                        'type': data['type'],
                        'physics_value': data.get('physics_value')
                    }
                }).execute()
                results['inserted'] += 1
            except Exception as e:
                results['errors'].append(f"{data['name']}: {e}")
        
        print(f"✅ Symbols populated: {results['inserted']} symbols")
        
        if results['errors']:
            print(f"⚠️  Errors: {len(results['errors'])}")
            for error in results['errors'][:5]:
                print(f"   {error}")
        
    except Exception as e:
        print(f"❌ Error populating symbols: {e}")
        results['errors'].append(str(e))
    
    return results

def main():
    """Main function"""
    print("=" * 60)
    print("Populate Semantic Data")
    print("=" * 60)
    print()
    
    # Check Supabase connection
    try:
        from supabase import create_client
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        
        if not url or not key:
            print("❌ SUPABASE_URL or SUPABASE_KEY not set")
            return
        
        supabase = create_client(url, key)
        
        # Test connection
        result = supabase.table('gematria_words').select('*').limit(1).execute()
        print("✅ Supabase connection verified")
        print()
        
        # Check if semantic layers tables exist
        try:
            supabase.table('alphabet_mappings').select('*').limit(1).execute()
            print("✅ Semantic layers tables exist")
        except Exception as e:
            print("❌ Semantic layers tables not found")
            print("   Please run migration first: python apply_semantic_migration.py")
            return
        
        print()
        print("=" * 60)
        print("Populating Data")
        print("=" * 60)
        print()
        
        # Populate alphabet mappings
        alphabet_results = populate_alphabet_mappings(supabase)
        print()
        
        # Populate symbols
        symbol_results = populate_symbols(supabase)
        print()
        
        print("=" * 60)
        print("✅ Population Complete")
        print("=" * 60)
        print()
        print(f"📊 Alphabet Mappings: {alphabet_results['greek'] + alphabet_results['roman'] + alphabet_results['hebrew']} total")
        print(f"📊 Symbols: {symbol_results['inserted']} total")
        
        if alphabet_results['errors'] or symbol_results['errors']:
            print()
            print("⚠️  Some errors occurred - check output above")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

