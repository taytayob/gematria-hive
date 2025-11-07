# Git Workflow & Hygiene Standards - Gematria Hive

**Purpose:** Prevent git issues from piling up and ensure clean, maintainable repository

---

## 🎯 Core Principles

1. **Commit Early, Commit Often** - Small, focused commits
2. **Never Commit Broken Code** - Always test before committing
3. **Keep Branches Clean** - Regular cleanup and rebasing
4. **Document Changes** - Clear commit messages
5. **Review Before Push** - Check what you're pushing

---

## 📋 Daily Git Hygiene Checklist

### Before Starting Work
```bash
# 1. Check current status
git status

# 2. Pull latest changes
git pull origin main

# 3. Check for uncommitted changes
git diff --stat
```

### During Work
```bash
# Commit small, logical changes frequently
git add <specific-files>
git commit -m "feat: Add specific feature"

# Don't let changes pile up - commit at least every 2 hours
```

### Before Ending Work Day
```bash
# 1. Check status
git status

# 2. Commit any pending changes
git add .
git commit -m "WIP: Work in progress description"

# 3. Push to remote
git push origin <branch-name>

# 4. Verify nothing left behind
git status
```

---

## 🔍 Pre-Commit Checks

### Automated Pre-Commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Pre-commit hook to prevent common issues

echo "🔍 Running pre-commit checks..."

# Check for large files (>10MB)
large_files=$(find . -type f -size +10M -not -path './.git/*' -not -path './node_modules/*' -not -path './venv/*' -not -path './__pycache__/*')
if [ ! -z "$large_files" ]; then
    echo "❌ ERROR: Large files detected (>10MB):"
    echo "$large_files"
    echo "Please remove or add to .gitignore"
    exit 1
fi

# Check for common temporary files
temp_files=$(git diff --cached --name-only | grep -E '\.(log|tmp|temp|swp|swo|~|pyc|pyo)$')
if [ ! -z "$temp_files" ]; then
    echo "⚠️  WARNING: Temporary files detected:"
    echo "$temp_files"
    echo "Consider adding to .gitignore"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for merge conflict markers
conflict_markers=$(git diff --cached | grep -E '^<<<<<<<|^=======|^>>>>>>>')
if [ ! -z "$conflict_markers" ]; then
    echo "❌ ERROR: Merge conflict markers detected!"
    echo "Please resolve conflicts before committing"
    exit 1
fi

# Check for TODO/FIXME in committed code (optional)
# Uncomment if you want to enforce this:
# todos=$(git diff --cached | grep -iE 'TODO|FIXME|XXX|HACK')
# if [ ! -z "$todos" ]; then
#     echo "⚠️  WARNING: TODO/FIXME comments detected in committed code"
# fi

echo "✅ Pre-commit checks passed"
exit 0
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

---

## 📝 Commit Message Standards

### Format
```
<type>: <subject>

<body (optional)>

<footer (optional)>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements
- `ci`: CI/CD changes
- `build`: Build system changes

### Examples
```bash
# Good
git commit -m "feat: Add MCP tool registry support to observer agent"

# Better
git commit -m "feat: Add MCP tool registry support to observer agent

- Initialize tool registry in ObserverAgent.__init__
- Add tool discovery methods
- Enable cross-agent tool sharing"

# Bad
git commit -m "fix stuff"
git commit -m "updates"
git commit -m "WIP"
```

---

## 🌿 Branch Management

### Branch Naming
```
<type>/<description>

Types:
- feat/ - New features
- fix/ - Bug fixes
- docs/ - Documentation
- refactor/ - Refactoring
- test/ - Testing
```

### Branch Workflow
```bash
# 1. Create feature branch from main
git checkout main
git pull origin main
git checkout -b feat/new-feature

# 2. Work on feature
# ... make changes ...

# 3. Commit frequently
git add .
git commit -m "feat: Add feature X"

# 4. Keep branch updated
git checkout main
git pull origin main
git checkout feat/new-feature
git rebase main  # or git merge main

# 5. Push to remote
git push origin feat/new-feature

# 6. Create PR and merge

# 7. Clean up after merge
git checkout main
git pull origin main
git branch -d feat/new-feature
git push origin --delete feat/new-feature
```

---

## 🧹 Regular Cleanup Procedures

### Weekly Cleanup
```bash
# 1. Check for untracked files
git status

# 2. Remove untracked files (be careful!)
git clean -n  # Dry run - see what would be deleted
git clean -f  # Actually delete untracked files
git clean -fd # Delete untracked files and directories

# 3. Check for large files
find . -type f -size +1M -not -path './.git/*' | head -20

# 4. Check git repository size
du -sh .git

# 5. Prune remote branches
git remote prune origin

# 6. Check for stale branches
git branch -vv  # Shows tracking info
```

### Monthly Cleanup
```bash
# 1. Clean up merged branches
git branch --merged main | grep -v "main" | xargs git branch -d

# 2. Optimize repository
git gc --prune=now

# 3. Check repository health
git fsck

