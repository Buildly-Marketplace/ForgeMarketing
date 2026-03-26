#!/usr/bin/env python3
"""
Email Delivery Verification Tool
Helps verify that outreach emails were actually sent via Brevo SMTP
"""

import re
import os
from datetime import datetime, timedelta

def analyze_email_logs(log_file_path):
    """Analyze email delivery logs"""
    
    if not os.path.exists(log_file_path):
        print(f"❌ Log file not found: {log_file_path}")
        return
    
    print("🔍 ANALYZING EMAIL DELIVERY LOGS")
    print("=" * 50)
    
    with open(log_file_path, 'r') as f:
        content = f.read()
    
    # Find all email sends
    sent_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+ - marketing\.buildly_user_outreach - INFO - Email sent via Brevo SMTP to ([^\s]+) \(BCC: ([^)]+)\)'
    
    sent_emails = re.findall(sent_pattern, content)
    
    print(f"📊 TOTAL EMAILS SENT: {len(sent_emails)}")
    print(f"🕐 TIME RANGE: Last 24 hours")
    print()
    
    if sent_emails:
        print("📧 EMAIL DELIVERY DETAILS:")
        print("-" * 80)
        
        # Group by hour for better analysis
        hourly_counts = {}
        
        for timestamp_str, recipient, bcc in sent_emails[-20:]:  # Show last 20
            try:
                # Parse timestamp
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                hour_key = timestamp.strftime('%Y-%m-%d %H:00')
                
                hourly_counts[hour_key] = hourly_counts.get(hour_key, 0) + 1
                
                print(f"  ✅ {timestamp_str} → {recipient} (BCC: {bcc})")
                
            except Exception as e:
                print(f"  ⚠️  Parse error: {e}")
        
        print()
        print("📈 HOURLY DISTRIBUTION:")
        print("-" * 30)
        for hour, count in sorted(hourly_counts.items()):
            print(f"  {hour}: {count} emails")
    
    # Check for failures
    failure_pattern = r'Email send failed|Error sending email|SMTP error'
    failures = re.findall(failure_pattern, content, re.IGNORECASE)
    
    print()
    print(f"❌ FAILURES DETECTED: {len(failures)}")
    
    # Check for bounces or delivery issues
    bounce_pattern = r'bounce|rejected|blocked|spam'
    bounces = re.findall(bounce_pattern, content, re.IGNORECASE)
    
    print(f"📬 POTENTIAL DELIVERY ISSUES: {len(bounces)}")
    
    print()
    print("🎯 VERIFICATION RECOMMENDATIONS:")
    print("-" * 40)
    print("1. Check greg@buildly.io inbox/spam folder")
    print("2. Log into Brevo dashboard for delivery reports")
    print("3. Check recipient spam folders (if you have access)")
    print("4. Monitor bounce/complaint reports in Brevo")
    
    print()
    print("🔗 BREVO VERIFICATION:")
    print("- Login: https://app.brevo.com/")
    print("- Check: Campaigns → Email → Delivery Reports")
    print("- Look for: Recent transactional email activity")

if __name__ == "__main__":
    log_file = "dashboard_progress.log"
    analyze_email_logs(log_file)