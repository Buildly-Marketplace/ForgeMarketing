#!/bin/bash

# Open Build Outreach Automation - Cron Setup Script
# This script sets up automated daily execution of the outreach system

echo "🚀 Setting up Open Build Outreach Automation Cron Jobs"
echo "=" * 60

# Get the current directory (parent of scripts folder)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="$SCRIPT_DIR/scripts"
PYTHON_PATH="$SCRIPT_DIR/.venv/bin/python"
AUTOMATION_SCRIPT="$SCRIPTS_DIR/outreach_automation.py"
LOG_DIR="$SCRIPT_DIR/logs"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

echo "📁 Project Directory: $SCRIPT_DIR"
echo "🐍 Python Path: $PYTHON_PATH"
echo "📊 Automation Script: $AUTOMATION_SCRIPT"
echo "📝 Log Directory: $LOG_DIR"
echo ""

# Verify files exist
if [ ! -f "$PYTHON_PATH" ]; then
    echo "❌ Python virtual environment not found at $PYTHON_PATH"
    echo "Please run setup_outreach.sh first to create the virtual environment"
    exit 1
fi

if [ ! -f "$AUTOMATION_SCRIPT" ]; then
    echo "❌ Automation script not found at $AUTOMATION_SCRIPT"
    exit 1
fi

# Create the cron script that will be executed
CRON_SCRIPT="$SCRIPTS_DIR/run_daily_automation.sh"

echo "📝 Creating daily automation script..."

cat > "$CRON_SCRIPT" << EOF
#!/bin/bash

# Open Build Daily Outreach Automation
# Executed by cron daily at 9:00 AM

# Set environment variables
export PATH="/usr/local/bin:/usr/bin:/bin"
export HOME="$HOME"

# Change to project directory
cd "$SCRIPT_DIR"

# Load environment variables
if [ -f .env ]; then
    export \$(cat .env | grep -v '^#' | xargs)
fi

# Log start time
echo "\$(date): Starting Open Build daily outreach automation..." >> "$LOG_DIR/cron.log"

# Run the automation with proper error handling
"$PYTHON_PATH" "$AUTOMATION_SCRIPT" --run >> "$LOG_DIR/daily_automation.log" 2>> "$LOG_DIR/daily_automation_errors.log"

# Check exit status
if [ \$? -eq 0 ]; then
    echo "\$(date): Daily automation completed successfully" >> "$LOG_DIR/cron.log"
else
    echo "\$(date): Daily automation failed with exit code \$?" >> "$LOG_DIR/cron.log"
    
    # Send error notification email
    "$PYTHON_PATH" -c "
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
" >> "$LOG_DIR/cron.log" 2>&1
fi

# Log completion
echo "\$(date): Cron job execution completed" >> "$LOG_DIR/cron.log"
EOF

# Make the script executable
chmod +x "$CRON_SCRIPT"

echo "✅ Created daily automation script: $CRON_SCRIPT"
echo ""

# Create weekly analytics report script
WEEKLY_SCRIPT="$SCRIPT_DIR/run_weekly_analytics.sh"

echo "📝 Creating weekly analytics script..."

cat > "$WEEKLY_SCRIPT" << EOF
#!/bin/bash

# Open Build Weekly Analytics Report
# Executed by cron weekly on Sundays at 8:00 AM

# Set environment variables
export PATH="/usr/local/bin:/usr/bin:/bin"
export HOME="$HOME"

# Change to project directory
cd "$SCRIPT_DIR"

# Load environment variables
if [ -f .env ]; then
    export \$(cat .env | grep -v '^#' | xargs)
fi

# Log start time
echo "\$(date): Starting Open Build weekly analytics report..." >> "$LOG_DIR/cron.log"

# Generate weekly report
"$PYTHON_PATH" "$AUTOMATION_SCRIPT" --report >> "$LOG_DIR/weekly_analytics.log" 2>> "$LOG_DIR/weekly_analytics_errors.log"

# Send comprehensive weekly analytics email
"$PYTHON_PATH" -c "
import sys
sys.path.append('$SCRIPT_DIR')
from outreach_automation import OutreachAutomation
import asyncio
from datetime import datetime, timedelta

