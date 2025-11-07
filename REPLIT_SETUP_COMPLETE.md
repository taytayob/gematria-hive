# Replit Setup - Complete Guide

**Purpose:** Step-by-step setup for Replit to sync with CLI and Cursor

**Last Updated:** November 6, 2025

---

## 🚀 Quick Start

### Step 1: Pull Latest Changes

**In Replit Shell:**

```bash
# Navigate to project directory (if not already there)
cd ~/workspace

# Pull latest changes from GitHub
git pull origin feat-agent-framework-9391b --rebase

# Verify you're on the right branch
git branch --show-current
```

**Expected Output:**
```
Updating...
Already up to date.
feat-agent-framework-9391b
```

---

### Step 2: Check Python Version

**In Replit Shell:**

```bash
# Check Python version
python3.12 --version

# If Python 3.12 not available, check what's available
python3 --version
python --version
```

**Expected:** Python 3.12.x (or at least 3.11+)

---

### Step 3: Install Dependencies

**Option A: Using pip (Recommended for Replit)**

```bash
# Install all dependencies
pip install -r requirements.txt

# Verify installation
python -c "import streamlit, pandas, supabase, sentence_transformers; print('✅ All packages installed')"
```

**Option B: Using conda (if available)**

```bash
# Check if conda is available
conda --version

# If available, create environment
conda env create -f environment.yml
conda activate gematria-hive

# Install dependencies
pip install -r requirements.txt

# Verify
python -c "import streamlit, pandas, supabase, sentence_transformers; print('✅ All packages installed')"
```

---

### Step 4: Configure Environment Variables

**Edit `.replit` file:**

```toml
run = "streamlit run app.py --server.port 5000 --server.address 0.0.0.0"

[env]
PYTHON_VERSION = "3.12"
SUPABASE_URL = "your_supabase_url_here"
SUPABASE_KEY = "your_anon_key_here"

[packager]
language = "python3"

[packager.features]
enabledForHosting = false
packageSearch = true
guessImports = true
```

**OR use Replit Secrets (Recommended):**

1. Click **lock icon** in Replit sidebar
2. Add secrets:
   - `SUPABASE_URL` = `https://your-project.supabase.co`
   - `SUPABASE_KEY` = `your-anon-key-here`

---

### Step 5: Test Streamlit

**In Replit Shell:**

```bash
# Run Streamlit
streamlit run app.py --server.port 5000 --server.address 0.0.0.0

# OR use the Run button (uses .replit config)
```

**Expected:**
- Streamlit starts successfully
- App accessible in Replit webview
- Port 5000 configured correctly

---

### Step 6: Verify Setup

**In Replit Shell:**

```bash
# Check Python version
python --version

# Check packages
python -c "
import streamlit
import pandas
import supabase
import sentence_transformers
print('✅ All core packages installed')
print('Streamlit:', streamlit.__version__)
print('Pandas:', pandas.__version__)
"

# Check environment variables (if set)
python -c "
import os
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
if url:
    print('✅ SUPABASE_URL set')
else:
    print('⚠️  SUPABASE_URL not set')
if key:
    print('✅ SUPABASE_KEY set')
else:
    print('⚠️  SUPABASE_KEY not set')
"
```

---

## 🔄 Sync Workflow

### Daily Workflow

**Starting Work in Replit:**

```bash
# Pull latest changes
git pull origin feat-agent-framework-9391b --rebase

# Verify setup
python -c "import streamlit, pandas, supabase; print('✅ Ready')"
```

**Making Changes:**

```bash
# Edit files in Replit...

# Stage changes
git add .

# Commit
git commit -m "Your descriptive message"

# Push
git push origin feat-agent-framework-9391b
```

**After Changes in CLI/Cursor:**

```bash
# Pull latest from CLI/Cursor
git pull origin feat-agent-framework-9391b --rebase

# App auto-redeploys (if using Run button)
```

---

## 🛠️ Troubleshooting

### Issue: "Python 3.12 not found"

**Solution:**
```bash
# Check available Python versions
ls /usr/bin/python*

# Use available version (3.11+ should work)
python3 --version

# Update .replit if needed
# PYTHON_VERSION = "3.11"  # or available version
```

### Issue: "Package installation fails"

**Solution:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Install packages one by one if needed
pip install streamlit
pip install pandas
pip install supabase
# etc.

# Or install from requirements.txt
pip install -r requirements.txt --no-cache-dir
```

### Issue: "Streamlit port already in use"

**Solution:**
```bash
# Kill existing Streamlit process
pkill -f streamlit

# Or use different port
streamlit run app.py --server.port 5001
```

### Issue: "Git pull fails"

**Solution:**
```bash
# Stash local changes
git stash

# Pull with rebase
git pull origin feat-agent-framework-9391b --rebase

# Reapply changes
git stash pop
```

### Issue: "Environment variables not loading"

**Solution:**
```bash
# Check .replit file has [env] section
cat .replit

# Or use Replit Secrets (lock icon in sidebar)
# Then access via os.getenv() in code
```

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Git pulls latest changes successfully
- [ ] Python 3.12 (or 3.11+) available
- [ ] All packages install without errors
- [ ] Streamlit runs on port 5000
- [ ] App accessible in Replit webview
- [ ] Environment variables set (if using Supabase)
- [ ] Git commits and pushes work
- [ ] Changes sync with CLI/Cursor

---

## 📝 Quick Reference

### Essential Commands

```bash
# Pull latest
git pull origin feat-agent-framework-9391b --rebase

# Install dependencies
pip install -r requirements.txt

# Run Streamlit
streamlit run app.py --server.port 5000

# Verify packages
python -c "import streamlit, pandas, supabase; print('✅ Ready')"

# Commit changes
git add .
git commit -m "Your message"
git push origin feat-agent-framework-9391b
```

### File Locations

- **Project root:** `~/workspace` or `/home/runner/workspace`
- **Config file:** `.replit`
- **Requirements:** `requirements.txt`
- **Environment:** `environment.yml` (if using conda)

---

## 🔗 Related Documentation

- **NEXT_STEPS.md** - Overall next steps guide
- **CONDA_SETUP_ALL_PLATFORMS.md** - Conda setup (if using conda)
- **GIT_COMMIT_COMMANDS.md** - Git workflow reference
- **SUPABASE_SETUP.md** - Database setup (after Replit is ready)

---

## 🎯 Next Steps After Replit Setup

1. **Test Streamlit App**
   - Run app in Replit
   - Verify all features work
   - Test port 5000 configuration

2. **Set Up Supabase**
   - Follow `SUPABASE_SETUP.md`
   - Add environment variables to Replit
   - Test database connection

3. **Test Ingestion**
   - Run `ingest_pass1.py` with test data
   - Verify Supabase integration
   - Check logs

---

**Replit setup complete! Ready for development!** 🐝✨

