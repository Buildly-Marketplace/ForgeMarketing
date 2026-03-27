#!/usr/bin/env python3
"""
Brand-Specific Outreach Campaign Runner
======================================

Executes outreach campaigns for specific brands with proper
rate limiting, personalization, and tracking.

Usage:
    python run_brand_outreach.py --brand foundry --limit 3
    python run_brand_outreach.py --brand buildly --limit 2 --dry-run
"""

import asyncio
import argparse
import logging
import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from automation.multi_brand_outreach import MultiBrandOutreachCampaign, BRAND_DISCOVERY_STRATEGIES

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Email templates per brand
EMAIL_TEMPLATES = {
    'buildly': {
        'subject': 'Partnership Opportunity: Low-Code Automation Platform',
        'template': '''Hello {contact_name},

I hope this message finds you well. I'm reaching out from Buildly, a comprehensive low-code platform that helps organizations accelerate their digital transformation through workflow automation.

{personalization}

Our platform enables businesses to:
• Build custom applications without extensive coding
• Automate complex business processes
• Integrate existing systems seamlessly
• Scale operations efficiently

I'd love to explore how we might collaborate or how Buildly could benefit your organization. Would you be open to a brief conversation?

Best regards,
Team Buildly
https://www.buildly.io

---
If you'd prefer not to receive these messages, please reply with "UNSUBSCRIBE"'''
    },
    'foundry': {
        'subject': 'Connecting with Fellow Entrepreneurs - Foundry Partnership',
        'template': '''Hi {contact_name},

Greetings from First City Foundry! We're a startup incubator dedicated to helping early-stage ventures grow and succeed.

{personalization}

We offer:
• Mentorship from experienced entrepreneurs
• Access to funding networks
• Co-working space and resources
• Community of like-minded founders

I'd love to learn more about your venture and explore potential synergies. Are you available for a quick chat?

Looking forward to connecting,
First City Foundry Team
https://www.firstcityfoundry.com

---
Reply "STOP" to opt out of future messages'''
    },
    'openbuild': {
        'subject': 'Developer Training Partnership - Open Build',
        'template': '''Hello {contact_name},

I'm writing from Open Build, where we provide comprehensive developer training and open-source education programs.

{personalization}

Our programs include:
• Hands-on coding bootcamps
• Open source project collaboration
• Developer community building
• Skills assessment and certification

We're always looking to connect with fellow developers and organizations in the tech education space. Would you be interested in exploring a collaboration?

Best,
Open Build Team
https://open-build.github.io

---
Unsubscribe by replying "REMOVE"'''
    },
    'radical': {
        'subject': 'Innovation in Mental Health Technology',
        'template': '''Dear {contact_name},

I'm reaching out from Radical Therapy, where we're pioneering innovative approaches to mental health and wellness technology.

{personalization}

Our focus areas:
• Digital therapy platforms
• Mental wellness applications
• Healthcare technology innovation
• Accessible mental health solutions

I'd value the opportunity to connect and learn about your work in this important field. Would you be open to a brief conversation?

Warm regards,
Radical Therapy Team
https://radical-therapy.github.io

---
To unsubscribe, please reply "NO THANKS"'''
    },
    'oregonsoftware': {
        'subject': 'Custom Software Development Partnership',
        'template': '''Hi {contact_name},

Hello from Oregon Software! We specialize in custom software development and technology consulting for businesses across the Pacific Northwest and beyond.

{personalization}

Our expertise includes:
• Custom web and mobile applications
• Software architecture consulting
• Digital transformation projects
• Technical strategy and planning

I'd love to learn more about your technology needs and explore how we might work together. Are you available for a brief discussion?

Best regards,
Oregon Software Team
https://oregonsoftware.github.io

---
Reply "UNSUBSCRIBE" to opt out'''
    }
}

