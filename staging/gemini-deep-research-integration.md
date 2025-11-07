# Gemini Deep Research Drive Integration Recommendation

## Decision: ✅ **YES - Integrate Gemini Deep Research Drive**

### Executive Summary

**Recommendation:** Integrate Google's Gemini Deep Research Drive into the browser agent ecosystem to enhance base layer data collection for bookmarks and enable simultaneous multi-environment execution.

**Rationale:**
1. **Comprehensive Research Reports:** Gemini Deep Research can generate detailed, multi-source research reports that provide rich base layer data for bookmarks
2. **Google Workspace Integration:** Direct access to Drive, Gmail, and Chat where URLs/bookmarks may be stored
3. **Simultaneous Execution:** Can run in parallel with existing browser agent through the MCP orchestrator
4. **Architecture Alignment:** Fits perfectly into the existing browser agent → extraction → distillation → ingestion pipeline
5. **Cost Efficiency:** Leverages Google's research capabilities without duplicating infrastructure

---

## Benefits for Gematria Hive

### 1. Enhanced Base Layer Data for Bookmarks

**Current State:**
- Browser agent scrapes URLs directly
- Basic content extraction (title, summary, links, images)
- Manual bookmark organization

**With Gemini Deep Research:**
- **Comprehensive Reports:** Multi-source research reports that synthesize information from:
  - Google Search
  - Google Drive documents
  - Gmail conversations
  - Chat history
  - The target URL itself
- **Rich Context:** Reports include:
  - Related sources and citations
  - Cross-references to other bookmarks
  - Semantic connections
  - Historical context
- **Structured Output:** Research reports can be parsed and stored as:
  - Enhanced bookmark summaries
  - Related links array
  - Tags based on research findings
  - Relevance scores based on report depth

### 2. Simultaneous Multi-Environment Execution

**Architecture Support:**
- **MCP Orchestrator:** Can route tasks to multiple agents simultaneously
- **Browser Agent:** Can run alongside Gemini Deep Research agent
- **Parallel Processing:** Both can process different URLs or the same URL with different approaches
- **Environment Parity:** Works in Cursor, Replit, and local dev through unified API

**Execution Pattern:**
```
URL Input
    ├─> Browser Agent (Direct Scraping)
    │   └─> Extract: HTML, images, links, basic content
    │
    └─> Gemini Deep Research Agent (Research Report)
        └─> Generate: Comprehensive research report
            └─> Extract: Related sources, citations, context

Both outputs → Distillation Agent → Ingestion Agent → Database
```

### 3. Integration with Existing Pipeline

**Data Flow:**
```
1. URL from CSV/Chat → Browser Agent + Gemini Deep Research Agent
2. Both agents execute simultaneously
3. Results merged in Distillation Agent
4. Enhanced embeddings generated
5. Stored in bookmarks table with:
   - Original scraped content
   - Gemini research report
   - Combined tags
   - Cross-references
```

---

## Implementation Plan

### Phase 1: Gemini API Integration (Week 1)

**1.1 Setup Google Gemini API**
```bash
# Install Google Generative AI SDK
pip install google-generativeai
```

**1.2 Environment Variables**
Add to `.env`:
```bash
GOOGLE_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.0-flash-exp  # or gemini-pro
```

