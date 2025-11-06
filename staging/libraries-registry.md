# Libraries & Dependencies Registry

**Purpose:** Comprehensive tracking of all libraries, repos, and dependencies across the Gematria Hive ecosystem.

**Last Updated:** November 6, 2025

---

## Currently Implemented (Phase 1)

### Core Dependencies

| Library | Version | Purpose | Phase | Status | Cost Impact | Notes |
|---------|---------|---------|-------|--------|-------------|-------|
| `streamlit` | 1.51.0+ | Web UI framework | Phase 1 | ✅ Active | Low (free tier) | Primary interface. Fast prototyping. Consider Streamlit Cloud for hosting. |
| `pandas` | 2.3.3+ | Data manipulation | Phase 1 | ✅ Active | Low (compute) | Essential for CSV processing. Watch memory usage with large datasets. |
| `python-dotenv` | 1.2.1+ | Environment config | Phase 1 | ✅ Active | None | Secret management. Integrate with Replit Secrets for production. |

### Development Tools

| Tool | Purpose | Phase | Status | Notes |
|------|---------|-------|--------|-------|
| Python 3.11 | Runtime environment | Phase 1 | ✅ Active | Stable version. Type hints support. |
| Replit | Development & hosting | Phase 1 | ✅ Active | Primary dev environment. Built-in deployment. |

---

## Planned Dependencies (Phase 2+)

### Database Layer

| Library | Version | Purpose | Phase | Priority | Cost Estimate | Rationale |
|---------|---------|---------|-------|----------|---------------|-----------|
| `supabase-py` | 2.3.4+ | PostgreSQL + pgvector | Phase 2 | **HIGH** | $25/mo (Pro) | Relational data + embeddings. Free tier: 500MB. Upgrade for 8GB + vectors. |
| `clickhouse-connect` | 0.7.0+ | OLAP analytics | Phase 3 | MEDIUM | $0-500/mo | Petabyte-scale analytics. Start with self-hosted (free), migrate to cloud. |
| `databend-py` | TBD | Backup OLAP | Phase 4 | LOW | TBD | Rust-based alternative to ClickHouse. Future-proofing option. |

**Synergies:**
- Supabase handles transactional + semantic search (pgvector)
- ClickHouse for heavy analytics, aggregations, time-series
- Databend as cost-optimized fallback or multi-cloud strategy

**Constraints:**
- Supabase pgvector limited on free tier
- ClickHouse memory-intensive; watch instance sizing
- Need data pipeline for sync between DBs

**Future-Proofing:**
- Consider DuckDB for local analytics (zero cost)
- Evaluate Pinecone/Weaviate if vector workload grows
- Keep abstraction layer for easy DB swapping

---

### Embeddings & ML

| Library | Version | Purpose | Phase | Priority | Cost Estimate | Rationale |
|---------|---------|---------|-------|----------|---------------|-----------|
| `sentence-transformers` | 2.3.1+ | Text embeddings | Phase 2 | **HIGH** | Compute only | Local inference. Models: all-MiniLM-L6-v2 (small), mpnet-base-v2 (better). |
| `transformers` | Latest | Hugging Face models | Phase 2 | MEDIUM | Compute + API | Backup for custom models. Watch GPU costs on Replit. |
| `stringzilla` | Latest | Fast string ops | Phase 3 | MEDIUM | None | 10x faster string search. Replaces standard Python string methods. |
| `simsimd` | Latest | Vector similarity | Phase 3 | MEDIUM | None | Hardware-accelerated vector ops. Optimizes embedding search. |
| `usearch` | Latest | Vector search | Phase 3 | MEDIUM | None | Alternative to FAISS. Better for mobile/edge. |
| `vllm` | Latest | LLM inference | Phase 4 | LOW | High (GPU) | Production LLM serving. Sleep mode for cost control. |

**Synergies:**
- SentenceTransformers + SimSIMD = fast embedding generation + search
- StringZilla for pre-processing before embedding
- vLLM for production-grade inference with batching

**Cost Optimization:**
- Start with smallest sentence-transformer models
- Use Replit Secrets for API keys, avoid hardcoding
- Implement caching to reduce re-computation
- Consider Hugging Face Inference API for occasional use

**Things to Watch:**
- Model size vs. RAM (Replit limits)
- Inference latency on free/basic tiers
- Cold start times with vLLM

---

### Agentic/MCP Layer

| Library | Version | Purpose | Phase | Priority | Cost Estimate | Rationale |
|---------|---------|---------|-------|----------|---------------|-----------|
| `langchain` | Latest | Agent orchestration | Phase 3 | **HIGH** | API costs | Industry standard. Rich ecosystem. Watch token usage. |
| `langgraph` | Latest | Stateful agents | Phase 3 | **HIGH** | API costs | Built on LangChain. Better for complex flows. |
| `deepagents` | TBD | Advanced agents | Phase 4 | MEDIUM | TBD | Cutting-edge research. Evaluate maturity before use. |
| `tinker` | TBD | Agent fine-tuning | Phase 4 | LOW | Compute | Optimize agent trajectories. Research-stage tool. |
| `adp` | TBD | Agent dev platform | Phase 4 | LOW | TBD | Scaling agent skills. Experimental. |

