# Quick Git Reference - Gematria Hive

**Quick commands for daily git workflow**

---

## 📋 Daily Checklist

### Before Starting Work
```bash
git status              # Check current status
git pull origin main    # Get latest changes
```

### During Work
```bash
git add <file>          # Stage specific file
git commit -m "type: description"  # Commit changes
```

### Before Ending Work
```bash
git status              # Check what's left
git add .               # Stage all changes
git commit -m "WIP: description"  # Commit
git push origin <branch>  # Push to remote
```

---

## 🚀 Common Commands

### Status & Info
```bash
git status              # Check status
git log --oneline -10   # Recent commits
git diff                # See changes
git diff --staged       # See staged changes
```

### Staging & Committing
```bash
git add <file>          # Stage file
git add .               # Stage all
git commit -m "message" # Commit
git commit --amend      # Fix last commit
```

### Branching
```bash
git branch              # List branches
git branch <name>       # Create branch
git checkout <branch>   # Switch branch
git checkout -b <name>  # Create & switch
git merge <branch>      # Merge branch
```

### Remote
```bash
git pull origin main    # Pull from remote
git push origin <branch>  # Push to remote
git fetch origin        # Fetch from remote
```

### Cleanup
```bash
git clean -n            # See what would be deleted
git clean -f            # Delete untracked files
git branch -d <branch>  # Delete local branch
```

---

## ⚠️ Emergency Commands

### Undo Changes
```bash
git checkout -- <file>  # Discard file changes
git reset --hard HEAD   # Discard all changes
git reset --soft HEAD~1 # Undo commit, keep changes
```

### Stash
```bash
git stash               # Save changes temporarily
git stash pop           # Restore stashed changes
git stash list          # List stashes
```

---

## 📝 Commit Message Format

```
<type>: <subject>

<body (optional)>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style
- `refactor`: Refactoring
- `test`: Tests
- `chore`: Maintenance

**Examples:**
```bash
git commit -m "feat: Add MCP tool registry support"
git commit -m "fix: Resolve baseline check bug"
git commit -m "docs: Update README"
```

---

## 🧹 Weekly Maintenance

```bash
./scripts/git_maintenance.sh  # Run weekly cleanup
```

---

## 🚫 Never Commit

- ❌ Large files (>10MB)
- ❌ Secrets/API keys
- ❌ Temporary files (.log, .tmp, etc.)
- ❌ Build artifacts (node_modules, dist, etc.)
- ❌ Database dumps

---

## 📚 Full Guide

See `GIT_WORKFLOW.md` for complete guide.

---

**Remember:** Commit early, commit often, commit clean! 🐝✨

