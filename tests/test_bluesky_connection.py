#!/usr/bin/env python3
"""
Test BlueSky Connection via API
==============================

Test script to verify the BlueSky connection test functionality
through the dashboard API endpoint.
"""

import requests
import json
import sys

def test_bluesky_connection():
    """Test the BlueSky connection via the dashboard API"""
    
    print("🔵 Testing BlueSky Connection API")
    print("=" * 40)
    
    # Dashboard API endpoint
    url = "http://127.0.0.1:5003/api/admin/test-connection/bluesky"
    
    # Test data - simulating what the frontend would send
    test_credentials = {
        "username": "test.bsky.social",
        "app_password": "test-app-password-here",
        "brand": "buildly"
    }
    
    print(f"🎯 Testing with credentials:")
    print(f"   Username: {test_credentials['username']}")
    print(f"   App Password: {'*' * len(test_credentials['app_password'])}")
    print(f"   Brand: {test_credentials['brand']}")
    
    try:
        print(f"\n📤 Sending POST request to: {url}")
        
        response = requests.post(
            url,
            headers={'Content-Type': 'application/json'},
            json=test_credentials,
            timeout=10
        )
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response Data: {json.dumps(data, indent=2)}")
            
            if data.get('success'):
                print(f"\n🎉 BlueSky connection test PASSED!")
                print(f"   Message: {data.get('message', 'No message')}")
            else:
                print(f"\n❌ BlueSky connection test FAILED!")
                print(f"   Error: {data.get('error', 'No error details')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   Raw response: {response.text}")
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True

def test_missing_credentials():
    """Test with missing credentials to verify error handling"""
    
    print(f"\n🔍 Testing Missing Credentials Handling")
    print("-" * 40)
    
    url = "http://127.0.0.1:5003/api/admin/test-connection/bluesky"
    
    # Test with missing credentials
    test_cases = [
        {"username": "test.bsky.social"},  # Missing app_password
        {"app_password": "test-password"},  # Missing username
        {}  # Empty credentials
    ]
    
    for i, credentials in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}: {credentials or 'Empty'}")
        
        try:
            response = requests.post(
                url,
                headers={'Content-Type': 'application/json'},
                json=credentials,
                timeout=5
            )
            
            data = response.json()
            
            if not data.get('success'):
                print(f"   ✅ Correctly rejected: {data.get('error', 'No error message')}")
            else:
                print(f"   ❌ Unexpectedly accepted invalid credentials")
                
        except Exception as e:
            print(f"   ❌ Error testing invalid credentials: {e}")

if __name__ == "__main__":
    print("🚀 BlueSky Connection Test Suite")
    print("=" * 50)
    
    # Test 1: Valid credentials format
    success = test_bluesky_connection()
    
    # Test 2: Invalid credentials
    test_missing_credentials()
    
    print(f"\n{'=' * 50}")
    print(f"🏁 Test Suite Complete")
    print(f"📋 Dashboard URL: http://127.0.0.1:5003/admin")
    print(f"💡 The button should now be visible and functional!")