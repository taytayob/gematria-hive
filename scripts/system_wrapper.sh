#!/bin/bash
# System-agnostic wrapper for Gematria Hive commands
# Provides autocompletion and baseline integrity checks

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Run baseline integrity check before commands
run_baseline_check() {
    if [ -f "$SCRIPT_DIR/baseline_integrity.sh" ]; then
        echo -e "${YELLOW}🔍 Running baseline integrity check...${NC}"
        "$SCRIPT_DIR/baseline_integrity.sh" || {
            echo -e "${YELLOW}⚠️  Baseline check failed, but continuing...${NC}"
        }
        echo ""
    fi
}

# Main command handler
case "$1" in
    run)
        run_baseline_check
        case "$2" in
            kanban)
                echo "🚀 Starting Kanban API..."
                cd "$PROJECT_ROOT" && python run_kanban.py
                ;;
            internal-api)
                echo "🚀 Starting Internal API..."
                cd "$PROJECT_ROOT" && python run_internal_api.py
                ;;
            agents)
                echo "🚀 Starting Agents..."
                cd "$PROJECT_ROOT" && python run_agents.py
                ;;
            ingestion)
                echo "🚀 Starting Ingestion Pipeline..."
                cd "$PROJECT_ROOT" && python run_ingestion_pipeline.py
                ;;
            pipeline)
                echo "🚀 Starting Full Pipeline..."
                cd "$PROJECT_ROOT" && python execute_critical_path.py
                ;;
            *)
                echo "Usage: $0 run [kanban|internal-api|agents|ingestion|pipeline]"
                exit 1
                ;;
        esac
        ;;
    test)
        run_baseline_check
        case "$2" in
            all)
                echo "🧪 Running all tests..."
                cd "$PROJECT_ROOT" && python run_tests.py
                ;;
            agents)
                echo "🧪 Running agent tests..."
                cd "$PROJECT_ROOT" && python -m pytest tests/test_agents.py -v
                ;;
            core)
                echo "🧪 Running core tests..."
                cd "$PROJECT_ROOT" && python -m pytest tests/test_core.py -v
                ;;
            integration)
                echo "🧪 Running integration tests..."
                cd "$PROJECT_ROOT" && python -m pytest tests/test_integration.py -v
                ;;
            api)
                echo "🧪 Running API tests..."
                cd "$PROJECT_ROOT" && python test_internal_api.py
                ;;
            kanban)
                echo "🧪 Running Kanban tests..."
                cd "$PROJECT_ROOT" && python test_enhanced_kanban.py
                ;;
            *)
                echo "Usage: $0 test [all|agents|core|integration|api|kanban]"
                exit 1
                ;;
        esac
        ;;
    commit)
        run_baseline_check
        if [ -z "$2" ]; then
            echo "Usage: $0 commit 'type: message'"
            exit 1
        fi
        echo "💾 Committing changes..."
        cd "$PROJECT_ROOT" && "$SCRIPT_DIR/auto_commit.sh" "$2"
        ;;
    status)
        case "$2" in
            git)
                echo "🌿 Git Status:"
                cd "$PROJECT_ROOT" && git status
                ;;
            system)
                echo "🔧 System Status:"
                "$SCRIPT_DIR/generate_status.sh"
                ;;
            services)
                echo "🔧 Service Status:"
                echo "Internal API: $(curl -s http://localhost:8001/internal/health 2>/dev/null | grep -q 'healthy' && echo '✅ Running' || echo '❌ Not running')"
                echo "Kanban API: $(curl -s http://localhost:8000/health 2>/dev/null | grep -q 'healthy' && echo '✅ Running' || echo '❌ Not running')"
                ;;
            agents)
                echo "🤖 Agent Status:"
                cd "$PROJECT_ROOT" && python -c "
import sys
sys.path.insert(0, '.')
from agents.orchestrator import MCPOrchestrator
orchestrator = MCPOrchestrator()
print(f'Total Agents: {len(orchestrator.agents)}')
for name in orchestrator.agents.keys():
    print(f'  - {name}')
" 2>/dev/null || echo "⚠️  Could not load agents"
                ;;
            *)
                echo "Usage: $0 status [git|system|services|agents]"
                exit 1
                ;;
        esac
        ;;
    integrity)
        echo "🔍 Running baseline integrity check..."
        "$SCRIPT_DIR/baseline_integrity.sh"
        ;;
    *)
        echo "Gematria Hive - System Wrapper"
        echo ""
        echo "Usage: $0 [command] [options]"
        echo ""
        echo "Commands:"
        echo "  run [service]     - Run services (kanban, internal-api, agents, ingestion, pipeline)"
        echo "  test [type]       - Run tests (all, agents, core, integration, api, kanban)"
        echo "  commit [message]  - Commit changes with message"
        echo "  status [type]     - Check status (git, system, services, agents)"
        echo "  integrity         - Run baseline integrity check"
        echo ""
        echo "Examples:"
        echo "  $0 run kanban"
        echo "  $0 test all"
        echo "  $0 commit 'feat: Add new feature'"
        echo "  $0 status system"
        echo "  $0 integrity"
        exit 1
        ;;
esac

