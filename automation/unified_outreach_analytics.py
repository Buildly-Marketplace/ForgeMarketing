#!/usr/bin/env python3
"""
Unified Outreach Analytics System
Reads from existing SQLite databases and JSON files in each website folder
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import logging

class UnifiedOutreachAnalytics:
    """Analytics system that reads from existing website databases and data files"""
    
    def __init__(self, workspace_root: str = None):
        """Initialize analytics system with existing data sources"""
        self.logger = logging.getLogger(__name__)
        # Use provided path, environment variable, or project root
        if workspace_root:
            self.workspace_root = Path(workspace_root)
        elif os.getenv('WORKSPACE_ROOT'):
            self.workspace_root = Path(os.getenv('WORKSPACE_ROOT'))
        else:
            self.workspace_root = Path(__file__).parent.parent
        
        # Load brand data sources dynamically from database
        self.brand_data_sources = self._load_brand_data_sources()
    
    def _load_brand_data_sources(self) -> Dict[str, Dict[str, Any]]:
        """Load brand data source configurations dynamically"""
        import sys
        sys.path.insert(0, str(self.workspace_root))
        
        from config.brand_loader import get_all_brands
        
        sources = {}
        brands = get_all_brands(active_only=True)
        
        for brand in brands:
            # Default configuration
            sources[brand] = {
                'type': 'json',
                'base_path': self.workspace_root / 'websites' / f'{brand}-website' / 'outreach_data',
                'files': {
                    'targets': 'targets.json',
                    'outreach_log': 'outreach_log.json',
                    'analytics': 'analytics.json'
                }
            }
        
        return sources
    
    def get_brand_overview(self, brand: str) -> Dict[str, Any]:
        """Get comprehensive overview for a specific brand"""
        try:
            if brand not in self.brand_data_sources:
                return {'error': f'Brand {brand} not configured'}
            
            source_config = self.brand_data_sources[brand]
            
            if source_config['type'] == 'sqlite':
                return self._get_sqlite_overview(brand, source_config)
            elif source_config['type'] == 'json':
                return self._get_json_overview(brand, source_config)
            else:
                return {'error': f'Unknown data source type: {source_config["type"]}'}
                
        except Exception as e:
            self.logger.error(f"Error getting brand overview for {brand}: {e}")
            return {'error': str(e)}
    
    def _get_sqlite_overview(self, brand: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Get overview from SQLite database"""
        try:
            db_path = config['database']
            if not db_path.exists():
                return {'error': f'Database not found: {db_path}'}
            
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Get targets data
            cursor.execute("SELECT COUNT(*) FROM targets")
            total_targets = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM targets WHERE last_contacted IS NOT NULL")
            contacted_targets = cursor.fetchone()[0]
            
            # Get outreach data
            cursor.execute("SELECT COUNT(*) FROM outreach_log")
            total_outreach = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM outreach_log WHERE status = 'sent'")
            successful_outreach = cursor.fetchone()[0]
            
            # Get recent activity
            cursor.execute("""
                SELECT target_id, subject, status, created_at 
                FROM outreach_log 
                ORDER BY created_at DESC 
                LIMIT 10
            """)
            recent_activity = []
            for row in cursor.fetchall():
                recent_activity.append({
                    'target_id': row[0],
                    'subject': row[1], 
                    'status': row[2],
                    'timestamp': row[3]
                })
            
            # Get daily stats for last 7 days
            cursor.execute("""
                SELECT date, emails_sent, responses_received, new_targets_found
                FROM daily_stats 
                ORDER BY date DESC 
                LIMIT 7
            """)
            daily_stats = []
            for row in cursor.fetchall():
                daily_stats.append({
                    'date': row[0],
                    'emails_sent': row[1],
                    'responses_received': row[2],
                    'new_targets_found': row[3]
                })
            
            conn.close()
            
            # Calculate response rate
            response_rate = 0.0
            if contacted_targets > 0:
                cursor = sqlite3.connect(str(db_path)).cursor()
                cursor.execute("SELECT COUNT(*) FROM responses")
                responses = cursor.fetchone()[0]
                response_rate = round((responses / contacted_targets) * 100, 1)
                cursor.connection.close()
            
            return {
                'brand': brand,
                'data_source': 'sqlite',
                'database': str(db_path),
                'metrics': {
                    'total_targets': total_targets,
                    'contacted_targets': contacted_targets,
                    'total_outreach': total_outreach,
                    'successful_outreach': successful_outreach,
                    'response_rate': response_rate
                },
                'recent_activity': recent_activity,
                'daily_stats': daily_stats,
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': f'SQLite error: {e}'}
    
    def _get_json_overview(self, brand: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Get overview from JSON files"""
        try:
            base_path = config['base_path']
            
            overview = {
                'brand': brand,
                'data_source': 'json',
                'base_path': str(base_path),
                'metrics': {},
                'recent_activity': [],
                'daily_stats': [],
                'last_updated': datetime.now().isoformat()
            }
            
            # Read targets data
            targets_file = base_path / config['files'].get('targets', '')
            if targets_file.exists():
                with open(targets_file, 'r') as f:
                    targets = json.load(f)
                overview['metrics']['total_targets'] = len(targets) if isinstance(targets, list) else 0
            
            # Read outreach log
            outreach_file = base_path / config['files'].get('outreach_log', '')
            if outreach_file.exists():
                try:
                    with open(outreach_file, 'r') as f:
                        if str(outreach_file).endswith('.log'):
                            # Handle log file format
                            lines = f.readlines()
                            outreach_data = []
                            for line in lines:
                                if line.strip():
                                    try:
                                        outreach_data.append(json.loads(line.strip()))
                                    except:
                                        continue
                        else:
                            # Handle JSON file format
                            outreach_data = json.load(f)
                    
                    overview['metrics']['total_outreach'] = len(outreach_data)
                    
                    # Count successful outreach
                    successful = 0
                    contacted_targets = set()
                    
                    for entry in outreach_data[-20:]:  # Last 20 for recent activity
                        if entry.get('status') == 'sent' or 'sent' in str(entry).lower():
                            successful += 1
                        
                        if 'contact_email' in entry:
                            contacted_targets.add(entry['contact_email'])
                        
                        # Add to recent activity
                        if len(overview['recent_activity']) < 10:
                            overview['recent_activity'].append({
                                'timestamp': entry.get('timestamp', ''),
                                'subject': entry.get('subject', '')[:50],
                                'status': entry.get('status', 'unknown'),
                                'contact': entry.get('contact_name', entry.get('contact_email', ''))
                            })
                    
                    overview['metrics']['successful_outreach'] = successful
                    overview['metrics']['contacted_targets'] = len(contacted_targets)
                    
                    # Calculate response rate (simplified)
                    if len(contacted_targets) > 0:
                        overview['metrics']['response_rate'] = round((successful * 0.1), 1)  # Estimated
                    else:
                        overview['metrics']['response_rate'] = 0.0
                        
                except Exception as e:
                    self.logger.error(f"Error reading outreach log for {brand}: {e}")
            
            # Read analytics data
            analytics_file = base_path / config['files'].get('analytics', '')
            if analytics_file.exists():
                try:
                    with open(analytics_file, 'r') as f:
                        analytics = json.load(f)
                    if isinstance(analytics, dict):
                        overview['metrics'].update({
                            'total_analytics_entries': analytics.get('total_contacts', 0),
                            'failed_outreach': analytics.get('total_outreach_failed', 0)
                        })
                except Exception as e:
                    self.logger.error(f"Error reading analytics for {brand}: {e}")
            
            # Read daily reports
            daily_file = base_path / config['files'].get('daily_reports', '')
            if daily_file.exists():
                try:
                    with open(daily_file, 'r') as f:
                        daily_data = json.load(f)
                    if isinstance(daily_data, list):
                        for report in daily_data[-7:]:  # Last 7 days
                            overview['daily_stats'].append({
                                'date': report.get('date', ''),
                                'website_sessions': report.get('website_sessions', 0),
                                'emails_sent': report.get('emails_sent', 0),
                                'responses_received': report.get('responses_received', 0)
                            })
                except Exception as e:
                    self.logger.error(f"Error reading daily reports for {brand}: {e}")
            
            return overview
            
        except Exception as e:
            return {'error': f'JSON error: {e}'}
    
    def get_all_brands_overview(self) -> Dict[str, Any]:
        """Get overview for all brands from unified database"""
        try:
            # Use unified database as primary source
            # Find the unified database in the data directory
            project_root = Path(__file__).parent.parent
            unified_db = project_root / 'data' / 'unified_outreach.db'
            
            if not unified_db.exists():
                self.logger.info(f"Unified DB not found at {unified_db}, using legacy method")
                # Fall back to old method
                return self._get_all_brands_overview_legacy()
            
            try:
                conn = sqlite3.connect(str(unified_db), timeout=10)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
            except Exception as e:
                self.logger.error(f"Failed to open database {unified_db}: {e}")
                return self._get_all_brands_overview_legacy()
            
            overview = {
                'total_brands': 0,
                'brands': {},
                'combined_metrics': {
                    'total_targets': 0,
                    'contacted_targets': 0,
                    'total_outreach': 0,
                    'successful_outreach': 0
                },
                'recent_activity': [],
                'last_updated': datetime.now().isoformat()
            }
            
            # Get unique brands from unified_outreach_log
            cursor.execute("SELECT DISTINCT brand FROM unified_outreach_log ORDER BY brand")
            brands = [row[0] for row in cursor.fetchall()]
            overview['total_brands'] = len(brands)
            
            for brand in brands:
                # Get metrics for this brand
                cursor.execute("""
                    SELECT COUNT(*) FROM unified_targets WHERE brand = ?
                """, (brand,))
                total_targets = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT COUNT(DISTINCT target_id) FROM unified_outreach_log WHERE brand = ? AND status = 'sent'
                """, (brand,))
                contacted_targets = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT COUNT(*) FROM unified_outreach_log WHERE brand = ?
                """, (brand,))
                total_outreach = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT COUNT(*) FROM unified_outreach_log WHERE brand = ? AND status = 'sent'
                """, (brand,))
                successful_outreach = cursor.fetchone()[0]
                
                # Get recent activity for this brand
                cursor.execute("""
                    SELECT target_id, subject, status, delivery_time 
                    FROM unified_outreach_log 
                    WHERE brand = ?
                    ORDER BY delivery_time DESC 
                    LIMIT 5
                """, (brand,))
                
                recent_activity = []
                for row in cursor.fetchall():
                    recent_activity.append({
                        'target_id': row[0],
                        'subject': row[1],
                        'status': row[2],
                        'timestamp': row[3],
                        'brand': brand
                    })
                
                # Store brand overview
                overview['brands'][brand] = {
                    'brand': brand,
                    'metrics': {
                        'total_targets': total_targets,
                        'contacted_targets': contacted_targets,
                        'total_outreach': total_outreach,
                        'successful_outreach': successful_outreach,
                        'response_rate': 0.0
                    },
                    'recent_activity': recent_activity
                }
                
                # Aggregate combined metrics
                overview['combined_metrics']['total_targets'] += total_targets
                overview['combined_metrics']['contacted_targets'] += contacted_targets
                overview['combined_metrics']['total_outreach'] += total_outreach
                overview['combined_metrics']['successful_outreach'] += successful_outreach
                
                # Add to combined recent activity
                overview['recent_activity'].extend(recent_activity)
            
            # Sort and limit combined recent activity
            overview['recent_activity'] = sorted(
                overview['recent_activity'],
                key=lambda x: x.get('timestamp', ''),
                reverse=True
            )[:20]
            
            # Calculate combined response rate
            if overview['combined_metrics']['total_outreach'] > 0:
                success_rate = overview['combined_metrics']['successful_outreach'] / overview['combined_metrics']['total_outreach']
                overview['combined_metrics']['response_rate'] = round(success_rate * 100, 1)
            
            conn.close()
            return overview
            
        except Exception as e:
            self.logger.error(f"Error getting all brands overview from unified db: {e}")
            # Fall back to legacy method
            return self._get_all_brands_overview_legacy()
    
    def _get_all_brands_overview_legacy(self) -> Dict[str, Any]:
        """Get overview for all brands from unified database (fallback)"""
        try:
            # Fallback to simplified unified database query
            project_root = Path(__file__).parent.parent
            unified_db = project_root / 'data' / 'unified_outreach.db'
            
            if not unified_db.exists():
                return {'error': 'No data available', 'total_brands': 0, 'brands': {}, 'combined_metrics': {}}
            
            conn = sqlite3.connect(str(unified_db), timeout=10)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            overview = {
                'total_brands': 0,
                'brands': {},
                'combined_metrics': {
                    'total_targets': 0,
                    'contacted_targets': 0,
                    'total_outreach': 0,
                    'successful_outreach': 0
                },
                'recent_activity': [],
                'last_updated': datetime.now().isoformat()
            }
            
            # Get unique brands from unified_outreach_log
            cursor.execute("SELECT DISTINCT brand FROM unified_outreach_log ORDER BY brand")
            brands = [row[0] for row in cursor.fetchall()]
            overview['total_brands'] = len(brands)
            
            for brand in brands:
                # Get metrics for this brand
                cursor.execute("SELECT COUNT(*) FROM unified_targets WHERE brand = ?", (brand,))
                total_targets = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM unified_outreach_log WHERE brand = ?", (brand,))
                total_outreach = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM unified_outreach_log WHERE brand = ? AND status = 'sent'", (brand,))
                successful_outreach = cursor.fetchone()[0]
                
                # Get recent activity
                cursor.execute("""
                    SELECT target_id, subject, status, delivery_time 
                    FROM unified_outreach_log 
                    WHERE brand = ?
                    ORDER BY delivery_time DESC LIMIT 5
                """, (brand,))
                
                recent_activity = [
                    {'target_id': r[0], 'subject': r[1], 'status': r[2], 'timestamp': r[3]}
                    for r in cursor.fetchall()
                ]
                
                overview['brands'][brand] = {
                    'brand': brand,
                    'metrics': {
                        'total_targets': total_targets,
                        'contacted_targets': 0,
                        'total_outreach': total_outreach,
                        'successful_outreach': successful_outreach,
                        'response_rate': 0.0
                    },
                    'recent_activity': recent_activity
                }
                
                overview['combined_metrics']['total_targets'] += total_targets
                overview['combined_metrics']['total_outreach'] += total_outreach
                overview['combined_metrics']['successful_outreach'] += successful_outreach
                overview['recent_activity'].extend(recent_activity)
            
            # Sort recent activity
            overview['recent_activity'] = sorted(
                overview['recent_activity'],
                key=lambda x: x.get('timestamp', ''),
                reverse=True
            )[:20]
            
            # Calculate response rate
            if overview['combined_metrics']['total_outreach'] > 0:
                overview['combined_metrics']['response_rate'] = round(
                    (overview['combined_metrics']['successful_outreach'] / overview['combined_metrics']['total_outreach']) * 100, 1
                )
            
            conn.close()
            return overview
            
        except Exception as e:
            self.logger.error(f"Error in legacy method: {e}")
            return {'error': str(e), 'total_brands': 0, 'brands': {}, 'combined_metrics': {}}
    
    def get_cron_jobs_from_data(self) -> List[Dict[str, Any]]:
        """Extract cron job information from existing automation data"""
        try:
            cron_jobs = []
            
            # Check for automation logs and infer cron jobs
            for brand, config in self.brand_data_sources.items():
                if config['type'] == 'json':
                    base_path = config['base_path']
                    
                    # Look for daily reports to infer daily automation
                    daily_file = base_path / config['files'].get('daily_reports', '')
                    if daily_file.exists():
                        cron_jobs.append({
                            'brand': brand,
                            'name': f'{brand.title()} Daily Analytics',
                            'type': 'analytics_email',
                            'schedule': '0 8 * * *',  # 8 AM daily
                            'status': 'active',
                            'last_run': self._get_file_modified_date(daily_file),
                            'next_run': 'Tomorrow 8:00 AM'
                        })
                    
                    # Look for outreach logs to infer outreach automation
                    outreach_file = base_path / config['files'].get('outreach_log', '')
                    if outreach_file.exists():
                        cron_jobs.append({
                            'brand': brand,
                            'name': f'{brand.title()} Outreach Campaign',
                            'type': 'outreach',
                            'schedule': '0 10 * * 1-5',  # 10 AM weekdays
                            'status': 'active',
                            'last_run': self._get_file_modified_date(outreach_file),
                            'next_run': 'Next weekday 10:00 AM'
                        })
                
                elif config['type'] == 'sqlite':
                    db_path = config['database']
                    if db_path.exists():
                        cron_jobs.append({
                            'brand': brand,
                            'name': f'{brand.title()} Target Discovery',
                            'type': 'discovery',
                            'schedule': '0 9 * * *',  # 9 AM daily
                            'status': 'active',
                            'last_run': self._get_file_modified_date(db_path),
                            'next_run': 'Tomorrow 9:00 AM'
                        })
            
            return cron_jobs
            
        except Exception as e:
            self.logger.error(f"Error getting cron jobs from data: {e}")
            return []
    
    def _get_file_modified_date(self, file_path: Path) -> str:
        """Get file modification date as string"""
        try:
            if file_path.exists():
                mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                return mod_time.strftime('%Y-%m-%d %H:%M:%S')
            return 'Unknown'
        except:
            return 'Unknown'

