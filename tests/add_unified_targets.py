#!/usr/bin/env python3
"""
Add Targets to Unified Database
==============================

Directly add targets to the unified outreach database that powers
the campaign manager to activate inactive brands.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

def get_unified_db_path():
    """Get the unified database path"""
    project_root = Path(__file__).parent
    db_path = project_root / 'data' / 'unified_outreach.db'
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path

def add_target_to_unified_db(name, email, category, brand, description="", website="", company_name=""):
    """Add a target to the unified database"""
    db_path = get_unified_db_path()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Generate unique target_key
        target_key = f"{name.lower().replace(' ', '_')}_{email.replace('@', '_at_').replace('.', '_')}"
        
        # Check if target already exists for this brand
        cursor.execute("""
            SELECT id FROM unified_targets 
            WHERE brand = ? AND target_key = ?
        """, (brand, target_key))
        
        if cursor.fetchone():
            print(f"   ⏭️  Skipped: {name} (already exists for {brand})")
            return False
        
        # Insert new target using existing schema
        cursor.execute("""
            INSERT INTO unified_targets 
            (brand, target_key, name, company_name, email, website, category, 
             description, priority, source, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 3, 'manual_setup', ?, ?)
        """, (brand, target_key, name, company_name or name, email, website, 
              category, description, datetime.now().isoformat(), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        print(f"   ✅ Added: {name}")
        return True
        
    except Exception as e:
        print(f"   ❌ Error adding {name}: {e}")
        return False

def add_targets_for_brand(brand_key, brand_name, targets):
    """Add multiple targets for a brand"""
    print(f"📝 Adding targets for {brand_name} ({brand_key})...")
    
    added_count = 0
    for target in targets:
        success = add_target_to_unified_db(
            name=target['name'],
            email=target['email'],
            category=target['category'],
            brand=brand_key,
            description=target['description'],
            website=target.get('website', ''),
            company_name=target.get('company_name', target['name'])
        )
        if success:
            added_count += 1
    
    print(f"   📊 Added {added_count}/{len(targets)} targets for {brand_name}")
    return added_count

def main():
    """Add targets for inactive brands"""
    print("🎯 Adding Targets to Unified Database")
    print("=" * 50)
    
    # Define targets for each brand
    brand_targets = {
        'buildly': {
            'name': 'Buildly',
            'targets': [
                {
                    'name': 'TechCrunch Editorial',
                    'email': 'tips@techcrunch.com',
                    'category': 'publication',
                    'description': 'Leading technology news publication',
                    'website': 'https://techcrunch.com'
                },
                {
                    'name': 'Product Hunt',
                    'email': 'hello@producthunt.com', 
                    'category': 'platform',
                    'description': 'Product discovery platform',
                    'website': 'https://producthunt.com'
                },
                {
                    'name': 'Zapier Partnerships',
                    'email': 'partnerships@zapier.com',
                    'category': 'platform',
                    'description': 'Automation platform partnerships',
                    'website': 'https://zapier.com'
                },
                {
                    'name': 'Bubble.io Partnerships',
                    'email': 'partnerships@bubble.io',
                    'category': 'platform',
                    'description': 'No-code platform partnerships',
                    'website': 'https://bubble.io'
                },
                {
                    'name': 'Retool Partnerships',
                    'email': 'partnerships@retool.com',
                    'category': 'platform',
                    'description': 'Internal tools platform partnerships',
                    'website': 'https://retool.com'
                }
            ]
        },
        
        'radical': {
            'name': 'Radical Therapy',
            'targets': [
                {
                    'name': 'Psychology Today Editorial',
                    'email': 'info@psychologytoday.com',
                    'category': 'publication',
                    'description': 'Mental health resources directory',
                    'website': 'https://psychologytoday.com'
                },
                {
                    'name': 'BetterHelp Partnerships',
                    'email': 'partnerships@betterhelp.com',
                    'category': 'platform',
                    'description': 'Online therapy platform',
                    'website': 'https://betterhelp.com'
                },
                {
                    'name': 'Headspace Business',
                    'email': 'business@headspace.com',
                    'category': 'platform', 
                    'description': 'Meditation and mindfulness platform',
                    'website': 'https://headspace.com'
                },
                {
                    'name': 'NAMI Partnership',
                    'email': 'info@nami.org',
                    'category': 'organization',
                    'description': 'National Alliance on Mental Illness',
                    'website': 'https://nami.org'
                }
            ]
        },
        
        'oregonsoftware': {
            'name': 'Oregon Software',
            'targets': [
                {
                    'name': 'Oregon Business Editorial',
                    'email': 'editor@oregonbusiness.com',
                    'category': 'publication',
                    'description': 'Oregon business magazine',
                    'website': 'https://oregonbusiness.com'
                },
                {
                    'name': 'Technology Association of Oregon',
                    'email': 'info@techoregon.org',
                    'category': 'organization',
                    'description': 'Oregon tech industry association',
                    'website': 'https://techoregon.org'
                },
                {
                    'name': 'Portland Business Journal',
                    'email': 'portland@bizjournals.com',
                    'category': 'publication',
                    'description': 'Portland business publication',
                    'website': 'https://bizjournals.com/portland'
                },
                {
                    'name': 'Puppet Partnerships',
                    'email': 'partnerships@puppet.com',
                    'category': 'company',
                    'description': 'Portland-based DevOps company',
                    'website': 'https://puppet.com'
                }
            ]
        }
    }
    
    total_added = 0
    
    for brand_key, brand_info in brand_targets.items():
        added = add_targets_for_brand(
            brand_key, 
            brand_info['name'],
            brand_info['targets']
        )
        total_added += added
        print()
    
    print("=" * 50)
    print(f"✅ Target Setup Complete!")
    print(f"📊 Total targets added: {total_added}")
    print()
    print("🔗 Campaign Manager: http://127.0.0.1:5003/campaigns")
    print("📊 Analytics Dashboard: http://127.0.0.1:5003/analytics")
    print()
    print("🎉 All brands should now show active status!")

if __name__ == "__main__":
    main()