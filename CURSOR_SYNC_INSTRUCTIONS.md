# Cursor IDE Sync Instructions

**Purpose:** Set up bidirectional sync between Replit and Cursor for hybrid development workflow.

**Last Updated:** November 6, 2025

---

## Prerequisites

✅ Git repository pushed to GitHub (complete `GIT_COMMIT_INSTRUCTIONS.md` first)  
✅ Cursor IDE installed on your local machine  
✅ GitHub account with SSH or HTTPS access configured  

---

## 📍 STEP 1: Clone Repository in Cursor

### A. Install Cursor (if you haven't):

Go to https://cursor.sh

Download and install for your OS (Mac/Windows/Linux)

### B. Clone Repository in Cursor:

**Option 1: Using Cursor UI**

1. Open Cursor → File → Clone Repository
2. Paste your GitHub URL: `https://github.com/taytayob13/gematria-hive.git`
3. Choose folder location
4. Click Clone

**Option 2: Using Terminal (in Cursor)**

Open Cursor → Terminal (Ctrl+` or View → Terminal), then:

```bash
# Navigate to where you want the project
cd ~/projects  # or wherever you keep projects

# Clone your repo
git clone https://github.com/taytayob13/gematria-hive.git

# Enter the directory
cd gematria-hive

# Open in Cursor
code .
```

---

## 📍 STEP 2: Set Up Cursor (On Your Local Machine)

### C. Set Up Python Environment in Cursor:

```bash
# Create virtual environment
python3.12 -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux

# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### D. Create .env file (for local development):

```bash
# Copy the example
cp .env.example .env

# Edit .env and add your actual values (when you get them in Phase 2)
nano .env  # or use Cursor to edit
```

### Configure Cursor Python Interpreter

1. Press **Cmd/Ctrl+Shift+P** to open command palette
2. Type and select: **Python: Select Interpreter**
3. Choose the venv you just created:
   - macOS/Linux: `./venv/bin/python`
   - Windows: `.\venv\Scripts\python.exe`

---

## Step 4: Test Streamlit App in Cursor

Run the app locally in Cursor:

```bash
# Make sure venv is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Run Streamlit
streamlit run app.py
```

You should see:
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Open `http://localhost:8501` in your browser to test.

**Note:** Local dev uses port **8501** by default. Replit uses **5000** (configured in `.streamlit/config.toml`).

---

## 📍 STEP 3: Daily Workflow (After Setup)

### When you work in Replit:

```bash
# Make changes in Replit
# Test with Run button
# Commit via Git pane (Steps 1-6 above)
# Push to GitHub
```

Then pull to Cursor:

```bash
# In Cursor terminal
git pull origin main
```

### When you work in Cursor:

```bash
# Make changes in Cursor
# Test locally: streamlit run app.py
# Commit and push
git add .
git commit -m "your message"
git push origin main
```

Then pull to Replit:

```bash
# In Replit Shell
git pull origin main
# App auto-redeploys
```

---

## Step 6: Cursor AI Configuration (Optional)

### Enable Cursor AI Features

1. **Cmd/Ctrl+K**: AI code generation
2. **Cmd/Ctrl+L**: AI chat sidebar
3. Configure AI rules for the project:

Create `.cursorrules` in project root:

```
# Gematria Hive - Cursor AI Rules

## Project Context
- Python 3.12 Streamlit app for gematria calculations
- Phase-based development (currently Phase 1)
- Cost-conscious (track API usage)
- See staging/ docs for architecture and roadmap

## Coding Standards
- Use type hints (Python 3.12+)
- Follow PEP 8 style guide
- Prefer composition over inheritance
- Keep functions small (<50 lines)
- Write docstrings for public functions

## Architecture
- See staging/architecture-decisions.md for ADRs
- Modular design (easy to swap DB, LLM, embeddings)
- Cost-optimized (cache aggressively, use free tiers)

## Testing
- Add pytest tests for new features (Phase 2+)
- Test locally before committing
- Run: pytest tests/

## Documentation
- Update staging/ docs when adding libraries
- Create ADR for significant technical decisions
- Update replit.md with major changes
```

This helps Cursor AI understand your project context.

---

## Step 7: Package Management

### In Cursor (Local Development)

Use pip for local packages:
```bash
pip install some-new-library
pip freeze > requirements.txt  # Update requirements
```

### In Replit (Deployment)

Agent will auto-install from `requirements.txt`, or manually:
```bash
pip install some-new-library
```

**Keep in sync:** Always commit `requirements.txt` changes to git.

---

## Troubleshooting

### Issue: "Module not found" in Cursor

**Solution:**
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Different behavior in Cursor vs Replit

**Common causes:**
- Port difference (Cursor: 8501, Replit: 5000) - expected
- Environment variables missing - check `.env` file
- Python version mismatch - both should use 3.12

### Issue: Git conflicts when pulling

**Solution:**
```bash
# Stash local changes
git stash

# Pull latest
git pull origin main

# Reapply your changes
git stash pop

# Resolve conflicts, then commit
git add .
git commit -m "Resolve merge conflicts"
```

### Issue: Streamlit won't start in Cursor

**Solution:**
```bash
# Check Python version
python --version  # Should be 3.12.x

# Reinstall Streamlit
pip uninstall streamlit
pip install streamlit

# Try running again
streamlit run app.py
```

---

## Best Practices

### When to Use Cursor

✅ **Use Cursor for:**
- Heavy refactoring (multi-file changes)
- Complex debugging (breakpoints, step-through)
- Offline development
- Local testing before deployment
- Bulk file operations
- Advanced git workflows (rebasing, cherry-picking)

### When to Use Replit

✅ **Use Replit for:**
- Quick prototypes
- Testing live deployment
- Using Replit integrations (Secrets, Object Storage)
- Sharing with collaborators (instant preview links)
- Production deployment (publish button)

### Hybrid Workflow (Recommended)

1. **Plan** in staging/ docs (either platform)
2. **Code** complex features in Cursor (better IDE)
3. **Test** locally in Cursor
4. **Commit & push** to GitHub
5. **Pull** in Replit
6. **Deploy** from Replit (auto-publish)
7. **Iterate** 🔄

---

## Quick Reference Commands

### Git Sync

```bash
# Pull latest from GitHub
git pull origin main

# Push your changes
git add .
git commit -m "Your message"
git push origin main
```

### Python Environment

```bash
# Activate venv (run every new terminal session)
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install/update packages
pip install -r requirements.txt

# Run app
streamlit run app.py
```

### Cursor AI

```bash
# Open AI chat
Cmd/Ctrl + L

# Generate code
Cmd/Ctrl + K

# AI edit selection
Cmd/Ctrl + I
```

---

## Next Steps

After completing sync setup:

1. ✅ Verify app runs in both Cursor and Replit
2. ✅ Test making a change in Cursor → push → pull in Replit
3. ✅ Test making a change in Replit → push → pull in Cursor
4. ✅ Review `staging/` docs to understand roadmap
5. 🚀 Ready for Phase 2 development!

---

**Sync Status:** 🟢 Ready  
**Last Sync:** Run `git log -1` to check  
**Branch:** main  
**Remote:** origin (GitHub)  

🐝 Happy coding across both platforms! ✨
