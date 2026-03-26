#!/usr/bin/env python3
"""
Simplified Google Ads API Integration using Service Account

This approach uses service account authentication which is simpler than OAuth flows.
It requires:
1. A service account JSON key file from your Google Cloud project
2. A developer token from your Google Ads account
3. Your Google Ads customer ID

Usage:
    python3 setup_service_account_auth.py
"""

import json
import os
import sys

def create_service_account_instructions():
    """Create instructions for setting up service account authentication"""
    
    print("🔧 Setting up Google Ads API with Service Account Authentication")
    print("=" * 70)
    
    print("\n📋 What we need:")
    print("1. 🔐 Service Account JSON key from Google Cloud Console")
    print("2. 🔑 Developer Token from Google Ads account")
    print("3. 🏢 Customer ID for your OpenBuild account")
    
    print("\n" + "=" * 70)
    print("STEP 1: Create Service Account in Google Cloud Console")
    print("=" * 70)
    
    print("📍 You already have the project: elite-bedrock-360516")
    print("📍 Google Ads API is already enabled")
    print()
    print("1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts?project=elite-bedrock-360516")
    print("2. Click 'CREATE SERVICE ACCOUNT'")
    print("3. Service account name: 'google-ads-api-service'")
    print("4. Service account ID: 'google-ads-api-service'") 
    print("5. Click 'CREATE AND CONTINUE'")
    print("6. Skip the optional steps and click 'DONE'")
    print()
    print("7. Click on the created service account")
    print("8. Go to 'KEYS' tab")
    print("9. Click 'ADD KEY' → 'Create new key'")
    print("10. Select 'JSON' and click 'CREATE'")
    print("11. Save the downloaded JSON file as 'google_ads_service_account.json'")
    
    print("\n" + "=" * 70)
    print("STEP 2: Get Developer Token from Google Ads")
    print("=" * 70)
    
    print("1. Go to your Google Ads account")
    print("2. Click Tools & Settings (wrench icon)")
    print("3. Under 'Setup', click 'API Center'")
    print("4. If you don't have a developer token:")
    print("   - Click 'APPLY FOR API ACCESS'")
    print("   - Fill out the form (may require manager account)")
    print("   - Wait for approval (can take several days)")
    print("5. Copy your 22-character developer token")
    
    print("\n" + "=" * 70)
    print("STEP 3: Grant Service Account Access to Google Ads")
    print("=" * 70)
    
    print("1. In your Google Ads account, go to Admin → Access and security")
    print("2. Click the '+' button under Users tab")
    print("3. Enter the service account email (from the JSON file)")
    print("4. Select appropriate access level (Admin recommended)")
    print("5. Click 'Add account'")
    
    print("\n" + "=" * 70)
    print("STEP 4: Find Your Customer ID")
    print("=" * 70)
    
    print("1. In your Google Ads account, look at the top-right corner")
    print("2. You'll see a number like 123-456-7890")
    print("3. Remove the dashes: 1234567890")
    print("4. This is your Customer ID")
    
    return True

