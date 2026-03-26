#!/usr/bin/env python3
"""
Comprehensive Email Configuration Tester
Tests Brevo SMTP configuration for all brands and campaign types
Using verified sender address for all brands
"""

import os
import smtplib
import sys
from datetime import datetime
from pathlib import Path
import json

# Fix email imports
try:
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
except ImportError:
    try:
        from email.MIMEText import MIMEText
        from email.MIMEMultipart import MIMEMultipart
    except ImportError:
        print("❌ Could not import email libraries. Please check Python installation.")
        sys.exit(1)

# Brand configurations - All use verified sender address but different display names
BRAND_CONFIGS = {
    'foundry': {
        'name': 'First City Foundry',
        'from_email': 'team@open.build',  # Verified sender
        'from_name': 'First City Foundry Team',
        'reply_to': 'team@firstcityfoundry.com',
        'website': 'https://www.firstcityfoundry.com',
        'description': 'Supporting innovative startups and entrepreneurs'
    },
    'buildly': {
        'name': 'Buildly',
        'from_email': 'team@open.build',  # Verified sender
        'from_name': 'Buildly Team',
        'reply_to': 'team@buildly.io',
        'website': 'https://buildly.io',
        'description': 'Low-code platform for rapid application development'
    },
    'openbuild': {
        'name': 'Open Build',
        'from_email': 'team@open.build',  # Verified sender
        'from_name': 'Open Build Team',
        'reply_to': 'team@open.build',
        'website': 'https://open.build',
        'description': 'Open source development community'
    },
    'radical': {
        'name': 'Radical Therapy',
        'from_email': 'team@open.build',  # Verified sender
        'from_name': 'Radical Therapy Team',
        'reply_to': 'hello@radicaltherapy.org',
        'website': 'https://radicaltherapy.org',
        'description': 'Mental health and wellness platform'
    },
    'oregonsoftware': {
        'name': 'Oregon Software',
        'from_email': 'team@open.build',  # Verified sender
        'from_name': 'Oregon Software Team',
        'reply_to': 'contact@oregonsoftware.org',
        'website': 'https://oregonsoftware.org',
        'description': 'Software development services'
    }
}

CAMPAIGN_TYPES = {
    'general_outreach': {
        'name': 'General Outreach',
        'subject': 'Partnership Opportunity with {brand_name}',
        'template': 'general_partnership'
    },
    'discovery_campaign': {
        'name': 'Discovery Campaign',
        'subject': 'Exploring Collaboration with {brand_name}',
        'template': 'discovery_outreach'
    },
    'follow_up': {
        'name': 'Follow-up Campaign',
        'subject': 'Following up on our {brand_name} conversation',
        'template': 'follow_up'
    },
    'daily_analytics': {
        'name': 'Daily Analytics Report',
        'subject': '{brand_name} - Daily Analytics Report',
        'template': 'analytics_daily'
    },
    'automation_notification': {
        'name': 'Automation Notification',
        'subject': '{brand_name} - Automation Status Update',
        'template': 'automation_status'
    }
}

