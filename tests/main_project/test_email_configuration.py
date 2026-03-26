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
        """Generate email content for testing using branded HTML templates"""
        from email_templates import BrandEmailRenderer
        
        brand = BRAND_CONFIGS[brand_key]
        campaign = CAMPAIGN_TYPES[campaign_type]
        
        # Initialize template renderer
        renderer = BrandEmailRenderer()
        
        # Prepare data for template
        template_data = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'analytics': {
                'sessions': '1,234',
                'users': '856',
                'pageviews': '2,856',
                'bounce_rate': '45.2%',
                'emails_sent': '25',
                'open_rate': '28.5%',
                'click_rate': '3.2%'
            },
            'targets_found': '5',
            'emails_sent': '8',
            'responses': '2',
            'daily_targets': '25',
            'success_rate': '94%'
        }
        
        # Render branded email
        email_result = renderer.render_email(brand_key, campaign_type, template_data)
        
        # Add test footer to both HTML and text versions
        test_footer_html = f"""
        <div style="border-top: 2px dashed #ccc; margin-top: 30px; padding-top: 20px; background: #f9f9f9; padding: 20px; border-radius: 8px;">
            <h4 style="color: #666; margin-top: 0;">📧 Test Email Information</h4>
            <p style="font-size: 12px; color: #666; margin: 5px 0;"><strong>Sent:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p style="font-size: 12px; color: #666; margin: 5px 0;"><strong>Brand:</strong> {brand['name']}</p>
            <p style="font-size: 12px; color: #666; margin: 5px 0;"><strong>Campaign:</strong> {campaign['name']}</p>
            <p style="font-size: 12px; color: #666; margin: 5px 0;"><strong>Reply To:</strong> {brand.get('reply_to', brand['from_email'])}</p>
            <p style="font-size: 11px; color: #888; margin-top: 15px; font-style: italic;">This is a test email from the marketing automation system.</p>
        </div>
        """
        
        test_footer_text = f"""

=======================================
📧 TEST EMAIL INFORMATION
=======================================
Sent: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Brand: {brand['name']}
Campaign: {campaign['name']}
Reply To: {brand.get('reply_to', brand['from_email'])}

This is a test email from the marketing automation system.
            """
        
        # Insert test footer before closing body tag in HTML
        html_body = email_result['html'].replace('</body>', f'{test_footer_html}</body>')
        text_body = email_result['text'] + test_footer_text
        
        return email_result['subject'], html_body, text_body
        
        return email_result['subject'], html_body, text_body
    
    def send_test_email(self, brand_key: str, campaign_type: str):
        """Send a test email for specific brand and campaign type"""
        try:
            brand = BRAND_CONFIGS[brand_key]
            subject, html_body, text_body = self.generate_email_content(brand_key, campaign_type)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{brand['from_name']} <{brand['from_email']}>"
            msg['To'] = self.test_email
            msg['Subject'] = f"[TEST] {subject}"
            msg['Reply-To'] = brand.get('reply_to', brand['from_email'])
            
            # Add BCC for testing
            msg['Bcc'] = self.test_email
            
            # Add both plain text and HTML parts
            text_part = MIMEText(text_body, 'plain')
            html_part = MIMEText(html_body, 'html')
            msg.attach(text_part)
            msg.attach(html_part)
            
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