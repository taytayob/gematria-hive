#!/usr/bin/env python3
"""
Complete Setup Script - Gematria Hive

Purpose: Automate all possible setup steps
- Check current configuration
- Guide through manual steps
- Test integrations

Usage:
    python scripts/complete_setup.py

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

load_dotenv()


def check_env_var(var_name, description):
    """Check if environment variable is set"""
    value = os.getenv(var_name)
    if value and value not in ['', 'NOT SET', 'your-key-here', 'your-client-id', 'your-client-secret']:
        print(f"  ✅ {var_name}: SET")
        return True
    else:
        print(f"  ❌ {var_name}: NOT SET - {description}")
        return False


def test_agent(agent_name, test_func, description):
    """Test an agent"""
    try:
        result = test_func()
        if result:
            print(f"  ✅ {agent_name}: OK")
            return True
        else:
            print(f"  ❌ {agent_name}: {description}")
            return False
    except Exception as e:
        print(f"  ⚠️  {agent_name}: Error - {e}")
        return False


def main():
    """Main setup function"""
    print("=" * 70)
    print("Gematria Hive - Complete Setup Status")
    print("=" * 70)
    print()
    
    # Check critical variables
    print("📋 Environment Variables Status:")
    print("-" * 70)
    
    critical_vars = {
        'SUPABASE_URL': 'Database connection',
        'SUPABASE_KEY': 'Database authentication',
        'INTERNAL_API_KEY': 'Internal API authentication'
    }
    
    critical_ok = True
    for var, desc in critical_vars.items():
        if not check_env_var(var, desc):
            critical_ok = False
    
    print()
    
    # Check high priority variables
    print("🔴 High Priority API Keys:")
    print("-" * 70)
    
    high_priority_vars = {
        'GOOGLE_API_KEY': 'Google Gemini API - Get from https://ai.google.dev',
        'GOOGLE_DRIVE_CLIENT_ID': 'Google Drive OAuth - Get from https://console.cloud.google.com',
        'GOOGLE_DRIVE_CLIENT_SECRET': 'Google Drive OAuth - Get from https://console.cloud.google.com',
        'GOOGLE_DRIVE_REFRESH_TOKEN': 'Google Drive OAuth - Run: python scripts/setup_google_drive_oauth.py'
    }
    
    high_priority_ok = True
    for var, desc in high_priority_vars.items():
        if not check_env_var(var, desc):
            high_priority_ok = False
    
    print()
    
    # Check medium priority variables
    print("🟢 Medium Priority API Keys (Optional):")
    print("-" * 70)
    
    medium_priority_vars = {
        'ANTHROPIC_API_KEY': 'Anthropic Claude API - Requires payment',
        'PERPLEXITY_API_KEY': 'Perplexity API - Requires payment',
        'GROK_API_KEY': 'Grok/X.ai API - Requires payment'
    }
    
    for var, desc in medium_priority_vars.items():
        check_env_var(var, desc)
    
    print()
    
    # Test agents
    print("🧪 Agent Integration Tests:")
    print("-" * 70)
    
    # Test Gemini
    try:
        from agents.gemini_research import GeminiResearchAgent
        gemini_agent = GeminiResearchAgent()
        test_agent('Gemini Research', lambda: gemini_agent.model is not None, 'Need GOOGLE_API_KEY')
    except Exception as e:
        print(f"  ⚠️  Gemini Research: Not available - {e}")
    
    # Test Drive
    try:
        from agents.google_drive_integrator import GoogleDriveIntegratorAgent
        drive_agent = GoogleDriveIntegratorAgent()
        test_agent('Google Drive', lambda: drive_agent.service is not None, 'Need OAuth credentials')
    except Exception as e:
        print(f"  ⚠️  Google Drive: Not available - {e}")
    
    # Test Claude
    try:
        from agents.claude_integrator import ClaudeIntegratorAgent
        claude_agent = ClaudeIntegratorAgent()
        test_agent('Claude Integrator', lambda: claude_agent.client is not None, 'Need ANTHROPIC_API_KEY')
    except Exception as e:
        print(f"  ⚠️  Claude Integrator: Not available - {e}")
    
    # Test Perplexity
    try:
        from agents.perplexity_integrator import PerplexityIntegratorAgent
        perplexity_agent = PerplexityIntegratorAgent()
        test_agent('Perplexity', lambda: os.getenv('PERPLEXITY_API_KEY') is not None, 'Need PERPLEXITY_API_KEY')
    except Exception as e:
        print(f"  ⚠️  Perplexity: Not available - {e}")
    
    # Test Grok
    try:
        from agents.twitter_fetcher import TwitterFetcherAgent
        grok_agent = TwitterFetcherAgent()
        test_agent('Grok/Twitter', lambda: grok_agent.api_key is not None, 'Need GROK_API_KEY')
    except Exception as e:
        print(f"  ⚠️  Grok/Twitter: Not available - {e}")
    
    print()
    print("=" * 70)
    print("📊 Setup Summary:")
    print("=" * 70)
    print()
    
    if critical_ok:
        print("✅ Critical configuration: OK")
    else:
        print("❌ Critical configuration: INCOMPLETE")
    
    if high_priority_ok:
        print("✅ High priority APIs: OK")
    else:
        print("⚠️  High priority APIs: INCOMPLETE")
        print("   See: BROWSER_SETUP_GUIDE.md for setup instructions")
        print("   See: PAYMENT_SUBSCRIPTION_GUIDE.md for payment requirements")
    
    print()
    print("=" * 70)
    print("📚 Documentation:")
    print("=" * 70)
    print()
    print("  • BROWSER_SETUP_GUIDE.md - Complete browser setup guide")
    print("  • PAYMENT_SUBSCRIPTION_GUIDE.md - Payment requirements")
    print("  • COMPLETE_API_KEYS_CHECKLIST.md - Full API keys checklist")
    print("  • SETUP_COMPLETE_GUIDE.md - Setup guide with links")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

