#!/usr/bin/env python3
"""
Real Analytics Dashboard Integration
===================================

Replaces the mock analytics system with real data collection
using the proven foundry approach. Integrates with the existing
dashboard to show real website and email performance metrics.
"""

import os
import sys
import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add the automation directory to the Python path
automation_dir = Path(__file__).parent
sys.path.append(str(automation_dir))

from analytics.multi_brand_analytics import analytics_collector, BRAND_CONFIGS

class RealAnalyticsDashboard:
    """Real analytics integration for the outreach dashboard"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.cache_file = self.project_root / 'data' / 'analytics' / 'latest_analytics.json'
        self.cache_duration = timedelta(hours=6)  # Refresh every 6 hours
    
    async def get_dashboard_analytics(self, brand: str = None) -> dict:
        """Get analytics data for the dashboard"""
        
        # Check if we have recent cached data
        if self._is_cache_valid():
            cached_data = self._load_cached_analytics()
            if cached_data:
                return self._format_dashboard_data(cached_data, brand)
        
        # Collect fresh analytics data
        print("🔄 Collecting fresh analytics data...")
        analytics_data = await analytics_collector.collect_all_brands_analytics(days_back=30)
        
        # Save to cache
        self._save_cache(analytics_data)
        
        return self._format_dashboard_data(analytics_data, brand)
    
    def _is_cache_valid(self) -> bool:
        """Check if cached data is still valid"""
        if not self.cache_file.exists():
            return False
        
        file_age = datetime.now() - datetime.fromtimestamp(self.cache_file.stat().st_mtime)
        return file_age < self.cache_duration
    
    def _load_cached_analytics(self) -> dict:
        """Load analytics data from cache"""
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading cache: {e}")
            return None
    
    def _save_cache(self, data: dict):
        """Save analytics data to cache"""
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def _format_dashboard_data(self, analytics_data: dict, brand: str = None) -> dict:
        """Format analytics data for dashboard display"""
        
        if brand and brand in analytics_data:
            # Return single brand data
            brand_data = analytics_data[brand]
            return self._format_single_brand(brand_data, brand)
        else:
            # Return multi-brand summary
            return self._format_multi_brand_summary(analytics_data)
    
    def _format_single_brand(self, brand_data: dict, brand_key: str) -> dict:
        """Format data for a single brand"""
        website = brand_data.get('website_analytics', {})
        email = brand_data.get('email_analytics', {})
        performance = brand_data.get('performance_summary', {})
        brand_config = BRAND_CONFIGS.get(brand_key, {})
        
        return {
            'brand': {
                'key': brand_key,
                'name': brand_config.get('name', brand_key),
                'website': brand_config.get('website', ''),
                'color': brand_config.get('color_theme', '#2563eb')
            },
            'website': {
                'sessions': website.get('sessions', 0),
                'users': website.get('users', 0),
                'pageviews': website.get('pageviews', 0),
                'bounce_rate': website.get('bounce_rate', 0.0),
                'avg_duration': website.get('avg_session_duration', 0),
                'top_pages': website.get('top_pages', []),
                'traffic_sources': website.get('traffic_sources', {})
            },
            'email': {
                'sent': email.get('total_sent', 0),
                'opened': email.get('total_opened', 0),
                'clicked': email.get('total_clicked', 0),
                'open_rate': email.get('avg_open_rate', 0.0),
                'click_rate': email.get('avg_click_rate', 0.0)
            },
            'performance': {
                'score': performance.get('overall_score', 5.0),
                'rating': performance.get('performance_rating', 'unknown'),
                'recommendations': performance.get('recommendations', [])
            },
            'last_updated': brand_data.get('collected_at', datetime.now().isoformat())
        }
    
    def _format_multi_brand_summary(self, analytics_data: dict) -> dict:
        """Format multi-brand summary data"""
        summary = analytics_data.get('summary', {})
        brands = []
        
        for brand_key, brand_data in analytics_data.items():
            if brand_key == 'summary':
                continue
                
            brand_config = BRAND_CONFIGS.get(brand_key, {})
            website = brand_data.get('website_analytics', {})
            email = brand_data.get('email_analytics', {})
            performance = brand_data.get('performance_summary', {})
            
            brands.append({
                'key': brand_key,
                'name': brand_config.get('name', brand_key),
                'website': brand_config.get('website', ''),
                'color': brand_config.get('color_theme', '#2563eb'),
                'sessions': website.get('sessions', 0),
                'users': website.get('users', 0),
                'emails_sent': email.get('total_sent', 0),
                'performance_score': performance.get('overall_score', 5.0),
                'performance_rating': performance.get('performance_rating', 'unknown')
            })
        
        return {
            'summary': {
                'total_brands': summary.get('total_brands', 0),
                'total_sessions': summary.get('total_website_sessions', 0),
                'total_users': summary.get('total_website_users', 0),
                'total_emails': summary.get('total_emails_sent', 0),
                'avg_sessions': summary.get('avg_sessions_per_brand', 0)
            },
            'brands': brands,
            'last_updated': summary.get('generated_at', datetime.now().isoformat())
        }

# Create dashboard instance
real_analytics = RealAnalyticsDashboard()

def get_analytics_for_dashboard(brand: str = None):
    """Synchronous wrapper for dashboard use"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(real_analytics.get_dashboard_analytics(brand))
    finally:
        loop.close()

async def main():
    """Test the real analytics dashboard integration"""
    print("🚀 Testing Real Analytics Dashboard Integration")
    print("=" * 60)
    
    dashboard = RealAnalyticsDashboard()
    
    # Test multi-brand summary
    print("\n📊 Multi-Brand Summary:")
    summary_data = await dashboard.get_dashboard_analytics()
    
    print(f"Total Brands: {summary_data['summary']['total_brands']}")
    print(f"Total Sessions: {summary_data['summary']['total_sessions']:,}")
    print(f"Total Users: {summary_data['summary']['total_users']:,}")
    
    print("\n🏢 Brand Performance:")
    for brand in summary_data['brands']:
        print(f"  {brand['name']}: {brand['sessions']:,} sessions, {brand['performance_rating']} performance")
    
    # Test single brand data
    print(f"\n🔍 Detailed Brand Data (Buildly):")
    buildly_data = await dashboard.get_dashboard_analytics('buildly')
    
    print(f"Website Sessions: {buildly_data['website']['sessions']:,}")
    print(f"Email Campaigns: {buildly_data['email']['sent']} sent")
    print(f"Performance Score: {buildly_data['performance']['score']}/10")
    print(f"Top Pages: {len(buildly_data['website']['top_pages'])} pages tracked")
    
    print("\n✅ Real analytics integration ready for dashboard!")

if __name__ == '__main__':
    asyncio.run(main())