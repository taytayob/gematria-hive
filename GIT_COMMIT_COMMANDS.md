# Git Commit Commands - All Platforms

**Purpose:** Quick reference for git commands on Replit, CLI, and Cursor

**Last Updated:** November 6, 2025

---

## 🚀 Commit Conda Setup (CLI - Do This Now)

**Run these commands in your CLI terminal:**

```bash
# Navigate to project directory
cd /Users/cooperladd/Desktop/gematria-hive/gematria-hive

# Activate conda environment (if not already)
conda activate gematria_env

# Stage all changes
git add .

# Commit with descriptive message
git commit -m "Add conda environment setup and configuration

- Created environment.yml for conda environment management
- Added CONDA_SETUP.md with detailed conda guide
- Added CONDA_SETUP_ALL_PLATFORMS.md with platform-specific instructions
- Updated .vscode/settings.json to use conda gematria_env interpreter
- All dependencies successfully installed in gematria_env (Python 3.12.12)
- Verified all packages: streamlit, pandas, supabase, sentence-transformers
- Ready for Replit and Cursor sync"

# Push to GitHub
git push origin main

# Verify
git status
git log --oneline -3
```

---

## 📋 Standard Git Workflow (All Platforms)

### Before Starting Work

**Always pull latest first:**

```bash
# Pull latest changes
git pull origin main --rebase

# Verify you're up to date
git status
```

### After Making Changes

**Stage, commit, and push:**

```bash
# Stage changes
git add .

# OR stage specific files
git add file1.py file2.py

# Commit with message
git commit -m "Your descriptive commit message"

# Push to GitHub
git push origin main

# Verify
git status
```

---

## 🔄 Platform-Specific Commands

### CLI (Mac Terminal)

```bash
# Activate conda
conda activate gematria_env

# Pull latest
git pull origin main --rebase

# Make changes...

# Stage and commit
git add .
git commit -m "Your message"
git push origin main
```

### Replit

```bash
# In Replit Shell
# Pull latest
git pull origin main --rebase

# Make changes...

# Stage and commit
git add .
git commit -m "Your message"
git push origin main
```

### Cursor

```bash
# In Cursor terminal
# Activate conda
conda activate gematria_env

# Pull latest
git pull origin main --rebase

# Make changes...

# Stage and commit
git add .
git commit -m "Your message"
git push origin main
```

---

## 📝 Commit Message Guidelines

### Good Commit Messages

```bash
# Descriptive and clear
git commit -m "Add conda environment setup and configuration"

# Multi-line for detailed changes
git commit -m "Add conda environment setup

- Created environment.yml
- Updated Cursor settings
- Added platform-specific guides"

# Feature-specific
git commit -m "Add Supabase ingestion script with AI tagging"
```

### Avoid

```bash
# Too vague
git commit -m "update"

# No context
git commit -m "fix"

# Better
git commit -m "Fix Streamlit port configuration in .replit"
```

---

## 🔍 Useful Git Commands

### Check Status

```bash
# See what's changed
git status

# See detailed changes
git diff

# See staged changes
git diff --staged
```

### View History

```bash
# Recent commits
git log --oneline -10

# Detailed log
git log --oneline --graph --all -10

# See what changed
git show HEAD
```

### Undo Changes

```bash
# Unstage files (keep changes)
git restore --staged file.py

# Discard changes (careful!)
git restore file.py

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

---

## ⚠️ Common Issues

### "Your branch is ahead of origin/main"

**Solution:**
```bash
git push origin main
```

### "Your branch is behind origin/main"

**Solution:**
```bash
git pull origin main --rebase
```

### Merge Conflicts

**Solution:**
```bash
# Pull with rebase
git pull origin main --rebase

# If conflicts occur:
# 1. Edit conflicted files
# 2. Remove <<<<<<< markers
# 3. Stage resolved files
git add .
git rebase --continue
```

### "Nothing to commit"

**Solution:**
- Check if files are staged: `git status`
- Check if files are ignored: `.gitignore`
- Verify you're in the right directory

---

## ✅ Verification Checklist

After committing:

- [ ] `git status` shows "nothing to commit"
- [ ] `git log --oneline -1` shows your commit
- [ ] `git push origin main` succeeds
- [ ] GitHub shows your commit

---

**Ready to commit!** 🐝✨

