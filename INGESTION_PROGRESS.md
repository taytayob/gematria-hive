# Full Ingestion Progress

**Date:** January 6, 2025  
**Status:** 🚀 **RUNNING**  
**Started:** 14:51:03

---

## ✅ Ingestion Started Successfully

### Current Status
- **File:** `purchased-gematrix789.csv` (first file, priority)
- **Total Rows:** 8,229,245
- **Progress:** Processing in chunks of 10,000 rows
- **Checkpoint Interval:** 50,000 rows
- **Processing Speed:** ~3,000-3,500 rows/second

### Progress Updates
- ✅ **50,000 rows processed** - First checkpoint saved
- ✅ **Source tagging:** `purchased-gematrix789` ✓
- ✅ **Validation:** Enabled ✓
- ✅ **Database insertion:** Working ✓

---

## 📊 Monitoring Commands

### Check Progress
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
print(f'Total records: {result.count if hasattr(result, \"count\") else 0:,}')
"
```

### Check Source Distribution
```bash
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

---

## ⏱️ Time Estimates

### purchased-gematrix789.csv
- **Total Rows:** 8,229,245
- **Processing Speed:** ~3,000-3,500 rows/second
- **Estimated Time:** ~40-45 minutes

### purchased-gimatria789.csv
- **Total Rows:** 659,635
- **Processing Speed:** ~3,000-3,500 rows/second
- **Estimated Time:** ~3-4 minutes

### Total
- **Total Rows:** ~8.9M
- **Estimated Total Time:** ~45-50 minutes

---

## 🔄 Resuming

If interrupted, the pipeline will automatically resume from the last checkpoint:
```bash
# Resume from checkpoint
python run_ingestion_pipeline.py --csv-only
```

Checkpoint files are saved as `*.checkpoint` in the project root.

---

## 📝 Notes

- **Background Process:** Ingestion is running in the background
- **Log Files:** `ingestion_full_run.log`, `ingestion_pipeline.log`
- **Checkpoints:** Saved every 50,000 rows
- **Validation:** Enabled against calculation engine
- **Source Tagging:** `purchased-gematrix789` and `purchased-gimatria789`

---

## ✅ Status: RUNNING

The full ingestion is in progress. Monitor the logs for real-time updates.

**Last Updated:** January 6, 2025  
**Status:** 🚀 **RUNNING**

