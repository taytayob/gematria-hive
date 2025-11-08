# System Autocompletion & Baseline Integrity - Gematria Hive

**Purpose:** System-agnostic autocompletion and baseline integrity checks

---

## 🎯 Overview

This system provides:
1. **Autocompletion** - Shell-agnostic command completion
2. **Baseline Integrity** - Automated system state verification
3. **System Wrapper** - Unified command interface

---

## 🔧 Setup

### Install Autocompletion

```bash
# Run setup script (detects shell automatically)
./scripts/completion_setup.sh

# Or manually for bash
source scripts/completion.bash

# Or manually for zsh
source scripts/completion.zsh
```

### Verify Installation

```bash
# Test completion (type and press TAB)
gematria-hive <TAB>
gh <TAB>
./scripts/<TAB>
```

---

## 📋 Available Commands

### Main Commands (with autocompletion)

```bash
# Run services
gematria-hive run kanban
gematria-hive run internal-api
gematria-hive run agents
gematria-hive run ingestion
gematria-hive run pipeline

# Run tests
gematria-hive test all
gematria-hive test agents
gematria-hive test core
gematria-hive test integration
gematria-hive test api
gematria-hive test kanban

# Commit changes
gematria-hive commit "feat: Add new feature"
gematria-hive commit "fix: Fix bug"
gematria-hive commit "docs: Update documentation"

# Check status
gematria-hive status git
gematria-hive status system
gematria-hive status services
gematria-hive status agents

# Run integrity check
gematria-hive integrity
```

### Short Alias

```bash
# Use 'gh' as shorthand
gh run kanban
gh test all
gh status system
gh integrity
```

---

## 🔍 Baseline Integrity Check

### What It Checks

1. **Required Files** - README.md, requirements.txt, docker-compose.yml, etc.
2. **Required Directories** - agents/, core/, scripts/, docs/, tests/, etc.
3. **Critical Scripts** - All executable scripts present
4. **Python Dependencies** - Critical packages installed
5. **Environment Variables** - SUPABASE_URL, SUPABASE_KEY configured
6. **Git Repository** - Repository initialized, remote configured
7. **Baseline Files** - GIT_WORKFLOW.md, CURRENT_STATUS.md, etc.
8. **System Services** - Internal API, Kanban API running

### Run Integrity Check

```bash
# Manual check
./scripts/baseline_integrity.sh

# Via wrapper
gematria-hive integrity
gh integrity
```

### Output

```
🔍 ========================================
🔍 Baseline Integrity Check
🔍 ========================================

📁 1. Checking required files...
✅ README.md
✅ requirements.txt
✅ docker-compose.yml
...

📊 Integrity Check Summary
✅ Baseline integrity: PASSED
   All checks passed
```

---

## 🛡️ System Wrapper

The system wrapper provides a unified interface for all commands with automatic baseline checks.

### Usage

```bash
# All commands run through wrapper
./scripts/system_wrapper.sh run kanban
./scripts/system_wrapper.sh test all
./scripts/system_wrapper.sh commit "feat: message"
./scripts/system_wrapper.sh status system
./scripts/system_wrapper.sh integrity
```

### Features

- **Automatic Baseline Checks** - Runs before commands
- **Error Handling** - Graceful failure handling
- **Status Reporting** - Clear status messages
- **System Agnostic** - Works on macOS, Linux, Windows (WSL)

---

## 🔄 Integration with Auto-Commit

The baseline integrity check is automatically run:
- Before auto-commit (via system wrapper)
- Before critical operations
- On demand via `gh integrity`

---

## 📝 Completion Examples

### Bash

```bash
# Type and press TAB
gematria-hive run <TAB>
# Shows: kanban internal-api agents ingestion pipeline

gematria-hive test <TAB>
# Shows: all agents core integration api kanban

gematria-hive commit <TAB>
# Shows: feat: fix: docs: refactor: test: chore:
```

### Zsh

```bash
# Type and press TAB
gematria-hive run <TAB>
# Shows menu with descriptions

gematria-hive test <TAB>
# Shows menu with descriptions
```

---

## 🚀 Quick Start

1. **Install Completion:**
   ```bash
   ./scripts/completion_setup.sh
   source ~/.bashrc  # or ~/.zshrc
   ```

2. **Test Completion:**
   ```bash
   gematria-hive <TAB>
   ```

3. **Run Integrity Check:**
   ```bash
   gh integrity
   ```

4. **Use Commands:**
   ```bash
   gh run kanban
   gh test all
   gh status system
   ```

---

## 🔧 Troubleshooting

### Completion Not Working

```bash
# Reinstall completion
./scripts/completion_setup.sh
source ~/.bashrc  # or ~/.zshrc

# Check completion file
ls ~/.bash_completion.d/gematria-hive  # bash
ls ~/.zsh/completions/gematria-hive    # zsh
```

### Integrity Check Fails

```bash
# Run with verbose output
./scripts/baseline_integrity.sh

# Fix missing files
# Fix missing dependencies
# Fix configuration issues
```

---

## 📚 Files

- `scripts/completion_setup.sh` - Setup script
- `scripts/completion.bash` - Bash completion
- `scripts/completion.zsh` - Zsh completion
- `scripts/baseline_integrity.sh` - Integrity check
- `scripts/system_wrapper.sh` - System wrapper

---

**Remember:** Always run integrity check before critical operations! 🐝✨

