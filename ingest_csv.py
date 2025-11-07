"""
CSV Ingestion Module for Gematria Database

Purpose: Ingest large CSV files containing gematria calculations
- gematrix789.csv: phrase, jewish_gematria, english_gematria, simple_gematria, search_num
- gimatria789.csv: Hebrew gematria variants with multiple calculation methods

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd
from tqdm import tqdm

# Core dependencies
from supabase import create_client, Client
from sentence_transformers import SentenceTransformer

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Logging setup (must be before Supabase check to use logger)
logging.basicConfig(
    filename='ingestion_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)
logger = logging.getLogger()
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

# Environment variables
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Make Supabase optional for imports - fail gracefully at runtime
HAS_SUPABASE = bool(SUPABASE_URL and SUPABASE_KEY)
if not HAS_SUPABASE:
    logger.warning("SUPABASE_URL and SUPABASE_KEY not set - database operations will be disabled")

# Supabase client
supabase: Optional[Client] = None
if HAS_SUPABASE:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    logger.warning("Supabase client not initialized - set SUPABASE_URL and SUPABASE_KEY to enable")

# Embedding model for semantic search
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

logger.info("CSV Ingestion Module initialized")


def detect_csv_format(file_path: str) -> str:
    """
    Detect CSV format by examining headers.
    
    Args:
        file_path: Path to CSV file
        
    Returns:
        Format type: 'gematrix789' or 'gimatria789'
    """
    try:
        # Read first row to check headers
        df_sample = pd.read_csv(file_path, nrows=1)
        headers = [col.lower().strip() for col in df_sample.columns]
        
        if 'phrase' in headers and 'jewish gematria' in headers:
            return 'gematrix789'
        elif 'g_full' in headers or 'gematria' in headers:
            return 'gimatria789'
        else:
            logger.warning(f"Unknown CSV format for {file_path}, defaulting to gematrix789")
            return 'gematrix789'
    except Exception as e:
        logger.error(f"Error detecting CSV format: {e}")
        return 'gematrix789'


def process_gematrix789_row(row: pd.Series) -> Dict:
    """
    Process a row from gematrix789.csv format.
    
    Args:
        row: pandas Series with columns: phrase, jewish_gematria, english_gematria, simple_gematria, search_num
        
    Returns:
        Dictionary ready for database insertion
    """
    phrase = str(row.get('phrase', '')).strip()
    if not phrase:
        return None
    
    # Convert numeric values, handling NaN
    def safe_int(value):
        try:
            if pd.isna(value):
                return None
            return int(float(value))
        except (ValueError, TypeError):
            return None
    
    return {
        'phrase': phrase,
        'jewish_gematria': safe_int(row.get('jewish gematria')),
        'english_gematria': safe_int(row.get('english gematria')),
        'simple_gematria': safe_int(row.get('simple gematria')),
        'search_num': safe_int(row.get('search num')),
        'source': 'gematrix789'
    }


def process_gimatria789_row(row: pd.Series) -> Dict:
    """
    Process a row from gimatria789.csv format.
    
    Args:
        row: pandas Series with Hebrew gematria columns
        
    Returns:
        Dictionary ready for database insertion
    """
    # Get phrase from 'text' column (Hebrew text)
    phrase = str(row.get('text', '')).strip()
    if not phrase:
        return None
    
    # Convert numeric values, handling NaN
    def safe_int(value):
        try:
            if pd.isna(value):
                return None
            return int(float(value))
        except (ValueError, TypeError):
            return None
    
    return {
        'phrase': phrase,
        'hebrew_full': safe_int(row.get('g_full')),
        'hebrew_musafi': safe_int(row.get('g_musafi')),
        'hebrew_katan': safe_int(row.get('g_katan')),
        'hebrew_ordinal': safe_int(row.get('g_ordinal')),
        'hebrew_atbash': safe_int(row.get('g_atbash')),
        'hebrew_kidmi': safe_int(row.get('g_kidmi')),
        'hebrew_perati': safe_int(row.get('g_perati')),
        'hebrew_shemi': safe_int(row.get('g_shemi')),
        'search_num': safe_int(row.get('searchnum')),
        'source': 'gimatria789'
    }


def generate_embeddings(phrases: List[str], batch_size: int = 100) -> List[List[float]]:
    """
    Generate embeddings for phrases in batches.
    
    Args:
        phrases: List of phrases to embed
        batch_size: Number of phrases to process per batch
        
    Returns:
        List of embedding vectors
    """
    embeddings = []
    for i in range(0, len(phrases), batch_size):
        batch = phrases[i:i+batch_size]
        batch_embeddings = embed_model.encode(batch, show_progress_bar=False)
        embeddings.extend(batch_embeddings.tolist())
    return embeddings


def ingest_csv_chunk(chunk: List[Dict], source: str, validate: bool = True) -> int:
    """
    Ingest a chunk of processed rows to Supabase with validation.
    
    Args:
        chunk: List of dictionaries ready for insertion
        source: Source identifier for logging
        validate: Whether to validate data before insertion
        
    Returns:
        Number of successfully inserted rows
    """
    if not chunk:
        return 0
    
    # Validate chunk data
    if validate:
        validated_chunk = []
        for item in chunk:
            if item and item.get('phrase'):
                # Ensure required fields are present
                if 'phrase' in item and item['phrase']:
                    validated_chunk.append(item)
                else:
                    logger.warning(f"Skipping invalid item: missing phrase")
        chunk = validated_chunk
    
    if not chunk:
        logger.warning(f"No valid items in chunk after validation")
        return 0
    
    # Generate embeddings for phrases
    phrases = [item['phrase'] for item in chunk if item.get('phrase')]
    try:
        embeddings = generate_embeddings(phrases)
        for i, item in enumerate(chunk):
            if i < len(embeddings):
                item['embedding'] = embeddings[i]
    except Exception as e:
        logger.warning(f"Error generating embeddings: {e}, continuing without embeddings")
    
    # Insert to Supabase in batches with validation
    if not HAS_SUPABASE or not supabase:
        logger.error("Supabase not configured - cannot insert data. Set SUPABASE_URL and SUPABASE_KEY.")
        return 0
    
    try:
        result = supabase.table('gematria_words').insert(chunk).execute()
        inserted_count = len(chunk)
        
        # Verify insertion by checking database
        if validate:
            try:
                # Check if data was actually inserted
                sample_phrase = chunk[0].get('phrase')
                if sample_phrase:
                    verify_result = supabase.table('gematria_words')\
                        .select('id')\
                        .eq('phrase', sample_phrase)\
                        .limit(1)\
                        .execute()
                    if not verify_result.data:
                        logger.error(f"Validation failed: Sample phrase not found in database after insertion")
                    else:
                        logger.info(f"Validation passed: {inserted_count} rows inserted and verified from {source}")
            except Exception as e:
                logger.warning(f"Could not verify insertion: {e}")
        
        logger.info(f"Inserted {inserted_count} rows from {source}")
        return inserted_count
    except Exception as e:
        logger.error(f"Error inserting chunk to Supabase: {e}")
        # Try individual inserts as fallback
        successful = 0
        for item in chunk:
            try:
                result = supabase.table('gematria_words').insert(item).execute()
                if result.data:
                    successful += 1
                else:
                    logger.warning(f"Insert returned no data for phrase: {item.get('phrase', 'unknown')}")
            except Exception as e2:
                logger.error(f"Error inserting individual item: {e2}, phrase: {item.get('phrase', 'unknown')}")
        return successful


def ingest_csv_file(file_path: str, chunk_size: int = 10000, max_rows: Optional[int] = None, 
                    checkpoint_interval: int = 50000, validate: bool = True) -> Dict:
    """
    Ingest a CSV file containing gematria data with progress tracking and checkpoints.
    
    Args:
        file_path: Path to CSV file
        chunk_size: Number of rows to process per chunk
        max_rows: Maximum number of rows to process (None for all)
        checkpoint_interval: Number of rows between checkpoints
        validate: Whether to validate data integrity
        
    Returns:
        Dictionary with ingestion results
    """
    logger.info(f"Starting CSV ingestion from {file_path}")
    
    if not os.path.exists(file_path):
        logger.error(f"CSV file not found: {file_path}")
        return {'success': False, 'error': 'File not found'}
    
    # Check current database count before ingestion
    initial_count = 0
    try:
        result = supabase.table('gematria_words').select('id', count='exact').limit(1).execute()
        initial_count = result.count if hasattr(result, 'count') else 0
        logger.info(f"Initial database count: {initial_count} records")
    except Exception as e:
        logger.warning(f"Could not get initial database count: {e}")
    
    # Detect CSV format
    csv_format = detect_csv_format(file_path)
    logger.info(f"Detected CSV format: {csv_format}")
    
    # Get total row count for progress bar
    try:
        total_rows = sum(1 for _ in open(file_path, 'r', encoding='utf-8')) - 1  # Subtract header
        if max_rows:
            total_rows = min(total_rows, max_rows)
        logger.info(f"Total rows to process: {total_rows}")
    except Exception as e:
        logger.warning(f"Could not determine total rows: {e}")
        total_rows = None
    
    # Process CSV in chunks
    total_ingested = 0
    total_processed = 0
    errors = []
    checkpoint_count = 0
    
    # Create checkpoint file for resuming
    checkpoint_file = f"{file_path}.checkpoint"
    last_checkpoint = 0
    
    # Try to resume from checkpoint
    if os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, 'r') as f:
                last_checkpoint = int(f.read().strip())
            logger.info(f"Resuming from checkpoint: {last_checkpoint} rows")
        except Exception as e:
            logger.warning(f"Could not read checkpoint file: {e}")
    
    try:
        # Use chunked reading for large files
        chunk_iterator = pd.read_csv(
            file_path,
            chunksize=chunk_size,
            encoding='utf-8',
            on_bad_lines='skip'  # Skip malformed lines
        )
        
        with tqdm(total=total_rows, desc=f"Ingesting {os.path.basename(file_path)}", unit="rows", 
                  initial=last_checkpoint) as pbar:
            for chunk_df in chunk_iterator:
                if max_rows and total_processed >= max_rows:
                    break
                
                # Skip rows before checkpoint
                if total_processed < last_checkpoint:
                    skip_count = min(len(chunk_df), last_checkpoint - total_processed)
                    total_processed += skip_count
                    pbar.update(skip_count)
                    continue
                
                # Process rows based on format
                processed_rows = []
                for _, row in chunk_df.iterrows():
                    if max_rows and total_processed >= max_rows:
                        break
                    
                    try:
                        if csv_format == 'gematrix789':
                            processed_row = process_gematrix789_row(row)
                        else:  # gimatria789
                            processed_row = process_gimatria789_row(row)
                        
                        if processed_row:
                            processed_rows.append(processed_row)
                            total_processed += 1
                    except Exception as e:
                        errors.append(f"Error processing row {total_processed}: {e}")
                        logger.warning(f"Error processing row {total_processed}: {e}")
                
                # Ingest chunk with validation
                if processed_rows:
                    ingested = ingest_csv_chunk(processed_rows, csv_format, validate=validate)
                    total_ingested += ingested
                    
                    # Verify database count increased
                    if validate and ingested > 0:
                        try:
                            verify_result = supabase.table('gematria_words').select('id', count='exact').limit(1).execute()
                            current_count = verify_result.count if hasattr(verify_result, 'count') else 0
                            expected_count = initial_count + total_ingested
                            if current_count < expected_count:
                                logger.warning(f"Database count mismatch: expected {expected_count}, got {current_count}")
                        except Exception as e:
                            logger.warning(f"Could not verify database count: {e}")
                
                # Update progress
                pbar.update(len(chunk_df))
                
                # Save checkpoint
                if total_processed % checkpoint_interval == 0:
                    checkpoint_count += 1
                    try:
                        with open(checkpoint_file, 'w') as f:
                            f.write(str(total_processed))
                        logger.info(f"Checkpoint {checkpoint_count}: {total_processed} rows processed, {total_ingested} ingested")
                    except Exception as e:
                        logger.warning(f"Could not save checkpoint: {e}")
                
                # Log progress periodically
                if total_processed % 50000 == 0:
                    logger.info(f"Progress: {total_processed} rows processed, {total_ingested} ingested")
    
    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")
        # Save checkpoint on error
        try:
            with open(checkpoint_file, 'w') as f:
                f.write(str(total_processed))
        except:
            pass
        return {'success': False, 'error': str(e), 'ingested': total_ingested, 'processed': total_processed}
    
    # Remove checkpoint file on successful completion
    if os.path.exists(checkpoint_file):
        try:
            os.remove(checkpoint_file)
            logger.info("Checkpoint file removed after successful completion")
        except Exception as e:
            logger.warning(f"Could not remove checkpoint file: {e}")
    
    # Final validation: check database count
    final_count = 0
    try:
        result = supabase.table('gematria_words').select('id', count='exact').limit(1).execute()
        final_count = result.count if hasattr(result, 'count') else 0
        records_added = final_count - initial_count
        logger.info(f"Final database count: {final_count} records (added {records_added}, ingested {total_ingested})")
        
        if records_added != total_ingested:
            logger.warning(f"Count mismatch: {records_added} records added vs {total_ingested} ingested")
    except Exception as e:
        logger.warning(f"Could not get final database count: {e}")
    
    # Log completion
    logger.info(f"CSV ingestion complete: {total_processed} rows processed, {total_ingested} ingested")
    
    # Log to hunches table
    try:
        hunch_content = f"CSV ingestion from {os.path.basename(file_path)}: {total_ingested}/{total_processed} rows ingested (DB: {initial_count} -> {final_count})"
        supabase.table('hunches').insert({
            'content': hunch_content,
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'completed',
            'cost': 0.0
        }).execute()
    except Exception as e:
        logger.error(f"Error logging hunch: {e}")
    
    return {
        'success': True,
        'total_processed': total_processed,
        'total_ingested': total_ingested,
        'initial_count': initial_count,
        'final_count': final_count,
        'records_added': final_count - initial_count,
        'errors': len(errors),
        'source': csv_format
    }


def main():
    """Main function for command-line usage."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python ingest_csv.py <csv_file_path> [chunk_size] [max_rows]")
        print("Example: python ingest_csv.py gematrix789.csv 10000 1000000")
        sys.exit(1)
    
    file_path = sys.argv[1]
    chunk_size = int(sys.argv[2]) if len(sys.argv) > 2 else 10000
    max_rows = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    print("=" * 60)
    print("Gematria Hive - CSV Ingestion")
    print("=" * 60)
    
    results = ingest_csv_file(file_path, chunk_size=chunk_size, max_rows=max_rows)
    
    print("\n" + "=" * 60)
    print("Ingestion Results:")
    print("=" * 60)
    print(f"Success: {results.get('success', False)}")
    print(f"Total Processed: {results.get('total_processed', 0)}")
    print(f"Total Ingested: {results.get('total_ingested', 0)}")
    print(f"Errors: {results.get('errors', 0)}")
    print(f"Source: {results.get('source', 'unknown')}")
    print("=" * 60)
    
    if results.get('success'):
        print("\n✅ CSV ingestion complete! Check ingestion_log.txt for details.")
    else:
        print(f"\n❌ CSV ingestion failed: {results.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()