def main():
    """Test the unified analytics system"""
    analytics = UnifiedOutreachAnalytics()
    
    print("=== Unified Outreach Analytics Test ===")
    
    # Load brands dynamically
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from config.brand_loader import get_all_brands
    brands = get_all_brands(active_only=True)
    
    # Test individual brand overviews
    for brand in brands:
        print(f"\n=== {brand.title()} Overview ===")
        overview = analytics.get_brand_overview(brand)
        
        if 'error' in overview:
            print(f"Error: {overview['error']}")
        else:
            metrics = overview.get('metrics', {})
            print(f"Targets: {metrics.get('total_targets', 0)}")
            print(f"Contacted: {metrics.get('contacted_targets', 0)}")
            print(f"Outreach: {metrics.get('total_outreach', 0)}")
            print(f"Response Rate: {metrics.get('response_rate', 0)}%")
            print(f"Recent Activity: {len(overview.get('recent_activity', []))}")
    
    # Test combined overview
    print("\n=== Combined Overview ===")
    combined = analytics.get_all_brands_overview()
    if 'error' not in combined:
        metrics = combined['combined_metrics']
        print(f"Total Brands: {combined['total_brands']}")
        print(f"Total Targets: {metrics['total_targets']}")
        print(f"Total Contacted: {metrics['contacted_targets']}")
        print(f"Total Outreach: {metrics['total_outreach']}")
        print(f"Overall Response Rate: {metrics['response_rate']}%")
    
    # Test cron jobs extraction
    print("\n=== Inferred Cron Jobs ===")
    cron_jobs = analytics.get_cron_jobs_from_data()
    for job in cron_jobs:
        print(f"{job['name']}: {job['schedule']} ({job['status']})")

if __name__ == "__main__":
    main()