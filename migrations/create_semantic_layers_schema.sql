-- Semantic Layers & Multi-Dimensional Word Associations Schema
-- Purpose: Store word meanings, associations, roots, and cross-language mappings
-- Date: 2025-01-06
-- Design: Separate baseline gematria from enriched semantic data

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- 1. WORD ROOTS & ETYMOLOGY TABLE
-- ============================================================================
-- Stores root words, etymology, and linguistic history
CREATE TABLE IF NOT EXISTS word_roots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  word TEXT NOT NULL,
  root_word TEXT,  -- Original root (e.g., "orange" -> "naranj" Arabic)
  root_language TEXT,  -- Language of origin (e.g., 'arabic', 'greek', 'latin')
  etymology TEXT,  -- Full etymology description
  phonetic_variants TEXT[],  -- Phonetic variations
  historical_forms TEXT[],  -- Historical spellings/forms
  frequency_history JSONB,  -- Historical frequency data
  first_attested TIMESTAMPTZ,  -- First known use
  language_family TEXT,  -- Indo-European, Semitic, etc.
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_word_roots_word ON word_roots(word);
CREATE INDEX IF NOT EXISTS idx_word_roots_root ON word_roots(root_word);
CREATE INDEX IF NOT EXISTS idx_word_roots_language ON word_roots(root_language);

-- ============================================================================
-- 2. SEMANTIC LAYERS TABLE
-- ============================================================================
-- Stores multi-dimensional meanings (orange = color/fruit/meaning/religious)
CREATE TABLE IF NOT EXISTS semantic_layers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  word TEXT NOT NULL,
  layer_type TEXT NOT NULL,  -- 'color', 'fruit', 'meaning', 'religious', 'symbolic', 'esoteric', 'sacred_geometry', 'frequency', 'idiom', 'metaphor'
  layer_value TEXT NOT NULL,  -- The specific meaning in this layer
  description TEXT,  -- Detailed description
  context TEXT,  -- Context where this meaning applies
  cultural_significance TEXT,  -- Cultural/religious significance
  frequency_score FLOAT,  -- How common this meaning is (0.0-1.0)
  confidence_score FLOAT,  -- Confidence in this association (0.0-1.0)
  sources TEXT[],  -- Source references
  related_words TEXT[],  -- Related words in this layer
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(word, layer_type, layer_value)
);

CREATE INDEX IF NOT EXISTS idx_semantic_layers_word ON semantic_layers(word);
CREATE INDEX IF NOT EXISTS idx_semantic_layers_type ON semantic_layers(layer_type);
CREATE INDEX IF NOT EXISTS idx_semantic_layers_value ON semantic_layers(layer_value);
CREATE INDEX IF NOT EXISTS idx_semantic_layers_frequency ON semantic_layers(frequency_score);

-- ============================================================================
-- 3. WORD ASSOCIATIONS TABLE
-- ============================================================================
-- Stores symmetry and deeper associations between words
CREATE TABLE IF NOT EXISTS word_associations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  word1 TEXT NOT NULL,
  word2 TEXT NOT NULL,
  association_type TEXT NOT NULL,  -- 'gematria_match', 'semantic', 'phonetic', 'etymological', 'symbolic', 'sacred_geometry', 'frequency', 'idiom', 'metaphor'
  strength FLOAT NOT NULL,  -- Strength of association (0.0-1.0)
  gematria_values JSONB,  -- Shared gematria values
  semantic_overlap JSONB,  -- Semantic layer overlaps
  description TEXT,  -- Description of association
  evidence TEXT[],  -- Evidence for this association
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(word1, word2, association_type)
);

CREATE INDEX IF NOT EXISTS idx_word_associations_word1 ON word_associations(word1);
CREATE INDEX IF NOT EXISTS idx_word_associations_word2 ON word_associations(word2);
CREATE INDEX IF NOT EXISTS idx_word_associations_type ON word_associations(association_type);
CREATE INDEX IF NOT EXISTS idx_word_associations_strength ON word_associations(strength);

-- ============================================================================
-- 4. CROSS-LANGUAGE ALPHABET MAPPINGS
-- ============================================================================
-- Stores alphabet equivalents across languages (Greek, Roman, Hebrew, etc.)
CREATE TABLE IF NOT EXISTS alphabet_mappings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  language TEXT NOT NULL,  -- 'greek', 'roman', 'hebrew', 'arabic', 'sanskrit', etc.
  letter TEXT NOT NULL,  -- The letter/symbol
  letter_name TEXT,  -- Name of the letter (e.g., 'lambda', 'alpha')
  numeric_value INTEGER,  -- Gematria/numeric value
  position INTEGER,  -- Position in alphabet
  uppercase TEXT,  -- Uppercase form
  lowercase TEXT,  -- Lowercase form
  equivalent_letters JSONB,  -- Equivalent letters in other languages
  phonetic_value TEXT,  -- Phonetic representation
  historical_forms TEXT[],  -- Historical variations
  symbol_meaning TEXT,  -- Symbolic meaning
  physics_value FLOAT,  -- Physics value (e.g., lambda = wavelength)
  sacred_geometry_value JSONB,  -- Sacred geometry associations
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(language, letter)
);

