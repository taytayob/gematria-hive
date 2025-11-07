#!/bin/bash
# Pre-commit hook template
# Copy this to .git/hooks/pre-commit and make it executable
# Usage: cp scripts/pre-commit-hook-template.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit

set -e  # Exit on error

echo "🔍 Running pre-commit checks..."

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Check for large files (>10MB)
echo "📦 Checking for large files..."
large_files=$(find . -type f -size +10M -not -path './.git/*' -not -path './node_modules/*' -not -path './venv/*' -not -path './__pycache__/*' -not -path './dist/*' -not -path './build/*' 2>/dev/null | head -10)
if [ ! -z "$large_files" ]; then
    echo -e "${RED}❌ ERROR: Large files detected (>10MB):${NC}"
    echo "$large_files"
    echo "Please remove or add to .gitignore"
    exit 1
fi
echo -e "${GREEN}✅ No large files detected${NC}"

# 2. Check for temporary files in staged changes
echo "🧹 Checking for temporary files..."
temp_files=$(git diff --cached --name-only | grep -E '\.(log|tmp|temp|swp|swo|~|pyc|pyo|checkpoint)$' || true)
if [ ! -z "$temp_files" ]; then
    echo -e "${YELLOW}⚠️  WARNING: Temporary files detected:${NC}"
    echo "$temp_files"
    echo "Consider adding to .gitignore"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
echo -e "${GREEN}✅ No temporary files detected${NC}"

# 3. Check for merge conflict markers
echo "🔍 Checking for merge conflict markers..."
conflict_markers=$(git diff --cached | grep -E '^<<<<<<<|^=======|^>>>>>>>' || true)
if [ ! -z "$conflict_markers" ]; then
    echo -e "${RED}❌ ERROR: Merge conflict markers detected!${NC}"
    echo "Please resolve conflicts before committing"
    exit 1
fi
echo -e "${GREEN}✅ No merge conflicts detected${NC}"

# 4. Check for secrets/API keys (basic check)
echo "🔐 Checking for potential secrets..."
secrets=$(git diff --cached | grep -iE '(api[_-]?key|secret|password|token|credential)\s*[:=]\s*["\']?[a-zA-Z0-9]{20,}' || true)
if [ ! -z "$secrets" ]; then
    echo -e "${RED}❌ ERROR: Potential secrets detected!${NC}"
    echo "Please use environment variables instead"
    echo "Secrets found:"
    echo "$secrets" | head -5
    exit 1
fi
echo -e "${GREEN}✅ No secrets detected${NC}"

# 5. Check commit message format (if commit message is provided)
if [ -n "$1" ]; then
    commit_msg="$1"
    if ! echo "$commit_msg" | grep -qE '^(feat|fix|docs|style|refactor|test|chore|perf|ci|build):'; then
        echo -e "${YELLOW}⚠️  WARNING: Commit message doesn't follow conventional format${NC}"
        echo "Format: <type>: <subject>"
        echo "Types: feat, fix, docs, style, refactor, test, chore, perf, ci, build"
    fi
fi

# 6. Check for TODO/FIXME in committed code (optional - uncomment if desired)
# echo "📝 Checking for TODO/FIXME comments..."
# todos=$(git diff --cached | grep -iE 'TODO|FIXME|XXX|HACK' || true)
# if [ ! -z "$todos" ]; then
#     echo -e "${YELLOW}⚠️  WARNING: TODO/FIXME comments detected in committed code${NC}"
#     echo "$todos" | head -5
# fi

echo ""
echo -e "${GREEN}✅ Pre-commit checks passed${NC}"
exit 0

