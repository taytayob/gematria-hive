# Architecture & Design Decisions

**Purpose:** Document key architectural choices, rationale, alternatives considered, and future considerations.

**Last Updated:** November 6, 2025

---

## Decision Log

### ADR-001: Use Streamlit for Initial UI (Phase 1)

**Date:** November 6, 2025  
**Status:** ✅ Accepted  
**Context:** Need rapid prototyping framework for gematria calculator.

**Decision:** Use Streamlit instead of React/Vue/Flask.

**Rationale:**
- **Speed:** Streamlit = pure Python, no frontend code needed
- **Replit integration:** Native support, easy deployment
- **Prototyping:** Perfect for Phase 1 MVP
- **Learning curve:** Minimal (team knows Python)

**Alternatives Considered:**
1. **Flask + Jinja2:** More control, but slower dev time
2. **React + FastAPI:** Modern stack, but overkill for Phase 1
3. **Django:** Too heavy for simple calculator

**Consequences:**
- ✅ Rapid development (Phase 1 done in 1 week)
- ✅ Easy deployment on Replit
- ⚠️ Less customization than React
- ⚠️ May need migration to React in Phase 5 for complex UX

**Future Review:** Phase 5 (evaluate if Streamlit scales for games/complex UI)

---

### ADR-002: Supabase for Phase 2 Database

**Date:** November 6, 2025  
**Status:** 🔄 Proposed  
**Context:** Need managed database with vector search for 1M+ words.

**Decision:** Use Supabase (PostgreSQL + pgvector) instead of self-hosted Postgres or NoSQL.

**Rationale:**
- **Managed:** Auto-backups, scaling, minimal ops
- **pgvector:** Native vector search for embeddings
- **Free tier:** 500MB free, $25/mo for 8GB
- **Replit-friendly:** REST API, easy integration

**Alternatives Considered:**
1. **Self-hosted PostgreSQL:** Full control, but ops burden
2. **MongoDB + Atlas Vector Search:** Good for unstructured data, but team knows SQL
3. **Pinecone:** Vector-specialized, but expensive ($70+/mo)
4. **Chroma:** Good for local dev, but harder to deploy

**Consequences:**
- ✅ Minimal DevOps overhead
- ✅ Vector search built-in
- ✅ Free tier for early development
- ⚠️ Vendor lock-in (mitigation: keep DB layer abstracted)
- ⚠️ Cost scales with data ($25/mo → $100+/mo at 50GB)

**Future Review:** Phase 3 (if cost exceeds $100/mo, consider migration to self-hosted)

---

### ADR-003: ClickHouse for Analytics (Phase 3)

**Date:** November 6, 2025  
**Status:** 🔄 Proposed  
**Context:** Need OLAP database for pattern discovery, heavy aggregations.

**Decision:** Use ClickHouse instead of adding analytics to Supabase.

**Rationale:**
- **OLAP-optimized:** 100x faster for aggregations vs. Postgres
- **Petabyte-scale:** Future-proof for massive datasets
- **Columnar:** Efficient storage for analytical queries
- **Free self-hosted:** Can start on Replit, migrate to cloud later

**Alternatives Considered:**
1. **Postgres with Timescale:** Good for time-series, but not general analytics
2. **DuckDB:** Excellent for local analytics, but harder to deploy as service
3. **BigQuery:** Powerful, but expensive and GCP lock-in
4. **Databend:** Rust-based alternative, less mature

**Consequences:**
- ✅ Blazing fast analytics
- ✅ Can start free (self-hosted)
- ⚠️ Need to maintain sync pipeline (Supabase → ClickHouse)
- ⚠️ Adds operational complexity (two databases)

**Decision Rule:** Only add ClickHouse if:
- Supabase analytics queries take >5 seconds
- Dataset exceeds 10M rows
- Need real-time dashboards

**Future Review:** Phase 3 (reassess if DuckDB or Postgres + Timescale sufficient)

---

### ADR-004: Local Embeddings vs. API

**Date:** November 6, 2025  
**Status:** 🔄 Proposed  
**Context:** Need text embeddings for semantic search in Phase 2.

**Decision:** Use local sentence-transformers (all-MiniLM-L6-v2) instead of OpenAI/Cohere APIs.