def create_service_account_config_updater():
    """Create a script to update configuration with service account details"""
    
    config_script = '''#!/usr/bin/env python3
"""
Google Ads Service Account Configuration

Interactive script to configure Google Ads API with service account authentication.
"""

import json
import os

def update_service_account_config():
    """Update configuration with service account details"""
    
    print("🔧 Google Ads Service Account Configuration")
    print("=" * 50)
    
    config_path = "automation/config/google_ads_config.json"
    
    # Load existing config
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ Configuration file not found")
        return False
    
    print("\\nConfiguring service account authentication...")
    print("Leave empty to keep current value\\n")
    
    # Get service account file path
    current_sa_path = config.get('service_account_path', '')
    sa_path = input(f"Service Account JSON file path [{current_sa_path or 'google_ads_service_account.json'}]: ").strip()
    if not sa_path:
        sa_path = current_sa_path or 'google_ads_service_account.json'
    
    # Verify service account file exists
    if not os.path.exists(sa_path):
        print(f"⚠️  Service account file not found: {sa_path}")
        print("   Please ensure the file exists and try again")
    else:
        print(f"✅ Service account file found: {sa_path}")
        
        # Load service account to get email
        try:
            with open(sa_path, 'r') as f:
                sa_data = json.load(f)
            sa_email = sa_data.get('client_email', 'Unknown')
            print(f"   📧 Service account email: {sa_email}")
        except Exception as e:
            print(f"   ⚠️  Could not read service account file: {e}")
    
    # Get developer token
    current_dev_token = config.get('developer_token', '')
    display_token = current_dev_token[:8] + '...' if len(current_dev_token) > 8 else current_dev_token
    dev_token = input(f"Developer Token [{display_token}]: ").strip()
    if dev_token:
        if len(dev_token) != 22:
            print("⚠️  Developer token should be 22 characters long")
    
    # Get OpenBuild Customer ID
    current_customer = config.get('customer_ids', {}).get('open_build', '')
    customer_id = input(f"OpenBuild Customer ID [{current_customer}]: ").strip()
    if customer_id:
        # Remove any dashes
        customer_id = customer_id.replace('-', '')
        if not customer_id.isdigit() or len(customer_id) != 10:
            print("⚠️  Customer ID should be 10 digits (without dashes)")
    
    # Update configuration
    config['service_account_path'] = sa_path
    if dev_token:
        config['developer_token'] = dev_token
    if customer_id:
        if 'customer_ids' not in config:
            config['customer_ids'] = {}
        config['customer_ids']['open_build'] = customer_id
    
    # Clear OAuth fields since we're using service account
    config['client_id'] = ''
    config['client_secret'] = ''
    config['refresh_token'] = ''
    
    # Save updated config
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("\\n✅ Configuration updated for service account authentication!")
    print("\\n🚀 Next steps:")
    print("   1. Ensure service account has access to your Google Ads account")
    print("   2. Run: python3 test_service_account_connection.py")
    
    return True

if __name__ == "__main__":
    update_service_account_config()
'''
    
    with open('update_service_account_config.py', 'w') as f:
        f.write(config_script)
    
    print("✅ Created update_service_account_config.py")

def create_service_account_connection_test():
    """Create a test script for service account connection"""
    
    test_script = '''#!/usr/bin/env python3
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
        print("\\n📡 Testing API connection...")
        
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
        print(f"\\n📊 Retrieving campaigns for customer {customer_id}...")
        
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
        print("\\n📈 Testing performance data retrieval...")
        
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
        
        print("\\n🎉 Google Ads API connection test successful!")
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
    
    print("\\n🔄 Updating dashboard configuration...")
    
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
        
        print("\\n" + "=" * 55)
        print("🎯 OpenBuild Google Ads Integration Ready!")
        print("=" * 55)
        print("✅ Service account authentication working")
        print("✅ API connection confirmed")
        print("✅ Dashboard configured")
        
        print("\\n🚀 Launch the dashboard to see your live OpenBuild campaign data:")
        print("   cd dashboard && python3 app.py")
        
        return 0
    else:
        print("\\n" + "=" * 55)
        print("❌ Setup incomplete")
        print("=" * 55)
        print("Complete the steps above, then run this test again")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
'''
    
    with open('test_service_account_connection.py', 'w') as f:
        f.write(test_script)
    
    print("✅ Created test_service_account_connection.py")

def main():
    """Main setup function"""
    
    print("🚀 Google Ads API Service Account Setup")
    print("=" * 50)
    
    create_service_account_instructions()
    
    print("\n" + "=" * 70)
    print("STEP 5: Helper Scripts Created")
    print("=" * 70)
    
    create_service_account_config_updater()
    create_service_account_connection_test()
    
    print("\n" + "=" * 70)
    print("🎯 SUMMARY - What to do next:")
    print("=" * 70)
    print("1. 🔐 Create service account in Google Cloud Console")
    print("2. 📥 Download the JSON key file")
    print("3. 🔑 Get your Developer Token from Google Ads")
    print("4. 🏢 Grant service account access to your Google Ads account")
    print("5. ⚙️  Run: python3 update_service_account_config.py")
    print("6. 🧪 Run: python3 test_service_account_connection.py")
    
    print(f"\n📍 Your Google Cloud project: elite-bedrock-360516")
    print(f"📍 Service account creation: https://console.cloud.google.com/iam-admin/serviceaccounts?project=elite-bedrock-360516")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())