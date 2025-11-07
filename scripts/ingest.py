#!/usr/bin/env python3
"""
Ingestion Agent CLI Script

Purpose: Standalone CLI script for running the ingestion agent.
Ingests processed data into the database.

Usage:
    python scripts/ingest.py --input processed.json
    python scripts/ingest.py --input processed.json --table bookmarks --batch-size 100

Author: Gematria Hive Team
Date: January 6, 2025
"""

import sys
import os
import json
import argparse
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.ingestion import IngestionAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Ingest processed data into database using Ingestion Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Ingest processed data
  python scripts/ingest.py --input processed.json
  
  # Ingest to specific table with custom batch size
  python scripts/ingest.py --input processed.json --table gematria_words --batch-size 50
        """
    )
    
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Input JSON file path with processed data"
    )
    
    parser.add_argument(
        "--table",
        type=str,
        choices=["bookmarks", "gematria_words"],
        default="bookmarks",
        help="Target table (default: bookmarks)"
    )
    
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="Batch size for ingestion (default: 1000)"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Load input data
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Input file not found: {args.input}")
        sys.exit(1)
    
    logger.info(f"Loading data from {args.input}")
    with open(input_path, 'r') as f:
        data = json.load(f)
    
    if not data:
        logger.error("No data to ingest")
        sys.exit(1)
    
    logger.info(f"Loaded {len(data)} items")
    
    # Initialize agent
    logger.info("Initializing Ingestion Agent...")
    agent = IngestionAgent()
    
    # Ingest data
    logger.info(f"Ingesting {len(data)} items to {args.table} table...")
    
    if args.table == "gematria_words":
        ingested_count = agent.ingest_gematria_words(data, batch_size=args.batch_size)
    else:
        # Use default ingestion (bookmarks table)
        from ingest_pass1 import ingest_to_db
        ingested_count = ingest_to_db(data)
    
    logger.info(f"Successfully ingested {ingested_count}/{len(data)} items")
    
    if ingested_count < len(data):
        logger.warning(f"Some items failed to ingest: {ingested_count}/{len(data)}")
    
    logger.info("Ingestion complete")


if __name__ == "__main__":
    main()

