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

# Summary
echo "============================================================"
echo "Setup Complete!"
echo "============================================================"
echo ""
echo "Next Steps:"
echo "1. Set SUPABASE_URL and SUPABASE_KEY in Replit Secrets"
echo "2. Run database setup: python setup_database.py"
echo "3. Run migrations in Supabase Dashboard SQL Editor"
echo "4. Test Streamlit: streamlit run app.py --server.port 5000"
echo ""
echo "Ready to go! 🐝✨"
echo ""

