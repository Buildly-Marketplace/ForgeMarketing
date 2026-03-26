#!/usr/bin/env python3
"""
Outreach Analytics System
Provides comprehensive analytics for multi-brand outreach campaigns
"""

import sqlite3
from datetime import datetime, timedelta
import json
from pathlib import Path
import logging
from collections import defaultdict
from typing import Dict, List, Any

class OutreachAnalytics:
    """Analytics for outreach campaigns across all brands"""
    
    def __init__(self, database_path: str = None):
        """Initialize analytics system"""
        # Use project root relative path or environment variable
        project_root = Path(__file__).parent.parent
        default_db = project_root / 'data' / 'unified_outreach.db'
        self.database_path = database_path or os.getenv('OUTREACH_DB_PATH', str(default_db))
        self.logger = logging.getLogger(__name__)
        
    def get_campaign_overview(self, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive overview of all outreach campaigns"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Date filter
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            # Get campaign summary by brand
            campaign_query = """
            SELECT 
                brand,
                COUNT(DISTINCT target_id) as total_targets,
                COUNT(CASE WHEN last_outreach_date IS NOT NULL THEN 1 END) as contacted_targets,
                COUNT(CASE WHEN response_received = 1 THEN 1 END) as responses_received,
                AVG(CASE WHEN response_received = 1 THEN 
                    julianday(response_date) - julianday(last_outreach_date) 
                END) as avg_response_time
            FROM outreach_targets 
            WHERE created_at >= ? OR last_outreach_date >= ?
            GROUP BY brand
            """
            
            cursor.execute(campaign_query, [start_date, start_date])
            campaigns = cursor.fetchall()
            campaign_columns = [description[0] for description in cursor.description]
            
            # Get discovery sessions
            discovery_query = """
            SELECT 
                brand,
                COUNT(*) as discovery_sessions,
                SUM(targets_found) as total_targets_discovered,
                AVG(targets_found) as avg_targets_per_session
            FROM discovery_sessions 
            WHERE discovery_date >= ?
            GROUP BY brand
            """
            
            cursor.execute(discovery_query, [start_date])
            discoveries = cursor.fetchall()
            discovery_columns = [description[0] for description in cursor.description]
            
            # Get recent activity
            activity_query = """
            SELECT 
                brand,
                last_outreach_date,
                response_date,
                response_received
            FROM outreach_targets 
            WHERE last_outreach_date >= ? OR response_date >= ?
            ORDER BY COALESCE(response_date, last_outreach_date) DESC
            LIMIT 50
            """
            
            cursor.execute(activity_query, [start_date, start_date])
            activities = cursor.fetchall()
            activity_columns = [description[0] for description in cursor.description]
            
            conn.close()
            
            # Convert to dictionaries
            campaigns_data = [dict(zip(campaign_columns, row)) for row in campaigns]
            discoveries_data = [dict(zip(discovery_columns, row)) for row in discoveries]
            activities_data = [dict(zip(activity_columns, row)) for row in activities]
            
            # Create discovery lookup
            discovery_by_brand = {d['brand']: d for d in discoveries_data}
            
            # Process data
            overview = {
                'period_days': days,
                'total_brands': len(campaigns_data),
                'brands': {},
                'totals': {
                    'targets_discovered': sum(d.get('total_targets_discovered', 0) or 0 for d in discoveries_data),
                    'targets_contacted': sum(c.get('contacted_targets', 0) or 0 for c in campaigns_data),
                    'responses_received': sum(c.get('responses_received', 0) or 0 for c in campaigns_data),
                    'discovery_sessions': sum(d.get('discovery_sessions', 0) or 0 for d in discoveries_data)
                },
                'recent_activity': []
            }
            
            # Calculate overall metrics
            if overview['totals']['targets_contacted'] > 0:
                overview['totals']['response_rate'] = round(
                    (overview['totals']['responses_received'] / overview['totals']['targets_contacted']) * 100, 1
                )
            else:
                overview['totals']['response_rate'] = 0.0
            
            # Process brand-specific data
            for campaign in campaigns_data:
                brand = campaign['brand']
                brand_discovery = discovery_by_brand.get(brand, {})
                
                brand_data = {
                    'targets_in_database': int(campaign['total_targets']),
                    'targets_contacted': int(campaign['contacted_targets']),
                    'responses_received': int(campaign['responses_received']),
                    'targets_discovered': int(brand_discovery.get('total_targets_discovered', 0) or 0),
                    'discovery_sessions': int(brand_discovery.get('discovery_sessions', 0) or 0),
                    'avg_targets_per_session': float(brand_discovery.get('avg_targets_per_session', 0) or 0)
                }
                
                # Calculate response rate
                if brand_data['targets_contacted'] > 0:
                    brand_data['response_rate'] = round(
                        (brand_data['responses_received'] / brand_data['targets_contacted']) * 100, 1
                    )
                else:
                    brand_data['response_rate'] = 0.0
                
                # Calculate average response time (in days)
                if campaign['avg_response_time'] is not None:
                    brand_data['avg_response_time_days'] = round(float(campaign['avg_response_time']), 1)
                else:
                    brand_data['avg_response_time_days'] = None
                
                overview['brands'][brand] = brand_data
            
            # Process recent activity
            for activity in activities_data[:20]:
                activity_item = {
                    'brand': activity['brand'],
                    'date': activity['last_outreach_date'] or activity['response_date'],
                    'type': 'response' if activity['response_received'] else 'outreach'
                }
                overview['recent_activity'].append(activity_item)
            
            return overview
            
        except Exception as e:
            self.logger.error(f"Error getting campaign overview: {e}")
            return {
                'error': str(e),
                'period_days': days,
                'total_brands': 0,
                'brands': {},
                'totals': {
                    'targets_discovered': 0,
                    'targets_contacted': 0,
                    'responses_received': 0,
                    'response_rate': 0.0,
                    'discovery_sessions': 0
                },
                'recent_activity': []
            }
    
    def get_brand_performance(self, brand: str, days: int = 30) -> Dict[str, Any]:
        """Get detailed performance metrics for a specific brand"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            # Get targets data
            targets_query = """
            SELECT 
                target_id,
                company_name,
                contact_name,
                email,
                source,
                created_at,
                last_outreach_date,
                outreach_count,
                response_received,
                response_date
            FROM outreach_targets 
            WHERE brand = ? AND (created_at >= ? OR last_outreach_date >= ?)
            ORDER BY COALESCE(response_date, last_outreach_date, created_at) DESC
            """
            
            cursor.execute(targets_query, [brand, start_date, start_date])
            targets = cursor.fetchall()
            target_columns = [description[0] for description in cursor.description]
            
            # Get discovery sessions
            discovery_query = """
            SELECT 
                discovery_date,
                targets_found,
                search_terms,
                platforms_searched
            FROM discovery_sessions 
            WHERE brand = ? AND discovery_date >= ?
            ORDER BY discovery_date DESC
            """
            
            cursor.execute(discovery_query, [brand, start_date])
            discoveries = cursor.fetchall()
            discovery_columns = [description[0] for description in cursor.description]
            
            conn.close()
            
            # Convert to dictionaries
            targets_data = [dict(zip(target_columns, row)) for row in targets]
            discoveries_data = [dict(zip(discovery_columns, row)) for row in discoveries]
            
            # Process performance metrics
            contacted_targets = len([t for t in targets_data if t['last_outreach_date']])
            responses_received = len([t for t in targets_data if t['response_received'] == 1])
            targets_discovered = sum(d.get('targets_found', 0) or 0 for d in discoveries_data)
            
            performance = {
                'brand': brand,
                'period_days': days,
                'metrics': {
                    'total_targets': len(targets_data),
                    'contacted_targets': contacted_targets,
                    'responses_received': responses_received,
                    'discovery_sessions': len(discoveries_data),
                    'targets_discovered': targets_discovered
                },
                'targets': [],
                'discovery_sessions': []
            }
            
            # Calculate response rate
            if performance['metrics']['contacted_targets'] > 0:
                performance['metrics']['response_rate'] = round(
                    (performance['metrics']['responses_received'] / performance['metrics']['contacted_targets']) * 100, 1
                )
            else:
                performance['metrics']['response_rate'] = 0.0
            
            # Process targets data (first 50)
            for target in targets_data[:50]:
                target_data = {
                    'target_id': target['target_id'],
                    'company_name': target['company_name'],
                    'contact_name': target['contact_name'],
                    'email': target['email'],
                    'source': target['source'],
                    'created_at': target['created_at'],
                    'last_outreach_date': target['last_outreach_date'],
                    'outreach_count': int(target['outreach_count']) if target['outreach_count'] is not None else 0,
                    'response_received': bool(target['response_received']),
                    'response_date': target['response_date']
                }
                performance['targets'].append(target_data)
            
            # Process discovery sessions (first 20)
            for session in discoveries_data[:20]:
                session_data = {
                    'discovery_date': session['discovery_date'],
                    'targets_found': int(session['targets_found']),
                    'search_terms': session['search_terms'],
                    'platforms_searched': session['platforms_searched']
                }
                performance['discovery_sessions'].append(session_data)
            
            return performance
            
        except Exception as e:
            self.logger.error(f"Error getting brand performance for {brand}: {e}")
            return {
                'error': str(e),
                'brand': brand,
                'period_days': days,
                'metrics': {
                    'total_targets': 0,
                    'contacted_targets': 0,
                    'responses_received': 0,
                    'response_rate': 0.0,
                    'discovery_sessions': 0,
                    'targets_discovered': 0
                },
                'targets': [],
                'discovery_sessions': []
            }
    
    def get_daily_stats(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get daily statistics for the past N days"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            daily_stats = []
            
            for i in range(days):
                date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                
                # Outreach stats for this day
                outreach_query = """
                SELECT 
                    brand,
                    COUNT(*) as emails_sent,
                    COUNT(CASE WHEN response_received = 1 AND response_date = ? THEN 1 END) as responses_received
                FROM outreach_targets 
                WHERE last_outreach_date = ?
                GROUP BY brand
                """
                
                cursor.execute(outreach_query, [date, date])
                outreach_data = cursor.fetchall()
                outreach_columns = [description[0] for description in cursor.description]
                
                # Discovery stats for this day
                discovery_query = """
                SELECT 
                    brand,
                    SUM(targets_found) as targets_discovered
                FROM discovery_sessions 
                WHERE discovery_date = ?
                GROUP BY brand
                """
                
                cursor.execute(discovery_query, [date])
                discovery_data = cursor.fetchall()
                discovery_columns = [description[0] for description in cursor.description]
                
                # Convert to dictionaries
                outreach_list = [dict(zip(outreach_columns, row)) for row in outreach_data]
                discovery_list = [dict(zip(discovery_columns, row)) for row in discovery_data]
                
                # Compile daily stats
                total_emails = sum(o.get('emails_sent', 0) or 0 for o in outreach_list)
                total_responses = sum(o.get('responses_received', 0) or 0 for o in outreach_list)
                total_discoveries = sum(d.get('targets_discovered', 0) or 0 for d in discovery_list)
                
                day_stats = {
                    'date': date,
                    'total_emails_sent': total_emails,
                    'total_responses': total_responses,
                    'total_discoveries': total_discoveries,
                    'brands': {}
                }
                
                # Brand-specific stats
                for row in outreach_list:
                    brand = row['brand']
                    if brand not in day_stats['brands']:
                        day_stats['brands'][brand] = {'emails_sent': 0, 'responses': 0, 'discoveries': 0}
                    day_stats['brands'][brand]['emails_sent'] = int(row['emails_sent'])
                    day_stats['brands'][brand]['responses'] = int(row['responses_received'])
                
                for row in discovery_list:
                    brand = row['brand']
                    if brand not in day_stats['brands']:
                        day_stats['brands'][brand] = {'emails_sent': 0, 'responses': 0, 'discoveries': 0}
                    day_stats['brands'][brand]['discoveries'] = int(row['targets_discovered'])
                
                daily_stats.append(day_stats)
            
            conn.close()
            return daily_stats
            
        except Exception as e:
            self.logger.error(f"Error getting daily stats: {e}")
            return []

def main():
    """Test the outreach analytics system"""
    analytics = OutreachAnalytics()
    
    print("=== Outreach Campaign Overview (Last 30 days) ===")
    overview = analytics.get_campaign_overview(30)
    
    if 'error' not in overview:
        print(f"Total Brands: {overview['total_brands']}")
        print(f"Targets Discovered: {overview['totals']['targets_discovered']}")
        print(f"Targets Contacted: {overview['totals']['targets_contacted']}")
        print(f"Responses Received: {overview['totals']['responses_received']}")
        print(f"Response Rate: {overview['totals']['response_rate']}%")
        
        print("\n=== Brand Performance ===")
        for brand, data in overview['brands'].items():
            print(f"{brand.title()}: {data['targets_contacted']} contacted, {data['responses_received']} responses ({data['response_rate']}%)")
    else:
        print(f"Error: {overview['error']}")
    
    print("\n=== Daily Stats (Last 7 days) ===")
    daily_stats = analytics.get_daily_stats(7)
    for day in daily_stats[:3]:  # Show last 3 days
        print(f"{day['date']}: {day['total_emails_sent']} emails, {day['total_responses']} responses, {day['total_discoveries']} discoveries")

if __name__ == "__main__":
    main()