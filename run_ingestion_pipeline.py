#!/usr/bin/env python3
"""
Coordinated Ingestion Pipeline

Purpose: Pull data from all sources and ingest with validation
- CSV files (gematrix789.csv, gimatria789.csv)
- Database sources
- Web scraping
- Bookmarks
- Coordinate with gematria calculator for validation

Author: Gematria Hive Team
Date: January 6, 2025
"""

import sys
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import json
import concurrent.futures

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('ingestion_pipeline.log')
    ]
)
logger = logging.getLogger(__name__)


def validate_gematria_calculations(phrase: str, csv_values: Dict, engine) -> Dict:
    """
    Validate CSV values against our calculation engine.
    
    Args:
        phrase: Text/phrase to validate
        csv_values: Dictionary with CSV values
        engine: GematriaEngine instance
        
    Returns:
        Dictionary with validation results
    """
    validation_results = {
        'phrase': phrase,
        'valid': True,
        'mismatches': [],
        'matches': []
    }
    
    # Calculate using our engine
    calculated = engine.calculate_all(phrase)
    
    # Compare with CSV values
    comparisons = {
        'english_gematria': csv_values.get('english_gematria'),
        'simple_gematria': csv_values.get('simple_gematria'),
        'jewish_gematria': csv_values.get('jewish_gematria'),
        'hebrew_full': csv_values.get('hebrew_full'),
        'hebrew_musafi': csv_values.get('hebrew_musafi'),
        'hebrew_katan': csv_values.get('hebrew_katan'),
        'hebrew_ordinal': csv_values.get('hebrew_ordinal'),
        'hebrew_atbash': csv_values.get('hebrew_atbash'),
        'hebrew_kidmi': csv_values.get('hebrew_kidmi'),
        'hebrew_perati': csv_values.get('hebrew_perati'),
        'hebrew_shemi': csv_values.get('hebrew_shemi'),
    }
    
    for method, csv_value in comparisons.items():
        if csv_value is not None:
            calculated_value = calculated.get(method, 0)
            if calculated_value == csv_value:
                validation_results['matches'].append(method)
            else:
                validation_results['valid'] = False
                validation_results['mismatches'].append({
                    'method': method,
                    'csv_value': csv_value,
                    'calculated_value': calculated_value,
                    'difference': abs(csv_value - calculated_value)
                })
    
    return validation_results


def ingest_csv_with_validation(file_path: str, validate: bool = True, 
                               max_rows: Optional[int] = None) -> Dict:
    """
    Ingest CSV file with validation against calculation engine.
    
    Args:
        file_path: Path to CSV file
        validate: Whether to validate calculations
        max_rows: Maximum rows to process (None for all)
        
    Returns:
        Dictionary with ingestion results
    """
    logger.info(f"📄 Starting CSV ingestion: {file_path}")
    
    try:
        from ingest_csv import ingest_csv_file, detect_csv_format
        from core.gematria_engine import get_gematria_engine
        
        # Initialize calculation engine for validation
        engine = get_gematria_engine() if validate else None
        
        # Detect format
        csv_format = detect_csv_format(file_path)
        logger.info(f"   Format detected: {csv_format}")
        
        # Ingest CSV file
        results = ingest_csv_file(
            file_path=file_path,
            chunk_size=10000,
            max_rows=max_rows,
            checkpoint_interval=50000,
            validate=validate
        )
        
        if results.get('success'):
            ingested = results.get('total_ingested', 0)
            processed = results.get('total_processed', 0)
            logger.info(f"   ✅ Ingested: {ingested}/{processed} rows")
            
            # Add validation summary if enabled
            if validate and engine:
                logger.info(f"   ✅ Validation: Enabled (using calculation engine)")
        else:
            error = results.get('error', 'Unknown error')
            logger.error(f"   ❌ Ingestion failed: {error}")
        
        return results
        
    except Exception as e:
        logger.error(f"   ❌ Error ingesting CSV: {e}")
        return {'success': False, 'error': str(e)}


