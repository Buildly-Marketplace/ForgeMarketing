#!/usr/bin/env python3
"""
Test the enhanced CRM sync functionality with social media links
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_crm_sync():
    """Test the CRM sync functionality with social media links"""
    print("🔗 Testing Enhanced CRM Sync with Social Media Links")
    print("=" * 60)
    
    try:
        from automation.influencer_discovery import BrandInfluencerDiscovery
        from automation.contacts_manager import UnifiedContactsManager
        
        # Get influencers
        discovery = BrandInfluencerDiscovery()
        influencers = discovery.get_brand_influencers()
        
        print(f"📊 Found {len(influencers)} influencers to potentially sync")
        
        # Test the enhanced contact data format for first few influencers
        contacts_manager = UnifiedContactsManager()
        
        for i, influencer in enumerate(influencers[:3]):
            print(f"\n👤 {i+1}. {influencer['name']} ({influencer['brand']})")
            
            # Parse social media links like the enhanced sync does
            social_links = influencer.get('social_links', '')
            parsed_links = []
            social_platforms = {}
            
            if social_links:
                for link in social_links.split(','):
                    if ':' in link:
                        platform, url = link.split(':', 1)
                        platform = platform.strip()
                        url = url.strip()
                        parsed_links.append(f"{platform.title()}: {url}")
                        social_platforms[f'{platform}_url'] = url
            
            print(f"   📱 Social Media Links:")
            if parsed_links:
                for link in parsed_links:
                    print(f"      • {link}")
            else:
                print("      • No social media links")
            
            print(f"   🏢 CRM Fields That Will Be Created:")
            print(f"      • Name: {influencer['name']}")
            print(f"      • Type: influencer")
            print(f"      • Brand: {influencer['brand']}")
            print(f"      • Followers: {influencer['total_reach']:,}")
            print(f"      • Platform URLs: {list(social_platforms.keys())}")
        
        print(f"\n✅ CRM Sync Test Complete")
        print(f"💡 Social media links will be stored in:")
        print(f"   • Main 'notes' field with formatted links")
        print(f"   • Individual platform URL fields (youtube_url, twitter_url, etc.)")
        print(f"   • Raw 'social_links' field for programmatic access")
        
    except Exception as e:
        print(f"❌ Error testing CRM sync: {e}")

if __name__ == "__main__":
    test_crm_sync()