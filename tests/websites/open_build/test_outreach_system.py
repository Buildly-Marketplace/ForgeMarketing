#!/usr/bin/env python3
"""
Test script for Open Build Outreach Automation email functionality
Tests the Brevo SMTP configuration
"""

import json
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def test_email_config():
    """Test the email configuration with Brevo SMTP"""
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Load configuration
    try:
        email_config = {
            'smtp_host': os.getenv('BREVO_SMTP_HOST'),
            'smtp_port': int(os.getenv('BREVO_SMTP_PORT', '587')),
            'smtp_user': os.getenv('BREVO_SMTP_USER'),
            'smtp_password': os.getenv('BREVO_SMTP_PASSWORD'),
            'from_email': os.getenv('FROM_EMAIL'),
            'from_name': os.getenv('FROM_NAME'),
            'reply_to': os.getenv('REPLY_TO_EMAIL')
        }
        
        # Validate required environment variables
        required_vars = ['smtp_host', 'smtp_user', 'smtp_password', 'from_email', 'from_name', 'reply_to']
        missing = [var for var in required_vars if not email_config.get(var)]
        
        if missing:
            print(f"❌ Missing environment variables: {missing}")
            print("Please check your .env file and ensure all variables are set.")
            return False
            
    except Exception as e:
        print(f"❌ Error loading environment config: {e}")
        return False
    
    # Test email content
    subject = "🚀 Open Build Outreach System - Test Email"
    message = f"""Hello from Open Build!

This is a test email from the Open Build Outreach Automation System.

✅ Brevo SMTP configuration is working correctly
📧 Email sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🎯 System is ready for automated outreach

If you received this email, the outreach automation system is properly configured and ready to start discovering and contacting potential partners, donors, and clients.

Best regards,
Open Build Foundry Team
https://open.build

---
This is an automated test message from the Open Build Outreach System.
"""
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = f"{email_config['from_name']} <{email_config['from_email']}>"
        msg['To'] = email_config['from_email']  # Send to ourselves for testing
        msg['Reply-To'] = email_config['reply_to']
        msg['Subject'] = subject
        
        msg.attach(MIMEText(message, 'plain'))
        
        # Connect to Brevo SMTP
        print("🔗 Connecting to Brevo SMTP server...")
        server = smtplib.SMTP(email_config['smtp_host'], email_config['smtp_port'])
        server.starttls()
        server.login(email_config['smtp_user'], email_config['smtp_password'])
        
        # Send email
        print("📤 Sending test email...")
        text = msg.as_string()
        server.sendmail(email_config['from_email'], [email_config['from_email']], text)
        server.quit()
        
        print("✅ Test email sent successfully!")
        print(f"📧 Check {email_config['from_email']} for the test message")
        return True
        
    except Exception as e:
        print(f"❌ Error sending test email: {e}")
        return False

def test_database_connection():
    """Test database functionality"""
    import sqlite3
    
    try:
        # Test database creation
        conn = sqlite3.connect('test_outreach.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name TEXT,
                created_at TEXT
            )
        """)
        
        cursor.execute("INSERT INTO test_table (name, created_at) VALUES (?, ?)",
                      ("Test Entry", datetime.now().isoformat()))
        
        cursor.execute("SELECT COUNT(*) FROM test_table")
        count = cursor.fetchone()[0]
        
        conn.commit()
        conn.close()
        
        print(f"✅ Database test successful - {count} entries")
        
        # Clean up test database
        import os
        if os.path.exists('test_outreach.db'):
            os.remove('test_outreach.db')
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Open Build Outreach Automation - System Test")
    print("=" * 50)
    
    # Test email configuration
    print("\n📧 Testing email configuration...")
    email_success = test_email_config()
    
    # Test database
    print("\n💾 Testing database functionality...")
    db_success = test_database_connection()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"📧 Email system: {'✅ PASS' if email_success else '❌ FAIL'}")
    print(f"💾 Database system: {'✅ PASS' if db_success else '❌ FAIL'}")
    
    if email_success and db_success:
        print("\n🎉 All systems ready! The outreach automation is configured correctly.")
        print("🚀 You can now run: python outreach_automation.py --run")
    else:
        print("\n⚠️  Some systems failed. Please check the configuration and try again.")
    
    print("\n📝 Next steps:")
    print("1. Run full system test: python outreach_automation.py --report")
    print("2. Start automated outreach: python outreach_automation.py --run")
    print("3. Set up daily automation using setup_outreach.sh")

if __name__ == "__main__":
    main()
