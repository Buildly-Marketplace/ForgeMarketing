#!/usr/bin/env python3
"""
Google Analytics Setup Script
=============================

Script to help configure Google Analytics integration for the Buildly Labs Foundry.
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

def setup_google_analytics():
    """Guide user through Google Analytics setup"""
    
    # Load environment variables from .env file
    load_dotenv()
    
    print("🔧 Google Analytics Setup for Buildly Labs Foundry")
    print("=" * 60)
    
    # Check current configuration
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found. Please create one first.")
        return
    
    # Read current .env
    with open(env_file, 'r') as f:
        env_content = f.read()
    
    print("\n📊 Current Google Analytics Configuration:")
    
    ga_api_key = os.getenv('GOOGLE_ANALYTICS_API_KEY')
    ga_property_id = os.getenv('GOOGLE_ANALYTICS_PROPERTY_ID')
    
    if ga_api_key:
        print(f"✅ API Key: {ga_api_key[:20]}...")
    else:
        print("❌ API Key: Not configured")
    
    if ga_property_id:
        print(f"✅ Property ID: {ga_property_id}")
    else:
        print("❌ Property ID: Not configured")
    
    print("\n🔍 What you need for Google Analytics integration:")
    print("1. Google Analytics 4 Property ID (format: 123456789)")
    print("2. Google Analytics Data API enabled")
    print("3. API Key with Analytics permission")
    
    print("\n📋 Setup Steps:")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Create or select a project")
    print("3. Enable the Google Analytics Data API")
    print("4. Create an API key")
    print("5. Go to https://analytics.google.com/")
    print("6. Find your GA4 Property ID")
    
    print("\n🎯 For firstcityfoundry.com:")
    print("- Website: https://www.firstcityfoundry.com")
    print("- You need to add Google Analytics tracking to the website")
    print("- Then get the Property ID from the GA4 dashboard")
    
    # Test current API key if available
    if ga_api_key and ga_property_id:
        print(f"\n🧪 Testing current configuration...")
        test_ga_api(ga_api_key, ga_property_id)
    elif ga_api_key:
        print(f"\n⚠️  API Key found but Property ID missing")
        print("Please add GOOGLE_ANALYTICS_PROPERTY_ID to your .env file")
    
    print("\n💡 Next Steps:")
    print("1. Add Google Analytics tracking code to firstcityfoundry.com")
    print("2. Get your GA4 Property ID")
    print("3. Update GOOGLE_ANALYTICS_PROPERTY_ID in .env")
    print("4. Test with: python3 scripts/analytics_reporter.py")

def test_ga_api(api_key: str, property_id: str):
    """Test Google Analytics API access"""
    try:
        # Test basic API access
        test_url = f"https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"  # Note: This might need OAuth for GA4
        }
        
        # Basic test payload
        payload = {
            "dateRanges": [{"startDate": "2025-09-10", "endDate": "2025-09-12"}],
            "metrics": [{"name": "sessions"}]
        }
        
        response = requests.post(test_url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print("✅ Google Analytics API test successful!")
            data = response.json()
            print(f"   Response received: {len(str(data))} characters")
        elif response.status_code == 401:
            print("🔑 API Key authentication issue")
            print("   Note: GA4 Data API might require OAuth instead of API key")
        elif response.status_code == 403:
            print("🚫 API Key doesn't have Analytics permission")
            print("   Enable Google Analytics Data API for your project")
        elif response.status_code == 404:
            print("❓ Property ID not found or no access")
            print(f"   Check if property ID {property_id} is correct")
        else:
            print(f"⚠️  API test failed with status {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")

def show_env_template():
    """Show .env template for analytics"""
    print("\n📄 .env Template for Analytics:")
    print("-" * 40)
    print("""
# Analytics Configuration
GOOGLE_ANALYTICS_PROPERTY_ID=123456789
GOOGLE_ANALYTICS_API_KEY=<your-google-analytics-api-key>
GOOGLE_ANALYTICS_CREDENTIALS_FILE=credentials.json
WEBSITE_URL=https://www.firstcityfoundry.com
YOUTUBE_CHANNEL_ID=
YOUTUBE_API_KEY=
    """)

if __name__ == "__main__":
    setup_google_analytics()
    show_env_template()
