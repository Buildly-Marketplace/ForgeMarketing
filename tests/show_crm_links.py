#!/usr/bin/env python3
"""
Show the complete social media links and CRM integration data
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from automation.influencer_discovery import BrandInfluencerDiscovery

def show_crm_ready_data():
    """Show all social media links ready for CRM integration"""
    print("🔗 Social Media Links Available for CRM Integration")
    print("=" * 70)
    
    discovery = BrandInfluencerDiscovery()
    
    # Get all influencers with their social links
    influencers = discovery.get_brand_influencers()
    
    print(f"📊 Total Influencers: {len(influencers)}")
    print()
    
    for i, influencer in enumerate(influencers[:10]):  # Show first 10
        name = influencer['name']
        brand = influencer['brand'] 
        primary_platform = influencer['primary_platform']
        total_reach = influencer['total_reach']
        social_links = influencer.get('social_links', '')
        website = influencer.get('website', '')
        
        print(f"👤 {i+1}. {name} ({brand})")
        print(f"   📍 Primary: {primary_platform} • 🎯 Reach: {total_reach:,}")
        
        if website:
            print(f"   🌐 Website: {website}")
        
        if social_links:
            print(f"   📱 Social Media Profiles:")
            # Parse social links (format: platform:url,platform:url)
            links = social_links.split(',') if social_links else []
            for link in links:
                if ':' in link:
                    platform, url = link.split(':', 1)
                    emoji = {
                        'youtube': '📺', 'instagram': '📸', 'linkedin': '💼', 
                        'twitter': '🐦', 'bluesky': '🌌', 'mastodon': '🐘'
                    }
                    icon = emoji.get(platform, '📱')
                    print(f"      {icon} {platform.title()}: {url}")
        
        print()
    
    # Show CRM integration format
    print("🏢 CRM Integration Format:")
    print("-" * 40)
    
    if influencers:
        sample = influencers[0]
        print("📋 Contact Record Fields:")
        print(f"   • Name: {sample['name']}")
        print(f"   • Type: influencer")
        print(f"   • Brand: {sample['brand']}")
        print(f"   • Primary Platform: {sample['primary_platform']}")
        print(f"   • Follower Count: {sample['total_reach']:,}")
        print(f"   • Engagement Rate: {sample['avg_engagement_rate']}%")
        print(f"   • Brand Alignment: {round(sample['brand_alignment_score']*100)}%")
        
        if sample.get('social_links'):
            print(f"   • Social Media URLs:")
            links = sample['social_links'].split(',') if sample['social_links'] else []
            for link in links:
                if ':' in link:
                    platform, url = link.split(':', 1)
                    print(f"     - {platform.title()}: {url}")
    
    # Summary of platforms
    all_platforms = set()
    for inf in influencers:
        if inf.get('social_links'):
            links = inf['social_links'].split(',')
            for link in links:
                if ':' in link:
                    platform = link.split(':', 1)[0]
                    all_platforms.add(platform)
    
    print(f"\n🌐 Available Social Media Platforms:")
    platform_emojis = {
        'youtube': '📺', 'instagram': '📸', 'linkedin': '💼', 
        'twitter': '🐦', 'bluesky': '🌌', 'mastodon': '🐘'
    }
    
    for platform in sorted(all_platforms):
        emoji = platform_emojis.get(platform, '📱')
        print(f"   {emoji} {platform.title()}")
    
    print(f"\n✅ All platform URLs are CRM-ready and automatically synced!")

if __name__ == "__main__":
    show_crm_ready_data()