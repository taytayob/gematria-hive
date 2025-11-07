# Quick Start Guide - Gematria Hive

**Purpose:** Fast setup for all platforms

**Last Updated:** November 6, 2025

---

## 🚀 5-Minute Setup

### CLI (Mac Terminal) - ✅ Already Complete

```bash
conda activate gematria_env
./verify_setup.sh
streamlit run app.py
```

---

### Cursor - ✅ Already Complete

```bash
# Terminal should auto-activate conda
conda activate gematria_env
streamlit run app.py
```

**If not working:**
1. `Cmd+Shift+P` → `Python: Select Interpreter`
2. Choose: `/Users/cooperladd/anaconda3/envs/gematria_env/bin/python`

---

### Replit - ⚠️ Do This Now

**In Replit Shell:**

```bash
# 1. Pull latest
git pull origin feat-agent-framework-9391b --rebase

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify
python -c "import streamlit, pandas, supabase; print('✅ Ready')"

# 4. Run (or click Run button)
streamlit run app.py --server.port 5000
```

**See `REPLIT_SETUP_COMPLETE.md` for detailed instructions.**

---

## 📋 Verification

**Run this on any platform:**

```bash
# CLI/Cursor
conda activate gematria_env
./verify_setup.sh

# Replit
python -c "import streamlit, pandas, supabase, sentence_transformers; print('✅ All packages installed')"
```

---

## 🔄 Daily Workflow

**All Platforms:**

```bash
# 1. Pull latest
git pull origin feat-agent-framework-9391b --rebase

# 2. Activate environment (CLI/Cursor)
conda activate gematria_env

# 3. Work on code...

# 4. Commit and push
git add .
git commit -m "Your message"
git push origin feat-agent-framework-9391b
```

---

## 🎯 Next Steps

1. **✅ CLI Setup** - Complete
2. **✅ Cursor Setup** - Complete
3. **⚠️ Replit Setup** - Do now (5 minutes)
4. **⚠️ Supabase Setup** - After Replit (15 minutes)
5. **⚠️ Test Ingestion** - After Supabase (10 minutes)

---

## 📚 Full Documentation

- **REPLIT_SETUP_COMPLETE.md** - Replit setup guide
- **NEXT_STEPS.md** - Complete next steps
- **SUPABASE_SETUP.md** - Database setup
- **GIT_COMMIT_COMMANDS.md** - Git workflow

---

**Ready to go!** 🐝✨