class EmailConfigTester:
    def __init__(self, test_email: str = None):
        self.test_email = test_email or "greg@buildly.io"  # Default test email
        self.smtp_config = self.load_smtp_config()
        self.results = []
        
    def load_smtp_config(self):
        """Load SMTP configuration from environment or foundry config"""
        # Try to load from foundry .env first
        foundry_env = Path("/Users/greglind/Projects/Sales and Marketing/websites/foundry-website/.env")
        
        if foundry_env.exists():
            config = {}
            with open(foundry_env, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        config[key] = value
            
            return {
                'host': config.get('BREVO_SMTP_HOST', 'smtp-relay.brevo.com'),
                'port': int(config.get('BREVO_SMTP_PORT', '587')),
                'user': config.get('BREVO_SMTP_USER', ''),
                'password': config.get('BREVO_SMTP_PASSWORD', ''),
            }
        
        # Fallback to environment variables
        return {
            'host': os.getenv('BREVO_SMTP_HOST', 'smtp-relay.brevo.com'),
            'port': int(os.getenv('BREVO_SMTP_PORT', '587')),
            'user': os.getenv('BREVO_SMTP_USER', ''),
            'password': os.getenv('BREVO_SMTP_PASSWORD', ''),
        }
    
    def test_smtp_connection(self):
        """Test basic SMTP connection"""
        try:
            print("🔗 Testing SMTP connection...")
            server = smtplib.SMTP(self.smtp_config['host'], self.smtp_config['port'])
            server.starttls()
            server.login(self.smtp_config['user'], self.smtp_config['password'])
            server.quit()
            print("✅ SMTP connection successful!")
            return True
        except Exception as e:
            print(f"❌ SMTP connection failed: {e}")
            return False
    
    def generate_email_content(self, brand_key: str, campaign_type: str):
        """Generate email content for testing"""
        brand = BRAND_CONFIGS[brand_key]
        campaign = CAMPAIGN_TYPES[campaign_type]
        
        subject = campaign['subject'].format(brand_name=brand['name'])
        
        # Generate appropriate content based on campaign type
        if campaign_type == 'general_outreach':
            body = f"""
Hello!

I hope this email finds you well. I'm reaching out from {brand['name']} ({brand['website']}).

{brand['description']}

We're always looking to connect with like-minded organizations and individuals who share our passion for innovation and growth.

Would you be interested in exploring potential collaboration opportunities?

Best regards,
{brand['from_name']}

---
This is a test email sent on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Testing brand: {brand['name']} 
Campaign type: {campaign['name']}
Reply to: {brand.get('reply_to', brand['from_email'])}
            """
        elif campaign_type == 'discovery_campaign':
            body = f"""
Hi there!

I'm conducting research on potential partnerships for {brand['name']}.

{brand['description']}

I'd love to learn more about your organization and see if there might be synergies between our missions.

Could we schedule a brief 15-minute call to explore this?

Looking forward to hearing from you,
{brand['from_name']}

---
This is a test email sent on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Testing brand: {brand['name']} 
Campaign type: {campaign['name']}
Reply to: {brand.get('reply_to', brand['from_email'])}
            """
        elif campaign_type == 'follow_up':
            body = f"""
Hello again!

I wanted to follow up on my previous message regarding potential collaboration with {brand['name']}.

I understand you're probably busy, but I wanted to make sure my message didn't get lost in your inbox.

If you're interested in learning more, I'd be happy to provide additional details about how we might work together.

No pressure at all - just wanted to check in!

Best,
{brand['from_name']}

---
This is a test email sent on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Testing brand: {brand['name']} 
Campaign type: {campaign['name']}
Reply to: {brand.get('reply_to', brand['from_email'])}
            """
        elif campaign_type == 'daily_analytics':
            body = f"""
Daily Analytics Report - {brand['name']}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 Website Analytics:
• Visitors: 1,234 (+5.2% from yesterday)
• Page views: 2,856 (+3.1% from yesterday)
• Bounce rate: 45.2% (-1.8% from yesterday)

📧 Email Campaign Performance:
• Emails sent: 25
• Open rate: 28.5%
• Click rate: 3.2%

🎯 Outreach Metrics:
• New targets identified: 5
• Outreach emails sent: 8
• Responses received: 2

This is an automated test of the daily analytics email system.

---
{brand['name']} Analytics System
{brand['website']}
Reply to: {brand.get('reply_to', brand['from_email'])}
            """
        elif campaign_type == 'automation_notification':
            body = f"""
Automation Status Update - {brand['name']}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🤖 Automation Status: Active
📈 Daily Targets: 25 contacts processed
✅ Email Delivery: All systems operational
🔄 Data Sync: Complete

Recent Activities:
• Target discovery: 5 new contacts identified
• Email campaigns: 8 messages sent successfully  
• Response tracking: 2 new responses detected
• Analytics update: Daily metrics collected

System Health: All green ✅

This is a test of the automation notification system.

---
{brand['name']} Automation System
Powered by Marketing Hub
Reply to: {brand.get('reply_to', brand['from_email'])}
            """
        
        return subject, body
    
    def send_test_email(self, brand_key: str, campaign_type: str):
        """Send a test email for specific brand and campaign type"""
        try:
            brand = BRAND_CONFIGS[brand_key]
            subject, body = self.generate_email_content(brand_key, campaign_type)
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{brand['from_name']} <{brand['from_email']}>"
            msg['To'] = self.test_email
            msg['Subject'] = f"[TEST] {subject}"
            msg['Reply-To'] = brand.get('reply_to', brand['from_email'])
            
            # Add BCC for testing
            msg['Bcc'] = self.test_email
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_config['host'], self.smtp_config['port'])
            server.starttls()
            server.login(self.smtp_config['user'], self.smtp_config['password'])
            
            # Send to both TO and BCC
            recipients = [self.test_email]
            server.send_message(msg, to_addrs=recipients)
            server.quit()
            
            result = {
                'brand': brand_key,
                'campaign_type': campaign_type,
                'status': 'success',
                'subject': subject,
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"✅ {brand['name']} - {CAMPAIGN_TYPES[campaign_type]['name']}: Sent successfully")
            return result
            
        except Exception as e:
            result = {
                'brand': brand_key,
                'campaign_type': campaign_type,
                'status': 'failed',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            print(f"❌ {brand['name']} - {CAMPAIGN_TYPES[campaign_type]['name']}: {e}")
            return result
    
    def run_comprehensive_test(self):
        """Run comprehensive test of all brands and campaign types"""
        print("🚀 Starting comprehensive email configuration test")
        print(f"📧 Test emails will be sent to: {self.test_email}")
        print("=" * 60)
        
        # Test SMTP connection first
        if not self.test_smtp_connection():
            print("❌ Cannot proceed - SMTP connection failed")
            return
        
        print("\n📬 Testing email delivery for all brands and campaign types...")
        print("=" * 60)
        
        # Test each brand with each campaign type
        for brand_key in BRAND_CONFIGS:
            print(f"\n🎨 Testing brand: {BRAND_CONFIGS[brand_key]['name']}")
            print("-" * 40)
            
            for campaign_type in CAMPAIGN_TYPES:
                result = self.send_test_email(brand_key, campaign_type)
                self.results.append(result)
                
                # Small delay between emails
                import time
                time.sleep(1)
        
        # Generate summary report
        self.generate_summary_report()
    
    def generate_summary_report(self):
        """Generate and save summary report"""
        successful = [r for r in self.results if r['status'] == 'success']
        failed = [r for r in self.results if r['status'] == 'failed']
        
        print("\n" + "=" * 60)
        print("📊 EMAIL CONFIGURATION TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Successful: {len(successful)}")
        print(f"❌ Failed: {len(failed)}")
        print(f"📧 Total tests: {len(self.results)}")
        print(f"📈 Success rate: {(len(successful)/len(self.results)*100):.1f}%")
        
        if failed:
            print("\n❌ Failed tests:")
            for result in failed:
                brand_name = BRAND_CONFIGS[result['brand']]['name']
                campaign_name = CAMPAIGN_TYPES[result['campaign_type']]['name']
                print(f"  • {brand_name} - {campaign_name}: {result['error']}")
        
        # Save detailed results
        report_file = Path(f"email_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_file, 'w') as f:
            json.dump({
                'test_config': {
                    'test_email': self.test_email,
                    'smtp_host': self.smtp_config['host'],
                    'smtp_user': self.smtp_config['user'],
                    'timestamp': datetime.now().isoformat()
                },
                'summary': {
                    'total_tests': len(self.results),
                    'successful': len(successful),
                    'failed': len(failed),
                    'success_rate': len(successful)/len(self.results)*100
                },
                'results': self.results
            }, f, indent=2)
        
        print(f"\n📁 Detailed results saved to: {report_file}")
        print("\nTest complete! Check your email for all test messages.")

def main():
    # Get test email from command line argument or use default
    test_email = sys.argv[1] if len(sys.argv) > 1 else "greg@buildly.io"
    
    print("📧 Email Configuration Tester")
    print("=" * 40)
    print(f"Target email: {test_email}")
    print(f"SMTP server: smtp-relay.brevo.com")
    print(f"Verified sender: team@open.build")
    print("=" * 40)
    
    tester = EmailConfigTester(test_email)
    tester.run_comprehensive_test()

if __name__ == "__main__":
    main()