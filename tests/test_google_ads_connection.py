#!/usr/bin/env python3
"""
Test Google Ads API Connection

This script tests your Google Ads API setup and retrieves basic campaign data
from your OpenBuild account.
"""

import json
import sys
import os
from datetime import datetime, timedelta

# Add automation directory to path
sys.path.append('automation')

def test_google_ads_connection():
    """Test the Google Ads API connection and retrieve OpenBuild campaigns"""
    
    print("🧪 Testing Google Ads API Connection")
    print("=" * 50)
    
    # Load configuration
    config_path = "automation/config/google_ads_config.json"
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ Configuration file not found")
        print("   Run: python3 google_ads_setup_helper.py")
        return False
    
    # Check required credentials
    required = ['developer_token', 'client_id', 'client_secret', 'refresh_token']
    missing = [field for field in required if not config.get(field)]
    
    if missing:
        print(f"❌ Missing credentials: {', '.join(missing)}")
        print("   Run: python3 update_google_ads_config.py")
        return False
    
    customer_id = config.get('customer_ids', {}).get('open_build')
    if not customer_id:
        print("❌ Missing OpenBuild Customer ID")
        print("   Run: python3 update_google_ads_config.py")
        return False
    
    print("✅ All required credentials found")
    
    # Test connection
    try:
        print("\n📡 Testing API connection...")
        
        # Import Google Ads manager
        from google_ads_manager import GoogleAdsManager
        
        # Initialize manager with real credentials
        ads_manager = GoogleAdsManager(use_mock=False)
        
        print("✅ Google Ads Manager initialized")
        
        # Test getting campaigns
        print(f"\n📊 Retrieving campaigns for OpenBuild (Customer ID: {customer_id})...")
        campaigns = ads_manager.get_campaigns('open_build')
        
        if campaigns:
            print(f"✅ Found {len(campaigns)} campaigns:")
            for campaign in campaigns[:5]:  # Show first 5
                status = campaign.get('status', 'UNKNOWN')
                budget = campaign.get('budget', 0)
                print(f"   • {campaign.get('name', 'Unnamed')} - {status} - ${budget:,.2f}")
                
            if len(campaigns) > 5:
                print(f"   ... and {len(campaigns) - 5} more campaigns")
        else:
            print("⚠️  No campaigns found (this might be normal for a new account)")
        
        # Test performance data
        print(f"\n📈 Testing performance data retrieval...")
        try:
            performance = ads_manager.get_performance_data('open_build', days=7)
            if performance:
                print("✅ Performance data retrieved successfully")
                
                # Show summary
                total_impressions = sum(p.get('impressions', 0) for p in performance)
                total_clicks = sum(p.get('clicks', 0) for p in performance)
                total_cost = sum(p.get('cost', 0) for p in performance)
                
                print(f"   📊 Last 7 days summary:")
                print(f"   • Impressions: {total_impressions:,}")
                print(f"   • Clicks: {total_clicks:,}")
                print(f"   • Cost: ${total_cost:,.2f}")
                
                if total_impressions > 0:
                    ctr = (total_clicks / total_impressions) * 100
                    print(f"   • CTR: {ctr:.2f}%")
            else:
                print("⚠️  No performance data found (might be no recent activity)")
                
        except Exception as e:
            print(f"⚠️  Performance data test failed: {e}")
        
        print("\n🎉 Google Ads API connection test successful!")
        print("🚀 Your OpenBuild campaign is ready for dashboard integration")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure google-ads library is installed:")
        print("   pip install google-ads")
        return False
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        
        # Provide helpful error messages
        error_str = str(e).lower()
        if 'invalid_grant' in error_str:
            print("\n💡 This usually means your refresh token is invalid or expired")
            print("   Run: python3 google_ads_oauth_helper.py")
        elif 'invalid_customer_id' in error_str:
            print("\n💡 Check your Customer ID format (remove dashes)")
            print("   Run: python3 update_google_ads_config.py")
        elif 'developer_token' in error_str:
            print("\n💡 Check your Developer Token from Google Ads API Center")
            print("   Run: python3 update_google_ads_config.py")
        else:
            print("\n💡 For detailed troubleshooting:")
            print("   1. Verify all credentials in Google Ads and Cloud Console")
            print("   2. Check that Google Ads API is enabled in your project")
            print("   3. Ensure your Developer Token is approved")
        
        return False

def switch_to_real_client():
    """Switch the dashboard to use real Google Ads client"""
    
    print("\n🔄 Switching dashboard to use real Google Ads data...")
    
    # Update the Google Ads manager to use real client by default
    manager_path = "automation/google_ads_manager.py"
    
    try:
        with open(manager_path, 'r') as f:
            content = f.read()
        
        # Replace use_mock=True with use_mock=False in the default initialization
        updated_content = content.replace(
            'def __init__(self, use_mock=True):',
            'def __init__(self, use_mock=False):'
        )
        
        if updated_content != content:
            with open(manager_path, 'w') as f:
                f.write(updated_content)
            print("✅ Dashboard configured to use real Google Ads data")
        else:
            print("ℹ️  Dashboard already configured for real data")
            
    except Exception as e:
        print(f"⚠️  Could not update dashboard config: {e}")
        print("   You can manually set use_mock=False in google_ads_manager.py")

def main():
    """Main function"""
    
    # Test the connection
    connection_ok = test_google_ads_connection()
    
    if connection_ok:
        # Switch to real client
        switch_to_real_client()
        
        print("\n" + "=" * 50)
        print("🎯 OpenBuild Google Ads Integration Ready!")
        print("=" * 50)
        print("✅ API connection working")
        print("✅ Campaign data accessible") 
        print("✅ Dashboard configured for real data")
        print("\n🚀 Launch the dashboard to see your live campaign data:")
        print("   cd dashboard && python3 app.py")
        
        return 0
    else:
        print("\n" + "=" * 50)
        print("❌ Setup incomplete")
        print("=" * 50)
        print("Complete the steps above, then run this test again")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())