**Synergies:**
- LangChain + LangGraph = flexible agent architecture
- DeepAgents for autonomous research/proofs
- Tinker/ADP for continuous agent improvement

**Constraints:**
- High API costs with GPT-4/Claude
- Need prompt caching strategies
- Rate limiting on free tiers

**Workarounds:**
- Start with GPT-3.5/Claude Haiku for prototyping
- Implement retry logic with exponential backoff
- Use local models (Llama, Mistral) where possible
- Replit AI can handle some agent tasks natively

**Related Modules:**
- `langsmith` for tracing/debugging
- `langserve` for deployment
- `chromadb` for agent memory

---

### Data Ingestion & Pipelines

| Library | Version | Purpose | Phase | Priority | Cost Estimate | Rationale |
|---------|---------|---------|-------|----------|---------------|-----------|
| `pixeltable` | Latest | Multimodal workflows | Phase 2 | **HIGH** | Compute | Unified interface for CSV/images/video. Reduces boilerplate. |
| `dewey` | TBD | X/IG bookmark sync | Phase 2 | MEDIUM | Free | Personal data extraction. Check API rate limits. |
| `caprl` | TBD | Image captioning | Phase 3 | LOW | Compute | Dense visual descriptions. Alternative: BLIP-2 API. |

**Synergies:**
- Pixeltable as central data hub
- Dewey feeds bookmarks → Pixeltable → embeddings
- CapRL enriches images → better semantic search

**Future-Proofing:**
- Pixeltable supports streaming, ready for real-time ingestion
- Can replace with custom Airflow/Prefect pipelines later
- Consider Apache Kafka for high-volume streams (Phase 5+)

---

### Geometry, Math & Quantum

| Library | Version | Purpose | Phase | Priority | Cost Estimate | Rationale |
|---------|---------|---------|-------|----------|---------------|-----------|
| `sympy` | Latest | Symbolic math | Phase 3 | **HIGH** | None | Theorem proving, symbolic geometry. Pure Python, no GPU needed. |
| `qiskit` | Latest | Quantum simulation | Phase 4 | MEDIUM | Compute | IBM quantum toolkit. Free simulator, paid real hardware access. |
| `iggt` | TBD | 3D reconstruction | Phase 4 | LOW | High (GPU) | Instance-grounded geometry. Research tool. |
| `vggt` | TBD | Video geometry | Phase 4 | LOW | High (GPU) | Video-based 3D. Cutting-edge. |

**Synergies:**
- SymPy for mathematical proofs → feeds into reports
- Qiskit for quantum-inspired algorithms
- IGGT/VGGT for sacred geometry visualizations

**Constraints:**
- Qiskit quantum hardware = paid credits
- 3D libs need GPU (expensive on Replit)
- Consider Google Colab for heavy GPU workloads

**Related Modules:**
- `matplotlib` / `plotly` for visualization
- `numpy` / `scipy` for numerical computation

---

### Visualization & Simulation

| Library | Version | Purpose | Phase | Priority | Cost Estimate | Rationale |
|---------|---------|---------|-------|----------|---------------|-----------|
| `matplotlib` | Latest | Static plots | Phase 2 | MEDIUM | None | Standard plotting. Good for reports. |
| `plotly` | Latest | Interactive viz | Phase 2 | MEDIUM | None | Better for web (Streamlit integration). |
| `nvidia-omniverse` | TBD | 3D simulation | Phase 5 | LOW | High (GPU+licensing) | High-fidelity wave/geometry sims. Overkill for Phase 1-3. |
| `pygame` | Latest | 2D games | Phase 5 | LOW | None | Generative media/games. Simple, no dependencies. |
| `godot-python` | TBD | 3D games | Phase 5 | LOW | None | Full game engine. Steep learning curve. |

**Synergies:**
- Plotly for interactive proofs in Streamlit
- Pygame for simple educational games
- Omniverse for high-end visualizations (if budget allows)

**Cost Optimization:**
- Use Plotly's free tier (works great with Streamlit)
- Pygame has zero cost, runs anywhere
- Defer Omniverse until revenue/funding secured

---

### Development & Ops

| Library | Version | Purpose | Phase | Priority | Cost Estimate | Rationale |
|---------|---------|---------|-------|----------|---------------|-----------|
| `pytest` | Latest | Testing | Phase 2 | **HIGH** | None | Industry standard. Must-have for production. |
| `black` | Latest | Code formatting | Phase 2 | MEDIUM | None | Consistent style. Auto-format. |
| `mypy` | Latest | Type checking | Phase 2 | MEDIUM | None | Catch bugs early. Python 3.11 support. |
| `docker` | Latest | Containerization | Phase 3 | MEDIUM | $5/mo (images) | Consistent environments. Note: Replit doesn't support Docker directly - use Nix instead. |
| `nix` | Latest | Package management | Phase 1 | ✅ Active | None | Replit's native package manager. Already configured. |

