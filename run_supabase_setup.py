#!/usr/bin/env python3
"""
Supabase Database Setup - Automated Guide

Purpose: Interactive guide to complete Supabase database setup
- Guides through project creation
- Provides SQL migration scripts
- Verifies setup
- Tests connection

Usage:
    python run_supabase_setup.py

Author: Gematria Hive Team
Date: November 7, 2025
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Optional

print("=" * 70)
print("GEMATRIA HIVE - SUPABASE DATABASE SETUP")
print("=" * 70)
print()

# Step 1: Check if already configured
print("Step 1: Checking current configuration...")
print("-" * 70)

from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if SUPABASE_URL and SUPABASE_KEY:
    print(f"✅ SUPABASE_URL: {SUPABASE_URL[:40]}...")
    print(f"✅ SUPABASE_KEY: {SUPABASE_KEY[:20]}...")
    print()
    print("Environment variables are set!")
    print()
    
    # Test connection
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        result = supabase.table('bookmarks').select('*').limit(1).execute()
        print("✅ Connection successful!")
        print("✅ Database is configured and working!")
        print()
        print("Next steps:")
        print("1. Run migrations if not done: python setup_database.py")
        print("2. Test ingestion: python ingest_pass1.py test_data.json")
        print("3. Run Streamlit: streamlit run app.py")
        sys.exit(0)
    except Exception as e:
        print(f"⚠️  Connection test failed: {e}")
        print("   This is expected if tables don't exist yet.")
        print("   Continue with setup to create tables.")
        print()
else:
    print("❌ Environment variables not set")
    print()
    print("You need to:")
    print("1. Create Supabase project at https://supabase.com")
    print("2. Get API keys from Settings → API")
    print("3. Set SUPABASE_URL and SUPABASE_KEY")
    print()

# Step 2: Guide through setup
print("=" * 70)
print("SETUP GUIDE")
print("=" * 70)
print()

print("📋 Step-by-Step Instructions:")
print()
print("1. CREATE SUPABASE PROJECT (5 minutes)")
print("   - Go to: https://supabase.com")
print("   - Sign in or create account")
print("   - Click 'New Project'")
print("   - Name: gematria-hive")
print("   - Set database password (SAVE IT!)")
print("   - Choose region")
print("   - Wait for project creation")
print()

print("2. GET API KEYS (2 minutes)")
print("   - Go to: Settings → API")
print("   - Copy 'Project URL' → This is SUPABASE_URL")
print("   - Copy 'anon public' key → This is SUPABASE_KEY")
print()

print("3. SET ENVIRONMENT VARIABLES (2 minutes)")
print()
print("   CLI/Cursor:")
print("   ```bash")
print("   cat > .env << EOF")
print("   SUPABASE_URL=https://your-project.supabase.co")
print("   SUPABASE_KEY=your-anon-key-here")
print("   EOF")
print("   ```")
print()
print("   Replit:")
print("   - Click lock icon in sidebar")
print("   - Add SUPABASE_URL and SUPABASE_KEY as secrets")
print()

print("4. ENABLE PGVECTOR (1 minute)")
print("   - Go to: Supabase Dashboard → SQL Editor")
print("   - Run: CREATE EXTENSION IF NOT EXISTS vector;")
print()

print("5. RUN MIGRATIONS (5 minutes)")
print("   - Go to: Supabase Dashboard → SQL Editor")
print("   - Run migrations/create_gematria_tables.sql")
print("   - Run migrations/create_complete_schema.sql")
print()

print("6. VERIFY SETUP (1 minute)")
print("   - Run: python setup_database.py")
print()

# Step 3: Provide SQL scripts
print("=" * 70)
print("SQL MIGRATION SCRIPTS")
print("=" * 70)
print()

migrations_dir = Path(__file__).parent / "migrations"

migration_files = [
    ("create_gematria_tables.sql", "Gematria tables"),
    ("create_complete_schema.sql", "Complete schema"),
]

print("Migration files to run in Supabase SQL Editor:")
print()

for filename, description in migration_files:
    file_path = migrations_dir / filename
    if file_path.exists():
        print(f"✅ {filename} - {description}")
        print(f"   Location: {file_path}")
        print()
        
        # Show first few lines
        with open(file_path, 'r') as f:
            lines = f.readlines()[:10]
            print("   First few lines:")
            for line in lines:
                print(f"   {line.rstrip()}")
            print("   ...")
            print()
    else:
        print(f"❌ {filename} - NOT FOUND")
        print()

# Step 4: Create .env template
print("=" * 70)
print("ENVIRONMENT VARIABLES TEMPLATE")
print("=" * 70)
print()

env_template = """# Gematria Hive - Environment Variables
# Copy this to .env and fill in your values

