#!/usr/bin/env python3
"""
Debug CRM sync issue - check if influencers are being synced to contacts
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def debug_crm_sync():
    """Debug why influencers aren't showing in CRM"""
    print("🔍 Debugging CRM Sync Issue")
    print("=" * 50)
    
    try:
        from automation.influencer_discovery import BrandInfluencerDiscovery
        from automation.contacts_manager import UnifiedContactsManager
        
        # Check influencers
        discovery = BrandInfluencerDiscovery()
        influencers = discovery.get_brand_influencers()
        print(f"📊 Found {len(influencers)} influencers in database")
        
        # Check contacts
        contacts_manager = UnifiedContactsManager()
        all_contacts = contacts_manager.get_contacts()
        print(f"👥 Found {len(all_contacts)} total contacts in CRM")
        
        # Check influencer contacts specifically
        influencer_contacts = contacts_manager.get_contacts(contact_type='influencer')
        print(f"🎯 Found {len(influencer_contacts)} influencer contacts in CRM")
        
        print(f"\n📋 Sample Contacts:")
        for i, contact in enumerate(all_contacts[:3]):
            contact_type = contact.get('contact_type', 'unknown')
            name = contact.get('name', 'Unknown')
            print(f"  {i+1}. {name} (Type: {contact_type})")
        
        print(f"\n🔄 Testing Manual Sync...")
        
        # Try syncing first few influencers manually
        synced_count = 0
        for influencer in influencers[:3]:
            # Check if already exists
            existing = contacts_manager.get_contacts(
                search=influencer['name'],
                contact_type='influencer',
                limit=1
            )
            
            if not existing:
                print(f"   Syncing: {influencer['name']} ({influencer['brand']})")
                
                # Create contact data like the API does
                contact_data = {
                    'name': influencer['name'],
                    'email': influencer.get('contact_email', ''),
                    'contact_type': 'influencer',
                    'brand': influencer['brand'],
                    'website': influencer.get('website', ''),
                    'notes': f"Auto-synced from influencer discovery. Platform: {influencer['primary_platform']}, Followers: {influencer['total_reach']}, Engagement: {influencer['avg_engagement_rate']}%, Alignment: {round(influencer['brand_alignment_score']*100)}%. Social Links: {influencer.get('social_links', '')}",
                    'platform': influencer['primary_platform'],
                    'followers_count': str(influencer['total_reach']),
                    'social_links': influencer.get('social_links', '')
                }
                
                try:
                    contact_id = contacts_manager.create_contact(contact_data)
                    if contact_id:
                        synced_count += 1
                        print(f"      ✅ Created contact ID: {contact_id}")
                    else:
                        print(f"      ❌ Failed to create contact - no ID returned")
                except Exception as e:
                    print(f"      ❌ Failed to create contact: {e}")
            else:
                print(f"   Already exists: {influencer['name']}")
        
        print(f"\n✅ Manual sync complete: {synced_count} new contacts created")
        
        # Check again after sync
        updated_influencer_contacts = contacts_manager.get_contacts(contact_type='influencer')
        print(f"🎯 After sync: {len(updated_influencer_contacts)} influencer contacts in CRM")
        
        if updated_influencer_contacts:
            print(f"\n📋 Influencer Contacts:")
            for contact in updated_influencer_contacts[:5]:
                name = contact.get('name', 'Unknown')
                brand = contact.get('brand', 'Unknown')
                platform = contact.get('platform', 'Unknown')
                social_links = contact.get('social_links', '')
                print(f"  • {name} ({brand}) - {platform}")
                if social_links:
                    print(f"    🔗 {social_links}")
        
    except Exception as e:
        import traceback
        print(f"❌ Error: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    debug_crm_sync()