**Constraints:**
- Replit doesn't support nested Docker
- Use Nix for reproducible builds instead
- CI/CD via GitHub Actions (free tier: 2000 min/mo)

**Related Modules:**
- `pre-commit` for git hooks
- `poetry` / `uv` for dependency management (alternative to pip)

---

### Evaluation & Enhancement

| Library | Version | Purpose | Phase | Priority | Cost Estimate | Rationale |
|---------|---------|---------|-------|----------|---------------|-----------|
| `profbench` | TBD | Accuracy evals | Phase 4 | MEDIUM | TBD | Rubrics for reasoning. Ensure proof quality. |
| `nemo` | TBD | LLM evals | Phase 4 | LOW | TBD | NVIDIA toolkit. Overlaps with ProfBench. |
| `extropic-thrml` | TBD | Probabilistic sampling | Phase 4 | LOW | Research access | Thermodynamic computing. Experimental. |

**Future-Proofing:**
- Start with simple accuracy metrics (Phase 2)
- Graduate to ProfBench when proofs are complex
- Extropic as research moonshot, not critical path

---

## External Services & APIs

| Service | Purpose | Phase | Priority | Cost Estimate | Notes |
|---------|---------|-------|----------|---------------|-------|
| **Gematrix.org** | 1M+ word CSV | Phase 2 | **HIGH** | Free (scraping) | Check ToS. May need to contact for bulk export. |
| **OpenAI API** | GPT-4 for agents | Phase 3 | **HIGH** | $20-200/mo | Start with GPT-3.5. Use Replit integration for key management. |
| **Anthropic API** | Claude for reasoning | Phase 3 | MEDIUM | $20-200/mo | Alternative to OpenAI. Better for long context. |
| **Hugging Face** | Model hosting | Phase 2 | MEDIUM | Free-$9/mo | Free inference API (rate limited). Pro for faster access. |
| **Replit AI** | Built-in coding assistant | Phase 1 | ✅ Active | Included | Leverage for rapid prototyping. |
| **GitHub** | Version control | Phase 1 | ✅ Active | Free | Already configured. Enable Actions for CI/CD. |

**Cost Control Strategies:**
1. **Use Replit Integrations** for API key rotation and secret management
2. **Implement caching** for API responses (Redis or SQLite)
3. **Set budget alerts** for Supabase, OpenAI, etc.
4. **Start local, scale cloud** (e.g., local embeddings → hosted only if needed)
5. **Monitor with logging** (track API calls, costs per feature)

---

## Repositories to Track

| Repo | Purpose | Priority | Integration Phase | Status |
|------|---------|----------|-------------------|--------|
| `gematria-hive` (this repo) | Main project | **HIGH** | Phase 1 | ✅ Active |
| `langchain` | Agent framework | **HIGH** | Phase 3 | 📋 Planned |
| `pixeltable` | Data pipeline | **HIGH** | Phase 2 | 📋 Planned |
| `sentence-transformers` | Embeddings | **HIGH** | Phase 2 | 📋 Planned |
| `streamlit` | UI framework | **HIGH** | Phase 1 | ✅ Active |
| `supabase` | Database | **HIGH** | Phase 2 | 📋 Planned |
| Custom cursor configs | IDE setup | MEDIUM | Phase 2 | 📋 Planned |

---

## Integration Notes

### Cursor IDE Setup (Recommended for Advanced Development)

While Replit is excellent for prototyping, Cursor may be better for:
- Complex refactoring across many files
- Advanced git workflows
- Custom AI coding rules
- Local development with full control

**When to use Cursor:**
- Phase 3+ (when codebase grows beyond 50 files)
- Heavy ML experimentation (better GPU access)
- Team collaboration with custom workflows

**When to stay in Replit:**
- Rapid prototyping (Phase 1-2)
- Deployment (built-in publish)
- Serverless functions
- Integrated secrets management

**Hybrid Approach:**
1. Use Replit for hosting, testing, deployment
2. Use Cursor for heavy coding sessions
3. Keep git sync between both

---

## Update Log

| Date | Change | Rationale |
|------|--------|-----------|
| 2025-11-06 | Initial registry created | Centralize library tracking and planning |
| TBD | Add cost tracking column | Monitor spend per library |
| TBD | Link to phase roadmap | Cross-reference with development_phases.md |

---

**Maintenance Protocol:**
- Update this file whenever adding/removing dependencies
- Review quarterly for cost optimization opportunities
- Archive deprecated libraries to `staging/archive/`
- Cross-reference with `development_phases.md` for alignment
