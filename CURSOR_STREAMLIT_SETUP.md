# Running Streamlit - Complete Guide (Replit & CLI/Cursor)

**Purpose:** Run Streamlit app on both Replit and CLI/Cursor with full sync

**Last Updated:** November 6, 2025

---

## 🚀 Quick Start (Both Platforms)

### Replit
1. Click **Run** button (uses `.replit` config automatically)
2. App opens on port 5000 in webview

### CLI/Cursor
```bash
source venv/bin/activate
streamlit run app.py
```
App opens on `http://localhost:5000`

---

## ✅ Method 1: Run Streamlit (Side-by-Side)

### Replit

**Using Run Button:**
1. Click the **Run** button in Replit
2. Streamlit starts automatically on port 5000
3. App opens in webview

**Using Shell:**
```bash
# In Replit Shell
streamlit run app.py --server.port 5000 --server.address 0.0.0.0
```

**Manual Steps:**
1. Open Replit Shell
2. Run: `streamlit run app.py`
3. App will use port 5000 from `.replit` config

### CLI/Cursor

**Using Cursor Tasks (Recommended):**
1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type: `Tasks: Run Task`
3. Select: `Run Streamlit App`
4. Streamlit starts on port 5000

**Using Shell Script:**
```bash
# In Cursor/CLI terminal
./run_streamlit.sh
```

**Manual Command:**
```bash
# In Cursor/CLI terminal
source venv/bin/activate
streamlit run app.py
```

**Direct Path (No Activation):**
```bash
venv/bin/streamlit run app.py
```

---

## 🔧 Setup Python Environment (Side-by-Side)

### Replit

**Automatic (Recommended):**
- Replit uses Python 3.12 from `.replit` config automatically
- Dependencies install from `requirements.txt` on first run

**Manual Setup:**
```bash
# In Replit Shell
python3.12 --version  # Verify Python version
pip install -r requirements.txt
```

**Verify Installation:**
```bash
# In Replit Shell
pip list | grep streamlit
python -c "import streamlit; print(streamlit.__version__)"
```

### CLI/Cursor

**Initial Setup:**
```bash
# In Cursor/CLI terminal
cd /Users/cooperladd/Desktop/gematria-hive/gematria-hive
python3.12 -m venv venv
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**Verify Installation:**
```bash
# In Cursor/CLI terminal
source venv/bin/activate
pip list | grep streamlit
python -c "import streamlit; print(streamlit.__version__)"
```

**Configure Cursor Python Interpreter:**
1. Press `Cmd/Ctrl+Shift+P`
2. Type: `Python: Select Interpreter`
3. Choose: `./venv/bin/python`

---

## 📦 Install/Update Dependencies (Side-by-Side)

### Replit

**Install New Package:**
```bash
# In Replit Shell
pip install package-name
pip freeze > requirements.txt  # Update requirements
```

**Update All Packages:**
```bash
# In Replit Shell
pip install --upgrade -r requirements.txt
```

**Manual Steps:**
1. Open Replit Shell
2. Run: `pip install package-name`
3. Update `requirements.txt`: `pip freeze > requirements.txt`
4. Commit changes: `git add requirements.txt && git commit -m "Add package-name" && git push`

### CLI/Cursor

**Install New Package:**
```bash
# In Cursor/CLI terminal
source venv/bin/activate
pip install package-name
pip freeze > requirements.txt  # Update requirements
```

**Update All Packages:**
```bash
# In Cursor/CLI terminal
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

**Manual Steps:**
1. Open Cursor/CLI terminal
2. Activate venv: `source venv/bin/activate`
3. Install: `pip install package-name`
4. Update requirements: `pip freeze > requirements.txt`
5. Commit: `git add requirements.txt && git commit -m "Add package-name" && git push`

---

## 🔄 Sync Changes (Side-by-Side)

### Replit → CLI/Cursor

**In Replit:**
```bash
# After making changes in Replit
git add .
git commit -m "Your message"
git push origin main
```

**In CLI/Cursor:**
```bash
# Pull latest changes
git pull origin main
```

**Manual Steps:**
1. **Replit:** Make changes, commit, push
2. **CLI/Cursor:** Run `git pull origin main`
3. **CLI/Cursor:** Activate venv if needed: `source venv/bin/activate`

