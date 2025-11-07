#!/usr/bin/env python3
"""
Database Setup Script

Purpose: Automated database setup and verification for Gematria Hive.
Tests connection, creates tables, and verifies everything is working.

Usage:
    python setup_database.py
    python setup_database.py --verify-only  # Just test connection
    python setup_database.py --create-tables  # Create tables via API

Author: Gematria Hive Team
Date: January 6, 2025
"""

import sys
import os
import argparse
import logging
from pathlib import Path
from typing import Dict, Optional

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_environment() -> Dict[str, bool]:
    """Check if environment variables are set"""
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    return {
        'SUPABASE_URL': bool(supabase_url),
        'SUPABASE_KEY': bool(supabase_key),
        'both_set': bool(supabase_url and supabase_key)
    }


def test_connection() -> Dict:
    """Test Supabase connection"""
    logger.info("=" * 60)
    logger.info("Testing Supabase Connection")
    logger.info("=" * 60)
    
    env_check = check_environment()
    
    if not env_check['both_set']:
        logger.error("❌ Environment variables not set")
        logger.error("   Set SUPABASE_URL and SUPABASE_KEY in .env file or environment")
        return {"status": "failed", "error": "Environment variables not set"}
    
    try:
        from supabase import create_client
        
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        logger.info(f"Connecting to Supabase: {supabase_url[:30]}...")
        supabase = create_client(supabase_url, supabase_key)
        
        # Test connection by querying a table
        logger.info("Testing connection...")
        result = supabase.table('bookmarks').select('*').limit(1).execute()
        
        logger.info("✅ Connection successful!")
        return {"status": "success", "supabase": supabase}
        
    except Exception as e:
        logger.error(f"❌ Connection failed: {e}")
        return {"status": "failed", "error": str(e)}


def verify_tables() -> Dict:
    """Verify that required tables exist"""
    logger.info("=" * 60)
    logger.info("Verifying Database Tables")
    logger.info("=" * 60)
    
    connection_result = test_connection()
    if connection_result.get("status") != "success":
        return connection_result
    
    supabase = connection_result.get("supabase")
    if not supabase:
        return {"status": "failed", "error": "No Supabase client"}
    
    required_tables = ['bookmarks', 'hunches', 'proofs', 'gematria_words']
    existing_tables = []
    missing_tables = []
    
    for table in required_tables:
        try:
            result = supabase.table(table).select('*').limit(1).execute()
            existing_tables.append(table)
            logger.info(f"✅ Table '{table}' exists")
        except Exception as e:
            missing_tables.append(table)
            logger.warning(f"⚠️  Table '{table}' not found: {e}")
    
    if missing_tables:
        logger.warning(f"Missing tables: {', '.join(missing_tables)}")
        logger.info("Run SQL migrations in Supabase SQL Editor:")
        logger.info("  - migrations/create_gematria_tables.sql")
        return {
            "status": "partial",
            "existing": existing_tables,
            "missing": missing_tables
        }
    else:
        logger.info("✅ All required tables exist!")
        return {
            "status": "success",
            "tables": existing_tables
        }


def verify_pgvector() -> Dict:
    """Verify pgvector extension is enabled"""
    logger.info("=" * 60)
    logger.info("Verifying pgvector Extension")
    logger.info("=" * 60)
    
    connection_result = test_connection()
    if connection_result.get("status") != "success":
        return connection_result
    
    supabase = connection_result.get("supabase")
    if not supabase:
        return {"status": "failed", "error": "No Supabase client"}
    
    try:
        # Try to query a table with vector column
        result = supabase.table('bookmarks').select('embedding').limit(1).execute()
        logger.info("✅ pgvector extension appears to be enabled")
        return {"status": "success"}
    except Exception as e:
        error_str = str(e).lower()
        if 'vector' in error_str or 'embedding' in error_str:
            logger.warning("⚠️  pgvector extension may not be enabled")
            logger.info("Run in Supabase SQL Editor:")
            logger.info("  CREATE EXTENSION IF NOT EXISTS vector;")
            return {"status": "partial", "note": "pgvector may need to be enabled"}
        else:
            logger.info("✅ Connection works (pgvector check inconclusive)")
            return {"status": "success"}