**Rationale:**
- **Cost:** Local = free (compute only), API = $0.0001/token × 1M words = $100+
- **Privacy:** No data sent to third parties
- **Speed:** Batch processing on Replit = 1M words in 2-3 hours
- **Control:** Can switch models anytime

**Alternatives Considered:**
1. **OpenAI text-embedding-ada-002:** High quality, but $$$
2. **Cohere Embed:** Competitive, but $0.0001/token
3. **Hugging Face Inference API:** Cheap, but rate limits

**Consequences:**
- ✅ Zero recurring cost
- ✅ Full control over model
- ⚠️ Upfront compute time (2-3 hours for 1M words)
- ⚠️ Model quality: MiniLM < OpenAI (acceptable tradeoff)

**Upgrade Path:** If semantic search accuracy <85%, upgrade to:
1. `mpnet-base-v2` (768 dims, better quality)
2. OpenAI embeddings (best quality, highest cost)

**Future Review:** Phase 2 (after testing semantic search accuracy)

---

### ADR-005: Gematria Calculation Methods

**Date:** November 6, 2025  
**Status:** ✅ Accepted  
**Context:** Phase 1 calculator needs distinct methods, not duplicates.

**Decision:** Implement Standard (A=1...Z=26) and Reduced (Pythagorean, A=1...I=9 repeating).

**Rationale:**
- **User value:** Reduced method provides different perspective
- **Correctness:** Initial duplicate methods were misleading
- **Extensibility:** Easy to add Hebrew, Greek, Full later

**Alternatives Considered:**
1. **Only Standard:** Simpler, but less useful
2. **Hebrew gematria:** Authentic, but need Hebrew alphabet support (Phase 2)
3. **Full gematria (A=1, B=2, ...Z=800):** Complex, defer to Phase 2

**Consequences:**
- ✅ Calculator now provides distinct value
- ✅ Users can compare methods
- ✅ Architecture supports adding more methods

**Implementation:**
```python
if method == 'standard':
    values = {chr(i + 96): i for i in range(1, 27)}
elif method == 'reduced':
    values = {chr(i + 96): ((i - 1) % 9) + 1 for i in range(1, 27)}
```

**Future Review:** Phase 2 (add Hebrew, Greek, Full methods)

---

### ADR-006: Replit for Hosting & Deployment

**Date:** November 6, 2025  
**Status:** ✅ Accepted  
**Context:** Need simple deployment for Phase 1 MVP.

**Decision:** Use Replit's built-in deployment (autoscale) instead of Vercel/Heroku/AWS.

**Rationale:**
- **Integrated:** Code, host, deploy in one platform
- **Secrets management:** Replit handles env vars securely
- **Auto-scaling:** Handles traffic spikes automatically
- **Rollback:** Built-in version control and rollback features

**Alternatives Considered:**
1. **Vercel:** Great for Next.js, but Streamlit not supported
2. **Heroku:** Classic choice, but $7/mo minimum, deprecated free tier
3. **AWS ECS/Lambda:** Most powerful, but complex setup
4. **DigitalOcean:** Affordable ($5/mo), but manual DevOps

**Consequences:**
- ✅ Zero DevOps burden
- ✅ Built-in SSL, domain, CDN
- ✅ Easy rollback (critical for safety)
- ⚠️ Vendor lock-in (mitigation: keep Docker-ready for migration)
- ⚠️ Cost unknown at scale (monitor closely in Phase 4+)

**Deployment Config:**
```toml
[deployment]
run = ["streamlit", "run", "app.py", "--server.port=5000"]
deploymentTarget = "autoscale"
```

**Future Review:** Phase 5 (if cost >$100/mo or need multi-region, consider AWS/Cloudflare)

---

### ADR-007: Pytest for Testing (Phase 2)

**Date:** November 6, 2025  
**Status:** 🔄 Proposed  
**Context:** Phase 2 adds complexity (DB, embeddings), need tests to prevent regressions.

**Decision:** Use pytest instead of unittest or no tests.

**Rationale:**
- **Industry standard:** Most popular Python testing framework
- **Fixtures:** Easy to set up test data
- **Plugins:** Great ecosystem (pytest-cov, pytest-asyncio)
- **Readable:** Simple assert statements