### CLI/Cursor → Replit

**In CLI/Cursor:**
```bash
# After making changes in Cursor/CLI
git add .
git commit -m "Your message"
git push origin main
```

**In Replit:**
```bash
# Pull latest changes
git pull origin main
# Replit auto-redeploys
```

**Manual Steps:**
1. **CLI/Cursor:** Make changes, commit, push
2. **Replit:** Run `git pull origin main` in Shell
3. **Replit:** Click Run button (or app auto-redeploys)

---

## 🛠️ Troubleshooting (Side-by-Side)

### Issue: "streamlit: command not found"

**Replit:**
```bash
# In Replit Shell
pip install streamlit
# Or reinstall from requirements
pip install -r requirements.txt
```

**CLI/Cursor:**
```bash
# In Cursor/CLI terminal
source venv/bin/activate
pip install streamlit
# Or reinstall from requirements
pip install -r requirements.txt
```

### Issue: "Port 5000 is already in use"

**Replit:**
```bash
# In Replit Shell
# Stop current process (click Stop button)
# Or kill process
pkill -f streamlit
```

**CLI/Cursor:**
```bash
# In Cursor/CLI terminal
lsof -ti :5000 | xargs kill -9
# Then run again
streamlit run app.py
```

### Issue: Wrong Python Version

**Replit:**
- Check `.replit` file has: `modules = ["python-3.12"]`
- Verify: `python3.12 --version` in Shell

**CLI/Cursor:**
```bash
# In Cursor/CLI terminal
python3.12 --version  # Should show 3.12.x
# If not, recreate venv:
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Dependencies Not Synced

**Replit:**
```bash
# In Replit Shell
pip install -r requirements.txt
# Verify
pip list
```

**CLI/Cursor:**
```bash
# In Cursor/CLI terminal
source venv/bin/activate
pip install -r requirements.txt
# Verify
pip list
```

---

## 📝 Daily Workflow (Side-by-Side)

### Replit Workflow

1. **Start Work:**
   ```bash
   # In Replit Shell
   git pull origin main
   ```

2. **Make Changes:**
   - Edit files in Replit editor
   - Test with Run button

3. **Commit & Push:**
   ```bash
   # In Replit Shell
   git add .
   git commit -m "Your message"
   git push origin main
   ```

### CLI/Cursor Workflow

1. **Start Work:**
   ```bash
   # In Cursor/CLI terminal
   cd /Users/cooperladd/Desktop/gematria-hive/gematria-hive
   source venv/bin/activate
   git pull origin main
   ```

2. **Make Changes:**
   - Edit files in Cursor
   - Test locally: `streamlit run app.py`

3. **Commit & Push:**
   ```bash
   # In Cursor/CLI terminal
   git add .
   git commit -m "Your message"
   git push origin main
   ```

---

## ✅ Verification Checklist

### Replit
- [ ] Python 3.12 is active (`python3.12 --version`)
- [ ] Streamlit installed (`pip list | grep streamlit`)
- [ ] App runs on port 5000 (Run button works)
- [ ] Changes sync to GitHub (`git status` shows clean)

### CLI/Cursor
- [ ] Python 3.12 venv created (`python --version` shows 3.12.x)
- [ ] Venv activated (see `(venv)` in prompt)
- [ ] Streamlit installed (`pip list | grep streamlit`)
- [ ] App runs on port 5000 (`streamlit run app.py`)
- [ ] Cursor using venv Python (check bottom-right corner)
- [ ] Changes sync to GitHub (`git status` shows clean)

---

## 🎯 Quick Reference Commands

| Action | Replit | CLI/Cursor |
|--------|--------|------------|
| **Run App** | Click Run button | `source venv/bin/activate && streamlit run app.py` |
| **Install Deps** | `pip install -r requirements.txt` | `source venv/bin/activate && pip install -r requirements.txt` |
| **Pull Changes** | `git pull origin main` | `git pull origin main` |
| **Push Changes** | `git add . && git commit -m "msg" && git push` | `git add . && git commit -m "msg" && git push` |
| **Check Status** | `git status` | `git status` |
| **Kill Port 5000** | Click Stop button | `lsof -ti :5000 \| xargs kill -9` |

---

**All methods are now configured and ready to use on both platforms!** 🎉
