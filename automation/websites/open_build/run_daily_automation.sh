#!/bin/bash

# Open Build Daily Outreach Automation
# Executed by cron daily at 9:00 AM

# Set environment variables
export PATH="/usr/local/bin:/usr/bin:/bin"
export HOME="/Users/greglind"

# Change to project directory
cd "/Users/greglind/Projects/open-build/open-build-new-website"

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Log start time
echo "$(date): Starting Open Build daily outreach automation..." >> "/Users/greglind/Projects/open-build/open-build-new-website/logs/cron.log"

# Run the automation with proper error handling
"/Users/greglind/Projects/open-build/open-build-new-website/.venv/bin/python" "/Users/greglind/Projects/open-build/open-build-new-website/scripts/outreach_automation.py" --run >> "/Users/greglind/Projects/open-build/open-build-new-website/logs/daily_automation.log" 2>> "/Users/greglind/Projects/open-build/open-build-new-website/logs/daily_automation_errors.log"

# Check exit status
if [ $? -eq 0 ]; then
    echo "$(date): Daily automation completed successfully" >> "/Users/greglind/Projects/open-build/open-build-new-website/logs/cron.log"
else
    echo "$(date): Daily automation failed with exit code $?" >> "/Users/greglind/Projects/open-build/open-build-new-website/logs/cron.log"
    
    # Send error notification email
    "/Users/greglind/Projects/open-build/open-build-new-website/.venv/bin/python" -c "
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

try:
    msg = MIMEMultipart()
    msg['From'] = f\"{os.getenv('FROM_NAME', 'Open Build System')} <{os.getenv('FROM_EMAIL', 'team@open.build')}>\"
    msg['To'] = os.getenv('TEAM_EMAIL', 'team@open.build')
    msg['Bcc'] = os.getenv('BCC_EMAILS', 'greg@open.build,greg@buildly.io')
    msg['Subject'] = '❌ Open Build Outreach Automation - Cron Job Failed'
    
    message = f'''❌ Open Build Outreach Automation - Cron Job Failure

The daily automation cron job failed to complete successfully.

Failure Details:
• Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
• Location: {os.getcwd()}
• Exit Code: Non-zero

Please check the logs for more details:
• Main Log: {os.getcwd()}/logs/daily_automation.log
• Error Log: {os.getcwd()}/logs/daily_automation_errors.log
• Cron Log: {os.getcwd()}/logs/cron.log

You can also run manually to troubleshoot:
{os.getcwd()}/.venv/bin/python {os.getcwd()}/outreach_automation.py --run

Next scheduled run: Tomorrow 9:00 AM

---
Open Build Outreach Automation System
'''
    
    msg.attach(MIMEText(message, 'plain'))
    
    server = smtplib.SMTP(os.getenv('BREVO_SMTP_HOST'), int(os.getenv('BREVO_SMTP_PORT', '587')))
    server.starttls()
    server.login(os.getenv('BREVO_SMTP_USER'), os.getenv('BREVO_SMTP_PASSWORD'))
    
    recipients = [os.getenv('TEAM_EMAIL', 'team@open.build')] + os.getenv('BCC_EMAILS', 'greg@open.build,greg@buildly.io').split(',')
    text = msg.as_string()
    server.sendmail(os.getenv('FROM_EMAIL'), recipients, text)
    server.quit()
    
    print('Error notification sent successfully')
except Exception as e:
    print(f'Failed to send error notification: {e}')
" >> "/Users/greglind/Projects/open-build/open-build-new-website/logs/cron.log" 2>&1
fi

# Log completion
echo "$(date): Cron job execution completed" >> "/Users/greglind/Projects/open-build/open-build-new-website/logs/cron.log"