def ingest_all_csv_files(validate: bool = True, max_rows: Optional[int] = None) -> Dict:
    """
    Find and ingest all CSV files in the project.
    Prioritizes purchased files over sample/scraped files.
    
    Args:
        validate: Whether to validate calculations
        max_rows: Maximum rows per file (None for all)
        
    Returns:
        Dictionary with results for each file
    """
    logger.info("=" * 60)
    logger.info("CSV FILES INGESTION")
    logger.info("=" * 60)
    
    # Find CSV files - prioritize purchased files
    purchased_files = []
    other_files = []
    sample_files = ['gematrix789.csv', 'gimatria789.csv']  # Small sample files to exclude
    
    # Look for purchased files first (priority)
    purchased_patterns = [
        'purchased-gematrix789.csv',
        'purchased-gimatria789.csv'
    ]
    
    for pattern in purchased_patterns:
        if Path(pattern).exists():
            purchased_files.append(Path(pattern))
            logger.info(f"✅ Found purchased file: {pattern}")
    
    # Look for other CSV files (excluding samples)
    all_csv_files = list(Path('.').glob('*.csv'))
    for csv_file in all_csv_files:
        csv_name = csv_file.name
        # Skip sample files and already-added purchased files
        if csv_name not in sample_files and csv_file not in purchased_files:
            other_files.append(csv_file)
    
    # Combine: purchased first, then others
    csv_files = purchased_files + other_files
    
    if not csv_files:
        logger.warning("⚠️  No CSV files found")
        return {'files_found': 0, 'results': {}}
    
    logger.info(f"📋 Found {len(csv_files)} CSV file(s) to process")
    logger.info("   Priority order: Purchased files first, then others")
    for csv_file in csv_files:
        file_size = csv_file.stat().st_size / (1024 * 1024)  # MB
        logger.info(f"   - {csv_file} ({file_size:.1f} MB)")
    
    if sample_files:
        logger.info(f"   ⚠️  Excluding sample files: {', '.join(sample_files)}")
    
    # Ingest all CSV files
    results = {}
    for csv_file in csv_files:
        file_results = ingest_csv_with_validation(
            str(csv_file),
            validate=validate,
            max_rows=max_rows
        )
        results[str(csv_file)] = file_results
    
    # Summary
    total_ingested = sum(r.get('total_ingested', 0) for r in results.values())
    total_processed = sum(r.get('total_processed', 0) for r in results.values())
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("CSV INGESTION SUMMARY")
    logger.info("=" * 60)
    logger.info(f"📊 Files processed: {len(results)}")
    logger.info(f"📊 Total ingested: {total_ingested}")
    logger.info(f"📊 Total processed: {total_processed}")
    logger.info("")
    
    return {
        'files_found': len(csv_files),
        'total_ingested': total_ingested,
        'total_processed': total_processed,
        'results': results
    }


def pull_from_database() -> Dict:
    """Pull data from database tables"""
    logger.info("=" * 60)
    logger.info("DATABASE PULL")
    logger.info("=" * 60)
    
    try:
        from supabase import create_client
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            logger.warning("⚠️  Supabase credentials not configured - skipping database pull")
            return {'success': False, 'error': 'Not configured'}
        
        supabase = create_client(supabase_url, supabase_key)
        
        # Pull from gematria_words table
        try:
            result = supabase.table('gematria_words')\
                .select('*', count='exact')\
                .limit(1000)\
                .execute()
            
            count = result.count if hasattr(result, 'count') else len(result.data or [])
            data = result.data or []
            
            logger.info(f"✅ Pulled {len(data)} items from gematria_words (total: {count})")
            
            return {
                'success': True,
                'count': count,
                'items': len(data),
                'data': data
            }
        except Exception as e:
            logger.error(f"❌ Error pulling from database: {e}")
            return {'success': False, 'error': str(e)}
            
    except Exception as e:
        logger.error(f"❌ Error connecting to database: {e}")
        return {'success': False, 'error': str(e)}


def scrape_websites() -> Dict:
    """Scrape gematria-related websites"""
    logger.info("=" * 60)
    logger.info("WEB SCRAPING")
    logger.info("=" * 60)
    
    try:
        from agents.browser import BrowserAgent
        
        browser = BrowserAgent()
        
        urls = [
            "https://www.gematrix.org",
        ]
        
        scraped_data = []
        for url in urls:
            try:
                state = {
                    "task": {"url": url, "max_depth": 1, "delay": 2.0},
                    "data": [],
                    "context": {},
                    "results": [],
                    "cost": 0.0,
                    "status": "pending",
                    "memory_id": None
                }
                result_state = browser.execute(state)
                if result_state.get("data"):
                    scraped_data.extend(result_state["data"])
                    logger.info(f"✅ Scraped {len(result_state['data'])} pages from {url}")
            except Exception as e:
                logger.warning(f"⚠️  Error scraping {url}: {e}")
        
        logger.info(f"✅ Total scraped: {len(scraped_data)} pages")
        return {'success': True, 'items': len(scraped_data), 'data': scraped_data}
        
    except Exception as e:
        logger.error(f"❌ Error scraping websites: {e}")
        return {'success': False, 'error': str(e)}


def process_bookmarks() -> Dict:
    """Process bookmark files"""
    logger.info("=" * 60)
    logger.info("BOOKMARK PROCESSING")
    logger.info("=" * 60)
    
    try:
        from agents.bookmark_ingestion import BookmarkIngestionAgent
        
        bookmark_agent = BookmarkIngestionAgent()
        
        # Find bookmark files
        bookmark_files = []
        bookmark_files.extend(Path('.').glob('*.json'))
        bookmark_files.extend(Path('.').glob('*.md'))
        
        if not bookmark_files:
            logger.info("ℹ️  No bookmark files found")
            return {'success': True, 'items': 0, 'data': []}
        
        all_bookmarks = []
        for bookmark_file in bookmark_files:
            try:
                state = {
                    "task": {"source": str(bookmark_file), "type": "bookmark_ingestion"},
                    "data": [],
                    "context": {},
                    "results": [],
                    "cost": 0.0,
                    "status": "pending",
                    "memory_id": None
                }
                result_state = bookmark_agent.execute(state)
                if result_state.get("data"):
                    all_bookmarks.extend(result_state["data"])
                    logger.info(f"✅ Processed {len(result_state['data'])} bookmarks from {bookmark_file}")
            except Exception as e:
                logger.warning(f"⚠️  Error processing {bookmark_file}: {e}")
        
        logger.info(f"✅ Total bookmarks processed: {len(all_bookmarks)}")
        return {'success': True, 'items': len(all_bookmarks), 'data': all_bookmarks}
        
    except Exception as e:
        logger.error(f"❌ Error processing bookmarks: {e}")
        return {'success': False, 'error': str(e)}


