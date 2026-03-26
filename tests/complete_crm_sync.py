#!/usr/bin/env python3
"""
Complete CRM sync of all influencers with social media links
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def complete_crm_sync():
    """Sync all influencers to CRM with full social media links"""
    print("🔄 Complete CRM Sync - All Influencers with Social Links")
    print("=" * 60)
    
    try:
        from automation.influencer_discovery import BrandInfluencerDiscovery
        from automation.contacts_manager import UnifiedContactsManager
        
        # Get all influencers
        discovery = BrandInfluencerDiscovery()
        influencers = discovery.get_brand_influencers()
        
        contacts_manager = UnifiedContactsManager()
        synced_count = 0
        error_count = 0
        
        print(f"📊 Processing {len(influencers)} influencers...")
        print()
        
        for i, influencer in enumerate(influencers):
            name = influencer['name']
            brand = influencer['brand']
            
            # Check if already exists
            existing = contacts_manager.get_contacts(
                search=name,
                contact_type='influencer',
                limit=1
            )
            
            if existing:
                print(f"✓ {i+1:2d}. {name} ({brand}) - Already exists")
                continue
            
            # Parse social links for rich notes
            social_links = influencer.get('social_links', '')
            social_notes = ""
            if social_links:
                links_list = []
                for link in social_links.split(','):
                    if ':' in link:
                        platform, url = link.split(':', 1)
                        platform_name = platform.strip().title()
                        links_list.append(f"{platform_name}: {url.strip()}")
                social_notes = " | ".join(links_list)
            
            # Create enhanced contact data
            contact_data = {
                'name': name,
                'email': influencer.get('contact_email', ''),
                'contact_type': 'influencer',
                'brand': brand,
                'website': influencer.get('website', ''),
                'notes': f"Influencer Discovery: {influencer['primary_platform']} • {influencer['total_reach']:,} followers • {influencer['avg_engagement_rate']}% engagement • {round(influencer['brand_alignment_score']*100)}% brand alignment. Social Media: {social_notes}",
                'platform': influencer['primary_platform'],
                'followers_count': str(influencer['total_reach']),
                'engagement_rate': str(influencer['avg_engagement_rate']),
                'alignment_score': str(round(influencer['brand_alignment_score']*100)),
                'niche': influencer.get('niche', ''),
                'bio_summary': influencer.get('bio_summary', ''),
                'social_links': social_links
            }
            
            try:
                contact_id = contacts_manager.create_contact(contact_data)
                if contact_id:
                    synced_count += 1
                    print(f"✅ {i+1:2d}. {name} ({brand}) - Created ID: {contact_id}")
                    if social_links:
                        # Show which platforms were synced
                        platforms = [link.split(':')[0].strip() for link in social_links.split(',') if ':' in link]
                        platform_icons = {'youtube': '📺', 'instagram': '📸', 'linkedin': '💼', 'twitter': '🐦', 'bluesky': '🌌', 'mastodon': '🐘'}
                        icons = [platform_icons.get(p, '📱') for p in platforms]
                        print(f"     📱 Social Links: {' '.join(icons)} {len(platforms)} platforms")
                else:
                    error_count += 1
                    print(f"❌ {i+1:2d}. {name} ({brand}) - Failed (no ID returned)")
            except Exception as e:
                error_count += 1
                print(f"❌ {i+1:2d}. {name} ({brand}) - Error: {str(e)[:50]}")
        
        print(f"\n📊 Sync Summary:")
        print(f"   ✅ Successfully synced: {synced_count}")
        print(f"   ❌ Errors: {error_count}")
        print(f"   📋 Total processed: {len(influencers)}")
        
        # Final verification
        final_contacts = contacts_manager.get_contacts(contact_type='influencer')
        print(f"   🎯 Total influencer contacts in CRM: {len(final_contacts)}")
        
        if final_contacts:
            print(f"\n📋 Sample Influencer Contacts in CRM:")
            for j, contact in enumerate(final_contacts[:5]):
                c_name = contact.get('name', 'Unknown')
                c_brand = contact.get('brand', 'Unknown')
                c_platform = contact.get('platform', 'Unknown')
                c_followers = contact.get('followers_count', '0')
                print(f"   {j+1}. {c_name} ({c_brand}) - {c_platform} • {c_followers} followers")
        
        print(f"\n✅ CRM sync complete! Influencers should now appear when filtering by 'influencer' type.")
        
    except Exception as e:
        import traceback
        print(f"❌ Error: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    complete_crm_sync()