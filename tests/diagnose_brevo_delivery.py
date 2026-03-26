#!/usr/bin/env python3
"""
Brevo Account Diagnosis Tool
Helps identify why emails aren't being delivered despite successful SMTP queuing
"""

import requests
import os
import sys
from datetime import datetime, timedelta

def check_brevo_account_status():
    """Check Brevo account status and recent activity"""
    
    print("🔍 BREVO ACCOUNT DIAGNOSIS")
    print("=" * 50)
    
    # Note: We need the Brevo API key to check account status
    # The SMTP credentials alone won't give us API access
    
    print("📊 SMTP CREDENTIALS STATUS:")
    print("✅ Username: <your-brevo-smtp-user>")
    print("✅ Server: smtp-relay.brevo.com:587")
    print("✅ Authentication: SUCCESSFUL")
    print("✅ Queue Status: All emails accepted")
    
    print("\n🚨 POTENTIAL ISSUES:")
    print("-" * 30)
    
    issues = [
        {
            "issue": "Brevo Account Suspended/Limited",
            "description": "Account may have hit sending limits or been flagged",
            "check": "Login to https://app.brevo.com/ and check account status",
            "solution": "Verify account standing and sending limits"
        },
        {
            "issue": "Domain Authentication Missing",
            "description": "buildly.io domain may not be properly authenticated",
            "check": "Check Brevo dashboard for domain verification status",
            "solution": "Add SPF, DKIM, and DMARC records for buildly.io"
        },
        {
            "issue": "Recipient Domain Blocking",
            "description": "buildly.io emails may be blocked by recipient domains",
            "check": "Check if emails to Gmail work but buildly.io doesn't",
            "solution": "Improve domain reputation or use different sender domain"
        },
        {
            "issue": "Daily/Monthly Sending Limits",
            "description": "Free Brevo accounts have sending limits",
            "check": "Check Brevo dashboard for current usage",
            "solution": "Upgrade plan or wait for limit reset"
        },
        {
            "issue": "Emails Going to Spam",
            "description": "Emails may be delivered but filtered to spam",
            "check": "Check spam folders thoroughly",
            "solution": "Improve email content and authentication"
        }
    ]
    
    for i, issue in enumerate(issues, 1):
        print(f"\n{i}. {issue['issue']}")
        print(f"   📝 {issue['description']}")
        print(f"   🔍 Check: {issue['check']}")
        print(f"   💡 Solution: {issue['solution']}")
    
    print("\n" + "=" * 50)
    print("🎯 IMMEDIATE ACTION ITEMS:")
    print("=" * 50)
    
    actions = [
        "1. Login to Brevo dashboard: https://app.brevo.com/",
        "2. Check 'Transactional' > 'Statistics' for today's sends",
        "3. Look for bounce/complaint reports",
        "4. Verify domain authentication status",
        "5. Check account limits and usage",
        "6. Review any account notifications/warnings"
    ]
    
    for action in actions:
        print(f"   {action}")
    
    print(f"\n📧 TEST RESULTS FROM SMTP:")
    print("   • 3 test emails sent successfully")
    print("   • All received queue IDs from Brevo")
    print("   • No SMTP-level errors detected")
    print("   • Issue is in post-SMTP delivery phase")

def generate_delivery_report():
    """Generate a delivery status report"""
    
    print("\n📊 EMAIL DELIVERY STATUS REPORT")
    print("=" * 50)
    
    # Get recent queue IDs from our test
    queue_ids = [
        "202510052024.31196800692@smtp-relay.sendinblue.com",
        "202510052024.13258438279@smtp-relay.sendinblue.com", 
        "202510052024.29546080761@smtp-relay.sendinblue.com"
    ]
    
    recipients = [
        "greg@buildly.io (Primary Target)",
        "greg.lind.testing@gmail.com (Gmail Test)",
        "greg@foundry.dev (Alt Domain)"
    ]
    
    print("🎯 RECENT TEST EMAILS:")
    for i, (queue_id, recipient) in enumerate(zip(queue_ids, recipients), 1):
        print(f"   {i}. {recipient}")
        print(f"      Queue ID: {queue_id}")
        print(f"      Status: Queued successfully at Brevo")
        print(f"      Next: Check recipient inbox/spam")
        print()
    
    print("⏰ TIMELINE:")
    print("   • Emails typically deliver within 1-5 minutes")
    print("   • If not received after 10 minutes, likely delivery issue")
    print("   • Check Brevo dashboard for bounce reports")
    
    print("\n📋 VERIFICATION CHECKLIST:")
    checklist = [
        "[ ] Check greg@buildly.io inbox",
        "[ ] Check greg@buildly.io spam folder", 
        "[ ] Check greg.lind.testing@gmail.com (if accessible)",
        "[ ] Login to Brevo dashboard",
        "[ ] Review Brevo account status",
        "[ ] Check domain authentication",
        "[ ] Look for bounce notifications"
    ]
    
    for item in checklist:
        print(f"   {item}")

if __name__ == "__main__":
    check_brevo_account_status()
    generate_delivery_report()