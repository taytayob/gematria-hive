-- Gematria Database Tables Migration
-- Purpose: Create tables for gematria words and scraped content
-- Date: 2025-01-06

-- Enable pgvector extension if not already enabled
CREATE EXTENSION IF NOT EXISTS vector;

-- 1. Gematria Words Table
-- Stores gematria calculations for phrases/words
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
  source TEXT,  -- 'gematrix789', 'gimatria789', 'scraped', etc.
  embedding vector(384),  -- For semantic search
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for fast lookups
CREATE INDEX IF NOT EXISTS idx_jewish_gematria ON gematria_words(jewish_gematria);
CREATE INDEX IF NOT EXISTS idx_english_gematria ON gematria_words(english_gematria);
CREATE INDEX IF NOT EXISTS idx_simple_gematria ON gematria_words(simple_gematria);
CREATE INDEX IF NOT EXISTS idx_phrase ON gematria_words(phrase);
CREATE INDEX IF NOT EXISTS idx_source ON gematria_words(source);
CREATE INDEX IF NOT EXISTS idx_search_num ON gematria_words(search_num);

-- Vector similarity search index (IVFFlat for pgvector)
CREATE INDEX IF NOT EXISTS idx_gematria_embedding ON gematria_words 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- 2. Scraped Content Table
-- Stores web scraped content from gematrix.org and related sites
CREATE TABLE IF NOT EXISTS scraped_content (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  url TEXT NOT NULL UNIQUE,
  title TEXT,
  content TEXT,
  content_type TEXT,  -- 'html', 'text', 'image', etc.
  images TEXT[],  -- Array of image URLs
  links TEXT[],  -- Array of discovered links
  source_site TEXT,  -- 'gematrix.org', 'shematria.com', etc.
  embedding vector(384),
  tags TEXT[],
  scraped_at TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for scraped_content
CREATE INDEX IF NOT EXISTS idx_scraped_url ON scraped_content(url);
CREATE INDEX IF NOT EXISTS idx_scraped_source ON scraped_content(source_site);
CREATE INDEX IF NOT EXISTS idx_scraped_at ON scraped_content(scraped_at);
CREATE INDEX IF NOT EXISTS idx_scraped_content_type ON scraped_content(content_type);

-- Vector similarity search index for scraped content
CREATE INDEX IF NOT EXISTS idx_scraped_embedding ON scraped_content 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- 3. Create views for common queries

-- View for words with same gematria value (relationships)
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

-- View for recent scraped content
CREATE OR REPLACE VIEW recent_scraped_content AS
SELECT *
FROM scraped_content
WHERE scraped_at > NOW() - INTERVAL '7 days'
ORDER BY scraped_at DESC;

-- 4. Enable Row Level Security (optional, can be disabled for development)
-- ALTER TABLE gematria_words ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE scraped_content ENABLE ROW LEVEL SECURITY;

-- 5. Create policies for public access (adjust as needed)
-- CREATE POLICY "Allow public read access" ON gematria_words
--   FOR SELECT USING (true);
-- 
-- CREATE POLICY "Allow public insert" ON gematria_words
--   FOR INSERT WITH CHECK (true);
-- 
-- CREATE POLICY "Allow public read access" ON scraped_content
--   FOR SELECT USING (true);
-- 
-- CREATE POLICY "Allow public insert" ON scraped_content
--   FOR INSERT WITH CHECK (true);

