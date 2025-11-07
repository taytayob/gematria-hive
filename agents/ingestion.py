"""
Ingestion Agent

Purpose: Store processed data in database

Author: Gematria Hive Team
Date: November 6, 2025
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
from agents.orchestrator import AgentState

# Import from main ingestion script
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ingest_pass1 import ingest_to_db

logger = logging.getLogger(__name__)

# Import CSV ingestion and Supabase client
try:
    from ingest_csv import ingest_csv_file
    HAS_CSV_INGESTION = True
except ImportError:
    HAS_CSV_INGESTION = False
    logger.warning("CSV ingestion module not available")

try:
    from supabase import create_client, Client
    from dotenv import load_dotenv
    import os
    load_dotenv()
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    if SUPABASE_URL and SUPABASE_KEY:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        HAS_SUPABASE = True
    else:
        HAS_SUPABASE = False
except Exception:
    HAS_SUPABASE = False


class IngestionAgent:
    """
    Ingestion Agent - Stores data in database
    
    Operations:
    - Batch insert to Supabase (bookmarks table)
    - Batch insert to gematria_words table
    - CSV file ingestion
    - Log hunches
    - Track ingestion metrics
    """
    
    def __init__(self):
        """Initialize ingestion agent"""
        self.name = "ingestion_agent"
        self.supabase = supabase if HAS_SUPABASE else None
        logger.info(f"Initialized {self.name}")
    
    def ingest_gematria_words(self, words: List[Dict], batch_size: int = 1000) -> int:
        """
        Ingest gematria words to gematria_words table.
        
        Args:
            words: List of word dictionaries
            batch_size: Number of words to insert per batch
            
        Returns:
            Number of successfully ingested words
        """
        if not self.supabase:
            logger.error("Supabase client not available")
            return 0
        
        if not words:
            return 0
        
        ingested_count = 0
        
        # Process in batches
        for i in range(0, len(words), batch_size):
            batch = words[i:i+batch_size]
            try:
                result = self.supabase.table('gematria_words').insert(batch).execute()
                ingested_count += len(batch)
                logger.info(f"Ingested batch of {len(batch)} gematria words")
            except Exception as e:
                logger.error(f"Error inserting gematria words batch: {e}")
                # Try individual inserts as fallback
                for word in batch:
                    try:
                        self.supabase.table('gematria_words').insert(word).execute()
                        ingested_count += 1
                    except Exception as e2:
                        logger.error(f"Error inserting individual gematria word: {e2}")
        
        return ingested_count
    
    def ingest_csv_file(self, file_path: str, chunk_size: int = 10000) -> Dict:
        """
        Ingest CSV file containing gematria data.
        
        Args:
            file_path: Path to CSV file
            chunk_size: Number of rows to process per chunk
            
        Returns:
            Dictionary with ingestion results
        """
        if not HAS_CSV_INGESTION:
            logger.error("CSV ingestion module not available")
            return {'success': False, 'error': 'CSV ingestion module not available'}
        
        try:
            results = ingest_csv_file(file_path, chunk_size=chunk_size)
            logger.info(f"CSV ingestion completed: {results.get('total_ingested', 0)} rows ingested")
            return results
        except Exception as e:
            logger.error(f"Error ingesting CSV file: {e}")
            return {'success': False, 'error': str(e)}
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute ingestion task
        
        Args:
            state: Agent state with processed data
            
        Returns:
            Updated state with ingestion results
        """
        data = state.get("data", [])
        data_type = state.get("data_type", "bookmarks")  # 'bookmarks', 'gematria_words', 'csv'
        source = state.get("source", None)  # For CSV files
        
        logger.info(f"Ingestion agent: Ingesting {len(data)} items (type: {data_type})")
        
        try:
            if data_type == "gematria_words":
                # Ingest to gematria_words table
                ingested_count = self.ingest_gematria_words(data)
                state["context"]["ingestion_count"] = ingested_count
                state["results"].append({
                    "agent": self.name,
                    "action": "ingest_gematria_words",
                    "count": ingested_count,
                    "total": len(data)
                })
                logger.info(f"Gematria words ingestion complete: {ingested_count}/{len(data)} items ingested")
            
            elif data_type == "csv" and source:
                # Ingest CSV file
                results = self.ingest_csv_file(source)
                ingested_count = results.get('total_ingested', 0)
                state["context"]["ingestion_count"] = ingested_count
                state["context"]["csv_results"] = results
                state["results"].append({
                    "agent": self.name,
                    "action": "ingest_csv",
                    "count": ingested_count,
                    "total": results.get('total_processed', 0),
                    "success": results.get('success', False)
                })
                logger.info(f"CSV ingestion complete: {ingested_count} rows ingested")
            
            else:
                # Default: Use ingest_to_db from ingest_pass1.py (bookmarks table)
                ingested_count = ingest_to_db(data)
                state["context"]["ingestion_count"] = ingested_count
                state["results"].append({
                    "agent": self.name,
                    "action": "ingest",
                    "count": ingested_count,
                    "total": len(data)
                })
                logger.info(f"Ingestion complete: {ingested_count}/{len(data)} items ingested")
            
        except Exception as e:
            logger.error(f"Ingestion error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

