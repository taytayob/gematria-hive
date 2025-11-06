#!/bin/bash
# Run Streamlit app with proper venv activation

cd "$(dirname "$0")"
source venv/bin/activate
streamlit run app.py

