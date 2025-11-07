# Conda Environment Setup - Complete Guide

**Purpose:** Set up conda environment for Gematria Hive (alternative to venv)

**Last Updated:** November 6, 2025

---

## 🚀 Quick Start

### Option 1: Use Existing Environment (if you have `gematria_env`)

```bash
# Activate existing environment
conda activate gematria_env

# Install/update dependencies
pip install -r requirements.txt
```

### Option 2: Create New Environment from environment.yml

```bash
# Create environment from environment.yml
conda env create -f environment.yml

# Activate environment
conda activate gematria-hive
```

### Install Dependencies

```bash
# With conda environment activated
pip install -r requirements.txt
```

---

## 📋 Setup (Replit & CLI/Cursor)

### Replit

**Note:** Replit typically uses pip directly, but you can use conda if available.

**Step 1: Check if Conda is Available**

```bash
# In Replit Shell
conda --version
```

**Step 2: Create Environment (if conda available)**

```bash
# In Replit Shell
conda env create -f environment.yml
conda activate gematria-hive
```

**Step 3: Install Dependencies**

```bash
# In Replit Shell (with conda env activated)
pip install -r requirements.txt
```

**Alternative (if conda not available):**
- Use pip directly: `pip install -r requirements.txt`
- Replit handles Python version via `.replit` config

### CLI/Cursor

**Step 1: Create Conda Environment**

```bash
# In Cursor/CLI terminal
cd /Users/cooperladd/Desktop/gematria-hive/gematria-hive
conda env create -f environment.yml
```

**Step 2: Activate Environment**

```bash
# In Cursor/CLI terminal
conda activate gematria-hive
```

**Step 3: Install Dependencies**

```bash
# In Cursor/CLI terminal (with conda env activated)
pip install -r requirements.txt
```

**Step 4: Configure Cursor Python Interpreter**

1. Press `Cmd/Ctrl+Shift+P`
2. Type: `Python: Select Interpreter`
3. Choose conda environment:
   - macOS/Linux: `~/anaconda3/envs/gematria-hive/bin/python` (or your conda path)
   - Or: `which python` (after activating conda env)

---

## 🔄 Daily Workflow

### Activate Environment

**CLI/Cursor:**
```bash
# Activate conda environment
conda activate gematria-hive

# Verify
python --version  # Should show 3.12.x
which python     # Should show conda env path
```

### Run Streamlit

**CLI/Cursor:**
```bash
# With conda env activated
streamlit run app.py
```

### Run Ingestion

**CLI/Cursor:**
```bash
# With conda env activated
python ingest_pass1.py
```

---

## 📦 Update Environment

### Add New Package

**CLI/Cursor:**
```bash
# With conda env activated
pip install new-package
pip freeze > requirements.txt  # Update requirements
```

### Update Environment File

**CLI/Cursor:**
```bash
# Export current environment
conda env export > environment.yml

# Or export without build info (cleaner)
conda env export --no-builds > environment.yml
```

### Update All Packages

**CLI/Cursor:**
```bash
# With conda env activated
pip install --upgrade -r requirements.txt
```

---

## 🔄 Sync Between Platforms

### Replit → CLI/Cursor

**In Replit:**
```bash
# Commit changes
git add requirements.txt environment.yml
git commit -m "Update dependencies"
git push origin main
```

**In CLI/Cursor:**
```bash
# Pull latest
git pull origin main

# Update conda environment
conda env update -f environment.yml --prune
# OR
pip install -r requirements.txt
```

### CLI/Cursor → Replit

**In CLI/Cursor:**
```bash
# Commit changes
git add requirements.txt environment.yml
git commit -m "Update dependencies"
git push origin main
```

**In Replit:**
```bash
# Pull latest
git pull origin main

# Update packages
pip install -r requirements.txt
```

---

## 🛠️ Troubleshooting

### Issue: "Conda command not found"

**Solution:**
```bash
# Initialize conda for your shell
conda init zsh  # For zsh
conda init bash # For bash

# Restart terminal or run:
source ~/.zshrc  # or ~/.bashrc
```

### Issue: "Environment already exists"

**Solution:**
```bash
# Remove existing environment
conda env remove -n gematria-hive

# Create fresh
conda env create -f environment.yml
```

### Issue: "Package conflicts"

**Solution:**
```bash
# Update conda
conda update conda

# Create environment with specific channel priority
conda env create -f environment.yml --force
```

### Issue: Cursor not using conda Python

**Solution:**
1. Activate conda env: `conda activate gematria-hive`
2. Find Python path: `which python`
3. In Cursor: `Cmd/Ctrl+Shift+P` → `Python: Select Interpreter`
4. Choose the conda Python path

---

## 📝 Environment Management

### List Environments

```bash
conda env list
```

### Activate Environment

```bash
conda activate gematria-hive
```

### Deactivate Environment

```bash
conda deactivate
```

### Remove Environment

```bash
conda env remove -n gematria-hive
```

### Export Environment

```bash
# Export with build info
conda env export > environment.yml

# Export without build info (cleaner, cross-platform)
conda env export --no-builds > environment.yml

# Export only pip packages
conda env export --from-history > environment.yml
```

---

## ✅ Verification

### Check Environment

```bash
# List environments
conda env list

# Check active environment
conda info --envs

# Verify Python version
python --version  # Should show 3.12.x

# Verify packages
pip list | grep -E "streamlit|pandas|supabase"
```

### Test Imports

```bash
# With conda env activated
python -c "import streamlit, pandas, supabase, sentence_transformers; print('✅ All packages installed')"
```

---

## 🎯 Quick Reference

| Action | Command |
|--------|---------|
| **Create environment** | `conda env create -f environment.yml` |
| **Activate** | `conda activate gematria-hive` |
| **Deactivate** | `conda deactivate` |
| **Install deps** | `pip install -r requirements.txt` |
| **Update environment** | `conda env update -f environment.yml --prune` |
| **Export environment** | `conda env export --no-builds > environment.yml` |
| **Remove environment** | `conda env remove -n gematria-hive` |
| **List environments** | `conda env list` |

---

## 📚 Related Documentation

- **CURSOR_SYNC_INSTRUCTIONS.md** - Setup and sync guide
- **CURSOR_STREAMLIT_SETUP.md** - Streamlit setup
- **SYNC_WORKFLOW.md** - Complete workflow guide
- **INGESTION_GUIDE.md** - Ingestion guide
- **SUPABASE_SETUP.md** - Database setup

---

## 💡 Conda vs Venv

### Use Conda When:
- ✅ You need system-level packages (C libraries, etc.)
- ✅ You want better dependency resolution
- ✅ You're working with data science packages
- ✅ You need multiple Python versions

### Use Venv When:
- ✅ You want lightweight virtual environments
- ✅ You're only using Python packages
- ✅ You want simpler setup
- ✅ You're deploying to environments without conda

**For Gematria Hive:** Conda is recommended for better package management, especially with ML/data science dependencies.

---

**Conda environment ready!** 🐝✨

