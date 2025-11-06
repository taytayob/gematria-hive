# Running Streamlit in Cursor - Complete Guide

## ✅ Solution: Multiple Ways to Run Streamlit

### Method 1: Using Cursor Tasks (Recommended)

1. **Open Command Palette**: `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. **Type**: `Tasks: Run Task`
3. **Select**: `Run Streamlit App` or `Activate Venv and Run Streamlit`

This will automatically use the venv and run Streamlit on port 5000.

### Method 2: Using the Shell Script

Simply run in Cursor's terminal:

```bash
./run_streamlit.sh
```

This script automatically:
- Navigates to the project directory
- Activates the venv
- Runs Streamlit

### Method 3: Manual Terminal Command

In Cursor's terminal:

```bash
source venv/bin/activate
streamlit run app.py
```

### Method 4: Direct Path (No Activation Needed)

```bash
venv/bin/streamlit run app.py
```

## 🔧 Cursor Configuration

The `.vscode/settings.json` file is configured to:
- Use the venv Python interpreter automatically
- Activate the venv in new terminals
- Set up proper Python paths

**To verify Cursor is using the right Python:**
1. Open any `.py` file
2. Check the bottom-right corner of Cursor - it should show: `Python 3.12.x ('venv': venv)`
3. If not, click it and select: `./venv/bin/python`

## 🚀 Quick Start

**Easiest way:**
1. Open Cursor
2. Press `Cmd+Shift+P` (or `Ctrl+Shift+P`)
3. Type: `Tasks: Run Task`
4. Select: `Run Streamlit App`
5. Streamlit will start on `http://localhost:5000`

## 📝 Troubleshooting

### Issue: "streamlit: command not found"
**Solution:** Make sure you're in the project directory and venv is activated:
```bash
cd /Users/cooperladd/Desktop/gematria-hive/gematria-hive
source venv/bin/activate
```

### Issue: "Port 5000 is already in use"
**Solution:** Kill the existing process:
```bash
lsof -ti :5000 | xargs kill -9
```

### Issue: Cursor not using venv Python
**Solution:** 
1. Press `Cmd+Shift+P` (or `Ctrl+Shift+P`)
2. Type: `Python: Select Interpreter`
3. Choose: `./venv/bin/python`

## ✅ Verification

After running, you should see:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:5000
```

Open `http://localhost:5000` in your browser to see the app.

---

**All methods are now configured and ready to use!** 🎉