# 4. Review .gitignore
# Make sure all temporary files are ignored
```

---

## 🚫 What NOT to Commit

### Never Commit:
- ❌ Large files (>10MB) - Use Git LFS or external storage
- ❌ Secrets/API keys - Use environment variables
- ❌ Temporary files (.log, .tmp, .swp, etc.)
- ❌ Build artifacts (node_modules, dist, __pycache__, etc.)
- ❌ IDE-specific files (.vscode, .idea, etc.) - unless shared
- ❌ Personal notes or TODOs
- ❌ Database dumps
- ❌ Media files (unless necessary)

### Always Add to .gitignore:
```
# Logs
*.log
*.log.txt

# Temporary files
*.tmp
*.temp
*.swp
*.swo
*~

# Build artifacts
node_modules/
dist/
__pycache__/
*.pyc
*.pyo

# IDE
.vscode/
.idea/
*.sublime-*

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
.env.*.local

# Large data files
*.zip
*.csv (if large)
*.db
*.sqlite
```

---

## 🔄 Merge vs Rebase

### Use Merge When:
- Working on shared branches
- Preserving complete history
- Merging feature branches to main

### Use Rebase When:
- Working on personal feature branches
- Cleaning up commit history
- Before merging to main

### Rebase Workflow
```bash
# 1. Update your branch
git checkout feat/my-feature
git fetch origin
git rebase origin/main

# 2. Resolve conflicts if any
# ... fix conflicts ...
git add .
git rebase --continue

# 3. Force push (only on your branch!)
git push origin feat/my-feature --force-with-lease
```

---

## 🛡️ Safety Checks

### Before Force Push
```bash
# Always use --force-with-lease instead of --force
git push origin <branch> --force-with-lease
```

### Before Deleting Branches
```bash
# Check if branch is merged
git branch --merged main

# Check remote branches
git branch -r

# Delete local branch
git branch -d <branch-name>

# Delete remote branch
git push origin --delete <branch-name>
```

### Before Large Changes
```bash
# Create backup branch
git checkout -b backup-before-large-change
git push origin backup-before-large-change

# Or create a tag
git tag backup-$(date +%Y%m%d)
git push origin backup-$(date +%Y%m%d)
```

---

## 📊 Git Status Interpretation

### Clean Working Directory
```
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```
✅ **Good to go!**

### Uncommitted Changes
```
On branch main
Your branch is up to date with 'origin/main'.
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes)
```
⚠️ **Commit or stash these changes**

### Untracked Files
```
Untracked files:
  (use "git add <file>..." to include in what will be committed)
```
⚠️ **Review and add to .gitignore if temporary**

### Diverged Branches
```
Your branch and 'origin/main' have diverged,
and have 5 and 3 different commits each, respectively.
```
⚠️ **Need to rebase or merge**

---

## 🚀 Quick Commands Reference

### Daily Commands
```bash
# Check status
git status

# See what changed
git diff

# Stage changes
git add <file>
git add .  # All files (be careful!)

# Commit
git commit -m "type: description"

# Push
git push origin <branch>

# Pull
git pull origin <branch>
```

### Emergency Commands
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Stash changes
git stash
git stash pop

# Discard local changes
git checkout -- <file>
git reset --hard HEAD
```

---

## 📅 Weekly Git Maintenance Script

Create `scripts/git_maintenance.sh`:

```bash
#!/bin/bash
# Weekly Git Maintenance Script

echo "🧹 Running weekly git maintenance..."

# 1. Check status
echo "📊 Checking git status..."
git status

# 2. Prune remote branches
echo "🌿 Pruning remote branches..."
git remote prune origin

# 3. Clean untracked files (dry run)
echo "🧹 Checking for untracked files..."
git clean -n

# 4. Check for large files
echo "📦 Checking for large files..."
find . -type f -size +1M -not -path './.git/*' -not -path './node_modules/*' | head -10

# 5. Optimize repository
echo "⚡ Optimizing repository..."
git gc --prune=now

# 6. Check repository size
echo "📏 Repository size:"
du -sh .git

echo "✅ Maintenance complete!"
```

Make it executable:
```bash
chmod +x scripts/git_maintenance.sh
```

Run weekly:
```bash
./scripts/git_maintenance.sh
```

---

## ✅ Pre-Push Checklist

Before pushing to remote:

- [ ] All tests pass
- [ ] Code is formatted
- [ ] No merge conflicts
- [ ] No large files
- [ ] No temporary files
- [ ] No secrets/API keys
- [ ] Commit messages are clear
- [ ] Branch is up to date
- [ ] Changes are reviewed

---

## 🎯 Golden Rules

1. **Never commit broken code** - Always test first
2. **Commit small, logical changes** - Don't let changes pile up
3. **Write clear commit messages** - Future you will thank you
4. **Keep branches clean** - Regular cleanup prevents issues
5. **Review before push** - Check what you're pushing
6. **Use branches for features** - Don't work directly on main
7. **Pull before push** - Always sync with remote first
8. **Don't force push to shared branches** - Use merge instead

---

## 📚 Additional Resources

- [Git Best Practices](https://github.com/git/git/blob/master/Documentation/SubmittingPatches)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Workflow Guide](https://www.atlassian.com/git/tutorials/comparing-workflows)

---

**Remember:** Clean git history = Happy team = Better codebase! 🐝✨

