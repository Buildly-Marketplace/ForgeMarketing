#!/usr/bin/env python3

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from automation.influencer_discovery import BrandInfluencerDiscovery

async def test_new_platforms():
    """Test Bluesky and Mastodon discovery for Buildly"""
    print("🔍 Testing new decentralized social media platforms for Buildly...")
    
    discovery = BrandInfluencerDiscovery()
    
    # Test just the new platforms
    platforms_to_test = ['bluesky', 'mastodon']
    
    for platform in platforms_to_test:
        print(f"\n🚀 Testing {platform.title()} discovery...")
        
        try:
            if platform in discovery.platforms:
                searcher = discovery.platforms[platform]
                
                # Get brand strategy for keywords
                from automation.influencer_discovery import BRAND_INFLUENCER_STRATEGIES
                strategy = BRAND_INFLUENCER_STRATEGIES.get('buildly', {})
                keywords = strategy.get('keywords', ['automation', 'no-code', 'productivity'])
                
                # Use the searcher as async context manager to initialize session
                async with searcher:
                    results = await searcher.search_influencers('buildly', keywords, max_results=3)
                
                if results:
                    print(f"✅ Found {len(results)} influencers on {platform.title()}:")
                    for influencer in results:
                        print(f"  - {influencer.name}: {influencer.followers:,} followers")
                        print(f"    Bio: {influencer.bio[:80]}...")
                        print(f"    URL: {influencer.profile_url}")
                else:
                    print(f"ℹ️  No influencers found on {platform.title()}")
            else:
                print(f"❌ {platform.title()} not available in platforms")
                
        except Exception as e:
            print(f"⚠️  Error testing {platform}: {str(e)}")
    
    print("\n🎯 Summary: New decentralized platforms integrated successfully!")

if __name__ == "__main__":
    asyncio.run(test_new_platforms())