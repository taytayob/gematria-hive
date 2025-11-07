-- Enhanced Kanban Schema for Gematria Hive
-- Purpose: Add phases, metadata, resources, tags, and role management
-- Date: 2025-01-06

-- ============================================================================
-- ENHANCE HUNCHES TABLE (Tasks)
-- ============================================================================

-- Add new columns to hunches table
ALTER TABLE hunches ADD COLUMN IF NOT EXISTS phase TEXT DEFAULT 'phase1_basic';
ALTER TABLE hunches ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}'::jsonb;
ALTER TABLE hunches ADD COLUMN IF NOT EXISTS tags TEXT[] DEFAULT '{}';
ALTER TABLE hunches ADD COLUMN IF NOT EXISTS resources TEXT[] DEFAULT '{}';
ALTER TABLE hunches ADD COLUMN IF NOT EXISTS assigned_to TEXT;
ALTER TABLE hunches ADD COLUMN IF NOT EXISTS role TEXT DEFAULT 'developer';
ALTER TABLE hunches ADD COLUMN IF NOT EXISTS priority TEXT DEFAULT 'medium';
ALTER TABLE hunches ADD COLUMN IF NOT EXISTS project_id UUID REFERENCES projects(id);
ALTER TABLE hunches ADD COLUMN IF NOT EXISTS parent_task_id UUID REFERENCES hunches(id);
ALTER TABLE hunches ADD COLUMN IF NOT EXISTS due_date TIMESTAMPTZ;
ALTER TABLE hunches ADD COLUMN IF NOT EXISTS estimated_hours FLOAT;
ALTER TABLE hunches ADD COLUMN IF NOT EXISTS actual_hours FLOAT;
ALTER TABLE hunches ADD COLUMN IF NOT EXISTS progress INTEGER DEFAULT 0;
ALTER TABLE hunches ADD COLUMN IF NOT EXISTS dependencies TEXT[];
ALTER TABLE hunches ADD COLUMN IF NOT EXISTS labels TEXT[] DEFAULT '{}';

-- Indexes for enhanced hunches
CREATE INDEX IF NOT EXISTS idx_hunches_phase ON hunches(phase);
CREATE INDEX IF NOT EXISTS idx_hunches_tags ON hunches USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_hunches_resources ON hunches USING GIN(resources);
CREATE INDEX IF NOT EXISTS idx_hunches_assigned_to ON hunches(assigned_to);
CREATE INDEX IF NOT EXISTS idx_hunches_role ON hunches(role);
CREATE INDEX IF NOT EXISTS idx_hunches_priority ON hunches(priority);
CREATE INDEX IF NOT EXISTS idx_hunches_project_id ON hunches(project_id);
CREATE INDEX IF NOT EXISTS idx_hunches_parent_task_id ON hunches(parent_task_id);
CREATE INDEX IF NOT EXISTS idx_hunches_due_date ON hunches(due_date);
CREATE INDEX IF NOT EXISTS idx_hunches_labels ON hunches USING GIN(labels);
CREATE INDEX IF NOT EXISTS idx_hunches_metadata ON hunches USING GIN(metadata);

