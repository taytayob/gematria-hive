#!/usr/bin/env python3
"""
Run Kanban Board

Simple script to start the kanban API server.

Usage:
    python run_kanban.py [--port PORT] [--host HOST]

Author: Gematria Hive Team
Date: January 6, 2025
"""

import argparse
import uvicorn
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Start Gematria Hive Kanban Board",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start on default port (8000)
  python run_kanban.py
  
  # Start on custom port
  python run_kanban.py --port 8080
  
  # Start on custom host and port
  python run_kanban.py --host 0.0.0.0 --port 8080
        """
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on (default: 8000)"
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🐝 Gematria Hive - Kanban Board")
    print("=" * 60)
    print(f"Starting server on http://{args.host}:{args.port}")
    print(f"Open in browser: http://localhost:{args.port}")
    print("=" * 60)
    print()
    
    uvicorn.run(
        "kanban_api:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )


if __name__ == "__main__":
    main()

