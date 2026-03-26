#!/usr/bin/env python3
"""
Weekly Analytics Report Generator
Generates comprehensive weekly analytics reports for all brands and marketing activities
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from pathlib import Path
import json

# Get project root directory
project_root = Path(__file__).parent.parent

# Add project root to Python path for imports
sys.path.insert(0, str(project_root))

# Import brand loader
from config.brand_loader import get_all_brands

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(project_root / 'logs' / 'weekly_analytics.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('WeeklyAnalytics')

def generate_activity_summary():
    """Generate activity summary from activity tracker"""
    try:
        from automation.activity_tracker import ActivityTracker
        
        tracker = ActivityTracker()
        
        # Get weekly activity data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        # Get AI generation stats
        ai_stats = tracker.get_ai_generation_stats(
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        
        # Get email stats
        email_stats = tracker.get_email_stats(
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        
        # Get campaign stats
        campaign_stats = tracker.get_campaign_stats(
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        
        return {
            'ai_generation': ai_stats,
            'email_campaigns': email_stats,
            'campaigns': campaign_stats,
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Error generating activity summary: {e}")
        return None

def generate_outreach_analytics():
    """Generate outreach analytics from unified database"""
    try:
        from automation.unified_analytics import UnifiedOutreachAnalytics
        
        analytics = UnifiedOutreachAnalytics()
        
        # Get 7-day overview for all brands
        overview = analytics.get_all_brands_overview(days=7)
        
        # Get brand-specific breakdowns - load from database
        brands = get_all_brands(active_only=True)
        brand_analytics = {}
        for brand in brands:
            try:
                brand_data = analytics.get_brand_analytics(brand, days=7)
                if 'error' not in brand_data:
                    brand_analytics[brand] = brand_data
            except Exception as e:
                logger.warning(f"⚠️ Could not get analytics for {brand}: {e}")
        
        return {
            'overview': overview,
            'brands': brand_analytics
        }
        
    except Exception as e:
        logger.error(f"❌ Error generating outreach analytics: {e}")
        return None

def generate_website_analytics():
    """Generate website analytics from real analytics dashboard"""
    try:
        from automation.real_analytics_dashboard import RealAnalyticsDashboard
        
        dashboard = RealAnalyticsDashboard()
        
        # Get comprehensive analytics for all brands
        all_analytics = dashboard.get_all_brand_analytics()
        
        # Filter for weekly data (if available)
        weekly_analytics = {}
        for brand, data in all_analytics.items():
            if data and 'error' not in data:
                weekly_analytics[brand] = {
                    'website': data.get('website_analytics', {}),
                    'email': data.get('email_analytics', {}),
                    'social': data.get('social_analytics', {}),
                    'collected_at': data.get('collected_at')
                }
        
        return weekly_analytics
        
    except Exception as e:
        logger.error(f"❌ Error generating website analytics: {e}")
        return None

def format_analytics_report(activity_data, outreach_data, website_data):
    """Format all analytics data into a comprehensive report"""
    report_date = datetime.now().strftime('%Y-%m-%d')
    week_start = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    report = f"""
# Weekly Marketing Analytics Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Period:** {week_start} to {report_date}

## Executive Summary
"""
    
    # Activity Summary
    if activity_data:
        ai_stats = activity_data.get('ai_generation', {})
        email_stats = activity_data.get('email_campaigns', {})
        
        report += f"""
### Content Generation Activity
- **AI Content Generated:** {ai_stats.get('total_generations', 0)} pieces
- **Brands Active:** {len(ai_stats.get('by_brand', {}))} brands
- **Average Quality Score:** {ai_stats.get('avg_quality_score', 0):.1f}/10
- **Success Rate:** {ai_stats.get('success_rate', 0):.1f}%

### Email Campaign Activity  
- **Emails Sent:** {email_stats.get('total_sent', 0)}
- **Delivery Rate:** {email_stats.get('delivery_rate', 0):.1f}%
- **Open Rate:** {email_stats.get('open_rate', 0):.1f}%
- **Click Rate:** {email_stats.get('click_rate', 0):.1f}%
"""
    
    # Outreach Analytics
    if outreach_data and outreach_data.get('overview'):
        overview = outreach_data['overview']
        
        report += f"""
