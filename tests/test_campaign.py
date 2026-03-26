#!/usr/bin/env python3
"""
Test Campaign Execution
=======================

Test the campaign execution directly to debug the unified_db_path error
"""

import sys
import os
sys.path.append('/Users/greglind/Projects/Sales and Marketing')

from automation.multi_brand_outreach import MultiBrandOutreachCampaign

def test_campaign_execution():
    """Test campaign execution for a brand"""
    print("🧪 Testing Campaign Execution")
    print("=" * 40)
    
    try:
        # Create campaign manager
        campaign_manager = MultiBrandOutreachCampaign()
        print("✅ Campaign manager created successfully")
        
        # Test getting targets
        print("\n📋 Testing target retrieval...")
        targets = campaign_manager.get_campaign_targets('buildly', limit=3)
        print(f"   Found {len(targets)} targets for buildly")
        
        for i, target in enumerate(targets[:3]):
            print(f"   {i+1}. {target.name} ({target.email})")
        
        if not targets:
            print("   ⚠️  No targets found - this might be why campaigns show 0 emails")
            return
        
        # Test campaign execution
        print("\n🚀 Testing campaign execution...")
        result = campaign_manager.execute_brand_campaign(
            'buildly', 
            target_count=3,
            campaign_type='general'
        )
        
        print("📊 Campaign Result:")
        print(f"   Success: {result.get('success', False)}")
        print(f"   Emails Sent: {result.get('emails_sent', 0)}")
        print(f"   Targets Processed: {result.get('targets_processed', 0)}")
        
        if 'error' in result:
            print(f"   Error: {result['error']}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_campaign_execution()