**Alternatives Considered:**
1. **unittest:** Built-in, but more verbose
2. **doctest:** Good for examples, not comprehensive tests
3. **No tests:** Faster dev, but risky for production

**Consequences:**
- ✅ Catch bugs early
- ✅ Refactor with confidence
- ✅ CI/CD integration (GitHub Actions)
- ⚠️ Upfront time investment (20% dev time)

**Testing Strategy:**
```
tests/
├── test_gematria.py          # Unit tests for calculator
├── test_database.py          # DB integration tests
├── test_embeddings.py        # Embedding generation tests
└── test_api.py               # End-to-end API tests
```

**Coverage Target:** >80% for critical paths (calculator, DB, search)

**Future Review:** Phase 2 (implement and assess ROI)

---

### ADR-008: LangChain for Agent Framework (Phase 4)

**Date:** November 6, 2025  
**Status:** 🔄 Proposed  
**Context:** Phase 4 needs multi-agent orchestration for autonomous research.

**Decision:** Use LangChain + LangGraph instead of custom agent framework or alternatives.

**Rationale:**
- **Mature:** Industry-standard, well-tested
- **Ecosystem:** 100+ integrations (OpenAI, Anthropic, Pinecone, etc.)
- **LangGraph:** Stateful workflows, better than basic chains
- **Community:** Large community, good docs

**Alternatives Considered:**
1. **AutoGPT / BabyAGI:** Good for exploration, but not production-ready
2. **Custom framework:** Full control, but reinventing wheel
3. **Semantic Kernel (Microsoft):** Good, but less mature than LangChain
4. **crewAI:** Promising, but very new

**Consequences:**
- ✅ Fast implementation (leverage existing tools)
- ✅ Easy LLM swapping (GPT-4 → Claude → local)
- ⚠️ Dependency on LangChain roadmap
- ⚠️ Learning curve for LangGraph

**Cost Control:**
- Use GPT-3.5 for simple tasks ($0.0015/1K tokens)
- GPT-4 only for complex reasoning ($0.03/1K tokens)
- Implement prompt caching to reduce tokens

**Future Review:** Phase 4 (evaluate crewAI if LangChain proves limiting)

---

### ADR-009: Git-based Version Control

**Date:** November 6, 2025  
**Status:** ✅ Accepted  
**Context:** Need version control for collaboration and rollback.

**Decision:** Use Git + GitHub instead of Replit-only versioning.

**Rationale:**
- **Standard:** Universal version control
- **Collaboration:** Easy for external contributors
- **CI/CD:** GitHub Actions for automated testing/deployment
- **Backup:** Code safe even if Replit account lost

**Alternatives Considered:**
1. **Replit versioning only:** Simpler, but limited features
2. **GitLab:** Good alternative, but GitHub more popular
3. **No version control:** Risky, not acceptable for production

**Consequences:**
- ✅ Full version history
- ✅ Can work offline (git clone)
- ✅ CI/CD integration
- ⚠️ Slight overhead (commit discipline)

**Commit Strategy:**
- Feature branches: `feature/embedding-search`
- Main branch: always deployable
- Auto-deploy: main → Replit production

**Future Review:** N/A (foundational decision)

---

### ADR-010: Cursor for Advanced Development (Optional)

**Date:** November 6, 2025  
**Status:** 🔄 Proposed (Optional)  
**Context:** User asked if staging should be in Cursor.

**Decision:** Use hybrid approach: Replit for hosting/deployment, Cursor for heavy coding.

**Rationale:**
- **Replit strengths:** Hosting, deployment, secrets, built-in preview
- **Cursor strengths:** Advanced coding, refactoring, local GPU, git workflows
- **Flexibility:** Use both as needed

**When to use Cursor:**
- Complex refactoring (Phase 3+)
- Heavy ML experimentation (local GPU)
- Multi-file code generation
- Deep debugging sessions

**When to use Replit:**
- Quick prototypes
- Testing live deployment
- Sharing with collaborators (instant links)
- Using Replit integrations (Supabase connector)

**Syncing Strategy:**
```bash
# Work in Cursor
git commit -m "Add proof validation agent"
git push origin main

# Pull in Replit
git pull origin main
# Replit auto-deploys
```