# Supabase Configuration
# Get these from: https://supabase.com/dashboard → Settings → API
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
"""

env_file = Path(__file__).parent / ".env"
env_example_file = Path(__file__).parent / ".env.example"

if not env_file.exists():
    print("Creating .env.example file...")
    with open(env_example_file, 'w') as f:
        f.write(env_template)
    print(f"✅ Created: {env_example_file}")
    print()
    print("To set up:")
    print("1. Copy .env.example to .env")
    print("2. Fill in your Supabase credentials")
    print("   cp .env.example .env")
    print("   # Then edit .env with your values")
    print()
else:
    print("✅ .env file exists")
    print()

# Step 5: Quick setup commands
print("=" * 70)
print("QUICK SETUP COMMANDS")
print("=" * 70)
print()

print("After setting up Supabase:")
print()
print("# 1. Test connection")
print("python setup_database.py")
print()
print("# 2. Test ingestion")
print("python ingest_pass1.py test_data.json")
print()
print("# 3. Test agents")
print("python -c \"from agents import MCPOrchestrator; print('✅ Ready')\"")
print()
print("# 4. Run Streamlit")
print("streamlit run app.py")
print()

# Step 6: Interactive setup (if possible)
print("=" * 70)
print("INTERACTIVE SETUP")
print("=" * 70)
print()

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Would you like to set environment variables now?")
    print("(You can also do this manually by creating .env file)")
    print()
    
    # Try to get input (but don't block if not available)
    try:
        response = input("Enter SUPABASE_URL (or press Enter to skip): ").strip()
        if response:
            SUPABASE_URL = response
            print(f"✅ SUPABASE_URL set: {SUPABASE_URL[:40]}...")
        
        response = input("Enter SUPABASE_KEY (or press Enter to skip): ").strip()
        if response:
            SUPABASE_KEY = response
            print(f"✅ SUPABASE_KEY set: {SUPABASE_KEY[:20]}...")
        
        if SUPABASE_URL and SUPABASE_KEY:
            # Create .env file
            env_content = f"""# Gematria Hive - Environment Variables
# Generated by run_supabase_setup.py

SUPABASE_URL={SUPABASE_URL}
SUPABASE_KEY={SUPABASE_KEY}
"""
            with open(env_file, 'w') as f:
                f.write(env_content)
            print()
            print(f"✅ Created .env file with your credentials")
            print()
            print("Next steps:")
            print("1. Enable pgvector in Supabase SQL Editor")
            print("2. Run migrations in Supabase SQL Editor")
            print("3. Verify: python setup_database.py")
    except (EOFError, KeyboardInterrupt):
        print()
        print("Skipping interactive setup. Set environment variables manually.")
        print()

print("=" * 70)
print("SETUP GUIDE COMPLETE")
print("=" * 70)
print()
print("📚 Documentation:")
print("   - SUPABASE_SETUP_INSTRUCTIONS.md - Detailed step-by-step guide")
print("   - DATABASE_SETUP_COMPLETE.md - Complete database setup")
print("   - COMPLETE_SETUP_GUIDE.md - Full setup guide")
print()
print("Ready to set up Supabase! 🐝✨")
print()

