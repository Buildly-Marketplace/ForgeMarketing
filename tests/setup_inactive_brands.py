#!/usr/bin/env python3
"""
Setup Target Discovery for Inactive Brands
==========================================

Manually add high-quality targets for buildly, radical, and oregonsoftware
brands to make them active in the Campaign Manager.
"""

import asyncio
import sys
from pathlib import Path
from automation.multi_brand_outreach import MultiBrandOutreachDatabase, OutreachTarget

# Brand-specific target lists
BRAND_TARGETS = {
    'buildly': [
        {
            'name': 'TechCrunch',
            'category': 'publication',
            'website': 'https://techcrunch.com',
            'description': 'Leading technology news publication',
            'contact_info': {'email': 'tips@techcrunch.com'},
            'relevance': 0.9
        },
        {
            'name': 'Product Hunt',
            'category': 'platform', 
            'website': 'https://producthunt.com',
            'description': 'Product discovery platform for entrepreneurs',
            'contact_info': {'email': 'hello@producthunt.com'},
            'relevance': 0.95
        },
        {
            'name': 'Zapier',
            'category': 'enterprise',
            'website': 'https://zapier.com',
            'description': 'Automation platform for business workflows',
            'contact_info': {'email': 'partnerships@zapier.com'},
            'relevance': 0.92
        },
        {
            'name': 'Airtable',
            'category': 'enterprise',
            'website': 'https://airtable.com',
            'description': 'Low-code database and collaboration platform',
            'contact_info': {'email': 'partnerships@airtable.com'},
            'relevance': 0.88
        },
        {
            'name': 'Bubble',
            'category': 'platform',
            'website': 'https://bubble.io',
            'description': 'No-code app development platform',
            'contact_info': {'email': 'partnerships@bubble.io'},
            'relevance': 0.90
        },
        {
            'name': 'Webflow',
            'category': 'platform',
            'website': 'https://webflow.com',
            'description': 'Visual web development platform',
            'contact_info': {'email': 'partnerships@webflow.com'},
            'relevance': 0.85
        },
        {
            'name': 'Retool',
            'category': 'enterprise',
            'website': 'https://retool.com',
            'description': 'Low-code platform for building internal tools',
            'contact_info': {'email': 'partnerships@retool.com'},
            'relevance': 0.89
        },
        {
            'name': 'Monday.com',
            'category': 'enterprise',
            'website': 'https://monday.com',
            'description': 'Work management platform',
            'contact_info': {'email': 'partnerships@monday.com'},
            'relevance': 0.82
        }
    ],
    
    'radical': [
        {
            'name': 'BetterHelp',
            'category': 'healthcare',
            'website': 'https://betterhelp.com',
            'description': 'Online therapy and mental health platform',
            'contact_info': {'email': 'partnerships@betterhelp.com'},
            'relevance': 0.95
        },
        {
            'name': 'Headspace',
            'category': 'healthcare',
            'website': 'https://headspace.com',
            'description': 'Meditation and mental wellness app',
            'contact_info': {'email': 'partnerships@headspace.com'},
            'relevance': 0.88
        },
        {
            'name': 'Calm',
            'category': 'healthcare',
            'website': 'https://calm.com',
            'description': 'Mental fitness and wellness platform',
            'contact_info': {'email': 'partnerships@calm.com'},
            'relevance': 0.87
        },
        {
            'name': 'Talkspace',
            'category': 'healthcare',
            'website': 'https://talkspace.com',
            'description': 'Online therapy platform',
            'contact_info': {'email': 'partnerships@talkspace.com'},
            'relevance': 0.92
        },
        {
            'name': 'Psychology Today',
            'category': 'publication',
            'website': 'https://psychologytoday.com',
            'description': 'Mental health resources and therapist directory',
            'contact_info': {'email': 'info@psychologytoday.com'},
            'relevance': 0.90
        },
        {
            'name': 'NAMI',
            'category': 'organization',
            'website': 'https://nami.org',
            'description': 'National Alliance on Mental Illness',
            'contact_info': {'email': 'info@nami.org'},
            'relevance': 0.85
        },
        {
            'name': 'Mental Health America',
            'category': 'organization',
            'website': 'https://mhanational.org',
            'description': 'Mental health advocacy organization',
            'contact_info': {'email': 'info@mhanational.org'},
            'relevance': 0.83
        }
    ],
    
    'oregonsoftware': [
        {
            'name': 'Oregon Business',
            'category': 'publication',
            'website': 'https://oregonbusiness.com',
            'description': 'Oregon business news and networking',
            'contact_info': {'email': 'editor@oregonbusiness.com'},
            'relevance': 0.88
        },
        {
            'name': 'Portland Business Journal',
            'category': 'publication',
            'website': 'https://bizjournals.com/portland',
            'description': 'Local business news and insights',
            'contact_info': {'email': 'portland@bizjournals.com'},
            'relevance': 0.85
        },
        {
            'name': 'Technology Association of Oregon',
            'category': 'organization',
            'website': 'https://techoregon.org',
            'description': 'Oregon technology industry association',
            'contact_info': {'email': 'info@techoregon.org'},
            'relevance': 0.90
        },
        {
            'name': 'Portland Startup Week',
            'category': 'event',
            'website': 'https://portlandstartupweek.com',
            'description': 'Annual startup conference and networking',
            'contact_info': {'email': 'info@portlandstartupweek.com'},
            'relevance': 0.82
        },
        {
            'name': 'Nike',
            'category': 'enterprise',
            'website': 'https://nike.com',
            'description': 'Global sportswear and technology company',
            'contact_info': {'email': 'partnerships@nike.com'},
            'relevance': 0.75
        },
        {
            'name': 'Columbia Sportswear',
            'category': 'enterprise', 
            'website': 'https://columbia.com',
            'description': 'Outdoor apparel and technology company',
            'contact_info': {'email': 'partnerships@columbia.com'},
            'relevance': 0.72
        },
        {
            'name': 'Puppet',
            'category': 'startup',
            'website': 'https://puppet.com',
            'description': 'Infrastructure automation company',
            'contact_info': {'email': 'partnerships@puppet.com'},
            'relevance': 0.88
        }
    ]
}

