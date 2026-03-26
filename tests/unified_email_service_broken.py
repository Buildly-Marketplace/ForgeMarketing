#!/usr/bin/env python3
"""
Unified Email Service
Routes emails to correct service based on brand:
- Buildly → MailerSend API  
- Others → Brevo SMTP
"""

import os
imp        response = requests.post(self.mailersend_config['api_url'], json=email_data, headers=headers)
        
        if response.status_code == 202:
            # MailerSend returns empty body on success, message ID is in headers
            message_id = response.headers.get('x-message-id', 'N/A')
            return {
                'success': True,
                'service': 'mailersend',
                'message_id': message_id
            }
        else:
            raise Exception(f"MailerSend API error: {response.status_code} - {response.text}")ts
import json
import smtplib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from email_templates import BrandEmailRenderer

# Import existing configurations
try:
    from test_email_configuration import BRAND_CONFIGS, CAMPAIGN_TYPES
except ImportError:
    # Fallback configurations if import fails
    BRAND_CONFIGS = {
        'foundry': {
            'name': 'First City Foundry',
            'from_email': 'team@open.build',
            'from_name': 'First City Foundry Team',
            'reply_to': 'team@firstcityfoundry.com',
            'website': 'https://www.firstcityfoundry.com',
            'description': 'Supporting innovative startups and entrepreneurs'
        }
    }
    CAMPAIGN_TYPES = {
        'general_outreach': {'name': 'General Outreach'},
        'daily_analytics': {'name': 'Daily Analytics Report'}
    }

