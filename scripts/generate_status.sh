#!/bin/bash
# Generate status report for current work
# Usage: ./scripts/generate_status.sh

echo "📊 ========================================"
echo "📊 GEMATRIA HIVE - STATUS REPORT"
echo "📊 ========================================"
echo ""
echo "📅 Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Git Status
echo "🌿 Git Status:"
echo "   Branch: $(git rev-parse --abbrev-ref HEAD)"
echo "   Last Commit: $(git log -1 --oneline)"
echo "   Uncommitted Changes: $(git status --porcelain | wc -l | tr -d ' ') files"
echo ""

# Recent Commits
echo "📝 Recent Commits (last 5):"
git log --oneline -5 | sed 's/^/   /'
echo ""

# Modified Files
echo "📝 Modified Files:"
git status --porcelain | head -10 | sed 's/^/   /'
if [ $(git status --porcelain | wc -l) -gt 10 ]; then
    echo "   ... and $(($(git status --porcelain | wc -l) - 10)) more"
fi
echo ""

# Next Steps (from NEXT_STEPS_PLAN.md if exists)
if [ -f "NEXT_STEPS_PLAN.md" ]; then
    echo "🎯 Next Steps (from NEXT_STEPS_PLAN.md):"
    grep -A 5 "## Immediate\|## This Week\|## Next" NEXT_STEPS_PLAN.md | head -10 | sed 's/^/   /'
    echo ""
fi

# Critical Path (from CRITICAL_PATH.md if exists)
if [ -f "CRITICAL_PATH.md" ]; then
    echo "🚨 Critical Path Items:"
    grep -E "^\s*[-*]\s*\[.*\]" CRITICAL_PATH.md | head -5 | sed 's/^/   /'
    echo ""
fi

# Phase Status (from NEXT_PHASE_ROADMAP.md if exists)
if [ -f "NEXT_PHASE_ROADMAP.md" ]; then
    echo "📈 Current Phase:"
    grep -E "Phase|## Phase" NEXT_PHASE_ROADMAP.md | head -3 | sed 's/^/   /'
    echo ""
fi

# System Status
echo "🔧 System Status:"
echo "   Internal API: $(curl -s http://localhost:8001/internal/health 2>/dev/null | grep -q 'healthy' && echo '✅ Running' || echo '❌ Not running')"
echo "   Kanban API: $(curl -s http://localhost:8000/health 2>/dev/null | grep -q 'healthy' && echo '✅ Running' || echo '❌ Not running')"
echo ""

echo "📊 ========================================"

