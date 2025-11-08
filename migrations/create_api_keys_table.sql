-- API Keys Management Table
-- Purpose: Securely store and track API keys and configuration
-- Date: 2025-01-06

-- API Keys Table
CREATE TABLE IF NOT EXISTS api_keys (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  key_name TEXT NOT NULL UNIQUE,  -- e.g., 'INTERNAL_API_KEY', 'GOOGLE_API_KEY'
  key_type TEXT NOT NULL,  -- 'internal', 'external', 'oauth'
  key_value_hash TEXT,  -- Hashed value for verification (never store plain text!)
  key_status TEXT DEFAULT 'active',  -- 'active', 'inactive', 'revoked', 'expired'
  service_name TEXT,  -- e.g., 'Google', 'Anthropic', 'Perplexity'
  service_url TEXT,  -- URL to get/rotate the key
  description TEXT,
  last_used_at TIMESTAMPTZ,
  expires_at TIMESTAMPTZ,
  rotation_schedule TEXT,  -- e.g., '30 days', '90 days'
  metadata JSONB,  -- Additional metadata
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  created_by TEXT DEFAULT 'system'
);

CREATE INDEX IF NOT EXISTS idx_api_keys_name ON api_keys(key_name);
CREATE INDEX IF NOT EXISTS idx_api_keys_type ON api_keys(key_type);
CREATE INDEX IF NOT EXISTS idx_api_keys_status ON api_keys(key_status);
CREATE INDEX IF NOT EXISTS idx_api_keys_service ON api_keys(service_name);
CREATE INDEX IF NOT EXISTS idx_api_keys_expires ON api_keys(expires_at);

-- API Key Usage Log Table
CREATE TABLE IF NOT EXISTS api_key_usage_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  key_name TEXT NOT NULL REFERENCES api_keys(key_name),
  usage_type TEXT,  -- 'read', 'write', 'auth', 'rotate'
  endpoint TEXT,
  agent_name TEXT,
  success BOOLEAN DEFAULT TRUE,
  error_message TEXT,
  metadata JSONB,
  used_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_api_key_usage_key ON api_key_usage_log(key_name);
CREATE INDEX IF NOT EXISTS idx_api_key_usage_type ON api_key_usage_log(usage_type);
CREATE INDEX IF NOT EXISTS idx_api_key_usage_agent ON api_key_usage_log(agent_name);
CREATE INDEX IF NOT EXISTS idx_api_key_usage_time ON api_key_usage_log(used_at);

-- Trigger to update updated_at
CREATE TRIGGER update_api_keys_updated_at BEFORE UPDATE ON api_keys
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments
COMMENT ON TABLE api_keys IS 'API keys and configuration management - stores metadata only, never plain text keys';
COMMENT ON TABLE api_key_usage_log IS 'Log of API key usage for security and monitoring';

