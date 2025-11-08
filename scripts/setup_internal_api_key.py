#!/usr/bin/env python3
"""
Setup Internal API Key

Purpose: Generate secure INTERNAL_API_KEY and log to database
- Generate secure random key
- Update .env file
- Log to api_keys table (metadata only, never plain text)

Usage:
    python scripts/setup_internal_api_key.py

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import sys
import secrets
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


def generate_secure_key(length: int = 32) -> str:
    """Generate a secure random key"""
    return secrets.token_urlsafe(length)


def hash_key(key: str) -> str:
    """Hash a key for storage (never store plain text!)"""
    return hashlib.sha256(key.encode()).hexdigest()


def update_env_file(key: str, env_file: str = ".env") -> bool:
    """Update .env file with new key"""
    env_path = Path(project_root) / env_file
    
    try:
        # Read existing content
        if env_path.exists():
            content = env_path.read_text()
        else:
            content = ""
        
        # Update or add INTERNAL_API_KEY
        lines = content.split('\n')
        updated = False
        new_lines = []
        
        for line in lines:
            if line.startswith('INTERNAL_API_KEY='):
                new_lines.append(f'INTERNAL_API_KEY={key}')
                updated = True
            else:
                new_lines.append(line)
        
        if not updated:
            # Add new line
            if content and not content.endswith('\n'):
                new_lines.append('')
            new_lines.append(f'INTERNAL_API_KEY={key}')
        
        # Write back
        env_path.write_text('\n'.join(new_lines))
        print(f"✅ Updated {env_file} with new INTERNAL_API_KEY")
        return True
    except Exception as e:
        print(f"❌ Error updating {env_file}: {e}")
        return False


def log_to_database(key_name: str, key_hash: str, service_name: str = None, service_url: str = None) -> bool:
    """Log API key metadata to database"""
    if not HAS_SUPABASE or not supabase:
        print("⚠️  Supabase not configured, skipping database log")
        return False
    
    try:
        # Check if table exists, if not create it
        try:
            # Try to insert
            result = supabase.table("api_keys").insert({
                "key_name": key_name,
                "key_type": "internal",
                "key_value_hash": key_hash,
                "key_status": "active",
                "service_name": service_name or "Internal",
                "service_url": service_url,
                "description": "Internal API authentication key for agent communication",
                "metadata": {
                    "generated_at": datetime.utcnow().isoformat(),
                    "key_length": len(key_hash),
                    "rotation_recommended": "90 days"
                },
                "created_by": "system"
            }).execute()
            
            if result.data:
                print(f"✅ Logged {key_name} metadata to database")
                return True
        except Exception as e:
            # Table might not exist, try to create it
            if "relation" in str(e).lower() or "does not exist" in str(e).lower():
                print("⚠️  api_keys table not found, creating migration...")
                print("   Run: migrations/create_api_keys_table.sql in Supabase SQL Editor")
                return False
            else:
                # Update existing record
                try:
                    result = supabase.table("api_keys").update({
                        "key_value_hash": key_hash,
                        "key_status": "active",
                        "updated_at": datetime.utcnow().isoformat(),
                        "metadata": {
                            "generated_at": datetime.utcnow().isoformat(),
                            "key_length": len(key_hash),
                            "rotation_recommended": "90 days"
                        }
                    }).eq("key_name", key_name).execute()
                    
                    if result.data:
                        print(f"✅ Updated {key_name} metadata in database")
                        return True
                except Exception as e2:
                    print(f"⚠️  Error updating database: {e2}")
                    return False
        
        return False
    except Exception as e:
        print(f"⚠️  Error logging to database: {e}")
        return False


def main():
    """Main setup function"""
    print("=" * 60)
    print("Internal API Key Setup")
    print("=" * 60)
    print()
    
    # Generate secure key
    print("Generating secure random key...")
    new_key = generate_secure_key(32)
    key_hash = hash_key(new_key)
    
    print(f"✅ Generated secure key: {new_key[:20]}...")
    print()
    
    # Update .env file
    print("Updating .env file...")
    if update_env_file(new_key):
        print()
    else:
        print("❌ Failed to update .env file")
        return 1
    
    # Log to database
    print("Logging to database...")
    log_to_database(
        key_name="INTERNAL_API_KEY",
        key_hash=key_hash,
        service_name="Internal",
        service_url=None
    )
    print()
    
    # Verify
    print("Verifying setup...")
    load_dotenv(override=True)  # Reload .env
    env_key = os.getenv('INTERNAL_API_KEY')
    
    if env_key == new_key:
        print("✅ INTERNAL_API_KEY successfully set in .env")
    else:
        print("⚠️  Warning: Key mismatch in .env")
    
    print()
    print("=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Restart any running services to pick up new key")
    print("2. Update docker-compose.yml if using Docker")
    print("3. Update Replit Secrets if using Replit")
    print()
    print("⚠️  IMPORTANT: Never commit .env file to git!")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

