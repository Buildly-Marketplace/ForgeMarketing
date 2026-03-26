#!/usr/bin/env python3
"""
Mastodon Setup Helper
====================

Helper script to set up Mastodon API access tokens for automated posting.
This script will guide you through the process of creating Mastodon applications
and obtaining the necessary access tokens.

For the accounts you mentioned:
- https://mastodon.social/@buildly
- https://mastodon.social/@buildly@cloud-native.social (This appears to be a mention format)
- https://mastodon.social/@glind

Note: @buildly@cloud-native.social suggests the buildly account is on cloud-native.social, 
not mastodon.social.
"""

import os
import json
from pathlib import Path

def print_setup_instructions():
    """Print detailed setup instructions for Mastodon API access"""
    
    print("🐘 MASTODON API SETUP INSTRUCTIONS")
    print("=" * 50)
    print()
    
    print("You have four Mastodon accounts to configure:")
    print("1. @buildly on mastodon.social")
    print("2. @buildly on cloud-native.social") 
    print("3. @openbuild on mastodon.social")
    print("4. @glind on mastodon.social")
    print()
    
    print("📋 SETUP STEPS FOR EACH ACCOUNT:")
    print("-" * 30)
    print()
    
    accounts = [
        {
            'name': 'Buildly (mastodon.social)',
            'instance': 'https://mastodon.social',
            'username': '@buildly',
            'env_prefix': 'MASTODON_BUILDLY'
        },
        {
            'name': 'Buildly (cloud-native.social)',
            'instance': 'https://cloud-native.social', 
            'username': '@buildly',
            'env_prefix': 'MASTODON_CLOUDNATIVE'
        },
        {
            'name': 'Personal (@glind)',
            'instance': 'https://mastodon.social',
            'username': '@glind', 
            'env_prefix': 'MASTODON_PERSONAL'
        },
        {
            'name': 'Open Build (@openbuild)',
            'instance': 'https://mastodon.social',
            'username': '@openbuild',
            'env_prefix': 'MASTODON_OPENBUILD'
        }
    ]
    
    for i, account in enumerate(accounts, 1):
        print(f"{i}. {account['name']}")
        print(f"   Instance: {account['instance']}")
        print(f"   Username: {account['username']}")
        print()
        print("   Steps:")
        print(f"   a) Go to {account['instance']}/settings/applications")
        print("   b) Click 'New Application'")
        print("   c) Fill in the form:")
        print("      - Application name: 'Marketing Automation Bot'")
        print("      - Application website: 'https://buildly.io'")
        print("      - Scopes: Check 'write:statuses'")
        print("   d) Click 'Submit'")
        print("   e) Copy the 'Your access token' value")
        print(f"   f) Add to .env file: {account['env_prefix']}_ACCESS_TOKEN=your_token_here")
        print()
    
    print("🔧 ENVIRONMENT CONFIGURATION:")
    print("-" * 30)
    print("Add these lines to your .env file:")
    print()
    
    for account in accounts:
        print(f"# {account['name']}")
        print(f"{account['env_prefix']}_INSTANCE={account['instance']}")
        print(f"{account['env_prefix']}_ACCESS_TOKEN=")
        print(f"{account['env_prefix']}_USERNAME={account['username']}")
        print()
    
    print("📝 TESTING:")
    print("-" * 30)
    print("After configuration, test with:")
    print("python3 automation/article_publisher.py")
    print()
    
    print("🤖 AUTOMATION:")
    print("-" * 30)
    print("The system will automatically:")
    print("• Scan for new articles every 6 hours")
    print("• Generate platform-appropriate content")
    print("• Post to LinkedIn, Bluesky, and Mastodon")
    print("• Track publication history to avoid duplicates")
    print("• Log all activities for monitoring")
    print()

def generate_env_template():
    """Generate a template .env section for Mastodon configuration"""
    
    template = """
# ==============================================
# MASTODON SOCIAL MEDIA CONFIGURATION
# ==============================================

# Mastodon - Buildly (mastodon.social)
MASTODON_BUILDLY_INSTANCE=https://mastodon.social
MASTODON_BUILDLY_ACCESS_TOKEN=
MASTODON_BUILDLY_USERNAME=@buildly

# Mastodon - Buildly (cloud-native.social)  
MASTODON_CLOUDNATIVE_INSTANCE=https://cloud-native.social
MASTODON_CLOUDNATIVE_ACCESS_TOKEN=
MASTODON_CLOUDNATIVE_USERNAME=@buildly

# Mastodon - Personal (@glind)
MASTODON_PERSONAL_INSTANCE=https://mastodon.social
MASTODON_PERSONAL_ACCESS_TOKEN=
MASTODON_PERSONAL_USERNAME=@glind

# Social Media Automation Settings
SOCIAL_POSTING_ENABLED=true
SOCIAL_POSTING_PLATFORMS=linkedin,bluesky,mastodon
SOCIAL_POSTING_DELAY_SECONDS=5
"""
    
    print("📄 ENVIRONMENT TEMPLATE:")
    print("=" * 30)
    print(template)
    
    # Save to file for easy copying
    template_file = Path(__file__).parent.parent / 'mastodon_env_template.txt'
    with open(template_file, 'w') as f:
        f.write(template)
    
    print(f"💾 Template saved to: {template_file}")

def check_current_config():
    """Check current Mastodon configuration in environment"""
    
    print("🔍 CURRENT CONFIGURATION CHECK:")
    print("=" * 35)
    
    from dotenv import load_dotenv
    load_dotenv()
    
    configs = [
        ('MASTODON_BUILDLY_ACCESS_TOKEN', 'Buildly (mastodon.social)'),
        ('MASTODON_CLOUDNATIVE_ACCESS_TOKEN', 'Buildly (cloud-native.social)'),
        ('MASTODON_PERSONAL_ACCESS_TOKEN', 'Personal (@glind)')
    ]
    
    for env_var, description in configs:
        value = os.getenv(env_var)
        status = "✅ Configured" if value else "❌ Missing"
        token_preview = f"({value[:10]}...)" if value else ""
        print(f"{description}: {status} {token_preview}")
    
    print()
    
    # Check if social posting is enabled
    social_enabled = os.getenv('ENABLE_SOCIAL_POSTING', 'false').lower() == 'true'
    print(f"Social posting enabled: {'✅' if social_enabled else '❌'} {social_enabled}")

def main():
    """Main setup function"""
    print_setup_instructions()
    print("\n" + "=" * 60 + "\n")
    generate_env_template()
    print("\n" + "=" * 60 + "\n")
    
    try:
        check_current_config()
    except ImportError:
        print("❌ python-dotenv not available for config check")
    
    print()
    print("🚀 QUICK START:")
    print("1. Follow the setup steps above to get Mastodon access tokens")
    print("2. Add the tokens to your .env file")
    print("3. Test with: python3 automation/article_publisher.py")
    print("4. The automation will run every 6 hours via cron")

if __name__ == "__main__":
    main()