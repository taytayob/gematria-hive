# Cost Optimization & Efficiency Tracking

**Purpose:** Monitor costs, identify optimization opportunities, and track efficiency metrics across all phases.

**Last Updated:** November 6, 2025

---

## Current Costs (Phase 1)

| Service | Tier | Monthly Cost | Usage | Status |
|---------|------|--------------|-------|--------|
| **Replit** | Free | $0 | Hosting, dev environment | ✅ Sufficient |
| **Streamlit** | Open source | $0 | UI framework | ✅ Sufficient |
| **Python libraries** | N/A | $0 | Compute only | ✅ Sufficient |
| **GitHub** | Free | $0 | Version control | ✅ Sufficient |

**Total Phase 1 Cost:** **$0/month** ✅

---

## Projected Costs (Phase 2-5)

### Phase 2: Database & Word Index

| Service | Tier | Est. Cost | Justification | Optimization Strategy |
|---------|------|-----------|---------------|----------------------|
| **Supabase** | Free → Pro | $0-25/mo | 1M words = ~200MB, free tier = 500MB. Upgrade if >500MB or need pgvector | Start free, monitor size. Use compression. |
| **Compute (embeddings)** | Replit Free | $0 | One-time: 2-3 hours for 1M embeddings | Batch processing, cache results |
| **Replit** | Free → Hacker | $0-7/mo | May need more RAM for large queries | Start free, upgrade only if OOM errors |

**Estimated Phase 2 Cost:** **$0-32/mo**

**Optimization Checklist:**
- [ ] Compress embeddings (float32 → int8 = 75% size reduction, minimal accuracy loss)
- [ ] Use Supabase Row-Level Security (RLS) to limit query scope
- [ ] Implement query result caching (Redis or SQLite)
- [ ] Monitor Supabase dashboard for storage trends
- [ ] Set budget alert at $20/mo

---

### Phase 3: Sacred Geometry & Proofs

| Service | Tier | Est. Cost | Justification | Optimization Strategy |
|---------|------|-----------|---------------|----------------------|
| **Supabase** | Pro | $25/mo | More data (proofs, patterns) | Archive old data, use ClickHouse for analytics |
| **ClickHouse** | Self-hosted → Cloud | $0-100/mo | Start free (Replit), cloud if >10GB | Self-host as long as possible |
| **Replit** | Hacker | $7/mo | More RAM for geometry computations | Profile code, optimize memory usage |
| **Compute (SymPy)** | Included | $0 | CPU-bound, no GPU needed | Cache proof results |

**Estimated Phase 3 Cost:** **$32-132/mo**

