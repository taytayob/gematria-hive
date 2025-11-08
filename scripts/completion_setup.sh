#!/bin/bash
# System-agnostic completion setup
# Detects shell and installs appropriate completion

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SHELL_NAME=$(basename "$SHELL")

echo "🔧 Setting up autocompletion for Gematria Hive..."
echo "Detected shell: $SHELL_NAME"

# Detect shell type
if [[ "$SHELL_NAME" == "zsh" ]]; then
    COMPLETION_FILE="$PROJECT_ROOT/scripts/completion.zsh"
    RC_FILE="$HOME/.zshrc"
    COMPLETION_DIR="$HOME/.zsh/completions"
elif [[ "$SHELL_NAME" == "bash" ]]; then
    COMPLETION_FILE="$PROJECT_ROOT/scripts/completion.bash"
    RC_FILE="$HOME/.bashrc"
    COMPLETION_DIR="$HOME/.bash_completion.d"
else
    echo "⚠️  Unsupported shell: $SHELL_NAME"
    echo "Supported shells: bash, zsh"
    exit 1
fi

# Create completion directory
mkdir -p "$COMPLETION_DIR"

# Copy completion file
if [ -f "$COMPLETION_FILE" ]; then
    cp "$COMPLETION_FILE" "$COMPLETION_DIR/gematria-hive"
    echo "✅ Completion file installed: $COMPLETION_DIR/gematria-hive"
else
    echo "❌ Completion file not found: $COMPLETION_FILE"
    exit 1
fi

# Add to RC file if not already present
if ! grep -q "gematria-hive" "$RC_FILE" 2>/dev/null; then
    echo "" >> "$RC_FILE"
    echo "# Gematria Hive completion" >> "$RC_FILE"
    if [[ "$SHELL_NAME" == "zsh" ]]; then
        echo "fpath=(\$HOME/.zsh/completions \$fpath)" >> "$RC_FILE"
        echo "autoload -U compinit && compinit" >> "$RC_FILE"
    else
        echo "source $COMPLETION_DIR/gematria-hive" >> "$RC_FILE"
    fi
    echo "✅ Added to $RC_FILE"
    echo "⚠️  Please restart your shell or run: source $RC_FILE"
else
    echo "✅ Already configured in $RC_FILE"
fi

echo "✅ Autocompletion setup complete!"

