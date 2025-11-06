# Cursor IDE Sync Instructions

**Purpose:** Set up bidirectional sync between Replit and Cursor for hybrid development workflow.

**Last Updated:** November 6, 2025

---

## Prerequisites

✅ Git repository pushed to GitHub (complete `GIT_COMMIT_INSTRUCTIONS.md` first)  
✅ Cursor IDE installed on your local machine  
✅ GitHub account with SSH or HTTPS access configured  

---

## Step 1: Clone Repository in Cursor

### Option A: Using Cursor UI

1. Open **Cursor IDE**
2. Click **File → Open Folder** (or Cmd/Ctrl+O)
3. Click **Clone Repository** button
4. Enter your GitHub repo URL:
   ```
   https://github.com/YOUR_USERNAME/gematria-hive.git
   ```
   Or SSH:
   ```
   git@github.com:YOUR_USERNAME/gematria-hive.git
   ```
5. Choose local directory (e.g., `~/projects/gematria-hive`)
6. Click **Clone**

### Option B: Using Terminal (in Cursor)

1. Open **Cursor IDE**
2. Open integrated terminal (Ctrl+` or View → Terminal)
3. Navigate to your projects directory:
   ```bash
   cd ~/projects
   ```
4. Clone the repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/gematria-hive.git
   cd gematria-hive
   ```
5. Open the folder in Cursor: **File → Open Folder** → select `gematria-hive`

---

## Step 2: Set Up Python Environment in Cursor

### Install Python (if not already installed)

**macOS:**
```bash
brew install python@3.11
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv
```

**Windows:**
Download from [python.org](https://www.python.org/downloads/)

### Create Virtual Environment

In Cursor's terminal:

```bash
# Create venv
python3.11 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configure Cursor Python Interpreter

1. Press **Cmd/Ctrl+Shift+P** to open command palette
2. Type and select: **Python: Select Interpreter**
3. Choose the venv you just created:
   - macOS/Linux: `./venv/bin/python`
   - Windows: `.\venv\Scripts\python.exe`

---

## Step 3: Set Up Environment Variables

Create `.env` file in Cursor (copied from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` and add your actual credentials:

```env
SUPABASE_URL=your_actual_supabase_url_here
SUPABASE_KEY=your_actual_supabase_key_here
CLICKHOUSE_HOST=your_clickhouse_host_here
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=your_password_here
```

**Important:** `.env` is in `.gitignore` and won't be committed (for security).

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

## Step 5: Bidirectional Sync Workflow

### Work in Cursor → Push to Replit

```bash
# Make changes in Cursor
# ... edit files ...

# Stage and commit
git add .
git commit -m "feat: Add new feature from Cursor"

# Push to GitHub
git push origin main
```

Then in **Replit Shell**:
```bash
git pull origin main
# Replit auto-deploys after pull
```

### Work in Replit → Pull to Cursor

After making changes in Replit and pushing (see `GIT_COMMIT_INSTRUCTIONS.md`):

In **Cursor terminal**:
```bash
git pull origin main
```

Your local copy is now synced!

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
- Python 3.11 Streamlit app for gematria calculations
- Phase-based development (currently Phase 1)
- Cost-conscious (track API usage)
- See staging/ docs for architecture and roadmap

## Coding Standards
- Use type hints (Python 3.11+)
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
- Python version mismatch - both should use 3.11

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
python --version  # Should be 3.11.x

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
