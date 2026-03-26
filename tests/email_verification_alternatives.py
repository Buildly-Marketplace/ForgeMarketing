#!/usr/bin/env python3
"""
Email Audit Trail System
Creates local copies of all sent emails for verification purposes
"""

import os
import json
from datetime import datetime

def create_email_audit_system():
    """Create an audit system that logs all email attempts"""
    
    audit_dir = "email_audit_logs"
    if not os.path.exists(audit_dir):
        os.makedirs(audit_dir)
    
    # Create audit log entry
    audit_entry = {
        "timestamp": datetime.now().isoformat(),
        "system_status": "operational",
        "smtp_server": "smtp-relay.brevo.com",
        "authentication": "successful",
        "queue_status": "accepting_emails",
        "diagnosis": {
            "smtp_level": "✅ Working - emails queued successfully",
            "brevo_level": "⚠️ Unknown - need dashboard verification", 
            "delivery_level": "❌ Not confirmed - no emails received",
            "likely_issues": [
                "Brevo account limits reached",
                "Domain authentication missing", 
                "Emails going to spam",
                "Recipient domain blocking"
            ]
        },
        "test_emails_sent": [
            {
                "recipient": "greg@buildly.io",
                "queue_id": "202510052024.31196800692@smtp-relay.sendinblue.com",
                "status": "queued"
            },
            {
                "recipient": "greg.lind.testing@gmail.com", 
                "queue_id": "202510052024.13258438279@smtp-relay.sendinblue.com",
                "status": "queued"
            },
            {
                "recipient": "greg@foundry.dev",
                "queue_id": "202510052024.29546080761@smtp-relay.sendinblue.com", 
                "status": "queued"
            }
        ],
        "campaign_emails": {
            "total_attempted": 27,
            "smtp_accepted": 27,
            "smtp_rejected": 0,
            "delivery_confirmed": 0
        },
        "recommendations": [
            "1. Login to Brevo dashboard immediately",
            "2. Check for account suspension/limits", 
            "3. Verify domain authentication",
            "4. Check bounce/complaint reports",
            "5. Consider switching to verified sender domain"
        ]
    }
    
    # Save audit log
    audit_file = f"{audit_dir}/email_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(audit_file, 'w') as f:
        json.dump(audit_entry, f, indent=2)
    
    print(f"📋 Email audit log created: {audit_file}")
    return audit_file

def create_alternative_verification_method():
    """Create alternative methods to verify email delivery"""
    
    print("\n🔧 ALTERNATIVE EMAIL VERIFICATION METHODS")
    print("=" * 60)
    
    methods = [
        {
            "method": "Webhook Delivery Notifications",
            "description": "Set up Brevo webhooks to get delivery confirmations",
            "implementation": "Configure webhook URL in Brevo dashboard",
            "pros": "Real-time delivery status",
            "cons": "Requires public endpoint setup"
        },
        {
            "method": "Local Email Archive",
            "description": "Save copy of every email to local file system",
            "implementation": "Modify outreach system to create local copies",
            "pros": "Always have proof of what was sent",
            "cons": "Doesn't confirm delivery"
        },
        {
            "method": "Test with Known Working Email",
            "description": "Send to Gmail/Yahoo accounts you control",
            "implementation": "Use personal email for testing",
            "pros": "Easy to verify receipt", 
            "cons": "Different from target domain"
        },
        {
            "method": "SMTP Logging Enhancement",
            "description": "Capture detailed SMTP conversation logs", 
            "implementation": "Enable full SMTP debugging",
            "pros": "See exact server responses",
            "cons": "Only shows SMTP acceptance, not delivery"
        }
    ]
    
    for i, method in enumerate(methods, 1):
        print(f"\n{i}. {method['method']}")
        print(f"   📝 {method['description']}")
        print(f"   🔧 Implementation: {method['implementation']}")
        print(f"   ✅ Pros: {method['pros']}")
        print(f"   ❌ Cons: {method['cons']}")

def implement_email_archive():
    """Implement local email archiving system"""
    
    archive_code = '''
# Add this to the BuildlyUserOutreach class send_email method:

def send_email_with_archive(self, user, message, preview_only=False, bcc_email=None):
    """Send email and create local archive copy"""
    
    # Create archive directory
    archive_dir = "sent_emails_archive"
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    
    # Generate archive filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_email = user.email.replace("@", "_at_").replace(".", "_")
    archive_file = f"{archive_dir}/email_{timestamp}_{safe_email}.txt"
    
    # Create archive content
    archive_content = f"""
EMAIL ARCHIVE - {timestamp}
{'='*50}
TO: {user.email}
BCC: {bcc_email or 'None'}
SUBJECT: {message.get('subject', 'No Subject')}
PREVIEW_ONLY: {preview_only}

MESSAGE BODY:
{'-'*30}
{message.get('body', 'No Body')}
{'-'*30}

SMTP STATUS: {'WOULD SEND' if preview_only else 'ATTEMPTING SEND'}
TIMESTAMP: {datetime.now().isoformat()}
"""
    
    # Save archive
    with open(archive_file, 'w') as f:
        f.write(archive_content)
    
    print(f"📁 Email archived: {archive_file}")
    
    # Continue with normal send process
    return self.send_email(user, message, preview_only, bcc_email)
'''
    
    print("\n💾 EMAIL ARCHIVE IMPLEMENTATION:")
    print("=" * 50) 
    print(archive_code)

if __name__ == "__main__":
    audit_file = create_email_audit_system()
    create_alternative_verification_method()
    implement_email_archive()
    
    print(f"\n🎯 SUMMARY:")
    print("=" * 30)
    print("✅ SMTP is working (emails queued)")
    print("❌ Delivery not confirmed (emails not received)")
    print("🔍 Need to check Brevo dashboard")
    print(f"📋 Audit log saved: {audit_file}")
    print("\n💡 NEXT STEPS:")
    print("1. Login to https://app.brevo.com/")
    print("2. Check transactional email statistics")
    print("3. Look for bounce/delivery reports")
    print("4. Verify account status and limits")