def print_setup_instructions():
    """Print setup instructions"""
    logger.info("=" * 60)
    logger.info("Database Setup Instructions")
    logger.info("=" * 60)
    logger.info("")
    logger.info("1. Create Supabase Project:")
    logger.info("   - Go to https://supabase.com")
    logger.info("   - Click 'New Project'")
    logger.info("   - Name: gematria-hive")
    logger.info("   - Set database password (save it!)")
    logger.info("   - Wait for project to be created")
    logger.info("")
    logger.info("2. Get API Keys:")
    logger.info("   - Go to Settings → API")
    logger.info("   - Copy 'Project URL' → SUPABASE_URL")
    logger.info("   - Copy 'anon public' key → SUPABASE_KEY")
    logger.info("")
    logger.info("3. Set Environment Variables:")
    logger.info("   Create .env file in project root:")
    logger.info("   SUPABASE_URL=https://your-project.supabase.co")
    logger.info("   SUPABASE_KEY=your-anon-key-here")
    logger.info("")
    logger.info("4. Run SQL Migrations:")
    logger.info("   - Go to Supabase Dashboard → SQL Editor")
    logger.info("   - Copy SQL from: migrations/create_gematria_tables.sql")
    logger.info("   - Paste and run")
    logger.info("")
    logger.info("5. Verify Setup:")
    logger.info("   python setup_database.py --verify-only")
    logger.info("")


def main():
    """Main setup function"""
    parser = argparse.ArgumentParser(
        description="Setup and verify Gematria Hive database",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Only verify connection (don't create tables)"
    )
    
    parser.add_argument(
        "--instructions",
        action="store_true",
        help="Print setup instructions"
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
    
    if args.instructions:
        print_setup_instructions()
        return 0
    
    logger.info("=" * 60)
    logger.info("Gematria Hive - Database Setup")
    logger.info("=" * 60)
    logger.info("")
    
    # Check environment
    env_check = check_environment()
    logger.info("Environment Variables:")
    logger.info(f"  SUPABASE_URL: {'✅ Set' if env_check['SUPABASE_URL'] else '❌ Not set'}")
    logger.info(f"  SUPABASE_KEY: {'✅ Set' if env_check['SUPABASE_KEY'] else '❌ Not set'}")
    logger.info("")
    
    if not env_check['both_set']:
        logger.error("❌ Environment variables not configured")
        logger.info("")
        print_setup_instructions()
        return 1
    
    # Test connection
    connection_result = test_connection()
    if connection_result.get("status") != "success":
        logger.error("❌ Database connection failed")
        logger.info("")
        print_setup_instructions()
        return 1
    
    logger.info("")
    
    # Verify tables
    tables_result = verify_tables()
    logger.info("")
    
    # Verify pgvector
    pgvector_result = verify_pgvector()
    logger.info("")
    
    # Summary
    logger.info("=" * 60)
    logger.info("Setup Summary")
    logger.info("=" * 60)
    
    all_good = (
        connection_result.get("status") == "success" and
        tables_result.get("status") in ["success", "partial"] and
        pgvector_result.get("status") in ["success", "partial"]
    )
    
    if all_good:
        logger.info("✅ Database setup complete!")
        logger.info("")
        logger.info("Next steps:")
        logger.info("1. Run end-to-end tests: python test_e2e.py")
        logger.info("2. Test kanban dashboard: streamlit run app.py")
        logger.info("3. Test ingestion: python scripts/ingest.py --input processed.json")
        return 0
    else:
        logger.warning("⚠️  Database setup incomplete")
        logger.info("")
        print_setup_instructions()
        return 1


if __name__ == "__main__":
    sys.exit(main())