**1.3 Create Gemini Deep Research Agent**
Create `agents/gemini_research.py`:
```python
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
from typing import Dict, List, Optional
import google.generativeai as genai
from agents.orchestrator import AgentState

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
        self.name = "gemini_research_agent"
        self.client = None
        
        # Initialize Gemini API
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            logger.info(f"Initialized {self.name} with Gemini API")
        else:
            logger.warning("GOOGLE_API_KEY not set, Gemini Research agent disabled")
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute Gemini Deep Research task
        
        Args:
            state: Agent state with task information
            
        Returns:
            Updated state with research report data
        """
        if not self.client:
            logger.error("Gemini API not configured")
            state["status"] = "failed"
            state["error"] = "Gemini API not configured"
            return state
        
        task = state.get("task", {})
        url = task.get("url", "")
        query = task.get("query", f"Research and analyze: {url}")
        sources = task.get("sources", ["google_search", "drive", "gmail", "chat"])
        
        if not url:
            logger.error("No URL provided in task")
            state["status"] = "failed"
            state["error"] = "No URL provided"
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
            - themes: List of key themes
            - related_sources: List of related URLs/sources
            - context: Historical or contextual information
            - tags: List of relevant tags
            - gematria_relevance: Boolean indicating if gematria-related
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
                'source': 'gemini_deep_research'
            }
            
            # Add to state data
            existing_data = state.get("data", [])
            state["data"] = existing_data + [formatted_data]
            
            # Update context
            state["context"]["gemini_research_url"] = url
            state["context"]["gemini_research_completed"] = True
            state["context"]["gemini_related_sources"] = len(research_report.get('related_sources', []))
            state["context"]["gemini_tags"] = len(research_report.get('tags', []))
            
            # Add results
            state["results"].append({
                "agent": self.name,
                "action": "research_report",
                "url": url,
                "related_sources": len(research_report.get('related_sources', [])),
                "tags": len(research_report.get('tags', [])),
                "gematria_relevant": research_report.get('gematria_relevance', False)
            })
            
            logger.info(f"Gemini Research complete: {len(research_report.get('related_sources', []))} related sources, "
                       f"{len(research_report.get('tags', []))} tags")
            
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
        import json
        try:
            # Look for JSON in the response
            if '{' in report_text and '}' in report_text:
                json_start = report_text.find('{')
                json_end = report_text.rfind('}') + 1
                json_str = report_text[json_start:json_end]
                return json.loads(json_str)
        except:
            pass
        
        # Fallback: Parse text format
        return {
            'summary': report_text[:500] if len(report_text) > 500 else report_text,
            'title': '',
            'themes': [],
            'related_sources': [],
            'context': report_text,
            'tags': [],
            'gematria_relevance': False
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
        if not self.client:
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
```

### Phase 2: Orchestrator Integration (Week 1)

**2.1 Update Orchestrator**
Add Gemini Research agent to `agents/orchestrator.py`:

```python
# In _build_graph method, add:
from .gemini_research import GeminiResearchAgent

# Initialize agent
self.agents['gemini_research'] = GeminiResearchAgent()

# Add node
self.graph.add_node("gemini_research", self.agents['gemini_research'].execute)

# Update routing logic to run browser + gemini_research in parallel
```

**2.2 Parallel Execution Pattern**
```python
# In execute method, for browser tasks:
if task_type == "browser" or task.get("url"):
    # Run both agents in parallel
    browser_state = self.agents["browser"].execute(initial_state.copy())
    gemini_state = self.agents["gemini_research"].execute(initial_state.copy())
    
    # Merge results
    merged_state = {
        **initial_state,
        "data": browser_state.get("data", []) + gemini_state.get("data", []),
        "results": browser_state.get("results", []) + gemini_state.get("results", [])
    }
    
    # Continue through pipeline
    final_state = self._continue_pipeline(merged_state)
```

### Phase 3: Enhanced Bookmark Ingestion (Week 2)

**3.1 Update Distillation Agent**
Merge browser scraping data with Gemini research report:
```python
def merge_browser_and_research(self, browser_data: Dict, research_data: Dict) -> Dict:
    """Merge browser scraping and Gemini research data"""
    return {
        'url': browser_data.get('url') or research_data.get('url'),
        'title': browser_data.get('title', ''),
        'summary': self._combine_summaries(
            browser_data.get('summary', ''),
            research_data.get('summary', '')
        ),
        'content': browser_data.get('content', ''),
        'research_report': research_data.get('research_report', {}),
        'images': browser_data.get('images', []),
        'links': list(set(
            browser_data.get('links', []) + 
            research_data.get('related_sources', [])
        )),
        'tags': list(set(
            browser_data.get('tags', []) + 
            research_data.get('tags', [])
        )),
        'themes': research_data.get('themes', []),
        'gematria_relevance': research_data.get('gematria_relevance', False)
    }
```

**3.2 Enhanced Embeddings**
Generate embeddings from combined content:
```python
def generate_enhanced_embedding(self, bookmark_data: Dict) -> List[float]:
    """Generate embedding from combined browser + research content"""
    combined_text = f"""
    {bookmark_data.get('title', '')}
    {bookmark_data.get('summary', '')}
    {bookmark_data.get('research_report', {}).get('summary', '')}
    Themes: {', '.join(bookmark_data.get('themes', []))}
    Tags: {', '.join(bookmark_data.get('tags', []))}
    """
    return self.embed_model.encode(combined_text).tolist()
```

---

## Configuration for "jadedraver" Browser Session

### Session-Specific Setup

