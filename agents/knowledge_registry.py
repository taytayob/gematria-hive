"""
Knowledge Registry - Gematria Hive

Purpose: Central registry for tracking:
- Claude skills and tools
- Processing status (what is/isn't processed)
- Domains and their foundations
- Git repositories and URLs from bookmarks
- Prioritization sequences for backend, libraries, and data

Author: Gematria Hive Team
Date: 2025-01-06
"""

import os
import json
import logging
from typing import Dict, List, Optional, Set
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field, asdict
from pathlib import Path

logger = logging.getLogger(__name__)


class ProcessingStatus(Enum):
    """Processing status enumeration"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"


class Priority(Enum):
    """Priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    FUTURE = "future"


class DomainCategory(Enum):
    """Domain categories"""
    ESOTERIC = "esoteric"  # Gematria, numerology, sacred geometry
    SCIENTIFIC = "scientific"  # Math, physics, quantum mechanics
    AI_ML = "ai_ml"  # AI/ML technologies
    SPIRITUAL = "spiritual"  # Consciousness, ancient wisdom
    TECHNICAL = "technical"  # Backend, libraries, infrastructure


@dataclass
class ClaudeSkill:
    """Claude skill/tool definition"""
    name: str
    description: str
    file_path: Optional[str] = None
    export_path: Optional[str] = None  # e.g., claude_export.json
    status: ProcessingStatus = ProcessingStatus.NOT_STARTED
    last_updated: Optional[str] = None
    usage_count: int = 0
    tags: List[str] = field(default_factory=list)


@dataclass
class Domain:
    """Domain definition with foundation"""
    name: str
    category: DomainCategory
    foundation: str  # What this domain is founded upon
    description: str
    related_domains: List[str] = field(default_factory=list)
    processing_status: ProcessingStatus = ProcessingStatus.NOT_STARTED
    priority: Priority = Priority.MEDIUM
    libraries: List[str] = field(default_factory=list)
    data_sources: List[str] = field(default_factory=list)


@dataclass
class Bookmark:
    """Bookmark/URL definition"""
    url: str
    title: Optional[str] = None
    description: Optional[str] = None
    source: Optional[str] = None  # 'onetab', 'gematrix', 'dewey', etc.
    processing_status: ProcessingStatus = ProcessingStatus.NOT_STARTED
    priority: Priority = Priority.MEDIUM
    tags: List[str] = field(default_factory=list)
    domain: Optional[str] = None
    scraped_at: Optional[str] = None
    ingested_at: Optional[str] = None


