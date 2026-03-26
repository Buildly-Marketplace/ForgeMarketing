#!/usr/bin/env python3
"""
Test BCC functionality specifically for greg@open.build
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_bcc_email():
    """Test BCC functionality to greg@open.build"""
    
    print("🔍 Testing BCC functionality to greg@open.build...")
    print("=" * 50)
    
    # Get credentials
    smtp_host = os.getenv('BREVO_SMTP_HOST')
    smtp_port = int(os.getenv('BREVO_SMTP_PORT', '587'))
    smtp_user = os.getenv('BREVO_SMTP_USER')
    smtp_password = os.getenv('BREVO_SMTP_PASSWORD')
    from_email = os.getenv('FROM_EMAIL')
    from_name = os.getenv('FROM_NAME')
    
    subject = "🔍 BCC Test - Open Build Outreach System"
    message = f"""Hello Team,

This is a BCC test for the Open Build Outreach Automation System.

🔍 Test Details:
• Primary recipient: team@open.build
• BCC recipient: greg@open.build
• Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📧 Email Delivery Test:
This email is being sent with team@open.build as the primary recipient and greg@open.build as BCC.

🎯 Expected Results:
1. team@open.build should receive this email normally
2. greg@open.build should receive this email as BCC (won't see BCC in headers)

✅ If greg receives this email:
The BCC functionality is working correctly for outreach emails.

❌ If greg doesn't receive this email:
There may be an issue with BCC handling or email filtering.

Previous outreach emails were sent with the same BCC configuration.

Best regards,
Open Build Outreach System Test
"""
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = f"{from_name} <{from_email}>"
        msg['To'] = "team@open.build"
        msg['Bcc'] = "greg@open.build"  # BCC header
        msg['Subject'] = subject
        
        msg.attach(MIMEText(message, 'plain'))
        
        # Connect and send
        print("🔗 Connecting to Brevo SMTP...")
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        
        print("📤 Sending email with BCC...")
        print("📧 Primary TO: team@open.build")
        print("📧 BCC: greg@open.build")
        
        # Send to both recipients
        recipients = ["team@open.build", "greg@open.build"]
        text = msg.as_string()
        server.sendmail(from_email, recipients, text)
        server.quit()
        
        print("✅ BCC test email sent successfully!")
        print()
        print("🔍 What to check:")
        print("1. team@open.build should receive the email normally")
        print("2. greg@open.build should receive the email as BCC")
        print("3. Greg's copy won't show the BCC header (normal behavior)")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to send BCC test email: {e}")
        return False

if __name__ == "__main__":
    test_bcc_email()