**Optimization Checklist:**
- [ ] Use ClickHouse for read-heavy analytics (cheaper than Supabase for aggregations)
- [ ] Pre-compute common geometric patterns (cache)
- [ ] Lazy-load visualizations (don't generate until user requests)
- [ ] Consider DuckDB for local analytics (zero cost)
- [ ] Implement proof deduplication (avoid re-computing same theorems)

---

### Phase 4: Full MCP/Agents

| Service | Tier | Est. Cost | Justification | Optimization Strategy |
|---------|------|-----------|---------------|----------------------|
| **OpenAI API** | Pay-as-you-go | $50-150/mo | GPT-4: $0.03/1K tokens. Est. 5M tokens/mo | Use GPT-3.5 for simple tasks ($0.0015/1K) |
| **Anthropic API** | Pay-as-you-go | $50-150/mo | Claude: similar pricing. Backup for OpenAI | Prompt caching, reduce token usage |
| **Supabase** | Pro | $25/mo | Agent memory storage | Use TTL for old memories, compress data |
| **ClickHouse** | Cloud Basic | $50-100/mo | Heavy analytics for pattern discovery | Query optimization, partition pruning |
| **Replit** | Pro | $20/mo | More RAM/CPU for agents | Profile and optimize agent code |

**Estimated Phase 4 Cost:** **$195-445/mo**

**Critical Optimization Checklist:**
- [ ] **Implement LLM prompt caching** (OpenAI: 50% cost reduction on repeated prompts)
- [ ] **Use function calling** instead of long prompts (fewer tokens)
- [ ] **Set per-agent budget limits** in code (hard stop at threshold)
- [ ] **Retry logic with exponential backoff** (avoid wasted API calls on errors)
- [ ] **Use local models** for simple tasks (Llama, Mistral via Ollama)
- [ ] **Monitor API usage daily** (set up alerts at 80% of budget)
- [ ] **Implement request batching** (group API calls where possible)
- [ ] **Use GPT-3.5-turbo for 80% of tasks**, GPT-4 only for complex reasoning

**Cost Control Automation:**
```python
# Example: Budget limit in agent code
MAX_MONTHLY_BUDGET = 400  # USD
current_spend = get_openai_usage()  # From OpenAI API

if current_spend > MAX_MONTHLY_BUDGET:
    raise BudgetExceededError("Monthly budget exceeded, pausing agents")
```

---

### Phase 5: Expansion & Generative Media

| Service | Tier | Est. Cost | Justification | Optimization Strategy |
|---------|------|-----------|---------------|----------------------|
| **All Phase 4 costs** | | $195-445/mo | Baseline | Continue Phase 4 optimizations |
| **CDN (Cloudflare)** | Free → Pro | $0-20/mo | Global distribution for media | Start free (500GB/mo), upgrade if needed |
| **ElevenLabs** | Starter | $5-30/mo | Text-to-speech for videos | Use sparingly, cache audio |
| **Stripe** | Pay-as-you-go | 2.9% + $0.30 | Payment processing | No optimization needed |
| **Replit** | Pro → Teams | $20-40/mo | Scale for traffic | Monitor metrics, upgrade only if needed |
| **Storage (S3/R2)** | Pay-as-you-go | $5-20/mo | Store generated games/videos | Use compression, lifecycle policies |

**Estimated Phase 5 Cost:** **$225-555/mo** (before revenue)

**Revenue Target:** **$1000+/mo** (breakeven at Month 5-6)

**Optimization Checklist:**
- [ ] Use Cloudflare R2 instead of AWS S3 (cheaper egress)
- [ ] Implement aggressive caching for static assets (CDN edge)
- [ ] Lazy-load media (don't generate unless user requests)
- [ ] Use open-source alternatives (Pygame > Godot > Unity for cost)
- [ ] Monitor CAC (Customer Acquisition Cost), aim for <$50
- [ ] Optimize API pricing tiers (negotiate if usage >100K req/mo)

---

## Cost Control Strategies

### 1. **Start Free, Scale Smart**

**Principle:** Use free tiers until they break, then upgrade incrementally.

**Example:**
- Supabase: Free (500MB) → Pro ($25, 8GB) → Team ($599, 500GB)
- Replit: Free → Hacker ($7) → Pro ($20)

**Trigger Points:**
- Supabase: Upgrade when >400MB used (80% of free tier)
- Replit: Upgrade when OOM errors occur frequently
- ClickHouse: Self-host until >10GB or >1M req/day

### 2. **Implement Hard Budget Limits**

**Code-based budgets:**
```python
# In config.py
MONTHLY_BUDGETS = {
    "openai": 150,  # USD
    "anthropic": 150,
    "supabase": 50,
    "clickhouse": 100,
    "total": 450
}

# In agent code
if current_month_spend() > MONTHLY_BUDGETS["total"]:
    send_alert("Budget exceeded!")
    pause_non_critical_agents()
```

**Dashboard:** Track spend in Streamlit app (admin page)

### 3. **Aggressive Caching**

**Cache everything:**
- API responses (Redis TTL: 24 hours)
- Embeddings (never re-compute)
- Proof results (permanent storage)
- Gematria calculations (memoization)

**Cache Layers:**
```
L1: In-memory (Python dict)      - 0ms latency
L2: Redis (local)                - 1-5ms latency
L3: Supabase (remote)            - 10-50ms latency
```

**Estimated savings:** 70-90% reduction in API calls

### 4. **Use Cheaper Alternatives First**

**LLM Hierarchy:**
1. **Local models** (Llama 3, Mistral): $0, 2-5s latency
2. **GPT-3.5-turbo**: $0.0015/1K tokens, <1s latency
3. **GPT-4-turbo**: $0.01/1K tokens, 1-3s latency
4. **GPT-4**: $0.03/1K tokens, 2-5s latency

**Decision tree:**
- Simple queries (lookup, format): Local model
- Medium complexity (summarize, classify): GPT-3.5
- Complex reasoning (proofs, research): GPT-4

**Estimated savings:** 80% cost reduction vs. all GPT-4

### 5. **Monitor and Alert**

**Monitoring Tools:**
- Supabase: Built-in dashboard (storage, API calls)
- OpenAI: Usage API (tokens, costs)
- Replit: System metrics (RAM, CPU)
- Custom: Python logging → CSV → daily report

**Alerts:**
- Email: Cost >80% of monthly budget
- Slack/Discord: Critical errors, unusual spikes
- Daily summary: Cost breakdown by service

**Automation:**
```python
# Daily cost report (cron job)
def daily_cost_report():
    costs = {
        "openai": get_openai_cost(),
        "supabase": get_supabase_cost(),
        # ... other services
    }
    total = sum(costs.values())
    if total > MONTHLY_BUDGETS["total"] * 0.8:
        send_alert(f"Warning: ${total} spent this month")
```

### 6. **Optimize Queries**

**Database:**
- Use indexes (Supabase: `CREATE INDEX` on gematria values)
- Limit result sets (`LIMIT 100` for searches)
- Paginate (don't load 1M rows at once)
- Use materialized views for complex aggregations

**APIs:**
- Batch requests (send 10 at once vs. 10 individual calls)
- Compress payloads (gzip HTTP requests)
- Use streaming for long responses (OpenAI streaming)

**Estimated savings:** 50-70% reduction in query times → lower compute costs

---

## Efficiency Metrics

### Phase 1 Metrics (Baseline)

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| **Page load time** | <2s | ~1s | ✅ Excellent |
| **Calculator response** | <100ms | ~10ms | ✅ Excellent |
| **Memory usage** | <200MB | ~150MB | ✅ Good |
| **Uptime** | >99% | 100% (1 week) | ✅ Excellent |

### Phase 2 Target Metrics

| Metric | Target | Measurement | Optimization |
|--------|--------|-------------|--------------|
| **Word lookup time** | <100ms | `time.time()` before/after query | Add indexes, cache |
| **Semantic search time** | <500ms | Include embedding + search | Pre-compute embeddings |
| **Database size** | <500MB | Supabase dashboard | Compression, pruning |
| **Embedding generation** | <3 hours for 1M words | Batch processing time | Use GPU (Colab) or optimize batch size |

### Phase 4 Target Metrics

| Metric | Target | Measurement | Optimization |
|--------|--------|-------------|--------------|
| **Agent task completion** | <60s per task | LangChain callbacks | Optimize prompts, use GPT-3.5 |
| **API cost per proof** | <$0.50 | Token usage × price | Prompt caching, reduce tokens |
| **Agent accuracy** | >80% | ProfBench eval | Fine-tune prompts, better models |
| **Tokens per request** | <2000 | OpenAI API response | Compress prompts, use functions |

---

## ROI Analysis (Phase 5)

### Cost Breakdown (Month 1 of Phase 5)

| Category | Cost | % of Total |
|----------|------|------------|
| **Infrastructure** | $150 | 40% |
| **LLM APIs** | $150 | 40% |
| **Media/Tools** | $30 | 8% |
| **Hosting** | $20 | 5% |
| **Other** | $25 | 7% |
| **Total** | **$375** | **100%** |

### Revenue Projections

| Month | Users | Paying | Revenue | Cost | Profit |
|-------|-------|--------|---------|------|--------|
| **M1** | 100 | 5 | $50 | $375 | -$325 |
| **M2** | 300 | 20 | $200 | $400 | -$200 |
| **M3** | 600 | 50 | $500 | $425 | +$75 |
| **M4** | 1000 | 100 | $1000 | $450 | +$550 |
| **M5** | 1500 | 180 | $1800 | $475 | +$1325 |
| **M6** | 2000 | 300 | $3000 | $500 | +$2500 |

**Breakeven:** Month 3  
**Profitability:** Month 4+  
**Target:** $3000/mo revenue by Month 6

### Unit Economics

| Metric | Value | Notes |
|--------|-------|-------|
| **ARPU** (Avg Revenue Per User) | $10/mo | Freemium model, $9.99/mo premium |
| **CAC** (Customer Acquisition Cost) | <$50 | Organic + minimal ads |
| **LTV** (Lifetime Value) | $240 | Avg 24 months retention |
| **LTV:CAC Ratio** | 4.8:1 | Target >3:1 for healthy SaaS |
| **Churn Rate** | <5%/mo | Target <10% |

**Optimization Levers:**
1. **Increase ARPU:** Add premium tiers ($19.99, $49.99)
2. **Reduce CAC:** SEO, word-of-mouth, partnerships
3. **Improve retention:** Better features, community building

---

## Optimization Opportunities (Prioritized)

### High Impact, Low Effort (Do First)

1. **✅ Implement API caching** (Redis or SQLite)
   - Impact: 70% reduction in API calls
   - Effort: 1 day
   - Savings: $100+/mo in Phase 4

2. **✅ Use GPT-3.5 for simple tasks**
   - Impact: 80% cost reduction on routine queries
   - Effort: 2 hours (update agent logic)
   - Savings: $120+/mo in Phase 4

3. **✅ Compress embeddings (float32 → int8)**
   - Impact: 75% storage reduction
   - Effort: 4 hours
   - Savings: $15/mo on Supabase

4. **✅ Set budget alerts**
   - Impact: Prevent runaway costs
   - Effort: 1 hour
   - Savings: Priceless (avoid $1000+ surprise bills)

### Medium Impact, Medium Effort (Do in Phase 3-4)

5. **Implement ClickHouse for analytics**
   - Impact: 10x faster queries, cheaper than Supabase for OLAP
   - Effort: 1 week
   - Savings: $50/mo (offset by ClickHouse cost, but better performance)

6. **Local LLM for simple tasks**
   - Impact: Zero cost for 50% of tasks
   - Effort: 3 days (set up Ollama, test Llama 3)
   - Savings: $75/mo in Phase 4

7. **Optimize database indexes**
   - Impact: 3-5x faster queries
   - Effort: 2 days
   - Savings: Better UX, less timeout errors

### Low Impact, High Effort (Defer to Phase 5+)

8. **Custom embeddings model**
   - Impact: 10-20% better accuracy
   - Effort: 2-4 weeks (fine-tuning)
   - Savings: Marginal

9. **Multi-region deployment**
   - Impact: Lower latency for global users
   - Effort: 1 week
   - Savings: N/A (cost increase, but better UX)

---

## Waste Audit (Quarterly)

**Process:** Every 3 months, review all services and ask:

1. **Are we using this?** (Check logs, metrics)
2. **Can we downgrade?** (Review usage vs. tier limits)
3. **Is there a cheaper alternative?** (New tools, better pricing)
4. **Can we consolidate?** (Merge services, reduce complexity)

**Example Audit Questions:**
- Are we still using ClickHouse, or can Supabase handle analytics?
- Is Replit Pro needed, or can we downgrade to Hacker?
- Are we paying for unused Supabase storage? (Old data can be archived)
- Can we negotiate better API rates with OpenAI? (If >100K req/mo)

---

## Update Log

| Date | Change | Impact |
|------|--------|--------|
| 2025-11-06 | Initial cost tracking setup | Baseline for future optimization |
| TBD | Phase 2 actual costs | Compare to estimates, adjust |
| TBD | First optimization sprint | Implement caching, budget alerts |

---

**Next Steps:**
1. Set up cost monitoring dashboard in Streamlit (admin page)
2. Implement budget alerts (email/Slack)
3. Review this doc monthly, update projections
4. Celebrate when we hit profitability! 🎉