async def send_weekly_report():
    automation = OutreachAutomation()
    
    # Collect comprehensive analytics
    website_analytics = await automation.analytics_manager.collect_website_analytics()
    youtube_analytics = await automation.analytics_manager.collect_youtube_analytics()
    social_analytics = await automation.analytics_manager.collect_social_media_analytics()
    
    # Get weekly data
    responses = automation.response_tracker.get_recent_responses(days=7)
    sources = automation.source_tracker.get_recent_sources(days=7)
    
    # Generate weekly report
    report = automation.generate_report()
    
    subject = f'📈 Open Build Weekly Analytics Report - {datetime.now().strftime(\"%Y-%m-%d\")}'
    
    message = f'''📈 Open Build Weekly Analytics & Performance Report
{'=' * 60}
Week Ending: {datetime.now().strftime('%Y-%m-%d')}

{report}

📊 WEEKLY ANALYTICS SUMMARY
---------------------------
🌐 Website Performance (7 days):
   • Total visitors: {website_analytics.get('visitors', 'N/A')}
   • Total page views: {website_analytics.get('page_views', 'N/A')}
   • Bounce rate: {website_analytics.get('bounce_rate', 'N/A')}%

📺 YouTube Performance:
   • Total views: {youtube_analytics.get('total_views', 'N/A'):,}
   • Subscribers: {youtube_analytics.get('subscribers', 'N/A'):,}
   • Videos published: {youtube_analytics.get('total_videos', 'N/A')}

📨 WEEKLY RESPONSE SUMMARY
--------------------------
• Total responses: {len(responses)}
• Positive responses: {len([r for r in responses if r['sentiment'] == 'positive'])}
• Response rate: {(len(responses) / max(1, len(responses))) * 100:.1f}%

🔍 SOURCE DISCOVERY (7 DAYS)
----------------------------
• New sources found: {len(sources)}
• Total potential targets: {sum(s.get('targets_found', 0) for s in sources)}

📈 GROWTH METRICS
-----------------
• GitHub stars: {social_analytics.get('github_stars', 'N/A')}
• GitHub forks: {social_analytics.get('github_forks', 'N/A')}

🎯 WEEK AHEAD PLANNING
----------------------
• Targets ready for follow-up
• New discovery sources to explore
• Analytics improvements to implement

---
📧 Generated automatically every Sunday
🔄 Next weekly report: {(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')}
'''
    
    automation.email_sender.send_email(
        'team@open.build', 
        subject, 
        message, 
        'greg@open.build,greg@buildly.io'
    )
    print('Weekly analytics report sent successfully')

asyncio.run(send_weekly_report())
" >> "$LOG_DIR/cron.log" 2>&1

echo "\$(date): Weekly analytics report completed" >> "$LOG_DIR/cron.log"
EOF

# Make the weekly script executable
chmod +x "$WEEKLY_SCRIPT"

echo "✅ Created weekly analytics script: $WEEKLY_SCRIPT"
echo ""

# Backup existing crontab
echo "💾 Backing up existing crontab..."
crontab -l > "$SCRIPT_DIR/crontab_backup_$(date +%Y%m%d_%H%M%S).txt" 2>/dev/null || echo "No existing crontab found"

# Add cron jobs
echo "⏰ Setting up cron jobs..."

# Create temporary cron file
TEMP_CRON="/tmp/openbuild_cron_$$"

# Get existing crontab (if any)
crontab -l 2>/dev/null > "$TEMP_CRON" || echo "" > "$TEMP_CRON"

# Remove any existing Open Build cron jobs
sed -i '' '/Open Build Outreach/d' "$TEMP_CRON" 2>/dev/null || sed -i '/Open Build Outreach/d' "$TEMP_CRON"

# Add new cron jobs
cat >> "$TEMP_CRON" << EOF

# Open Build Outreach Automation - Daily Run at 9:00 AM
0 9 * * * $CRON_SCRIPT

# Open Build Outreach Automation - Weekly Analytics Report (Sundays at 8:00 AM)
0 8 * * 0 $WEEKLY_SCRIPT

