#!/usr/bin/env python3
"""
Google Drive OAuth Setup Script

Purpose: Run OAuth 2.0 flow to get Google Drive API access
- Generate OAuth credentials
- Handle token refresh
- Save refresh token to .env

Usage:
    python scripts/setup_google_drive_oauth.py

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.google_drive_auth import run_oauth_flow, save_refresh_token

load_dotenv()


def main():
    """Run OAuth flow and save refresh token"""
    print("=" * 60)
    print("Google Drive OAuth Setup")
    print("=" * 60)
    print()
    
    # Get credentials from environment
    client_id = os.getenv('GOOGLE_DRIVE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_DRIVE_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("❌ Error: GOOGLE_DRIVE_CLIENT_ID and GOOGLE_DRIVE_CLIENT_SECRET must be set in .env")
        print()
        print("Steps to get credentials:")
        print("1. Go to https://console.cloud.google.com")
        print("2. Create a project or select existing")
        print("3. Enable Google Drive API")
        print("4. Go to APIs & Services → Credentials")
        print("5. Create OAuth 2.0 Client ID (Desktop app)")
        print("6. Copy Client ID and Client Secret to .env")
        print()
        return 1
    
    print("✅ Found OAuth credentials in .env")
    print()
    print("Starting OAuth flow...")
    print("A browser window will open for authentication.")
    print()
    
    # Run OAuth flow
    try:
        creds = run_oauth_flow(client_id, client_secret)
        
        if not creds:
            print("❌ OAuth flow failed")
            return 1
        
        print("✅ OAuth flow completed successfully")
        print()
        
        # Save refresh token
        env_file = project_root / ".env"
        if save_refresh_token(creds, str(env_file)):
            print(f"✅ Refresh token saved to {env_file}")
            print()
            print("You can now use Google Drive integration!")
            print()
            return 0
        else:
            print("❌ Failed to save refresh token")
            print()
            print("Manual step: Add this to your .env file:")
            print(f"GOOGLE_DRIVE_REFRESH_TOKEN={creds.refresh_token}")
            print()
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

