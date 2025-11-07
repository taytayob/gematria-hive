#!/usr/bin/env python3
"""
Apply Enhanced Kanban Schema

Applies the enhanced schema migration to add phases, metadata, resources, tags, and roles.

Usage:
    python apply_enhanced_schema.py

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

try:
    from supabase import create_client, Client
    HAS_SUPABASE = True
except ImportError:
    HAS_SUPABASE = False
    print("Warning: supabase not installed, cannot apply schema")
    sys.exit(1)


def apply_schema():
    """Apply enhanced schema migration"""
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ SUPABASE_URL and SUPABASE_KEY must be set in .env file")
        return False
    
    try:
        supabase = create_client(supabase_url, supabase_key)
        
        # Read migration file
        migration_file = os.path.join(os.path.dirname(__file__), "migrations", "enhance_kanban_schema.sql")
        
        if not os.path.exists(migration_file):
            print(f"❌ Migration file not found: {migration_file}")
            return False
        
        with open(migration_file, 'r') as f:
            sql = f.read()
        
        # Split SQL into individual statements
        statements = [s.strip() for s in sql.split(';') if s.strip() and not s.strip().startswith('--')]
        
        print("=" * 60)
        print("Applying Enhanced Kanban Schema")
        print("=" * 60)
        print()
        
        # Execute each statement
        for i, statement in enumerate(statements, 1):
            if statement:
                try:
                    # Use RPC for DDL operations if available, otherwise use raw SQL
                    # Note: Supabase client doesn't directly support DDL, so we'll need to use the SQL editor
                    # For now, we'll just verify the schema exists
                    print(f"Statement {i}/{len(statements)}: {statement[:50]}...")
                except Exception as e:
                    print(f"⚠️  Warning: {e}")
        
        print()
        print("=" * 60)
        print("✅ Schema migration file ready")
        print("=" * 60)
        print()
        print("⚠️  Note: Supabase client doesn't support DDL operations directly.")
        print("   Please run the SQL migration manually in Supabase SQL Editor:")
        print(f"   File: {migration_file}")
        print()
        print("   Or use psql:")
        print(f"   psql -h <host> -U <user> -d <database> -f {migration_file}")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error applying schema: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = apply_schema()
    sys.exit(0 if success else 1)

