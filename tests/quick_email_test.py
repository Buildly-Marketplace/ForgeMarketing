#!/usr/bin/env python3
"""
Quick Email Test Script
Simple command-line interface to test email configurations
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from test_email_configuration import EmailConfigTester, BRAND_CONFIGS, CAMPAIGN_TYPES

def main():
    print("🚀 Quick Email Configuration Test")
    print("=" * 50)
    
    # Get email address
    if len(sys.argv) > 1:
        test_email = sys.argv[1]
    else:
        test_email = input("Enter test email address (default: greg@buildly.io): ").strip()
        if not test_email:
            test_email = "greg@buildly.io"
    
    print(f"📧 Testing with: {test_email}")
    
    # Show brand options
    print("\n🎨 Available Brands:")
    for i, (key, config) in enumerate(BRAND_CONFIGS.items(), 1):
        print(f"  {i}. {config['name']} ({key})")
    
    # Show campaign options
    print("\n📋 Available Campaign Types:")
    for i, (key, config) in enumerate(CAMPAIGN_TYPES.items(), 1):
        print(f"  {i}. {config['name']} ({key})")
    
    # Quick test menu
    print("\n🎯 Quick Test Options:")
    print("  a. Test all brands with General Outreach")
    print("  b. Test all campaign types with Foundry")
    print("  c. Test single brand/campaign combination")
    print("  d. Run comprehensive test (all combinations)")
    
    choice = input("\nEnter your choice (a/b/c/d): ").strip().lower()
    
    tester = EmailConfigTester(test_email)
    
    # Test SMTP connection first
    print("\n🔗 Testing SMTP connection...")
    if not tester.test_smtp_connection():
        print("❌ SMTP connection failed. Please check credentials.")
        return
    
    print("✅ SMTP connection successful!")
    
    if choice == 'a':
        print(f"\n📧 Testing all brands with General Outreach...")
        for brand_key in BRAND_CONFIGS:
            result = tester.send_test_email(brand_key, 'general_outreach')
    
    elif choice == 'b':
        print(f"\n📧 Testing all campaign types with Foundry...")
        for campaign_key in CAMPAIGN_TYPES:
            result = tester.send_test_email('foundry', campaign_key)
    
    elif choice == 'c':
        brand_list = list(BRAND_CONFIGS.keys())
        campaign_list = list(CAMPAIGN_TYPES.keys())
        
        print(f"\nSelect brand (1-{len(brand_list)}): ", end="")
        try:
            brand_idx = int(input()) - 1
            brand_key = brand_list[brand_idx]
        except (ValueError, IndexError):
            print("Invalid brand selection")
            return
        
        print(f"Select campaign type (1-{len(campaign_list)}): ", end="")
        try:
            campaign_idx = int(input()) - 1
            campaign_key = campaign_list[campaign_idx]
        except (ValueError, IndexError):
            print("Invalid campaign selection")
            return
        
        print(f"\n📧 Testing {BRAND_CONFIGS[brand_key]['name']} - {CAMPAIGN_TYPES[campaign_key]['name']}...")
        result = tester.send_test_email(brand_key, campaign_key)
    
    elif choice == 'd':
        print(f"\n📧 Running comprehensive test...")
        tester.run_comprehensive_test()
        return
    
    else:
        print("Invalid choice")
        return
    
    print(f"\n✅ Test completed! Check {test_email} for test messages.")

if __name__ == "__main__":
    main()