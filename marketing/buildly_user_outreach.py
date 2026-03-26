#!/usr/bin/env python3
"""
Buildly User Outreach System
===========================

Custom email outreach system for Buildly users based on CSV data.
Adapted from the existing Foundry outreach system to handle:
- CSV user data processing
- Personalized Buildly account update emails
- Rate limiting and tracking
- Template-based messaging with user-specific data

Usage:
    python buildly_user_outreach.py --csv users.csv --template account_update --preview
    python buildly_user_outreach.py --csv users.csv --template account_update --send
    python buildly_user_outreach.py --csv users.csv --template feature_announcement --send
"""

import json
import csv
import time
import random
import logging
import argparse
import os
import sys
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Set, Optional
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
import yagmail
import yaml

@dataclass
class BuildlyUser:
    """Data class for Buildly user information"""
    email: str
    name: str = ""
    company: str = ""
    account_type: str = ""
    last_login: str = ""
    signup_date: str = ""
    features_used: str = ""
    subscription_status: str = ""
    usage_level: str = ""
    custom_field_1: str = ""
    custom_field_2: str = ""

class BuildlyUserOutreach:
    """Main outreach system for Buildly users"""
    
    def __init__(self, brand_name: str = None):
        # Set up directories
        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / "buildly_outreach_data"
        self.data_dir.mkdir(exist_ok=True)
        
        # Data files
        self.outreach_log_file = self.data_dir / "outreach_log.json"
        self.opt_outs_file = self.data_dir / "opt_outs.json"
        self.analytics_file = self.data_dir / "analytics.json"
        
        # Load existing data
        self.outreach_log = self.load_outreach_log()
        self.opt_outs = self.load_opt_outs()
        
        # Store brand name for configuration lookup
        self.brand_name = brand_name
        
        # Email configuration - Use unified email service (routes Buildly → MailerSend)
        self.from_email = os.getenv('BUILDLY_FROM_EMAIL', 'team@buildly.io')
        self.bcc_email = None  # Will be set from brand config if available
        
        # Rate limiting
        self.rate_limit_delay = (5, 15)  # 5-15 seconds between emails
        self.daily_limit = int(os.getenv('BUILDLY_DAILY_EMAIL_LIMIT', '100'))
        
        # Setup logging
        self.setup_logging()
        
        # Import and initialize unified email service (after logging setup)
        try:
            # Add the project root to path for imports
            project_root = os.getenv('PROJECT_ROOT', str(Path(__file__).parent.parent))
            if project_root not in sys.path:
                sys.path.insert(0, project_root)
            from unified_email_service import UnifiedEmailService
            self.email_service = UnifiedEmailService()
            self.logger.info("✅ Unified email service initialized (Buildly → MailerSend routing)")
        except ImportError as e:
            self.logger.error(f"❌ Failed to import unified email service: {e}")
            # Fallback to direct SMTP (not recommended for Buildly)
            self.email_service = None
            self.smtp_server = os.getenv('BREVO_SMTP_HOST', 'smtp-relay.brevo.com')
            self.smtp_port = int(os.getenv('BREVO_SMTP_PORT', '587'))
            self.smtp_user = os.getenv('BREVO_SMTP_USER', '<your-brevo-smtp-user>')
            self.smtp_password = os.getenv('BREVO_SMTP_PASSWORD', 'F9BCg30JqkyZmVWw')
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = self.data_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"outreach_{datetime.now().strftime('%Y%m%d')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Load brand configuration if brand_name is provided
        if self.brand_name:
            self.load_brand_config()

    def load_brand_config(self):
        """Load brand-specific configuration from YAML file"""
        try:
            config_file = self.base_dir.parent / 'config' / 'outreach_config.yaml'
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = yaml.safe_load(f)
                
                if self.brand_name in config.get('brands', {}):
                    brand_config = config['brands'][self.brand_name]
                    self.from_email = brand_config.get('from_email', self.from_email)
                    self.bcc_email = brand_config.get('bcc_email')
                    self.logger.info(f"Loaded config for brand '{self.brand_name}' - BCC: {self.bcc_email}")
                else:
                    self.logger.warning(f"Brand '{self.brand_name}' not found in configuration")
            else:
                self.logger.warning("Brand configuration file not found")
        except Exception as e:
            self.logger.error(f"Failed to load brand configuration: {e}")

    def load_outreach_log(self) -> List[Dict]:
        """Load outreach log from file"""
        if self.outreach_log_file.exists():
            with open(self.outreach_log_file, 'r') as f:
                return json.load(f)
        return []

    def save_outreach_log(self):
        """Save outreach log to file"""
        with open(self.outreach_log_file, 'w') as f:
            json.dump(self.outreach_log, f, indent=2)

    def load_opt_outs(self) -> Set[str]:
        """Load opt-out list from file"""
        if self.opt_outs_file.exists():
            with open(self.opt_outs_file, 'r') as f:
                return set(json.load(f))
        return set()

    def save_opt_outs(self):
        """Save opt-out list to file"""
        with open(self.opt_outs_file, 'w') as f:
            json.dump(list(self.opt_outs), f, indent=2)

    def load_users_from_csv(self, csv_file: str) -> List[BuildlyUser]:
        """Load user data from CSV file"""
        users = []
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Map CSV columns to BuildlyUser fields - updated for conversion targets format
                user = BuildlyUser(
                    email=row.get('Email', row.get('email', '')).strip(),
                    name=row.get('Full Name', row.get('name', row.get('full_name', ''))).strip(),
                    company=row.get('Organization', row.get('company', row.get('organization', ''))).strip(),
                    account_type=row.get('Current Status', row.get('account_type', row.get('plan', ''))).strip(),
                    last_login=row.get('last_login', row.get('last_active', 'N/A')).strip(),
                    signup_date=row.get('Customer Since', row.get('signup_date', row.get('created_at', ''))).strip(),
                    features_used=row.get('features_used', row.get('modules', 'Platform Usage')).strip(),
                    subscription_status=row.get('Current Status', row.get('subscription_status', row.get('status', ''))).strip(),
                    usage_level=row.get('Priority', row.get('usage_level', row.get('tier', ''))).strip(),
                    custom_field_1=row.get('Notes', row.get('custom_field_1', row.get('notes', ''))).strip(),
                    custom_field_2=row.get('Action Required', row.get('custom_field_2', row.get('tags', ''))).strip(),
                )
                
                if user.email:  # Only add users with valid email
                    users.append(user)
                    
        self.logger.info(f"Loaded {len(users)} users from CSV file")
        return users

    def get_email_templates(self) -> Dict[str, str]:
        """Get available email templates for Buildly users"""
        return {
            'account_update': '''Subject: Important updates to your Buildly account

Hi {{ user.name or "there" }},

We hope you've been making great progress with Buildly! We wanted to reach out with some important updates about your account and new features that can help streamline your development process.

{% if user.company %}
We see you're working with {{ user.company }}, and we believe these updates will be particularly valuable for your team's workflow.
{% endif %}

**What's New:**
• Enhanced API management tools for faster development
• Improved team collaboration features
• New integrations with popular development tools
• Advanced analytics and reporting capabilities

{% if user.last_login %}
Since your last login{% if user.last_login != "Never" %} on {{ user.last_login }}{% endif %}, we've rolled out several improvements based on user feedback.
{% endif %}

**Action Required:**
Please log into your Buildly account to:
1. Review your current subscription status
2. Explore the new features available to you
3. Update your account preferences if needed

Login to your account: https://app.buildly.io/login

If you have any questions or need assistance, our team is here to help. Simply reply to this email or contact us at support@buildly.io.

Best regards,
The Buildly Team

---
You're receiving this email because you have an active Buildly account. If you no longer wish to receive these updates, you can unsubscribe here: {{ opt_out_link }}''',

            'feature_announcement': '''Subject: New Buildly features to accelerate your development

Hello {{ user.name or "Developer" }},

Great news! We've just released several powerful new features in Buildly that we think you'll love.

{% if user.features_used %}
Based on your usage of {{ user.features_used }}, these new additions should integrate seamlessly with your current workflow.
{% endif %}

**🚀 What's New:**
• **Smart Code Generation**: AI-powered code suggestions based on your project patterns
• **Advanced Deployment Pipeline**: One-click deployments with automated testing
• **Team Collaboration Hub**: Real-time collaboration tools for distributed teams
• **Enhanced Security Suite**: Advanced security scanning and compliance tools

{% if user.account_type %}
As a {{ user.account_type }} user, you have access to{% if user.account_type.lower() in ['premium', 'enterprise'] %} all these features plus exclusive advanced capabilities{% else %} these features with some usage limits - consider upgrading for full access{% endif %}.
{% endif %}

**Get Started:**
1. Log into your Buildly dashboard: https://app.buildly.io
2. Check out the "What's New" section
3. Try the new features with your current projects

We'd love to hear your feedback on these new capabilities. Let us know what you think!

Best,
The Buildly Product Team

---
Don't want these updates? Unsubscribe here: {{ opt_out_link }}''',

            'reengagement': '''Subject: We miss you at Buildly - Special offer inside

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>We miss you at Buildly</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background-color: #f8f9fa; }
        .container { max-width: 600px; margin: 0 auto; background-color: #ffffff; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center; }
        .header h1 { color: #ffffff; margin: 0; font-size: 28px; font-weight: 300; }
        .content { padding: 40px 30px; }
        .greeting { font-size: 18px; color: #2c3e50; margin-bottom: 20px; }
        .highlight-box { background-color: #f8f9fa; border-left: 4px solid #667eea; padding: 20px; margin: 25px 0; }
        .offer-box { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 8px; margin: 25px 0; text-align: center; }
        .cta-button { display: inline-block; background-color: #28a745; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; margin: 20px 0; }
        .footer { background-color: #2c3e50; color: #ecf0f1; padding: 30px; text-align: center; font-size: 14px; }
        ul { padding-left: 0; list-style: none; }
        ul li { padding: 8px 0; }
        ul li:before { content: "✓ "; color: #28a745; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Buildly</h1>
        </div>
        
        <div class="content">
            <div class="greeting">
                Hi {{ user.name or "there" }},
            </div>
            
            <p>We noticed you haven't been active in your Buildly account recently{% if user.last_login and user.last_login != "Never" %} (last login: {{ user.last_login }}){% endif %}, and we wanted to check in.</p>
            
            {% if user.company %}
            <p>We know <strong>{{ user.company }}</strong> has important projects to build, and we want to make sure Buildly is providing the value you need.</p>
            {% endif %}
            
            <div class="highlight-box">
                <h3>🎯 What you might have missed:</h3>
                <ul>
                    <li>Major platform improvements and bug fixes</li>
                    <li>New integrations with popular development tools</li>
                    <li>Enhanced documentation and tutorials</li>
                    <li>Expanded template library for faster project setup</li>
                </ul>
            </div>
            
            <div class="offer-box">
                <h3>🎁 Special Re-engagement Offer</h3>
                <p>To welcome you back, we're extending a special offer:</p>
                <ul style="text-align: left; display: inline-block;">
                    <li>30 Day Free Trial Extension!</li>
                    <li>One-on-one setup session with our team</li>
                </ul>
                
                <a href="https://app.buildly.io/login" class="cta-button">🚀 Login to Buildly</a><br/>
                <p>Then go to your profile > Subscriptions and use The Foundry Free 30 Day Trial.</p>
                
                <p>IF you need more help, then you can use our helpful Buildly chatbot for process or tool specific questions, or if you are having technical isses submit them vie the Chatbot issues tab.</p>
                <p>Finally feel to reach out via the <b>Request Help</b> in the Insights report section and we can schedule a call to help you find a technical co-founder or team to build your app or tool.</p>
            </div>
            
            <p>If there's anything specific that prevented you from continuing with Buildly, we'd love to hear about it. Your feedback helps us improve the platform for everyone.</p>
            
            <p>Looking forward to seeing you back,<br>
            <strong>The Buildly Team</strong></p>
            
            <p><em>P.S. This offer expires in 7 days, so don't wait too long!</em></p>
        </div>
        
        <div class="footer">
            <p>© 2025 Buildly. All rights reserved.</p>
            <p><a href="{{ opt_out_link }}" style="color: #ecf0f1;">Unsubscribe from these emails</a></p>
        </div>
    </div>
</body>
</html>''',

            'custom': '''Subject: {{ custom_subject }}

Hi {{ user.name or "there" }},

{{ custom_message }}

Best regards,
The Buildly Team

---
Unsubscribe: {{ opt_out_link }}'''
        }

    def generate_outreach_message(self, user: BuildlyUser, template_name: str, custom_subject: str = "", custom_message: str = "") -> Dict[str, str]:
        """Generate personalized outreach message for a user"""
        templates = self.get_email_templates()
        
        if template_name not in templates:
            raise ValueError(f"Template '{template_name}' not found. Available templates: {list(templates.keys())}")
        
        template_text = templates[template_name]
        template = Template(template_text.strip())
        
        # Generate opt-out link
        opt_out_link = f"https://app.buildly.io/unsubscribe?email={user.email}"
        
        message = template.render(
            user=user,
            opt_out_link=opt_out_link,
            custom_subject=custom_subject,
            custom_message=custom_message
        )
        
        # Extract subject and body
        lines = message.split('\n')
        subject = lines[0].replace('Subject: ', '') if lines[0].startswith('Subject: ') else "Update from Buildly"
        body = '\n'.join(lines[2:])  # Skip subject and empty line
        
        return {
            'subject': subject,
            'body': body,
            'template_used': template_name
        }

    def is_opted_out(self, email: str) -> bool:
        """Check if user has opted out"""
        return email.lower() in self.opt_outs

    def has_been_contacted_recently(self, email: str, days: int = 2) -> bool:
        """Check if user has been contacted recently - reduced to 2 days for re-engagement campaigns"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for log_entry in self.outreach_log:
            if (log_entry['email'] == email and 
                datetime.fromisoformat(log_entry['timestamp']) > cutoff_date):
                return True
        return False

    def check_daily_limit(self) -> bool:
        """Check if daily email limit has been reached"""
        today = datetime.now().date()
        today_count = sum(1 for log_entry in self.outreach_log 
                         if datetime.fromisoformat(log_entry['timestamp']).date() == today)
        return today_count < self.daily_limit
    
    def _archive_email(self, user: BuildlyUser, message: Dict[str, str], preview_only: bool, bcc_email: str = None) -> str:
        """Create local archive of email for verification purposes"""
        try:
            # Create archive directory
            archive_dir = "sent_emails_archive"
            if not os.path.exists(archive_dir):
                os.makedirs(archive_dir)
            
            # Generate archive filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            safe_email = user.email.replace("@", "_at_").replace(".", "_").replace("/", "_")
            archive_file = f"{archive_dir}/email_{timestamp}_{safe_email}.txt"
            
            # Create archive content
            archive_content = f"""EMAIL ARCHIVE - {datetime.now().isoformat()}
{'='*70}
CAMPAIGN DETAILS:
Brand: {getattr(self, 'brand_name', 'buildly')}
Template: {message.get('template_used', 'custom')}
Status: {'PREVIEW ONLY' if preview_only else 'SENT TO SMTP'}