**Consequences:**
- ✅ Best of both worlds
- ✅ Team flexibility (some use Cursor, some use Replit)
- ⚠️ Need git discipline to avoid conflicts

**Staging Location Decision:**
- **Keep staging/ in git repo:** Accessible from both Replit and Cursor
- **Update from either platform:** Whoever is working updates docs
- **Single source of truth:** Git repo (not platform-specific)

**Future Review:** Phase 2 (test workflow, adjust as needed)

---

## Architecture Principles

### 1. **Modularity**
- Keep components loosely coupled
- Use abstraction layers (DB, LLM, embeddings)
- Easy to swap implementations

### 2. **Cost-Consciousness**
- Start free/cheap, scale as needed
- Monitor costs weekly in Phase 3+
- Implement hard budget limits in code

### 3. **Future-Proofing**
- Avoid vendor lock-in where possible
- Design for migration (Docker-ready, API abstraction)
- Keep data portable (standard formats: CSV, JSON)

### 4. **Simplicity**
- Choose boring technology when possible
- Avoid over-engineering in early phases
- YAGNI (You Aren't Gonna Need It) for Phase 1-2

### 5. **Observability**
- Log all important events
- Track metrics (API usage, query times, costs)
- Build dashboards in Phase 3+

---

## System Diagrams

### Phase 1 Architecture (Current)

```
┌──────────────┐
│   Browser    │
│  (User UI)   │
└──────┬───────┘
       │ HTTPS (Replit proxy)
       │
┌──────▼───────────────────┐
│   Streamlit App (app.py) │
│   - Calculator logic     │
│   - UI rendering         │
│   - Navigation          │
└──────────────────────────┘
```

### Phase 2 Architecture (Planned)

```
┌──────────────┐
│   Browser    │
└──────┬───────┘
       │
┌──────▼───────────────────┐
│   Streamlit App          │
│   ├─ Calculator          │
│   ├─ Search (semantic)   │
│   └─ Word lookup         │
└──────┬───────────────────┘
       │
┌──────▼─────────────────────────────┐
│   Business Logic Layer             │
│   ├─ Gematria calculator           │
│   ├─ Embedding generator           │
│   │   (sentence-transformers)      │
│   └─ Search engine                 │
└──────┬─────────────────────────────┘
       │
┌──────▼─────────────────────────────┐
│   Supabase (PostgreSQL + pgvector) │
│   ├─ words table (1M+ rows)        │
│   ├─ permutations table            │
│   └─ search_log table              │
└────────────────────────────────────┘
```

### Phase 4 Architecture (Planned)

```
┌──────────────┐
│   Browser    │
└──────┬───────┘
       │
┌──────▼────────────────┐
│   Streamlit UI        │
│   ├─ Calculator       │
│   ├─ Proof viewer     │
│   ├─ Geometry viz     │
│   └─ Agent dashboard  │
└──────┬────────────────┘
       │
┌──────▼───────────────────────────────────────┐
│   MCP Orchestrator (LangGraph)               │
│   ├─ Research Agent                          │
│   ├─ Proof Validation Agent                  │
│   ├─ Pattern Discovery Agent                 │
│   └─ Report Generation Agent                 │
└──────┬──────────────────┬────────────────────┘
       │                  │
┌──────▼───────┐   ┌──────▼────────────┐
│   Supabase   │   │   ClickHouse      │
│   (OLTP)     │   │   (OLAP)          │
│   - Words    │   │   - Patterns      │
│   - Proofs   │   │   - Analytics     │
│   - Memory   │   │   - Aggregations  │
└──────────────┘   └───────────────────┘
       │
┌──────▼────────────────┐
│   LLM APIs            │
│   ├─ OpenAI (GPT-4)   │
│   └─ Anthropic (Claude│
└───────────────────────┘
```

---

## Update Log

| Date | ADR | Change | Rationale |
|------|-----|--------|-----------|
| 2025-11-06 | All | Initial architecture decisions | Document foundational choices |
| TBD | ADR-002 | Finalize Supabase | After Phase 2 kickoff |
| TBD | ADR-010 | Update Cursor workflow | After testing hybrid approach |

---

**Next Steps:**
1. Review all proposed (🔄) ADRs before Phase 2
2. Update status to ✅ Accepted or ❌ Rejected
3. Document any new architectural decisions as they arise