def add_targets_for_brand(db: MultiBrandOutreachDatabase, brand: str, targets_data: list):
    """Add targets for a specific brand"""
    print(f"📝 Adding targets for {brand}...")
    
    added_count = 0
    for target_data in targets_data:
        try:
            target = OutreachTarget(
                name=target_data['name'],
                website=target_data['website'],
                category=target_data['category'],
                email=target_data['contact_info'].get('email', ''),
                description=target_data['description'],
                brand_relevance={brand: target_data['relevance']},
                priority=2  # Medium priority
            )
            
            # Check if target already exists
            if not db.target_exists(target.name, brand):
                db.add_target(target, brand)
                added_count += 1
                print(f"   ✅ Added: {target.name}")
            else:
                print(f"   ⏭️  Skipped: {target.name} (already exists)")
                
        except Exception as e:
            print(f"   ❌ Error adding {target_data['name']}: {e}")
    
    print(f"   📊 Added {added_count} new targets for {brand}")
    return added_count

def main():
    """Set up target discovery for inactive brands"""
    print("🎯 Setting Up Target Discovery for Inactive Brands")
    print("=" * 60)
    
    # Initialize database
    db = MultiBrandOutreachDatabase()
    
    total_added = 0
    
    # Add targets for each brand
    for brand, targets_data in BRAND_TARGETS.items():
        added = add_targets_for_brand(db, brand, targets_data)
        total_added += added
        print()
    
    print(f"✅ Setup Complete!")
    print(f"📊 Total targets added: {total_added}")
    print()
    print("🎉 All brands should now be active in the Campaign Manager!")
    print("   • buildly: Low-code and automation platforms")
    print("   • radical: Mental health and therapy platforms") 
    print("   • oregonsoftware: Regional tech and business networks")
    print()
    print("🔗 View updated campaign manager at: http://127.0.0.1:5003/campaigns")

if __name__ == "__main__":
    main()