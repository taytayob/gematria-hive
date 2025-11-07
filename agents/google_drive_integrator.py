"""
Google Drive Integrator Agent

Purpose: Integrate Google Drive API for file access and bookmark extraction
- Access Google Drive files and folders
- Extract bookmarks and links from Drive documents
- Integrate with bookmark ingestion pipeline
- Support OAuth 2.0 authentication

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
import json
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv

from agents.orchestrator import AgentState

# Load environment variables
load_dotenv()

# Google Drive API integration
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    HAS_GOOGLE_DRIVE = True
except ImportError:
    HAS_GOOGLE_DRIVE = False
    print("Warning: google-api-python-client package not installed, Google Drive API disabled")

logger = logging.getLogger(__name__)

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


class GoogleDriveIntegratorAgent:
    """
    Google Drive Integrator Agent - Drive file access and bookmark extraction
    
    Operations:
    - Access Google Drive files and folders
    - Extract bookmarks and links from Drive documents
    - Integrate with bookmark ingestion pipeline
    - Support OAuth 2.0 authentication
    """
    
    def __init__(self):
        """Initialize Google Drive Integrator agent"""
        self.name = "google_drive_integrator"
        self.service = None
        self.credentials = None
        
        # Initialize Google Drive API
        client_id = os.getenv('GOOGLE_DRIVE_CLIENT_ID')
        client_secret = os.getenv('GOOGLE_DRIVE_CLIENT_SECRET')
        refresh_token = os.getenv('GOOGLE_DRIVE_REFRESH_TOKEN')
        
        if client_id and client_secret and HAS_GOOGLE_DRIVE:
            try:
                self.credentials = self._get_credentials(
                    client_id, client_secret, refresh_token
                )
                if self.credentials:
                    self.service = build('drive', 'v3', credentials=self.credentials)
                    logger.info(f"Initialized {self.name} with Google Drive API")
                else:
                    logger.warning("Google Drive credentials not available")
            except Exception as e:
                logger.error(f"Failed to initialize Google Drive API: {e}")
                self.service = None
        else:
            if not client_id or not client_secret:
                logger.warning("GOOGLE_DRIVE_CLIENT_ID or GOOGLE_DRIVE_CLIENT_SECRET not set, Google Drive agent disabled")
            if not HAS_GOOGLE_DRIVE:
                logger.warning("google-api-python-client package not installed, Google Drive agent disabled")
    
    def _get_credentials(self, client_id: str, client_secret: str, refresh_token: Optional[str] = None) -> Optional[Credentials]:
        """
        Get Google Drive API credentials
        
        Args:
            client_id: OAuth client ID
            client_secret: OAuth client secret
            refresh_token: Optional refresh token
            
        Returns:
            Credentials object or None
        """
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
            # Need to run OAuth flow
            logger.warning("No refresh token provided, OAuth flow required")
            return None
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute Google Drive integration task
        
        Args:
            state: Agent state with task information
            
        Returns:
            Updated state with Drive file data
        """
        if not self.service:
            logger.warning("Google Drive API not configured, skipping Drive integration")
            return state
        
        task = state.get("task", {})
        drive_query = task.get("drive_query", "")
        folder_id = task.get("folder_id", "")
        file_id = task.get("file_id", "")
        
        logger.info(f"Google Drive Integrator: Processing query={drive_query}, folder_id={folder_id}, file_id={file_id}")
        
        try:
            extracted_data = []
            
            if file_id:
                # Extract from specific file
                file_data = self._extract_from_file(file_id)
                if file_data:
                    extracted_data.append(file_data)
            elif folder_id:
                # Extract from folder
                folder_data = self._extract_from_folder(folder_id)
                extracted_data.extend(folder_data)
            elif drive_query:
                # Search Drive
                search_data = self._search_drive(drive_query)
                extracted_data.extend(search_data)
            else:
                # Default: search for bookmark files
                search_data = self._search_drive("name contains 'bookmark' or name contains 'link'")
                extracted_data.extend(search_data)
            
            # Add to state data
            existing_data = state.get("data", [])
            state["data"] = existing_data + extracted_data
            
            # Update context
            state["context"]["google_drive_files_processed"] = len(extracted_data)
            state["context"]["google_drive_completed"] = True
            
            # Add results
            state["results"].append({
                "agent": self.name,
                "action": "drive_extraction",
                "files_processed": len(extracted_data),
                "query": drive_query or folder_id or file_id
            })
            
            logger.info(f"Google Drive extraction complete: {len(extracted_data)} files processed")
            
        except Exception as e:
            logger.error(f"Google Drive integration error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state
    
    def _extract_from_file(self, file_id: str) -> Optional[Dict]:
        """
        Extract data from a specific Drive file
        
        Args:
            file_id: Google Drive file ID
            
        Returns:
            Extracted data dictionary or None
        """
        try:
            # Get file metadata
            file_metadata = self.service.files().get(fileId=file_id, fields='id,name,mimeType,webViewLink,createdTime,modifiedTime').execute()
            
            # Get file content
            file_content = ""
            if 'text/plain' in file_metadata.get('mimeType', '') or 'text/html' in file_metadata.get('mimeType', ''):
                request = self.service.files().get_media(fileId=file_id)
                file_content = request.execute().decode('utf-8')
            
            # Extract links/bookmarks from content
            links = self._extract_links(file_content)
            
            return {
                'file_id': file_id,
                'file_name': file_metadata.get('name', ''),
                'file_type': file_metadata.get('mimeType', ''),
                'file_url': file_metadata.get('webViewLink', ''),
                'content': file_content,
                'links': links,
                'created_time': file_metadata.get('createdTime', ''),
                'modified_time': file_metadata.get('modifiedTime', ''),
                'source': 'google_drive',
                'timestamp': datetime.utcnow().isoformat()
            }
        except HttpError as e:
            logger.error(f"Error extracting from file {file_id}: {e}")
            return None
    
    def _extract_from_folder(self, folder_id: str) -> List[Dict]:
        """
        Extract data from all files in a folder
        
        Args:
            folder_id: Google Drive folder ID
            
        Returns:
            List of extracted data dictionaries
        """
        extracted_data = []
        
        try:
            # List files in folder
            query = f"'{folder_id}' in parents and trashed=false"
            results = self.service.files().list(q=query, fields='files(id,name,mimeType)').execute()
            files = results.get('files', [])
            
            for file in files:
                file_data = self._extract_from_file(file['id'])
                if file_data:
                    extracted_data.append(file_data)
            
        except HttpError as e:
            logger.error(f"Error extracting from folder {folder_id}: {e}")
        
        return extracted_data
    
    def _search_drive(self, query: str) -> List[Dict]:
        """
        Search Google Drive for files
        
        Args:
            query: Search query
            
        Returns:
            List of extracted data dictionaries
        """
        extracted_data = []
        
        try:
            # Search Drive
            results = self.service.files().list(q=query, fields='files(id,name,mimeType)').execute()
            files = results.get('files', [])
            
            for file in files:
                file_data = self._extract_from_file(file['id'])
                if file_data:
                    extracted_data.append(file_data)
            
        except HttpError as e:
            logger.error(f"Error searching Drive: {e}")
        
        return extracted_data
    
    def _extract_links(self, content: str) -> List[str]:
        """
        Extract URLs/links from content
        
        Args:
            content: Text content to extract links from
            
        Returns:
            List of URLs
        """
        import re
        
        # Pattern for URLs
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, content)
        
        # Also look for markdown links
        markdown_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        markdown_links = re.findall(markdown_pattern, content)
        for _, url in markdown_links:
            if url.startswith('http'):
                urls.append(url)
        
        # Remove duplicates
        return list(set(urls))
    
    def list_files(self, folder_id: Optional[str] = None, query: Optional[str] = None) -> List[Dict]:
        """
        List files in Google Drive
        
        Args:
            folder_id: Optional folder ID to list files from
            query: Optional search query
            
        Returns:
            List of file metadata dictionaries
        """
        if not self.service:
            logger.error("Google Drive API not configured")
            return []
        
        try:
            if folder_id:
                query_str = f"'{folder_id}' in parents and trashed=false"
            elif query:
                query_str = query
            else:
                query_str = "trashed=false"
            
            results = self.service.files().list(q=query_str, fields='files(id,name,mimeType,webViewLink,createdTime,modifiedTime)').execute()
            return results.get('files', [])
        except HttpError as e:
            logger.error(f"Error listing files: {e}")
            return []