RECIPIENT DETAILS:
TO: {user.email}
NAME: {getattr(user, 'name', 'Unknown')}
COMPANY: {getattr(user, 'company', 'Unknown')}
BCC: {bcc_email or 'None'}

EMAIL CONTENT:
{'='*70}
SUBJECT: {message.get('subject', 'No Subject')}

BODY:
{'-'*70}
{message.get('body', 'No Body')}
{'-'*70}

SMTP DETAILS:
Server: {self.smtp_server}:{self.smtp_port}
From: {self.from_email}
Authentication: {'Configured' if self.smtp_password else 'Not Configured'}

DELIVERY STATUS:
Queue Status: {'Would Queue' if preview_only else 'Queued to Brevo SMTP'}
Expected Delivery: {'N/A (Preview)' if preview_only else '1-5 minutes'}
Archive Created: {datetime.now().isoformat()}

{'='*70}
"""
            
            # Save archive
            with open(archive_file, 'w', encoding='utf-8') as f:
                f.write(archive_content)
            
            # Log archive creation
            self.logger.info(f"Email archived: {archive_file}")
            return archive_file
            
        except Exception as e:
            self.logger.warning(f"Failed to archive email: {str(e)}")
            return None

    def send_email(self, user: BuildlyUser, message: Dict[str, str], preview_only: bool = False, bcc_email: str = None) -> bool:
        """Send email to user with optional BCC"""
        # Use provided BCC or fall back to instance BCC
        actual_bcc = bcc_email or self.bcc_email
        
        # Create email archive for verification
        self._archive_email(user, message, preview_only, actual_bcc)
        
        if preview_only:
            print(f"\n{'='*60}")
            print(f"PREVIEW - Email to {user.email}")
            print(f"{'='*60}")
            print(f"To: {user.email}")
            print(f"From: {self.from_email}")
            if actual_bcc:
                print(f"BCC: {actual_bcc}")
            print(f"Subject: {message['subject']}")
            print("-" * 60)
            print(message['body'])
            print(f"{'='*60}\n")
            return True

        try:
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = user.email
            msg['Subject'] = message['subject']
            
            # Add BCC if specified
            if actual_bcc:
                msg['Bcc'] = actual_bcc
            
            # Add body - detect HTML content
            if '<html>' in message['body'] or '<!DOCTYPE html>' in message['body']:
                msg.attach(MIMEText(message['body'], 'html'))
            else:
                msg.attach(MIMEText(message['body'], 'plain'))
            
            # Prepare recipient list (includes BCC for actual sending)
            recipients = [user.email]
            if actual_bcc:
                recipients.append(actual_bcc)
            
            # Send email using unified service (routes Buildly → MailerSend)
            if self.email_service:
                # Detect if the message body contains HTML
                is_html_content = '<html>' in message['body'] or '<!DOCTYPE html>' in message['body']
                
                result = self.email_service.send_email(
                    brand='buildly',
                    to_email=user.email,
                    subject=message['subject'],
                    body=message['body'],
                    is_html=is_html_content,
                    bcc_email=actual_bcc
                )
                
                if result['success']:
                    service_used = result.get('service', 'unknown')
                    message_id = result.get('message_id', 'N/A')
                    self.logger.info(f"Email sent via {service_used} to {user.email} (BCC: {actual_bcc}) - ID: {message_id}")
                    
                    # Store service details for logging
                    email_service_info = {
                        'service_used': service_used,
                        'message_id': message_id,
                        'api_response': result.get('raw_response', {})
                    }
                else:
                    raise Exception(f"Unified email service failed: {result.get('error', 'Unknown error')}")
            else:
                # Fallback to direct SMTP (not recommended for Buildly)
                self.logger.warning("⚠️ Using fallback SMTP - should use unified service for proper Buildly routing")
                if self.smtp_password and self.smtp_user:
                    server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                    server.starttls()
                    server.login(self.smtp_user, self.smtp_password)
                    text = msg.as_string()
                    server.sendmail(self.from_email, recipients, text)
                    server.quit()
                    self.logger.info(f"Email sent via Brevo SMTP fallback to {user.email} (BCC: {actual_bcc})")
                    
                    # Store service details for logging
                    email_service_info = {
                        'service_used': 'brevo_smtp',
                        'message_id': 'smtp_no_id',
                        'api_response': {}
                    }
                else:
                    # Last resort fallback
                    self.logger.warning("No email service available, using yagmail fallback")
                    yag = yagmail.SMTP(self.from_email)
                    yag.send(to=user.email, bcc=actual_bcc, subject=message['subject'], contents=message['body'])
                    
                    # Store service details for logging
                    email_service_info = {
                        'service_used': 'yagmail_fallback',
                        'message_id': 'yagmail_no_id',
                        'api_response': {}
                    }
            
            # Log successful send with enhanced information
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'email': user.email,
                'name': user.name,
                'company': user.company,
                'template_used': message['template_used'],
                'subject': message['subject'],
                'bcc_email': actual_bcc,
                'status': 'sent',
                'service_used': email_service_info.get('service_used', 'unknown'),
                'message_id': email_service_info.get('message_id', 'N/A'),
                'delivery_details': {
                    'sent_at': datetime.now().isoformat(),
                    'email_length': len(message['body']),
                    'is_html': message.get('is_html', False),
                    'has_bcc': actual_bcc is not None
                }
            }
            
            self.outreach_log.append(log_entry)
            self.save_outreach_log()
            
            self.logger.info(f"Email sent successfully to {user.email}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email to {user.email}: {str(e)}")
            
            # Log failed send with enhanced information
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'email': user.email,
                'name': user.name,
                'company': user.company,
                'template_used': message['template_used'],
                'subject': message['subject'],
                'status': 'failed',
                'error': str(e),
                'error_type': type(e).__name__,
                'service_attempted': getattr(self, 'email_service', {}).get('name', 'unified_service') if hasattr(self, 'email_service') else 'unified_service',
                'retry_count': 0,
                'failure_details': {
                    'failed_at': datetime.now().isoformat(),
                    'email_length': len(message['body']) if message.get('body') else 0,
                    'is_html': message.get('is_html', False),
                    'has_bcc': bcc_email is not None
                }
            }
            
            self.outreach_log.append(log_entry)
            self.save_outreach_log()
            
            return False

    def run_outreach_campaign(self, csv_file: str, template_name: str, preview_only: bool = False, 
                            custom_subject: str = "", custom_message: str = "", 
                            skip_recent: bool = True, max_emails: int = None, bcc_email: str = None,
                            progress_callback: callable = None) -> Dict[str, int]:
        """Run outreach campaign for users in CSV file"""
        
        # Load users
        users = self.load_users_from_csv(csv_file)
        
        stats = {
            'total_users': len(users),
            'emails_sent': 0,
            'emails_failed': 0,
            'skipped_opted_out': 0,
            'skipped_recent': 0,
            'skipped_daily_limit': 0
        }
        
        self.logger.info(f"Starting outreach campaign with {len(users)} users")
        self.logger.info(f"Template: {template_name}, Preview only: {preview_only}")
        
        for i, user in enumerate(users):
            # Call progress callback if provided
            if progress_callback:
                try:
                    progress_callback(i, len(users), user.email, 'processing')
                except Exception as e:
                    self.logger.warning(f"Progress callback error: {e}")
            
            # Check daily limit
            if not preview_only and not self.check_daily_limit():
                self.logger.warning("Daily email limit reached")
                stats['skipped_daily_limit'] = len(users) - i
                break

            # Check max emails limit
            if max_emails and stats['emails_sent'] >= max_emails:
                self.logger.info(f"Reached max emails limit ({max_emails})")
                break

            # Check opt-out status
            if self.is_opted_out(user.email):
                self.logger.info(f"Skipping {user.email} - opted out")
                stats['skipped_opted_out'] += 1
                if progress_callback:
                    try:
                        progress_callback(i, len(users), user.email, 'skipped_opted_out')
                    except Exception as e:
                        self.logger.warning(f"Progress callback error: {e}")
                continue
            
            # Check recent contact (if skip_recent is True)
            if skip_recent and self.has_been_contacted_recently(user.email):
                self.logger.info(f"Skipping {user.email} - contacted recently")
                stats['skipped_recent'] += 1
                if progress_callback:
                    try:
                        progress_callback(i, len(users), user.email, 'skipped_recent')
                    except Exception as e:
                        self.logger.warning(f"Progress callback error: {e}")
                continue
            
            try:
                # Generate message
                message = self.generate_outreach_message(
                    user, template_name, custom_subject, custom_message
                )
                
                # Send email
                if self.send_email(user, message, preview_only, bcc_email):
                    stats['emails_sent'] += 1
                    if progress_callback:
                        try:
                            progress_callback(i, len(users), user.email, 'sent')
                        except Exception as e:
                            self.logger.warning(f"Progress callback error: {e}")
                else:
                    stats['emails_failed'] += 1
                    if progress_callback:
                        try:
                            progress_callback(i, len(users), user.email, 'failed')
                        except Exception as e:
                            self.logger.warning(f"Progress callback error: {e}")
                
                # Rate limiting (only for real sends)
                if not preview_only and i < len(users) - 1:
                    delay = random.uniform(*self.rate_limit_delay)
                    time.sleep(delay)
                    
            except Exception as e:
                self.logger.error(f"Error processing user {user.email}: {str(e)}")
                stats['emails_failed'] += 1
        
        # Print summary
        print(f"\n{'='*60}")
        print("CAMPAIGN SUMMARY")
        print(f"{'='*60}")
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        print(f"{'='*60}\n")
        
        return stats

def main():
    parser = argparse.ArgumentParser(description='Buildly User Outreach System')
    parser.add_argument('--csv', required=True, help='CSV file with user data')
    parser.add_argument('--template', required=True, 
                       choices=['account_update', 'feature_announcement', 'reengagement', 'custom'],
                       help='Email template to use')
    parser.add_argument('--preview', action='store_true', help='Preview emails without sending')
    parser.add_argument('--send', action='store_true', help='Actually send emails')
    parser.add_argument('--custom-subject', help='Custom subject for custom template')
    parser.add_argument('--custom-message', help='Custom message for custom template')
    parser.add_argument('--max-emails', type=int, help='Maximum number of emails to send')
    parser.add_argument('--include-recent', action='store_true', 
                       help='Include users contacted recently (default: skip)')
    
    args = parser.parse_args()
    
    if not args.preview and not args.send:
        print("Error: Must specify either --preview or --send")
        return
    
    if args.template == 'custom' and (not args.custom_subject or not args.custom_message):
        print("Error: Custom template requires --custom-subject and --custom-message")
        return
    
    # Initialize outreach system
    outreach = BuildlyUserOutreach()
    
    # Run campaign
    stats = outreach.run_outreach_campaign(
        csv_file=args.csv,
        template_name=args.template,
        preview_only=args.preview,
        custom_subject=args.custom_subject or "",
        custom_message=args.custom_message or "",
        skip_recent=not args.include_recent,
        max_emails=args.max_emails
    )

if __name__ == "__main__":
    main()