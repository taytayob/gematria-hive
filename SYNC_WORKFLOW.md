# Complete Sync Workflow - Replit & CLI/Cursor

**Purpose:** Maintain perfect sync between Replit and CLI/Cursor for all operations

**Last Updated:** November 6, 2025

---

## 🔄 Complete Sync Workflow

### Initial Setup (Both Platforms)

#### Replit

**Step 1: Clone Repository**
```bash
# In Replit Shell (if not already cloned)
git clone https://github.com/taytayob13/gematria-hive.git
cd gematria-hive
```

**Step 2: Verify Python Version**
```bash
# In Replit Shell
python3.12 --version  # Should show 3.12.x
```

**Step 3: Install Dependencies**
```bash
# In Replit Shell
pip install -r requirements.txt
```

**Step 4: Verify Installation**
```bash
# In Replit Shell
pip list | grep -E "streamlit|pandas|python-dotenv"
python -c "import streamlit, pandas, dotenv; print('✅ All packages installed')"
```

**Step 5: Run App**
- Click **Run** button in Replit
- App opens on port 5000 automatically

#### CLI/Cursor

**Step 1: Clone Repository**
```bash
# In Cursor/CLI terminal
cd ~/projects  # or your preferred location
git clone https://github.com/taytayob13/gematria-hive.git
cd gematria-hive
```

**Step 2: Create Environment (Choose ONE option)**

**Option A: Conda (Recommended for data science)**
```bash
# In Cursor/CLI terminal
conda create -n gematria-hive python=3.12 -y
conda activate gematria-hive
```

**Option B: venv (Standard Python)**
```bash
# In Cursor/CLI terminal
python3.12 -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# OR Activate (Windows)
venv\Scripts\activate
```

**Step 3: Verify Environment Active**
```bash
# Should show your environment's python
which python
python --version  # Should show Python 3.12.x
```

**Step 4: Install Dependencies**
```bash
# In Cursor/CLI terminal (with conda OR venv activated)
pip install -r requirements.txt

# For full package set (all 221 packages):
# pip install -r requirements-full.txt
```

**Step 5: Verify Installation**
```bash
# In Cursor/CLI terminal (with venv activated)
pip list | grep -E "streamlit|pandas|python-dotenv"
python -c "import streamlit, pandas, dotenv; print('✅ All packages installed')"
```

**Step 6: Configure Cursor Python Interpreter**
1. Press `Cmd/Ctrl+Shift+P`
2. Type: `Python: Select Interpreter`
3. Choose: `./venv/bin/python`

**Step 7: Run App**
```bash
# In Cursor/CLI terminal (with venv activated)
streamlit run app.py
```

---

## 📝 Daily Workflow (Side-by-Side)

### Starting Your Work Day

#### Replit

**Step 1: Pull Latest Changes**
```bash
# In Replit Shell
git pull origin main
```

**Step 2: Verify App Runs**
- Click **Run** button
- Verify app loads correctly

**Step 3: Start Coding**
- Make changes in Replit editor
- Test with Run button

#### CLI/Cursor

**Step 1: Navigate to Project**
```bash
# In Cursor/CLI terminal
cd /Users/cooperladd/Desktop/gematria-hive/gematria-hive
```

**Step 2: Activate Environment**
```bash
# In Cursor/CLI terminal (conda)
conda activate gematria-hive

# OR (venv Mac/Linux)
source venv/bin/activate

# OR (venv Windows)
venv\Scripts\activate
```

**Step 3: Pull Latest Changes**
```bash
# In Cursor/CLI terminal (with venv activated)
git pull origin main
```

**Step 4: Verify App Runs**
```bash
# In Cursor/CLI terminal (with venv activated)
streamlit run app.py
```

**Step 5: Start Coding**
- Make changes in Cursor
- Test locally with Streamlit running

---

## 💾 Committing Changes (Side-by-Side)

### Replit

**Step 1: Check Status**
```bash
# In Replit Shell
git status
```

**Step 2: Stage Changes**
```bash
# In Replit Shell
git add .
# OR specific files
git add app.py requirements.txt
```

**Step 3: Commit Changes**
```bash
# In Replit Shell
git commit -m "Your descriptive commit message"
```

**Step 4: Push to GitHub**
```bash
# In Replit Shell
git push origin main
```

**Complete One-Liner:**
```bash
# In Replit Shell
git add . && git commit -m "Your message" && git push origin main
```

### CLI/Cursor

**Step 1: Check Status**
```bash
# In Cursor/CLI terminal
git status
```

**Step 2: Stage Changes**
```bash
# In Cursor/CLI terminal
git add .
# OR specific files
git add app.py requirements.txt
```

**Step 3: Commit Changes**
```bash
# In Cursor/CLI terminal
git commit -m "Your descriptive commit message"
```

**Step 4: Push to GitHub**
```bash
# In Cursor/CLI terminal
git push origin main
```

