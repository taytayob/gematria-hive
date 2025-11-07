"""
Author Indexing Agent
Purpose: Index and track authors across platforms
- Extract author info from sources (Twitter, GitHub, YouTube, etc.)
- Create/update author records
- Track subjects/topics per author
- Index account metadata (followers, bio, etc.)
- Link sources to authors
- Update last_seen_at timestamps

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime
from urllib.parse import urlparse

from agents.orchestrator import AgentState
from core.data_table import DataTable

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


class AuthorIndexerAgent(DataTable):
    """
    Author Indexing Agent - Tracks authors across platforms
    """
    
    def __init__(self):
        """Initialize author indexer agent"""
        super().__init__('authors')
        self.name = "author_indexer_agent"
        logger.info(f"Initialized {self.name}")
    
    def detect_platform(self, url: str) -> str:
        """
        Detect platform from URL.
        
        Args:
            url: URL to detect platform from
            
        Returns:
            Platform name: 'twitter', 'x', 'github', 'youtube', etc.
        """
        if not url:
            return 'unknown'
        
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Twitter/X
        if 'twitter.com' in domain or 'x.com' in domain:
            return 'twitter' if 'twitter.com' in domain else 'x'
        
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
        if 'medium.com' in domain:
            return 'medium'
        if 'substack.com' in domain:
            return 'substack'
        
        # Default
        return 'unknown'
    
    def extract_username(self, url: str, platform: str) -> Optional[str]:
        """
        Extract username from URL.
        
        Args:
            url: URL to extract username from
            platform: Platform name
            
        Returns:
            Username or None
        """
        try:
            parsed = urlparse(url)
            path_parts = parsed.path.strip('/').split('/')
            
            if not path_parts:
                return None
            
            # Platform-specific extraction
            if platform in ['twitter', 'x']:
                # https://twitter.com/username/status/123
                if len(path_parts) > 0:
                    return path_parts[0]
            
            elif platform == 'github':
                # https://github.com/username
                if len(path_parts) > 0:
                    return path_parts[0]
            
            elif platform == 'youtube':
                # https://youtube.com/@username or https://youtube.com/c/username
                if len(path_parts) > 0:
                    if path_parts[0].startswith('@'):
                        return path_parts[0][1:]
                    elif path_parts[0] == 'c' and len(path_parts) > 1:
                        return path_parts[1]
                    else:
                        return path_parts[0]
            
            elif platform == 'reddit':
                # https://reddit.com/user/username
                if len(path_parts) > 1 and path_parts[0] == 'user':
                    return path_parts[1]
                elif len(path_parts) > 0:
                    return path_parts[0]
            
            elif platform in ['medium', 'substack']:
                # https://medium.com/@username or https://username.substack.com
                if len(path_parts) > 0:
                    if path_parts[0].startswith('@'):
                        return path_parts[0][1:]
                    else:
                        return path_parts[0]
            
            # Default: first path part
            if len(path_parts) > 0:
                return path_parts[0]
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting username from {url}: {e}")
            return None
    
    def extract_author_from_source(self, source: Dict) -> Optional[Dict]:
        """
        Extract author information from source data.
        
        Args:
            source: Source dictionary with extracted data
            
        Returns:
            Author dictionary or None
        """
        if not source:
            return None
        
        # Check extracted_data for author info
        extracted_data = source.get('extracted_data', {})
        if isinstance(extracted_data, dict):
            author_info = extracted_data.get('author')
            if author_info:
                return author_info
        
        # Check metadata for author info
        metadata = source.get('metadata', {})
        if isinstance(metadata, dict):
            author_info = metadata.get('author')
            if author_info:
                return author_info
        
        # Try to extract from URL
        url = source.get('url', '')
        if url:
            platform = self.detect_platform(url)
            username = self.extract_username(url, platform)
            
            if username:
                return {
                    'username': username,
                    'platform': platform,
                    'profile_url': url
                }
        
        return None
    
    def find_or_create_author(self, author_info: Dict) -> Optional[str]:
        """
        Find existing author or create new one.
        
        Args:
            author_info: Author information dictionary
            
        Returns:
            Author ID or None
        """
        if not author_info:
            return None
        
        username = author_info.get('username')
        platform = author_info.get('platform')
        
        if not username or not platform:
            logger.warning("Missing username or platform in author info")
            return None
        
        # Try to find existing author
        try:
            result = self.supabase.table('authors')\
                .select('id')\
                .eq('username', username)\
                .eq('platform', platform)\
                .limit(1)\
                .execute()
            
            if result.data:
                author_id = result.data[0]['id']
                
                # Update last_seen_at and other fields
                update_data = {
                    'last_seen_at': datetime.utcnow().isoformat()
                }
                
                # Update fields if provided
                if 'display_name' in author_info:
                    update_data['display_name'] = author_info['display_name']
                if 'bio' in author_info:
                    update_data['bio'] = author_info['bio']
                if 'profile_url' in author_info:
                    update_data['profile_url'] = author_info['profile_url']
                if 'avatar_url' in author_info:
                    update_data['avatar_url'] = author_info['avatar_url']
                if 'verified' in author_info:
                    update_data['verified'] = author_info['verified']
                if 'follower_count' in author_info:
                    update_data['follower_count'] = author_info['follower_count']
                if 'following_count' in author_info:
                    update_data['following_count'] = author_info['following_count']
                
                # Update subject tags
                if 'subject_tags' in author_info:
                    # Merge with existing tags
                    existing = self.read(author_id)
                    if existing and existing.get('subject_tags'):
                        existing_tags = set(existing['subject_tags'])
                        new_tags = set(author_info['subject_tags'])
                        update_data['subject_tags'] = list(existing_tags.union(new_tags))
                    else:
                        update_data['subject_tags'] = author_info['subject_tags']
                
                self.update(author_id, update_data)
                logger.info(f"Updated existing author: {username} on {platform}")
                return author_id
        except Exception as e:
            logger.warning(f"Error finding author: {e}")
        
        # Create new author
        author_data = {
            'username': username,
            'platform': platform,
            'display_name': author_info.get('display_name', ''),
            'bio': author_info.get('bio', ''),
            'profile_url': author_info.get('profile_url', ''),
            'avatar_url': author_info.get('avatar_url', ''),
            'verified': author_info.get('verified', False),
            'follower_count': author_info.get('follower_count'),
            'following_count': author_info.get('following_count'),
            'subject_tags': author_info.get('subject_tags', []),
            'account_indexed_at': datetime.utcnow().isoformat(),
            'last_seen_at': datetime.utcnow().isoformat()
        }
        
        result = self.create(author_data)
        if result:
            author_id = result['id']
            logger.info(f"Created new author: {username} on {platform}")
            return author_id
        
        return None
    
    def link_source_to_author(self, source_id: str, author_id: str):
        """
        Link source to author.
        
        Args:
            source_id: Source ID
            author_id: Author ID
        """
        if not self.supabase:
            return
        
        try:
            self.supabase.table('sources')\
                .update({'author_id': author_id})\
                .eq('id', source_id)\
                .execute()
            
            logger.info(f"Linked source {source_id} to author {author_id}")
        except Exception as e:
            logger.error(f"Error linking source to author: {e}")
    
    def extract_subject_tags(self, source: Dict) -> List[str]:
        """
        Extract subject tags from source content.
        
        Args:
            source: Source dictionary
            
        Returns:
            List of subject tags
        """
        tags = []
        
        # Get tags from source
        source_tags = source.get('tags', [])
        if isinstance(source_tags, list):
            tags.extend(source_tags)
        
        # Extract from content (simple keyword extraction)
        content = source.get('content', '') or source.get('title', '')
        if content:
            # Simple keyword extraction (can be enhanced with NLP)
            keywords = ['gematria', 'numerology', 'sacred geometry', 'kabbalah', 
                        'hermetic', 'esoteric', 'occult', 'quantum', 'physics',
                        'mathematics', 'philosophy', 'religion', 'spirituality']
            
            content_lower = content.lower()
            for keyword in keywords:
                if keyword in content_lower:
                    tags.append(keyword)
        
        return list(set(tags))  # Remove duplicates
    
    def validate(self, data: Dict, record_id: Optional[str] = None) -> Dict:
        """Validate author data."""
        errors = []
        
        # Required fields
        if 'username' not in data or not data['username']:
            errors.append("username is required")
        
        if 'platform' not in data or not data['platform']:
            errors.append("platform is required")
        
        # Check uniqueness
        if not record_id:  # Only check on create
            if self.supabase:
                try:
                    existing = self.supabase.table(self.table_name)\
                        .select('id')\
                        .eq('username', data['username'])\
                        .eq('platform', data['platform'])\
                        .execute()
                    if existing.data:
                        errors.append(f"Author {data['username']} on {data['platform']} already exists")
                except Exception as e:
                    logger.warning(f"Could not check uniqueness: {e}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute author indexing task.
        
        Args:
            state: Agent state with source data
            
        Returns:
            Updated state with author information
        """
        data = state.get("data", [])
        
        if not data:
            logger.warning("No data provided for author indexing")
            return state
        
        logger.info(f"Author indexer agent: Processing {len(data)} sources")
        
        try:
            indexed_authors = []
            
            for source in data:
                if not isinstance(source, dict):
                    continue
                
                # Extract author info from source
                author_info = self.extract_author_from_source(source)
                
                if not author_info:
                    logger.warning(f"No author info found in source: {source.get('url', 'unknown')}")
                    continue
                
                # Extract subject tags
                subject_tags = self.extract_subject_tags(source)
                if subject_tags:
                    author_info['subject_tags'] = subject_tags
                
                # Find or create author
                author_id = self.find_or_create_author(author_info)
                
                if author_id:
                    indexed_authors.append({
                        'author_id': author_id,
                        'author_info': author_info
                    })
                    
                    # Link source to author if source has ID
                    source_id = source.get('id')
                    if source_id:
                        self.link_source_to_author(source_id, author_id)
            
            # Update state
            state["context"]["indexed_authors"] = indexed_authors
            state["context"]["author_count"] = len(indexed_authors)
            state["results"].append({
                "agent": self.name,
                "action": "index_authors",
                "count": len(indexed_authors),
                "authors": indexed_authors
            })
            
            logger.info(f"Author indexing complete: {len(indexed_authors)} authors indexed")
            
        except Exception as e:
            logger.error(f"Author indexing error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

