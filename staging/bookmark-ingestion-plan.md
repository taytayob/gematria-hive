# Bookmark Ingestion & Analysis System - Implementation Plan

## Overview

Comprehensive system for ingesting bookmarks (JSON/markdown), fetching Twitter/X threads via Grok, indexing authors, extracting symbols/esoteric content, running gematria calculations, performing phonetic analysis, detecting patterns, and building deep research capabilities.

## Goals from PRD

- **Data Unification**: Unify bookmark data from multiple sources (JSON, markdown, Twitter/X, etc.)
- **Author Indexing**: Track authors across platforms, index their accounts and subjects
- **Source Repository**: Track what we extracted, why it fits our goals, and how it matches PRD objectives
- **Pattern Detection**: Log key terms, find patterns, understand cross-domain inferences
- **Symbol Extraction**: Extract symbols, arcane/esoteric content, narratives, events
- **Deep Research**: Build browser agent for topic exploration, gather proofs, track importance
- **Gematria Integration**: Run terms through gematria calculator, index results
- **Phonetic Analysis**: Explore phonetic connections (I, eyes, ice, numerology, geometry, sacred)
- **Resource Discovery**: Find high-fidelity datasets, repos, resources
- **Multi-modal Support**: Handle libraries, videos, images, text
- **Caching & Logging**: Maintain cache, logs, prompts, and all metadata

---

## Database Schema

### 1. Authors Table
```sql
CREATE TABLE authors (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  username TEXT NOT NULL,
  platform TEXT NOT NULL,  -- 'twitter', 'x', 'github', 'youtube', etc.
  display_name TEXT,
  bio TEXT,
  profile_url TEXT,
  avatar_url TEXT,
  verified BOOLEAN DEFAULT FALSE,
  follower_count INTEGER,
  following_count INTEGER,
  subject_tags TEXT[],  -- Topics they discuss
  account_indexed_at TIMESTAMPTZ DEFAULT NOW(),
  last_seen_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(username, platform)
);

CREATE INDEX idx_authors_username ON authors(username);
CREATE INDEX idx_authors_platform ON authors(platform);
CREATE INDEX idx_authors_subject_tags ON authors USING GIN(subject_tags);
```

### 2. Sources Table
```sql
CREATE TABLE sources (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  url TEXT NOT NULL UNIQUE,
  source_type TEXT NOT NULL,  -- 'bookmark', 'tweet', 'thread', 'article', 'video', 'image', 'library'
  title TEXT,
  content TEXT,
  author_id UUID REFERENCES authors(id),
  extracted_data JSONB,  -- What we extracted
  extraction_reason TEXT,  -- Why it fits our goals
  prd_alignment JSONB,  -- How it matches PRD objectives
  relevance_score FLOAT,
  tags TEXT[],
  metadata JSONB,
  ingested_at TIMESTAMPTZ DEFAULT NOW(),
  processed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_sources_url ON sources(url);
CREATE INDEX idx_sources_type ON sources(source_type);
CREATE INDEX idx_sources_author ON sources(author_id);
CREATE INDEX idx_sources_tags ON sources USING GIN(tags);
CREATE INDEX idx_sources_relevance ON sources(relevance_score);
```

### 3. Key Terms Table
```sql
CREATE TABLE key_terms (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  term TEXT NOT NULL,
  term_type TEXT,  -- 'symbol', 'esoteric', 'narrative', 'event', 'phonetic', 'gematria'
  phonetic_variants TEXT[],  -- I, eyes, ice, etc.
  gematria_values JSONB,  -- {jewish: 123, english: 456, ...}
  context TEXT,
  source_ids UUID[],
  pattern_matches JSONB,  -- Cross-domain connections
  frequency INTEGER DEFAULT 1,
  first_seen_at TIMESTAMPTZ DEFAULT NOW(),
  last_seen_at TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_key_terms_term ON key_terms(term);
CREATE INDEX idx_key_terms_type ON key_terms(term_type);
CREATE INDEX idx_key_terms_phonetic ON key_terms USING GIN(phonetic_variants);
CREATE INDEX idx_key_terms_frequency ON key_terms(frequency);
```

### 4. Patterns Table
```sql
CREATE TABLE patterns (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  pattern_name TEXT NOT NULL,
  pattern_type TEXT,  -- 'cross_domain', 'phonetic', 'gematria', 'temporal', 'symbolic'
  description TEXT,
  key_terms UUID[],  -- References to key_terms
  sources UUID[],  -- References to sources
  confidence_score FLOAT,
  inference_logic JSONB,  -- How the pattern was inferred
  cross_domain_connections JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_patterns_type ON patterns(pattern_type);
CREATE INDEX idx_patterns_confidence ON patterns(confidence_score);
```

