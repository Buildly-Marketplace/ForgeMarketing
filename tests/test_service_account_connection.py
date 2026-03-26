#!/usr/bin/env python3
"""
Test Google Ads API Connection with Service Account

This script tests the Google Ads API connection using service account authentication.
"""

import json
import sys
import os
from datetime import datetime

# Add automation directory to path
sys.path.append('automation')

def test_service_account_connection():
    """Test the Google Ads API connection with service account"""
    
    print("🧪 Testing Google Ads API with Service Account")
    print("=" * 55)
    
    # Load configuration
    config_path = "automation/config/google_ads_config.json"
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ Configuration file not found")
        return False
    
    # Check required fields
    required_fields = ['service_account_path', 'developer_token']
    missing = [field for field in required_fields if not config.get(field)]
    
    customer_id = config.get('customer_ids', {}).get('open_build')
    if not customer_id:
        missing.append('OpenBuild Customer ID')
    
    if missing:
        print(f"❌ Missing configuration: {', '.join(missing)}")
        print("   Run: python3 update_service_account_config.py")
        return False
    
    # Check if service account file exists
    sa_path = config['service_account_path']
    if not os.path.exists(sa_path):
        print(f"❌ Service account file not found: {sa_path}")
        return False
    
    print("✅ Configuration looks good")
    print(f"   📁 Service account: {sa_path}")
    print(f"   🔑 Developer token: {config['developer_token'][:8]}...")
    print(f"   🏢 Customer ID: {customer_id}")
    
    # Test the connection
    try:
        print("\n📡 Testing API connection...")
        
        # Import and test Google Ads client
        from google.ads.googleads.client import GoogleAdsClient
        from google.auth.exceptions import DefaultCredentialsError
        
        # Create client with service account
        client = GoogleAdsClient.load_from_dict({
            'developer_token': config['developer_token'],
            'use_proto_plus': True,
            'service_account_path': sa_path
        })
        
        print("✅ Google Ads client created successfully")
        
        # Test API call - get campaigns
        print(f"\n📊 Retrieving campaigns for customer {customer_id}...")
        
        ga_service = client.get_service("GoogleAdsService")
        
        query = """
SELECT
    campaign.id,
    campaign.name,
    campaign.status,
    campaign.advertising_channel_type
FROM campaign
ORDER BY campaign.id
LIMIT 10
"""
        
        response = ga_service.search(customer_id=customer_id, query=query)
        
        campaigns = list(response)
        
        if campaigns:
            print(f"✅ Found {len(campaigns)} campaigns:")
            for row in campaigns:
                campaign = row.campaign
                print(f"   • {campaign.name} (ID: {campaign.id}) - {campaign.status.name}")
        else:
            print("ℹ️  No campaigns found (this is normal for new accounts)")
        
        # Test performance data
        print("\n📈 Testing performance data retrieval...")
        
        perf_query = """
SELECT
    campaign.id,
    campaign.name,
    metrics.impressions,
    metrics.clicks,
    metrics.cost_micros
FROM campaign
WHERE segments.date DURING LAST_7_DAYS
ORDER BY campaign.id
LIMIT 5
"""
        
        perf_response = ga_service.search(customer_id=customer_id, query=perf_query)
        perf_data = list(perf_response)
        
        if perf_data:
            print("✅ Performance data retrieved successfully")
            total_impressions = sum(row.metrics.impressions for row in perf_data)
            total_clicks = sum(row.metrics.clicks for row in perf_data)
            total_cost = sum(row.metrics.cost_micros for row in perf_data) / 1_000_000
            
            print(f"   📊 Last 7 days summary:")
            print(f"   • Impressions: {total_impressions:,}")
            print(f"   • Clicks: {total_clicks:,}")
            print(f"   • Cost: ${total_cost:.2f}")
        else:
            print("ℹ️  No recent performance data found")
        
        print("\n🎉 Google Ads API connection test successful!")
        print("✅ Service account authentication working")
        print("✅ API access confirmed")
        print("✅ Campaign data accessible")
        
        return True
        
    except ImportError as e:
        print(f"❌ Google Ads library not installed: {e}")
        print("   Run: pip install google-ads")
        return False
        
    except DefaultCredentialsError as e:
        print(f"❌ Service account authentication failed: {e}")
        print("   Check your service account file and permissions")
        return False
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        
        error_str = str(e).lower()
        if 'developer_token' in error_str:
            print("💡 Check your Developer Token:")
            print("   • Must be 22 characters long")
            print("   • Must be approved (not just pending)")
            print("   • Must be from a Google Ads Manager account")
        elif 'customer_id' in error_str or 'customer' in error_str:
            print("💡 Check your Customer ID:")
            print("   • Must be 10 digits without dashes")
            print("   • Service account must have access to this account")
        elif 'permission' in error_str or 'access' in error_str:
            print("💡 Service account needs access:")
            print("   • Add service account email to Google Ads account")
            print("   • Grant appropriate permissions (Admin recommended)")
        
        return False

def update_dashboard_config():
    """Update dashboard to use service account authentication"""
    
    print("\n🔄 Updating dashboard configuration...")
    
    # Update the google_ads_manager.py to use service account by default
    manager_path = "automation/google_ads_manager.py"
    
    try:
        with open(manager_path, 'r') as f:
            content = f.read()
        
        # Update default initialization to use service account
        if 'use_mock=True' in content:
            updated_content = content.replace(
                'def __init__(self, use_mock=True):',
                'def __init__(self, use_mock=False, use_service_account=True):'
            )
            
            with open(manager_path, 'w') as f:
                f.write(updated_content)
            print("✅ Dashboard configured for service account authentication")
        else:
            print("ℹ️  Dashboard already configured for real API access")
            
    except Exception as e:
        print(f"⚠️  Could not update dashboard config: {e}")

def main():
    """Main function"""
    
    success = test_service_account_connection()
    
    if success:
        update_dashboard_config()
        
        print("\n" + "=" * 55)
        print("🎯 OpenBuild Google Ads Integration Ready!")
        print("=" * 55)
        print("✅ Service account authentication working")
        print("✅ API connection confirmed")
        print("✅ Dashboard configured")
        
        print("\n🚀 Launch the dashboard to see your live OpenBuild campaign data:")
        print("   cd dashboard && python3 app.py")
        
        return 0
    else:
        print("\n" + "=" * 55)
        print("❌ Setup incomplete")
        print("=" * 55)
        print("Complete the steps above, then run this test again")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
