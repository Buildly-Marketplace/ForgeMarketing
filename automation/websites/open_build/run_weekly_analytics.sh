#!/bin/bash

# Open Build Weekly Analytics Report
# Executed by cron weekly on Sundays at 8:00 AM

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
echo "$(date): Starting Open Build weekly analytics report..." >> "/Users/greglind/Projects/open-build/open-build-new-website/logs/cron.log"

# Generate weekly report
"/Users/greglind/Projects/open-build/open-build-new-website/.venv/bin/python" "/Users/greglind/Projects/open-build/open-build-new-website/scripts/outreach_automation.py" --report >> "/Users/greglind/Projects/open-build/open-build-new-website/logs/weekly_analytics.log" 2>> "/Users/greglind/Projects/open-build/open-build-new-website/logs/weekly_analytics_errors.log"

# Send comprehensive weekly analytics email
"/Users/greglind/Projects/open-build/open-build-new-website/.venv/bin/python" -c "
import sys
sys.path.append('/Users/greglind/Projects/open-build/open-build-new-website/scripts')
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
        os.getenv('TEAM_EMAIL', 'team@open.build'), 
        subject, 
        message, 
        os.getenv('BCC_EMAILS', 'greg@open.build,greg@buildly.io')
    )
    print('Weekly analytics report sent successfully')

asyncio.run(send_weekly_report())
" >> "/Users/greglind/Projects/open-build/open-build-new-website/logs/cron.log" 2>&1

echo "$(date): Weekly analytics report completed" >> "/Users/greglind/Projects/open-build/open-build-new-website/logs/cron.log"
