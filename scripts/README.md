# Agent CLI Scripts

This directory contains standalone CLI scripts for running individual agents without the full application.

## Available Scripts

### `extract.py` - Extraction Agent
Extract data from various sources (JSON files, Dewey API, etc.)

```bash
# Extract from JSON file
python scripts/extract.py --source dewey_json.json

# Extract and save to output file
python scripts/extract.py --source data.json --output extracted.json

# Extract and print summary
python scripts/extract.py --source dewey_json.json --summary
```

**Options:**
- `--source`: Source file path or identifier (required)
- `--output`: Output file path (optional)
- `--format`: Output format (json, csv) - default: json
- `--summary`: Print summary statistics instead of full data
- `--verbose`: Enable verbose logging

### `distill.py` - Distillation Agent
Process extracted data, generate embeddings, and categorize relevance

```bash
# Process extracted data
python scripts/distill.py --input extracted.json --output processed.json

# Process with custom batch size
python scripts/distill.py --input extracted.json --output processed.json --batch-size 50
```

**Options:**
- `--input`: Input JSON file path (required)
- `--output`: Output JSON file path (required)
- `--batch-size`: Batch size for processing (default: 100)
- `--verbose`: Enable verbose logging

### `ingest.py` - Ingestion Agent
Ingest processed data into the database

```bash
# Ingest processed data
python scripts/ingest.py --input processed.json

# Ingest to specific table with custom batch size
python scripts/ingest.py --input processed.json --table gematria_words --batch-size 50
```

**Options:**
- `--input`: Input JSON file path (required)
- `--table`: Target table (bookmarks, gematria_words) - default: bookmarks
- `--batch-size`: Batch size for ingestion (default: 1000)
- `--verbose`: Enable verbose logging

### `browser.py` - Browser Agent
Scrape websites and extract content

```bash
# Scrape a single URL
python scripts/browser.py --url https://example.com

# Scrape with custom depth and save output
python scripts/browser.py --url https://example.com --max-depth 2 --output scraped.json
```

**Options:**
- `--url`: URL to scrape (required)
- `--max-depth`: Maximum crawl depth (default: 3)
- `--delay`: Delay between requests in seconds (default: 1.0)
- `--output`: Output JSON file path (optional)
- `--use-sitemap`: Use sitemap if available (default: True)
- `--respect-robots`: Respect robots.txt (default: True)
- `--verbose`: Enable verbose logging

## Usage Examples

### Complete Pipeline

```bash
# 1. Extract data
python scripts/extract.py --source dewey_json.json --output extracted.json

# 2. Process data
python scripts/distill.py --input extracted.json --output processed.json

# 3. Ingest to database
python scripts/ingest.py --input processed.json
```

### Standalone Operations

```bash
# Just extract
python scripts/extract.py --source data.json --summary

# Just scrape a website
python scripts/browser.py --url https://example.com --output scraped.json
```

## Making Scripts Executable

On Unix-like systems, make scripts executable:

```bash
chmod +x scripts/*.py
```

Then run directly:

```bash
./scripts/extract.py --source data.json
```

## Requirements

All scripts require:
- Python 3.12+
- Conda environment activated (`conda activate gematria_env`)
- Required dependencies installed (see `requirements.txt`)

## Error Handling

All scripts include error handling and will:
- Exit with code 1 on failure
- Log errors to stderr
- Provide helpful error messages

## Integration with Orchestrator

These scripts use the same agent classes as the MCP orchestrator, so they're fully compatible. You can:

1. Use scripts for standalone operations
2. Use orchestrator for full workflows
3. Mix and match as needed

For orchestrator usage, see `AGENT_SETUP.md` in the root directory.

