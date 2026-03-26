#!/usr/bin/env python3
"""
Test the enhanced daily report with analytics and new features
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from outreach_automation import OutreachAutomation

async def test_enhanced_report():
    """Test the enhanced daily report functionality"""
    
    print("🚀 Testing Enhanced Daily Report with Analytics")
    print("=" * 50)
    
    try:
        # Initialize the system
        automation = OutreachAutomation()
        
        # Create some test response data
        test_responses = [
            {
                'target_name': 'TechCrunch',
                'target_url': 'https://techcrunch.com',
                'response_type': 'email_reply',
                'content': 'Thanks for reaching out! We would love to feature Open Build in our upcoming article about innovative developer training programs.',
                'sentiment': 'positive',
                'date': datetime.now().isoformat()
            },
            {
                'target_name': 'Y Combinator',
                'target_url': 'https://ycombinator.com',
                'response_type': 'meeting_request',
                'content': 'This looks interesting. Can we schedule a 30-minute call to discuss partnership opportunities?',
                'sentiment': 'positive',
                'date': (datetime.now() - timedelta(days=1)).isoformat()
            }
        ]
        
        # Create some test new sources data
        test_sources = [
            {
                'url': 'https://startup-weekly.com',
                'type': 'publication',
                'discovery_method': 'web_scraping',
                'targets_found': 3,
                'date': datetime.now().isoformat()
            },
            {
                'url': 'https://developer-founders.io',
                'type': 'community',
                'discovery_method': 'social_media_discovery',
                'targets_found': 5,
                'date': (datetime.now() - timedelta(days=2)).isoformat()
            }
        ]
        
        # Collect analytics (this will use simulated data since APIs aren't configured)
        print("📊 Collecting analytics data...")
        website_analytics = await automation.analytics_manager.collect_website_analytics()
        youtube_analytics = await automation.analytics_manager.collect_youtube_analytics()
        social_analytics = await automation.analytics_manager.collect_social_media_analytics()
        
        analytics_data = {
            'website': website_analytics,
            'youtube': youtube_analytics,
            'social': social_analytics
        }
        
        print(f"✅ Website analytics: {website_analytics}")
        print(f"✅ YouTube analytics: {youtube_analytics}")
        print(f"✅ Social analytics: {social_analytics}")
        
        # Create test stats
        stats = {
            'new_targets': 2,
            'emails_sent': 4,
            'total_targets': 8,
            'errors': 0
        }
        
        # Get some test targets for the report
        targets_contacted = automation.db_manager.get_targets_for_outreach(limit=4)
        
        print("\n📧 Sending enhanced daily report...")
        print("Recipients:")
        print("- Primary: team@open.build")
        print("- BCC: greg@open.build, greg@buildly.io")
        
        # Send the enhanced daily report
        automation.email_sender.send_daily_report(
            stats=stats,
            targets_contacted=targets_contacted,
            analytics_data=analytics_data,
            responses=test_responses,
            new_sources=test_sources
        )
        
        print("\n✅ Enhanced daily report sent successfully!")
        print("\n📊 Report includes:")
        print("• Outreach summary with target details")
        print("• Recent responses with sentiment analysis")
        print("• New sources discovered")
        print("• Website analytics (visitors, page views, bounce rate)")
        print("• YouTube analytics (views, subscribers, videos)")
        print("• GitHub & social media stats")
        print("• Enhanced pipeline analytics")
        print("• Quick links and upcoming actions")
        
        print(f"\n📧 Check your email addresses for the comprehensive report!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing enhanced report: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    try:
        result = asyncio.run(test_enhanced_report())
        if result:
            print("\n🎉 Enhanced daily report test successful!")
        else:
            print("\n⚠️  Test encountered errors.")
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()