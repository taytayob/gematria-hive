# Conda Setup - All Platforms (Replit, CLI, Cursor)

**Purpose:** Complete conda environment setup for Replit, CLI, and Cursor

**Last Updated:** November 6, 2025

---

## ✅ Current Status

- ✅ **CLI:** Conda environment `gematria_env` created and packages installed
- ⚠️ **Replit:** May not have conda yet (check and set up)
- ⚠️ **Cursor:** May need interpreter configuration

---

## 🚀 Setup Instructions by Platform

### CLI (Already Complete ✅)

**Your conda environment is ready!**

```bash
# Activate conda environment
conda activate gematria_env

# Verify installation
python -c "import streamlit, pandas, supabase, sentence_transformers; print('✅ All packages installed')"

# Run Streamlit
streamlit run app.py
```

**Python Interpreter Path:**
```
/Users/cooperladd/anaconda3/envs/gematria_env/bin/python
```

---

### Replit

**Step 1: Check if Conda is Available**

```bash
# In Replit Shell
conda --version
```

**If conda is NOT available:**

**Option A: Use pip (Recommended for Replit)**
```bash
# In Replit Shell
pip install -r requirements.txt
```

**Option B: Install Conda in Replit (if needed)**
```bash
# In Replit Shell
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
export PATH="$HOME/miniconda3/bin:$PATH"
conda init bash
source ~/.bashrc
```

**If conda IS available:**

**Step 2: Create Conda Environment**

```bash
# In Replit Shell
conda env create -f environment.yml

# Activate environment
conda activate gematria-hive

# OR use existing gematria_env if it exists
conda activate gematria_env
```

**Step 3: Install Dependencies**

```bash
# In Replit Shell (with conda env activated)
pip install -r requirements.txt
```

**Step 4: Verify Installation**

```bash
# In Replit Shell (with conda env activated)
python -c "import streamlit, pandas, supabase, sentence_transformers; print('✅ All packages installed')"
```

**Step 5: Update .replit for Conda (Optional)**

Edit `.replit` file:
```toml
run = "conda activate gematria_env && streamlit run app.py --server.port 5000"

[env]
PYTHON_VERSION = "3.12"
CONDA_ENV = "gematria_env"
```

---

### Cursor

**Step 1: Configure Python Interpreter**

1. **Press:** `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. **Type:** `Python: Select Interpreter`
3. **Choose:** `/Users/cooperladd/anaconda3/envs/gematria_env/bin/python`

**OR manually edit `.vscode/settings.json`:**

```json
{
  "python.defaultInterpreterPath": "/Users/cooperladd/anaconda3/envs/gematria_env/bin/python",
  "python.terminal.activateEnvironment": true,
  "python.terminal.activateEnvInCurrentTerminal": true
}
```

**Step 2: Activate Conda in Terminal**

```bash
# In Cursor terminal
conda activate gematria_env

# Verify
python --version  # Should show 3.12.12
which python     # Should show conda path
```

**Step 3: Verify Installation**

```bash
# In Cursor terminal (with conda env activated)
python -c "import streamlit, pandas, supabase, sentence_transformers; print('✅ All packages installed')"
```

**Step 4: Run Streamlit**

```bash
# In Cursor terminal (with conda env activated)
streamlit run app.py
```

**If Cursor is stuck:**

1. **Restart Cursor** completely
2. **Close and reopen** the project
3. **Check Python interpreter** is set correctly
4. **Verify conda is in PATH:**
   ```bash
   which conda
   echo $PATH | grep conda
   ```

---

## 📝 Git Commands for All Platforms

### Commit Conda Setup

**In CLI (where you are now):**

```bash
# Stage all changes
git add .

# Commit conda setup
git commit -m "Add conda environment setup and configuration

- Created environment.yml for conda environment
- Added CONDA_SETUP.md with platform-specific instructions
- Updated documentation for conda usage
- All dependencies installed in gematria_env conda environment
- Python 3.12.12 with all required packages verified"

# Push to GitHub
git push origin main
```

**In Replit (after setup):**

```bash
# In Replit Shell
git pull origin main

# If you made changes in Replit:
git add .
git commit -m "Update Replit conda configuration"
git push origin main
```

**In Cursor (after fixing interpreter):**

```bash
# In Cursor terminal
git pull origin main

# If you made changes in Cursor:
git add .
git commit -m "Configure Cursor to use conda gematria_env interpreter"
git push origin main
```

---

## 🔄 Sync Workflow

### Daily Workflow

**CLI:**
```bash
conda activate gematria_env
# Work on code
git add .
git commit -m "Your message"
git push origin main
```

**Replit:**
```bash
# Pull latest
git pull origin main

# Work on code
# Commit and push
git add .
git commit -m "Your message"
git push origin main
```

**Cursor:**
```bash
# Activate conda
conda activate gematria_env

# Pull latest
git pull origin main

# Work on code
# Commit and push
git add .
git commit -m "Your message"
git push origin main
```

---

## ✅ Verification Checklist

### CLI
- [x] Conda environment `gematria_env` created
- [x] All packages installed
- [x] Python 3.12.12 verified
- [ ] Git commit and push completed

### Replit
- [ ] Conda available or using pip
- [ ] Dependencies installed
- [ ] Python interpreter configured
- [ ] Streamlit runs successfully

### Cursor
- [ ] Python interpreter set to conda path
- [ ] Conda environment activates in terminal
- [ ] All packages importable
- [ ] Streamlit runs successfully

---

## 🛠️ Troubleshooting

### Cursor Stuck/Not Using Conda

**Solution 1: Restart Cursor**
```bash
# Quit Cursor completely
# Reopen project
# Set interpreter again
```

**Solution 2: Manual Settings**
Edit `.vscode/settings.json`:
```json
{
  "python.defaultInterpreterPath": "/Users/cooperladd/anaconda3/envs/gematria_env/bin/python"
}
```

**Solution 3: Terminal Activation**
```bash
# In Cursor terminal
conda activate gematria_env
export PATH="/Users/cooperladd/anaconda3/envs/gematria_env/bin:$PATH"
```

### Replit No Conda

**Use pip instead:**
```bash
# In Replit Shell
pip install -r requirements.txt
```

### Git Sync Issues

**Always pull first:**
```bash
git pull origin main --rebase
```

**Then commit:**
```bash
git add .
git commit -m "Your message"
git push origin main
```

---

## 📚 Related Documentation

- **CONDA_SETUP.md** - Detailed conda guide
- **CURSOR_SYNC_INSTRUCTIONS.md** - Cursor setup
- **SYNC_WORKFLOW.md** - Complete workflow
- **environment.yml** - Conda environment file

---

**Ready to commit and sync!** 🐝✨

