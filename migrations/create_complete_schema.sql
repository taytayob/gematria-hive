-- Complete Gematria Hive Database Schema Migration
-- Purpose: Create all tables for bookmark ingestion, analysis, and research system
-- Date: 2025-01-06

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- EXISTING TABLES (from create_gematria_tables.sql)
-- ============================================================================

-- 1. Gematria Words Table (existing, but ensure it exists)
CREATE TABLE IF NOT EXISTS gematria_words (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  phrase TEXT NOT NULL,
  jewish_gematria INTEGER,
  english_gematria INTEGER,
  simple_gematria INTEGER,
  hebrew_full INTEGER,
  hebrew_musafi INTEGER,
  hebrew_katan INTEGER,
  hebrew_ordinal INTEGER,
  hebrew_atbash INTEGER,
  hebrew_kidmi INTEGER,
  hebrew_perati INTEGER,
  hebrew_shemi INTEGER,
  search_num INTEGER,
  source TEXT,
  embedding vector(384),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Scraped Content Table (existing, but ensure it exists)
CREATE TABLE IF NOT EXISTS scraped_content (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  url TEXT NOT NULL UNIQUE,
  title TEXT,
  content TEXT,
  content_type TEXT,
  images TEXT[],
  links TEXT[],
  source_site TEXT,
  embedding vector(384),
  tags TEXT[],
  scraped_at TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- NEW TABLES FROM BOOKMARK INGESTION PLAN
-- ============================================================================

-- 3. Authors Table
CREATE TABLE IF NOT EXISTS authors (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  username TEXT NOT NULL,
  platform TEXT NOT NULL,
  display_name TEXT,
  bio TEXT,
  profile_url TEXT,
  avatar_url TEXT,
  verified BOOLEAN DEFAULT FALSE,
  follower_count INTEGER,
  following_count INTEGER,
  subject_tags TEXT[],
  account_indexed_at TIMESTAMPTZ DEFAULT NOW(),
  last_seen_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(username, platform)
);

CREATE INDEX IF NOT EXISTS idx_authors_username ON authors(username);
CREATE INDEX IF NOT EXISTS idx_authors_platform ON authors(platform);
CREATE INDEX IF NOT EXISTS idx_authors_subject_tags ON authors USING GIN(subject_tags);
CREATE INDEX IF NOT EXISTS idx_authors_last_seen ON authors(last_seen_at);

-- 4. Sources Table
CREATE TABLE IF NOT EXISTS sources (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  url TEXT NOT NULL UNIQUE,
  source_type TEXT NOT NULL,
  title TEXT,
  content TEXT,
  author_id UUID REFERENCES authors(id),
  extracted_data JSONB,
  extraction_reason TEXT,
  prd_alignment JSONB,
  relevance_score FLOAT,
  tags TEXT[],
  metadata JSONB,
  ingested_at TIMESTAMPTZ DEFAULT NOW(),
  processed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sources_url ON sources(url);
CREATE INDEX IF NOT EXISTS idx_sources_type ON sources(source_type);
CREATE INDEX IF NOT EXISTS idx_sources_author ON sources(author_id);
CREATE INDEX IF NOT EXISTS idx_sources_tags ON sources USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_sources_relevance ON sources(relevance_score);
CREATE INDEX IF NOT EXISTS idx_sources_ingested ON sources(ingested_at);

-- 5. Key Terms Table
CREATE TABLE IF NOT EXISTS key_terms (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  term TEXT NOT NULL,
  term_type TEXT,
  phonetic_variants TEXT[],
  gematria_values JSONB,
  context TEXT,
  source_ids UUID[],
  pattern_matches JSONB,
  frequency INTEGER DEFAULT 1,
  first_seen_at TIMESTAMPTZ DEFAULT NOW(),
  last_seen_at TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_key_terms_term ON key_terms(term);
CREATE INDEX IF NOT EXISTS idx_key_terms_type ON key_terms(term_type);
CREATE INDEX IF NOT EXISTS idx_key_terms_phonetic ON key_terms USING GIN(phonetic_variants);
CREATE INDEX IF NOT EXISTS idx_key_terms_frequency ON key_terms(frequency);
CREATE INDEX IF NOT EXISTS idx_key_terms_last_seen ON key_terms(last_seen_at);

-- 6. Patterns Table
CREATE TABLE IF NOT EXISTS patterns (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  pattern_name TEXT NOT NULL,
  pattern_type TEXT,
  description TEXT,
  key_terms UUID[],
  sources UUID[],
  confidence_score FLOAT,
  inference_logic JSONB,
  cross_domain_connections JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_patterns_type ON patterns(pattern_type);
CREATE INDEX IF NOT EXISTS idx_patterns_confidence ON patterns(confidence_score);
CREATE INDEX IF NOT EXISTS idx_patterns_name ON patterns(pattern_name);

-- 6.5. Dark Matter Patterns Table (hidden patterns, latent connections)
CREATE TABLE IF NOT EXISTS dark_matter_patterns (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  pattern_name TEXT NOT NULL,
  pattern_type TEXT,  -- 'latent', 'implicit', 'hidden', 'quantum', 'temporal_dark_matter', 'semantic_shadow'
  description TEXT,
  elements TEXT[],
  confidence FLOAT,
  perspectives JSONB,  -- Multi-perspective analysis
  quantum_state JSONB,  -- Quantum-like superposition state
  inference_logic JSONB,
  cross_domain_connections JSONB,
  first_principles TEXT[],  -- First principles analysis
  persona_insights JSONB,  -- Insights from different personas
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_dark_matter_type ON dark_matter_patterns(pattern_type);
CREATE INDEX IF NOT EXISTS idx_dark_matter_confidence ON dark_matter_patterns(confidence);
CREATE INDEX IF NOT EXISTS idx_dark_matter_name ON dark_matter_patterns(pattern_name);

-- 7. Research Topics Table
CREATE TABLE IF NOT EXISTS research_topics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  topic_name TEXT NOT NULL,
  topic_description TEXT,
  importance_score FLOAT,
  proofs JSONB,
  beliefs JSONB,
  needs JSONB,
  monitoring JSONB,
  potential_leads JSONB,
  sources UUID[],
  key_terms UUID[],
  patterns UUID[],
  research_status TEXT DEFAULT 'active',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_research_topics_name ON research_topics(topic_name);
CREATE INDEX IF NOT EXISTS idx_research_topics_importance ON research_topics(importance_score);
CREATE INDEX IF NOT EXISTS idx_research_topics_status ON research_topics(research_status);

-- 8. Proofs Table
CREATE TABLE IF NOT EXISTS proofs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  proof_name TEXT NOT NULL,
  proof_type TEXT,
  theorem TEXT,
  evidence JSONB,
  accuracy_metric FLOAT,
  efficiency_score FLOAT,
  sources UUID[],
  research_topic_id UUID REFERENCES research_topics(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_proofs_type ON proofs(proof_type);
CREATE INDEX IF NOT EXISTS idx_proofs_topic ON proofs(research_topic_id);
CREATE INDEX IF NOT EXISTS idx_proofs_accuracy ON proofs(accuracy_metric);
CREATE INDEX IF NOT EXISTS idx_proofs_name ON proofs(proof_name);

-- 9. Resource Discovery Table
CREATE TABLE IF NOT EXISTS discovered_resources (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  resource_type TEXT,
  name TEXT NOT NULL,
  url TEXT,
  description TEXT,
  fidelity_score FLOAT,
  relevance_to_goals JSONB,
  tags TEXT[],
  discovered_at TIMESTAMPTZ DEFAULT NOW(),
  ingested BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_resources_type ON discovered_resources(resource_type);
CREATE INDEX IF NOT EXISTS idx_resources_fidelity ON discovered_resources(fidelity_score);
CREATE INDEX IF NOT EXISTS idx_resources_tags ON discovered_resources USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_resources_name ON discovered_resources(name);

-- 10. Cache & Logs Table
CREATE TABLE IF NOT EXISTS cache_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  cache_key TEXT NOT NULL UNIQUE,
  cache_type TEXT,
  cached_data JSONB,
  expires_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cache_key ON cache_logs(cache_key);
CREATE INDEX IF NOT EXISTS idx_cache_type ON cache_logs(cache_type);
CREATE INDEX IF NOT EXISTS idx_cache_expires ON cache_logs(expires_at);

-- ============================================================================
-- NEW TABLES FROM PLAN ADDITIONS
-- ============================================================================

-- 11. Personas Table
CREATE TABLE IF NOT EXISTS personas (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  domain TEXT,
  contributions JSONB,
  models JSONB,
  frameworks JSONB,
  knowledge JSONB,
  subject_tags TEXT[],
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_personas_name ON personas(name);
CREATE INDEX IF NOT EXISTS idx_personas_domain ON personas(domain);
CREATE INDEX IF NOT EXISTS idx_personas_tags ON personas USING GIN(subject_tags);

-- 12. Alphabets Table
CREATE TABLE IF NOT EXISTS alphabets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  language TEXT NOT NULL,
  character TEXT NOT NULL,
  numeric_value INTEGER,
  deeper_meaning TEXT,
  celestial_events TEXT[],
  historical_context JSONB,
  phonetic_variants TEXT[],
  gematria_methods JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(language, character)
);

CREATE INDEX IF NOT EXISTS idx_alphabets_language ON alphabets(language);
CREATE INDEX IF NOT EXISTS idx_alphabets_character ON alphabets(character);
CREATE INDEX IF NOT EXISTS idx_alphabets_value ON alphabets(numeric_value);
CREATE INDEX IF NOT EXISTS idx_alphabets_events ON alphabets USING GIN(celestial_events);

-- 13. Baselines Table
CREATE TABLE IF NOT EXISTS baselines (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  baseline_type TEXT NOT NULL,
  value JSONB,
  source TEXT,
  validated BOOLEAN DEFAULT FALSE,
  validation_notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_baselines_type ON baselines(baseline_type);
CREATE INDEX IF NOT EXISTS idx_baselines_validated ON baselines(validated);

-- 14. Validations Table
CREATE TABLE IF NOT EXISTS validations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  validation_type TEXT NOT NULL,
  entity_id UUID NOT NULL,
  entity_type TEXT NOT NULL,
  score FLOAT,
  passed BOOLEAN DEFAULT FALSE,
  notes TEXT,
  baseline_id UUID REFERENCES baselines(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_validations_type ON validations(validation_type);
CREATE INDEX IF NOT EXISTS idx_validations_entity ON validations(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_validations_passed ON validations(passed);
CREATE INDEX IF NOT EXISTS idx_validations_score ON validations(score);

-- 15. Floating Index Table
CREATE TABLE IF NOT EXISTS floating_index (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  key TEXT NOT NULL UNIQUE,
  entity_type TEXT NOT NULL,
  entity_id UUID NOT NULL,
  metadata JSONB,
  last_accessed TIMESTAMPTZ DEFAULT NOW(),
  access_count INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_floating_index_key ON floating_index(key);
CREATE INDEX IF NOT EXISTS idx_floating_index_entity ON floating_index(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_floating_index_last_accessed ON floating_index(last_accessed);

-- 16. Projects/Sandbox Table
CREATE TABLE IF NOT EXISTS projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_name TEXT NOT NULL,
  project_description TEXT,
  project_type TEXT DEFAULT 'sandbox',
  status TEXT DEFAULT 'active',
  data_snapshot JSONB,
  master_sync_enabled BOOLEAN DEFAULT TRUE,
  completion_notes TEXT,
  documentation JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_projects_name ON projects(project_name);
CREATE INDEX IF NOT EXISTS idx_projects_type ON projects(project_type);
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);

-- 17. Cost Tracking Table
CREATE TABLE IF NOT EXISTS cost_tracking (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  cost_type TEXT NOT NULL,
  api_name TEXT,
  operation TEXT,
  cost_amount FLOAT NOT NULL,
  currency TEXT DEFAULT 'USD',
  metadata JSONB,
  tracked_at TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cost_type ON cost_tracking(cost_type);
CREATE INDEX IF NOT EXISTS idx_cost_api ON cost_tracking(api_name);
CREATE INDEX IF NOT EXISTS idx_cost_tracked_at ON cost_tracking(tracked_at);

-- 18. Agent Memory Table
CREATE TABLE IF NOT EXISTS agent_memory (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id TEXT NOT NULL,
  context TEXT,
  state JSONB,
  expires_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_agent_memory_agent ON agent_memory(agent_id);
CREATE INDEX IF NOT EXISTS idx_agent_memory_expires ON agent_memory(expires_at);

-- 19. Hunches Table (if not exists)
CREATE TABLE IF NOT EXISTS hunches (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content TEXT NOT NULL,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  status TEXT DEFAULT 'pending',
  cost FLOAT DEFAULT 0.0,
  links TEXT[],
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_hunches_status ON hunches(status);
CREATE INDEX IF NOT EXISTS idx_hunches_timestamp ON hunches(timestamp);

-- 20. Bookmarks Table (if not exists)
CREATE TABLE IF NOT EXISTS bookmarks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  url TEXT NOT NULL UNIQUE,
  summary TEXT,
  embedding vector(384),
  tags TEXT[],
  phase TEXT,
  relevance_score FLOAT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_bookmarks_url ON bookmarks(url);
CREATE INDEX IF NOT EXISTS idx_bookmarks_tags ON bookmarks USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_bookmarks_relevance ON bookmarks(relevance_score);

-- 21. Synchronicities Table (for affinity agent)
CREATE TABLE IF NOT EXISTS synchronicities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sync_id TEXT NOT NULL UNIQUE,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  pattern_type TEXT NOT NULL,
  strength FLOAT NOT NULL,
  significance FLOAT NOT NULL,
  description TEXT,
  gematria_values INTEGER[],
  symbols TEXT[],
  elements JSONB,
  quantum_state JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_synchronicities_sync_id ON synchronicities(sync_id);
CREATE INDEX IF NOT EXISTS idx_synchronicities_pattern_type ON synchronicities(pattern_type);
CREATE INDEX IF NOT EXISTS idx_synchronicities_strength ON synchronicities(strength);
CREATE INDEX IF NOT EXISTS idx_synchronicities_significance ON synchronicities(significance);
CREATE INDEX IF NOT EXISTS idx_synchronicities_timestamp ON synchronicities(timestamp);
CREATE INDEX IF NOT EXISTS idx_synchronicities_gematria_values ON synchronicities USING GIN(gematria_values);
CREATE INDEX IF NOT EXISTS idx_synchronicities_symbols ON synchronicities USING GIN(symbols);

-- 22. Observations Table (for observer agent)
CREATE TABLE IF NOT EXISTS observations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  observation_id TEXT NOT NULL UNIQUE,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  event_type TEXT NOT NULL,
  agent_name TEXT,
  data JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_observations_observation_id ON observations(observation_id);
CREATE INDEX IF NOT EXISTS idx_observations_event_type ON observations(event_type);
CREATE INDEX IF NOT EXISTS idx_observations_agent_name ON observations(agent_name);
CREATE INDEX IF NOT EXISTS idx_observations_timestamp ON observations(timestamp);

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- View for gematria relationships
CREATE OR REPLACE VIEW gematria_relationships AS
SELECT 
  jewish_gematria,
  COUNT(*) as word_count,
  array_agg(DISTINCT phrase) as phrases
FROM gematria_words
WHERE jewish_gematria IS NOT NULL
GROUP BY jewish_gematria
HAVING COUNT(*) > 1
ORDER BY word_count DESC;

-- View for recent sources
CREATE OR REPLACE VIEW recent_sources AS
SELECT *
FROM sources
WHERE ingested_at > NOW() - INTERVAL '7 days'
ORDER BY ingested_at DESC;

-- View for active research topics
CREATE OR REPLACE VIEW active_research_topics AS
SELECT *
FROM research_topics
WHERE research_status = 'active'
ORDER BY importance_score DESC;

-- View for high-confidence patterns
CREATE OR REPLACE VIEW high_confidence_patterns AS
SELECT *
FROM patterns
WHERE confidence_score >= 0.7
ORDER BY confidence_score DESC;

-- View for cost summary (daily)
CREATE OR REPLACE VIEW daily_cost_summary AS
SELECT 
  DATE(tracked_at) as date,
  cost_type,
  SUM(cost_amount) as total_cost,
  COUNT(*) as operation_count
FROM cost_tracking
WHERE tracked_at > NOW() - INTERVAL '30 days'
GROUP BY DATE(tracked_at), cost_type
ORDER BY date DESC, total_cost DESC;

-- ============================================================================
-- FUNCTIONS FOR COMMON OPERATIONS
-- ============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers to all tables
CREATE TRIGGER update_gematria_words_updated_at BEFORE UPDATE ON gematria_words
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_scraped_content_updated_at BEFORE UPDATE ON scraped_content
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_authors_updated_at BEFORE UPDATE ON authors
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_sources_updated_at BEFORE UPDATE ON sources
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_key_terms_updated_at BEFORE UPDATE ON key_terms
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_patterns_updated_at BEFORE UPDATE ON patterns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_research_topics_updated_at BEFORE UPDATE ON research_topics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_proofs_updated_at BEFORE UPDATE ON proofs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_discovered_resources_updated_at BEFORE UPDATE ON discovered_resources
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_cache_logs_updated_at BEFORE UPDATE ON cache_logs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_personas_updated_at BEFORE UPDATE ON personas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_alphabets_updated_at BEFORE UPDATE ON alphabets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_baselines_updated_at BEFORE UPDATE ON baselines
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_validations_updated_at BEFORE UPDATE ON validations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_floating_index_updated_at BEFORE UPDATE ON floating_index
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_cost_tracking_updated_at BEFORE UPDATE ON cost_tracking
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agent_memory_updated_at BEFORE UPDATE ON agent_memory
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_hunches_updated_at BEFORE UPDATE ON hunches
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_bookmarks_updated_at BEFORE UPDATE ON bookmarks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_synchronicities_updated_at BEFORE UPDATE ON synchronicities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_observations_updated_at BEFORE UPDATE ON observations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- COMMENTS FOR DOCUMENTATION
-- ============================================================================

COMMENT ON TABLE authors IS 'Tracks authors across platforms (Twitter, GitHub, YouTube, etc.)';
COMMENT ON TABLE sources IS 'Repository of all ingested sources with extraction metadata';
COMMENT ON TABLE key_terms IS 'Extracted terms with gematria values and phonetic variants';
COMMENT ON TABLE patterns IS 'Cross-domain patterns and inference logic';
COMMENT ON TABLE research_topics IS 'Deep research topics with proofs and importance scores';
COMMENT ON TABLE proofs IS 'Evidence and proofs for research topics';
COMMENT ON TABLE discovered_resources IS 'High-fidelity datasets, repos, papers';
COMMENT ON TABLE personas IS 'Master personas for different domains (Einstein, Tesla, Pythagoras, etc.)';
COMMENT ON TABLE alphabets IS 'Alphabets and languages with character values and deeper meanings';
COMMENT ON TABLE baselines IS 'Baseline values for validation and comparison';
COMMENT ON TABLE validations IS 'Validation results with scores and notes';
COMMENT ON TABLE floating_index IS 'Quick lookup index for fast access without full database queries';
COMMENT ON TABLE projects IS 'Projects/sandbox system for experimental work';
COMMENT ON TABLE cost_tracking IS 'API and processing cost tracking with $10 cap alerts';
COMMENT ON TABLE synchronicities IS 'Detected synchronicities, patterns, and meaningful coincidences from affinity agent';
COMMENT ON TABLE observations IS 'System observations and events tracked by observer agent';

