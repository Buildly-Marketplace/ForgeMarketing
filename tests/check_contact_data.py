#!/usr/bin/env python3
"""
Quick check of contact data structure
"""

import sys
from pathlib import Path
import json

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_contact_data():
    """Check the actual structure of contact data"""
    try:
        from automation.contacts_manager import UnifiedContactsManager
        
        contacts_manager = UnifiedContactsManager()
        
        # Get influencer contacts
        contacts = contacts_manager.get_contacts(contact_type='influencer', limit=3)
        
        print(f"🎯 Found {len(contacts)} influencer contacts")
        
        if contacts:
            contact = contacts[0]
            print(f"\n📋 Sample Contact: {contact.get('name', 'Unknown')}")
            print("\n🔍 All fields:")
            for key, value in contact.items():
                if value:  # Only show non-empty values
                    print(f"  {key}: {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}")
            
            print(f"\n📱 Social-related fields:")
            for key, value in contact.items():
                if ('social' in key.lower() or 'url' in key.lower() or 'link' in key.lower()) and value:
                    print(f"  {key}: {value}")
            
            # Check notes for social links
            notes = contact.get('notes', '')
            if 'Social Media:' in notes:
                social_part = notes.split('Social Media:')[1].strip() if 'Social Media:' in notes else ''
                print(f"\n🔗 Social Media from notes: {social_part}")
        
    except Exception as e:
        import traceback
        print(f"❌ Error: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    check_contact_data()