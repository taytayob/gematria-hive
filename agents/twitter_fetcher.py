"""
Twitter/X Thread Fetcher Agent
Purpose: Fetch full Twitter/X threads using Grok API
- Detect Twitter/X URLs in bookmarks
- Use Grok API to fetch full thread context
- Extract author information
- Parse thread structure (replies, quotes, media)
- Extract all text, images, links from thread
- Handle rate limiting and caching

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import json
import logging
import time
import requests
from typing import Dict, List, Optional
from datetime import datetime
from urllib.parse import urlparse, parse_qs

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

# Grok API configuration
GROK_API_KEY = os.getenv('GROK_API_KEY')
if not GROK_API_KEY:
    logger.warning("GROK_API_KEY not set - Twitter fetcher will be limited")
GROK_API_URL = 'https://api.x.ai/v1/chat/completions'
GROK_MODEL = 'grok-beta'


class TwitterFetcherAgent:
    """
    Twitter/X Thread Fetcher Agent - Fetches full threads using Grok API
    """
    
    def __init__(self):
        """Initialize Twitter fetcher agent"""
        self.name = "twitter_fetcher_agent"
        self.api_key = GROK_API_KEY
        self.api_url = GROK_API_URL
        self.model = GROK_MODEL
        self.supabase = supabase if HAS_SUPABASE else None
        self.rate_limit_delay = 1.0  # Delay between requests (seconds)
        self.last_request_time = 0
        
        if not self.api_key:
            logger.warning(f"{self.name}: GROK_API_KEY not set - Twitter fetching will be disabled")
        else:
            logger.info(f"Initialized {self.name}")
    
    def extract_tweet_id(self, url: str) -> Optional[str]:
        """
        Extract tweet ID from Twitter/X URL.
        
        Args:
            url: Twitter/X URL
            
        Returns:
            Tweet ID or None
        """
        try:
            parsed = urlparse(url)
            path_parts = parsed.path.strip('/').split('/')
            
            # Twitter/X URL formats:
            # https://twitter.com/username/status/1234567890
            # https://x.com/username/status/1234567890
            # https://twitter.com/i/web/status/1234567890
            
            if 'status' in path_parts:
                status_index = path_parts.index('status')
                if status_index + 1 < len(path_parts):
                    tweet_id = path_parts[status_index + 1]
                    # Remove query parameters if any
                    tweet_id = tweet_id.split('?')[0]
                    return tweet_id
            
            return None
        except Exception as e:
            logger.error(f"Error extracting tweet ID from {url}: {e}")
            return None
    
    def check_cache(self, tweet_id: str) -> Optional[Dict]:
        """
        Check cache for thread data.
        
        Args:
            tweet_id: Tweet ID
            
        Returns:
            Cached thread data or None
        """
        if not self.supabase:
            return None
        
        try:
            cache_key = f"twitter_thread_{tweet_id}"
            result = self.supabase.table('cache_logs')\
                .select('*')\
                .eq('cache_key', cache_key)\
                .gt('expires_at', datetime.utcnow().isoformat())\
                .limit(1)\
                .execute()
            
            if result.data:
                cached_data = result.data[0].get('cached_data', {})
                logger.info(f"Found cached thread data for tweet {tweet_id}")
                return cached_data
            
            return None
        except Exception as e:
            logger.warning(f"Error checking cache: {e}")
            return None
    
    def save_cache(self, tweet_id: str, thread_data: Dict, ttl_hours: int = 24):
        """
        Save thread data to cache.
        
        Args:
            tweet_id: Tweet ID
            thread_data: Thread data to cache
            ttl_hours: Time to live in hours
        """
        if not self.supabase:
            return
        
        try:
            cache_key = f"twitter_thread_{tweet_id}"
            expires_at = datetime.utcnow().timestamp() + (ttl_hours * 3600)
            
            self.supabase.table('cache_logs').upsert({
                'cache_key': cache_key,
                'cache_type': 'api_response',
                'cached_data': thread_data,
                'expires_at': datetime.fromtimestamp(expires_at).isoformat()
            }).execute()
            
            logger.info(f"Cached thread data for tweet {tweet_id}")
        except Exception as e:
            logger.warning(f"Error saving cache: {e}")
    
    def rate_limit(self):
        """Apply rate limiting."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def fetch_thread_via_grok(self, tweet_url: str) -> Optional[Dict]:
        """
        Fetch full thread using Grok API.
        
        Args:
            tweet_url: Twitter/X URL
            
        Returns:
            Thread data or None
        """
        if not self.api_key:
            logger.error("GROK_API_KEY not set - cannot fetch thread")
            return None
        
        tweet_id = self.extract_tweet_id(tweet_url)
        if not tweet_id:
            logger.error(f"Could not extract tweet ID from {tweet_url}")
            return None
        
        # Check cache first
        cached_data = self.check_cache(tweet_id)
        if cached_data:
            return cached_data
        
        # Apply rate limiting
        self.rate_limit()
        
        # Prepare Grok API request
        prompt = f"""Fetch the full thread for this tweet URL: {tweet_url}

Please provide:
1. The original tweet content
2. All replies in the thread
3. Author information (username, display name, bio, follower count)
4. All images and media URLs
5. All links mentioned in the thread
6. Thread structure (which tweets are replies to which)
7. Any quotes or retweets
8. Timestamps for each tweet

Format the response as JSON with the following structure:
{{
  "tweet_id": "...",
  "author": {{
    "username": "...",
    "display_name": "...",
    "bio": "...",
    "follower_count": ...,
    "verified": true/false
  }},
  "original_tweet": {{
    "text": "...",
    "timestamp": "...",
    "images": [...],
    "links": [...]
  }},
  "replies": [
    {{
      "tweet_id": "...",
      "text": "...",
      "timestamp": "...",
      "author": {...},
      "images": [...],
      "links": [...]
    }}
  ],
  "thread_structure": {...}
}}"""

        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': self.model,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'temperature': 0.1,
                'max_tokens': 4000
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract thread data from Grok response
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                
                # Try to parse JSON from response
                try:
                    # Extract JSON from markdown code blocks if present
                    if '```json' in content:
                        json_start = content.find('```json') + 7
                        json_end = content.find('```', json_start)
                        content = content[json_start:json_end].strip()
                    elif '```' in content:
                        json_start = content.find('```') + 3
                        json_end = content.find('```', json_start)
                        content = content[json_start:json_end].strip()
                    
                    thread_data = json.loads(content)
                    thread_data['tweet_id'] = tweet_id
                    thread_data['tweet_url'] = tweet_url
                    thread_data['fetched_at'] = datetime.utcnow().isoformat()
                    
                    # Save to cache
                    self.save_cache(tweet_id, thread_data)
                    
                    logger.info(f"Fetched thread data for tweet {tweet_id}")
                    return thread_data
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Could not parse JSON from Grok response: {e}")
                    logger.debug(f"Response content: {content[:500]}")
                    return None
            else:
                logger.error(f"Unexpected Grok API response format: {result}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching thread via Grok API: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching thread: {e}")
            return None
    
    def extract_author_info(self, thread_data: Dict) -> Optional[Dict]:
        """
        Extract author information from thread data.
        
        Args:
            thread_data: Thread data from Grok API
            
        Returns:
            Author information dictionary
        """
        if 'author' in thread_data:
            return thread_data['author']
        elif 'original_tweet' in thread_data and 'author' in thread_data['original_tweet']:
            return thread_data['original_tweet']['author']
        return None
    
    def extract_thread_content(self, thread_data: Dict) -> Dict:
        """
        Extract all content from thread.
        
        Args:
            thread_data: Thread data from Grok API
            
        Returns:
            Dictionary with extracted content
        """
        content = {
            'text': '',
            'images': [],
            'links': [],
            'replies': []
        }
        
        # Extract original tweet content
        if 'original_tweet' in thread_data:
            original = thread_data['original_tweet']
            content['text'] = original.get('text', '')
            content['images'].extend(original.get('images', []))
            content['links'].extend(original.get('links', []))
        
        # Extract replies content
        if 'replies' in thread_data:
            for reply in thread_data['replies']:
                reply_content = {
                    'text': reply.get('text', ''),
                    'images': reply.get('images', []),
                    'links': reply.get('links', [])
                }
                content['replies'].append(reply_content)
                content['images'].extend(reply_content['images'])
                content['links'].extend(reply_content['links'])
        
        # Remove duplicates
        content['images'] = list(set(content['images']))
        content['links'] = list(set(content['links']))
        
        return content
    
    def store_thread_data(self, thread_data: Dict) -> Optional[str]:
        """
        Store thread data in database.
        
        Args:
            thread_data: Thread data from Grok API
            
        Returns:
            Source ID or None
        """
        if not self.supabase:
            return None
        
        try:
            tweet_id = thread_data.get('tweet_id')
            tweet_url = thread_data.get('tweet_url')
            
            if not tweet_id or not tweet_url:
                logger.error("Missing tweet_id or tweet_url in thread data")
                return None
            
            # Extract author info
            author_info = self.extract_author_info(thread_data)
            
            # Extract content
            content = self.extract_thread_content(thread_data)
            
            # Store as source
            source_data = {
                'url': tweet_url,
                'source_type': 'thread',
                'title': f"Twitter Thread: {tweet_id}",
                'content': content['text'],
                'extracted_data': {
                    'thread_data': thread_data,
                    'content': content,
                    'author': author_info
                },
                'metadata': {
                    'tweet_id': tweet_id,
                    'images': content['images'],
                    'links': content['links'],
                    'reply_count': len(content['replies']),
                    'fetched_at': thread_data.get('fetched_at')
                },
                'ingested_at': datetime.utcnow().isoformat()
            }
            
            result = self.supabase.table('sources').upsert(source_data, on_conflict='url').execute()
            
            if result.data:
                source_id = result.data[0]['id']
                logger.info(f"Stored thread data for tweet {tweet_id}")
                return source_id
            else:
                logger.error("Failed to store thread data")
                return None
                
        except Exception as e:
            logger.error(f"Error storing thread data: {e}")
            return None
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute Twitter thread fetching task.
        
        Args:
            state: Agent state with task information
            
        Returns:
            Updated state with thread data
        """
        task = state.get("task", {})
        url = task.get("url", "")
        
        if not url:
            # Try to get URL from data
            data = state.get("data", [])
            if data and isinstance(data, list) and len(data) > 0:
                url = data[0].get('url', '')
        
        if not url:
            logger.error("No URL provided for Twitter fetching")
            state["status"] = "failed"
            state["error"] = "No URL provided"
            return state
        
        logger.info(f"Twitter fetcher agent: Fetching thread from {url}")
        
        try:
            # Fetch thread via Grok API
            thread_data = self.fetch_thread_via_grok(url)
            
            if not thread_data:
                logger.error(f"Failed to fetch thread data for {url}")
                state["status"] = "failed"
                state["error"] = "Failed to fetch thread data"
                return state
            
            # Store thread data
            source_id = self.store_thread_data(thread_data)
            
            # Update state
            state["data"] = [thread_data]
            state["context"]["thread_data"] = thread_data
            state["context"]["source_id"] = source_id
            state["context"]["tweet_id"] = thread_data.get('tweet_id')
            state["results"].append({
                "agent": self.name,
                "action": "fetch_thread",
                "url": url,
                "tweet_id": thread_data.get('tweet_id'),
                "source_id": source_id
            })
            
            logger.info(f"Twitter thread fetching complete: {thread_data.get('tweet_id')}")
            
        except Exception as e:
            logger.error(f"Twitter fetching error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

