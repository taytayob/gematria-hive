"""
Note-Taking System

Purpose: Centralized note-taking system for observations, advice, and mentoring
notes. Provides unified interface for all note-taking activities.

Author: Gematria Hive Team
Date: January 6, 2025
"""

import logging
import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

try:
    from supabase import create_client, Client
    HAS_SUPABASE = True
except ImportError:
    HAS_SUPABASE = False
    print("Warning: supabase not installed, notes will use file-based storage only")

logger = logging.getLogger(__name__)


class NoteTakingSystem:
    """
    Centralized Note-Taking System
    
    Operations:
    - Unified note-taking interface
    - Search and retrieval of notes
    - Note categorization and tagging
    - Integration with observer, advisor, and mentor agents
    """
    
    def __init__(self, notes_dir: str = None):
        """
        Initialize note-taking system
        
        Args:
            notes_dir: Base directory for notes (default: ./notes)
        """
        self.notes_dir = Path(notes_dir) if notes_dir else Path("./notes")
        self.notes_dir.mkdir(parents=True, exist_ok=True)
        
        # Subdirectories
        self.observations_dir = self.notes_dir / "observations"
        self.advice_dir = self.notes_dir / "advice"
        self.mentoring_dir = self.notes_dir / "mentoring"
        self.general_dir = self.notes_dir / "general"
        
        for dir_path in [self.observations_dir, self.advice_dir, 
                        self.mentoring_dir, self.general_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Supabase for persistent storage
        if HAS_SUPABASE:
            supabase_url = os.getenv('SUPABASE_URL')
            supabase_key = os.getenv('SUPABASE_KEY')
            if supabase_url and supabase_key:
                self.supabase = create_client(supabase_url, supabase_key)
                logger.info("Note-taking system: Supabase connected")
            else:
                self.supabase = None
        else:
            self.supabase = None
        
        logger.info(f"Initialized note-taking system with base directory: {self.notes_dir}")
    
    def take_note(self, note_type: str, content: Dict[str, Any], 
                  tags: List[str] = None, category: str = None) -> str:
        """
        Take a note
        
        Args:
            note_type: Type of note (observation, advice, mentoring, general)
            content: Note content dictionary
            tags: Optional list of tags
            category: Optional category
            
        Returns:
            Note ID
        """
        note_id = f"note_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        note = {
            "id": note_id,
            "type": note_type,
            "timestamp": datetime.utcnow().isoformat(),
            "content": content,
            "tags": tags or [],
            "category": category or "general"
        }
        
        # Save to appropriate directory
        date_str = datetime.now().strftime("%Y%m%d")
        
        if note_type == "observation":
            filepath = self.observations_dir / f"notes_{date_str}.jsonl"
        elif note_type == "advice":
            filepath = self.advice_dir / f"notes_{date_str}.jsonl"
        elif note_type == "mentoring":
            filepath = self.mentoring_dir / f"notes_{date_str}.jsonl"
        else:
            filepath = self.general_dir / f"notes_{date_str}.jsonl"
        
        with open(filepath, 'a') as f:
            f.write(json.dumps(note) + '\n')
        
        # Save to Supabase if available
        if self.supabase:
            try:
                self.supabase.table("notes").insert({
                    "note_id": note_id,
                    "note_type": note_type,
                    "timestamp": note["timestamp"],
                    "content": json.dumps(content),
                    "tags": tags or [],
                    "category": category or "general"
                }).execute()
            except Exception as e:
                logger.error(f"Error saving note to Supabase: {e}")
        
        logger.debug(f"Note taken: {note_type} - {note_id}")
        return note_id
    
    def search_notes(self, query: str = None, note_type: str = None,
                    tags: List[str] = None, category: str = None,
                    start_date: datetime = None, end_date: datetime = None,
                    limit: int = 100) -> List[Dict[str, Any]]:
        """
        Search notes
        
        Args:
            query: Text query to search for
            note_type: Filter by note type
            tags: Filter by tags
            category: Filter by category
            start_date: Start date filter
            end_date: End date filter
            limit: Maximum number of results
            
        Returns:
            List of matching notes
        """
        results = []
        
        # Determine which directories to search
        dirs_to_search = []
        if note_type == "observation" or not note_type:
            dirs_to_search.append(self.observations_dir)
        if note_type == "advice" or not note_type:
            dirs_to_search.append(self.advice_dir)
        if note_type == "mentoring" or not note_type:
            dirs_to_search.append(self.mentoring_dir)
        if note_type == "general" or not note_type:
            dirs_to_search.append(self.general_dir)
        
        # Search files
        for dir_path in dirs_to_search:
            for file_path in dir_path.glob("notes_*.jsonl"):
                try:
                    with open(file_path, 'r') as f:
                        for line in f:
                            note = json.loads(line.strip())
                            
                            # Apply filters
                            if note_type and note.get("type") != note_type:
                                continue
                            
                            if tags and not any(tag in note.get("tags", []) for tag in tags):
                                continue
                            
                            if category and note.get("category") != category:
                                continue
                            
                            note_date = datetime.fromisoformat(note.get("timestamp", ""))
                            if start_date and note_date < start_date:
                                continue
                            if end_date and note_date > end_date:
                                continue
                            
                            # Text search
                            if query:
                                query_lower = query.lower()
                                content_str = json.dumps(note.get("content", {})).lower()
                                if query_lower not in content_str:
                                    continue
                            
                            results.append(note)
                            
                            if len(results) >= limit:
                                return results
                
                except Exception as e:
                    logger.error(f"Error reading note file {file_path}: {e}")
        
        # Sort by timestamp (newest first)
        results.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        return results[:limit]
    
    def get_recent_notes(self, hours: int = 24, note_type: str = None,
                        limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent notes
        
        Args:
            hours: Number of hours to look back
            note_type: Optional note type filter
            limit: Maximum number of results
            
        Returns:
            List of recent notes
        """
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        return self.search_notes(
            note_type=note_type,
            start_date=cutoff,
            limit=limit
        )
    
    def get_note_summary(self, hours: int = 24) -> Dict[str, Any]:
        """
        Get summary of notes
        
        Args:
            hours: Number of hours to summarize
            
        Returns:
            Summary dictionary
        """
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        
        observations = self.search_notes(
            note_type="observation",
            start_date=cutoff,
            limit=1000
        )
        
        advice = self.search_notes(
            note_type="advice",
            start_date=cutoff,
            limit=1000
        )
        
        mentoring = self.search_notes(
            note_type="mentoring",
            start_date=cutoff,
            limit=1000
        )
        
        general = self.search_notes(
            note_type="general",
            start_date=cutoff,
            limit=1000
        )
        
        # Count by category
        categories = {}
        for note in observations + advice + mentoring + general:
            cat = note.get("category", "general")
            categories[cat] = categories.get(cat, 0) + 1
        
        # Count by tags
        tag_counts = {}
        for note in observations + advice + mentoring + general:
            for tag in note.get("tags", []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        summary = {
            "timestamp": datetime.utcnow().isoformat(),
            "period_hours": hours,
            "total_notes": len(observations) + len(advice) + len(mentoring) + len(general),
            "by_type": {
                "observations": len(observations),
                "advice": len(advice),
                "mentoring": len(mentoring),
                "general": len(general)
            },
            "by_category": categories,
            "top_tags": dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        }
        
        return summary
    
    def save_summary(self, filepath: str = None) -> str:
        """
        Save note summary to file
        
        Args:
            filepath: Optional filepath (default: notes/summary_YYYYMMDD.json)
            
        Returns:
            Path to saved file
        """
        if not filepath:
            date_str = datetime.now().strftime("%Y%m%d")
            filepath = self.notes_dir / f"summary_{date_str}.json"
        
        summary = self.get_note_summary(hours=168)  # Last week
        
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Note summary saved to: {filepath}")
        return str(filepath)


# Singleton instance
_note_system = None

def get_note_system(notes_dir: str = None) -> NoteTakingSystem:
    """Get or create note-taking system singleton"""
    global _note_system
    if _note_system is None:
        _note_system = NoteTakingSystem(notes_dir)
    return _note_system