CREATE INDEX IF NOT EXISTS idx_alphabet_mappings_language ON alphabet_mappings(language);
CREATE INDEX IF NOT EXISTS idx_alphabet_mappings_letter ON alphabet_mappings(letter);
CREATE INDEX IF NOT EXISTS idx_alphabet_mappings_value ON alphabet_mappings(numeric_value);

-- ============================================================================
-- 5. GREEK & ROMAN NUMERALS
-- ============================================================================
-- Stores Greek and Roman numeral systems
CREATE TABLE IF NOT EXISTS numeral_systems (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  system_type TEXT NOT NULL,  -- 'greek', 'roman', 'hebrew', etc.
  symbol TEXT NOT NULL,  -- The numeral symbol
  numeric_value INTEGER NOT NULL,  -- The numeric value
  symbol_name TEXT,  -- Name of the symbol
  usage_context TEXT,  -- Context where used
  historical_period TEXT,  -- Historical period
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(system_type, symbol)
);

CREATE INDEX IF NOT EXISTS idx_numeral_systems_type ON numeral_systems(system_type);
CREATE INDEX IF NOT EXISTS idx_numeral_systems_value ON numeral_systems(numeric_value);

-- ============================================================================
-- 6. SYMBOLS & SACRED GEOMETRY
-- ============================================================================
-- Stores symbols, sacred geometry, and esoteric associations
CREATE TABLE IF NOT EXISTS symbols_sacred_geometry (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  symbol TEXT NOT NULL,  -- The symbol (e.g., 'λ', 'π', 'Ω', '∞', 'φ')
  symbol_name TEXT,  -- Name of symbol (e.g., 'lambda', 'pi', 'omega', 'infinity', 'phi')
  symbol_type TEXT NOT NULL,  -- 'greek_letter', 'mathematical', 'sacred_geometry', 'esoteric', 'religious', 'physics'
  numeric_value INTEGER,  -- Gematria/numeric value
  physics_value FLOAT,  -- Physics value (e.g., lambda = wavelength, pi = 3.14159)
  sacred_geometry_value JSONB,  -- Sacred geometry associations
  esoteric_meaning TEXT,  -- Esoteric meaning
  religious_significance TEXT,  -- Religious significance
  mathematical_meaning TEXT,  -- Mathematical meaning
  frequency_in_language FLOAT,  -- Frequency in language
  associated_words TEXT[],  -- Words associated with this symbol
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(symbol, symbol_type)
);

CREATE INDEX IF NOT EXISTS idx_symbols_symbol ON symbols_sacred_geometry(symbol);
CREATE INDEX IF NOT EXISTS idx_symbols_type ON symbols_sacred_geometry(symbol_type);
CREATE INDEX IF NOT EXISTS idx_symbols_name ON symbols_sacred_geometry(symbol_name);

-- ============================================================================
-- 7. LANGUAGE FREQUENCY DATA
-- ============================================================================
-- Stores historical and current frequency data for words
CREATE TABLE IF NOT EXISTS language_frequency (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  word TEXT NOT NULL,
  language TEXT NOT NULL,  -- 'english', 'greek', 'hebrew', etc.
  time_period TEXT,  -- 'ancient', 'medieval', 'modern', 'contemporary', or specific date range
  frequency_score FLOAT NOT NULL,  -- Frequency score (0.0-1.0)
  rank INTEGER,  -- Rank in frequency
  corpus_size BIGINT,  -- Size of corpus analyzed
  context TEXT,  -- Context of frequency (e.g., 'literary', 'scientific', 'religious')
  source TEXT,  -- Source of frequency data
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(word, language, time_period, context)
);

CREATE INDEX IF NOT EXISTS idx_language_frequency_word ON language_frequency(word);
CREATE INDEX IF NOT EXISTS idx_language_frequency_language ON language_frequency(language);
CREATE INDEX IF NOT EXISTS idx_language_frequency_score ON language_frequency(frequency_score);

-- ============================================================================
-- 8. MASTER BLOB STRUCTURES (Indexed, Non-Polluting)
-- ============================================================================
-- Stores master blob structures for indexing without polluting baselines
CREATE TABLE IF NOT EXISTS master_blobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  blob_type TEXT NOT NULL,  -- 'word_complete', 'association_network', 'semantic_cluster', 'symbol_system', 'language_mapping'
  blob_name TEXT NOT NULL,  -- Name/identifier for this blob
  blob_data JSONB NOT NULL,  -- The actual blob data (structured JSON)
  metadata JSONB,  -- Metadata about the blob
  version INTEGER DEFAULT 1,  -- Version of the blob
  baseline_reference UUID,  -- Reference to baseline data (if applicable)
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(blob_type, blob_name, version)
);

