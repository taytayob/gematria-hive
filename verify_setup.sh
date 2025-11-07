#!/bin/zsh
# Gematria Hive - Complete Setup Verification Script
# Run this in Cursor terminal to verify everything is configured correctly

echo "============================================================"
echo "Gematria Hive - Complete Setup Verification"
echo "============================================================"
echo ""

# Check Shell
echo "📋 Checking Shell..."
echo "  Shell: $SHELL"
zsh --version
echo ""

# Check Python
echo "🐍 Checking Python..."
if command -v python &> /dev/null; then
    PYTHON_PATH=$(which python)
    PYTHON_VERSION=$(python --version 2>&1)
    echo "  ✅ Python found: $PYTHON_PATH"
    echo "  ✅ Version: $PYTHON_VERSION"
else
    echo "  ❌ Python not found in PATH"
fi
echo ""

# Check Conda
echo "🔧 Checking Conda..."
if command -v conda &> /dev/null; then
    CONDA_PATH=$(which conda)
    CONDA_VERSION=$(conda --version)
    echo "  ✅ Conda found: $CONDA_PATH"
    echo "  ✅ Version: $CONDA_VERSION"
else
    echo "  ❌ Conda not found in PATH"
fi
echo ""

# Check Conda Environment
echo "🌍 Checking Conda Environment..."
if conda env list | grep -q "gematria_env"; then
    echo "  ✅ gematria_env environment exists"
    conda env list | grep gematria_env
else
    echo "  ❌ gematria_env environment not found"
fi
echo ""

# Activate and Check Environment
echo "🔌 Activating gematria_env..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate gematria_env 2>/dev/null || echo "  ⚠️  Could not activate (may need manual activation)"

if [ "$CONDA_DEFAULT_ENV" = "gematria_env" ]; then
    echo "  ✅ Environment activated: $CONDA_DEFAULT_ENV"
    echo "  ✅ Python: $(which python)"
    echo "  ✅ Python Version: $(python --version 2>&1)"
else
    echo "  ⚠️  Environment not activated (run: conda activate gematria_env)"
fi
echo ""

# Check Streamlit
echo "📊 Checking Streamlit..."
if command -v streamlit &> /dev/null; then
    STREAMLIT_PATH=$(which streamlit)
    STREAMLIT_VERSION=$(streamlit --version 2>&1 | head -1)
    echo "  ✅ Streamlit found: $STREAMLIT_PATH"
    echo "  ✅ Version: $STREAMLIT_VERSION"
else
    echo "  ❌ Streamlit not found"
fi
echo ""

# Check Python Packages
echo "📦 Checking Python Packages..."
if [ "$CONDA_DEFAULT_ENV" = "gematria_env" ]; then
    python - <<'PYCODE'
import sys

packages = {
    'streamlit': 'streamlit',
    'pandas': 'pandas',
    'numpy': 'numpy',
    'supabase': 'supabase',
    'sentence-transformers': 'sentence_transformers',
    'transformers': 'transformers',
    'langchain': 'langchain',
    'pixeltable': 'pixeltable',
    'stringzilla': 'stringzilla',
    'simsimd': 'simsimd',
    'requests': 'requests',
    'beautifulsoup4': 'bs4',
    'opencv-python': 'cv2',
    'pytesseract': 'pytesseract',
    'Pillow': 'PIL',
    'qiskit': 'qiskit'
}

missing = []

for display_name, module_name in packages.items():
    try:
        __import__(module_name)
        print(f"  ✅ {display_name}")
    except ImportError:
        print(f"  ❌ {display_name} - MISSING")
        missing.append(display_name)

if missing:
    print(f"\n  ⚠️  Missing packages: {', '.join(missing)}")
    sys.exit(1)
else:
    print("\n  ✅ All packages installed!")
PYCODE
else
    echo "  ⚠️  Activate conda environment first: conda activate gematria_env"
fi
echo ""

# Check Git
echo "🔀 Checking Git..."
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    echo "  ✅ Git found: $GIT_VERSION"
    echo "  ✅ Current branch: $(git branch --show-current 2>/dev/null || echo 'unknown')"
    echo "  ✅ Git status:"
    git status --short 2>/dev/null | head -5 || echo "    (no changes)"
else
    echo "  ❌ Git not found"
fi
echo ""

# Check Cursor Configuration
echo "⚙️  Checking Cursor Configuration..."
if [ -f ".vscode/settings.json" ]; then
    echo "  ✅ .vscode/settings.json exists"
    if grep -q "gematria_env" .vscode/settings.json; then
        echo "  ✅ Conda environment configured in Cursor"
        grep "python.defaultInterpreterPath" .vscode/settings.json
    else
        echo "  ⚠️  Conda environment not configured in Cursor settings"
    fi
else
    echo "  ⚠️  .vscode/settings.json not found"
fi
echo ""

# Check Project Files
echo "📁 Checking Project Files..."
files=("app.py" "ingest_pass1.py" "requirements.txt" "environment.yml")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file exists"
    else
        echo "  ❌ $file missing"
    fi
done
echo ""

# Summary
echo "============================================================"
echo "Verification Complete!"
echo "============================================================"
echo ""
echo "Next Steps:"
echo "1. If conda environment not activated: conda activate gematria_env"
echo "2. Verify Python interpreter in Cursor: Cmd+Shift+P → Python: Select Interpreter"
echo "3. Test Streamlit: streamlit run app.py"
echo "4. Check git status: git status"
echo ""

