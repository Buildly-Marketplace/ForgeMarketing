#!/usr/bin/env python3
"""
Google Ads Configuration Updater

Interactive script to update your Google Ads API credentials.
"""

import json
import os

def update_config():
    """Interactive configuration updater"""
    config_path = "automation/config/google_ads_config.json"
    
    # Load existing config
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ Configuration file not found")
        return
        
    print("🔧 Google Ads Configuration Updater")
    print("=" * 40)
    print("Leave empty to keep current value")
    print()
    
    # Update each field
    fields = [
        ('developer_token', 'Developer Token'),
        ('client_id', 'OAuth Client ID'),
        ('client_secret', 'OAuth Client Secret'),
        ('refresh_token', 'Refresh Token')
    ]
    
    for field, description in fields:
        current = config.get(field, '')
        display_current = current[:10] + '...' if len(current) > 10 else current
        new_value = input(f"{description} [{display_current}]: ").strip()
        if new_value:
            config[field] = new_value
            
    # Update OpenBuild Customer ID
    current_customer = config.get('customer_ids', {}).get('open_build', '')
    new_customer = input(f"OpenBuild Customer ID [{current_customer}]: ").strip()
    if new_customer:
        if 'customer_ids' not in config:
            config['customer_ids'] = {}
        config['customer_ids']['open_build'] = new_customer
        
    # Save updated config
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
        
    print("\n✅ Configuration updated!")
    print("🚀 Ready to test Google Ads integration")

if __name__ == "__main__":
    update_config()