### 5. Research Topics Table
```sql
CREATE TABLE research_topics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  topic_name TEXT NOT NULL,
  topic_description TEXT,
  importance_score FLOAT,
  proofs JSONB,  -- Evidence and proofs of importance
  beliefs JSONB,  -- What we believe about this topic
  needs JSONB,  -- What we still need or want
  monitoring JSONB,  -- What to monitor
  potential_leads JSONB,  -- Where it could lead
  sources UUID[],
  key_terms UUID[],
  patterns UUID[],
  research_status TEXT,  -- 'active', 'completed', 'monitoring', 'archived'
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_research_topics_name ON research_topics(topic_name);
CREATE INDEX idx_research_topics_importance ON research_topics(importance_score);
CREATE INDEX idx_research_topics_status ON research_topics(research_status);
```

### 6. Proofs Table
```sql
CREATE TABLE proofs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  proof_name TEXT NOT NULL,
  proof_type TEXT,  -- 'gematria', 'phonetic', 'symbolic', 'temporal', 'cross_domain'
  theorem TEXT,
  evidence JSONB,
  accuracy_metric FLOAT,
  efficiency_score FLOAT,
  sources UUID[],
  research_topic_id UUID REFERENCES research_topics(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_proofs_type ON proofs(proof_type);
CREATE INDEX idx_proofs_topic ON proofs(research_topic_id);
CREATE INDEX idx_proofs_accuracy ON proofs(accuracy_metric);
```

### 7. Resource Discovery Table
```sql
CREATE TABLE discovered_resources (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  resource_type TEXT,  -- 'dataset', 'repository', 'library', 'paper', 'video', 'image'
  name TEXT NOT NULL,
  url TEXT,
  description TEXT,
  fidelity_score FLOAT,  -- Quality/reliability score
  relevance_to_goals JSONB,
  tags TEXT[],
  discovered_at TIMESTAMPTZ DEFAULT NOW(),
  ingested BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_resources_type ON discovered_resources(resource_type);
CREATE INDEX idx_resources_fidelity ON discovered_resources(fidelity_score);
CREATE INDEX idx_resources_tags ON discovered_resources USING GIN(tags);
```

### 8. Cache & Logs Table
```sql
CREATE TABLE cache_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  cache_key TEXT NOT NULL UNIQUE,
  cache_type TEXT,  -- 'prompt', 'embedding', 'gematria', 'phonetic', 'api_response'
  cached_data JSONB,
  expires_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_cache_key ON cache_logs(cache_key);
CREATE INDEX idx_cache_type ON cache_logs(cache_type);
CREATE INDEX idx_cache_expires ON cache_logs(expires_at);
```

---

## Implementation Components

### 1. Bookmark Ingestion Module (`agents/bookmark_ingestion.py`)

**Purpose**: Process JSON and markdown bookmark files

**Features**:
- Parse JSON bookmark files (Dewey, OneTab, browser exports)
- Parse markdown files with links
- Extract URLs, titles, descriptions, tags
- Normalize data format
- Route to appropriate processors (Twitter, articles, videos, etc.)

**Input Formats**:
- JSON: `[{url, title, summary, tags, ...}]`
- Markdown: Links in `[text](url)` format
- OneTab exports
- Browser bookmark exports

**Output**: Standardized bookmark objects ready for processing

---

### 2. Twitter/X Thread Fetcher (`agents/twitter_fetcher.py`)

**Purpose**: Fetch full Twitter/X threads using Grok API

**Features**:
- Detect Twitter/X URLs in bookmarks
- Use Grok API to fetch full thread context
- Extract author information
- Parse thread structure (replies, quotes, media)
- Extract all text, images, links from thread
- Handle rate limiting and caching

**Grok API Integration**:
- Endpoint: `https://api.x.ai/v1/chat/completions`
- Model: `grok-beta` or `grok-2`
- Prompt: "Fetch the full thread for this tweet URL: {url}. Include all replies, context, and metadata."

**Output**: Complete thread data with author info

---

### 3. Author Indexing System (`agents/author_indexer.py`)

**Purpose**: Index and track authors across platforms

**Features**:
- Extract author info from sources (Twitter, GitHub, YouTube, etc.)
- Create/update author records
- Track subjects/topics per author
- Index account metadata (followers, bio, etc.)
- Link sources to authors
- Update last_seen_at timestamps

**Platform Support**:
- Twitter/X
- GitHub
- YouTube
- Medium/Substack
- Reddit
- Other platforms via URL parsing

