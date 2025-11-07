#!/bin/bash
# Weekly Git Maintenance Script
# Run this weekly to keep git repository clean and healthy

set -e  # Exit on error

echo "🧹 ========================================"
echo "🧹 Weekly Git Maintenance"
echo "🧹 ========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Check status
echo "📊 1. Checking git status..."
status=$(git status --porcelain)
if [ -z "$status" ]; then
    echo -e "${GREEN}✅ Working directory is clean${NC}"
else
    echo -e "${YELLOW}⚠️  Uncommitted changes detected:${NC}"
    echo "$status"
fi
echo ""

# 2. Prune remote branches
echo "🌿 2. Pruning remote branches..."
pruned=$(git remote prune origin --dry-run 2>&1 | grep -c "prune" || true)
if [ "$pruned" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Found $pruned stale remote branches${NC}"
    read -p "Prune them? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote prune origin
        echo -e "${GREEN}✅ Remote branches pruned${NC}"
    fi
else
    echo -e "${GREEN}✅ No stale remote branches${NC}"
fi
echo ""

# 3. Check for untracked files
echo "🧹 3. Checking for untracked files..."
untracked=$(git ls-files --others --exclude-standard | wc -l | tr -d ' ')
if [ "$untracked" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Found $untracked untracked files${NC}"
    echo "Top 10 untracked files:"
    git ls-files --others --exclude-standard | head -10
    echo ""
    echo "Review these files and add to .gitignore if temporary"
else
    echo -e "${GREEN}✅ No untracked files${NC}"
fi
echo ""

# 4. Check for large files
echo "📦 4. Checking for large files (>1MB)..."
large_files=$(find . -type f -size +1M -not -path './.git/*' -not -path './node_modules/*' -not -path './venv/*' -not -path './__pycache__/*' -not -path './dist/*' -not -path './build/*' 2>/dev/null | head -10)
if [ ! -z "$large_files" ]; then
    echo -e "${YELLOW}⚠️  Large files detected:${NC}"
    echo "$large_files" | while read file; do
        size=$(du -h "$file" | cut -f1)
        echo "  - $file ($size)"
    done
    echo ""
    echo "Consider adding large files to .gitignore or using Git LFS"
else
    echo -e "${GREEN}✅ No large files detected${NC}"
fi
echo ""

# 5. Check repository size
echo "📏 5. Checking repository size..."
repo_size=$(du -sh .git 2>/dev/null | cut -f1)
echo "Repository size: $repo_size"
if [ -f .git/objects/pack/pack-*.pack ]; then
    pack_size=$(du -sh .git/objects/pack/pack-*.pack 2>/dev/null | cut -f1 | head -1)
    echo "Pack file size: $pack_size"
fi
echo ""

# 6. Check for merged branches
echo "🌿 6. Checking for merged branches..."
merged_branches=$(git branch --merged main 2>/dev/null | grep -v "main" | grep -v "master" | sed 's/^[ *]*//' || true)
if [ ! -z "$merged_branches" ]; then
    echo -e "${YELLOW}⚠️  Merged branches that can be deleted:${NC}"
    echo "$merged_branches"
    echo ""
    read -p "Delete these branches? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "$merged_branches" | xargs -r git branch -d
        echo -e "${GREEN}✅ Merged branches deleted${NC}"
    fi
else
    echo -e "${GREEN}✅ No merged branches to clean up${NC}"
fi
echo ""

# 7. Optimize repository (optional)
echo "⚡ 7. Optimizing repository..."
read -p "Run git gc (garbage collection)? This may take a while. (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git gc --prune=now
    echo -e "${GREEN}✅ Repository optimized${NC}"
else
    echo "Skipped optimization"
fi
echo ""

# 8. Check for merge conflicts
echo "🔍 8. Checking for merge conflict markers..."
conflicts=$(git diff HEAD | grep -E '^<<<<<<<|^=======|^>>>>>>>' || true)
if [ ! -z "$conflicts" ]; then
    echo -e "${RED}❌ Merge conflict markers detected!${NC}"
    echo "Please resolve conflicts before continuing"
    exit 1
else
    echo -e "${GREEN}✅ No merge conflicts detected${NC}"
fi
echo ""

# 9. Check .gitignore
echo "📋 9. Checking .gitignore..."
if [ ! -f .gitignore ]; then
    echo -e "${YELLOW}⚠️  .gitignore file not found${NC}"
else
    echo -e "${GREEN}✅ .gitignore file exists${NC}"
    # Check if common patterns are in .gitignore
    common_patterns=("*.log" "*.tmp" "__pycache__" "node_modules" ".env")
    missing_patterns=()
    for pattern in "${common_patterns[@]}"; do
        if ! grep -q "$pattern" .gitignore 2>/dev/null; then
            missing_patterns+=("$pattern")
        fi
    done
    if [ ${#missing_patterns[@]} -gt 0 ]; then
        echo -e "${YELLOW}⚠️  Consider adding to .gitignore:${NC}"
        printf '  - %s\n' "${missing_patterns[@]}"
    else
        echo -e "${GREEN}✅ Common patterns are in .gitignore${NC}"
    fi
fi
echo ""

# Summary
echo "🧹 ========================================"
echo "✅ Maintenance complete!"
echo "🧹 ========================================"
echo ""
echo "Next steps:"
echo "  1. Review any warnings above"
echo "  2. Commit pending changes"
echo "  3. Push to remote"
echo "  4. Clean up merged branches"
echo ""

