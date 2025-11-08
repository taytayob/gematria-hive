#!/bin/bash
# Baseline Integrity Check
# Verifies system state matches expected baseline

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🔍 ========================================"
echo "🔍 Baseline Integrity Check"
echo "🔍 ========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0
WARNINGS=0

# 1. Check required files exist
echo "📁 1. Checking required files..."
REQUIRED_FILES=(
    "README.md"
    "requirements.txt"
    "docker-compose.yml"
    ".gitignore"
    "GIT_WORKFLOW.md"
    "CURRENT_STATUS.md"
    "NEXT_STEPS_PLAN.md"
    "CRITICAL_PATH.md"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$PROJECT_ROOT/$file" ]; then
        echo -e "${GREEN}✅ $file${NC}"
    else
        echo -e "${RED}❌ $file missing${NC}"
        ((ERRORS++))
    fi
done
echo ""

# 2. Check required directories exist
echo "📂 2. Checking required directories..."
REQUIRED_DIRS=(
    "agents"
    "core"
    "scripts"
    "docs"
    "tests"
    "migrations"
    "schemas"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$PROJECT_ROOT/$dir" ]; then
        echo -e "${GREEN}✅ $dir/${NC}"
    else
        echo -e "${RED}❌ $dir/ missing${NC}"
        ((ERRORS++))
    fi
done
echo ""

# 3. Check critical scripts exist
echo "🔧 3. Checking critical scripts..."
CRITICAL_SCRIPTS=(
    "scripts/auto_commit.sh"
    "scripts/generate_status.sh"
    "scripts/git_maintenance.sh"
    "scripts/baseline_integrity.sh"
    "run_kanban.py"
    "run_internal_api.py"
    "run_agents.py"
)

for script in "${CRITICAL_SCRIPTS[@]}"; do
    if [ -f "$PROJECT_ROOT/$script" ]; then
        if [ -x "$PROJECT_ROOT/$script" ]; then
            echo -e "${GREEN}✅ $script (executable)${NC}"
        else
            echo -e "${YELLOW}⚠️  $script (not executable)${NC}"
            ((WARNINGS++))
        fi
    else
        echo -e "${RED}❌ $script missing${NC}"
        ((ERRORS++))
    fi
done
echo ""

# 4. Check Python dependencies
echo "🐍 4. Checking Python dependencies..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✅ Python $PYTHON_VERSION installed${NC}"
    
    # Check critical packages
    CRITICAL_PACKAGES=("fastapi" "uvicorn" "supabase" "pydantic")
    for package in "${CRITICAL_PACKAGES[@]}"; do
        if python3 -c "import $package" 2>/dev/null; then
            echo -e "${GREEN}✅ $package installed${NC}"
        else
            echo -e "${RED}❌ $package not installed${NC}"
            ((ERRORS++))
        fi
    done
else
    echo -e "${RED}❌ Python3 not found${NC}"
    ((ERRORS++))
fi
echo ""

# 5. Check environment variables
echo "🔐 5. Checking environment variables..."
if [ -f "$PROJECT_ROOT/.env" ]; then
    echo -e "${GREEN}✅ .env file exists${NC}"
    
    # Check for critical variables
    if grep -q "SUPABASE_URL" "$PROJECT_ROOT/.env"; then
        echo -e "${GREEN}✅ SUPABASE_URL configured${NC}"
    else
        echo -e "${YELLOW}⚠️  SUPABASE_URL not configured${NC}"
        ((WARNINGS++))
    fi
    
    if grep -q "SUPABASE_KEY" "$PROJECT_ROOT/.env"; then
        echo -e "${GREEN}✅ SUPABASE_KEY configured${NC}"
    else
        echo -e "${YELLOW}⚠️  SUPABASE_KEY not configured${NC}"
        ((WARNINGS++))
    fi
else
    echo -e "${YELLOW}⚠️  .env file not found (using defaults)${NC}"
    ((WARNINGS++))
fi
echo ""

# 6. Check git repository integrity
echo "🌿 6. Checking git repository integrity..."
if [ -d "$PROJECT_ROOT/.git" ]; then
    echo -e "${GREEN}✅ Git repository initialized${NC}"
    
    # Check for uncommitted changes
    if [ -z "$(git status --porcelain 2>/dev/null)" ]; then
        echo -e "${GREEN}✅ Working directory clean${NC}"
    else
        echo -e "${YELLOW}⚠️  Uncommitted changes detected${NC}"
        ((WARNINGS++))
    fi
    
    # Check for remote
    if git remote get-url origin &>/dev/null; then
        echo -e "${GREEN}✅ Remote configured${NC}"
    else
        echo -e "${YELLOW}⚠️  No remote configured${NC}"
        ((WARNINGS++))
    fi
else
    echo -e "${RED}❌ Not a git repository${NC}"
    ((ERRORS++))
fi
echo ""

# 7. Check baseline files integrity
echo "📋 7. Checking baseline files integrity..."
BASELINE_FILES=(
    "GIT_WORKFLOW.md"
    "CURRENT_STATUS.md"
    "NEXT_STEPS_PLAN.md"
    "CRITICAL_PATH.md"
)

for file in "${BASELINE_FILES[@]}"; do
    if [ -f "$PROJECT_ROOT/$file" ]; then
        # Check if file has content
        if [ -s "$PROJECT_ROOT/$file" ]; then
            echo -e "${GREEN}✅ $file (has content)${NC}"
        else
            echo -e "${YELLOW}⚠️  $file (empty)${NC}"
            ((WARNINGS++))
        fi
    else
        echo -e "${RED}❌ $file missing${NC}"
        ((ERRORS++))
    fi
done
echo ""

# 8. Check system services (if running)
echo "🔧 8. Checking system services..."
if curl -s http://localhost:8001/internal/health &>/dev/null; then
    echo -e "${GREEN}✅ Internal API running (port 8001)${NC}"
else
    echo -e "${YELLOW}⚠️  Internal API not running${NC}"
    ((WARNINGS++))
fi

if curl -s http://localhost:8000/health &>/dev/null; then
    echo -e "${GREEN}✅ Kanban API running (port 8000)${NC}"
else
    echo -e "${YELLOW}⚠️  Kanban API not running${NC}"
    ((WARNINGS++))
fi
echo ""

# Summary
echo "🔍 ========================================"
echo "📊 Integrity Check Summary"
echo "🔍 ========================================"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ Baseline integrity: PASSED${NC}"
    echo "   All checks passed"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Baseline integrity: PASSED WITH WARNINGS${NC}"
    echo "   Errors: $ERRORS"
    echo "   Warnings: $WARNINGS"
    exit 0
else
    echo -e "${RED}❌ Baseline integrity: FAILED${NC}"
    echo "   Errors: $ERRORS"
    echo "   Warnings: $WARNINGS"
    exit 1
fi

