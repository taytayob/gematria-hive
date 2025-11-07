"""
Claude Integrator Agent

Purpose: Integrate Claude API and Claude Skills browser plugin
- Claude API integration for reasoning and analysis
- Claude Skills browser plugin support
- Multi-perspective analysis using Claude
- First principles reasoning with Claude
- Highest persona thinking via Claude

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime
import json

from agents.orchestrator import AgentState

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Claude API integration
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False
    print("Warning: anthropic package not installed, Claude API disabled")

logger = logging.getLogger(__name__)


class ClaudeIntegratorAgent:
    """
    Claude Integrator Agent - Integrates Claude API and Claude Skills
    
    Features:
    - Claude API for reasoning and analysis
    - Claude Skills browser plugin support
    - Multi-perspective analysis
    - First principles reasoning
    - Highest persona thinking
    """
    
    def __init__(self):
        """Initialize Claude integrator agent"""
        self.name = "claude_integrator_agent"
        
        # Claude API client
        self.claude_client = None
        if HAS_ANTHROPIC:
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if api_key:
                try:
                    self.claude_client = anthropic.Anthropic(api_key=api_key)
                    logger.info("Claude API client initialized")
                except Exception as e:
                    logger.warning(f"Failed to initialize Claude API: {e}")
        
        # Claude Skills browser plugin support
        self.browser_plugin_enabled = os.getenv('CLAUDE_BROWSER_PLUGIN_ENABLED', 'false').lower() == 'true'
        
        logger.info(f"Initialized {self.name}")
    
    def analyze_with_claude(self, query: str, context: Dict, 
                           persona: Optional[str] = None,
                           apply_first_principles: bool = True) -> Dict:
        """
        Analyze query using Claude API
        
        Args:
            query: Query string
            context: Context dictionary
            persona: Optional persona name for highest persona thinking
            apply_first_principles: Whether to apply first principles thinking
            
        Returns:
            Analysis result dictionary
        """
        if not self.claude_client:
            logger.warning("Claude API not available")
            return {
                'error': 'Claude API not available',
                'query': query
            }
        
        try:
            # Build system prompt
            system_prompt = self._build_system_prompt(persona, apply_first_principles)
            
            # Build user message
            user_message = self._build_user_message(query, context)
            
            # Call Claude API
            message = self.claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",  # Latest Claude model
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )
            
            # Extract response
            response_text = ""
            if message.content:
                for content_block in message.content:
                    if hasattr(content_block, 'text'):
                        response_text += content_block.text
            
            return {
                'query': query,
                'response': response_text,
                'persona': persona,
                'first_principles': apply_first_principles,
                'model': 'claude-3-5-sonnet',
                'usage': {
                    'input_tokens': message.usage.input_tokens if hasattr(message, 'usage') else 0,
                    'output_tokens': message.usage.output_tokens if hasattr(message, 'usage') else 0
                }
            }
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return {
                'error': str(e),
                'query': query
            }
    
    def _build_system_prompt(self, persona: Optional[str] = None,
                            apply_first_principles: bool = True) -> str:
        """Build system prompt for Claude"""
        prompt_parts = []
        
        # Base prompt
        prompt_parts.append("You are an advanced reasoning system for the Gematria Hive, a system for data triangulation, unification, and eternal truth pursuit.")
        prompt_parts.append("Your role is to analyze patterns, detect hidden connections, and provide multi-perspective insights.")
        
        # First principles thinking
        if apply_first_principles:
            prompt_parts.append("\nFirst Principles Thinking:")
            prompt_parts.append("- Break down problems to fundamental components")
            prompt_parts.append("- Question assumptions and established beliefs")
            prompt_parts.append("- Build up from basic truths")
            prompt_parts.append("- Identify core principles and axioms")
        
        # Highest persona thinking
        if persona:
            prompt_parts.append(f"\nApply highest persona thinking from the perspective of: {persona}")
            prompt_parts.append("- Use the frameworks, models, and contributions of this persona")
            prompt_parts.append("- Apply their unique perspective and insights")
            prompt_parts.append("- Consider their domain expertise and knowledge")
        else:
            prompt_parts.append("\nApply highest persona thinking:")
            prompt_parts.append("- Consider multiple perspectives (Einstein, Tesla, Pythagoras, etc.)")
            prompt_parts.append("- Apply first principles from each relevant persona")
            prompt_parts.append("- Synthesize insights across personas")
        
        # Dark matter tracking
        prompt_parts.append("\nDark Matter Tracking:")
        prompt_parts.append("- Identify hidden patterns and latent connections")
        prompt_parts.append("- Detect implicit knowledge structures")
        prompt_parts.append("- Explore quantum-like superposition states of meaning")
        prompt_parts.append("- Find semantic shadows and temporal dark matter")
        
        # Multi-perspective analysis
        prompt_parts.append("\nMulti-Perspective Analysis:")
        prompt_parts.append("- Analyze from multiple angles and domains")
        prompt_parts.append("- Consider esoteric, scientific, mathematical, and philosophical perspectives")
        prompt_parts.append("- Synthesize insights across perspectives")
        
        return "\n".join(prompt_parts)
    
    def _build_user_message(self, query: str, context: Dict) -> str:
        """Build user message for Claude"""
        message_parts = []
        
        message_parts.append(f"Query: {query}")
        
        # Add context
        if context:
            message_parts.append("\nContext:")
            if 'data' in context:
                message_parts.append(f"Data items: {len(context['data'])}")
            if 'patterns' in context:
                message_parts.append(f"Patterns: {len(context['patterns'])}")
            if 'dark_matter_patterns' in context:
                message_parts.append(f"Dark matter patterns: {len(context['dark_matter_patterns'])}")
        
        return "\n".join(message_parts)
    
    def analyze_multi_perspective(self, query: str, context: Dict,
                                 personas: List[str]) -> Dict:
        """
        Analyze query from multiple persona perspectives
        
        Args:
            query: Query string
            context: Context dictionary
            personas: List of persona names
            
        Returns:
            Multi-perspective analysis result
        """
        results = {}
        
        for persona in personas:
            result = self.analyze_with_claude(
                query=query,
                context=context,
                persona=persona,
                apply_first_principles=True
            )
            results[persona] = result
        
        # Synthesize insights
        synthesis = self._synthesize_perspectives(results)
        
        return {
            'query': query,
            'perspectives': results,
            'synthesis': synthesis
        }
    
    def _synthesize_perspectives(self, perspective_results: Dict) -> str:
        """Synthesize insights from multiple perspectives"""
        # In production, use Claude to synthesize
        # For now, return summary
        synthesis_parts = []
        synthesis_parts.append("Synthesis of multi-perspective analysis:")
        
        for persona, result in perspective_results.items():
            if 'response' in result:
                synthesis_parts.append(f"\n{persona}: {result['response'][:200]}...")
        
        return "\n".join(synthesis_parts)
    
    def use_browser_plugin(self, url: str, query: str) -> Dict:
        """
        Use Claude Skills browser plugin to analyze web content
        
        Args:
            url: URL to analyze
            query: Query about the content
            
        Returns:
            Analysis result
        """
        if not self.browser_plugin_enabled:
            logger.warning("Claude browser plugin not enabled")
            return {
                'error': 'Browser plugin not enabled',
                'url': url
            }
        
        # In production, integrate with Claude Skills browser plugin
        # For now, placeholder
        return {
            'url': url,
            'query': query,
            'note': 'Browser plugin integration pending',
            'status': 'placeholder'
        }
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute Claude integration task
        
        Args:
            state: Agent state with task information
            
        Returns:
            Updated state with Claude analysis
        """
        task = state.get("task", {})
        query = task.get("query", "")
        use_claude = task.get("use_claude", True)
        personas = task.get("personas", [])
        
        if not use_claude or not query:
            logger.warning("Claude integration skipped: no query or use_claude=false")
            return state
        
        logger.info(f"Claude integrator: Analyzing query with {len(personas)} personas")
        
        try:
            context = state.get("context", {})
            
            if personas:
                # Multi-perspective analysis
                result = self.analyze_multi_perspective(
                    query=query,
                    context=context,
                    personas=personas
                )
            else:
                # Single analysis with first principles
                result = self.analyze_with_claude(
                    query=query,
                    context=context,
                    apply_first_principles=True
                )
            
            # Update state
            state["context"]["claude_analysis"] = result
            state["results"].append({
                "agent": self.name,
                "action": "claude_analysis",
                "query": query,
                "personas_used": personas if personas else ["default"],
                "result": result
            })
            
            logger.info("Claude analysis complete")
            
        except Exception as e:
            logger.error(f"Claude integration error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