**Output**: Author records with linked sources

---

### 4. Symbol & Esoteric Extractor (`agents/symbol_extractor.py`)

**Purpose**: Extract symbols, arcane/esoteric content, narratives, events

**Features**:
- Pattern matching for symbols (geometric, alchemical, astrological, etc.)
- Esoteric terminology detection
- Narrative structure analysis
- Event extraction (dates, locations, significance)
- Symbol relationships and connections

**Symbol Categories**:
- Geometric (sacred geometry, mandalas, etc.)
- Alchemical
- Astrological
- Numerological
- Kabbalistic
- Hermetic
- Other esoteric traditions

**Output**: Extracted symbols with context and relationships

---

### 5. Gematria Integration (`agents/gematria_integrator.py`)

**Purpose**: Run key terms through gematria calculator

**Features**:
- Extract key terms from content
- Calculate gematria values (Jewish, English, Simple, Hebrew variants)
- Store gematria results in key_terms table
- Find related terms by gematria value
- Detect gematria patterns and connections

**Integration**:
- Use existing `gematria_calculator.py`
- Batch process terms
- Cache results
- Link to sources and patterns

**Output**: Gematria-calculated terms with relationships

---

### 6. Phonetic Analyzer (`agents/phonetic_analyzer.py`)

**Purpose**: Explore phonetic connections (I, eyes, ice, numerology, geometry, sacred)

**Features**:
- Phonetic similarity detection
- Sound-based pattern matching
- Homophone identification
- Phonetic variant tracking
- Cross-domain phonetic connections

**Phonetic Patterns**:
- I/eyes/ice connections
- Numerology/numerical sounds
- Geometry/geometric sounds
- Sacred/sacred sounds
- Other phonetic relationships

**Output**: Phonetic variants and connections

---

### 7. Pattern Detector (`agents/pattern_detector.py`)

**Purpose**: Detect patterns and cross-domain inferences

**Features**:
- Key term frequency analysis
- Cross-domain pattern detection
- Temporal pattern analysis
- Symbolic pattern recognition
- Inference logic generation
- Pattern confidence scoring

**Pattern Types**:
- Cross-domain (gematria + phonetic + symbolic)
- Temporal (events, dates, sequences)
- Symbolic (symbol relationships)
- Phonetic (sound-based connections)
- Gematria (numerical relationships)

**Output**: Detected patterns with confidence scores

---

### 8. Deep Research Browser Agent (`agents/deep_research_browser.py`)

**Purpose**: Deep research on topics, gather proofs, track importance

**Features**:
- Topic-based research initiation
- Multi-source research gathering
- Proof collection and validation
- Importance scoring
- Research status tracking
- Lead generation and monitoring

**Research Workflow**:
1. Identify research topic
2. Gather initial sources
3. Extract key terms and patterns
4. Build proofs
5. Assess importance
6. Identify needs and monitoring points
7. Generate potential leads

**Output**: Research topics with proofs and insights

---

### 9. Source Repository Tracker (`agents/source_tracker.py`)

**Purpose**: Track sources, extraction metadata, PRD alignment

**Features**:
- Store source records
- Track extraction data
- Log extraction reasons
- PRD alignment scoring
- Relevance scoring
- Source categorization

**Output**: Source records with full metadata

---

### 10. Resource Discovery Agent (`agents/resource_discoverer.py`)

**Purpose**: Find high-fidelity datasets, repos, resources

**Features**:
- Search for relevant resources
- Fidelity scoring
- Relevance assessment
- Resource categorization
- Integration with discovery APIs (GitHub, arXiv, etc.)

**Resource Types**:
- Datasets
- Code repositories
- Research papers
- Libraries
- Videos
- Images
- Other resources

**Output**: Discovered resources with fidelity scores

---

## Workflow Architecture

### Main Ingestion Workflow

```
1. Bookmark Ingestion
   ↓
2. URL Classification (Twitter, Article, Video, etc.)
   ↓
3. Parallel Processing:
   ├─ Twitter Fetcher (if Twitter URL)
   ├─ Author Indexer
   ├─ Content Extractor
   └─ Symbol Extractor
   ↓
4. Gematria Integration
   ↓
5. Phonetic Analysis
   ↓
6. Pattern Detection
   ↓
7. Source Repository Tracking
   ↓
8. Deep Research (if high importance)
   ↓
9. Resource Discovery (if needed)
   ↓
10. Cache & Logging
```

### Research Workflow

