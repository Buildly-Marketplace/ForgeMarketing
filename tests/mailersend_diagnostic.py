#!/usr/bin/env python3
"""
MailerSend Deliverability Diagnostic Tool
"""

import sys
import requests
import json
from datetime import datetime

# Add project path
sys.path.append('/Users/greglind/Projects/Sales and Marketing')
from unified_email_service import UnifiedEmailService

def test_mailersend_deliverability():
    """Test MailerSend deliverability with different configurations"""
    
    print("🔍 MailerSend Deliverability Diagnostic")
    print("=" * 45)
    
    email_service = UnifiedEmailService()
    
    # Test 1: Current configuration (team@buildly.io)
    print("\n📧 Test 1: Current from address (team@buildly.io)")
    result1 = email_service.send_email(
        brand='buildly',
        to_email='lindg@mac.com',  # Different recipient to avoid filters
        subject='🔍 MailerSend Deliverability Test #1',
        body="""This is a deliverability test for MailerSend.

From: team@buildly.io
To: lindg@mac.com
Service: MailerSend API

If you receive this, the current configuration is working for lindg@mac.com.

Test timestamp: """ + str(datetime.now()),
        is_html=False
    )
    
    print(f"Result 1: {'✅ Sent' if result1['success'] else '❌ Failed'}")
    if result1['success']:
        print(f"Message ID: {result1['message_id']}")
    else:
        print(f"Error: {result1.get('error')}")
    
    # Test 2: Try different Gmail address
    print(f"\n📧 Test 2: Testing to Gmail address")
    result2 = email_service.send_email(
        brand='buildly',
        to_email='greglindtest@gmail.com',  # Gmail address for testing
        subject='🔍 MailerSend Gmail Deliverability Test',
        body="""This is a Gmail deliverability test for MailerSend.

From: team@buildly.io  
To: greglindtest@gmail.com
Service: MailerSend API

Testing if MailerSend delivers better to Gmail addresses.

Test timestamp: """ + str(datetime.now()),
        is_html=False
    )
    
    print(f"Result 2: {'✅ Sent' if result2['success'] else '❌ Failed'}")
    if result2['success']:
        print(f"Message ID: {result2['message_id']}")
    
    # Test 3: Brevo comparison
    print(f"\n📬 Test 3: Brevo control test (to greg@buildly.io)")
    result3 = email_service.send_email(
        brand='foundry',  # Routes to Brevo
        to_email='greg@buildly.io',
        subject='🔍 Brevo Deliverability Control Test',
        body="""This is a control test using Brevo SMTP.

From: team@open.build (via Brevo)
To: greg@buildly.io
Service: Brevo SMTP

This should arrive in your inbox as it has been working.

Test timestamp: """ + str(datetime.now()),
        is_html=False
    )
    
    print(f"Result 3: {'✅ Sent' if result3['success'] else '❌ Failed'}")
    
    # Summary and recommendations
    print(f"\n📊 Diagnostic Summary:")
    print(f"MailerSend → lindg@mac.com: {'✅' if result1['success'] else '❌'}")
    print(f"MailerSend → Gmail: {'✅' if result2['success'] else '❌'}")
    print(f"Brevo → greg@buildly.io: {'✅' if result3['success'] else '❌'}")
    
    print(f"\n💡 Common MailerSend Deliverability Issues:")
    print(f"1. Domain reputation: buildly.io might be filtered by some providers")
    print(f"2. Email content: 'Team' emails often filtered as promotional")
    print(f"3. SPF/DKIM: buildly.io domain records might not include MailerSend")
    print(f"4. Rate limiting: New MailerSend accounts have deliverability ramp-up")
    print(f"5. Recipient filtering: greg@buildly.io might filter external emails to same domain")
    
    return {
        'mailersend_mac': result1['success'],
        'mailersend_gmail': result2['success'],
        'brevo_control': result3['success']
    }

def check_mailersend_logs():
    """Check MailerSend delivery logs via API"""
    
    print(f"\n🔍 Checking MailerSend Delivery Logs...")
    
    token = 'mlsn.<your-mailersend-api-token>'
    
    # Try to get activity logs
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Get recent activity (last 24 hours)
        activity_url = 'https://api.mailersend.com/v1/activity'
        response = requests.get(activity_url, headers=headers)
        
        print(f"Activity API Status: {response.status_code}")
        
        if response.status_code == 200:
            activity_data = response.json()
            print(f"Recent activity found: {len(activity_data.get('data', []))} events")
            
            # Show recent deliveries
            for event in activity_data.get('data', [])[:5]:
                event_type = event.get('type', 'unknown')
                email = event.get('email', {}).get('recipient', {}).get('email', 'unknown')
                timestamp = event.get('timestamp', 'unknown')
                print(f"  • {event_type}: {email} at {timestamp}")
        else:
            print(f"Could not fetch activity: {response.text}")
            
    except Exception as e:
        print(f"Error checking logs: {e}")

if __name__ == "__main__":
    # Run deliverability tests
    results = test_mailersend_deliverability()
    
    # Check logs
    check_mailersend_logs()
    
    # Recommendations
    print(f"\n🛠️ Recommended Solutions:")
    
    if not results['mailersend_mac'] or not results['mailersend_gmail']:
        print(f"❌ MailerSend deliverability issues detected")
        print(f"")
        print(f"Option 1: Configure MailerSend domain verification")
        print(f"  • Add buildly.io to MailerSend verified domains")
        print(f"  • Set up SPF/DKIM records for buildly.io")
        print(f"")
        print(f"Option 2: Use alternative from address")
        print(f"  • Change from 'team@buildly.io' to verified domain")
        print(f"  • Use 'noreply@mailersend-domain.com' format")
        print(f"")
        print(f"Option 3: Switch Buildly back to Brevo (temporary)")
        print(f"  • Modify routing to use Brevo for Buildly until domain is verified")
        print(f"")
    else:
        print(f"✅ MailerSend appears to be working for test addresses")
        print(f"Issue might be specific to greg@buildly.io filtering")
        
    print(f"\nNext steps:")
    print(f"1. Check lindg@mac.com and greglindtest@gmail.com inboxes")
    print(f"2. Verify domain settings in MailerSend dashboard")
    print(f"3. Consider temporary Brevo fallback for critical emails")