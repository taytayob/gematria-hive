"""
Quantum Inference Affinity Agent

Purpose: Detect synchronicities, signs, symbols, and explore the "unknown known"
- Quantum-like probabilistic inference (superposition states, entanglement)
- Synchronicity detection (meaningful coincidences, patterns)
- Symbolic interpretation (gematria connections, signs, symbols)
- Latent knowledge exploration (known but unrecognized patterns)

Author: Gematria Hive Team
Date: January 6, 2025
"""

import logging
import os
import json
import random
import math
import asyncio
from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from dataclasses import dataclass, field
from agents.orchestrator import AgentState
from dotenv import load_dotenv

load_dotenv()

try:
    from supabase import create_client, Client
    from sentence_transformers import SentenceTransformer, util
    HAS_DEPENDENCIES = True
except ImportError:
    HAS_DEPENDENCIES = False
    print("Warning: Affinity agent dependencies not available")

logger = logging.getLogger(__name__)


@dataclass
class Synchronicity:
    """Represents a meaningful coincidence or pattern"""
    id: str
    timestamp: str
    pattern_type: str  # 'gematria', 'symbolic', 'temporal', 'semantic', 'quantum'
    elements: List[Dict]  # Connected elements
    strength: float  # 0.0 to 1.0 - how strong the connection
    significance: float  # 0.0 to 1.0 - how significant/meaningful
    description: str
    gematria_values: List[int] = field(default_factory=list)
    symbols: List[str] = field(default_factory=list)
    quantum_state: Optional[Dict] = None  # Quantum-like superposition state


@dataclass
class Symbol:
    """Represents a sign or symbol with meaning"""
    id: str
    symbol: str  # The symbol itself (text, number, pattern)
    meaning: str
    domain: str  # 'geometric', 'numerological', 'kabbalistic', 'hermetic', etc.
    gematria_value: Optional[int] = None
    related_symbols: List[str] = field(default_factory=list)
    affinity_score: float = 0.0  # Quantum affinity score


@dataclass
class QuantumState:
    """Quantum-like superposition state for inference"""
    element_id: str
    superposition: Dict[str, float]  # Possible states and their probabilities
    entanglement: List[str] = field(default_factory=list)  # Entangled elements
    coherence: float = 1.0  # Quantum coherence (1.0 = fully coherent)
    collapsed: bool = False  # Whether state has collapsed to a single value