@dataclass
class GitRepository:
    """Git repository definition"""
    name: str
    url: str
    purpose: str
    priority: Priority = Priority.MEDIUM
    integration_phase: Optional[str] = None  # e.g., 'Phase 2', 'Phase 3'
    status: ProcessingStatus = ProcessingStatus.NOT_STARTED
    branch: Optional[str] = None
    last_synced: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class ProcessingQueue:
    """Processing queue item"""
    item_id: str
    item_type: str  # 'bookmark', 'url', 'git', 'domain', 'library'
    priority: Priority
    status: ProcessingStatus
    dependencies: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class KnowledgeRegistry:
    """
    Central registry for all knowledge, skills, tools, domains, and processing status
    """
    
    def __init__(self, registry_file: str = "knowledge_registry.json"):
        """Initialize the knowledge registry"""
        self.registry_file = Path(registry_file)
        self.claude_skills: Dict[str, ClaudeSkill] = {}
        self.domains: Dict[str, Domain] = {}
        self.bookmarks: Dict[str, Bookmark] = {}
        self.git_repos: Dict[str, GitRepository] = {}
        self.processing_queue: List[ProcessingQueue] = []
        
        # Initialize with default data
        self._initialize_defaults()
        
        # Load from file if exists
        if self.registry_file.exists():
            self.load()
        else:
            self.save()
    
    def _initialize_defaults(self):
        """Initialize with default domains, skills, and repositories"""
        
        # Initialize Claude Skills
        self.claude_skills = {
            "gematria_query": ClaudeSkill(
                name="Gematria Query",
                description="Query gematria data from exported JSON for insights and narratives",
                export_path="claude_export.json",
                status=ProcessingStatus.NOT_STARTED,
                tags=["gematria", "query", "narrative"]
            ),
            "bookmark_analysis": ClaudeSkill(
                name="Bookmark Analysis",
                description="Analyze bookmarks for relevance, categorization, and domain mapping",
                status=ProcessingStatus.NOT_STARTED,
                tags=["bookmarks", "analysis", "categorization"]
            ),
            "domain_unification": ClaudeSkill(
                name="Domain Unification",
                description="Unify esoteric and scientific domains through proofs and narratives",
                status=ProcessingStatus.NOT_STARTED,
                tags=["domains", "unification", "proofs"]
            )
        }
        
        # Initialize Domains
        self.domains = {
            "gematria": Domain(
                name="Gematria",
                category=DomainCategory.ESOTERIC,
                foundation="Hebrew letter-to-number mapping system; ancient Jewish numerology",
                description="Numerical value assignment to letters/words for mystical interpretation",
                related_domains=["numerology", "kabbalah", "sacred_geometry"],
                processing_status=ProcessingStatus.IN_PROGRESS,
                priority=Priority.CRITICAL,
                libraries=["gematria_calculator.py"],
                data_sources=["gematrix.org", "1M+ word CSV"]
            ),
            "numerology": Domain(
                name="Numerology",
                category=DomainCategory.ESOTERIC,
                foundation="Universal number symbolism; Pythagorean and Chaldean systems",
                description="Study of numbers and their mystical meanings",
                related_domains=["gematria", "sacred_geometry"],
                processing_status=ProcessingStatus.NOT_STARTED,
                priority=Priority.HIGH,
                data_sources=["gematrix.org"]
            ),
            "sacred_geometry": Domain(
                name="Sacred Geometry",
                category=DomainCategory.ESOTERIC,
                foundation="Geometric patterns found in nature; Phi, Pi, Fibonacci sequences",
                description="Mathematical patterns underlying physical and spiritual reality",
                related_domains=["gematria", "mathematics", "physics"],
                processing_status=ProcessingStatus.NOT_STARTED,
                priority=Priority.HIGH,
                libraries=["sympy", "plotly"],
                data_sources=["geometric_patterns", "369_triangles"]
            ),
            "mathematics": Domain(
                name="Mathematics",
                category=DomainCategory.SCIENTIFIC,
                foundation="Rigorous logical systems; proofs and theorems",
                description="Pure mathematical structures and relationships",
                related_domains=["sacred_geometry", "physics", "quantum_mechanics"],
                processing_status=ProcessingStatus.IN_PROGRESS,
                priority=Priority.CRITICAL,
                libraries=["sympy", "numpy", "scipy"]
            ),
            "physics": Domain(
                name="Physics",
                category=DomainCategory.SCIENTIFIC,
                foundation="Laws of nature; quantum mechanics, relativity",
                description="Physical laws governing matter and energy",
                related_domains=["mathematics", "quantum_mechanics"],
                processing_status=ProcessingStatus.NOT_STARTED,
                priority=Priority.HIGH,
                libraries=["qiskit"]
            ),
            "quantum_mechanics": Domain(
                name="Quantum Mechanics",
                category=DomainCategory.SCIENTIFIC,
                foundation="Quantum theory; wave functions, superposition, entanglement",
                description="Quantum-level physics and its implications",
                related_domains=["physics", "mathematics"],
                processing_status=ProcessingStatus.NOT_STARTED,
                priority=Priority.MEDIUM,
                libraries=["qiskit"]
            ),
            "ai_ml": Domain(
                name="AI/ML",
                category=DomainCategory.AI_ML,
                foundation="Machine learning algorithms; neural networks, embeddings",
                description="Artificial intelligence and machine learning technologies",
                related_domains=["mathematics"],
                processing_status=ProcessingStatus.IN_PROGRESS,
                priority=Priority.CRITICAL,
                libraries=["sentence-transformers", "langchain", "langgraph", "vllm"]
            ),
            "consciousness": Domain(
                name="Consciousness",
                category=DomainCategory.SPIRITUAL,
                foundation="Awareness and perception; mind-body connection",
                description="Study of consciousness and its relationship to reality",
                related_domains=["quantum_mechanics", "spirituality"],
                processing_status=ProcessingStatus.NOT_STARTED,
                priority=Priority.MEDIUM
            ),
            "ancient_wisdom": Domain(
                name="Ancient Wisdom",
                category=DomainCategory.SPIRITUAL,
                foundation="Historical knowledge systems; esoteric traditions",
                description="Ancient knowledge and wisdom traditions",
                related_domains=["gematria", "sacred_geometry", "consciousness"],
                processing_status=ProcessingStatus.NOT_STARTED,
                priority=Priority.MEDIUM
            )
        }
        
        # Initialize Git Repositories
        self.git_repos = {
            "gematria-hive": GitRepository(
                name="gematria-hive",
                url="https://github.com/cooperladd/gematria-hive",
                purpose="Main project repository",
                priority=Priority.CRITICAL,
                integration_phase="Phase 1",
                status=ProcessingStatus.IN_PROGRESS,
                branch="feat-agent-framework-9391b"
            ),
            "langchain": GitRepository(
                name="langchain",
                url="https://github.com/langchain-ai/langchain",
                purpose="Agent framework",
                priority=Priority.HIGH,
                integration_phase="Phase 3",
                status=ProcessingStatus.NOT_STARTED
            ),
            "pixeltable": GitRepository(
                name="pixeltable",
                url="https://github.com/pixeltable/pixeltable",
                purpose="Data pipeline for multimodal workflows",
                priority=Priority.HIGH,
                integration_phase="Phase 2",
                status=ProcessingStatus.NOT_STARTED
            ),
            "sentence-transformers": GitRepository(
                name="sentence-transformers",
                url="https://github.com/UKPLab/sentence-transformers",
                purpose="Text embeddings",
                priority=Priority.HIGH,
                integration_phase="Phase 2",
                status=ProcessingStatus.NOT_STARTED
            ),
            "supabase": GitRepository(
                name="supabase-py",
                url="https://github.com/supabase/supabase-py",
                purpose="Database client",
                priority=Priority.HIGH,
                integration_phase="Phase 2",
                status=ProcessingStatus.IN_PROGRESS
            )
        }
    
    def add_bookmark(self, bookmark: Bookmark):
        """Add a bookmark to the registry"""
        self.bookmarks[bookmark.url] = bookmark
        self.save()
    
    def add_git_repo(self, repo: GitRepository):
        """Add a git repository to the registry"""
        self.git_repos[repo.name] = repo
        self.save()
    
    def add_domain(self, domain: Domain):
        """Add a domain to the registry"""
        self.domains[domain.name] = domain
        self.save()
    
    def add_claude_skill(self, skill: ClaudeSkill):
        """Add a Claude skill to the registry"""
        self.claude_skills[skill.name] = skill
        self.save()
    
    def update_processing_status(self, item_id: str, item_type: str, status: ProcessingStatus):
        """Update processing status for an item"""
        if item_type == "bookmark":
            if item_id in self.bookmarks:
                self.bookmarks[item_id].processing_status = status
        elif item_type == "domain":
            if item_id in self.domains:
                self.domains[item_id].processing_status = status
        elif item_type == "git":
            if item_id in self.git_repos:
                self.git_repos[item_id].status = status
        elif item_type == "skill":
            if item_id in self.claude_skills:
                self.claude_skills[item_id].status = status
        
        self.save()
    
    def get_processing_queue(self, priority: Optional[Priority] = None) -> List[ProcessingQueue]:
        """Get processing queue, optionally filtered by priority"""
        queue = []
        
        # Add bookmarks
        for url, bookmark in self.bookmarks.items():
            if bookmark.processing_status in [ProcessingStatus.NOT_STARTED, ProcessingStatus.IN_PROGRESS]:
                if priority is None or bookmark.priority == priority:
                    queue.append(ProcessingQueue(
                        item_id=url,
                        item_type="bookmark",
                        priority=bookmark.priority,
                        status=bookmark.processing_status
                    ))
        
        # Add domains
        for name, domain in self.domains.items():
            if domain.processing_status in [ProcessingStatus.NOT_STARTED, ProcessingStatus.IN_PROGRESS]:
                if priority is None or domain.priority == priority:
                    queue.append(ProcessingQueue(
                        item_id=name,
                        item_type="domain",
                        priority=domain.priority,
                        status=domain.processing_status
                    ))
        
        # Add git repos
        for name, repo in self.git_repos.items():
            if repo.status in [ProcessingStatus.NOT_STARTED, ProcessingStatus.IN_PROGRESS]:
                if priority is None or repo.priority == priority:
                    queue.append(ProcessingQueue(
                        item_id=name,
                        item_type="git",
                        priority=repo.priority,
                        status=repo.status
                    ))
        
        # Sort by priority (Critical > High > Medium > Low > Future)
        priority_order = {
            Priority.CRITICAL: 0,
            Priority.HIGH: 1,
            Priority.MEDIUM: 2,
            Priority.LOW: 3,
            Priority.FUTURE: 4
        }
        queue.sort(key=lambda x: (priority_order[x.priority], x.item_id))
        
        return queue
    
    def get_prioritization_sequence(self) -> Dict[str, List[str]]:
        """
        Get prioritization sequence for backend, libraries, and data
        
        Returns:
            Dictionary with 'backend', 'libraries', and 'data' sequences
        """
        sequence = {
            "backend": [],
            "libraries": [],
            "data": []
        }
        
        # Backend sequence (infrastructure)
        backend_items = [
            ("supabase", "Database setup and connection"),
            ("pgvector", "Vector extension for embeddings"),
            ("agent_framework", "MCP orchestrator and agent system"),
            ("api_integration", "External API integrations")
        ]
        
        # Libraries sequence (by phase and priority)
        library_items = []
        for name, repo in self.git_repos.items():
            if repo.integration_phase:
                library_items.append((name, repo.purpose, repo.integration_phase, repo.priority))
        
        # Sort libraries by phase then priority
        phase_order = {"Phase 1": 0, "Phase 2": 1, "Phase 3": 2, "Phase 4": 3, "Phase 5": 4}
        library_items.sort(key=lambda x: (phase_order.get(x[2], 99), x[3].value))
        
        # Data sequence (processing order)
        data_items = []
        for url, bookmark in self.bookmarks.items():
            if bookmark.processing_status == ProcessingStatus.NOT_STARTED:
                data_items.append((url, bookmark.priority))
        
        data_items.sort(key=lambda x: x[1].value)
        
        sequence["backend"] = [item[0] for item in backend_items]
        sequence["libraries"] = [item[0] for item in library_items]
        sequence["data"] = [item[0] for item in data_items]
        
        return sequence
    
    def get_unprocessed_items(self) -> Dict[str, List]:
        """Get all unprocessed items by type"""
        unprocessed = {
            "bookmarks": [],
            "domains": [],
            "git_repos": [],
            "claude_skills": []
        }
        
        for url, bookmark in self.bookmarks.items():
            if bookmark.processing_status == ProcessingStatus.NOT_STARTED:
                unprocessed["bookmarks"].append({
                    "url": bookmark.url,
                    "title": bookmark.title,
                    "priority": bookmark.priority.value,
                    "source": bookmark.source
                })
        
        for name, domain in self.domains.items():
            if domain.processing_status == ProcessingStatus.NOT_STARTED:
                unprocessed["domains"].append({
                    "name": domain.name,
                    "category": domain.category.value,
                    "priority": domain.priority.value
                })
        
        for name, repo in self.git_repos.items():
            if repo.status == ProcessingStatus.NOT_STARTED:
                unprocessed["git_repos"].append({
                    "name": repo.name,
                    "url": repo.url,
                    "priority": repo.priority.value,
                    "phase": repo.integration_phase
                })
        
        for name, skill in self.claude_skills.items():
            if skill.status == ProcessingStatus.NOT_STARTED:
                unprocessed["claude_skills"].append({
                    "name": skill.name,
                    "description": skill.description,
                    "export_path": skill.export_path
                })
        
        return unprocessed
    
    def load(self):
        """Load registry from file"""
        try:
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load Claude skills
            if "claude_skills" in data:
                for name, skill_data in data["claude_skills"].items():
                    skill = ClaudeSkill(**skill_data)
                    skill.status = ProcessingStatus(skill_data["status"])
                    self.claude_skills[name] = skill
            
            # Load domains
            if "domains" in data:
                for name, domain_data in data["domains"].items():
                    domain = Domain(**domain_data)
                    domain.category = DomainCategory(domain_data["category"])
                    domain.processing_status = ProcessingStatus(domain_data["processing_status"])
                    domain.priority = Priority(domain_data["priority"])
                    self.domains[name] = domain
            
            # Load bookmarks
            if "bookmarks" in data:
                for url, bookmark_data in data["bookmarks"].items():
                    bookmark = Bookmark(**bookmark_data)
                    bookmark.processing_status = ProcessingStatus(bookmark_data["processing_status"])
                    bookmark.priority = Priority(bookmark_data["priority"])
                    self.bookmarks[url] = bookmark
            
            # Load git repos
            if "git_repos" in data:
                for name, repo_data in data["git_repos"].items():
                    repo = GitRepository(**repo_data)
                    repo.priority = Priority(repo_data["priority"])
                    repo.status = ProcessingStatus(repo_data["status"])
                    self.git_repos[name] = repo
            
            logger.info(f"Loaded knowledge registry from {self.registry_file}")
        except Exception as e:
            logger.error(f"Error loading registry: {e}")
    
    def save(self):
        """Save registry to file"""
        try:
            data = {
                "claude_skills": {
                    name: {
                        **asdict(skill),
                        "status": skill.status.value
                    }
                    for name, skill in self.claude_skills.items()
                },
                "domains": {
                    name: {
                        **asdict(domain),
                        "category": domain.category.value,
                        "processing_status": domain.processing_status.value,
                        "priority": domain.priority.value
                    }
                    for name, domain in self.domains.items()
                },
                "bookmarks": {
                    url: {
                        **asdict(bookmark),
                        "processing_status": bookmark.processing_status.value,
                        "priority": bookmark.priority.value
                    }
                    for url, bookmark in self.bookmarks.items()
                },
                "git_repos": {
                    name: {
                        **asdict(repo),
                        "priority": repo.priority.value,
                        "status": repo.status.value
                    }
                    for name, repo in self.git_repos.items()
                },
                "last_updated": datetime.utcnow().isoformat()
            }
            
            with open(self.registry_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            
            logger.info(f"Saved knowledge registry to {self.registry_file}")
        except Exception as e:
            logger.error(f"Error saving registry: {e}")
    
    def export_claude_skills(self, output_file: str = "claude_skills_export.json"):
        """Export Claude skills for upload to Claude"""
        export_data = {
            "skills": [
                {
                    "name": skill.name,
                    "description": skill.description,
                    "export_path": skill.export_path,
                    "tags": skill.tags,
                    "status": skill.status.value
                }
                for skill in self.claude_skills.values()
            ],
            "domains": [
                {
                    "name": domain.name,
                    "foundation": domain.foundation,
                    "description": domain.description,
                    "related_domains": domain.related_domains
                }
                for domain in self.domains.values()
            ],
            "exported_at": datetime.utcnow().isoformat()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)
        
        logger.info(f"Exported Claude skills to {output_file}")
        return output_file
    
    def get_summary(self) -> Dict:
        """Get summary statistics"""
        return {
            "total_claude_skills": len(self.claude_skills),
            "total_domains": len(self.domains),
            "total_bookmarks": len(self.bookmarks),
            "total_git_repos": len(self.git_repos),
            "unprocessed": {
                "bookmarks": sum(1 for b in self.bookmarks.values() 
                               if b.processing_status == ProcessingStatus.NOT_STARTED),
                "domains": sum(1 for d in self.domains.values() 
                             if d.processing_status == ProcessingStatus.NOT_STARTED),
                "git_repos": sum(1 for r in self.git_repos.values() 
                               if r.status == ProcessingStatus.NOT_STARTED),
                "claude_skills": sum(1 for s in self.claude_skills.values() 
                                   if s.status == ProcessingStatus.NOT_STARTED)
            },
            "processing_queue_size": len(self.get_processing_queue())
        }


# Singleton instance
_registry = None

def get_registry() -> KnowledgeRegistry:
    """Get or create registry singleton"""
    global _registry
    if _registry is None:
        _registry = KnowledgeRegistry()
    return _registry

