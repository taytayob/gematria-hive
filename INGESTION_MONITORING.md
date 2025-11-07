# Ingestion Monitoring Guide

**Date:** January 6, 2025  
**Status:** 🚀 **RUNNING**

---

## 📊 Quick Status Check

### Check Database Count
```bash
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

### View Live Progress
```bash
# View last 50 lines
tail -50 ingestion_full_run.log

# Follow live updates
tail -f ingestion_full_run.log

# Check for errors
grep -i error ingestion_full_run.log | tail -10
```

### Check Process Status
```bash
# Check if ingestion is still running
ps aux | grep "python run_ingestion_pipeline.py" | grep -v grep

# Check checkpoint files
ls -lh *.checkpoint
```

---

## 📈 Progress Tracking

### Expected Progress
- **purchased-gematrix789.csv:** 8,229,245 rows
- **purchased-gimatria789.csv:** 659,635 rows
- **Total:** ~8.9M rows

### Processing Speed
- **Average:** ~3,000-3,500 rows/second
- **Estimated Time:** ~40-50 minutes total

### Checkpoints
- **Interval:** Every 50,000 rows
- **Location:** `*.checkpoint` files in project root
- **Resume:** Automatically resumes from last checkpoint if interrupted

---

## 🔍 Troubleshooting

### If Ingestion Stops
1. **Check logs:** `tail -100 ingestion_full_run.log`
2. **Check errors:** `grep -i error ingestion_full_run.log`
3. **Resume:** `python run_ingestion_pipeline.py --csv-only`

### If Database Connection Issues
1. **Check credentials:** `.env` file
2. **Test connection:** `python setup_database.py --verify-only`
3. **Check Supabase dashboard:** https://supabase.com/dashboard

### If Slow Processing
- **Normal:** Large files take time
- **Check network:** Database connection speed
- **Check resources:** System CPU/memory usage

---

## ✅ Completion Indicators

### When Complete
- Log shows: `✅ PIPELINE COMPLETE!`
- Database count: ~8.9M records
- Source distribution shows:
  - `purchased-gematrix789`: ~8.2M records
  - `purchased-gimatria789`: ~659K records

### Verify Completion
```bash
# Check final count
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

---

## 📝 Notes

- **Background Process:** Ingestion runs in background
- **Log Files:** `ingestion_full_run.log`, `ingestion_pipeline.log`
- **Results:** `ingestion_pipeline_results_*.json`
- **Checkpoints:** `*.checkpoint` files

---

**Last Updated:** January 6, 2025  
**Status:** 🚀 **RUNNING**