class AffinityAgent:
    """
    Quantum Inference Affinity Agent
    
    Operations:
    - Quantum-like probabilistic inference
    - Synchronicity detection
    - Symbolic interpretation
    - Latent knowledge exploration (unknown known)
    """
    
    def __init__(self):
        """Initialize affinity agent"""
        self.name = "affinity_agent"
        
        # Quantum states for elements
        self.quantum_states: Dict[str, QuantumState] = {}
        
        # Detected synchronicities
        self.synchronicities: List[Synchronicity] = []
        
        # Symbol registry
        self.symbols: Dict[str, Symbol] = {}
        
        # Affinity graph (connections between elements)
        self.affinity_graph: Dict[str, Dict[str, float]] = defaultdict(dict)
        
        if HAS_DEPENDENCIES:
            supabase_url = os.getenv('SUPABASE_URL')
            supabase_key = os.getenv('SUPABASE_KEY')
            if supabase_url and supabase_key:
                self.supabase = create_client(supabase_url, supabase_key)
                self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')
            else:
                self.supabase = None
                self.embed_model = None
        else:
            self.supabase = None
            self.embed_model = None
        
        # Initialize gematria calculator if available
        try:
            from gematria_calculator import GematriaCalculator
            self.gematria_calc = GematriaCalculator()
        except:
            self.gematria_calc = None
        
        logger.info(f"Initialized {self.name}")
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute affinity task
        
        Args:
            state: Agent state with data
            
        Returns:
            Updated state with synchronicities, symbols, and quantum insights
        """
        task = state.get("task", {})
        task_type = task.get("type", "detect")
        query = task.get("query", "")
        
        logger.info(f"Affinity agent: {task_type} for query: {query}")
        
        if not self.supabase or not self.embed_model:
            logger.warning("Affinity agent: Dependencies not available, skipping")
            return state
        
        try:
            results = []
            
            if task_type == "detect":
                # Detect synchronicities and patterns
                synchronicities = self.detect_synchronicities(state)
                results.append({
                    "agent": self.name,
                    "action": "detect",
                    "synchronicities_count": len(synchronicities),
                    "synchronicities": [self._synchronicity_to_dict(s) for s in synchronicities]
                })
            
            elif task_type == "quantum_inference":
                # Quantum-like probabilistic inference
                quantum_insights = self.quantum_inference(state, query)
                results.append({
                    "agent": self.name,
                    "action": "quantum_inference",
                    "insights": quantum_insights
                })
            
            elif task_type == "symbol_analysis":
                # Analyze signs and symbols
                symbol_analysis = self.analyze_symbols(state, query)
                results.append({
                    "agent": self.name,
                    "action": "symbol_analysis",
                    "symbols": symbol_analysis
                })
            
            elif task_type == "unknown_known":
                # Explore unknown known - latent patterns
                latent_patterns = self.explore_unknown_known(state, query)
                results.append({
                    "agent": self.name,
                    "action": "unknown_known",
                    "latent_patterns": latent_patterns
                })
            
            elif task_type == "affinity_map":
                # Generate affinity map
                affinity_map = self.generate_affinity_map(state)
                results.append({
                    "agent": self.name,
                    "action": "affinity_map",
                    "affinity_map": affinity_map
                })
            
            state["results"].extend(results)
            logger.info(f"Affinity agent complete: {len(results)} results")
            
        except Exception as e:
            logger.error(f"Affinity agent error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state
    
    async def execute_async(self, state: AgentState) -> AgentState:
        """
        Execute affinity task asynchronously
        
        Args:
            state: Agent state with data
            
        Returns:
            Updated state with synchronicities, symbols, and quantum insights
        """
        task = state.get("task", {})
        task_type = task.get("type", "detect")
        query = task.get("query", "")
        
        logger.info(f"Affinity agent (async): {task_type} for query: {query}")
        
        if not self.supabase or not self.embed_model:
            logger.warning("Affinity agent: Dependencies not available, skipping")
            return state
        
        try:
            results = []
            
            if task_type == "detect":
                # Detect synchronicities and patterns asynchronously
                synchronicities = await self.detect_synchronicities_async(state)
                results.append({
                    "agent": self.name,
                    "action": "detect",
                    "synchronicities_count": len(synchronicities),
                    "synchronicities": [self._synchronicity_to_dict(s) for s in synchronicities]
                })
            
            elif task_type == "quantum_inference":
                # Quantum-like probabilistic inference asynchronously
                quantum_insights = await self.quantum_inference_async(state, query)
                results.append({
                    "agent": self.name,
                    "action": "quantum_inference",
                    "insights": quantum_insights
                })
            
            elif task_type == "symbol_analysis":
                # Analyze signs and symbols asynchronously
                symbol_analysis = await self.analyze_symbols_async(state, query)
                results.append({
                    "agent": self.name,
                    "action": "symbol_analysis",
                    "symbols": symbol_analysis
                })
            
            elif task_type == "unknown_known":
                # Explore unknown known - latent patterns asynchronously
                latent_patterns = await self.explore_unknown_known_async(state, query)
                results.append({
                    "agent": self.name,
                    "action": "unknown_known",
                    "latent_patterns": latent_patterns
                })
            
            elif task_type == "affinity_map":
                # Generate affinity map asynchronously
                affinity_map = await self.generate_affinity_map_async(state)
                results.append({
                    "agent": self.name,
                    "action": "affinity_map",
                    "affinity_map": affinity_map
                })
            
            state["results"].extend(results)
            logger.info(f"Affinity agent (async) complete: {len(results)} results")
            
        except Exception as e:
            logger.error(f"Affinity agent (async) error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state
    
    def detect_synchronicities(self, state: AgentState) -> List[Synchronicity]:
        """
        Detect synchronicities - meaningful coincidences and patterns
        
        Args:
            state: Agent state with data
            
        Returns:
            List of detected synchronicities
        """
        synchronicities = []
        data = state.get("data", [])
        
        if not data:
            return synchronicities
        
        # Group data by various dimensions
        by_gematria = defaultdict(list)
        by_symbol = defaultdict(list)
        by_time = defaultdict(list)
        by_semantic = defaultdict(list)
        
        for item in data:
            # Gematria-based grouping
            if self.gematria_calc and item.get("text"):
                try:
                    value = self.gematria_calc.calculate_phrase_value(
                        item["text"], "jewish"
                    )
                    if value:
                        by_gematria[value].append(item)
                except:
                    pass
            
            # Symbol-based grouping
            symbols = self._extract_symbols(item)
            for symbol in symbols:
                by_symbol[symbol].append(item)
            
            # Temporal grouping
            timestamp = item.get("timestamp") or item.get("created_at")
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    time_key = dt.strftime("%Y-%m-%d %H:00")  # Group by hour
                    by_time[time_key].append(item)
                except:
                    pass
            
            # Semantic grouping
            if item.get("embedding"):
                # Use embedding for semantic clustering
                embedding = item["embedding"]
                # Simple hash-based clustering (could be improved)
                cluster_id = hash(tuple(embedding[:10])) % 100
                by_semantic[cluster_id].append(item)
        
        # Detect synchronicities
        
        # 1. Gematria synchronicities
        for value, items in by_gematria.items():
            if len(items) >= 2:  # At least 2 items with same gematria value
                strength = min(1.0, len(items) / 10.0)  # Stronger with more items
                significance = self._calculate_significance(items, "gematria")
                
                synchronicity = Synchronicity(
                    id=f"sync_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                    timestamp=datetime.utcnow().isoformat(),
                    pattern_type="gematria",
                    elements=items,
                    strength=strength,
                    significance=significance,
                    description=f"Gematria value {value} appears in {len(items)} items",
                    gematria_values=[value]
                )
                synchronicities.append(synchronicity)
        
        # 2. Symbolic synchronicities
        for symbol, items in by_symbol.items():
            if len(items) >= 2:
                strength = min(1.0, len(items) / 5.0)
                significance = self._calculate_significance(items, "symbolic")
                
                synchronicity = Synchronicity(
                    id=f"sync_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                    timestamp=datetime.utcnow().isoformat(),
                    pattern_type="symbolic",
                    elements=items,
                    strength=strength,
                    significance=significance,
                    description=f"Symbol '{symbol}' appears in {len(items)} items",
                    symbols=[symbol]
                )
                synchronicities.append(synchronicity)
        
        # 3. Temporal synchronicities
        for time_key, items in by_time.items():
            if len(items) >= 3:  # At least 3 items in same time window
                strength = min(1.0, len(items) / 10.0)
                significance = self._calculate_significance(items, "temporal")
                
                synchronicity = Synchronicity(
                    id=f"sync_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                    timestamp=datetime.utcnow().isoformat(),
                    pattern_type="temporal",
                    elements=items,
                    strength=strength,
                    significance=significance,
                    description=f"{len(items)} items clustered in time window {time_key}"
                )
                synchronicities.append(synchronicity)
        
        # 4. Semantic synchronicities
        for cluster_id, items in by_semantic.items():
            if len(items) >= 2:
                # Calculate semantic similarity
                similarities = []
                for i, item1 in enumerate(items):
                    for item2 in items[i+1:]:
                        if item1.get("embedding") and item2.get("embedding"):
                            sim = util.cos_sim(
                                item1["embedding"],
                                item2["embedding"]
                            ).item()
                            similarities.append(sim)
                
                if similarities:
                    avg_similarity = sum(similarities) / len(similarities)
                    if avg_similarity > 0.7:  # High semantic similarity
                        strength = avg_similarity
                        significance = self._calculate_significance(items, "semantic")
                        
                        synchronicity = Synchronicity(
                            id=f"sync_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                            timestamp=datetime.utcnow().isoformat(),
                            pattern_type="semantic",
                            elements=items,
                            strength=strength,
                            significance=significance,
                            description=f"Semantic cluster with {len(items)} similar items (avg similarity: {avg_similarity:.2f})"
                        )
                        synchronicities.append(synchronicity)
        
        # 5. Quantum synchronicities (cross-domain patterns)
        quantum_syncs = self._detect_quantum_synchronicities(
            by_gematria, by_symbol, by_time, by_semantic
        )
        synchronicities.extend(quantum_syncs)
        
        # Store synchronicities
        self.synchronicities.extend(synchronicities)
        
        # Save to database
        if self.supabase:
            for sync in synchronicities:
                try:
                    self.supabase.table("synchronicities").insert({
                        "sync_id": sync.id,
                        "timestamp": sync.timestamp,
                        "pattern_type": sync.pattern_type,
                        "strength": sync.strength,
                        "significance": sync.significance,
                        "description": sync.description,
                        "gematria_values": sync.gematria_values,
                        "symbols": sync.symbols,
                        "elements": json.dumps([self._item_to_dict(e) for e in sync.elements])
                    }).execute()
                except Exception as e:
                    logger.error(f"Error saving synchronicity: {e}")
        
        return synchronicities
    
    async def detect_synchronicities_async(self, state: AgentState) -> List[Synchronicity]:
        """
        Detect synchronicities asynchronously - meaningful coincidences and patterns
        
        Args:
            state: Agent state with data
            
        Returns:
            List of detected synchronicities
        """
        # Run synchronous method in executor
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.detect_synchronicities, state)
    
    def quantum_inference(self, state: AgentState, query: str) -> List[Dict]:
        """
        Quantum-like probabilistic inference
        
        Uses superposition states and entanglement to explore possibilities
        
        Args:
            state: Agent state
            query: Query string
            
        Returns:
            List of quantum insights
        """
        insights = []
        
        if not query:
            return insights
        
        # Create quantum state for query
        query_state = self._create_quantum_state(query, "query")
        
        # Find related elements
        related = self._find_related_elements(query)
        
        # Create superposition states for related elements
        for element in related:
            element_state = self._create_quantum_state(element["id"], "element")
            
            # Calculate entanglement strength
            entanglement = self._calculate_entanglement(query_state, element_state)
            
            if entanglement > 0.5:  # Significant entanglement
                # Collapse state to get insight
                collapsed = self._collapse_state(element_state)
                
                insight = {
                    "element_id": element["id"],
                    "entanglement": entanglement,
                    "superposition": element_state.superposition,
                    "collapsed_state": collapsed,
                    "coherence": element_state.coherence,
                    "description": f"Quantum entanglement detected: {entanglement:.2f}"
                }
                insights.append(insight)
        
        # Quantum interference patterns
        interference = self._detect_quantum_interference(related)
        if interference:
            insights.append({
                "type": "quantum_interference",
                "pattern": interference,
                "description": "Quantum interference pattern detected"
            })
        
        return insights
    
    async def quantum_inference_async(self, state: AgentState, query: str) -> List[Dict]:
        """
        Quantum-like probabilistic inference asynchronously
        
        Args:
            state: Agent state
            query: Query string
            
        Returns:
            List of quantum insights
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.quantum_inference, state, query)
    
    def analyze_symbols(self, state: AgentState, query: str) -> List[Dict]:
        """
        Analyze signs and symbols
        
        Args:
            state: Agent state
            query: Query string
            
        Returns:
            List of symbol analyses
        """
        symbols = []
        data = state.get("data", [])
        
        # Extract symbols from data
        all_symbols = set()
        for item in data:
            item_symbols = self._extract_symbols(item)
            all_symbols.update(item_symbols)
        
        # Analyze each symbol
        for symbol_str in all_symbols:
            # Calculate gematria value if possible
            gematria_value = None
            if self.gematria_calc:
                try:
                    gematria_value = self.gematria_calc.calculate_phrase_value(
                        symbol_str, "jewish"
                    )
                except:
                    pass
            
            # Find related symbols
            related = []
            if gematria_value and self.gematria_calc:
                try:
                    related_words = self.gematria_calc.find_words_by_value(
                        gematria_value, "jewish", limit=10
                    )
                    related = [w.get("phrase") for w in related_words[:5]]
                except:
                    pass
            
            # Calculate affinity score (quantum affinity)
            affinity_score = self._calculate_symbol_affinity(symbol_str, data)
            
            symbol = Symbol(
                id=f"sym_{hash(symbol_str) % 1000000}",
                symbol=symbol_str,
                meaning=self._interpret_symbol(symbol_str),
                gematria_value=gematria_value,
                related_symbols=related,
                domain=self._classify_symbol_domain(symbol_str),
                affinity_score=affinity_score
            )
            
            self.symbols[symbol.id] = symbol
            
            symbols.append({
                "id": symbol.id,
                "symbol": symbol.symbol,
                "meaning": symbol.meaning,
                "gematria_value": symbol.gematria_value,
                "related_symbols": symbol.related_symbols,
                "domain": symbol.domain,
                "affinity_score": symbol.affinity_score
            })
        
        return symbols
    
    async def analyze_symbols_async(self, state: AgentState, query: str) -> List[Dict]:
        """
        Analyze signs and symbols asynchronously
        
        Args:
            state: Agent state
            query: Query string
            
        Returns:
            List of symbol analyses
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.analyze_symbols, state, query)
    
    def explore_unknown_known(self, state: AgentState, query: str) -> List[Dict]:
        """
        Explore the "unknown known" - latent patterns that exist but aren't recognized
        
        This pushes the "point of the spear" to discover hidden connections
        
        Args:
            state: Agent state
            query: Query string
            
        Returns:
            List of latent patterns
        """
        latent_patterns = []
        data = state.get("data", [])
        
        if not data:
            return latent_patterns
        
        # 1. Cross-domain pattern detection
        cross_domain = self._detect_cross_domain_patterns(data)
        latent_patterns.extend(cross_domain)
        
        # 2. Hidden gematria connections
        hidden_gematria = self._detect_hidden_gematria_connections(data)
        latent_patterns.extend(hidden_gematria)
        
        # 3. Temporal patterns (things that happen together but aren't obvious)
        temporal_patterns = self._detect_temporal_patterns(data)
        latent_patterns.extend(temporal_patterns)
        
        # 4. Semantic shadows (things that are semantically related but not obviously)
        semantic_shadows = self._detect_semantic_shadows(data, query)
        latent_patterns.extend(semantic_shadows)
        
        # 5. Quantum superposition of meanings
        quantum_meanings = self._explore_quantum_meanings(data, query)
        latent_patterns.extend(quantum_meanings)
        
        return latent_patterns
    
    def generate_affinity_map(self, state: AgentState) -> Dict:
        """
        Generate affinity map showing connections between elements
        
        Args:
            state: Agent state
            
        Returns:
            Affinity map dictionary
        """
        data = state.get("data", [])
        
        # Build affinity graph
        for i, item1 in enumerate(data):
            id1 = item1.get("id", f"item_{i}")
            for j, item2 in enumerate(data[i+1:], i+1):
                id2 = item2.get("id", f"item_{j}")
                
                # Calculate affinity
                affinity = self._calculate_affinity(item1, item2)
                
                if affinity > 0.3:  # Threshold for connection
                    self.affinity_graph[id1][id2] = affinity
                    self.affinity_graph[id2][id1] = affinity
        
        # Find clusters
        clusters = self._find_affinity_clusters()
        
        # Find bridges (connections between clusters)
        bridges = self._find_affinity_bridges(clusters)
        
        return {
            "nodes": len(self.affinity_graph),
            "edges": sum(len(connections) for connections in self.affinity_graph.values()) // 2,
            "clusters": clusters,
            "bridges": bridges,
            "graph": {
                k: dict(v) for k, v in self.affinity_graph.items()
            }
        }
    
    async def explore_unknown_known_async(self, state: AgentState, query: str) -> List[Dict]:
        """
        Explore the "unknown known" asynchronously - latent patterns that exist but aren't recognized
        
        Args:
            state: Agent state
            query: Query string
            
        Returns:
            List of latent patterns
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.explore_unknown_known, state, query)
    
    async def generate_affinity_map_async(self, state: AgentState) -> Dict:
        """
        Generate affinity map asynchronously showing connections between elements
        
        Args:
            state: Agent state
            
        Returns:
            Affinity map dictionary
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.generate_affinity_map, state)
    
    # Helper methods
    
    def _extract_symbols(self, item: Dict) -> List[str]:
        """Extract symbols from an item"""
        symbols = []
        text = item.get("text") or item.get("summary") or item.get("title", "")
        
        if not text:
            return symbols
        
        # Extract numbers
        import re
        numbers = re.findall(r'\d+', text)
        symbols.extend(numbers)
        
        # Extract special characters/patterns
        special = re.findall(r'[^\w\s]+', text)
        symbols.extend(special)
        
        # Extract key words (could be improved with NLP)
        words = text.split()
        # Filter for potentially symbolic words
        symbolic_keywords = ['circle', 'triangle', 'square', 'star', 'cross', 'spiral',
                           'infinity', 'phi', 'pi', 'golden', 'ratio', 'sacred', 'holy']
        for word in words:
            if word.lower() in symbolic_keywords:
                symbols.append(word.lower())
        
        return list(set(symbols))
    
    def _calculate_significance(self, items: List[Dict], pattern_type: str) -> float:
        """Calculate significance score for a pattern"""
        base_score = min(1.0, len(items) / 10.0)
        
        # Boost significance based on pattern type
        if pattern_type == "gematria":
            # Gematria patterns are more significant
            return min(1.0, base_score * 1.2)
        elif pattern_type == "quantum":
            # Quantum patterns are highly significant
            return min(1.0, base_score * 1.5)
        else:
            return base_score
    
    def _detect_quantum_synchronicities(self, by_gematria, by_symbol, by_time, by_semantic) -> List[Synchronicity]:
        """Detect quantum synchronicities (cross-domain patterns)"""
        quantum_syncs = []
        
        # Find elements that appear in multiple dimensions
        element_counts = defaultdict(int)
        
        for value, items in by_gematria.items():
            for item in items:
                element_counts[item.get("id", str(item))] += 1
        
        for symbol, items in by_symbol.items():
            for item in items:
                element_counts[item.get("id", str(item))] += 1
        
        for time_key, items in by_time.items():
            for item in items:
                element_counts[item.get("id", str(item))] += 1
        
        # Elements that appear in multiple dimensions are quantum synchronicities
        for element_id, count in element_counts.items():
            if count >= 2:  # Appears in at least 2 dimensions
                # Find all occurrences
                all_items = []
                for value, items in by_gematria.items():
                    for item in items:
                        if item.get("id", str(item)) == element_id:
                            all_items.append(item)
                
                for symbol, items in by_symbol.items():
                    for item in items:
                        if item.get("id", str(item)) == element_id:
                            all_items.append(item)
                
                if len(all_items) >= 2:
                    strength = min(1.0, count / 5.0)
                    significance = min(1.0, strength * 1.3)  # Quantum patterns are more significant
                    
                    sync = Synchronicity(
                        id=f"sync_quantum_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                        timestamp=datetime.utcnow().isoformat(),
                        pattern_type="quantum",
                        elements=all_items,
                        strength=strength,
                        significance=significance,
                        description=f"Quantum synchronicity: element appears across {count} dimensions"
                    )
                    quantum_syncs.append(sync)
        
        return quantum_syncs
    
    def _create_quantum_state(self, element_id: str, element_type: str) -> QuantumState:
        """Create a quantum-like superposition state"""
        if element_id in self.quantum_states:
            return self.quantum_states[element_id]
        
        # Create superposition with multiple possible states
        # In reality, this would be based on actual data analysis
        superposition = {
            "state_1": 0.3,
            "state_2": 0.4,
            "state_3": 0.3
        }
        
        state = QuantumState(
            element_id=element_id,
            superposition=superposition,
            entanglement=[],
            coherence=1.0,
            collapsed=False
        )
        
        self.quantum_states[element_id] = state
        return state
    
    def _find_related_elements(self, query: str) -> List[Dict]:
        """Find elements related to query"""
        related = []
        
        if not self.supabase or not self.embed_model:
            return related
        
        try:
            # Generate query embedding
            query_embedding = self.embed_model.encode(query)
            
            # Search for similar bookmarks
            result = self.supabase.table("bookmarks").select("*").limit(20).execute()
            
            if result.data:
                for item in result.data:
                    if item.get("embedding"):
                        similarity = util.cos_sim(
                            query_embedding,
                            [item["embedding"]]
                        )[0][0].item()
                        
                        if similarity > 0.5:
                            related.append({
                                "id": item.get("id"),
                                "similarity": similarity,
                                "data": item
                            })
        except Exception as e:
            logger.error(f"Error finding related elements: {e}")
        
        return related
    
    def _calculate_entanglement(self, state1: QuantumState, state2: QuantumState) -> float:
        """Calculate quantum entanglement strength between two states"""
        # Simplified entanglement calculation
        # In reality, this would be more sophisticated
        
        # Check if states share any superposition states
        shared_states = set(state1.superposition.keys()) & set(state2.superposition.keys())
        
        if not shared_states:
            return 0.0
        
        # Calculate entanglement based on shared states
        entanglement = 0.0
        for state in shared_states:
            prob1 = state1.superposition[state]
            prob2 = state2.superposition[state]
            entanglement += prob1 * prob2
        
        return min(1.0, entanglement)
    
    def _collapse_state(self, state: QuantumState) -> str:
        """Collapse quantum state to a single value"""
        if state.collapsed:
            return state.superposition.get("collapsed_value", "unknown")
        
        # Collapse based on probabilities
        rand = random.random()
        cumulative = 0.0
        
        for state_name, prob in state.superposition.items():
            cumulative += prob
            if rand <= cumulative:
                state.collapsed = True
                state.superposition["collapsed_value"] = state_name
                return state_name
        
        return "unknown"
    
    def _detect_quantum_interference(self, related: List[Dict]) -> Optional[Dict]:
        """Detect quantum interference patterns"""
        if len(related) < 2:
            return None
        
        # Look for interference patterns (constructive/destructive)
        # Simplified version
        return {
            "type": "interference",
            "pattern": "constructive",
            "strength": 0.7
        }
    
    def _interpret_symbol(self, symbol: str) -> str:
        """Interpret a symbol's meaning"""
        # Simplified interpretation
        interpretations = {
            "circle": "Unity, wholeness, infinity",
            "triangle": "Trinity, stability, ascension",
            "square": "Foundation, stability, material",
            "star": "Guidance, light, divine",
            "cross": "Intersection, sacrifice, transcendence",
            "spiral": "Evolution, growth, cycles",
            "phi": "Golden ratio, divine proportion",
            "pi": "Circle, infinity, cycles"
        }
        
        return interpretations.get(symbol.lower(), f"Symbol: {symbol}")
    
    def _classify_symbol_domain(self, symbol: str) -> str:
        """Classify symbol into domain"""
        geometric = ["circle", "triangle", "square", "spiral", "phi", "pi"]
        numerological = [str(i) for i in range(10)]
        
        if symbol.lower() in geometric:
            return "geometric"
        elif symbol in numerological:
            return "numerological"
        elif any(char in symbol for char in "אבגדהוזחטיכסעפצקרשת"):
            return "kabbalistic"
        else:
            return "general"
    
    def _calculate_symbol_affinity(self, symbol: str, data: List[Dict]) -> float:
        """Calculate quantum affinity score for a symbol"""
        # Count occurrences
        count = sum(1 for item in data if symbol in str(item).lower())
        
        # Calculate affinity based on frequency and context
        base_affinity = min(1.0, count / 10.0)
        
        # Boost if symbol has gematria value
        if self.gematria_calc:
            try:
                value = self.gematria_calc.calculate_phrase_value(symbol, "jewish")
                if value:
                    base_affinity *= 1.2
            except:
                pass
        
        return min(1.0, base_affinity)
    
    def _detect_cross_domain_patterns(self, data: List[Dict]) -> List[Dict]:
        """Detect patterns across different domains"""
        patterns = []
        
        # Group by domain indicators
        domains = defaultdict(list)
        for item in data:
            text = str(item).lower()
            if any(word in text for word in ["gematria", "numerology", "number"]):
                domains["numerological"].append(item)
            if any(word in text for word in ["geometry", "shape", "pattern"]):
                domains["geometric"].append(item)
            if any(word in text for word in ["symbol", "sign", "meaning"]):
                domains["symbolic"].append(item)
        
        # Find cross-domain connections
        for domain1, items1 in domains.items():
            for domain2, items2 in domains.items():
                if domain1 != domain2:
                    # Find shared elements
                    shared = [i for i in items1 if i in items2]
                    if shared:
                        patterns.append({
                            "type": "cross_domain",
                            "domains": [domain1, domain2],
                            "shared_elements": len(shared),
                            "description": f"Pattern spanning {domain1} and {domain2}"
                        })
        
        return patterns
    
    def _detect_hidden_gematria_connections(self, data: List[Dict]) -> List[Dict]:
        """Detect hidden gematria connections"""
        patterns = []
        
        if not self.gematria_calc:
            return patterns
        
        # Extract all text
        all_texts = []
        for item in data:
            text = item.get("text") or item.get("summary") or item.get("title", "")
            if text:
                all_texts.append(text)
        
        # Calculate gematria values
        gematria_values = {}
        for text in all_texts:
            try:
                value = self.gematria_calc.calculate_phrase_value(text, "jewish")
                if value:
                    if value not in gematria_values:
                        gematria_values[value] = []
                    gematria_values[value].append(text)
            except:
                pass
        
        # Find hidden connections (same value, different texts)
        for value, texts in gematria_values.items():
            if len(texts) >= 2:
                patterns.append({
                    "type": "hidden_gematria",
                    "gematria_value": value,
                    "connected_texts": texts,
                    "description": f"Hidden gematria connection: value {value} links {len(texts)} texts"
                })
        
        return patterns
    
    def _detect_temporal_patterns(self, data: List[Dict]) -> List[Dict]:
        """Detect temporal patterns"""
        patterns = []
        
        # Group by time
        by_time = defaultdict(list)
        for item in data:
            timestamp = item.get("timestamp") or item.get("created_at")
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    time_key = dt.strftime("%Y-%m-%d")
                    by_time[time_key].append(item)
                except:
                    pass
        
        # Find patterns in time
        for time_key, items in by_time.items():
            if len(items) >= 3:
                patterns.append({
                    "type": "temporal",
                    "time_key": time_key,
                    "items_count": len(items),
                    "description": f"Temporal cluster: {len(items)} items on {time_key}"
                })
        
        return patterns
    
    def _detect_semantic_shadows(self, data: List[Dict], query: str) -> List[Dict]:
        """Detect semantic shadows - hidden semantic connections"""
        patterns = []
        
        if not self.embed_model or not query:
            return patterns
        
        try:
            query_embedding = self.embed_model.encode(query)
            
            # Find items with low direct similarity but high indirect similarity
            for item in data:
                if item.get("embedding"):
                    direct_sim = util.cos_sim(
                        query_embedding,
                        [item["embedding"]]
                    )[0][0].item()
                    
                    # If direct similarity is low but item is semantically rich
                    if 0.3 < direct_sim < 0.6:
                        patterns.append({
                            "type": "semantic_shadow",
                            "item_id": item.get("id"),
                            "similarity": direct_sim,
                            "description": f"Semantic shadow detected: indirect connection to query"
                        })
        except Exception as e:
            logger.error(f"Error detecting semantic shadows: {e}")
        
        return patterns
    
    def _explore_quantum_meanings(self, data: List[Dict], query: str) -> List[Dict]:
        """Explore quantum superposition of meanings"""
        patterns = []
        
        # Create superposition states for query
        query_states = self._create_quantum_state(query, "query")
        
        # Explore multiple possible meanings
        meanings = []
        for state_name, prob in query_states.superposition.items():
            if state_name != "collapsed_value":
                meanings.append({
                    "state": state_name,
                    "probability": prob,
                    "interpretation": f"Possible meaning: {state_name}"
                })
        
        if meanings:
            patterns.append({
                "type": "quantum_meanings",
                "query": query,
                "meanings": meanings,
                "description": "Quantum superposition of possible meanings"
            })
        
        return patterns
    
    def _calculate_affinity(self, item1: Dict, item2: Dict) -> float:
        """Calculate affinity between two items"""
        affinity = 0.0
        
        # Semantic affinity
        if item1.get("embedding") and item2.get("embedding"):
            try:
                sim = util.cos_sim(
                    item1["embedding"],
                    item2["embedding"]
                )[0][0].item()
                affinity += sim * 0.5
            except:
                pass
        
        # Gematria affinity
        if self.gematria_calc:
            text1 = item1.get("text") or item1.get("summary", "")
            text2 = item2.get("text") or item2.get("summary", "")
            
            if text1 and text2:
                try:
                    val1 = self.gematria_calc.calculate_phrase_value(text1, "jewish")
                    val2 = self.gematria_calc.calculate_phrase_value(text2, "jewish")
                    
                    if val1 and val2 and val1 == val2:
                        affinity += 0.5
                except:
                    pass
        
        return min(1.0, affinity)
    
    def _find_affinity_clusters(self) -> List[Dict]:
        """Find clusters in affinity graph"""
        # Simplified clustering
        visited = set()
        clusters = []
        
        for node in self.affinity_graph:
            if node not in visited:
                cluster = self._bfs_cluster(node, visited)
                if len(cluster) > 1:
                    clusters.append({
                        "nodes": cluster,
                        "size": len(cluster)
                    })
        
        return clusters
    
    def _bfs_cluster(self, start: str, visited: Set) -> List[str]:
        """BFS to find cluster"""
        cluster = []
        queue = [start]
        visited.add(start)
        
        while queue:
            node = queue.pop(0)
            cluster.append(node)
            
            for neighbor in self.affinity_graph.get(node, {}):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return cluster
    
    def _find_affinity_bridges(self, clusters: List[Dict]) -> List[Dict]:
        """Find bridges between clusters"""
        bridges = []
        
        for i, cluster1 in enumerate(clusters):
            for cluster2 in clusters[i+1:]:
                # Find connections between clusters
                connections = []
                for node1 in cluster1["nodes"]:
                    for node2 in cluster2["nodes"]:
                        if node2 in self.affinity_graph.get(node1, {}):
                            affinity = self.affinity_graph[node1][node2]
                            connections.append({
                                "from": node1,
                                "to": node2,
                                "affinity": affinity
                            })
                
                if connections:
                    bridges.append({
                        "cluster1": i,
                        "cluster2": i + 1,
                        "connections": connections
                    })
        
        return bridges
    
    def _synchronicity_to_dict(self, sync: Synchronicity) -> Dict:
        """Convert synchronicity to dictionary"""
        return {
            "id": sync.id,
            "timestamp": sync.timestamp,
            "pattern_type": sync.pattern_type,
            "strength": sync.strength,
            "significance": sync.significance,
            "description": sync.description,
            "gematria_values": sync.gematria_values,
            "symbols": sync.symbols,
            "elements_count": len(sync.elements)
        }
    
    def _item_to_dict(self, item: Dict) -> Dict:
        """Convert item to dictionary for storage"""
        return {
            "id": item.get("id"),
            "text": item.get("text") or item.get("summary") or item.get("title", ""),
            "timestamp": item.get("timestamp") or item.get("created_at")
        }