class BrandOutreachRunner:
    """Executes outreach campaigns for specific brands"""
    
    def __init__(self, brand: str):
        self.brand = brand
        self.brand_config = BRAND_DISCOVERY_STRATEGIES.get(brand, {})
        self.campaign = MultiBrandOutreachCampaign()
        
        # SMTP configuration (proven Brevo setup)
        self.smtp_config = {
            'smtp_server': 'smtp-relay.brevo.com',
            'smtp_port': 587,
            'username': os.getenv('BREVO_SMTP_USER', ''),
            'password': os.getenv('BREVO_SMTP_PASSWORD', '')
        }
    
    def generate_personalized_message(self, target, template_data):
        """Generate personalized outreach message"""
        
        # Create personalization based on target info
        personalization_parts = []
        
        if target.description:
            personalization_parts.append(f"I came across {target.name} and was impressed by your work in {target.category}.")
        
        if target.focus_areas:
            focus = ', '.join(target.focus_areas[:2])
            personalization_parts.append(f"Your focus on {focus} aligns well with our mission.")
        
        if not personalization_parts:
            personalization_parts.append(f"I discovered {target.name} and believe there could be great synergy between our organizations.")
        
        personalization = ' '.join(personalization_parts)
        
        # Fill template
        contact_name = target.contact_name or "there"
        subject = template_data['subject']
        body = template_data['template'].format(
            contact_name=contact_name,
            personalization=personalization,
            target_name=target.name,
            target_category=target.category
        )
        
        return {
            'subject': subject,
            'body': body,
            'personalization_used': personalization
        }
    
    def send_outreach_email(self, target, message, dry_run=False):
        """Send outreach email to target"""
        
        # Use target email or construct generic one
        to_email = target.email or f"info@{target.website.replace('https://', '').replace('http://', '').split('/')[0]}"
        
        if dry_run:
            logger.info(f"[DRY RUN] Would send to {target.name} ({to_email})")
            logger.info(f"[DRY RUN] Subject: {message['subject']}")
            return True
        
        try:
            # Create SMTP connection
            server = smtplib.SMTP(self.smtp_config['smtp_server'], self.smtp_config['smtp_port'])
            server.starttls()
            server.login(self.smtp_config['username'], self.smtp_config['password'])
            
            # Create message
            msg = MIMEMultipart()
            
            # Get brand-specific from address from database
            brand_data = get_brand_details(self.brand)
            from_email = os.getenv(f'{self.brand.upper()}_FROM_EMAIL', f'team@{self.brand}.io')
            brand_name = brand_data.get('display_name', self.brand.title()) if brand_data else self.brand.title()
            
            msg['From'] = f\"{brand_name} <{from_email}>\"
            msg['To'] = to_email
            msg['Subject'] = message['subject']
            msg['Reply-To'] = from_email
            
            # Add text body
            text_part = MIMEText(message['body'], 'plain')
            msg.attach(text_part)
            
            # Send message
            server.send_message(msg)
            server.quit()
            
            logger.info(f"✅ Outreach sent to {target.name} ({to_email})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to send to {target.name}: {e}")
            return False
    
    def update_target_contact_status(self, target, success):
        """Update target's contact status in database"""
        import sqlite3
        
        conn = sqlite3.connect(self.campaign.db.db_path)
        cursor = conn.cursor()
        
        # Update contact count and last contacted date
        cursor.execute("""
            UPDATE targets 
            SET contact_count = contact_count + 1,
                last_contacted = ?,
                notes = COALESCE(notes, '') || ?
            WHERE name = ? AND website = ?
        """, (
            datetime.now().isoformat(),
            f"\n[{datetime.now().strftime('%Y-%m-%d')}] Outreach sent ({'success' if success else 'failed'})",
            target.name,
            target.website
        ))
        
        conn.commit()
        conn.close()
    
    def log_campaign_activity(self, targets_contacted, successful_sends):
        """Log campaign activity to database"""
        import sqlite3
        
        conn = sqlite3.connect(self.campaign.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO campaigns 
            (brand, campaign_type, sent_date, status)
            VALUES (?, ?, ?, ?)
        """, (
            self.brand,
            'automated_outreach',
            datetime.now().isoformat(),
            f"sent_{successful_sends}_of_{targets_contacted}"
        ))
        
        conn.commit()
        conn.close()
    
    async def run_outreach_campaign(self, limit=5, dry_run=False):
        """Run outreach campaign for the brand"""
        
        brand_name = self.brand_config.get('name', self.brand.title())
        logger.info(f"🚀 Starting {brand_name} outreach campaign (limit: {limit})")
        
        if dry_run:
            logger.info("🧪 DRY RUN MODE - No emails will be sent")
        
        # Get campaign targets
        targets = self.campaign.get_campaign_targets(self.brand, limit=limit)
        
        if not targets:
            logger.warning(f"No targets available for {brand_name} outreach")
            return {'sent': 0, 'failed': 0, 'targets': 0}
        
        # Get email template
        template_data = EMAIL_TEMPLATES.get(self.brand, EMAIL_TEMPLATES['buildly'])
        
        successful_sends = 0
        failed_sends = 0
        
        for target in targets:
            try:
                # Generate personalized message
                message = self.generate_personalized_message(target, template_data)
                
                # Send email
                success = self.send_outreach_email(target, message, dry_run)
                
                if success:
                    successful_sends += 1
                    if not dry_run:
                        self.update_target_contact_status(target, True)
                else:
                    failed_sends += 1
                    if not dry_run:
                        self.update_target_contact_status(target, False)
                
                # Rate limiting - wait between sends
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Error processing target {target.name}: {e}")
                failed_sends += 1
        
        # Log campaign activity
        if not dry_run and (successful_sends > 0 or failed_sends > 0):
            self.log_campaign_activity(len(targets), successful_sends)
        
        # Summary
        logger.info(f"📊 {brand_name} campaign complete:")
        logger.info(f"   ✅ Sent: {successful_sends}")
        logger.info(f"   ❌ Failed: {failed_sends}")
        logger.info(f"   📋 Total targets: {len(targets)}")
        
        return {
            'sent': successful_sends,
            'failed': failed_sends,
            'targets': len(targets)
        }

async def main():
    """Main outreach campaign runner"""
    parser = argparse.ArgumentParser(description='Run brand-specific outreach campaign')
    parser.add_argument('--brand', required=True, choices=list(BRAND_DISCOVERY_STRATEGIES.keys()),
                      help='Brand to run outreach for')
    parser.add_argument('--limit', type=int, default=5, help='Maximum number of contacts to reach out to')
    parser.add_argument('--dry-run', action='store_true', help='Test run without sending emails')
    
    args = parser.parse_args()
    
    # Create and run outreach campaign
    runner = BrandOutreachRunner(args.brand)
    results = await runner.run_outreach_campaign(limit=args.limit, dry_run=args.dry_run)
    
    # Exit with status code based on results
    if results['sent'] > 0:
        exit(0)  # Success
    elif results['targets'] == 0:
        exit(2)  # No targets available
    else:
        exit(1)  # Failures occurred

if __name__ == '__main__':
    asyncio.run(main())