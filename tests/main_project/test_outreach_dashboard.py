#!/usr/bin/env python3
"""
Test script for the integrated outreach system in the dashboard
"""

import requests
import json
import tempfile
import os

# Dashboard URL
DASHBOARD_URL = "http://localhost:5003"

def test_brand_config():
    """Test brand configuration API"""
    print("🧪 Testing brand configuration API...")
    
    response = requests.get(f"{DASHBOARD_URL}/api/outreach/brand-config/buildly")
    if response.status_code == 200:
        config = response.json()
        print(f"✅ Buildly config loaded: {config['name']}")
        print(f"   Templates available: {len(config['templates'])}")
        return True
    else:
        print(f"❌ Failed to load config: {response.status_code}")
        return False

def test_preview_email():
    """Test email preview generation"""
    print("\n🧪 Testing email preview generation...")
    
    payload = {
        "brand": "buildly",
        "template": "account_update",
        "sampleUser": {
            "email": "test@example.com",
            "name": "Test User",
            "company": "Test Company",
            "account_type": "Premium",
            "last_login": "2024-10-01",
            "features_used": "API Management"
        }
    }
    
    response = requests.post(f"{DASHBOARD_URL}/api/outreach/preview", json=payload)
    if response.status_code == 200:
        preview = response.json()
        print(f"✅ Email preview generated")
        print(f"   Subject: {preview['subject']}")
        print(f"   Body length: {len(preview['body'])} characters")
        return True
    else:
        print(f"❌ Failed to generate preview: {response.status_code}")
        print(f"   Error: {response.text}")
        return False

def test_csv_campaign():
    """Test CSV campaign upload and preview"""
    print("\n🧪 Testing CSV campaign...")
    
    # Create test CSV
    csv_content = '''email,name,company,account_type,last_login
test1@example.com,John Doe,Acme Corp,Premium,2024-09-15
test2@example.com,Jane Smith,StartupXYZ,Free,2024-08-20'''
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(csv_content)
        temp_csv = f.name
    
    try:
        # Test campaign with preview
        with open(temp_csv, 'rb') as f:
            files = {'csv_file': f}
            data = {
                'brand': 'buildly',
                'template': 'account_update',
                'campaign_name': 'Test Campaign',
                'preview_only': 'true',
                'max_emails': '2'
            }
            
            response = requests.post(f"{DASHBOARD_URL}/api/outreach/run-campaign", 
                                   files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                stats = result['stats']
                print(f"✅ Campaign preview successful")
                print(f"   Total users: {stats['total_users']}")
                print(f"   Emails sent: {stats['emails_sent']}")
                return True
            else:
                print(f"❌ Campaign failed: {result['message']}")
                return False
        else:
            print(f"❌ Campaign request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    finally:
        # Clean up
        os.unlink(temp_csv)

def test_campaign_analytics():
    """Test campaign analytics API"""
    print("\n🧪 Testing campaign analytics...")
    
    response = requests.get(f"{DASHBOARD_URL}/api/outreach/analytics/buildly")
    if response.status_code == 200:
        analytics = response.json()
        print(f"✅ Analytics loaded")
        print(f"   Total campaigns: {analytics['total_campaigns']}")
        print(f"   Total emails sent: {analytics['total_emails_sent']}")
        return True
    else:
        print(f"❌ Failed to load analytics: {response.status_code}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Integrated Outreach System")
    print("=" * 50)
    
    tests = [
        test_brand_config,
        test_preview_email,
        test_csv_campaign,
        test_campaign_analytics
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {i+1}. {test.__name__}: {status}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Outreach system is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()