# Open Build Outreach Automation - Log Cleanup (Monthly on 1st at 2:00 AM)
0 2 1 * * find "$LOG_DIR" -name "*.log" -type f -mtime +30 -delete

EOF

# Install the new crontab
crontab "$TEMP_CRON"

# Clean up
rm "$TEMP_CRON"

echo "✅ Cron jobs installed successfully!"
echo ""

# Display current crontab
echo "📅 Current cron schedule:"
echo "------------------------"
crontab -l | grep -A 10 -B 2 "Open Build"
echo ""

# Create monitoring script
MONITOR_SCRIPT="$SCRIPT_DIR/monitor_automation.sh"

cat > "$MONITOR_SCRIPT" << EOF
#!/bin/bash

# Open Build Outreach Automation Monitor
# Check system status and recent activity

echo "🔍 Open Build Outreach Automation Status"
echo "========================================"
echo "Current Time: \$(date)"
echo ""

echo "📊 Recent Automation Runs:"
echo "-------------------------"
if [ -f "$LOG_DIR/cron.log" ]; then
    tail -10 "$LOG_DIR/cron.log"
else
    echo "No cron log found"
fi
echo ""

echo "📈 Database Status:"
echo "-------------------"
if [ -f "outreach_automation.db" ]; then
    "$PYTHON_PATH" -c "
import sqlite3
conn = sqlite3.connect('outreach_automation.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM targets')
total_targets = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM targets WHERE last_contacted IS NOT NULL')
contacted = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM outreach_log WHERE created_at >= date(\"now\", \"-7 days\")')
recent_emails = cursor.fetchone()[0]
print(f'• Total targets: {total_targets}')
print(f'• Contacted targets: {contacted}')
print(f'• Emails sent (7 days): {recent_emails}')
conn.close()
"
else
    echo "No database found"
fi
echo ""

echo "📝 Log Files:"
echo "-------------"
if [ -d "$LOG_DIR" ]; then
    ls -la "$LOG_DIR"/*.log 2>/dev/null || echo "No log files found"
else
    echo "Log directory not found"
fi
echo ""

echo "⏰ Next Scheduled Run:"
echo "----------------------"
crontab -l | grep "Open Build" | head -1 | awk '{print "Daily automation: " \$1 " " \$2 " hours"}'
echo ""

echo "🔧 Quick Commands:"
echo "------------------"
echo "• Manual run: $PYTHON_PATH $AUTOMATION_SCRIPT --run"
echo "• Generate report: $PYTHON_PATH $AUTOMATION_SCRIPT --report"
echo "• View logs: tail -f $LOG_DIR/daily_automation.log"
echo "• Check cron: crontab -l | grep 'Open Build'"
EOF

chmod +x "$MONITOR_SCRIPT"

echo "✅ Created monitoring script: $MONITOR_SCRIPT"
echo ""

# Summary
echo "🎉 SETUP COMPLETE!"
echo "=================="
echo ""
echo "✅ Daily automation scheduled for 9:00 AM every day"
echo "✅ Weekly analytics reports scheduled for Sundays at 8:00 AM"
echo "✅ Monthly log cleanup scheduled for 1st of each month at 2:00 AM"
echo "✅ Error notifications configured"
echo "✅ Monitoring script available"
echo ""
echo "📧 All reports will be sent to:"
echo "   • team@open.build (primary)"
echo "   • greg@open.build (BCC)"
echo "   • greg@buildly.io (BCC)"
echo ""
echo "🔧 Management Commands:"
echo "   • Monitor status: ./monitor_automation.sh"
echo "   • View cron jobs: crontab -l"
echo "   • Test run: $PYTHON_PATH $AUTOMATION_SCRIPT --run"
echo "   • Remove cron: crontab -e (then delete Open Build lines)"
echo ""
echo "📁 Log Files Location: $LOG_DIR/"
echo "   • daily_automation.log - Main automation logs"
echo "   • daily_automation_errors.log - Error logs"
echo "   • weekly_analytics.log - Weekly report logs"
echo "   • cron.log - Cron execution logs"
echo ""
echo "🚀 The system will now run automatically every day!"
echo "   First run: Tomorrow at 9:00 AM"
echo "   First weekly report: Next Sunday at 8:00 AM"