class UnifiedEmailService:
    """Unified email service that routes emails based on brand guidelines"""
    
    def __init__(self):
        self.renderer = BrandEmailRenderer()
        
        # Brand-to-service routing per BUILDLY_WORKING_GUIDELINES.md
        self.service_routing = {
            'buildly': 'mailersend',
            'foundry': 'brevo', 
            'open_build': 'brevo',
            'openbuild': 'brevo',
            'oregonsoftware': 'brevo',
            'radical_therapy': 'brevo'
        }
        
        # Load service configurations
        self.mailersend_config = self._load_mailersend_config()
        self.brevo_config = self._load_brevo_config()
        
        print(f"📧 Email Service Initialized:")
        print(f"   • MailerSend: {'✅ Configured' if self.mailersend_config['api_token'] else '❌ Missing Token'}")
        print(f"   • Brevo SMTP: {'✅ Configured' if self.brevo_config['user'] else '❌ Missing Config'}")
        
    def _load_mailersend_config(self) -> Dict[str, Any]:
        """Load MailerSend API configuration"""
        return {
            'api_token': os.getenv('MAILERSEND_API_TOKEN', 'mlsn.<your-mailersend-api-token>'),
            'api_url': 'https://api.mailersend.com/v1/email',
            'from_email': 'team@buildly.io',
            'from_name': 'Buildly Team'
        }
        
    def _load_brevo_config(self) -> Dict[str, Any]:
        """Load Brevo SMTP configuration from foundry .env file"""
        foundry_env = Path("/Users/greglind/Projects/Sales and Marketing/websites/foundry-website/.env")
        
        if foundry_env.exists():
            config = {}
            try:
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
                    'from_email': 'team@open.build'
                }
            except Exception as e:
                print(f"⚠️ Error reading foundry .env: {e}")
        
        # Fallback to environment variables
        return {
            'host': os.getenv('BREVO_SMTP_HOST', 'smtp-relay.brevo.com'),
            'port': int(os.getenv('BREVO_SMTP_PORT', '587')),
            'user': os.getenv('BREVO_SMTP_USER', ''),
            'password': os.getenv('BREVO_SMTP_PASSWORD', ''),
            'from_email': 'team@open.build'
        }
    
    def send_email(self, brand: str, to_email: str, subject: str, body: str, 
                   is_html: bool = False, bcc_email: Optional[str] = None) -> Dict[str, Any]:
        """Send email using correct service based on brand routing"""
        
        service_name = self.service_routing.get(brand.lower(), 'brevo')
        
        try:
            if service_name == 'mailersend':
                return self._send_via_mailersend(to_email, subject, body, is_html, bcc_email)
            else:
                return self._send_via_brevo(to_email, subject, body, is_html, bcc_email)
                
        except Exception as e:
            print(f"❌ Email send failed for {brand}: {e}")
            return {
                'success': False,
                'error': str(e),
                'service': service_name
            }
    
    def _send_via_mailersend(self, to_email: str, subject: str, body: str, 
                           is_html: bool = False, bcc_email: Optional[str] = None) -> Dict[str, Any]:
        """Send email via MailerSend API"""
        
        if not self.mailersend_config['api_token']:
            raise Exception("MailerSend API token not configured! Please add MAILERSEND_API_TOKEN to environment or update _load_mailersend_config()")
        
        # Prepare email data
        email_data = {
            "from": {
                "email": self.mailersend_config['from_email'],
                "name": self.mailersend_config['from_name']
            },
            "to": [{
                "email": to_email
            }],
            "subject": subject
        }
        
        # Add content based on type
        if is_html:
            email_data["html"] = body
            email_data["text"] = self._html_to_text(body)
        else:
            email_data["text"] = body
        
        # Add BCC if provided (but not if same as recipient)
        if bcc_email and bcc_email.lower() != to_email.lower():
            email_data["bcc"] = [{"email": bcc_email}]
        
        # Send via API
        headers = {
            'Authorization': f'Bearer {self.mailersend_config["api_token"]}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(self.mailersend_config['api_url'], json=email_data, headers=headers)
        
        if response.status_code == 202:
            # MailerSend returns empty body on success, message ID is in headers
            message_id = response.headers.get('x-message-id', 'N/A')
            return {
                'success': True,
                'service': 'mailersend',
                'message_id': message_id
            }
        else:
            raise Exception(f"MailerSend API error: {response.status_code} - {response.text}")
    
    def _send_via_brevo(self, to_email: str, subject: str, body: str, 
                       is_html: bool = False, bcc_email: Optional[str] = None) -> Dict[str, Any]:
        """Send email via Brevo SMTP"""
        
        if not self.brevo_config['user'] or not self.brevo_config['password']:
            raise Exception("Brevo SMTP credentials not configured!")
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = self.brevo_config['from_email']
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add BCC if provided
        if bcc_email:
            msg['Bcc'] = bcc_email
        
        # Add content
        if is_html:
            msg.attach(MIMEText(self._html_to_text(body), 'plain'))
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))
        
        # Send via SMTP
        recipients = [to_email]
        if bcc_email:
            recipients.append(bcc_email)
        
        server = smtplib.SMTP(self.brevo_config['host'], self.brevo_config['port'])
        server.starttls()
        server.login(self.brevo_config['user'], self.brevo_config['password'])
        server.sendmail(self.brevo_config['from_email'], recipients, msg.as_string())
        server.quit()
        
        return {
            'success': True,
            'service': 'brevo',
            'recipients': recipients
        }
    
    def _html_to_text(self, html: str) -> str:
        """Convert HTML to plain text"""
        # Remove HTML tags
        clean = re.compile('<.*?>')
        return re.sub(clean, '', html).strip()

    def send_branded_email(
        self, 
        brand_key: str,
        campaign_type: str,
        to_email: str,
        custom_data: Optional[Dict[str, Any]] = None,
        bcc_emails: Optional[List[str]] = None
    ) -> bool:
        """
        Send a branded email using the appropriate template and service
        
        Args:
            brand_key: Brand identifier (foundry, buildly, etc.)
            campaign_type: Type of email campaign
            to_email: Recipient email address
            custom_data: Additional data for template rendering
            bcc_emails: List of BCC email addresses
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            if brand_key not in BRAND_CONFIGS:
                raise ValueError(f"Unknown brand: {brand_key}")
            
            brand = BRAND_CONFIGS[brand_key]
            
            # Prepare template data
            template_data = {
                'brand_name': brand['name'],
                'subtitle': CAMPAIGN_TYPES.get(campaign_type, {}).get('name', 'Marketing Communication'),
                'description': brand['description'],
                'from_name': brand['from_name'],
                'website': brand['website'],
                'date': datetime.now().strftime('%Y-%m-%d'),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'unsubscribe_url': f"{brand['website']}/unsubscribe"
            }
            
            # Add custom data if provided
            if custom_data:
                template_data.update(custom_data)
            
            # Render branded email
            email_result = self.renderer.render_email(brand_key, campaign_type, template_data)
            
            # Create MIME message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{brand['from_name']} <{brand['from_email']}>"
            msg['To'] = to_email
            msg['Subject'] = email_result['subject']
            msg['Reply-To'] = brand.get('reply_to', brand['from_email'])
            
            # Add BCC if provided
            if bcc_emails:
                msg['Bcc'] = ', '.join(bcc_emails)
            
            # Add both text and HTML parts
            text_part = MIMEText(email_result['text'], 'plain')
            html_part = MIMEText(email_result['html'], 'html')
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_config['host'], self.smtp_config['port']) as server:
                server.starttls()
                server.login(self.smtp_config['user'], self.smtp_config['password'])
                
                # Send to all recipients (TO + BCC)
                recipients = [to_email]
                if bcc_emails:
                    recipients.extend(bcc_emails)
                
                server.send_message(msg, to_addrs=recipients)
            
            print(f"✅ Branded email sent: {brand['name']} -> {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send branded email: {e}")
            return False
    
    def send_outreach_email(
        self,
        brand_key: str,
        target_name: str,
        target_email: str,
        target_organization: str = "",
        custom_message: Optional[str] = None,
        bcc_emails: Optional[List[str]] = None
    ) -> bool:
        """
        Send a branded outreach email
        
        Args:
            brand_key: Brand identifier
            target_name: Name of the person being contacted
            target_email: Target's email address
            target_organization: Target's organization name
            custom_message: Custom message to include
            bcc_emails: List of BCC email addresses
            
        Returns:
            bool: True if sent successfully
        """
        custom_data = {
            'target_name': target_name,
            'target_organization': target_organization,
            'custom_message': custom_message or '',
            'subtitle': f'Partnership Opportunity - {target_organization or target_name}'
        }
        
        return self.send_branded_email(
            brand_key=brand_key,
            campaign_type='general_outreach',
            to_email=target_email,
            custom_data=custom_data,
            bcc_emails=bcc_emails
        )
    
    def send_analytics_email(
        self,
        brand_key: str,
        recipient_email: str,
        analytics_data: Dict[str, Any],
        bcc_emails: Optional[List[str]] = None
    ) -> bool:
        """
        Send a branded daily analytics email
        
        Args:
            brand_key: Brand identifier
            recipient_email: Recipient email address
            analytics_data: Analytics data to include in email
            bcc_emails: List of BCC email addresses
            
        Returns:
            bool: True if sent successfully
        """
        return self.send_branded_email(
            brand_key=brand_key,
            campaign_type='daily_analytics',
            to_email=recipient_email,
            custom_data={'analytics': analytics_data},
            bcc_emails=bcc_emails
        )
    
    def send_follow_up_email(
        self,
        brand_key: str,
        target_name: str,
        target_email: str,
        original_subject: str = "",
        bcc_emails: Optional[List[str]] = None
    ) -> bool:
        """
        Send a branded follow-up email
        
        Args:
            brand_key: Brand identifier
            target_name: Name of the person being contacted
            target_email: Target's email address
            original_subject: Subject of the original email
            bcc_emails: List of BCC email addresses
            
        Returns:
            bool: True if sent successfully
        """
        custom_data = {
            'target_name': target_name,
            'original_subject': original_subject,
            'subtitle': f'Following up with {target_name}'
        }
        
        return self.send_branded_email(
            brand_key=brand_key,
            campaign_type='follow_up',
            to_email=target_email,
            custom_data=custom_data,
            bcc_emails=bcc_emails
        )
    
    def test_all_brands(self, test_email: str = "greg@buildly.io") -> Dict[str, Any]:
        """
        Test email sending for all brands
        
        Args:
            test_email: Email address to send test emails to
            
        Returns:
            dict: Test results for each brand
        """
        results = {}
        
        for brand_key in BRAND_CONFIGS.keys():
            print(f"\n🎨 Testing {brand_key.title()} brand...")
            
            # Test outreach email
            outreach_success = self.send_outreach_email(
                brand_key=brand_key,
                target_name="Test Recipient",
                target_email=test_email,
                target_organization="Test Organization",
                bcc_emails=[test_email]
            )
            
            # Test analytics email (with sample data)
            sample_analytics = {
                'sessions': '1,234',
                'users': '856',
                'pageviews': '2,856',
                'bounce_rate': '45.2%',
                'emails_sent': '25',
                'open_rate': '28.5%',
                'click_rate': '3.2%'
            }
            
            analytics_success = self.send_analytics_email(
                brand_key=brand_key,
                recipient_email=test_email,
                analytics_data=sample_analytics,
                bcc_emails=[test_email]
            )
            
            results[brand_key] = {
                'outreach': outreach_success,
                'analytics': analytics_success,
                'overall': outreach_success and analytics_success
            }
        
        return results
    
    def test_service_routing(self, test_email: str = "greg@buildly.io") -> Dict[str, Any]:
        """Test email service routing for all brands"""
        
        print("🧪 Testing Email Service Routing...")
        results = {}
        
        brands_to_test = ['buildly', 'foundry', 'open_build']
        
        for brand in brands_to_test:
            service_name = self.service_routing.get(brand, 'brevo')
            print(f"\n📧 Testing {brand} → {service_name}")
            
            result = self.send_email(
                brand=brand,
                to_email=test_email,
                subject=f"🧪 Email Service Test - {brand.title()}",
                body=f"""This is a test email for the {brand.title()} brand.

