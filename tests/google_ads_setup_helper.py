#!/usr/bin/env python3
"""
Google Ads API Setup Helper for OpenBuild Campaign Integration

This script helps you:
1. Verify Google Cloud Console setup
2. Test API access with your existing credentials  
3. Gather required information for Google Ads API
4. Generate OAuth refresh tokens

Usage:
    python3 google_ads_setup_helper.py
"""

import os
import sys
import json
import requests
from datetime import datetime

class GoogleAdsSetupHelper:
    def __init__(self):
        self.config_path = "automation/config/google_ads_config.json"
        self.analytics_api_key = os.environ.get('GOOGLE_ANALYTICS_API_KEY', '')
        
    def print_header(self, title):
        """Print a formatted header"""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
        
    def print_step(self, step_num, title, description=""):
        """Print a formatted step"""
        print(f"\n📋 Step {step_num}: {title}")
        if description:
            print(f"   {description}")
            
    def check_analytics_access(self):
        """Test if the Analytics API key works (to verify Cloud Console project)"""
        self.print_step(1, "Testing Analytics API Access", 
                       "Verifying your Google Cloud Console project...")
        
        # Test with Google Analytics Reporting API
        test_url = f"https://analyticsreporting.googleapis.com/v4/reports:batchGet?key={self.analytics_api_key}"
        
        try:
            # Simple test request (will fail auth but should show API is enabled)
            response = requests.post(test_url, json={
                "reportRequests": []
            })
            
            if response.status_code == 400:  # Bad request is OK - means API is accessible
                print("   ✅ Analytics API is accessible")
                print("   ✅ Google Cloud Console project is properly configured")
                return True
            elif response.status_code == 403:
                print("   ❌ API key may be restricted or Analytics API not enabled")
                return False
            else:
                print(f"   ⚠️  Unexpected response: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error testing Analytics API: {e}")
            return False
    
    def check_ads_api_requirements(self):
        """Explain Google Ads API requirements"""
        self.print_step(2, "Google Ads API Requirements", 
                       "Understanding what we need for Google Ads integration...")
        
        print("\n   For Google Ads API, we need:")
        print("   📝 Developer Token (from Google Ads account)")
        print("   🔐 OAuth 2.0 Client ID & Secret (from Google Cloud Console)")
        print("   🎫 Refresh Token (generated via OAuth flow)")
        print("   🏢 Customer ID (your Google Ads account ID)")
        
        print("\n   Unlike Analytics API, Google Ads uses OAuth 2.0 instead of API keys")
        print("   This provides more secure access to campaign data")
        
    def check_existing_config(self):
        """Check current configuration file"""
        self.print_step(3, "Checking Current Configuration")
        
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                
            print("   📄 Configuration file found")
            
            # Check what's missing
            missing = []
            if not config.get('developer_token'):
                missing.append("Developer Token")
            if not config.get('client_id'):
                missing.append("Client ID")
            if not config.get('client_secret'):
                missing.append("Client Secret")
            if not config.get('refresh_token'):
                missing.append("Refresh Token")
            if not config.get('customer_ids', {}).get('open_build'):
                missing.append("OpenBuild Customer ID")
                
            if missing:
                print(f"   ⚠️  Missing credentials: {', '.join(missing)}")
            else:
                print("   ✅ All credentials are configured")
                
            return config, missing
            
        except FileNotFoundError:
            print("   ❌ Configuration file not found")
            return None, ["All credentials"]
        except Exception as e:
            print(f"   ❌ Error reading config: {e}")
            return None, ["All credentials"]
    
    def provide_setup_instructions(self, missing_items):
        """Provide step-by-step setup instructions"""
        self.print_step(4, "Setup Instructions")
        
        if "Developer Token" in missing_items:
            print("\n   🔑 Getting Developer Token:")
            print("   1. Sign in to your Google Ads account")
            print("   2. Go to Tools & Settings → Setup → API Center")
            print("   3. Apply for API access (if not already done)")
            print("   4. Copy your Developer Token")
            
        if any(item in missing_items for item in ["Client ID", "Client Secret"]):
            print("\n   🔐 Setting up OAuth 2.0:")
            print("   1. Go to Google Cloud Console (console.cloud.google.com)")
            print("   2. Select your project (same one used for Analytics)")
            print("   3. Enable Google Ads API in API Library")
            print("   4. Go to Credentials → Create Credentials → OAuth 2.0 Client ID")
            print("   5. Choose 'Desktop Application' as application type")
            print("   6. Copy Client ID and Client Secret")
            
        if "OpenBuild Customer ID" in missing_items:
            print("\n   🏢 Finding Customer ID:")
            print("   1. Sign in to your Google Ads account")
            print("   2. Look at the top right corner - you'll see a number like 123-456-7890")
            print("   3. Remove the dashes: 1234567890")
            print("   4. This is your Customer ID")
            
    def create_oauth_helper(self):
        """Create a simple OAuth helper script"""
        self.print_step(5, "Creating OAuth Helper Script")
        
        oauth_script = '''#!/usr/bin/env python3
"""
OAuth 2.0 Token Generator for Google Ads API

Run this after you have Client ID and Client Secret configured.
"""

from google_auth_oauthlib.flow import InstalledAppFlow
import json

# Scopes required for Google Ads API
SCOPES = ['https://www.googleapis.com/auth/adwords']

def generate_refresh_token():
    """Generate refresh token using OAuth 2.0 flow"""
    
    # Load config
    with open('automation/config/google_ads_config.json', 'r') as f:
        config = json.load(f)
    
    if not config.get('client_id') or not config.get('client_secret'):
        print("❌ Please configure client_id and client_secret first")
        return
        
    # Create OAuth config
    oauth_config = {
        "installed": {
            "client_id": config['client_id'],
            "client_secret": config['client_secret'],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }
    
    # Save temporary OAuth config
    with open('client_secrets.json', 'w') as f:
        json.dump(oauth_config, f)
    
    try:
        # Run OAuth flow
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secrets.json', SCOPES)
        credentials = flow.run_local_server(port=0)
        
        print("✅ OAuth flow completed!")
        print(f"🎫 Refresh Token: {credentials.refresh_token}")
        
        # Update config with refresh token
        config['refresh_token'] = credentials.refresh_token
        with open('automation/config/google_ads_config.json', 'w') as f:
            json.dump(config, f, indent=2)
            
        print("✅ Configuration updated with refresh token!")
        
    except Exception as e:
        print(f"❌ OAuth flow failed: {e}")
    finally:
        # Clean up
        import os
        if os.path.exists('client_secrets.json'):
            os.remove('client_secrets.json')

if __name__ == "__main__":
    generate_refresh_token()
'''
        
        with open('google_ads_oauth_helper.py', 'w') as f:
            f.write(oauth_script)
            
        print("   ✅ Created google_ads_oauth_helper.py")
        print("   📝 Run this script after configuring Client ID and Secret")
        
    def create_config_updater(self):
        """Create a script to easily update configuration"""
        self.print_step(6, "Creating Configuration Updater")
        
        updater_script = '''#!/usr/bin/env python3
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
        
    print("\\n✅ Configuration updated!")
    print("🚀 Ready to test Google Ads integration")

if __name__ == "__main__":
    update_config()
'''
        
        with open('update_google_ads_config.py', 'w') as f:
            f.write(updater_script)
            
        print("   ✅ Created update_google_ads_config.py")
        print("   📝 Use this to easily update your credentials")
        
    def run_setup_wizard(self):
        """Run the complete setup wizard"""
        self.print_header("Google Ads API Setup for OpenBuild Campaign")
        
        print("🎯 Goal: Connect your existing OpenBuild Google Ads campaign")
        print("🔑 Using your Analytics API key as a starting point")
        
        # Step 1: Test Analytics access
        analytics_ok = self.check_analytics_access()
        
        # Step 2: Explain requirements
        self.check_ads_api_requirements()
        
        # Step 3: Check current config
        config, missing = self.check_existing_config()
        
        # Step 4: Provide instructions
        if missing:
            self.provide_setup_instructions(missing)
            
        # Step 5: Create helper scripts
        self.create_oauth_helper()
        self.create_config_updater()
        
        # Final summary
        self.print_header("Next Steps Summary")
        
        if analytics_ok:
            print("✅ Your Google Cloud Console project is properly set up")
            print("✅ You can proceed with Google Ads API setup")
        else:
            print("⚠️  Please verify your Google Cloud Console setup first")
            
        print(f"\\n📋 Missing credentials: {len(missing)} items")
        for item in missing:
            print(f"   • {item}")
            
        print("\\n🚀 What to do next:")
        print("   1. Follow the setup instructions above")
        print("   2. Run: python3 update_google_ads_config.py")
        print("   3. Run: python3 google_ads_oauth_helper.py")
        print("   4. Test integration with: python3 test_google_ads_connection.py")
        
        return len(missing) == 0

def main():
    """Main function"""
    setup_helper = GoogleAdsSetupHelper()
    ready = setup_helper.run_setup_wizard()
    
    if ready:
        print("\\n🎉 Your Google Ads integration is ready to test!")
    else:
        print("\\n⏳ Complete the setup steps above to proceed")
        
    return 0 if ready else 1

if __name__ == "__main__":
    sys.exit(main())