### Outreach Campaign Performance
- **Total Outreach Emails:** {overview.get('total_emails_sent', 0)}
- **Response Rate:** {overview.get('overall_response_rate', 0):.1f}%
- **Active Brands:** {len(outreach_data.get('brands', {}))}
- **Database Records:** {overview.get('total_database_records', 0)}
"""
    
    # Website Analytics
    if website_data:
        total_sessions = sum(
            brand_data.get('website', {}).get('overview', {}).get('sessions', 0)
            for brand_data in website_data.values()
        )
        
        report += f"""
### Website Performance
- **Total Sessions:** {total_sessions:,}
- **Active Websites:** {len(website_data)}
"""
        
        for brand, data in website_data.items():
            website = data.get('website', {}).get('overview', {})
            if website:
                report += f"""
#### {brand.title()} Website
- Sessions: {website.get('sessions', 0):,}
- Users: {website.get('users', 0):,}
- Pageviews: {website.get('pageviews', 0):,}
- Bounce Rate: {website.get('bounce_rate', 0):.1f}%
"""
    
    # Brand-specific outreach details
    if outreach_data and outreach_data.get('brands'):
        report += "\n## Brand-Specific Outreach Details\n"
        
        for brand, data in outreach_data['brands'].items():
            if data and 'error' not in data:
                stats = data.get('summary_stats', {})
                report += f"""
### {brand.title()}
- **Emails Sent:** {stats.get('total_sent', 0)}
- **Responses:** {stats.get('total_responses', 0)}
- **Response Rate:** {stats.get('response_rate', 0):.1f}%
- **Database Contacts:** {stats.get('total_contacts', 0)}
"""
    
    report += f"""
---
*Generated by Marketing Automation System*
*Report ID: weekly-{report_date}*
"""
    
    return report

def save_report(report_content):
    """Save the report to file"""
    try:
        reports_dir = project_root / 'reports'
        reports_dir.mkdir(exist_ok=True)
        
        report_filename = f"weekly-analytics-{datetime.now().strftime('%Y-%m-%d')}.md"
        report_path = reports_dir / report_filename
        
        with open(report_path, 'w') as f:
            f.write(report_content)
        
        logger.info(f"📄 Report saved to {report_path}")
        return str(report_path)
        
    except Exception as e:
        logger.error(f"❌ Error saving report: {e}")
        return None

def email_report(report_content, report_path):
    """Email the report to stakeholders"""
    try:
        from automation.daily_analytics_emailer import DailyAnalyticsEmailer
        
        emailer = DailyAnalyticsEmailer()
        
        # Send HTML version of the report
        html_content = report_content.replace('\n', '<br>').replace('# ', '<h1>').replace('## ', '<h2>').replace('### ', '<h3>')
        
        result = emailer.send_daily_report(
            subject=f"Weekly Marketing Analytics Report - {datetime.now().strftime('%Y-%m-%d')}",
            content=html_content,
            recipients=['greg@buildly.io'],  # Configure as needed
            attachments=[report_path] if report_path else None
        )
        
        if result.get('success'):
            logger.info("📧 Weekly report emailed successfully")
        else:
            logger.error(f"❌ Error emailing report: {result.get('error')}")
        
    except Exception as e:
        logger.error(f"❌ Error emailing report: {e}")

def main():
    """Main weekly analytics report generator"""
    logger.info("📊 Starting weekly analytics report generation")
    
    try:
        # Generate all analytics data
        logger.info("📈 Gathering activity data...")
        activity_data = generate_activity_summary()
        
        logger.info("📧 Gathering outreach analytics...")
        outreach_data = generate_outreach_analytics()
        
        logger.info("🌐 Gathering website analytics...")
        website_data = generate_website_analytics()
        
        # Format comprehensive report
        logger.info("📝 Formatting analytics report...")
        report_content = format_analytics_report(activity_data, outreach_data, website_data)
        
        # Save report
        report_path = save_report(report_content)
        
        # Email report
        email_report(report_content, report_path)
        
        logger.info("✅ Weekly analytics report generated and distributed successfully")
        
    except Exception as e:
        logger.error(f"❌ Error generating weekly analytics report: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()