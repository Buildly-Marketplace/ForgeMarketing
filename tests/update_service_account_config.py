#!/usr/bin/env python3
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
    
    print("\nConfiguring service account authentication...")
    print("Leave empty to keep current value\n")
    
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
    
    print("\n✅ Configuration updated for service account authentication!")
    print("\n🚀 Next steps:")
    print("   1. Ensure service account has access to your Google Ads account")
    print("   2. Run: python3 test_service_account_connection.py")
    
    return True

if __name__ == "__main__":
    update_service_account_config()