-- ============================================================================
-- RESOURCES TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS task_resources (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id UUID REFERENCES hunches(id) ON DELETE CASCADE,
  resource_type TEXT NOT NULL,  -- 'url', 'file', 'document', 'code', 'image', 'video', etc.
  resource_name TEXT NOT NULL,
  resource_url TEXT,
  resource_path TEXT,
  resource_content TEXT,
  resource_metadata JSONB DEFAULT '{}'::jsonb,
  tags TEXT[] DEFAULT '{}',
  created_by TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_task_resources_task_id ON task_resources(task_id);
CREATE INDEX IF NOT EXISTS idx_task_resources_type ON task_resources(resource_type);
CREATE INDEX IF NOT EXISTS idx_task_resources_tags ON task_resources USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_task_resources_name ON task_resources(resource_name);

-- ============================================================================
-- ROLES TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS roles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  role_name TEXT NOT NULL UNIQUE,  -- 'project_manager', 'product_manager', 'developer', etc.
  role_display_name TEXT NOT NULL,
  role_description TEXT,
  permissions JSONB DEFAULT '{}'::jsonb,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insert default roles
INSERT INTO roles (role_name, role_display_name, role_description, permissions) VALUES
  ('project_manager', 'Project Manager', 'Manages project phases, timelines, and resources', '{"can_create_tasks": true, "can_assign_tasks": true, "can_view_all": true, "can_manage_phases": true}'::jsonb),
  ('product_manager', 'Product Manager', 'Manages product requirements, features, and roadmap', '{"can_create_tasks": true, "can_assign_tasks": true, "can_view_all": true, "can_manage_prd": true}'::jsonb),
  ('developer', 'Developer', 'Develops features, fixes bugs, implements solutions', '{"can_create_tasks": true, "can_assign_tasks": false, "can_view_assigned": true, "can_update_status": true}'::jsonb),
  ('designer', 'Designer', 'Creates designs, mockups, and user interfaces', '{"can_create_tasks": true, "can_assign_tasks": false, "can_view_assigned": true, "can_update_status": true}'::jsonb),
  ('qa', 'QA Engineer', 'Tests features, reports bugs, validates quality', '{"can_create_tasks": true, "can_assign_tasks": false, "can_view_assigned": true, "can_update_status": true}'::jsonb)
ON CONFLICT (role_name) DO NOTHING;

CREATE INDEX IF NOT EXISTS idx_roles_name ON roles(role_name);

-- ============================================================================
-- PHASES TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS phases (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  phase_name TEXT NOT NULL UNIQUE,  -- 'phase1_basic', 'phase2_deep', 'phase3_advanced', etc.
  phase_display_name TEXT NOT NULL,
  phase_description TEXT,
  phase_order INTEGER DEFAULT 0,
  project_id UUID REFERENCES projects(id),
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insert default phases
INSERT INTO phases (phase_name, phase_display_name, phase_description, phase_order) VALUES
  ('phase1_basic', 'Phase 1: Foundation', 'Basic setup, core features, initial implementation', 1),
  ('phase2_deep', 'Phase 2: Deep Analysis', 'Advanced features, deep analysis, optimization', 2),
  ('phase3_advanced', 'Phase 3: Advanced', 'Advanced features, scaling, enterprise', 3),
  ('phase4_scale', 'Phase 4: Scale', 'Scaling, performance, enterprise features', 4)
ON CONFLICT (phase_name) DO NOTHING;

CREATE INDEX IF NOT EXISTS idx_phases_name ON phases(phase_name);
CREATE INDEX IF NOT EXISTS idx_phases_order ON phases(phase_order);
CREATE INDEX IF NOT EXISTS idx_phases_project_id ON phases(project_id);

-- ============================================================================
-- TASK COMMENTS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS task_comments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id UUID REFERENCES hunches(id) ON DELETE CASCADE,
  comment_text TEXT NOT NULL,
  created_by TEXT NOT NULL,
  role TEXT,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_task_comments_task_id ON task_comments(task_id);
CREATE INDEX IF NOT EXISTS idx_task_comments_created_by ON task_comments(created_by);
CREATE INDEX IF NOT EXISTS idx_task_comments_created_at ON task_comments(created_at);

-- ============================================================================
-- TASK HISTORY TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS task_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id UUID REFERENCES hunches(id) ON DELETE CASCADE,
  action TEXT NOT NULL,  -- 'created', 'updated', 'status_changed', 'assigned', etc.
  field_name TEXT,
  old_value TEXT,
  new_value TEXT,
  changed_by TEXT,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_task_history_task_id ON task_history(task_id);
CREATE INDEX IF NOT EXISTS idx_task_history_action ON task_history(action);
CREATE INDEX IF NOT EXISTS idx_task_history_created_at ON task_history(created_at);

-- ============================================================================
-- TASK RELATIONSHIPS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS task_relationships (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id UUID REFERENCES hunches(id) ON DELETE CASCADE,
  related_task_id UUID REFERENCES hunches(id) ON DELETE CASCADE,
  relationship_type TEXT NOT NULL,  -- 'blocks', 'blocked_by', 'relates_to', 'duplicates', etc.
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(task_id, related_task_id, relationship_type)
);

CREATE INDEX IF NOT EXISTS idx_task_relationships_task_id ON task_relationships(task_id);
CREATE INDEX IF NOT EXISTS idx_task_relationships_related_task_id ON task_relationships(related_task_id);
CREATE INDEX IF NOT EXISTS idx_task_relationships_type ON task_relationships(relationship_type);

-- ============================================================================
-- VIEWS FOR AGENT/MCP NAVIGATION
-- ============================================================================

-- View for tasks by phase and role
CREATE OR REPLACE VIEW tasks_by_phase_role AS
SELECT 
  h.id,
  h.content,
  h.status,
  h.phase,
  h.role,
  h.assigned_to,
  h.priority,
  h.project_id,
  h.tags,
  h.labels,
  h.cost,
  h.progress,
  h.due_date,
  h.created_at,
  h.updated_at,
  p.phase_display_name,
  r.role_display_name,
  pr.project_name
FROM hunches h
LEFT JOIN phases p ON h.phase = p.phase_name
LEFT JOIN roles r ON h.role = r.role_name
LEFT JOIN projects pr ON h.project_id = pr.id;

-- View for task resources
CREATE OR REPLACE VIEW task_resources_view AS
SELECT 
  tr.id,
  tr.task_id,
  tr.resource_type,
  tr.resource_name,
  tr.resource_url,
  tr.resource_path,
  tr.tags,
  tr.created_at,
  h.content as task_content,
  h.status as task_status,
  h.phase as task_phase
FROM task_resources tr
JOIN hunches h ON tr.task_id = h.id;

-- View for task statistics by phase
CREATE OR REPLACE VIEW task_stats_by_phase AS
SELECT 
  phase,
  status,
  COUNT(*) as task_count,
  SUM(cost) as total_cost,
  AVG(cost) as avg_cost,
  AVG(progress) as avg_progress
FROM hunches
GROUP BY phase, status;

-- View for task statistics by role
CREATE OR REPLACE VIEW task_stats_by_role AS
SELECT 
  role,
  status,
  COUNT(*) as task_count,
  SUM(cost) as total_cost,
  AVG(cost) as avg_cost,
  AVG(progress) as avg_progress
FROM hunches
GROUP BY role, status;

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE task_resources IS 'Resources associated with tasks (URLs, files, documents, etc.)';
COMMENT ON TABLE roles IS 'Role definitions for task assignment and permissions';
COMMENT ON TABLE phases IS 'Project phases for task organization';
COMMENT ON TABLE task_comments IS 'Comments on tasks for collaboration';
COMMENT ON TABLE task_history IS 'History of all task changes for audit trail';
COMMENT ON TABLE task_relationships IS 'Relationships between tasks (blocks, relates to, etc.)';
COMMENT ON VIEW tasks_by_phase_role IS 'View for agent/MCP navigation by phase and role';
COMMENT ON VIEW task_resources_view IS 'View for agent/MCP resource navigation';
COMMENT ON VIEW task_stats_by_phase IS 'Statistics view for phase-based analysis';
COMMENT ON VIEW task_stats_by_role IS 'Statistics view for role-based analysis';

