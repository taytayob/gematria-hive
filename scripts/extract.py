#!/usr/bin/env python3
"""
Extraction Agent CLI Script

Purpose: Standalone CLI script for running the extraction agent.
Can be used independently without running the full application.

Usage:
    python scripts/extract.py --source dewey_json.json
    python scripts/extract.py --source data.json --output extracted.json
    python scripts/extract.py --source dewey_json.json --format json

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

from agents.extraction import ExtractionAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Extract data from various sources using Extraction Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract from JSON file
  python scripts/extract.py --source dewey_json.json
  
  # Extract and save to output file
  python scripts/extract.py --source data.json --output extracted.json
  
  # Extract and print summary
  python scripts/extract.py --source dewey_json.json --summary
        """
    )
    
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="Source file path or identifier (e.g., 'dewey_json.json')"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (optional, prints to stdout if not specified)"
    )
    
    parser.add_argument(
        "--format",
        type=str,
        choices=["json", "csv"],
        default="json",
        help="Output format (default: json)"
    )
    
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print summary statistics instead of full data"
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
    
    # Initialize agent
    logger.info("Initializing Extraction Agent...")
    agent = ExtractionAgent()
    
    # Extract data
    logger.info(f"Extracting from source: {args.source}")
    data = agent.extract_from_source(args.source)
    
    if not data:
        logger.error("No data extracted")
        sys.exit(1)
    
    logger.info(f"Successfully extracted {len(data)} items")
    
    # Output results
    if args.summary:
        # Print summary
        print(f"\nExtraction Summary:")
        print(f"  Total items: {len(data)}")
        if data:
            print(f"  Sample keys: {list(data[0].keys())}")
    else:
        # Output full data
        if args.output:
            # Write to file
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            if args.format == "json":
                with open(output_path, 'w') as f:
                    json.dump(data, f, indent=2)
            elif args.format == "csv":
                import pandas as pd
                df = pd.DataFrame(data)
                df.to_csv(output_path, index=False)
            
            logger.info(f"Data written to {args.output}")
        else:
            # Print to stdout
            print(json.dumps(data, indent=2))
    
    logger.info("Extraction complete")


if __name__ == "__main__":
    main()