CREATE INDEX IF NOT EXISTS idx_master_blobs_type ON master_blobs(blob_type);
CREATE INDEX IF NOT EXISTS idx_master_blobs_name ON master_blobs(blob_name);
CREATE INDEX IF NOT EXISTS idx_master_blobs_baseline ON master_blobs(baseline_reference);
CREATE INDEX IF NOT EXISTS idx_master_blobs_data ON master_blobs USING GIN(blob_data);

-- ============================================================================
-- 9. IDIOMS & PHRASES TABLE
-- ============================================================================
-- Stores idioms, phrases, and their multi-dimensional meanings
CREATE TABLE IF NOT EXISTS idioms_phrases (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  phrase TEXT NOT NULL,
  literal_meaning TEXT,  -- Literal meaning
  figurative_meaning TEXT,  -- Figurative/idiomatic meaning
  cultural_context TEXT,  -- Cultural context
  origin TEXT,  -- Origin of the idiom/phrase
  usage_examples TEXT[],  -- Usage examples
  semantic_layers JSONB,  -- Multi-dimensional meanings
  gematria_values JSONB,  -- Gematria values for the phrase
  associated_words TEXT[],  -- Associated words
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_idioms_phrases_phrase ON idioms_phrases(phrase);
CREATE INDEX IF NOT EXISTS idx_idioms_phrases_literal ON idioms_phrases(literal_meaning);
CREATE INDEX IF NOT EXISTS idx_idioms_phrases_figurative ON idioms_phrases(figurative_meaning);

-- ============================================================================
-- 10. VIEWS FOR COMMON QUERIES
-- ============================================================================

-- View for complete word information (joins baseline + semantic layers)
CREATE OR REPLACE VIEW word_complete AS
SELECT 
  gw.id as gematria_id,
  gw.phrase,
  gw.jewish_gematria,
  gw.english_gematria,
  gw.simple_gematria,
  gw.source as baseline_source,
  wr.root_word,
  wr.root_language,
  wr.etymology,
  array_agg(DISTINCT sl.layer_type) as semantic_layers,
  array_agg(DISTINCT sl.layer_value) as semantic_values,
  lf.frequency_score as current_frequency,
  gw.created_at,
  gw.updated_at
FROM gematria_words gw
LEFT JOIN word_roots wr ON gw.phrase = wr.word
LEFT JOIN semantic_layers sl ON gw.phrase = sl.word
LEFT JOIN language_frequency lf ON gw.phrase = lf.word AND lf.time_period = 'contemporary'
GROUP BY gw.id, gw.phrase, gw.jewish_gematria, gw.english_gematria, gw.simple_gematria, 
         gw.source, wr.root_word, wr.root_language, wr.etymology, lf.frequency_score, 
         gw.created_at, gw.updated_at;

-- View for word associations network
CREATE OR REPLACE VIEW word_associations_network AS
SELECT 
  wa.word1,
  wa.word2,
  wa.association_type,
  wa.strength,
  wa.gematria_values,
  wa.semantic_overlap,
  gw1.english_gematria as word1_english,
  gw2.english_gematria as word2_english,
  gw1.jewish_gematria as word1_jewish,
  gw2.jewish_gematria as word2_jewish
FROM word_associations wa
LEFT JOIN gematria_words gw1 ON wa.word1 = gw1.phrase
LEFT JOIN gematria_words gw2 ON wa.word2 = gw2.phrase
WHERE wa.strength > 0.5  -- Only show strong associations
ORDER BY wa.strength DESC;

-- ============================================================================
-- 11. COMMENTS & DOCUMENTATION
-- ============================================================================

COMMENT ON TABLE word_roots IS 'Stores root words, etymology, and linguistic history - separate from baseline gematria';
COMMENT ON TABLE semantic_layers IS 'Stores multi-dimensional word meanings (color, fruit, meaning, religious, etc.) - separate from baseline';
COMMENT ON TABLE word_associations IS 'Stores symmetry and deeper associations between words - separate from baseline';
COMMENT ON TABLE alphabet_mappings IS 'Stores cross-language alphabet mappings (Greek, Roman, Hebrew, etc.)';
COMMENT ON TABLE numeral_systems IS 'Stores Greek and Roman numeral systems';
COMMENT ON TABLE symbols_sacred_geometry IS 'Stores symbols, sacred geometry, and esoteric associations';
COMMENT ON TABLE language_frequency IS 'Stores historical and current frequency data for words';
COMMENT ON TABLE master_blobs IS 'Stores master blob structures for indexing without polluting baselines';
COMMENT ON TABLE idioms_phrases IS 'Stores idioms, phrases, and their multi-dimensional meanings';

