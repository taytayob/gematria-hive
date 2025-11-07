"""
Supabase Python Integration Script (Ingestion Pass #1)

Purpose: Foundation for ingestion - Pulling data, understanding category/relevance,
logging all steps, segmenting scope into phases.

Optimized for efficiency (chunking for large data, StringZilla for fast text ops)
and future-proofed (modular functions for adding agents/MCP, master/dynamic DB copies).

Author: Gematria Hive Team
Date: November 6, 2025
"""

import os
import json
import logging
from typing import List, Dict, Tuple, Optional
from datetime import datetime

# Core dependencies
try:
    from supabase import create_client, Client
    HAS_SUPABASE_LIB = True
except ImportError:
    HAS_SUPABASE_LIB = False
    Client = None

try:
    from sentence_transformers import SentenceTransformer, util
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False
    SentenceTransformer = None
    util = None

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    pd = None

# Performance optimizations
try:
    import stringzilla as sz  # Fast string ops
    HAS_STRINGZILLA = True
except ImportError:
    HAS_STRINGZILLA = False
    print("Warning: stringzilla not installed, using standard string ops")

# Future-proofed libraries (some may be optional for pass #1)
try:
    from pixeltable import create_dir, create_table, udf, Array, String, Float32
    HAS_PIXELTABLE = True
except ImportError:
    HAS_PIXELTABLE = False
    print("Warning: pixeltable not installed, using direct Supabase ingestion")

try:
    from langchain.agents import create_react_agent
    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False
    print("Warning: langchain not installed, agent features disabled")

try:
    from langgraph.graph import StateGraph
    HAS_LANGGRAPH = True
except ImportError:
    HAS_LANGGRAPH = False
    print("Warning: langgraph not installed, graph flows disabled")

try:
    from vllm import LLM
    HAS_VLLM = True
except ImportError:
    HAS_VLLM = False
    print("Warning: vllm not installed, using standard inference")

# Image/OCR processing
try:
    import cv2
    import pytesseract
    from PIL import Image
    HAS_OCR = True
except ImportError:
    HAS_OCR = False
    print("Warning: OCR libraries not installed, photo processing disabled")

# Web scraping
try:
    import requests
    from bs4 import BeautifulSoup
    HAS_SCRAPING = True
except ImportError:
    HAS_SCRAPING = False
    print("Warning: scraping libraries not installed, URL pulls disabled")

# Quantum sims (future-proofing)
try:
    import qiskit
    HAS_QISKIT = True
except ImportError:
    HAS_QISKIT = False
    print("Warning: qiskit not installed, quantum sims disabled")

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Logging setup (consolidate to file/console for full visibility/hunches)
# Must be before Supabase check to use logger
logging.basicConfig(
    filename='ingestion_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'  # Append mode
)
logger = logging.getLogger()
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

# Environment variables (set in .replit or .env)
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Make Supabase optional for imports - fail gracefully at runtime
HAS_SUPABASE = bool(SUPABASE_URL and SUPABASE_KEY)
if not HAS_SUPABASE:
    logger.warning("SUPABASE_URL and SUPABASE_KEY not set - database operations will be disabled")

# Consolidated vision keywords for relevance (from project—expand dynamically)
VISION_KEYWORDS = [
    'gematria', 'numerology', 'sacred geometry', 'vibration', 'harmonics',
    'quantum', 'duality', '369', 'Pi', 'esoteric', 'consciousness', 'DNA',
    'frequencies', 'light', 'love', 'synchronicity', 'ancient wisdom',
    'occult', 'mysticism', 'spirituality', 'mathematics', 'physics'
]

# Supabase client (consolidate connection)
supabase: Optional[Client] = None
if HAS_SUPABASE and HAS_SUPABASE_LIB:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        logger.warning(f"Could not initialize Supabase client: {e}")
        supabase = None
else:
    if not HAS_SUPABASE_LIB:
        logger.warning("Supabase library not installed - install with: pip install supabase")
    else:
        logger.warning("Supabase client not initialized - set SUPABASE_URL and SUPABASE_KEY to enable")

