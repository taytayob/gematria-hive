#!/usr/bin/env python3
"""
Create Sample CSV Files for Testing

Purpose: Create sample CSV files in gematrix789 and gimatria789 formats
for testing the ingestion pipeline.

Author: Gematria Hive Team
Date: January 6, 2025
"""

import csv
import os
from pathlib import Path
from core.gematria_engine import get_gematria_engine

def create_sample_gematrix789_csv(file_path: str = 'gematrix789_sample.csv', num_rows: int = 100):
    """
    Create sample gematrix789.csv format file.
    
    Format: phrase, jewish gematria, english gematria, simple gematria, search num
    """
    engine = get_gematria_engine()
    
    # Sample phrases for testing
    sample_phrases = [
        "LOVE", "HELLO", "WORLD", "PEACE", "HARMONY", "UNITY", "TRUTH", "WISDOM",
        "KNOWLEDGE", "UNDERSTANDING", "COMPASSION", "GRATITUDE", "JOY", "HAPPINESS",
        "FREEDOM", "LIBERTY", "JUSTICE", "EQUITY", "BALANCE", "HARMONY", "BEAUTY",
        "CREATIVITY", "INSPIRATION", "MOTIVATION", "DETERMINATION", "PERSEVERANCE",
        "COURAGE", "BRAVERY", "STRENGTH", "POWER", "ENERGY", "FORCE", "MOMENTUM",
        "VELOCITY", "SPEED", "ACCELERATION", "MOTION", "MOVEMENT", "CHANGE",
        "TRANSFORMATION", "EVOLUTION", "GROWTH", "DEVELOPMENT", "PROGRESS",
        "ADVANCEMENT", "IMPROVEMENT", "ENHANCEMENT", "OPTIMIZATION", "EFFICIENCY",
        "PRODUCTIVITY", "PERFORMANCE", "EXCELLENCE", "QUALITY", "STANDARD",
        "BENCHMARK", "METRIC", "MEASUREMENT", "QUANTIFICATION", "ANALYSIS",
        "EVALUATION", "ASSESSMENT", "REVIEW", "EXAMINATION", "INVESTIGATION",
        "RESEARCH", "STUDY", "LEARNING", "EDUCATION", "TRAINING", "DEVELOPMENT",
        "PRACTICE", "EXERCISE", "REPETITION", "ITERATION", "REFINEMENT",
        "PERFECTION", "MASTERY", "EXPERTISE", "PROFICIENCY", "COMPETENCE",
        "SKILL", "ABILITY", "CAPACITY", "POTENTIAL", "POSSIBILITY", "OPPORTUNITY",
        "CHANCE", "PROBABILITY", "LIKELIHOOD", "CERTAINTY", "CONFIDENCE", "TRUST",
        "FAITH", "BELIEF", "CONVICTION", "ASSURANCE", "GUARANTEE", "PROMISE",
        "COMMITMENT", "DEDICATION", "DEVOTION", "LOYALTY", "ALLEGIANCE", "FIDELITY"
    ]
    
    # Extend list if needed
    while len(sample_phrases) < num_rows:
        sample_phrases.extend(sample_phrases[:num_rows - len(sample_phrases)])
    
    sample_phrases = sample_phrases[:num_rows]
    
    # Create CSV file
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow(['phrase', 'jewish gematria', 'english gematria', 'simple gematria', 'search num'])
        
        # Write data rows
        for phrase in sample_phrases:
            # Calculate values using engine
            results = engine.calculate_all(phrase)
            
            writer.writerow([
                phrase,
                results.get('jewish_gematria', 0),
                results.get('english_gematria', 0),
                results.get('simple_gematria', 0),
                results.get('search_num', 0)
            ])
    
    print(f"✅ Created {file_path} with {num_rows} rows")
    return file_path


def create_sample_gimatria789_csv(file_path: str = 'gimatria789_sample.csv', num_rows: int = 50):
    """
    Create sample gimatria789.csv format file.
    
    Format: text, g_full, g_musafi, g_katan, g_ordinal, g_atbash, g_kidmi, g_perati, g_shemi, searchnum
    """
    engine = get_gematria_engine()
    
    # Sample Hebrew phrases for testing
    sample_phrases = [
        "א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט", "י",
        "כ", "ל", "מ", "נ", "ס", "ע", "פ", "צ", "ק", "ר",
        "ש", "ת", "אב", "אג", "אד", "אה", "או", "אז", "אח", "אט",
        "אי", "אכ", "אל", "אמ", "אנ", "אס", "אע", "אפ", "אצ", "אק",
        "אר", "אש", "את", "בג", "בד", "בה", "בו", "בז", "בח", "בט"
    ]
    
    # Extend list if needed
    while len(sample_phrases) < num_rows:
        sample_phrases.extend(sample_phrases[:num_rows - len(sample_phrases)])
    
    sample_phrases = sample_phrases[:num_rows]
    
    # Create CSV file
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow(['text', 'g_full', 'g_musafi', 'g_katan', 'g_ordinal', 
                        'g_atbash', 'g_kidmi', 'g_perati', 'g_shemi', 'searchnum'])
        
        # Write data rows
        for phrase in sample_phrases:
            # Calculate values using engine
            results = engine.calculate_all(phrase)
            
            writer.writerow([
                phrase,
                results.get('hebrew_full', 0),
                results.get('hebrew_musafi', 0),
                results.get('hebrew_katan', 0),
                results.get('hebrew_ordinal', 0),
                results.get('hebrew_atbash', 0),
                results.get('hebrew_kidmi', 0),
                results.get('hebrew_perati', 0),
                results.get('hebrew_shemi', 0),
                results.get('search_num', 0)
            ])
    
    print(f"✅ Created {file_path} with {num_rows} rows")
    return file_path


def main():
    """Create sample CSV files"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Create sample CSV files for testing')
    parser.add_argument('--gematrix-rows', type=int, default=100,
                       help='Number of rows for gematrix789.csv (default: 100)')
    parser.add_argument('--gimatria-rows', type=int, default=50,
                       help='Number of rows for gimatria789.csv (default: 50)')
    parser.add_argument('--output-dir', type=str, default='.',
                       help='Output directory (default: current directory)')
    
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample files
    gematrix_file = output_dir / 'gematrix789_sample.csv'
    gimatria_file = output_dir / 'gimatria789_sample.csv'
    
    print("=" * 60)
    print("Creating Sample CSV Files")
    print("=" * 60)
    print()
    
    # Create gematrix789 sample
    create_sample_gematrix789_csv(str(gematrix_file), args.gematrix_rows)
    
    # Create gimatria789 sample
    create_sample_gimatria789_csv(str(gimatria_file), args.gimatria_rows)
    
    print()
    print("=" * 60)
    print("✅ Sample CSV Files Created!")
    print("=" * 60)
    print(f"📄 {gematrix_file}")
    print(f"📄 {gimatria_file}")
    print()
    print("You can now run the ingestion pipeline:")
    print("  python run_ingestion_pipeline.py --csv-only")


if __name__ == "__main__":
    main()

