#!/usr/bin/env python3
"""
Activate Inactive Brands via Campaign API
=========================================

Use the existing campaign API to run target discovery for inactive brands.
"""

import requests
import time

def activate_brand_via_api(brand_key: str, brand_name: str):
    """Activate a brand by running target discovery via the campaign API"""
    print(f"🔍 Activating {brand_name} ({brand_key})...")
    
    try:
        # Execute discovery campaign
        response = requests.post(
            f"http://127.0.0.1:5003/api/campaigns/execute/{brand_key}",
            headers={'Content-Type': 'application/json'},
            json={
                'type': 'discovery',
                'target_count': 10
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"   ✅ Discovery successful: {result.get('message', 'Targets discovered')}")
                
                # Get campaign results
                targets_found = result.get('targets_discovered', 0)
                campaigns_sent = result.get('campaigns_sent', 0)
                
                if targets_found > 0:
                    print(f"   📊 Found {targets_found} new targets")
                if campaigns_sent > 0:
                    print(f"   📧 Sent {campaigns_sent} initial outreach emails")
                    
                return True
            else:
                print(f"   ❌ Discovery failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"   ❌ HTTP Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def check_server_status():
    """Check if the dashboard server is running"""
    try:
        response = requests.get("http://127.0.0.1:5003/api/status", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Activate all inactive brands"""
    print("🎯 Activating Inactive Brands via Campaign API")
    print("=" * 60)
    
    # Check server status
    if not check_server_status():
        print("❌ Dashboard server not running at http://127.0.0.1:5003")
        print("   Please start the server with: python dashboard/app.py")
        return
    
    print("✅ Server is running")
    print()
    
    # Brands to activate
    brands_to_activate = [
        ('buildly', 'Buildly'),
        ('radical', 'Radical Therapy'),
        ('oregonsoftware', 'Oregon Software')
    ]
    
    activated_count = 0
    
    for brand_key, brand_name in brands_to_activate:
        success = activate_brand_via_api(brand_key, brand_name)
        if success:
            activated_count += 1
        
        # Brief pause between activations
        time.sleep(2)
        print()
    
    print("=" * 60)
    print(f"✅ Activation Complete!")
    print(f"📊 Successfully activated {activated_count}/{len(brands_to_activate)} brands")
    print()
    print("🔗 View updated Campaign Manager: http://127.0.0.1:5003/campaigns")
    print("📊 Check Analytics Dashboard: http://127.0.0.1:5003/analytics") 
    
    if activated_count > 0:
        print("🎉 All brands should now show active status with targets!")
    else:
        print("⚠️  No brands were activated - check the logs for details")

if __name__ == "__main__":
    main()