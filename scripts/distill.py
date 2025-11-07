#!/usr/bin/env python3
"""
Distillation Agent CLI Script

Purpose: Standalone CLI script for running the distillation agent.
Processes extracted data, generates embeddings, and categorizes relevance.

Usage:
    python scripts/distill.py --input extracted.json --output processed.json
    python scripts/distill.py --input extracted.json --output processed.json --batch-size 100

Author: Gematria Hive Team
Date: January 6, 2025
"""

import sys
import os
import json
import argparse
import logging
from pathlib import Path
from typing import List, Dict

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.distillation import DistillationAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Process and distill data using Distillation Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process extracted data
  python scripts/distill.py --input extracted.json --output processed.json
  
  # Process with custom batch size
  python scripts/distill.py --input extracted.json --output processed.json --batch-size 50
        """
    )
    
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Input JSON file path with extracted data"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output JSON file path for processed data"
    )
    
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Batch size for processing (default: 100)"
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
        logger.error("No data to process")
        sys.exit(1)
    
    logger.info(f"Loaded {len(data)} items")
    
    # Initialize agent
    logger.info("Initializing Distillation Agent...")
    agent = DistillationAgent()
    
    # Process data
    logger.info(f"Processing {len(data)} items...")
    processed_data = agent.process_data(data)
    
    if not processed_data:
        logger.error("Processing failed")
        sys.exit(1)
    
    logger.info(f"Successfully processed {len(processed_data)} items")
    
    # Save output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(processed_data, f, indent=2)
    
    logger.info(f"Processed data written to {args.output}")
    
    # Print summary
    if processed_data:
        avg_relevance = sum(item.get("relevance_score", 0) for item in processed_data) / len(processed_data)
        print(f"\nDistillation Summary:")
        print(f"  Total processed: {len(processed_data)}")
        print(f"  Average relevance: {avg_relevance:.2f}")
        print(f"  Sample item keys: {list(processed_data[0].keys())}")
    
    logger.info("Distillation complete")


if __name__ == "__main__":
    main()

