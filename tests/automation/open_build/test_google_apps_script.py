#!/usr/bin/env python3
"""
Test script to verify Google Apps Script form submission functionality.
This script tests the new deployment URL to ensure form submissions work correctly.
"""

import json
import requests
import sys

# Configuration
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzV56JpDbHzr10lOPI5843WWP_QENV14lkTohTlkOTTkhaqETaXa0JAxVpTUzXXQ80F/exec"
SPREADSHEET_ID = "1Zu_Ij0vG8Q_ebdjdeFVGY8cDaqyrKIXMoY9qwsgY3JM"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check endpoint...")
    try:
        response = requests.get(f"{SCRIPT_URL}?health=check", timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_get_endpoint():
    """Test the GET test endpoint"""
    print("\n🔍 Testing GET test endpoint...")
    try:
        response = requests.get(f"{SCRIPT_URL}?test=true", timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ GET test failed: {e}")
        return False

def test_form_submission():
    """Test actual form submission"""
    print("\n📝 Testing contact form submission...")

    test_data = {
        "sheetName": "contacts",
        "data": {
            "timestamp": "2025-08-31T12:00:00.000Z",
            "name": "Test User",
            "email": "test@example.com",
            "subject": "Test Submission",
            "message": "This is a test form submission to verify the Google Apps Script is working correctly.",
            "source": "test-script"
        }
    }

    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(SCRIPT_URL, json=test_data, headers=headers, timeout=30)

        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            try:
                result = response.json()
                if result.get('success'):
                    print("✅ Form submission successful!")
                    return True
                else:
                    print(f"❌ Form submission failed: {result.get('error')}")
                    return False
            except json.JSONDecodeError:
                print("❌ Invalid JSON response")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Form submission failed: {e}")
        return False

def test_application_submission():
    """Test application form submission"""
    print("\n📝 Testing application form submission...")

    test_data = {
        "sheetName": "applications",
        "data": {
            "timestamp": "2025-08-31T12:00:00.000Z",
            "type": "developer",
            "name": "Test Developer",
            "email": "developer@example.com",
            "experience": "junior",
            "skills": "Python, JavaScript, React",
            "motivation": "I want to learn and contribute to open source projects.",
            "github": "https://github.com/testuser",
            "source": "test-script"
        }
    }

    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(SCRIPT_URL, json=test_data, headers=headers, timeout=30)

        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            try:
                result = response.json()
                if result.get('success'):
                    print("✅ Application submission successful!")
                    return True
                else:
                    print(f"❌ Application submission failed: {result.get('error')}")
                    return False
            except json.JSONDecodeError:
                print("❌ Invalid JSON response")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Application submission failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Open Build Google Apps Script Integration")
    print("=" * 60)

    tests = [
        ("Health Check", test_health_check),
        ("GET Test Endpoint", test_get_endpoint),
        ("Contact Form Submission", test_form_submission),
        ("Application Form Submission", test_application_submission)
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        result = test_func()
        results.append((test_name, result))

    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)

    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1

    print(f"\nPassed: {passed}/{len(results)} tests")

    if passed == len(results):
        print("🎉 All tests passed! The Google Apps Script is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
