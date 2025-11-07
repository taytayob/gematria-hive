#!/bin/bash
# Replit Setup Script - Gematria Hive
# Complete setup for Replit environment

set -e  # Exit on error

echo "============================================================"
echo "Gematria Hive - Replit Setup"
echo "============================================================"
echo ""

# Check Python version
echo "🐍 Checking Python version..."
python3 --version
echo ""

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip
echo ""

# Install dependencies
echo "📦 Installing dependencies from requirements.txt..."
pip install -r requirements.txt
echo ""

# Verify critical packages
echo "✅ Verifying critical packages..."
python3 -c "
import sys
packages = {
    'streamlit': 'streamlit',
    'pandas': 'pandas',
    'supabase': 'supabase',
    'sentence-transformers': 'sentence_transformers',
    'langchain': 'langchain',
    'langgraph': 'langgraph',
    'pixeltable': 'pixeltable'
}

missing = []
for display_name, module_name in packages.items():
    try:
        __import__(module_name)
        print(f'  ✅ {display_name}')
    except ImportError:
        print(f'  ❌ {display_name} - MISSING')
        missing.append(display_name)

if missing:
    print(f'\n⚠️  Missing packages: {missing}')
    print('   Run: pip install ' + ' '.join(missing))
    sys.exit(1)
else:
    print('\n✅ All critical packages installed!')
"
echo ""

# Check environment variables
echo "🔑 Checking environment variables..."
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')

if url:
    print(f'  ✅ SUPABASE_URL set ({url[:30]}...)')
else:
    print('  ⚠️  SUPABASE_URL not set')
    print('     Set in Replit Secrets (lock icon) or .env file')

if key:
    print(f'  ✅ SUPABASE_KEY set ({key[:20]}...)')
else:
    print('  ⚠️  SUPABASE_KEY not set')
    print('     Set in Replit Secrets (lock icon) or .env file')
"
echo ""

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x scripts/*.py 2>/dev/null || true
chmod +x run_*.py 2>/dev/null || true
echo ""

# Test MCP and agent integration
echo "🔧 Testing MCP and agent integration..."
python3 -c "
import sys
sys.path.insert(0, '.')

try:
    from agents.mcp_tool_registry import get_tool_registry
    from agents.orchestrator import MCPOrchestrator
    
    # Test tool registry
    registry = get_tool_registry()
    tools = registry.list_all_tools()
    print(f'  ✅ MCP Tool Registry: {tools.get(\"total_tools\", 0)} tools registered')
    
    # Test orchestrator
    orchestrator = MCPOrchestrator()
    agent_count = len(orchestrator.agents)
    print(f'  ✅ MCP Orchestrator: {agent_count} agents initialized')
    
    # Test internal API
    from internal_api import app, tool_registry, orchestrator as api_orchestrator
    print(f'  ✅ Internal API: Ready')
    print(f'  ✅ Internal API - Tool Registry: {len(tool_registry.tools) if tool_registry else 0} tools')
    print(f'  ✅ Internal API - Orchestrator: {len(api_orchestrator.agents) if api_orchestrator else 0} agents')
    
    print('\n✅ MCP and agent integration verified!')
except Exception as e:
    print(f'  ⚠️  MCP/Agent integration test failed: {e}')
    print('     This is expected if dependencies are not installed')
"
echo ""

# Summary
echo "============================================================"
echo "Setup Complete!"
echo "============================================================"
echo ""
echo "Next Steps:"
echo "1. Set SUPABASE_URL and SUPABASE_KEY in Replit Secrets"
echo "2. Set INTERNAL_API_KEY in Replit Secrets (optional)"
echo "3. Run database setup: python setup_database.py"
echo "4. Run migrations in Supabase Dashboard SQL Editor"
echo "5. Test services:"
echo "   - Kanban API: python run_kanban.py (port 8000)"
echo "   - Internal API: python run_internal_api.py (port 8001)"
echo "   - Streamlit: streamlit run app.py --server.port 5000"
echo ""
echo "Services:"
echo "  - Port 8000: Public Kanban API"
echo "  - Port 8001: Internal API (MCP & Agents)"
echo "  - Port 5000: Streamlit Dashboard"
echo ""
echo "Ready to go! 🐝✨"
echo ""

