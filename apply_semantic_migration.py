#!/usr/bin/env python3
"""
Apply Semantic Layers Migration

Purpose: Apply semantic layers schema migration to Supabase
Note: Supabase Python client cannot execute DDL directly, so this script
provides instructions and validates the migration SQL.

Author: Gematria Hive Team
Date: January 6, 2025
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def validate_migration_sql(sql_file: str) -> bool:
    """Validate migration SQL file exists and is readable"""
    if not Path(sql_file).exists():
        print(f"❌ Migration file not found: {sql_file}")
        return False
    
    with open(sql_file, 'r') as f:
        sql = f.read()
    
    # Basic validation
    required_tables = [
        'word_roots',
        'semantic_layers',
        'word_associations',
        'alphabet_mappings',
        'numeral_systems',
        'symbols_sacred_geometry',
        'language_frequency',
        'master_blobs',
        'idioms_phrases'
    ]
    
    missing_tables = []
    for table in required_tables:
        if f'CREATE TABLE' in sql and table in sql:
            continue
        else:
            missing_tables.append(table)
    
    if missing_tables:
        print(f"⚠️  Warning: Some tables may be missing: {missing_tables}")
    
    print(f"✅ Migration SQL validated")
    print(f"📊 SQL length: {len(sql)} characters")
    print(f"📋 Tables to create: {len(required_tables) - len(missing_tables)}/{len(required_tables)}")
    
    return True

def check_supabase_connection() -> bool:
    """Check if Supabase connection is available"""
    try:
        from supabase import create_client
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        
        if not url or not key:
            print("❌ SUPABASE_URL or SUPABASE_KEY not set")
            return False
        
        supabase = create_client(url, key)
        # Test connection
        result = supabase.table('gematria_words').select('*').limit(1).execute()
        print("✅ Supabase connection verified")
        return True
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("Semantic Layers Migration Helper")
    print("=" * 60)
    print()
    
    # Validate migration file
    migration_file = "migrations/create_semantic_layers_schema.sql"
    if not validate_migration_sql(migration_file):
        return
    
    print()
    
    # Check Supabase connection
    if not check_supabase_connection():
        print()
        print("⚠️  Cannot verify Supabase connection")
        print("   Please check your .env file")
        return
    
    print()
    print("=" * 60)
    print("📋 Migration Instructions")
    print("=" * 60)
    print()
    print("⚠️  IMPORTANT: Supabase Python client cannot execute DDL")
    print("   You must apply the migration via Supabase Dashboard")
    print()
    print("📝 Steps to Apply Migration:")
    print()
    print("1. Go to Supabase Dashboard:")
    print("   https://supabase.com/dashboard")
    print()
    print("2. Select your project")
    print()
    print("3. Navigate to SQL Editor (left sidebar)")
    print()
    print("4. Click 'New Query'")
    print()
    print("5. Copy the contents of:")
    print(f"   {migration_file}")
    print()
    print("6. Paste into SQL Editor")
    print()
    print("7. Click 'Run' (or press Cmd/Ctrl + Enter)")
    print()
    print("8. Verify tables created:")
    print("   - word_roots")
    print("   - semantic_layers")
    print("   - word_associations")
    print("   - alphabet_mappings")
    print("   - numeral_systems")
    print("   - symbols_sacred_geometry")
    print("   - language_frequency")
    print("   - master_blobs")
    print("   - idioms_phrases")
    print()
    print("=" * 60)
    print("✅ Migration file ready for manual application")
    print("=" * 60)

if __name__ == "__main__":
    main()

