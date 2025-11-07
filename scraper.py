"""
Base Web Scraper Module

Purpose: Base functionality for web scraping with:
- Sitemap discovery and parsing
- Recursive page crawling with depth limits
- Image extraction and storage
- Link discovery and queue management
- Rate limiting and respectful scraping

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import time
import logging
import requests
from typing import List, Dict, Set, Optional, Tuple
from urllib.parse import urljoin, urlparse, urlunparse
from datetime import datetime
from collections import deque
import re

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False
    print("Warning: beautifulsoup4 not installed, scraping disabled")

try:
    from urllib.robotparser import RobotFileParser
    HAS_ROBOTSPARSER = True
except ImportError:
    HAS_ROBOTSPARSER = False

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Logging setup
logging.basicConfig(
    filename='scraping_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)
logger = logging.getLogger()
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)


class BaseScraper:
    """
    Base web scraper with common functionality.
    """
    
    def __init__(
        self,
        base_url: str,
        max_depth: int = 3,
        delay: float = 1.0,
        respect_robots: bool = True,
        user_agent: str = "GematriaHive/1.0 (Educational Research)"
    ):
        """
        Initialize base scraper.
        
        Args:
            base_url: Base URL to start scraping from
            max_depth: Maximum depth for recursive crawling
            delay: Delay between requests (seconds)
            respect_robots: Whether to respect robots.txt
            user_agent: User agent string for requests
        """
        self.base_url = base_url.rstrip('/')
        self.max_depth = max_depth
        self.delay = delay
        self.respect_robots = respect_robots
        self.user_agent = user_agent
        
        self.visited_urls: Set[str] = set()
        self.url_queue: deque = deque()
        self.images: List[str] = []
        self.links: List[str] = []
        self.scraped_data: List[Dict] = []
        
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': user_agent})
        
        # Robots.txt parser
        self.robots_parser = None
        if respect_robots and HAS_ROBOTSPARSER:
            try:
                robots_url = urljoin(base_url, '/robots.txt')
                self.robots_parser = RobotFileParser()
                self.robots_parser.set_url(robots_url)
                self.robots_parser.read()
                logger.info(f"Loaded robots.txt from {robots_url}")
            except Exception as e:
                logger.warning(f"Could not load robots.txt: {e}")
        
        logger.info(f"Initialized scraper for {base_url}")
    
    def can_fetch(self, url: str) -> bool:
        """
        Check if URL can be fetched according to robots.txt.
        
        Args:
            url: URL to check
            
        Returns:
            True if URL can be fetched
        """
        if not self.respect_robots or not self.robots_parser:
            return True
        
        try:
            return self.robots_parser.can_fetch(self.user_agent, url)
        except Exception as e:
            logger.warning(f"Error checking robots.txt for {url}: {e}")
            return True
    
    def normalize_url(self, url: str, base: Optional[str] = None) -> str:
        """
        Normalize URL to absolute form.
        
        Args:
            url: URL to normalize
            base: Base URL for relative URLs
            
        Returns:
            Normalized absolute URL
        """
        if not base:
            base = self.base_url
        
        # Handle relative URLs
        if url.startswith('/'):
            url = urljoin(base, url)
        elif not url.startswith('http'):
            url = urljoin(base, url)
        
        # Remove fragments
        parsed = urlparse(url)
        normalized = urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            parsed.query,
            ''  # Remove fragment
        ))
        
        return normalized.rstrip('/')
    
    def is_same_domain(self, url: str) -> bool:
        """
        Check if URL is from the same domain as base URL.
        
        Args:
            url: URL to check
            
        Returns:
            True if same domain
        """
        try:
            base_domain = urlparse(self.base_url).netloc
            url_domain = urlparse(url).netloc
            return base_domain == url_domain
        except Exception:
            return False
    
    def fetch_page(self, url: str) -> Optional[requests.Response]:
        """
        Fetch a page with rate limiting and error handling.
        
        Args:
            url: URL to fetch
            
        Returns:
            Response object or None if failed
        """
        if url in self.visited_urls:
            return None
        
        if not self.can_fetch(url):
            logger.info(f"Skipping {url} (robots.txt disallows)")
            return None
        
        # Rate limiting
        time.sleep(self.delay)
        
        try:
            response = self.session.get(url, timeout=10, allow_redirects=True)
            response.raise_for_status()
            self.visited_urls.add(url)
            logger.info(f"Fetched {url} (status: {response.status_code})")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_links(self, html: str, base_url: str) -> List[str]:
        """
        Extract all links from HTML.
        
        Args:
            html: HTML content
            base_url: Base URL for resolving relative links
            
        Returns:
            List of absolute URLs
        """
        if not HAS_BS4:
            return []
        
        links = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            for tag in soup.find_all('a', href=True):
                href = tag['href']
                normalized = self.normalize_url(href, base_url)
                if normalized and normalized not in links:
                    links.append(normalized)
        except Exception as e:
            logger.error(f"Error extracting links: {e}")
        
        return links
    
    def extract_images(self, html: str, base_url: str) -> List[str]:
        """
        Extract all image URLs from HTML.
        
        Args:
            html: HTML content
            base_url: Base URL for resolving relative image URLs
            
        Returns:
            List of absolute image URLs
        """
        if not HAS_BS4:
            return []
        
        images = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            for tag in soup.find_all('img', src=True):
                src = tag['src']
                normalized = self.normalize_url(src, base_url)
                if normalized and normalized not in images:
                    images.append(normalized)
            
            # Also check CSS background images
            for tag in soup.find_all(style=True):
                style = tag.get('style', '')
                bg_image_match = re.search(r'background-image:\s*url\(["\']?([^"\']+)["\']?\)', style)
                if bg_image_match:
                    src = bg_image_match.group(1)
                    normalized = self.normalize_url(src, base_url)
                    if normalized and normalized not in images:
                        images.append(normalized)
        except Exception as e:
            logger.error(f"Error extracting images: {e}")
        
        return images
    
    def extract_text(self, html: str) -> str:
        """
        Extract text content from HTML.
        
        Args:
            html: HTML content
            
        Returns:
            Extracted text
        """
        if not HAS_BS4:
            return ""
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            return soup.get_text(separator=' ', strip=True)
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return ""
    
    def extract_title(self, html: str) -> str:
        """
        Extract page title from HTML.
        
        Args:
            html: HTML content
            
        Returns:
            Page title
        """
        if not HAS_BS4:
            return ""
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            title_tag = soup.find('title')
            return title_tag.get_text(strip=True) if title_tag else ""
        except Exception as e:
            logger.error(f"Error extracting title: {e}")
            return ""
    
    def find_sitemap(self) -> Optional[str]:
        """
        Try to find sitemap URL.
        
        Returns:
            Sitemap URL or None
        """
        sitemap_urls = [
            urljoin(self.base_url, '/sitemap.xml'),
            urljoin(self.base_url, '/sitemap_index.xml'),
            urljoin(self.base_url, '/sitemap.txt'),
        ]
        
        for sitemap_url in sitemap_urls:
            try:
                response = self.session.head(sitemap_url, timeout=5)
                if response.status_code == 200:
                    logger.info(f"Found sitemap at {sitemap_url}")
                    return sitemap_url
            except Exception:
                continue
        
        logger.info("No sitemap found")
        return None
    
    def parse_sitemap(self, sitemap_url: str) -> List[str]:
        """
        Parse sitemap XML and extract URLs.
        
        Args:
            sitemap_url: URL of sitemap
            
        Returns:
            List of URLs from sitemap
        """
        urls = []
        try:
            response = self.fetch_page(sitemap_url)
            if not response:
                return urls
            
            # Try to parse as XML
            if HAS_BS4:
                soup = BeautifulSoup(response.text, 'xml')
                # Look for <url><loc> tags
                for url_tag in soup.find_all('loc'):
                    url = url_tag.get_text(strip=True)
                    if url:
                        urls.append(self.normalize_url(url))
                # Also check for sitemap index
                for sitemap_tag in soup.find_all('sitemap'):
                    loc_tag = sitemap_tag.find('loc')
                    if loc_tag:
                        nested_sitemap = loc_tag.get_text(strip=True)
                        nested_urls = self.parse_sitemap(nested_sitemap)
                        urls.extend(nested_urls)
        except Exception as e:
            logger.error(f"Error parsing sitemap {sitemap_url}: {e}")
        
        return urls
    
    def scrape_page(self, url: str, depth: int = 0) -> Optional[Dict]:
        """
        Scrape a single page.
        
        Args:
            url: URL to scrape
            depth: Current depth level
            
        Returns:
            Dictionary with scraped data or None
        """
        if depth > self.max_depth:
            return None
        
        if not self.is_same_domain(url):
            return None
        
        response = self.fetch_page(url)
        if not response:
            return None
        
        html = response.text
        title = self.extract_title(html)
        text = self.extract_text(html)
        page_images = self.extract_images(html, url)
        page_links = self.extract_links(html, url)
        
        # Add images and links to collections
        self.images.extend(page_images)
        self.links.extend(page_links)
        
        # Add new links to queue if within depth limit
        if depth < self.max_depth:
            for link in page_links:
                if link not in self.visited_urls and self.is_same_domain(link):
                    self.url_queue.append((link, depth + 1))
        
        return {
            'url': url,
            'title': title,
            'content': text,
            'content_type': 'html',
            'images': page_images,
            'links': page_links,
            'scraped_at': datetime.utcnow().isoformat()
        }
    
    def crawl(self, start_url: Optional[str] = None, use_sitemap: bool = True) -> List[Dict]:
        """
        Start crawling from base URL or sitemap.
        
        Args:
            start_url: Starting URL (defaults to base_url)
            use_sitemap: Whether to use sitemap if available
            
        Returns:
            List of scraped data dictionaries
        """
        if start_url:
            self.url_queue.append((start_url, 0))
        else:
            self.url_queue.append((self.base_url, 0))
        
        # Try to use sitemap
        if use_sitemap:
            sitemap_url = self.find_sitemap()
            if sitemap_url:
                sitemap_urls = self.parse_sitemap(sitemap_url)
                for url in sitemap_urls:
                    if url not in self.visited_urls:
                        self.url_queue.append((url, 0))
        
        # Process queue
        while self.url_queue:
            url, depth = self.url_queue.popleft()
            
            if url in self.visited_urls:
                continue
            
            scraped = self.scrape_page(url, depth)
            if scraped:
                self.scraped_data.append(scraped)
                logger.info(f"Scraped {url} (depth: {depth}, total: {len(self.scraped_data)})")
        
        logger.info(f"Crawling complete: {len(self.scraped_data)} pages scraped")
        return self.scraped_data