def run_full_pipeline(validate: bool = True, max_rows: Optional[int] = None,
                     sources: Optional[List[str]] = None) -> Dict:
    """
    Run full ingestion pipeline from all sources.
    
    Args:
        validate: Whether to validate calculations against engine
        max_rows: Maximum rows per CSV file (None for all)
        sources: List of sources to process (None for all)
                 Options: 'csv', 'database', 'websites', 'bookmarks'
        
    Returns:
        Dictionary with complete pipeline results
    """
    logger.info("=" * 60)
    logger.info("GEMATRIA HIVE - FULL INGESTION PIPELINE")
    logger.info("=" * 60)
    logger.info(f"⏰ Started: {datetime.now().isoformat()}")
    logger.info(f"✅ Validation: {'Enabled' if validate else 'Disabled'}")
    logger.info("")
    
    start_time = datetime.now()
    
    # Default to all sources if not specified
    if sources is None:
        sources = ['csv', 'database', 'websites', 'bookmarks']
    
    results = {}
    
    # Run all sources concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(sources)) as executor:
        futures = {}
        
        if 'csv' in sources:
            futures[executor.submit(ingest_all_csv_files, validate, max_rows)] = 'csv'
        
        if 'database' in sources:
            futures[executor.submit(pull_from_database)] = 'database'
        
        if 'websites' in sources:
            futures[executor.submit(scrape_websites)] = 'websites'
        
        if 'bookmarks' in sources:
            futures[executor.submit(process_bookmarks)] = 'bookmarks'
        
        # Collect results
        for future in concurrent.futures.as_completed(futures):
            source = futures[future]
            try:
                result = future.result()
                results[source] = result
                logger.info(f"✅ {source} completed")
            except Exception as e:
                logger.error(f"❌ {source} failed: {e}")
                results[source] = {'success': False, 'error': str(e)}
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Final summary
    logger.info("")
    logger.info("=" * 60)
    logger.info("PIPELINE SUMMARY")
    logger.info("=" * 60)
    logger.info(f"⏱️  Duration: {duration:.2f} seconds")
    logger.info(f"📊 Sources processed: {len(results)}")
    
    # CSV summary
    if 'csv' in results:
        csv_result = results['csv']
        logger.info(f"📄 CSV files: {csv_result.get('files_found', 0)} files")
        logger.info(f"   Ingested: {csv_result.get('total_ingested', 0)} rows")
        logger.info(f"   Processed: {csv_result.get('total_processed', 0)} rows")
    
    # Database summary
    if 'database' in results:
        db_result = results['database']
        if db_result.get('success'):
            logger.info(f"📊 Database: {db_result.get('count', 0)} total records")
            logger.info(f"   Pulled: {db_result.get('items', 0)} items")
    
    # Websites summary
    if 'websites' in results:
        web_result = results['websites']
        if web_result.get('success'):
            logger.info(f"🌐 Websites: {web_result.get('items', 0)} pages scraped")
    
    # Bookmarks summary
    if 'bookmarks' in results:
        bookmark_result = results['bookmarks']
        if bookmark_result.get('success'):
            logger.info(f"🔖 Bookmarks: {bookmark_result.get('items', 0)} bookmarks processed")
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("✅ PIPELINE COMPLETE!")
    logger.info("=" * 60)
    
    return {
        'success': True,
        'duration': duration,
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'sources': results,
        'validation_enabled': validate
    }


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run Gematria Hive Ingestion Pipeline')
    parser.add_argument('--sources', nargs='+', 
                       choices=['csv', 'database', 'websites', 'bookmarks'],
                       default=None,
                       help='Sources to process (default: all)')
    parser.add_argument('--no-validate', action='store_true',
                       help='Disable calculation validation')
    parser.add_argument('--max-rows', type=int, default=None,
                       help='Maximum rows per CSV file (default: all)')
    parser.add_argument('--csv-only', action='store_true',
                       help='Only process CSV files')
    
    args = parser.parse_args()
    
    # Determine sources
    if args.csv_only:
        sources = ['csv']
    elif args.sources:
        sources = args.sources
    else:
        sources = None  # All sources
    
    # Run pipeline
    results = run_full_pipeline(
        validate=not args.no_validate,
        max_rows=args.max_rows,
        sources=sources
    )
    
    # Save results
    results_file = f"ingestion_pipeline_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        logger.info(f"📄 Results saved to: {results_file}")
    except Exception as e:
        logger.warning(f"⚠️  Could not save results: {e}")
    
    return 0 if results.get('success') else 1


if __name__ == "__main__":
    sys.exit(main())