**Complete One-Liner:**
```bash
# In Cursor/CLI terminal
git add . && git commit -m "Your message" && git push origin main
```

---

## 🔄 Syncing Between Platforms

### After Working in Replit

**In Replit:**
```bash
# In Replit Shell
git add .
git commit -m "Changes made in Replit"
git push origin main
```

**Then in CLI/Cursor:**
```bash
# In Cursor/CLI terminal
cd /Users/cooperladd/Desktop/gematria-hive/gematria-hive
source venv/bin/activate
git pull origin main
```

### After Working in CLI/Cursor

**In CLI/Cursor:**
```bash
# In Cursor/CLI terminal
cd /Users/cooperladd/Desktop/gematria-hive/gematria-hive
source venv/bin/activate
git add .
git commit -m "Changes made in Cursor"
git push origin main
```

**Then in Replit:**
```bash
# In Replit Shell
git pull origin main
# Replit auto-redeploys
```

---

## 📦 Adding New Dependencies (Side-by-Side)

### Replit

**Step 1: Install Package**
```bash
# In Replit Shell
pip install package-name
```

**Step 2: Update requirements.txt**
```bash
# In Replit Shell
pip freeze > requirements.txt
```

**Step 3: Commit Changes**
```bash
# In Replit Shell
git add requirements.txt
git commit -m "Add package-name dependency"
git push origin main
```

### CLI/Cursor

**Step 1: Activate Venv**
```bash
# In Cursor/CLI terminal
cd /Users/cooperladd/Desktop/gematria-hive/gematria-hive
source venv/bin/activate
```

**Step 2: Install Package**
```bash
# In Cursor/CLI terminal (with venv activated)
pip install package-name
```

**Step 3: Update requirements.txt**
```bash
# In Cursor/CLI terminal (with venv activated)
pip freeze > requirements.txt
```

**Step 4: Commit Changes**
```bash
# In Cursor/CLI terminal
git add requirements.txt
git commit -m "Add package-name dependency"
git push origin main
```

**Step 5: Sync to Replit**
```bash
# In Replit Shell
git pull origin main
pip install -r requirements.txt
```

---

## 🛠️ Troubleshooting Sync Issues

### Issue: Merge Conflicts

**Both Platforms:**
```bash
# Check what's different
git status
git diff

# If conflicts exist, resolve them:
# 1. Open conflicted files
# 2. Resolve conflicts manually
# 3. Stage resolved files
git add .
git commit -m "Resolve merge conflicts"
git push origin main
```

### Issue: Out of Sync

**Replit:**
```bash
# In Replit Shell
git fetch origin
git status
# If behind, pull
git pull origin main
```

**CLI/Cursor:**
```bash
# In Cursor/CLI terminal
git fetch origin
git status
# If behind, pull
git pull origin main
```

### Issue: Local Changes Conflict

**Both Platforms:**
```bash
# Stash local changes
git stash

# Pull latest
git pull origin main

# Reapply stashed changes
git stash pop

# Resolve any conflicts, then commit
git add .
git commit -m "Merge stashed changes"
git push origin main
```

---

## ✅ Verification Checklist

### Before Starting Work

**Replit:**
- [ ] `git pull origin main` - Latest changes pulled
- [ ] `git status` - Working tree clean
- [ ] Run button works - App starts correctly

**CLI/Cursor:**
- [ ] `cd` to project directory
- [ ] `source venv/bin/activate` - Venv activated
- [ ] `git pull origin main` - Latest changes pulled
- [ ] `git status` - Working tree clean
- [ ] `streamlit run app.py` - App starts correctly

### Before Committing

**Both Platforms:**
- [ ] `git status` - See what changed
- [ ] Test app - Everything works
- [ ] `git diff` - Review changes (optional)

### After Committing

**Both Platforms:**
- [ ] `git push origin main` - Changes pushed
- [ ] `git log -1` - Verify commit
- [ ] Pull on other platform - Verify sync

---

## 🎯 Best Practices

### Always Do This

1. **Pull before starting work** - Both platforms
2. **Test before committing** - Both platforms
3. **Commit frequently** - Small, logical commits
4. **Push after committing** - Keep remote in sync
5. **Pull after pushing** - Sync other platform

### Never Do This

1. ❌ Work without pulling latest changes
2. ❌ Commit without testing
3. ❌ Push without committing
4. ❌ Work on both platforms without syncing
5. ❌ Force push to main branch

---

## 📚 Related Documentation

- **CURSOR_SYNC_INSTRUCTIONS.md** - Detailed setup guide
- **CURSOR_STREAMLIT_SETUP.md** - Streamlit-specific guide
- **GIT_COMMIT_INSTRUCTIONS.md** - Git workflow details
- **README.md** - Project overview

---

**Keep both platforms in perfect sync!** 🔄✨