```
1. Research Topic Creation
   ↓
2. Source Gathering
   ↓
3. Key Term Extraction
   ↓
4. Pattern Detection
   ↓
5. Proof Building
   ↓
6. Importance Assessment
   ↓
7. Needs Identification
   ↓
8. Monitoring Setup
   ↓
9. Lead Generation
```

---

## File Structure

```
agents/
  ├── bookmark_ingestion.py      # Main bookmark processor
  ├── twitter_fetcher.py         # Grok API integration
  ├── author_indexer.py          # Author tracking
  ├── symbol_extractor.py        # Symbol/esoteric extraction
  ├── gematria_integrator.py     # Gematria calculations
  ├── phonetic_analyzer.py       # Phonetic analysis
  ├── pattern_detector.py        # Pattern detection
  ├── deep_research_browser.py  # Research agent
  ├── source_tracker.py          # Source repository
  └── resource_discoverer.py     # Resource discovery

migrations/
  ├── create_bookmark_tables.sql # New schema

utils/
  ├── cache_manager.py           # Caching utilities
  ├── logger.py                  # Enhanced logging
  └── prompt_templates.py        # Prompt templates

config/
  ├── grok_config.json           # Grok API config
  └── extraction_patterns.json  # Symbol/esoteric patterns
```

---

## Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Database schema migration
- [ ] Bookmark ingestion module
- [ ] Basic author indexing
- [ ] Source repository tracking

### Phase 2: Twitter Integration (Week 2)
- [ ] Grok API integration
- [ ] Twitter thread fetcher
- [ ] Enhanced author indexing
- [ ] Thread content extraction

### Phase 3: Analysis (Week 3)
- [ ] Symbol extractor
- [ ] Gematria integrator
- [ ] Phonetic analyzer
- [ ] Key term extraction

### Phase 4: Intelligence (Week 4)
- [ ] Pattern detector
- [ ] Cross-domain inference
- [ ] Research browser agent
- [ ] Proof building

### Phase 5: Discovery & Optimization (Week 5)
- [ ] Resource discovery agent
- [ ] Caching system
- [ ] Enhanced logging
- [ ] Performance optimization

---

## API Integrations

### Grok API (Twitter/X)
- **Endpoint**: `https://api.x.ai/v1/chat/completions`
- **Authentication**: API key from environment
- **Rate Limits**: Handle appropriately
- **Caching**: Cache thread responses

### Other APIs (Future)
- GitHub API (repositories)
- arXiv API (papers)
- YouTube API (videos)
- Other discovery APIs

---

## Caching Strategy

### Cache Types
1. **Prompt Cache**: Store LLM prompts and responses
2. **Embedding Cache**: Store computed embeddings
3. **Gematria Cache**: Store gematria calculations
4. **API Response Cache**: Store API responses (Twitter, etc.)
5. **Pattern Cache**: Store detected patterns

### Cache Implementation
- Use `cache_logs` table
- TTL-based expiration
- Key-based lookups
- Batch invalidation

---

## Logging Strategy

### Log Levels
- **INFO**: Normal operations
- **DEBUG**: Detailed debugging
- **WARNING**: Issues that don't stop processing
- **ERROR**: Errors that stop processing

### Log Categories
- Bookmark ingestion
- Twitter fetching
- Author indexing
- Symbol extraction
- Gematria calculations
- Pattern detection
- Research activities
- API calls
- Cache operations

### Log Storage
- File logs: `logs/bookmark_ingestion.log`
- Database logs: `cache_logs` table
- Structured logging: JSON format

---

## Testing Strategy

### Unit Tests
- Each agent module
- Utility functions
- Database operations

### Integration Tests
- End-to-end workflows
- API integrations
- Database migrations

### Performance Tests
- Large bookmark files
- Batch processing
- Cache efficiency

---

## Success Metrics

1. **Ingestion**: Process 1000+ bookmarks successfully
2. **Twitter**: Fetch 100+ full threads via Grok
3. **Authors**: Index 500+ unique authors
4. **Terms**: Extract 10,000+ key terms
5. **Patterns**: Detect 100+ cross-domain patterns
6. **Research**: Create 50+ research topics with proofs
7. **Resources**: Discover 200+ high-fidelity resources
8. **Performance**: Process bookmarks in <5 seconds each
9. **Cache Hit Rate**: >80% for repeated operations
10. **Accuracy**: >90% correct symbol/esoteric extraction

---

## Next Steps

1. Review and approve this plan
2. Create database migration SQL
3. Implement Phase 1 components
4. Test with sample bookmark files
5. Iterate and refine

---

## Notes

- All components should be modular and testable
- Use existing infrastructure (Supabase, agents framework)
- Maintain backward compatibility
- Document all APIs and workflows
- Follow existing code style and patterns

