"""
Bookmark Ingestion Agent
Purpose: Process JSON and markdown bookmark files
- Parse JSON bookmark files (Dewey, OneTab, browser exports)
- Parse markdown files with links
- Extract URLs, titles, descriptions, tags
- Normalize data format
- Route to appropriate processors (Twitter, articles, videos, etc.)

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import json
import logging
import re
from typing import Dict, List, Optional
from datetime import datetime
from urllib.parse import urlparse

from agents.orchestrator import AgentState

# Load environment variables
from dotenv import load_dotenv
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

logger = logging.getLogger(__name__)


class BookmarkIngestionAgent:
    """
    Bookmark Ingestion Agent - Processes JSON and markdown bookmark files
    """
    
    def __init__(self):
        """Initialize bookmark ingestion agent"""
        self.name = "bookmark_ingestion_agent"
        self.supabase = supabase if HAS_SUPABASE else None
        logger.info(f"Initialized {self.name}")
    
    def detect_url_type(self, url: str) -> str:
        """
        Detect URL type for routing to appropriate processor.
        
        Args:
            url: URL to detect
            
        Returns:
            URL type: 'twitter', 'x', 'github', 'youtube', 'article', 'video', 'image', etc.
        """
        if not url:
            return 'unknown'
        
        url_lower = url.lower()
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Twitter/X
        if 'twitter.com' in domain or 'x.com' in domain:
            return 'twitter'
        
        # GitHub
        if 'github.com' in domain:
            return 'github'
        
        # YouTube
        if 'youtube.com' in domain or 'youtu.be' in domain:
            return 'youtube'
        
        # Reddit
        if 'reddit.com' in domain:
            return 'reddit'
        
        # Medium/Substack
        if 'medium.com' in domain or 'substack.com' in domain:
            return 'article'
        
        # Image files
        if any(url_lower.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']):
            return 'image'
        
        # Video files
        if any(url_lower.endswith(ext) for ext in ['.mp4', '.avi', '.mov', '.webm', '.mkv']):
            return 'video'
        
        # PDF files
        if url_lower.endswith('.pdf'):
            return 'pdf'
        
        # Default to article
        return 'article'
    
    def parse_json_bookmarks(self, file_path: str) -> List[Dict]:
        """
        Parse JSON bookmark file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            List of bookmark dictionaries
        """
        bookmarks = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different JSON formats
            if isinstance(data, list):
                # Direct list of bookmarks
                bookmarks = data
            elif isinstance(data, dict):
                # Check for common bookmark export formats
                if 'bookmarks' in data:
                    bookmarks = data['bookmarks']
                elif 'items' in data:
                    bookmarks = data['items']
                elif 'links' in data:
                    bookmarks = data['links']
                else:
                    # Try to extract URLs from dict
                    bookmarks = [data]
            
            # Normalize bookmark format
            normalized = []
            for item in bookmarks:
                normalized_item = self.normalize_bookmark(item)
                if normalized_item:
                    normalized.append(normalized_item)
            
            logger.info(f"Parsed {len(normalized)} bookmarks from {file_path}")
            return normalized
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {file_path}: {e}")
            return []
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return []
        except Exception as e:
            logger.error(f"Error parsing JSON file {file_path}: {e}")
            return []
    
    def parse_markdown_bookmarks(self, file_path: str) -> List[Dict]:
        """
        Parse markdown file with links.
        
        Args:
            file_path: Path to markdown file
            
        Returns:
            List of bookmark dictionaries
        """
        bookmarks = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract markdown links: [text](url)
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            matches = re.findall(link_pattern, content)
            
            for text, url in matches:
                bookmark = {
                    'url': url,
                    'title': text,
                    'description': '',
                    'tags': [],
                    'source': 'markdown'
                }
                bookmarks.append(bookmark)
            
            # Also extract plain URLs
            url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
            urls = re.findall(url_pattern, content)
            
            for url in urls:
                # Skip if already in bookmarks
                if not any(b['url'] == url for b in bookmarks):
                    bookmark = {
                        'url': url,
                        'title': '',
                        'description': '',
                        'tags': [],
                        'source': 'markdown'
                    }
                    bookmarks.append(bookmark)
            
            logger.info(f"Parsed {len(bookmarks)} bookmarks from {file_path}")
            return bookmarks
            
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return []
        except Exception as e:
            logger.error(f"Error parsing markdown file {file_path}: {e}")
            return []
    
    def normalize_bookmark(self, item: Dict) -> Optional[Dict]:
        """
        Normalize bookmark to standard format.
        
        Args:
            item: Raw bookmark item
            
        Returns:
            Normalized bookmark dictionary or None
        """
        if not isinstance(item, dict):
            return None
        
        # Extract URL
        url = item.get('url') or item.get('link') or item.get('href') or item.get('uri')
        if not url:
            return None
        
        # Extract title
        title = item.get('title') or item.get('name') or item.get('text') or ''
        
        # Extract description/summary
        description = item.get('description') or item.get('summary') or item.get('note') or ''
        
        # Extract tags
        tags = item.get('tags') or item.get('tag') or []
        if isinstance(tags, str):
            tags = [tags]
        if not isinstance(tags, list):
            tags = []
        
        # Detect URL type
        url_type = self.detect_url_type(url)
        
        # Normalized bookmark
        normalized = {
            'url': url,
            'title': title,
            'description': description,
            'tags': tags,
            'source_type': url_type,
            'source': item.get('source', 'json'),
            'metadata': {
                'original_item': item,
                'parsed_at': datetime.utcnow().isoformat()
            }
        }
        
        return normalized
    
    def store_bookmarks(self, bookmarks: List[Dict]) -> int:
        """
        Store bookmarks in database.
        
        Args:
            bookmarks: List of normalized bookmarks
            
        Returns:
            Number of successfully stored bookmarks
        """
        if not self.supabase:
            logger.warning("Supabase not available, bookmarks not stored")
            return 0
        
        if not bookmarks:
            return 0
        
        stored_count = 0
        
        # Prepare data for insertion
        insert_data = []
        for bookmark in bookmarks:
            insert_item = {
                'url': bookmark['url'],
                'source_type': bookmark.get('source_type', 'bookmark'),
                'title': bookmark.get('title', ''),
                'content': bookmark.get('description', ''),
                'tags': bookmark.get('tags', []),
                'metadata': bookmark.get('metadata', {}),
                'ingested_at': datetime.utcnow().isoformat()
            }
            insert_data.append(insert_item)
        
        # Insert in batches
        batch_size = 50
        for i in range(0, len(insert_data), batch_size):
            batch = insert_data[i:i+batch_size]
            try:
                result = self.supabase.table('sources').insert(batch).execute()
                if result.data:
                    stored_count += len(result.data)
                    logger.info(f"Stored batch of {len(batch)} bookmarks")
            except Exception as e:
                logger.error(f"Error inserting bookmark batch: {e}")
                # Try individual inserts as fallback
                for item in batch:
                    try:
                        result = self.supabase.table('sources').insert(item).execute()
                        if result.data:
                            stored_count += 1
                    except Exception as e2:
                        logger.error(f"Error inserting individual bookmark: {e2}")
        
        logger.info(f"Stored {stored_count}/{len(bookmarks)} bookmarks")
        return stored_count
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute bookmark ingestion task.
        
        Args:
            state: Agent state with task information
            
        Returns:
            Updated state with ingested bookmarks
        """
        task = state.get("task", {})
        source = task.get("source", "")
        
        if not source:
            logger.error("No source provided for bookmark ingestion")
            state["status"] = "failed"
            state["error"] = "No source provided"
            return state
        
        logger.info(f"Bookmark ingestion agent: Processing {source}")
        
        try:
            bookmarks = []
            
            # Detect file type and parse accordingly
            if source.endswith('.json'):
                bookmarks = self.parse_json_bookmarks(source)
            elif source.endswith('.md') or source.endswith('.markdown'):
                bookmarks = self.parse_markdown_bookmarks(source)
            else:
                logger.warning(f"Unknown file type: {source}")
                state["status"] = "failed"
                state["error"] = f"Unknown file type: {source}"
                return state
            
            if not bookmarks:
                logger.warning(f"No bookmarks found in {source}")
                state["status"] = "failed"
                state["error"] = "No bookmarks found"
                return state
            
            # Store bookmarks
            stored_count = self.store_bookmarks(bookmarks)
            
            # Update state
            state["data"] = bookmarks
            state["context"]["bookmark_count"] = len(bookmarks)
            state["context"]["stored_count"] = stored_count
            state["context"]["source_file"] = source
            state["results"].append({
                "agent": self.name,
                "action": "ingest_bookmarks",
                "count": stored_count,
                "total": len(bookmarks),
                "source": source
            })
            
            logger.info(f"Bookmark ingestion complete: {stored_count}/{len(bookmarks)} bookmarks stored")
            
        except Exception as e:
            logger.error(f"Bookmark ingestion error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