# Embedding model (consolidate for relevance scoring)
embed_model = None
vision_embeds = None
if HAS_SENTENCE_TRANSFORMERS:
    try:
        embed_model = SentenceTransformer('all-MiniLM-L6-v2')
        vision_embeds = embed_model.encode(VISION_KEYWORDS)  # Pre-embed for cosine checks
    except Exception as e:
        logger.warning(f"Could not initialize embedding model: {e}")
        embed_model = None
        vision_embeds = None
else:
    logger.warning("sentence-transformers not installed - embeddings will be disabled")

logger.info(f"Initialized with {len(VISION_KEYWORDS)} vision keywords")


def pull_data(source: str = 'dewey_json.json') -> List[Dict]:
    """
    Pull/extract data (manual/JSON for pass #1; future: agents/Dewey API).
    
    Args:
        source: Path to JSON file, CSV file, image file, or URL
        
    Returns:
        List of dictionaries with 'url', 'summary', and 'tags' keys
    """
    data = []
    
    # CSV file detection and routing
    if source.endswith('.csv'):
        try:
            from ingest_csv import ingest_csv_file
            logger.info(f"Detected CSV file: {source}, routing to CSV ingestion module")
            # CSV ingestion handles its own processing and database insertion
            # Return empty list as CSV ingestion is handled separately
            results = ingest_csv_file(source)
            if results.get('success'):
                logger.info(f"CSV ingestion completed: {results.get('total_ingested', 0)} rows ingested")
                # Return minimal data structure for compatibility
                return [{'url': source, 'summary': f"CSV ingestion completed: {results.get('total_ingested', 0)} rows", 'tags': ['csv', 'gematria']}]
            else:
                logger.error(f"CSV ingestion failed: {results.get('error', 'Unknown error')}")
                return []
        except ImportError:
            logger.error("CSV ingestion module (ingest_csv.py) not found")
            return []
        except Exception as e:
            logger.error(f"Error routing CSV file to ingestion module: {e}")
            return []
    
    elif source.endswith('.json'):
        try:
            with open(source, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Loaded {len(data)} items from JSON file: {source}")
        except FileNotFoundError:
            logger.error(f"JSON file not found: {source}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {source}: {e}")
            return []
            
    elif HAS_OCR and (source.endswith('.jpg') or source.endswith('.png') or 
                      source.endswith('.jpeg') or source.endswith('.gif')):
        # Photo OCR
        try:
            img = cv2.imread(source)
            if img is None:
                logger.error(f"Could not read image: {source}")
                return []
            text = pytesseract.image_to_string(Image.fromarray(img))
            data = [{'url': source, 'summary': text, 'tags': []}]
            logger.info(f"Extracted text from image: {source}")
        except Exception as e:
            logger.error(f"Error processing image {source}: {e}")
            return []
            
    elif HAS_SCRAPING and source.startswith('http'):
        # URL pull
        try:
            response = requests.get(source, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            data = [{'url': source, 'summary': text, 'tags': []}]
            logger.info(f"Scraped content from URL: {source}")
        except Exception as e:
            logger.error(f"Error scraping URL {source}: {e}")
            return []
    else:
        logger.error(f"Unsupported source type: {source}")
        return []
    
    logger.info(f"Pulled {len(data)} items from {source}")
    return data


def categorize_relevance(item: Dict) -> Tuple[str, float, List[str]]:
    """
    Understand category/relevance: Embed summary, cosine to vision, tag/phase segment.
    
    Args:
        item: Dictionary with 'summary' key
        
    Returns:
        Tuple of (phase, max_score, tags)
    """
    if not item.get('summary'):
        return 'phase1_basic', 0.0, []
    
    # Normalize summary text
    summary = item['summary']
    if HAS_STRINGZILLA:
        summary = sz.normalize(summary)
    
    # Embed and compute similarity
    item_emb = embed_model.encode(summary)
    scores = util.cos_sim(item_emb, vision_embeds)[0]
    max_score = float(scores.max().item())
    
    # Segment for further processing
    phase = 'phase1_basic' if max_score > 0.5 else 'phase2_deep'
    
    # Consolidate tags (threshold: 0.5)
    tags = [VISION_KEYWORDS[i] for i, score in enumerate(scores) if float(score.item()) > 0.5]
    
    logger.info(f"Item {item.get('url', 'unknown')}: Relevance {max_score:.3f}, phase {phase}, tags {tags}")
    return phase, max_score, tags


def ingest_to_db(data: List[Dict]) -> int:
    """
    Ingestion: Process data and insert to Supabase (master copy).
    
    Args:
        data: List of dictionaries with item data
        
    Returns:
        Number of items successfully ingested
    """
    # First pass: categorize all items and collect summaries for batch embedding
    items_with_metadata = []
    summaries = []
    summary_to_index = {}
    
    for idx, item in enumerate(data):
        try:
            phase, score, tags = categorize_relevance(item)
            summary = item.get('summary', '')
            
            items_with_metadata.append({
                'item': item,
                'phase': phase,
                'score': score,
                'tags': tags,
                'summary': summary
            })
            
            # Collect unique summaries for batch embedding
            if summary and summary not in summary_to_index:
                summary_to_index[summary] = len(summaries)
                summaries.append(summary)
                
        except Exception as e:
            logger.error(f"Error processing item {item.get('url', 'unknown')}: {e}")
            continue
    
    # Batch generate embeddings (5-10x faster than sequential)
    embedding_dict = {}
    if summaries:
        try:
            logger.info(f"Generating embeddings for {len(summaries)} unique summaries in batch...")
            # Use batch_size=32 for optimal performance
            embeddings_batch = embed_model.encode(
                summaries,
                batch_size=32,
                show_progress_bar=True,
                convert_to_numpy=True
            )
            
            # Map embeddings back to summaries
            for summary, embedding in zip(summaries, embeddings_batch):
                embedding_dict[summary] = embedding.tolist()
            
            logger.info(f"Batch embedding generation complete: {len(embeddings_batch)} embeddings")
        except Exception as e:
            logger.error(f"Error in batch embedding generation: {e}")
            # Fallback to sequential if batch fails
            logger.warning("Falling back to sequential embedding generation")
            for summary in summaries:
                try:
                    embedding = embed_model.encode(summary).tolist()
                    embedding_dict[summary] = embedding
                except Exception as e2:
                    logger.warning(f"Error generating embedding for summary: {e2}")
    
    # Second pass: create insert data with batch-generated embeddings
    insert_data = []
    successful = 0
    
    for metadata in items_with_metadata:
        try:
            item = metadata['item']
            summary = metadata['summary']
            
            # Prepare data for Supabase
            supabase_item = {
                'url': item.get('url', ''),
                'summary': summary,
                'tags': metadata['tags'],
                'phase': metadata['phase'],
                'relevance_score': metadata['score'],
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Get embedding from batch-generated dict
            if summary:
                embedding = embedding_dict.get(summary)
                if embedding:
                    supabase_item['embedding'] = embedding
            
            insert_data.append(supabase_item)
            
        except Exception as e:
            logger.error(f"Error preparing item {item.get('url', 'unknown')}: {e}")
            continue
    
    # Batch insert to Supabase
    if not HAS_SUPABASE or not supabase:
        logger.error("Supabase not configured - cannot insert data. Set SUPABASE_URL and SUPABASE_KEY.")
        return 0
    
    if insert_data:
        try:
            # Insert in chunks to avoid payload limits
            chunk_size = 50
            for i in range(0, len(insert_data), chunk_size):
                chunk = insert_data[i:i+chunk_size]
                result = supabase.table('bookmarks').insert(chunk).execute()
                successful += len(chunk)
                logger.info(f"Inserted chunk of {len(chunk)} items to Supabase")
        except Exception as e:
            logger.error(f"Error inserting to Supabase: {e}")
            # Try individual inserts as fallback
            for item in insert_data:
                try:
                    supabase.table('bookmarks').insert(item).execute()
                    successful += 1
                except Exception as e2:
                    logger.error(f"Error inserting individual item: {e2}")
    
    # Log hunch for leaps
    try:
        avg_relevance = sum(score for _, score, _ in [categorize_relevance(d) for d in data]) / len(data) if data else 0.0
        hunch_content = f"Ingestion pass #1 complete: {successful} items ingested, avg relevance {avg_relevance:.3f}"
        supabase.table('hunches').insert({
            'content': hunch_content,
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'completed',
            'cost': 0.0  # Track costs in future
        }).execute()
        logger.info(f"Logged hunch: {hunch_content}")
    except Exception as e:
        logger.error(f"Error logging hunch: {e}")
    
    logger.info(f"Ingestion complete: {successful}/{len(data)} items successfully ingested")
    return successful


def run_ingestion_pass1(source: str = 'dewey_json.json', chunk_size: int = 50) -> Dict:
    """
    Main Pass #1 ingestion function (optimize with chunks for large data).
    
    Args:
        source: Path to data source (JSON, image, or URL)
        chunk_size: Number of items to process per chunk
        
    Returns:
        Dictionary with ingestion results
    """
    logger.info(f"Starting ingestion pass #1 from source: {source}")
    
    # Pull data
    data = pull_data(source)
    if not data:
        logger.warning(f"No data pulled from {source}")
        return {'success': False, 'items_processed': 0, 'items_ingested': 0}
    
    # Process in chunks
    total_ingested = 0
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        logger.info(f"Processing chunk {i//chunk_size + 1} ({len(chunk)} items)")
        ingested = ingest_to_db(chunk)
        total_ingested += ingested
    
    # Export for Claude skills (future-proof)
    try:
        result = supabase.table('bookmarks').select('*').limit(1000).execute()
        export_data = [dict(row) for row in result.data]
        
        with open('claude_export.json', 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)
        logger.info(f"Exported {len(export_data)} items to claude_export.json")
    except Exception as e:
        logger.error(f"Error creating Claude export: {e}")
    
    results = {
        'success': True,
        'items_processed': len(data),
        'items_ingested': total_ingested,
        'source': source
    }
    
    logger.info(f"Ingestion pass #1 complete: {results}")
    return results


# MCP/Agent Prep (self-scaffolding foundation—expand later)
# Note: StateGraph is handled by agents/orchestrator.py
# This is just a placeholder for future expansion
if HAS_LANGGRAPH:
    logger.info("LangGraph available for future agent workflows")


# Claude Skill Prompt Template (copy to Claude after export)
CLAUDE_SKILL_PROMPT = """
System: Unify gematria/esoteric with math—log leaps, measure costs.

MCP: Triangulate data, segment phases, update master DB.

Task: From uploaded json, query 'best vector libs'—return summaries/tags/relevance; flag for phase2 if score <0.5.
"""


if __name__ == "__main__":
    import sys
    
    # Allow source to be passed as command line argument
    source = sys.argv[1] if len(sys.argv) > 1 else 'dewey_json.json'
    chunk_size = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    
    logger.info("=" * 60)
    logger.info("Gematria Hive - Ingestion Pass #1")
    logger.info("=" * 60)
    
    results = run_ingestion_pass1(source=source, chunk_size=chunk_size)
    
    print("\n" + "=" * 60)
    print("Ingestion Results:")
    print("=" * 60)
    print(f"Source: {results['source']}")
    print(f"Items Processed: {results['items_processed']}")
    print(f"Items Ingested: {results['items_ingested']}")
    print(f"Success: {results['success']}")
    print("=" * 60)
    
    if results['success']:
        print("\n✅ Ingestion complete! Check ingestion_log.txt for details.")
        print("📊 Data exported to claude_export.json for Claude skills.")
    else:
        print("\n❌ Ingestion failed. Check ingestion_log.txt for errors.")

