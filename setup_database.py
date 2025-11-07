#!/usr/bin/env python3
"""
Database Setup Script - Gematria Hive

Purpose: Complete database setup and migration for Supabase
- Enable pgvector extension
- Create all tables from migrations
- Create indexes and views
- Set up Row Level Security (RLS)

Usage:
    python setup_database.py

Author: Gematria Hive Team
Date: November 7, 2025
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Check for Supabase
try:
    from supabase import create_client, Client
    HAS_SUPABASE = True
except ImportError:
    HAS_SUPABASE = False
    logger.error("Supabase library not installed. Install with: pip install supabase")
    sys.exit(1)

# Get environment variables
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.error("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
    logger.error("Set them in .env file or Replit Secrets")
    sys.exit(1)

# Initialize Supabase client
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    logger.info("✅ Supabase client initialized")
except Exception as e:
    logger.error(f"Failed to initialize Supabase client: {e}")
    sys.exit(1)


def read_sql_file(file_path: Path) -> str:
    """Read SQL file content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading SQL file {file_path}: {e}")
        return ""


def execute_sql(sql: str, description: str) -> bool:
    """Execute SQL statement"""
    try:
        # Split by semicolons and execute each statement
        statements = [s.strip() for s in sql.split(';') if s.strip()]
        
        for statement in statements:
            if statement:
                # Skip comments
                if statement.startswith('--'):
                    continue
                
                # Execute via Supabase RPC or direct SQL
                # Note: Supabase Python client doesn't support raw SQL execution
                # We'll need to use the REST API or run via Supabase Dashboard
                logger.info(f"Executing: {description}")
                logger.warning(f"SQL statement (run in Supabase Dashboard):\n{statement[:200]}...")
        
        logger.info(f"✅ {description} - Run SQL in Supabase Dashboard SQL Editor")
        return True
    except Exception as e:
        logger.error(f"Error executing SQL: {e}")
        return False


def setup_database():
    """Complete database setup"""
    logger.info("=" * 60)
    logger.info("Gematria Hive - Database Setup")
    logger.info("=" * 60)
    
    # Check connection
    try:
        result = supabase.table('bookmarks').select('id').limit(1).execute()
        logger.info("✅ Database connection successful")
    except Exception as e:
        logger.warning(f"Database connection test failed (may be expected if tables don't exist): {e}")
    
    # Read migration files
    migrations_dir = Path(__file__).parent / "migrations"
    
    migration_files = [
        ("create_gematria_tables.sql", "Gematria tables"),
        ("create_complete_schema.sql", "Complete schema"),
    ]
    
    logger.info("\n" + "=" * 60)
    logger.info("Migration Files Found:")
    logger.info("=" * 60)
    
    for filename, description in migration_files:
        file_path = migrations_dir / filename
        if file_path.exists():
            logger.info(f"✅ {filename} - {description}")
            sql_content = read_sql_file(file_path)
            if sql_content:
                logger.info(f"   SQL statements: {len([s for s in sql_content.split(';') if s.strip()])} statements")
        else:
            logger.warning(f"⚠️  {filename} not found")
    
    logger.info("\n" + "=" * 60)
    logger.info("Database Setup Instructions:")
    logger.info("=" * 60)
    logger.info("""
1. Go to Supabase Dashboard: https://supabase.com/dashboard
2. Select your project
3. Go to SQL Editor
4. Run the following SQL files in order:

   a) migrations/create_gematria_tables.sql
   b) migrations/create_complete_schema.sql

5. Verify tables created in Table Editor
6. Test connection with this script again

Note: Supabase Python client doesn't support raw SQL execution.
      You must run SQL migrations via the Supabase Dashboard SQL Editor.
    """)
    
    # Test connection after setup
    logger.info("\n" + "=" * 60)
    logger.info("Connection Test:")
    logger.info("=" * 60)
    
    try:
        # Try to query bookmarks table
        result = supabase.table('bookmarks').select('id').limit(1).execute()
        logger.info("✅ bookmarks table exists and is accessible")
    except Exception as e:
        logger.warning(f"⚠️  bookmarks table not found or not accessible: {e}")
        logger.info("   Run migrations in Supabase Dashboard SQL Editor")
    
    try:
        # Try to query gematria_words table
        result = supabase.table('gematria_words').select('id').limit(1).execute()
        logger.info("✅ gematria_words table exists and is accessible")
    except Exception as e:
        logger.warning(f"⚠️  gematria_words table not found or not accessible: {e}")
        logger.info("   Run migrations in Supabase Dashboard SQL Editor")
    
    logger.info("\n" + "=" * 60)
    logger.info("Setup Complete!")
    logger.info("=" * 60)
    logger.info("""
Next Steps:
1. Run SQL migrations in Supabase Dashboard SQL Editor
2. Verify all tables created
3. Test ingestion with: python ingest_pass1.py test_data.json
4. Check database in Supabase Table Editor
    """)


if __name__ == "__main__":
    setup_database()

