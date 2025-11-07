# Product Requirements Document (PRD)

## Overview

**Product Name:** Gematria Hive (v0.1: Foundation for Extraction, Ingestion, MCP/Agents)

**Goal:** Create a self-scaffolding ecosystem for data triangulation, unification, and eternal truth pursuit, starting with bookmark/photo ingestion to enable scaling agents/skills, generative media, and proofs.

**Target:** Developer-led with agent autonomy; full visibility for all layers.

---

## Objectives

1. Extract/distill 1000s bookmarks/photos → Ingest to DB with master/dynamic copies → Scale agents/skills for inferences/leaps/narratives/proofs (e.g., "Generate game level from 369 proof")
2. Self-scaffolding: Agents review/update models, logs, and flows; measure accuracy/efficiency/costs

---

## Features

### Modular Agents/Skills

- **Extraction** (Dewey/OCR/CapRL)
- **Distillation** (embed/summarize with StringZilla/SimSIMD)
- **Ingestion** (Pixeltable to DB)
- **Inference** (DeepAnalyze/vLLM for reports)
- **Proofs** (SymPy/IGGT/Omniverse)
- **Generative** (media/games from unifications)

### Prompt Layers

- **System** (vision guardrails: "Pursue truth with falsifiability")
- **MCP** (orchestration: "Triangulate data, log leaps, update master DB")
- **Task** (explicit: "Filter cosine >0.7; measure costs")

### DB Structure

- **Bookmarks** (id, url, summary, embedding vector(384), tags array, timestamp)
- **Hunches** (id, timestamp, content, links, status, cost)
- **Proofs** (id, theorem, report, accuracy_metric, efficiency_score)
- Master/Dynamic copies via replication/views

### Enhancements

- Extropic for leaps
- ProfBench evals
- Multiple LLMs/caches for views (geometrical/matrix)
- Kanban integration for tasks/ideas/possibilities/statuses/costs

### Unifying Goal

Convergence without infinity—bound by reason; segment domains but overlap for synergy.

---

## Tech Requirements

Consolidated stack as above; Python base; Docker for DBs; Claude skills for queries/narratives.

See README.md for full tech stack details.

---

## Scope & Phases

### Phase 1 (Foundation)

Env/DB setup, ingestion for bookmarks/photos.

**Success Metrics:**
- DB populated
- Agents run without errors
- Proofs/reports generated
- Costs < threshold

**Out of Scope:**
- Full game/media (defer)
- Unbounded scaling (cap at validated unifications)

---

## Assumptions/Risks

- **Manual start**
- **Risks:**
  - Scope—mitigate with kanban
  - Costs—log/optimize

---

## Success Criteria

### Phase 1 Success Metrics

- Database populated with bookmarks/photos
- Agents run without errors
- Proofs/reports generated successfully
- Costs maintained below threshold

### Long-term Success Metrics

- Self-scaffolding system operational
- Multiple validated proofs generated
- Generative media pipeline functional
- Cross-domain unifications discovered
- Community engagement and contribution

---

## Dependencies

- Supabase/ClickHouse database setup
- API keys for MCP services
- Docker environment configured
- Python virtual environment with dependencies

---

## Timeline

See README.md Roadmap section for detailed phases.

---

## Notes

This PRD is a living document and will be updated as the project evolves. For full project vision and technical details, see README.md.

