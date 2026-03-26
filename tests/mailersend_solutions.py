#!/usr/bin/env python3
"""
MailerSend Deliverability Solutions
"""

import sys
sys.path.append('/Users/greglind/Projects/Sales and Marketing')

from unified_email_service import UnifiedEmailService

def test_alternative_configurations():
    """Test different configurations to improve deliverability"""
    
    print("🛠️ Testing MailerSend Deliverability Solutions")
    print("=" * 50)
    
    email_service = UnifiedEmailService()
    
    # Solution 1: Test with different from address
    print("\n📧 Solution 1: Testing alternative from address")
    
    # Temporarily modify the from email for testing
    original_from = email_service.mailersend_config['from_email']
    original_name = email_service.mailersend_config['from_name']
    
    # Test with a different from address format
    email_service.mailersend_config['from_email'] = 'hello@buildly.io'  # Different prefix
    email_service.mailersend_config['from_name'] = 'Buildly'  # Shorter name
    
    result1 = email_service.send_email(
        brand='buildly',
        to_email='greg@buildly.io',
        subject='🔧 Buildly Deliverability Test - Alternative From Address',
        body="""This is a deliverability test using an alternative from address.

FROM: hello@buildly.io (instead of team@buildly.io)
TO: greg@buildly.io
SERVICE: MailerSend API

Testing if different from address improves deliverability to same domain.

If you receive this email, the alternative from address works better.

Timestamp: """ + str(__import__('datetime').datetime.now()),
        is_html=False
    )
    
    print(f"Alternative from address: {'✅ Sent' if result1['success'] else '❌ Failed'}")
    if result1['success']:
        print(f"Message ID: {result1['message_id']}")
    
    # Restore original settings
    email_service.mailersend_config['from_email'] = original_from
    email_service.mailersend_config['from_name'] = original_name
    
    # Solution 2: Test with HTML content (sometimes filters plain text differently)
    print(f"\n📧 Solution 2: Testing HTML email format")
    
    html_body = """<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <h2 style="color: #2c3e50;">🔧 Buildly HTML Deliverability Test</h2>
    
    <p>This is an HTML-formatted email to test deliverability improvements.</p>
    
    <ul>
        <li><strong>FROM:</strong> team@buildly.io</li>
        <li><strong>TO:</strong> greg@buildly.io</li>
        <li><strong>SERVICE:</strong> MailerSend API</li>
        <li><strong>FORMAT:</strong> HTML (instead of plain text)</li>
    </ul>
    
    <p>Some email filters treat HTML emails differently than plain text.</p>
    
    <p>If you receive this email, HTML format may improve deliverability.</p>
    
    <p style="color: #7f8c8d; font-size: 0.9em;">
        Timestamp: """ + str(__import__('datetime').datetime.now()) + """
    </p>
</body>
</html>"""
    
    result2 = email_service.send_email(
        brand='buildly',
        to_email='greg@buildly.io',
        subject='🔧 Buildly HTML Deliverability Test',
        body=html_body,
        is_html=True  # HTML format
    )
    
    print(f"HTML format test: {'✅ Sent' if result2['success'] else '❌ Failed'}")
    if result2['success']:
        print(f"Message ID: {result2['message_id']}")
    
    # Solution 3: Temporary Brevo fallback for Buildly
    print(f"\n📧 Solution 3: Testing Brevo fallback for Buildly")
    
    # Temporarily change routing for testing
    original_routing = email_service.service_routing['buildly']
    email_service.service_routing['buildly'] = 'brevo'  # Temporary fallback
    
    result3 = email_service.send_email(
        brand='buildly',
        to_email='greg@buildly.io',
        subject='🔧 Buildly Brevo Fallback Test',
        body="""This is a test using Brevo SMTP as a fallback for Buildly emails.

FROM: team@open.build (via Brevo SMTP)
TO: greg@buildly.io
SERVICE: Brevo SMTP (temporary fallback)

This tests if Brevo delivers better to greg@buildly.io than MailerSend.

If you receive this email, Brevo might be a good temporary fallback.

Timestamp: """ + str(__import__('datetime').datetime.now()),
        is_html=False
    )
    
    print(f"Brevo fallback test: {'✅ Sent' if result3['success'] else '❌ Failed'}")
    
    # Restore original routing
    email_service.service_routing['buildly'] = original_routing
    
    return {
        'alternative_from': result1['success'],
        'html_format': result2['success'],
        'brevo_fallback': result3['success']
    }

def create_deliverability_config():
    """Create an improved configuration for better deliverability"""
    
    print(f"\n🔧 Creating Improved MailerSend Configuration...")
    
    improved_config = {
        'from_email_options': [
            'hello@buildly.io',      # More personal
            'support@buildly.io',    # Support-related
            'updates@buildly.io',    # Update notifications
            'noreply@buildly.io'     # No-reply format
        ],
        'content_improvements': {
            'use_html': True,        # HTML often has better deliverability
            'shorter_subject': True,  # Avoid spam trigger words
            'personal_tone': True    # More conversational content
        },
        'fallback_strategy': {
            'primary': 'mailersend',
            'fallback': 'brevo',
            'trigger_fallback_on_failure': True
        }
    }
    
    print(f"💡 Recommended Configuration:")
    print(f"✅ Alternative from addresses: {improved_config['from_email_options']}")
    print(f"✅ Use HTML format for better filtering")
    print(f"✅ Implement Brevo fallback for delivery failures")
    print(f"✅ Monitor delivery rates and adjust accordingly")
    
    return improved_config

if __name__ == "__main__":
    # Test solutions
    results = test_alternative_configurations()
    
    # Create improved config
    config = create_deliverability_config()
    
    # Summary and next steps
    print(f"\n📊 Solution Test Results:")
    print(f"Alternative from address: {'✅ Working' if results['alternative_from'] else '❌ Failed'}")
    print(f"HTML format: {'✅ Working' if results['html_format'] else '❌ Failed'}")
    print(f"Brevo fallback: {'✅ Working' if results['brevo_fallback'] else '❌ Failed'}")
    
    print(f"\n🎯 Immediate Action Plan:")
    
    if results['brevo_fallback']:
        print(f"1. ✅ Brevo fallback works - consider temporary switch")
        print(f"   • Modify unified_email_service.py routing temporarily")
        print(f"   • Keep MailerSend for external recipients (lindg@mac.com works)")
        
    if results['alternative_from']:
        print(f"2. ✅ Alternative from address works - update configuration")
        print(f"   • Change from 'team@buildly.io' to 'hello@buildly.io'")
        
    if results['html_format']:
        print(f"3. ✅ HTML format works - update email templates")
        print(f"   • Use HTML format for better deliverability")
        
    print(f"\n🔍 Next Steps to Check:")
    print(f"1. Check your email now - you should have received 3 test emails")
    print(f"2. Verify which solution(s) reached your inbox")
    print(f"3. Check lindg@mac.com and greglindtest@gmail.com for external delivery")
    print(f"4. Decide on permanent configuration based on results")