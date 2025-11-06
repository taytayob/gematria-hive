# Gematria Hive - Project Overview

## Project Vision

Gematria Hive is a self-scaffolding AI ecosystem designed to unify gematria, numerology, sacred geometry, esoteric principles, and ancient knowledge with modern mathematics, physics, quantum mechanics, and AI/ML breakthroughs.

## Current Status: Phase 1 - Foundation (v0.1)

**Last Updated:** November 6, 2025

This is a fresh project setup containing:
- Basic Gematria Calculator using Streamlit
- Project scaffolding and configuration
- Database configuration templates (Supabase, ClickHouse)

## Project Structure

```
gematria-hive/
├── app.py                         # Main Streamlit application
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variable template
├── .streamlit/
│   └── config.toml               # Streamlit configuration
├── .gitignore                    # Git ignore patterns
├── README.md                     # Original project documentation
├── replit.md                     # This file (project memory)
└── staging/                      # Comprehensive planning & tracking
    ├── README.md                 # Staging area index & guide
    ├── libraries-registry.md     # All deps, repos, costs, integration plans
    ├── development-phases.md     # Detailed roadmap with milestones
    ├── architecture-decisions.md # ADR log with rationale
    └── cost-optimization.md      # Cost tracking, efficiency metrics, ROI
```

## Tech Stack

### Current Implementation (Phase 1)
- **Frontend:** Streamlit (Python web framework)
- **Language:** Python 3.11
- **Core Libraries:** pandas, python-dotenv
- **Port:** 5000 (configured for Replit webview)

### Planned Future Stack
- **Databases:** Supabase (relational + pgvector), ClickHouse (OLAP analytics)
- **Embeddings:** Sentence-Transformers, Hugging Face models
- **Agentic/MCP:** LangChain, LangGraph, DeepAgents
- **Geometry/Proofs:** SymPy, Qiskit
- **Additional Tools:** Pixeltable, Dewey, CapRL, vLLM

## Features

### Currently Implemented
- ✅ Basic gematria calculator (standard/ordinal methods)
- ✅ Character breakdown visualization
- ✅ Clean, responsive UI with navigation
- ✅ About page with project vision
- ✅ Setup guide with environment status

### Planned Features
- 📋 1M+ word database from gematrix.org
- 📋 Advanced calculation methods
- 📋 Phonetic analysis
- 📋 Etymological insights
- 📋 Sacred geometry visualizations
- 📋 MCP agent orchestration
- 📋 Proof generation and reports
- 📋 Generative media/games

## Development Roadmap

- **Phase 1:** Data foundation (Current) ✅
- **Phase 2:** Gematria app with full database
- **Phase 3:** Sacred geometry unifications
- **Phase 4:** Full MCP/agents implementation
- **Phase 5:** Expansion, sharing, generative media

## Environment Setup

### Required Environment Variables (for future phases)
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
CLICKHOUSE_HOST=your_clickhouse_host
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=your_password
```

See `.env.example` for template.

## Running the Application

The application runs automatically via Replit workflow:
- **Command:** `streamlit run app.py`
- **Port:** 5000
- **Host:** 0.0.0.0 (configured for Replit proxy)

## Architecture Notes

### Streamlit Configuration
- Configured to trust Replit's proxy (enableCORS=false, enableXsrfProtection=false)
- Binds to 0.0.0.0:5000 for proper webview display
- Headless mode enabled for server deployment

### Future Considerations
- Database migrations will use ORM tools
- Agent orchestration via MCP (Model Context Protocol)
- Modular architecture for scaling agents/skills
- Task tracking integrated with Kanban boards
- Cost/performance metrics logging

## User Preferences

- **Planning & Documentation:** Uses comprehensive staging area (`staging/`) for tracking libraries, costs, roadmap, and architecture decisions
- **Development Approach:** Phased development with clear milestones and success metrics
- **Cost Consciousness:** Careful budget tracking and optimization (see `staging/cost-optimization.md`)
- **IDE Preference:** Hybrid approach - Replit for hosting/deployment, option to use Cursor for heavy development
- **Documentation Style:** Detailed, structured, with rationale and alternatives considered

## Recent Changes

**November 6, 2025** - Initial Project Setup
- Created basic Streamlit application with gematria calculator
- Set up Python 3.11 environment
- Configured Streamlit for Replit (port 5000, CORS disabled)
- Added project structure and documentation
- Created .gitignore for Python projects
- Added environment variable templates
- **Created comprehensive staging area** (`staging/`) for project tracking:
  - Libraries registry with costs and synergies
  - 5-phase development roadmap with milestones
  - Architecture decision records (ADRs)
  - Cost optimization and efficiency tracking
- Fixed gematria calculator to implement distinct methods (Standard vs Reduced/Pythagorean)
- Configured deployment settings (autoscale)
