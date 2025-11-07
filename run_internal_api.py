#!/usr/bin/env python3
"""
Run Internal API Server

Simple script to start the internal API server.

Usage:
    python run_internal_api.py [--port PORT] [--host HOST]

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
        description="Start Gematria Hive Internal API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start on default port (8001)
  python run_internal_api.py
  
  # Start on custom port
  python run_internal_api.py --port 8081
  
  # Start on custom host and port
  python run_internal_api.py --host 0.0.0.0 --port 8081
        """
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("INTERNAL_API_PORT", "8001")),
        help="Port to run the server on (default: 8001)"
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default=os.getenv("INTERNAL_API_HOST", "0.0.0.0"),
        help="Host to bind to (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )
    
    args = parser.parse_args()
    
    # Check for API key
    api_key = os.getenv("INTERNAL_API_KEY", "internal-api-key-change-in-production")
    if api_key == "internal-api-key-change-in-production":
        print("⚠️  WARNING: Using default API key. Set INTERNAL_API_KEY environment variable for production!")
    
    print("=" * 60)
    print("🐝 Gematria Hive - Internal API")
    print("=" * 60)
    print(f"Starting internal API on http://{args.host}:{args.port}")
    print(f"API Key: {'*' * 20} (set INTERNAL_API_KEY to customize)")
    print("=" * 60)
    print()
    print("Available endpoints:")
    print("  GET  /internal/health - Health check (no auth)")
    print("  GET  /internal/agents - List agents (requires auth)")
    print("  POST /internal/agents/{name}/execute - Execute agent (requires auth)")
    print("  GET  /internal/tools - List tools (requires auth)")
    print("  POST /internal/tools/{name}/execute - Execute tool (requires auth)")
    print("  GET  /internal/cost/current - Get current cost (requires auth)")
    print("=" * 60)
    print()
    
    uvicorn.run(
        "internal_api:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )


if __name__ == "__main__":
    main()