Service: {service_name}
Timestamp: {datetime.now()}
Brand Routing: {brand} → {service_name}

If you receive this email, the {service_name} integration is working correctly!

Best regards,
{brand.title()} Team""",
                bcc_email="greg@buildly.io" if brand == 'buildly' else None
            )
            
            results[brand] = result
            
            if result['success']:
                print(f"✅ {brand} email sent successfully via {result['service']}")
                if 'message_id' in result:
                    print(f"   Message ID: {result['message_id']}")
            else:
                print(f"❌ {brand} email failed: {result.get('error', 'Unknown error')}")
        
        return results

def main():
    """Test the unified email service routing"""
    email_service = UnifiedEmailService()
    
    print("🚀 Testing Email Service Routing (Buildly → MailerSend, Others → Brevo)")
    print("=" * 70)
    
    # Test service routing first
    routing_results = email_service.test_service_routing()
    
    # Print routing summary
    print("\n📊 Routing Test Summary:")
    print("=" * 30)
    
    successful_routes = sum(1 for result in routing_results.values() if result['success'])
    total_routes = len(routing_results)
    
    print(f"✅ Successful: {successful_routes}/{total_routes}")
    print(f"📈 Success Rate: {(successful_routes/total_routes*100):.1f}%")
    
    for brand, result in routing_results.items():
        status = "✅" if result['success'] else "❌"
        service = result.get('service', 'unknown')
        print(f"{status} {brand}: routed to {service}")
        if not result['success']:
            print(f"    Error: {result.get('error', 'Unknown error')}")
    
    if successful_routes == total_routes:
        print("\n🎉 All email routing is working correctly!")
        print("📧 Check your inbox for test emails from each service")
        
        # Instructions for MailerSend setup if needed
        if not email_service.mailersend_config['api_token']:
            print("\n⚠️  MailerSend token not configured!")
            print("📝 To complete setup:")
            print("   1. Go to MailerSend dashboard → API Tokens")
            print("   2. Create new token with 'Email' permission")
            print("   3. Set MAILERSEND_API_TOKEN environment variable")
            print("   4. Or update _load_mailersend_config() in this file")
    else:
        print(f"\n⚠️  Some routes failed. Check configurations:")
        if not email_service.mailersend_config['api_token']:
            print("   • MailerSend: Missing API token")
        if not email_service.brevo_config['user']:
            print("   • Brevo: Missing SMTP credentials")

if __name__ == "__main__":
    main()