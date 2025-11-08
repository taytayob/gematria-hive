#!/usr/bin/env python3
"""
Apply API Keys Migration

Purpose: Create api_keys table in Supabase and log INTERNAL_API_KEY
- Read migration SQL
- Apply to Supabase
- Log existing INTERNAL_API_KEY

Usage:
    python scripts/apply_api_keys_migration.py

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import sys
import hashlib
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

load_dotenv()

try:
    from supabase import create_client, Client
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    if SUPABASE_URL and SUPABASE_KEY:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        HAS_SUPABASE = True
    else:
        HAS_SUPABASE = False
        supabase = None
except Exception:
    HAS_SUPABASE = False
    supabase = None


def hash_key(key: str) -> str:
    """Hash a key for storage"""
    return hashlib.sha256(key.encode()).hexdigest()


def apply_migration():
    """Apply API keys migration to Supabase"""
    if not HAS_SUPABASE or not supabase:
        print("❌ Supabase not configured")
        return False
    
    migration_file = project_root / "migrations" / "create_api_keys_table.sql"
    
    if not migration_file.exists():
        print(f"❌ Migration file not found: {migration_file}")
        return False
    
    try:
        # Read migration SQL
        sql = migration_file.read_text()
        
        # Split into individual statements
        statements = [s.strip() for s in sql.split(';') if s.strip() and not s.strip().startswith('--')]
        
        print("Applying API keys migration...")
        for i, statement in enumerate(statements, 1):
            if statement:
                try:
                    # Execute via Supabase RPC or direct SQL
                    # Note: Supabase Python client doesn't support raw SQL directly
                    # We'll need to use the SQL Editor or create a function
                    print(f"  Statement {i}/{len(statements)}: {statement[:50]}...")
                except Exception as e:
                    print(f"  ⚠️  Error in statement {i}: {e}")
        
        print("⚠️  Note: Supabase Python client doesn't support raw SQL execution")
        print("   Please run migrations/create_api_keys_table.sql in Supabase SQL Editor")
        print("   Go to: https://supabase.com/dashboard → SQL Editor")
        return False
        
    except Exception as e:
        print(f"❌ Error reading migration: {e}")
        return False


def log_internal_api_key():
    """Log INTERNAL_API_KEY to database"""
    if not HAS_SUPABASE or not supabase:
        print("⚠️  Supabase not configured, skipping database log")
        return False
    
    internal_key = os.getenv('INTERNAL_API_KEY')
    if not internal_key or internal_key == 'internal-api-key-change-in-production':
        print("⚠️  INTERNAL_API_KEY not set or using default")
        return False
    
    key_hash = hash_key(internal_key)
    
    try:
        # Check if table exists
        try:
            result = supabase.table("api_keys").select("key_name").eq("key_name", "INTERNAL_API_KEY").limit(1).execute()
            
            if result.data:
                # Update existing
                result = supabase.table("api_keys").update({
                    "key_value_hash": key_hash,
                    "key_status": "active",
                    "updated_at": datetime.now().isoformat(),
                    "metadata": {
                        "generated_at": datetime.now().isoformat(),
                        "key_length": len(internal_key),
                        "rotation_recommended": "90 days"
                    }
                }).eq("key_name", "INTERNAL_API_KEY").execute()
                
                if result.data:
                    print("✅ Updated INTERNAL_API_KEY metadata in database")
                    return True
            else:
                # Insert new
                result = supabase.table("api_keys").insert({
                    "key_name": "INTERNAL_API_KEY",
                    "key_type": "internal",
                    "key_value_hash": key_hash,
                    "key_status": "active",
                    "service_name": "Internal",
                    "description": "Internal API authentication key for agent communication",
                    "metadata": {
                        "generated_at": datetime.now().isoformat(),
                        "key_length": len(internal_key),
                        "rotation_recommended": "90 days"
                    },
                    "created_by": "system"
                }).execute()
                
                if result.data:
                    print("✅ Logged INTERNAL_API_KEY metadata to database")
                    return True
                    
        except Exception as e:
            if "relation" in str(e).lower() or "does not exist" in str(e).lower():
                print("⚠️  api_keys table not found")
                print("   Please run migrations/create_api_keys_table.sql in Supabase SQL Editor")
                print("   Go to: https://supabase.com/dashboard → SQL Editor")
                return False
            else:
                raise
        
        return False
    except Exception as e:
        print(f"⚠️  Error logging to database: {e}")
        return False


def main():
    """Main function"""
    print("=" * 60)
    print("API Keys Migration & Logging")
    print("=" * 60)
    print()
    
    # Try to apply migration
    print("Step 1: Applying migration...")
    apply_migration()
    print()
    
    # Try to log key
    print("Step 2: Logging INTERNAL_API_KEY...")
    log_internal_api_key()
    print()
    
    print("=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print()
    print("1. Run migration in Supabase SQL Editor:")
    print("   - Go to: https://supabase.com/dashboard")
    print("   - Click: SQL Editor")
    print("   - Run: migrations/create_api_keys_table.sql")
    print()
    print("2. After migration, run this script again to log the key")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

