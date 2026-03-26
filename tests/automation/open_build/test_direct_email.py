#!/usr/bin/env python3
"""
Direct email test to greg@open.build to troubleshoot email delivery
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_direct_email():
    """Send a direct test email to greg@open.build"""
    
    print("🔍 Testing direct email to greg@open.build...")
    print("=" * 50)
    
    # Get credentials from environment
    smtp_host = os.getenv('BREVO_SMTP_HOST')
    smtp_port = int(os.getenv('BREVO_SMTP_PORT', '587'))
    smtp_user = os.getenv('BREVO_SMTP_USER')
    smtp_password = os.getenv('BREVO_SMTP_PASSWORD')
    from_email = os.getenv('FROM_EMAIL')
    from_name = os.getenv('FROM_NAME')
    
    print(f"📧 SMTP Host: {smtp_host}")
    print(f"📧 SMTP Port: {smtp_port}")
    print(f"📧 SMTP User: {smtp_user}")
    print(f"📧 From Email: {from_email}")
    print()
    
    # Test message
    subject = "🔍 Direct Email Test - Open Build Outreach System"
    message = f"""Hello Greg,

This is a direct email test from the Open Build Outreach Automation System.

🔍 Test Details:
• Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
• SMTP Server: {smtp_host}:{smtp_port}
• From: {from_email}
• Authentication: Brevo SMTP

🎯 Purpose:
Testing direct email delivery to greg@open.build to troubleshoot why you didn't receive the outreach emails.

📊 Previous Run Results:
The system logged successful email sends, but you reported not receiving them. This test will help identify if:
1. Emails are being sent but going to spam
2. There's an issue with the recipient address
3. There's a delivery delay
4. There's an SMTP configuration issue

✅ If you receive this email:
The email system is working correctly, and previous emails may have gone to spam or been delayed.

❌ If you don't receive this email:
There may be an issue with the SMTP configuration or email delivery.

Next Steps:
1. Check your spam/junk folder
2. Verify greg@open.build is the correct email address
3. Check if your email provider is blocking emails from team@open.build

Best regards,
Open Build Outreach Automation System
team@open.build

---
This is a test message to troubleshoot email delivery issues.
"""
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = f"{from_name} <{from_email}>"
        msg['To'] = "greg@open.build"
        msg['Subject'] = subject
        
        msg.attach(MIMEText(message, 'plain'))
        
        # Connect and send
        print("🔗 Connecting to Brevo SMTP...")
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        
        print("🔐 Authenticating...")
        server.login(smtp_user, smtp_password)
        
        print("📤 Sending test email to greg@open.build...")
        text = msg.as_string()
        server.sendmail(from_email, ["greg@open.build"], text)
        server.quit()
        
        print("✅ Direct test email sent successfully!")
        print("📧 Sent to: greg@open.build")
        print()
        print("🔍 Troubleshooting next steps:")
        print("1. Check your inbox for the test email")
        print("2. Check your spam/junk folder")
        print("3. Verify greg@open.build is correct")
        print("4. If you receive this but not the previous emails, they may have been filtered")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to send direct test email: {e}")
        print()
        print("🔍 Possible issues:")
        print("1. SMTP credentials may be incorrect")
        print("2. Network connectivity issues")
        print("3. Brevo account limitations")
        print("4. Email address formatting issues")
        
        return False

if __name__ == "__main__":
    test_direct_email()
