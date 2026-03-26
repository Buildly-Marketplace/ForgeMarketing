# Website Analytics Monitor
# Monitors performance across all Buildly ecosystem websites

import os
import sys
import logging
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path
import json
import time

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class WebsiteMonitor:
    """
    Monitors all Buildly ecosystem websites dynamically loaded from database
    """
    
    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.data_dir = self.project_root / 'data'
        self.logs_dir = self.project_root / 'logs'
        
        # Load website configurations from database
        self.websites = self._load_website_configs()
        
        # Set up logging
        self.setup_logging()
    
    def _load_website_configs(self) -> Dict[str, Dict[str, Any]]:
        """Load website configurations from database"""
        import sys
        sys.path.insert(0, str(self.project_root))
        
        from config.brand_loader import get_all_brands, get_brand_details
        
        configs = {}
        brands = get_all_brands(active_only=True)
        
        for brand in brands:
            brand_data = get_brand_details(brand)
            if brand_data:
                configs[brand] = {
                    'name': brand_data.get('display_name', brand.title()),
                    'url': brand_data.get('website_url', f'https://{brand}.io'),
                    'type': 'website',
                    'expected_pages': ['/', '/about.html', '/contact.html']
                }
        
        return configs
        
    def setup_logging(self):
        """Set up logging for website monitoring"""
        self.logs_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.logs_dir / 'website_monitor.log'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('WebsiteMonitor')
    
    async def check_website_health(self, website_key: str, website_config: Dict[str, Any]) -> Dict[str, Any]:
        """Check health and performance of a single website"""
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                url = website_config['url']
                
                # Check main page
                async with session.get(url, timeout=30) as response:
                    response_time = time.time() - start_time
                    
                    health_data = {
                        'website': website_key,
                        'name': website_config['name'],
                        'url': url,
                        'timestamp': datetime.now().isoformat(),
                        'status_code': response.status,
                        'response_time': round(response_time, 3),
                        'is_healthy': response.status == 200,
                        'content_length': len(await response.text()) if response.status == 200 else 0,
                        'headers': dict(response.headers)
                    }
                    
                    # Check expected pages
                    page_status = {}
                    for page in website_config.get('expected_pages', []):
                        try:
                            page_url = f"{url.rstrip('/')}{page}" if page != '/' else url
                            async with session.get(page_url, timeout=15) as page_response:
                                page_status[page] = {
                                    'status_code': page_response.status,
                                    'is_accessible': page_response.status == 200
                                }
                        except Exception as e:
                            page_status[page] = {
                                'status_code': 0,
                                'is_accessible': False,
                                'error': str(e)
                            }
                    
                    health_data['pages'] = page_status
                    
                    return health_data
                    
        except asyncio.TimeoutError:
            return {
                'website': website_key,
                'name': website_config['name'],
                'url': website_config['url'],
                'timestamp': datetime.now().isoformat(),
                'status_code': 0,
                'response_time': time.time() - start_time,
                'is_healthy': False,
                'error': 'Timeout'
            }
        except Exception as e:
            return {
                'website': website_key,
                'name': website_config['name'],
                'url': website_config['url'],
                'timestamp': datetime.now().isoformat(),
                'status_code': 0,
                'response_time': time.time() - start_time,
                'is_healthy': False,
                'error': str(e)
            }
    
    async def monitor_all_websites(self) -> Dict[str, Any]:
        """Monitor all websites concurrently"""
        self.logger.info("🌐 Starting website health monitoring")
        
        # Check all websites concurrently
        tasks = []
        for website_key, config in self.websites.items():
            task = self.check_website_health(website_key, config)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        # Compile monitoring report
        monitoring_report = {
            'timestamp': datetime.now().isoformat(),
            'total_websites': len(self.websites),
            'healthy_websites': sum(1 for result in results if result.get('is_healthy', False)),
            'websites': {result['website']: result for result in results}
        }
        
        # Log results
        for result in results:
            website = result['website']
            status = "✅" if result.get('is_healthy', False) else "❌"
            response_time = result.get('response_time', 0)
            status_code = result.get('status_code', 0)
            
            self.logger.info(f"{status} {website}: {status_code} ({response_time}s)")
        
        # Save monitoring data
        await self.save_monitoring_data(monitoring_report)
        
        return monitoring_report
    
    async def save_monitoring_data(self, report: Dict[str, Any]):
        """Save monitoring data to file"""
        try:
            # Ensure data directory exists
            monitoring_dir = self.data_dir / 'monitoring'
            monitoring_dir.mkdir(parents=True, exist_ok=True)
            
            # Save daily report
            date_str = datetime.now().strftime('%Y%m%d')
            filename = f"website_health_{date_str}.json"
            filepath = monitoring_dir / filename
            
            # Load existing data or create new
            if filepath.exists():
                with open(filepath, 'r') as f:
                    daily_data = json.load(f)
            else:
                daily_data = {'date': date_str, 'checks': []}
            
            # Append new check
            daily_data['checks'].append(report)
            
            # Save updated data
            with open(filepath, 'w') as f:
                json.dump(daily_data, f, indent=2)
            
            self.logger.info(f"Monitoring data saved to {filename}")
            
        except Exception as e:
            self.logger.error(f"Failed to save monitoring data: {e}")
    
    def get_website_uptime_stats(self, days: int = 7) -> Dict[str, Any]:
        """Get uptime statistics for the last N days"""
        try:
            monitoring_dir = self.data_dir / 'monitoring'
            
            if not monitoring_dir.exists():
                return {'error': 'No monitoring data available'}
            
            stats = {}
            
            # Check last N days
            for i in range(days):
                date = datetime.now() - timedelta(days=i)
                date_str = date.strftime('%Y%m%d')
                filename = f"website_health_{date_str}.json"
                filepath = monitoring_dir / filename
                
                if filepath.exists():
                    with open(filepath, 'r') as f:
                        daily_data = json.load(f)
                    
                    for check in daily_data.get('checks', []):
                        for website_key, website_data in check.get('websites', {}).items():
                            if website_key not in stats:
                                stats[website_key] = {
                                    'name': website_data.get('name', website_key),
                                    'total_checks': 0,
                                    'successful_checks': 0,
                                    'uptime_percentage': 0.0,
                                    'avg_response_time': 0.0,
                                    'response_times': []
                                }
                            
                            stats[website_key]['total_checks'] += 1
                            
                            if website_data.get('is_healthy', False):
                                stats[website_key]['successful_checks'] += 1
                            
                            response_time = website_data.get('response_time', 0)
                            if response_time > 0:
                                stats[website_key]['response_times'].append(response_time)
            
            # Calculate final statistics
            for website_key in stats:
                if stats[website_key]['total_checks'] > 0:
                    stats[website_key]['uptime_percentage'] = (
                        stats[website_key]['successful_checks'] / 
                        stats[website_key]['total_checks'] * 100
                    )
                
                if stats[website_key]['response_times']:
                    stats[website_key]['avg_response_time'] = (
                        sum(stats[website_key]['response_times']) / 
                        len(stats[website_key]['response_times'])
                    )
                
                # Remove raw response times from output
                del stats[website_key]['response_times']
            
            return {
                'period_days': days,
                'generated_at': datetime.now().isoformat(),
                'websites': stats
            }
            
        except Exception as e:
            self.logger.error(f"Error generating uptime stats: {e}")
            return {'error': str(e)}
    
    async def generate_monitoring_report(self) -> str:
        """Generate a comprehensive monitoring report"""
        # Get current health status
        current_status = await self.monitor_all_websites()
        
        # Get uptime statistics
        uptime_stats = self.get_website_uptime_stats(7)
        
        # Generate report
        report = f"""
🌐 Website Monitoring Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

CURRENT STATUS:
===============
Total Websites: {current_status['total_websites']}
Healthy: {current_status['healthy_websites']}/{current_status['total_websites']}

Website Details:
"""
        
        for website_key, data in current_status['websites'].items():
            status_icon = "✅" if data.get('is_healthy', False) else "❌"
            report += f"\n{status_icon} {data['name']}"
            report += f"\n   URL: {data['url']}"
            report += f"\n   Status: {data.get('status_code', 'N/A')}"
            report += f"\n   Response Time: {data.get('response_time', 'N/A')}s"
            
            if 'pages' in data:
                accessible_pages = sum(1 for page in data['pages'].values() if page.get('is_accessible', False))
                total_pages = len(data['pages'])
                report += f"\n   Pages Accessible: {accessible_pages}/{total_pages}"
        
        if uptime_stats.get('websites'):
            report += f"\n\n7-DAY UPTIME STATISTICS:\n========================"
            
            for website_key, stats in uptime_stats['websites'].items():
                uptime = stats.get('uptime_percentage', 0)
                avg_response = stats.get('avg_response_time', 0)
                report += f"\n{stats['name']}: {uptime:.1f}% uptime, {avg_response:.2f}s avg response"
        
        return report

async def main():
    """Main entry point for website monitoring"""
    monitor = WebsiteMonitor()
    
    print("🌐 Website Monitor")
    print("Choose an option:")
    print("1. Check all websites now")
    print("2. Generate monitoring report")
    print("3. Get 7-day uptime statistics")
    
    choice = input("Enter your choice (1-3): ")
    
    if choice == '1':
        results = await monitor.monitor_all_websites()
        print(f"✅ Monitoring completed. {results['healthy_websites']}/{results['total_websites']} websites healthy")
    
    elif choice == '2':
        report = await monitor.generate_monitoring_report()
        print(report)
    
    elif choice == '3':
        stats = monitor.get_website_uptime_stats(7)
        if 'error' in stats:
            print(f"❌ Error: {stats['error']}")
        else:
            print(json.dumps(stats, indent=2))
    
    else:
        print("Invalid choice")

if __name__ == "__main__":
    asyncio.run(main())