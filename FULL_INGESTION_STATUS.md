# Full Ingestion Status

**Date:** January 6, 2025  
**Status:** 🚀 **RUNNING**  
**Files:** `purchased-gematrix789.csv`, `purchased-gimatria789.csv`

---

## 🚀 Ingestion Started

### Files Being Processed
- **purchased-gematrix789.csv** - 511 MB, ~8,229,245 rows
- **purchased-gimatria789.csv** - 90 MB, ~659,635 rows

### Total Expected Records
- **English/Simple/Jewish:** ~8.2M records
- **Hebrew Variants:** ~659K records
- **Total:** ~8.9M records

---

## 📊 Progress Tracking

### Monitor Progress
```bash
# View live log
tail -f ingestion_full_run.log

# Check database count
python -c "
from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
result = supabase.table('gematria_words').select('*', count='exact').limit(1).execute()
print(f'Total records: {result.count if hasattr(result, \"count\") else 0}')
"

# Check source distribution
python -c "
from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
result = supabase.table('gematria_words').select('source', count='exact').execute()
sources = {}
for r in result.data:
    source = r.get('source', 'unknown')
    sources[source] = sources.get(source, 0) + 1
print('Records by source:')
for k, v in sorted(sources.items()):
    print(f'  - {k}: {v:,}')
"
```

### Checkpoints
- Checkpoint files: `*.checkpoint`
- Resume capability: Yes
- Checkpoint interval: 50,000 rows

---

## ⚙️ Configuration

### Processing Settings
- **Chunk Size:** 10,000 rows per chunk
- **Checkpoint Interval:** 50,000 rows
- **Validation:** Enabled (against calculation engine)
- **Batch Insertion:** Enabled
- **Progress Tracking:** Enabled (tqdm progress bars)

### Source Tagging
- **purchased-gematrix789.csv** → `purchased-gematrix789`
- **purchased-gimatria789.csv** → `purchased-gimatria789`

---

## 📝 Notes

### Time Estimates
- **purchased-gematrix789.csv:** ~8.2M rows - Estimated time: Several hours
- **purchased-gimatria789.csv:** ~659K rows - Estimated time: ~30-60 minutes
- **Total:** ~8.9M rows - Estimated time: Several hours

### Resuming
If interrupted, the pipeline will resume from the last checkpoint:
```bash
# Resume from checkpoint
python run_ingestion_pipeline.py --csv-only
```

### Monitoring
- **Log File:** `ingestion_full_run.log`
- **Pipeline Log:** `ingestion_pipeline.log`
- **Results:** `ingestion_pipeline_results_*.json`

---

## ✅ Status: RUNNING

The full ingestion is in progress. Monitor the logs for progress updates.

**Last Updated:** January 6, 2025  
**Status:** 🚀 **RUNNING**

