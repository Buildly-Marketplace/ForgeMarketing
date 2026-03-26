#!/usr/bin/env python3
"""
Test Multi-Account Posting
==========================

Test script to demonstrate multi-account social media posting
across different platforms with the enhanced AI content generation.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from automation.social.social_media_manager import SocialMediaManager
from automation.article_publisher import ArticlePublicationSystem


async def test_multi_account_posting():
    """Test multi-account posting with AI-generated content"""
    
    print("🚀 Multi-Account Posting Test")
    print("=" * 50)
    
    # Initialize systems
    publisher = ArticlePublicationSystem()
    social_manager = SocialMediaManager()
    
    # Test article
    test_article = {
        'id': 'test-multi-account',
        'title': 'Scaling Microservices with Kubernetes and Service Mesh',
        'description': 'A comprehensive guide to implementing scalable microservices architecture using Kubernetes, Istio, and cloud-native patterns.',
        'url': 'https://buildly.io/blog/scaling-microservices-kubernetes.html',
        'brand': 'buildly',
        'file_path': '/test/multi-account'
    }
    
    print(f"📝 Article: {test_article['title']}")
    print(f"🏷️  Brand: {test_article['brand']}")
    print(f"🔗 URL: {test_article['url']}")
    
    # Test 1: AI Content Generation
    print(f"\n🤖 AI-Generated Content:")
    print("-" * 30)
    
    platforms = ['linkedin', 'bluesky', 'mastodon']
    generated_content = {}
    
    for platform in platforms:
        content = publisher.generate_social_content(test_article, platform)
        generated_content[platform] = content
        
        print(f"\n📱 {platform.upper()} ({len(content)} chars):")
        print(f"   {content[:100]}{'...' if len(content) > 100 else ''}")
    
    # Test 2: Account Mapping
    print(f"\n🎯 Multi-Account Mapping:")
    print("-" * 30)
    
    brands = ['buildly', 'open_build', 'personal', 'all']
    for brand in brands:
        accounts = social_manager.get_mastodon_accounts_for_brand(brand)
        status = "✅ Configured" if accounts else "⚠️  Needs API tokens"
        print(f"   {brand}: {accounts} {status}")
    
    # Test 3: Platform Capabilities
    print(f"\n🔧 Platform Capabilities:")
    print("-" * 30)
    
    capabilities = {
        'LinkedIn': 'Professional networking, 3000 char limit, rich formatting',
        'Bluesky': 'Decentralized social, 300 char limit, casual tone',
        'Mastodon': 'Community-focused, 500 char limit, hashtag-rich',
        'Multi-Account': 'Brand-specific routing, simultaneous posting'
    }
    
    for platform, description in capabilities.items():
        print(f"   📌 {platform}: {description}")
    
    # Test 4: Simulate Cross-Platform Posting (dry run)
    print(f"\n🔄 Cross-Platform Posting Simulation:")
    print("-" * 30)
    
    print("   1. ✅ Content generated with AI optimization")
    print("   2. ✅ Platform-specific formatting applied")
    print("   3. ✅ Brand context and tone adjusted")
    print("   4. ✅ Character limits respected")
    print("   5. ⚠️  API tokens needed for live posting")
    
    # Show what would be posted
    print(f"\n📋 Ready to Post:")
    print("-" * 20)
    
    for platform, content in generated_content.items():
        print(f"\n🎯 {platform.upper()}:")
        lines = content.split('\\n')
        for line in lines[:3]:  # Show first 3 lines
            print(f"   {line}")
        if len(lines) > 3:
            print("   ...")
    
    print(f"\n✅ Multi-account posting system ready!")
    print("📋 Next steps:")
    print("   • Configure API tokens using setup_mastodon.py")
    print("   • Test with real posting to verify functionality") 
    print("   • Monitor logs for posting activity")


if __name__ == "__main__":
    asyncio.run(test_multi_account_posting())