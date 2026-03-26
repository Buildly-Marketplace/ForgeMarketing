#!/usr/bin/env python3
"""
Quick test of branded email templates
Sends one email from each brand to showcase the designs
"""

from test_email_configuration import EmailConfigTester
import time

def test_all_brand_designs():
    """Send one email from each brand to showcase designs"""
    tester = EmailConfigTester('greg@buildly.io')
    
    print("🎨 Testing Branded Email Designs")
    print("=" * 50)
    
    # Test SMTP connection first
    if not tester.test_smtp_connection():
        print("❌ Cannot proceed - SMTP connection failed")
        return
    
    brands_to_test = ['foundry', 'buildly', 'openbuild', 'radical', 'oregonsoftware']
    
    for brand in brands_to_test:
        try:
            print(f"\n📧 Sending {brand.title()} branded email...")
            result = tester.send_test_email(brand, 'general_outreach')
            
            if result['status'] == 'success':
                print(f"✅ {brand.title()}: {result['subject']}")
            else:
                print(f"❌ {brand.title()}: {result.get('error', 'Unknown error')}")
            
            # Small delay between emails
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ {brand.title()}: {e}")
    
    print("\n🎉 Brand design test complete!")
    print("Check your email for 5 different branded email designs")

if __name__ == "__main__":
    test_all_brand_designs()