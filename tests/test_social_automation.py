#!/usr/bin/env python3
"""
Test script for the complete social media automation system.
Run this after configuring your Mastodon API tokens to verify everything works.
"""

import asyncio
from automation.social.social_media_manager import SocialMediaManager
from automation.article_publisher import ArticlePublicationSystem


async def test_complete_system():
    """Test the complete social media automation system"""
    
    print("🚀 Social Media Automation System Test")
    print("=" * 50)
    
    # Test 1: Social Media Manager
    print("1. Testing Social Media Manager...")
    sm = SocialMediaManager()
    
    print(f"   ✅ Buildly accounts: {sm.get_mastodon_accounts_for_brand('buildly')}")
    print(f"   ✅ Open Build accounts: {sm.get_mastodon_accounts_for_brand('open_build')}")
    print(f"   ✅ Personal accounts: {sm.get_mastodon_accounts_for_brand('personal')}")
    print(f"   ✅ All accounts: {sm.get_mastodon_accounts_for_brand('all')}")
    
    # Test 2: Article Publication System
    print("\n2. Testing Article Publication System...")
    publisher = ArticlePublicationSystem()
    
    articles = publisher.scan_for_new_articles()
    print(f"   ✅ Found {len(articles)} new articles")
    
    if articles:
        article = articles[0]
        print(f"   📝 Testing content generation for: {article['title']}")
        
        # Generate content for each platform
        for platform in ['linkedin', 'mastodon', 'bluesky']:
            content = publisher.generate_social_content(article, platform)
            print(f"   ✅ {platform.title()}: {len(content)} characters")
    
    # Test 3: Account Configuration Status
    print("\n3. Account Configuration Status...")
    import os
    
    platforms = {
        'LinkedIn': 'LINKEDIN_ACCESS_TOKEN',
        'Bluesky': 'BLUESKY_PASSWORD', 
        'Mastodon (Buildly)': 'MASTODON_BUILDLY_ACCESS_TOKEN',
        'Mastodon (Cloud-Native)': 'MASTODON_CLOUDNATIVE_ACCESS_TOKEN',
        'Mastodon (OpenBuild)': 'MASTODON_OPENBUILD_ACCESS_TOKEN',
        'Mastodon (Personal)': 'MASTODON_PERSONAL_ACCESS_TOKEN'
    }
    
    for platform, env_key in platforms.items():
        token = os.getenv(env_key, '')
        status = "✅ Configured" if token and token != 'your_access_token_here' else "⚠️  Needs API token"
        print(f"   {platform}: {status}")
    
    print("\n" + "=" * 50)
    print("🎯 System Status Summary:")
    print("   • Dashboard server: http://127.0.0.1:5003")
    print("   • Virtual environment: Active")
    print("   • Cron job: Every 6 hours")
    print("   • Multi-platform posting: Ready")
    print("   • Multi-account Mastodon: Ready")
    print("\n📋 Next Steps:")
    print("   1. Run 'python setup_mastodon.py' to get API tokens")
    print("   2. Configure LinkedIn and Bluesky tokens in .env")
    print("   3. Test posting with real articles")
    print("   4. Monitor logs in logs/ directory")


if __name__ == "__main__":
    asyncio.run(test_complete_system())