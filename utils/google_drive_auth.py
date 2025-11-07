"""
Google Drive OAuth Authentication Helper

Purpose: Handle OAuth 2.0 flow for Google Drive API access
- Generate OAuth credentials
- Handle token refresh
- Store credentials securely

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import json
import logging
from typing import Optional, Dict
from pathlib import Path
from dotenv import load_dotenv

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    HAS_GOOGLE_AUTH = True
except ImportError:
    HAS_GOOGLE_AUTH = False
    print("Warning: google-auth-oauthlib package not installed, OAuth disabled")

load_dotenv()

logger = logging.getLogger(__name__)

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


def get_credentials_from_env() -> Optional[Credentials]:
    """
    Get credentials from environment variables
    
    Returns:
        Credentials object or None
    """
    if not HAS_GOOGLE_AUTH:
        return None
    
    client_id = os.getenv('GOOGLE_DRIVE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_DRIVE_CLIENT_SECRET')
    refresh_token = os.getenv('GOOGLE_DRIVE_REFRESH_TOKEN')
    
    if not client_id or not client_secret:
        logger.warning("GOOGLE_DRIVE_CLIENT_ID or GOOGLE_DRIVE_CLIENT_SECRET not set")
        return None
    
    if refresh_token:
        # Use existing refresh token
        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=client_id,
            client_secret=client_secret,
            scopes=SCOPES
        )
        try:
            # Refresh the token
            creds.refresh(Request())
            return creds
        except Exception as e:
            logger.error(f"Failed to refresh credentials: {e}")
            return None
    else:
        logger.warning("GOOGLE_DRIVE_REFRESH_TOKEN not set, OAuth flow required")
        return None


def run_oauth_flow(client_id: str, client_secret: str, credentials_path: str = "credentials.json") -> Optional[Credentials]:
    """
    Run OAuth 2.0 flow to get credentials
    
    Args:
        client_id: OAuth client ID
        client_secret: OAuth client secret
        credentials_path: Path to save credentials
        
    Returns:
        Credentials object or None
    """
    if not HAS_GOOGLE_AUTH:
        logger.error("google-auth-oauthlib package not installed")
        return None
    
    try:
        # Create OAuth client config
        client_config = {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost"]
            }
        }
        
        # Save to file temporarily
        with open(credentials_path, 'w') as f:
            json.dump(client_config, f)
        
        # Run OAuth flow
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        creds = flow.run_local_server(port=0)
        
        # Clean up
        if os.path.exists(credentials_path):
            os.remove(credentials_path)
        
        logger.info("OAuth flow completed successfully")
        return creds
    except Exception as e:
        logger.error(f"OAuth flow error: {e}")
        return None


def save_refresh_token(creds: Credentials, env_file: str = ".env") -> bool:
    """
    Save refresh token to .env file
    
    Args:
        creds: Credentials object
        env_file: Path to .env file
        
    Returns:
        True if successful, False otherwise
    """
    if not creds or not creds.refresh_token:
        logger.warning("No refresh token to save")
        return False
    
    try:
        # Read existing .env file
        env_path = Path(env_file)
        if env_path.exists():
            content = env_path.read_text()
        else:
            content = ""
        
        # Update or add GOOGLE_DRIVE_REFRESH_TOKEN
        if "GOOGLE_DRIVE_REFRESH_TOKEN" in content:
            # Update existing
            lines = content.split('\n')
            updated_lines = []
            for line in lines:
                if line.startswith("GOOGLE_DRIVE_REFRESH_TOKEN"):
                    updated_lines.append(f"GOOGLE_DRIVE_REFRESH_TOKEN={creds.refresh_token}")
                else:
                    updated_lines.append(line)
            content = '\n'.join(updated_lines)
        else:
            # Add new
            if content and not content.endswith('\n'):
                content += '\n'
            content += f"GOOGLE_DRIVE_REFRESH_TOKEN={creds.refresh_token}\n"
        
        # Write back
        env_path.write_text(content)
        logger.info(f"Refresh token saved to {env_file}")
        return True
    except Exception as e:
        logger.error(f"Error saving refresh token: {e}")
        return False

