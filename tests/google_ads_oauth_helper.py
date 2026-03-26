#!/usr/bin/env python3
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
