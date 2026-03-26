#!/bin/bash

# Open Build Outreach Automation Monitor
# Check system status and recent activity

echo "🔍 Open Build Outreach Automation Status"
echo "========================================"
echo "Current Time: $(date)"
echo ""

echo "📊 Recent Automation Runs:"
echo "-------------------------"
if [ -f "/Users/greglind/Projects/open-build/open-build-new-website/logs/cron.log" ]; then
    tail -10 "/Users/greglind/Projects/open-build/open-build-new-website/logs/cron.log"
else
    echo "No cron log found"
fi
echo ""

echo "📈 Database Status:"
echo "-------------------"
if [ -f "outreach_automation.db" ]; then
    "/Users/greglind/Projects/open-build/open-build-new-website/.venv/bin/python" -c "
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
if [ -d "/Users/greglind/Projects/open-build/open-build-new-website/logs" ]; then
    ls -la "/Users/greglind/Projects/open-build/open-build-new-website/logs"/*.log 2>/dev/null || echo "No log files found"
else
    echo "Log directory not found"
fi
echo ""

echo "⏰ Next Scheduled Run:"
echo "----------------------"
crontab -l | grep "Open Build" | head -1 | awk '{print "Daily automation: " $1 " " $2 " hours"}'
echo ""

echo "🔧 Quick Commands:"
echo "------------------"
echo "• Manual run: /Users/greglind/Projects/open-build/open-build-new-website/.venv/bin/python /Users/greglind/Projects/open-build/open-build-new-website/outreach_automation.py --run"
echo "• Generate report: /Users/greglind/Projects/open-build/open-build-new-website/.venv/bin/python /Users/greglind/Projects/open-build/open-build-new-website/outreach_automation.py --report"
echo "• View logs: tail -f /Users/greglind/Projects/open-build/open-build-new-website/logs/daily_automation.log"
echo "• Check cron: crontab -l | grep 'Open Build'"
