#!/usr/bin/env python3
"""
Unified Email Service
Routes emails to correct service based on brand:
- Buildly → MailerSend API  
- Others → Brevo SMTP
"""

import os
import requests
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
        """Load MailerSend API configuration with improved deliverability settings"""
        return {
            'api_token': os.getenv('MAILERSEND_API_TOKEN', 'mlsn.<your-mailersend-api-token>'),
            'api_url': 'https://api.mailersend.com/v1/email',
            'from_email': 'hello@buildly.io',  # Changed from team@ for better deliverability
            'from_name': 'Buildly',  # Shorter, more personal name
            'fallback_to_brevo': True  # Enable Brevo fallback for same-domain issues
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
        """Send email using correct service based on brand routing with intelligent fallback"""
        
        service_name = self.service_routing.get(brand.lower(), 'brevo')
        
        # Smart routing: For Buildly emails to same domain, consider Brevo fallback
        if (brand.lower() == 'buildly' and service_name == 'mailersend' and 
            to_email.endswith('@buildly.io') and self.mailersend_config.get('fallback_to_brevo')):
            
            print(f"📧 Smart routing: Buildly email to same domain, trying MailerSend first with Brevo fallback")
            
            # Try MailerSend first
            try:
                result = self._send_via_mailersend(to_email, subject, body, is_html, bcc_email)
                if result['success']:
                    result['routing_note'] = 'MailerSend primary succeeded'
                    return result
            except Exception as e:
                print(f"⚠️ MailerSend failed, falling back to Brevo: {e}")
            
            # Fallback to Brevo for better deliverability to same domain
            try:
                result = self._send_via_brevo(to_email, subject, body, is_html, bcc_email)
                if result['success']:
                    result['routing_note'] = 'Brevo fallback used for same-domain delivery'
                    result['service'] = 'brevo_fallback'
                return result
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Both MailerSend and Brevo fallback failed: {e}',
                    'service': 'both_failed'
                }
        
        # Standard routing
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