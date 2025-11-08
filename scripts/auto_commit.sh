#!/bin/bash
# Auto-commit script - Run after completing work
# Usage: ./scripts/auto_commit.sh "commit message"

set -e

COMMIT_MSG="${1:-Auto-commit: Work completed}"
BRANCH=$(git rev-parse --abbrev-ref HEAD)

echo "🔄 Auto-committing changes..."

# Check if there are changes to commit
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ No changes to commit"
    exit 0
fi

# Stage all changes
git add .

# Commit with message
git commit -m "$COMMIT_MSG"

# Push to remote
echo "📤 Pushing to remote..."
git push origin "$BRANCH" || echo "⚠️  Push failed - check remote connection"

echo "✅ Auto-commit complete: $COMMIT_MSG"