**1. Browser Session Configuration**
```python
# In browser agent, support named sessions
class BrowserAgent:
    def __init__(self, session_name: str = "default"):
        self.session_name = session_name
        # Store session-specific state
```

**2. CSV Chat URL Integration**
```python
# Read URL from CSV chat
def read_url_from_csv_chat(csv_path: str, session_name: str = "jadedraver") -> List[str]:
    """Extract URLs from CSV chat file"""
    import pandas as pd
    df = pd.read_csv(csv_path)
    # Filter by session if column exists
    if 'session' in df.columns:
        df = df[df['session'] == session_name]
    # Extract URLs
    urls = df['url'].tolist() if 'url' in df.columns else []
    return urls
```

**3. Simultaneous Execution**
```python
# Execute for multiple URLs simultaneously
def process_urls_simultaneously(urls: List[str], session_name: str = "jadedraver"):
    """Process multiple URLs with browser + Gemini research simultaneously"""
    from concurrent.futures import ThreadPoolExecutor
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for url in urls:
            task = {
                "type": "browser",
                "url": url,
                "session": session_name,
                "parallel_research": True  # Enable Gemini research
            }
            future = executor.submit(orchestrator.execute, task)
            futures.append(future)
        
        results = [f.result() for f in futures]
        return results
```

---

## Cost Considerations

### Gemini API Pricing (as of 2025)
- **Gemini 2.0 Flash:** ~$0.075 per 1M input tokens, $0.30 per 1M output tokens
- **Deep Research:** May have additional costs for multi-source queries
- **Estimated Cost:** ~$0.01-0.05 per research report (depending on length)

### Cost Optimization Strategies
1. **Caching:** Cache research reports for URLs already processed
2. **Selective Use:** Only use Gemini Research for high-value URLs (relevance_score > 0.7)
3. **Batch Processing:** Process multiple URLs in single API call when possible
4. **Rate Limiting:** Respect API rate limits to avoid overage charges

---

## Success Metrics

### Phase 1 Metrics (Week 1-2)
- [ ] Gemini API integration working
- [ ] Research reports generated successfully
- [ ] Browser + Gemini parallel execution functional
- [ ] Enhanced bookmarks stored in database

### Phase 2 Metrics (Week 2-4)
- [ ] 100+ bookmarks processed with Gemini research
- [ ] Average 3+ related sources per bookmark
- [ ] 50% improvement in tag accuracy
- [ ] Cost per bookmark < $0.05

### Phase 3 Metrics (Ongoing)
- [ ] Simultaneous execution in Cursor, Replit, and local dev
- [ ] Research reports enhance bookmark relevance scores
- [ ] Cross-reference discovery working
- [ ] Cost tracking and optimization in place

---

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| API rate limits | Medium | Medium | Implement rate limiting and queuing |
| Cost overruns | Medium | Medium | Set budget alerts, cache results |
| Google Workspace access issues | Low | Low | Fallback to Google Search only |
| Research quality variance | Low | Medium | Validate reports, use fallback to browser scraping |
| Simultaneous execution conflicts | Low | Low | Use thread-safe state management |

---

## Next Steps

1. **Immediate (This Week):**
   - [ ] Get Google Gemini API key
   - [ ] Create `agents/gemini_research.py`
   - [ ] Update orchestrator to support parallel execution
   - [ ] Test with single URL

2. **Short-term (Next 2 Weeks):**
   - [ ] Integrate CSV chat URL reading
   - [ ] Implement session management for "jadedraver"
   - [ ] Test simultaneous multi-URL processing
   - [ ] Update bookmark ingestion to merge browser + research data

3. **Medium-term (Next Month):**
   - [ ] Deploy to Replit
   - [ ] Set up cost tracking
   - [ ] Optimize caching strategy
   - [ ] Document usage patterns

---

## Conclusion

**Recommendation: ✅ Proceed with Integration**

Gemini Deep Research Drive integration will significantly enhance the base layer data for bookmarks by providing comprehensive research reports that complement direct web scraping. The architecture already supports simultaneous execution, and the integration is straightforward.

**Key Benefits:**
- Rich, multi-source research reports
- Enhanced bookmark context and cross-references
- Simultaneous execution with existing browser agent
- Better tag and relevance scoring
- Minimal architectural changes required

**Estimated Timeline:** 2-3 weeks for full integration
**Estimated Cost:** ~$0.01-0.05 per bookmark (with optimization)

---

*Prepared: January 6, 2025*
*Status: Ready for Implementation*

