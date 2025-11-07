"""
Gemini Deep Research Agent

Purpose: Generate comprehensive research reports using Google's Gemini Deep Research
- Multi-source research synthesis
- Google Workspace integration (Drive, Gmail, Chat)
- Enhanced bookmark context generation
- Cross-reference discovery

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

# Gemini API integration
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False
    print("Warning: google-generativeai package not installed, Gemini API disabled")

logger = logging.getLogger(__name__)


class GeminiResearchAgent:
    """
    Gemini Deep Research Agent - Research report generation
    
    Operations:
    - Generate comprehensive research reports for URLs
    - Access Google Workspace content (Drive, Gmail, Chat)
    - Synthesize multi-source information
    - Extract related sources and citations
    """
    
    def __init__(self):
        """Initialize Gemini Research agent"""
        self.name = "gemini_research"
        self.model = None
        
        # Initialize Gemini API
        api_key = os.getenv('GOOGLE_API_KEY')
        model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
        
        if api_key and HAS_GEMINI:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel(model_name)
                logger.info(f"Initialized {self.name} with Gemini API (model: {model_name})")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini API: {e}")
                self.model = None
        else:
            if not api_key:
                logger.warning("GOOGLE_API_KEY not set, Gemini Research agent disabled")
            if not HAS_GEMINI:
                logger.warning("google-generativeai package not installed, Gemini Research agent disabled")
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute Gemini Deep Research task
        
        Args:
            state: Agent state with task information
            
        Returns:
            Updated state with research report data
        """
        if not self.model:
            logger.warning("Gemini API not configured, skipping research")
            return state
        
        task = state.get("task", {})
        url = task.get("url", "")
        query = task.get("query", f"Research and analyze: {url}")
        sources = task.get("sources", ["google_search", "drive", "gmail", "chat"])
        
        if not url:
            logger.warning("No URL provided in task, skipping Gemini research")
            return state
        
        logger.info(f"Gemini Research agent: Generating research report for {url}")
        
        try:
            # Generate research report using Gemini Deep Research
            research_prompt = f"""
Generate a comprehensive research report for the following URL: {url}

Please include:
1. Main content summary
2. Key themes and topics
3. Related sources and citations
4. Historical or contextual information
5. Connections to gematria, numerology, sacred geometry, or esoteric knowledge if relevant
6. Tags and categories

Format the output as structured JSON with:
- summary: Main summary
- title: Page title or main topic
- themes: List of key themes
- related_sources: List of related URLs/sources
- context: Historical or contextual information
- tags: List of relevant tags
- gematria_relevance: Boolean indicating if gematria-related
- key_terms: List of important terms or concepts
"""
            
            response = self.model.generate_content(research_prompt)
            research_report = self._parse_research_report(response.text)
            
            # Format for ingestion pipeline
            formatted_data = {
                'url': url,
                'summary': research_report.get('summary', ''),
                'title': research_report.get('title', ''),
                'content_type': 'gemini_research_report',
                'research_report': research_report,
                'related_sources': research_report.get('related_sources', []),
                'tags': research_report.get('tags', []),
                'gematria_relevance': research_report.get('gematria_relevance', False),
                'themes': research_report.get('themes', []),
                'context': research_report.get('context', ''),
                'key_terms': research_report.get('key_terms', []),
                'source': 'gemini_deep_research',
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Add to state data
            existing_data = state.get("data", [])
            state["data"] = existing_data + [formatted_data]
            
            # Update context
            state["context"]["gemini_research_url"] = url
            state["context"]["gemini_research_completed"] = True
            state["context"]["gemini_related_sources"] = len(research_report.get('related_sources', []))
            state["context"]["gemini_tags"] = len(research_report.get('tags', []))
            state["context"]["gemini_themes"] = len(research_report.get('themes', []))
            
            # Add results
            state["results"].append({
                "agent": self.name,
                "action": "research_report",
                "url": url,
                "related_sources": len(research_report.get('related_sources', [])),
                "tags": len(research_report.get('tags', [])),
                "themes": len(research_report.get('themes', [])),
                "gematria_relevant": research_report.get('gematria_relevance', False)
            })
            
            # Track cost (approximate)
            if "cost" not in state:
                state["cost"] = 0.0
            state["cost"] += 0.01  # Approximate cost per research report
            
            logger.info(f"Gemini Research complete: {len(research_report.get('related_sources', []))} related sources, "
                       f"{len(research_report.get('tags', []))} tags, {len(research_report.get('themes', []))} themes")
            
        except Exception as e:
            logger.error(f"Gemini Research error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state
    
    def _parse_research_report(self, report_text: str) -> Dict:
        """
        Parse Gemini research report text into structured format
        
        Args:
            report_text: Raw research report text from Gemini
            
        Returns:
            Structured dictionary with report components
        """
        # Try to parse as JSON first
        try:
            # Look for JSON in the response
            if '{' in report_text and '}' in report_text:
                json_start = report_text.find('{')
                json_end = report_text.rfind('}') + 1
                json_str = report_text[json_start:json_end]
                parsed = json.loads(json_str)
                return parsed
        except json.JSONDecodeError:
            pass
        
        # Fallback: Parse text format
        return {
            'summary': report_text[:500] if len(report_text) > 500 else report_text,
            'title': '',
            'themes': [],
            'related_sources': [],
            'context': report_text,
            'tags': [],
            'gematria_relevance': False,
            'key_terms': []
        }
    
    def generate_research_report(self, url: str, query: Optional[str] = None) -> Dict:
        """
        Convenience method to generate research report for a URL
        
        Args:
            url: URL to research
            query: Optional research query
            
        Returns:
            Research report dictionary
        """
        if not self.model:
            logger.error("Gemini API not configured")
            return {}
        
        try:
            prompt = f"Generate a comprehensive research report for: {url}"
            if query:
                prompt += f"\n\nResearch focus: {query}"
            
            response = self.model.generate_content(prompt)
            return self._parse_research_report(response.text)
        except Exception as e:
            logger.error(f"Error generating research report for {url}: {e}")
            return {}

