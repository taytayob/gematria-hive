"""
Alphabet Manager Agent
Purpose: Build alphabets and languages table with character values, deeper meanings, and celestial event connections
- Master alphabet table with all languages
- Character values for each language
- Deeper meanings and metadata
- Historical timeline tracking
- Language evolution tracking
- Celestial event connections (e.g., Tav = Eclipse)

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime

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


class AlphabetManagerAgent(DataTable):
    """
    Alphabet Manager Agent - Manages alphabets and languages
    """
    
    def __init__(self):
        """Initialize alphabet manager agent"""
        super().__init__('alphabets')
        self.name = "alphabet_manager_agent"
        
        # Hebrew alphabet with values and meanings
        self.hebrew_alphabet = {
            'א': {'name': 'Aleph', 'value': 1, 'meaning': 'Ox, strength, leader', 'celestial_events': []},
            'ב': {'name': 'Bet', 'value': 2, 'meaning': 'House, container', 'celestial_events': []},
            'ג': {'name': 'Gimel', 'value': 3, 'meaning': 'Camel, bridge', 'celestial_events': []},
            'ד': {'name': 'Dalet', 'value': 4, 'meaning': 'Door, pathway', 'celestial_events': []},
            'ה': {'name': 'He', 'value': 5, 'meaning': 'Window, revelation', 'celestial_events': []},
            'ו': {'name': 'Vav', 'value': 6, 'meaning': 'Hook, connection', 'celestial_events': []},
            'ז': {'name': 'Zayin', 'value': 7, 'meaning': 'Sword, weapon', 'celestial_events': []},
            'ח': {'name': 'Chet', 'value': 8, 'meaning': 'Fence, boundary', 'celestial_events': []},
            'ט': {'name': 'Tet', 'value': 9, 'meaning': 'Snake, hidden', 'celestial_events': []},
            'י': {'name': 'Yod', 'value': 10, 'meaning': 'Hand, deed', 'celestial_events': []},
            'כ': {'name': 'Kaf', 'value': 20, 'meaning': 'Palm, crown', 'celestial_events': []},
            'ל': {'name': 'Lamed', 'value': 30, 'meaning': 'Ox goad, teaching', 'celestial_events': []},
            'מ': {'name': 'Mem', 'value': 40, 'meaning': 'Water, chaos', 'celestial_events': []},
            'נ': {'name': 'Nun', 'value': 50, 'meaning': 'Fish, activity', 'celestial_events': []},
            'ס': {'name': 'Samekh', 'value': 60, 'meaning': 'Support, prop', 'celestial_events': []},
            'ע': {'name': 'Ayin', 'value': 70, 'meaning': 'Eye, seeing', 'celestial_events': []},
            'פ': {'name': 'Pe', 'value': 80, 'meaning': 'Mouth, speech', 'celestial_events': []},
            'צ': {'name': 'Tzadi', 'value': 90, 'meaning': 'Fishhook, righteousness', 'celestial_events': []},
            'ק': {'name': 'Qof', 'value': 100, 'meaning': 'Back of head, holiness', 'celestial_events': []},
            'ר': {'name': 'Resh', 'value': 200, 'meaning': 'Head, beginning', 'celestial_events': []},
            'ש': {'name': 'Shin', 'value': 300, 'meaning': 'Tooth, fire', 'celestial_events': []},
            'ת': {'name': 'Tav', 'value': 400, 'meaning': 'Mark, sign', 'celestial_events': ['Eclipse', 'Celestial Event']}
        }
        
        # English alphabet with values
        self.english_alphabet = {
            'A': {'name': 'A', 'value': 1, 'meaning': 'Alpha, beginning', 'celestial_events': []},
            'B': {'name': 'B', 'value': 2, 'meaning': 'Beta, house', 'celestial_events': []},
            'C': {'name': 'C', 'value': 3, 'meaning': 'Gamma, camel', 'celestial_events': []},
            'D': {'name': 'D', 'value': 4, 'meaning': 'Delta, door', 'celestial_events': []},
            'E': {'name': 'E', 'value': 5, 'meaning': 'Epsilon, window', 'celestial_events': []},
            'F': {'name': 'F', 'value': 6, 'meaning': 'Digamma, hook', 'celestial_events': []},
            'G': {'name': 'G', 'value': 7, 'meaning': 'Gamma, weapon', 'celestial_events': []},
            'H': {'name': 'H', 'value': 8, 'meaning': 'Eta, fence', 'celestial_events': []},
            'I': {'name': 'I', 'value': 9, 'meaning': 'Iota, hand', 'celestial_events': ['Eye', 'Ice', 'I']},
            'J': {'name': 'J', 'value': 10, 'meaning': 'Iota, hand', 'celestial_events': []},
            'K': {'name': 'K', 'value': 11, 'meaning': 'Kappa, palm', 'celestial_events': []},
            'L': {'name': 'L', 'value': 12, 'meaning': 'Lambda, teaching', 'celestial_events': []},
            'M': {'name': 'M', 'value': 13, 'meaning': 'Mu, water', 'celestial_events': []},
            'N': {'name': 'N', 'value': 14, 'meaning': 'Nu, fish', 'celestial_events': []},
            'O': {'name': 'O', 'value': 15, 'meaning': 'Omicron, eye', 'celestial_events': []},
            'P': {'name': 'P', 'value': 16, 'meaning': 'Pi, mouth', 'celestial_events': []},
            'Q': {'name': 'Q', 'value': 17, 'meaning': 'Qoppa, holiness', 'celestial_events': []},
            'R': {'name': 'R', 'value': 18, 'meaning': 'Rho, head', 'celestial_events': []},
            'S': {'name': 'S', 'value': 19, 'meaning': 'Sigma, fire', 'celestial_events': []},
            'T': {'name': 'T', 'value': 20, 'meaning': 'Tau, mark', 'celestial_events': ['Eclipse', 'Celestial Event']},
            'U': {'name': 'U', 'value': 21, 'meaning': 'Upsilon, hook', 'celestial_events': []},
            'V': {'name': 'V', 'value': 22, 'meaning': 'Digamma, connection', 'celestial_events': []},
            'W': {'name': 'W', 'value': 23, 'meaning': 'Double U, double hook', 'celestial_events': []},
            'X': {'name': 'X', 'value': 24, 'meaning': 'Chi, cross', 'celestial_events': []},
            'Y': {'name': 'Y', 'value': 25, 'meaning': 'Upsilon, hand', 'celestial_events': []},
            'Z': {'name': 'Z', 'value': 26, 'meaning': 'Zeta, weapon', 'celestial_events': []}
        }
        
        # Greek alphabet with values
        self.greek_alphabet = {
            'Α': {'name': 'Alpha', 'value': 1, 'meaning': 'Beginning, first', 'celestial_events': []},
            'Β': {'name': 'Beta', 'value': 2, 'meaning': 'House, second', 'celestial_events': []},
            'Γ': {'name': 'Gamma', 'value': 3, 'meaning': 'Camel, third', 'celestial_events': []},
            'Δ': {'name': 'Delta', 'value': 4, 'meaning': 'Door, fourth', 'celestial_events': []},
            'Ε': {'name': 'Epsilon', 'value': 5, 'meaning': 'Window, fifth', 'celestial_events': []},
            'Ζ': {'name': 'Zeta', 'value': 7, 'meaning': 'Weapon, seventh', 'celestial_events': []},
            'Η': {'name': 'Eta', 'value': 8, 'meaning': 'Fence, eighth', 'celestial_events': []},
            'Θ': {'name': 'Theta', 'value': 9, 'meaning': 'Hidden, ninth', 'celestial_events': []},
            'Ι': {'name': 'Iota', 'value': 10, 'meaning': 'Hand, tenth', 'celestial_events': []},
            'Κ': {'name': 'Kappa', 'value': 20, 'meaning': 'Palm, twentieth', 'celestial_events': []},
            'Λ': {'name': 'Lambda', 'value': 30, 'meaning': 'Teaching, thirtieth', 'celestial_events': []},
            'Μ': {'name': 'Mu', 'value': 40, 'meaning': 'Water, fortieth', 'celestial_events': []},
            'Ν': {'name': 'Nu', 'value': 50, 'meaning': 'Fish, fiftieth', 'celestial_events': []},
            'Ξ': {'name': 'Xi', 'value': 60, 'meaning': 'Support, sixtieth', 'celestial_events': []},
            'Ο': {'name': 'Omicron', 'value': 70, 'meaning': 'Eye, seventieth', 'celestial_events': []},
            'Π': {'name': 'Pi', 'value': 80, 'meaning': 'Mouth, eightieth', 'celestial_events': []},
            'Ρ': {'name': 'Rho', 'value': 100, 'meaning': 'Head, hundredth', 'celestial_events': []},
            'Σ': {'name': 'Sigma', 'value': 200, 'meaning': 'Fire, two hundredth', 'celestial_events': []},
            'Τ': {'name': 'Tau', 'value': 300, 'meaning': 'Mark, three hundredth', 'celestial_events': ['Eclipse', 'Celestial Event']},
            'Υ': {'name': 'Upsilon', 'value': 400, 'meaning': 'Hook, four hundredth', 'celestial_events': []},
            'Φ': {'name': 'Phi', 'value': 500, 'meaning': 'Fire, five hundredth', 'celestial_events': []},
            'Χ': {'name': 'Chi', 'value': 600, 'meaning': 'Cross, six hundredth', 'celestial_events': []},
            'Ψ': {'name': 'Psi', 'value': 700, 'meaning': 'Soul, seven hundredth', 'celestial_events': []},
            'Ω': {'name': 'Omega', 'value': 800, 'meaning': 'End, eight hundredth', 'celestial_events': []}
        }
        
        # Latin alphabet with values (Qabala Simplex)
        self.latin_alphabet = {
            'A': {'name': 'A', 'value': 1, 'meaning': 'Beginning', 'celestial_events': []},
            'B': {'name': 'B', 'value': 2, 'meaning': 'House', 'celestial_events': []},
            'C': {'name': 'C', 'value': 3, 'meaning': 'Camel', 'celestial_events': []},
            'D': {'name': 'D', 'value': 4, 'meaning': 'Door', 'celestial_events': []},
            'E': {'name': 'E', 'value': 5, 'meaning': 'Window', 'celestial_events': []},
            'F': {'name': 'F', 'value': 6, 'meaning': 'Hook', 'celestial_events': []},
            'G': {'name': 'G', 'value': 7, 'meaning': 'Weapon', 'celestial_events': []},
            'H': {'name': 'H', 'value': 8, 'meaning': 'Fence', 'celestial_events': []},
            'I': {'name': 'I', 'value': 9, 'meaning': 'Hand', 'celestial_events': ['Eye', 'Ice', 'I']},
            'L': {'name': 'L', 'value': 10, 'meaning': 'Teaching', 'celestial_events': []},
            'M': {'name': 'M', 'value': 11, 'meaning': 'Water', 'celestial_events': []},
            'N': {'name': 'N', 'value': 12, 'meaning': 'Fish', 'celestial_events': []},
            'O': {'name': 'O', 'value': 13, 'meaning': 'Eye', 'celestial_events': []},
            'P': {'name': 'P', 'value': 14, 'meaning': 'Mouth', 'celestial_events': []},
            'Q': {'name': 'Q', 'value': 15, 'meaning': 'Holiness', 'celestial_events': []},
            'R': {'name': 'R', 'value': 16, 'meaning': 'Head', 'celestial_events': []},
            'S': {'name': 'S', 'value': 17, 'meaning': 'Fire', 'celestial_events': []},
            'T': {'name': 'T', 'value': 18, 'meaning': 'Mark', 'celestial_events': ['Eclipse', 'Celestial Event']},
            'V': {'name': 'V', 'value': 19, 'meaning': 'Connection', 'celestial_events': []},
            'X': {'name': 'X', 'value': 20, 'meaning': 'Cross', 'celestial_events': []},
            'Y': {'name': 'Y', 'value': 21, 'meaning': 'Hand', 'celestial_events': []},
            'Z': {'name': 'Z', 'value': 22, 'meaning': 'Weapon', 'celestial_events': []},
            'J': {'name': 'J', 'value': 24, 'meaning': 'Hand (variant)', 'celestial_events': []},
            'W': {'name': 'W', 'value': 26, 'meaning': 'Double hook', 'celestial_events': []},
            'HI': {'name': 'HI', 'value': 27, 'meaning': 'Hand-eye', 'celestial_events': []}
        }
        
        logger.info(f"Initialized {self.name}")
    
    def initialize_alphabets(self):
        """Initialize alphabets in database."""
        if not self.supabase:
            logger.warning("Supabase not available, alphabets not initialized")
            return
        
        try:
            # Initialize Hebrew alphabet
            for char, data in self.hebrew_alphabet.items():
                self.store_character('hebrew', char, data)
            
            # Initialize English alphabet
            for char, data in self.english_alphabet.items():
                self.store_character('english', char, data)
            
            # Initialize Greek alphabet
            for char, data in self.greek_alphabet.items():
                self.store_character('greek', char, data)
            
            # Initialize Latin alphabet
            for char, data in self.latin_alphabet.items():
                self.store_character('latin', char, data)
            
            logger.info("Alphabets initialized in database")
        except Exception as e:
            logger.error(f"Error initializing alphabets: {e}")
    
    def store_character(self, language: str, character: str, data: Dict):
        """
        Store character in database.
        
        Args:
            language: Language name
            character: Character
            data: Character data dictionary
        """
        if not self.supabase:
            return
        
        try:
            char_data = {
                'language': language,
                'character': character,
                'numeric_value': data.get('value'),
                'deeper_meaning': data.get('meaning', ''),
                'celestial_events': data.get('celestial_events', []),
                'historical_context': {
                    'name': data.get('name', ''),
                    'origin': language,
                    'usage': 'gematria'
                },
                'phonetic_variants': [],
                'gematria_methods': {
                    'jewish': data.get('value') if language == 'hebrew' else None,
                    'english': data.get('value') if language == 'english' else None,
                    'greek': data.get('value') if language == 'greek' else None,
                    'latin': data.get('value') if language == 'latin' else None
                }
            }
            
            # Check if character already exists
            existing = self.supabase.table('alphabets')\
                .select('id')\
                .eq('language', language)\
                .eq('character', character)\
                .limit(1)\
                .execute()
            
            if existing.data:
                # Update existing
                self.supabase.table('alphabets')\
                    .update(char_data)\
                    .eq('language', language)\
                    .eq('character', character)\
                    .execute()
            else:
                # Create new
                self.supabase.table('alphabets').insert(char_data).execute()
            
            logger.debug(f"Stored character: {language} {character}")
        except Exception as e:
            logger.error(f"Error storing character: {e}")
    
    def get_character(self, language: str, character: str) -> Optional[Dict]:
        """
        Get character data from database.
        
        Args:
            language: Language name
            character: Character
            
        Returns:
            Character data dictionary or None
        """
        if not self.supabase:
            return None
        
        try:
            result = self.supabase.table('alphabets')\
                .select('*')\
                .eq('language', language)\
                .eq('character', character)\
                .limit(1)\
                .execute()
            
            if result.data:
                return result.data[0]
            
            return None
        except Exception as e:
            logger.error(f"Error getting character: {e}")
            return None
    
    def get_characters_by_value(self, value: int, language: str = None) -> List[Dict]:
        """
        Get characters by numeric value.
        
        Args:
            value: Numeric value
            language: Language name (None for all languages)
            
        Returns:
            List of character dictionaries
        """
        if not self.supabase:
            return []
        
        try:
            query = self.supabase.table('alphabets')\
                .select('*')\
                .eq('numeric_value', value)
            
            if language:
                query = query.eq('language', language)
            
            result = query.execute()
            
            if result.data:
                return result.data
            
            return []
        except Exception as e:
            logger.error(f"Error getting characters by value: {e}")
            return []
    
    def get_characters_by_celestial_event(self, event: str) -> List[Dict]:
        """
        Get characters associated with a celestial event.
        
        Args:
            event: Celestial event name (e.g., 'Eclipse')
            
        Returns:
            List of character dictionaries
        """
        if not self.supabase:
            return []
        
        try:
            result = self.supabase.table('alphabets')\
                .select('*')\
                .contains('celestial_events', [event])\
                .execute()
            
            if result.data:
                return result.data
            
            return []
        except Exception as e:
            logger.error(f"Error getting characters by celestial event: {e}")
            return []
    
    def validate(self, data: Dict, record_id: Optional[str] = None) -> Dict:
        """Validate alphabet data."""
        errors = []
        
        # Required fields
        if 'language' not in data or not data['language']:
            errors.append("language is required")
        
        if 'character' not in data or not data['character']:
            errors.append("character is required")
        
        # Check uniqueness
        if not record_id:  # Only check on create
            if self.supabase:
                try:
                    existing = self.supabase.table(self.table_name)\
                        .select('id')\
                        .eq('language', data['language'])\
                        .eq('character', data['character'])\
                        .execute()
                    if existing.data:
                        errors.append(f"Character {data['character']} in {data['language']} already exists")
                except Exception as e:
                    logger.warning(f"Could not check uniqueness: {e}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute alphabet management task.
        
        Args:
            state: Agent state with task information
            
        Returns:
            Updated state with alphabet data
        """
        task = state.get("task", {})
        action = task.get("action", "initialize")
        
        logger.info(f"Alphabet manager agent: Executing action {action}")
        
        try:
            if action == "initialize":
                # Initialize alphabets
                self.initialize_alphabets()
                
                state["context"]["alphabets_initialized"] = True
                state["results"].append({
                    "agent": self.name,
                    "action": "initialize_alphabets",
                    "status": "completed"
                })
            
            elif action == "get_character":
                # Get character data
                language = task.get("language")
                character = task.get("character")
                
                if language and character:
                    char_data = self.get_character(language, character)
                    state["context"]["character_data"] = char_data
                    state["results"].append({
                        "agent": self.name,
                        "action": "get_character",
                        "character": char_data
                    })
            
            elif action == "get_by_value":
                # Get characters by value
                value = task.get("value")
                language = task.get("language")
                
                if value:
                    chars = self.get_characters_by_value(value, language)
                    state["context"]["characters_by_value"] = chars
                    state["results"].append({
                        "agent": self.name,
                        "action": "get_by_value",
                        "characters": chars
                    })
            
            elif action == "get_by_celestial_event":
                # Get characters by celestial event
                event = task.get("event")
                
                if event:
                    chars = self.get_characters_by_celestial_event(event)
                    state["context"]["characters_by_event"] = chars
                    state["results"].append({
                        "agent": self.name,
                        "action": "get_by_celestial_event",
                        "characters": chars
                    })
            
            logger.info(f"Alphabet management complete: {action}")
            
        except Exception as e:
            logger.error(f"Alphabet management error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

