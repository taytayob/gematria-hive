# Replit Branch Cleanup - Instructions

**Purpose:** Clean up branches in Replit (stage, replit-agent)

**Date:** November 6, 2025

---

## Current Situation in Replit

You have these branches:
- ✅ `main` (keep this)
- ⚠️ `replit-agent` (check if needed)
- ⚠️ `stage` (delete - was created by mistake)
- ⚠️ `remotes/origin/stage` (delete - remote branch)

---

## Step-by-Step Cleanup

### Step 1: Switch to Main Branch

**In Replit Shell:**

```bash
git checkout main
```

### Step 2: Pull Latest Changes

**In Replit Shell:**

```bash
git pull origin main --rebase
```

### Step 3: Check replit-agent Branch

**In Replit Shell:**

```bash
# See what's in replit-agent branch
git log --oneline replit-agent -5

# Check if it has unique changes
git log --oneline main..replit-agent | head -10
```

**If replit-agent has important changes:**
```bash
# Merge it into main first
git merge replit-agent --no-ff -m "Merge replit-agent branch"
git push origin main
```

**If replit-agent has no unique changes:**
- Proceed to delete it

### Step 4: Delete Local Branches

**In Replit Shell:**

```bash
# Delete local stage branch
git branch -d stage

# Delete local replit-agent branch (if not needed)
git branch -d replit-agent

# Force delete if needed
git branch -D stage
git branch -D replit-agent
```

### Step 5: Delete Remote Branches

**In Replit Shell:**

```bash
# Delete remote stage branch
git push origin --delete stage

# Delete remote replit-agent branch (if exists and not needed)
git push origin --delete replit-agent 2>/dev/null || echo "replit-agent doesn't exist on remote"
```

### Step 6: Prune Remote References

**In Replit Shell:**

```bash
# Remove stale remote references
git fetch origin --prune
```

### Step 7: Verify Cleanup

**In Replit Shell:**

```bash
# Check all branches
git branch -a

# Should only see:
# * main
#   remotes/origin/main
#   remotes/origin/HEAD -> origin/main
```

---

## Complete Cleanup Script (Copy-Paste)

**Run this in Replit Shell:**

```bash
# Switch to main
git checkout main

# Pull latest
git pull origin main --rebase

# Check replit-agent (optional - see what's in it)
echo "=== Checking replit-agent branch ==="
git log --oneline replit-agent -3

# Delete local branches
git branch -d stage 2>/dev/null || git branch -D stage
git branch -d replit-agent 2>/dev/null || echo "replit-agent already deleted or doesn't exist"

# Delete remote branches
git push origin --delete stage 2>/dev/null || echo "Remote stage already deleted"
git push origin --delete replit-agent 2>/dev/null || echo "Remote replit-agent doesn't exist"

# Prune stale references
git fetch origin --prune

# Verify
echo "=== Final branch status ==="
git branch -a
```

---

## After Cleanup

**You should only have:**
- ✅ `main` branch (local)
- ✅ `remotes/origin/main` (remote)
- ✅ `remotes/origin/HEAD -> origin/main` (default)

**All other branches deleted!**

---

## If You Get Errors

### "Cannot delete branch 'main'"
- This is normal - you can't delete the branch you're on
- Make sure you're on `main` first

### "Remote branch not found"
- Branch already deleted - that's fine
- Continue with cleanup

### "Branch has unmerged changes"
- Use `git branch -D` (force delete) instead of `-d`
- Or merge the branch first if it has important changes

---

**Ready to clean up!** 🐝✨

