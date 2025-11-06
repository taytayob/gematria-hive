# Merge Stage Branch into Main - Instructions

**Purpose:** Merge the accidentally created `stage` branch into `main` and clean up

**Date:** November 6, 2025

---

## Current Situation

- ✅ `main` branch is **ahead** of `stage` branch
- ✅ `main` has all the latest changes (Supabase setup, ingestion script, etc.)
- ✅ `stage` branch is missing recent commits
- ⚠️ `stage` branch was created by mistake in Replit

---

## Step-by-Step Merge Process

### Step 1: Check for Uncommitted Changes in Replit

**In Replit (on stage branch):**

```bash
# In Replit Shell
git status
```

**If you have uncommitted changes:**
```bash
# In Replit Shell
git add .
git commit -m "Save changes from stage branch"
git push origin stage
```

**If no uncommitted changes:**
- Proceed to Step 2

---

### Step 2: Merge Stage into Main (CLI/Cursor)

**In CLI/Cursor:**

```bash
# In Cursor/CLI terminal
cd /Users/cooperladd/Desktop/gematria-hive/gematria-hive
source venv/bin/activate  # If needed
git checkout main
git pull origin main --rebase
git merge origin/stage --no-ff -m "Merge stage branch into main"
```

**If merge conflicts occur:**
```bash
# Resolve conflicts in files
# Edit files to remove <<<<<<< markers
git add .
git commit -m "Resolve merge conflicts from stage branch"
```

---

### Step 3: Push Merged Changes

```bash
# In Cursor/CLI terminal
git push origin main
```

---

### Step 4: Delete Stage Branch

**Delete local branch:**
```bash
# In Cursor/CLI terminal
git branch -d stage  # Safe delete (only if merged)
# OR
git branch -D stage  # Force delete
```

**Delete remote branch:**
```bash
# In Cursor/CLI terminal
git push origin --delete stage
```

**Or delete via GitHub:**
1. Go to: https://github.com/taytayob/gematria-hive/branches
2. Click "Delete branch" next to `stage` branch

---

## Alternative: Quick Cleanup (If Stage Has No Unique Changes)

Since `main` is ahead of `stage`, you can simply delete the branch:

**In Replit:**
```bash
# In Replit Shell
git checkout main
git pull origin main
```

**In CLI/Cursor:**
```bash
# In Cursor/CLI terminal
git checkout main
git pull origin main --rebase
git push origin --delete stage
```

---

## Verification

**After merge/cleanup:**

```bash
# Check branches
git branch -a

# Verify main is up to date
git status

# Check recent commits
git log --oneline -5
```

---

## Summary

**Recommended Action:**
1. ✅ Check Replit for uncommitted changes on `stage` branch
2. ✅ If changes exist, commit and push them
3. ✅ Merge `stage` into `main` (or just delete if no unique changes)
4. ✅ Delete `stage` branch (local and remote)
5. ✅ Verify everything is synced

**Since `main` is ahead, you can likely just delete `stage` branch directly.**

---

**Ready to proceed!** 🐝✨

