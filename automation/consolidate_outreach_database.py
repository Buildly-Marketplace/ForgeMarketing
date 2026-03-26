#!/usr/bin/env python3
"""
Database Consolidation System
Consolidates all existing outreach data into a single unified database with brand-based keys
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Tuple
import logging

class OutreachDatabaseConsolidator:
    """Consolidates all existing outreach data into a unified database"""
    
    def __init__(self, unified_db_path: str = None, workspace_root: str = None):
        """Initialize consolidator with unified database path"""
        self.logger = logging.getLogger(__name__)
        # Use provided path, environment variable, or project root
        if workspace_root:
            self.workspace_root = Path(workspace_root)
        elif os.getenv('WORKSPACE_ROOT'):
            self.workspace_root = Path(os.getenv('WORKSPACE_ROOT'))
        else:
            self.workspace_root = Path(__file__).parent.parent
        
        default_db = self.workspace_root / 'data' / 'unified_outreach.db'
        self.unified_db_path = unified_db_path or os.getenv('UNIFIED_DB_PATH', str(default_db))
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.unified_db_path), exist_ok=True)
        
        # Load source configurations dynamically from database
        self.data_sources = self._load_data_sources()
    
    def _load_data_sources(self) -> Dict[str, Dict[str, Any]]:
        """Load brand data source configurations from database"""
        import sys
        sys.path.insert(0, str(self.workspace_root))
        
        from config.brand_loader import get_all_brands, get_brand_details
        
        sources = {}
        brands = get_all_brands(active_only=True)
        
        for brand in brands:
            brand_data = get_brand_details(brand)
            if brand_data:
                # Default source configuration
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
            },
            'oregonsoftware': {
                'type': 'inferred', 
                'base_path': self.workspace_root / 'oregonsoftware'
            }
        }
    
    def create_unified_schema(self):
        """Create the unified database schema with brand-based keys"""
        try:
            conn = sqlite3.connect(self.unified_db_path)
            cursor = conn.cursor()
            
            # Targets table - consolidated from all sources
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS unified_targets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand TEXT NOT NULL,
                    target_key TEXT NOT NULL,  -- brand + original_id or name
                    name TEXT NOT NULL,
                    company_name TEXT,
                    email TEXT,
                    website TEXT,
                    contact_name TEXT,
                    contact_role TEXT,
                    category TEXT,
                    focus_areas TEXT,  -- JSON array of focus areas
                    description TEXT,
                    priority INTEGER DEFAULT 3,
                    source TEXT,  -- where this target was discovered
                    notes TEXT,
                    last_contacted TIMESTAMP,
                    contact_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(brand, target_key)
                )
            """)
            
            # Outreach log table - all outreach activities
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS unified_outreach_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand TEXT NOT NULL,
                    target_id INTEGER,  -- references unified_targets.id
                    target_key TEXT,    -- backup reference
                    campaign_id TEXT,   -- campaign identifier
                    email_address TEXT,
                    subject TEXT,
                    message_template TEXT,
                    personalization_data TEXT,  -- JSON
                    status TEXT DEFAULT 'pending',  -- pending, sent, failed, bounced
                    response_received BOOLEAN DEFAULT FALSE,
                    response_type TEXT,  -- positive, negative, neutral, auto-reply
                    response_content TEXT,
                    sentiment_score REAL,
                    follow_up_needed BOOLEAN DEFAULT FALSE,
                    delivery_time TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (target_id) REFERENCES unified_targets (id)
                )
            """)
            
            # Discovery sessions - target finding activities
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS unified_discovery_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand TEXT NOT NULL,
                    session_key TEXT NOT NULL,  -- brand + date
                    discovery_date DATE NOT NULL,
                    search_terms TEXT,  -- JSON array
                    platforms_searched TEXT,  -- JSON array  
                    targets_found INTEGER DEFAULT 0,
                    discovery_method TEXT,  -- manual, automated, import
                    source_urls TEXT,  -- JSON array
                    success_rate REAL,  -- percentage of viable targets found
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(brand, session_key)
                )
            """)
            
            # Campaign metrics - performance tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS unified_campaign_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand TEXT NOT NULL,
                    metric_key TEXT NOT NULL,  -- brand + date + type
                    date DATE NOT NULL,
                    metric_type TEXT NOT NULL,  -- daily_stats, weekly_summary, campaign_performance
                    targets_added INTEGER DEFAULT 0,
                    emails_sent INTEGER DEFAULT 0,
                    emails_delivered INTEGER DEFAULT 0,
                    emails_failed INTEGER DEFAULT 0,
                    responses_received INTEGER DEFAULT 0,
                    positive_responses INTEGER DEFAULT 0,
                    meetings_scheduled INTEGER DEFAULT 0,
                    conversion_rate REAL DEFAULT 0.0,
                    website_visitors INTEGER DEFAULT 0,
                    website_pageviews INTEGER DEFAULT 0,
                    social_engagement INTEGER DEFAULT 0,
                    additional_data TEXT,  -- JSON for extra metrics
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(brand, metric_key)
                )
            """)
            
            # Response tracking - detailed response management
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS unified_responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand TEXT NOT NULL,
                    outreach_log_id INTEGER,
                    target_id INTEGER,
                    response_type TEXT NOT NULL,  -- email, form, call, meeting
                    response_status TEXT,  -- interested, not_interested, maybe, auto_reply
                    response_content TEXT,
                    sentiment_analysis TEXT,  -- JSON with sentiment data
                    action_items TEXT,  -- JSON array of follow-up actions
                    priority INTEGER DEFAULT 3,
                    follow_up_date DATE,
                    response_time_hours REAL,  -- hours from outreach to response
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (outreach_log_id) REFERENCES unified_outreach_log (id),
                    FOREIGN KEY (target_id) REFERENCES unified_targets (id)
                )
            """)
            
            # Create indexes for performance
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_targets_brand ON unified_targets (brand)",
                "CREATE INDEX IF NOT EXISTS idx_targets_email ON unified_targets (email)",
                "CREATE INDEX IF NOT EXISTS idx_targets_last_contacted ON unified_targets (last_contacted)",
                "CREATE INDEX IF NOT EXISTS idx_outreach_brand ON unified_outreach_log (brand)",
                "CREATE INDEX IF NOT EXISTS idx_outreach_status ON unified_outreach_log (status)",
                "CREATE INDEX IF NOT EXISTS idx_outreach_delivery ON unified_outreach_log (delivery_time)",
                "CREATE INDEX IF NOT EXISTS idx_discovery_brand_date ON unified_discovery_sessions (brand, discovery_date)",
                "CREATE INDEX IF NOT EXISTS idx_metrics_brand_date ON unified_campaign_metrics (brand, date)",
                "CREATE INDEX IF NOT EXISTS idx_responses_brand ON unified_responses (brand)"
            ]
            
            for index_sql in indexes:
                cursor.execute(index_sql)
            
            conn.commit()
            conn.close()
            
            print("✅ Unified database schema created successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating unified schema: {e}")
            return False
    
    def consolidate_all_data(self):
        """Consolidate all existing data into the unified database"""
        try:
            # Create the schema first
            if not self.create_unified_schema():
                return False
            
            conn = sqlite3.connect(self.unified_db_path)
            
            # Consolidate each brand's data
            for brand, config in self.data_sources.items():
                print(f"\n=== Consolidating {brand.upper()} data ===")
                
                if config['type'] == 'sqlite':
                    self._consolidate_sqlite_data(conn, brand, config)
                elif config['type'] == 'json':
                    self._consolidate_json_data(conn, brand, config)
                elif config['type'] == 'inferred':
                    self._create_placeholder_data(conn, brand, config)
            
            conn.commit()
            conn.close()
            
            print("✅ Data consolidation completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error consolidating data: {e}")
            return False
    
    def _consolidate_sqlite_data(self, conn: sqlite3.Connection, brand: str, config: Dict):
        """Consolidate data from SQLite database"""
        try:
            source_db = str(config['database'])
            if not os.path.exists(source_db):
                print(f"  ❌ Database not found: {source_db}")
                return
            
            source_conn = sqlite3.connect(source_db)
            cursor = conn.cursor()
            source_cursor = source_conn.cursor()
            
            # Migrate targets
            source_cursor.execute("SELECT * FROM targets")
            targets = source_cursor.fetchall()
            source_columns = [desc[0] for desc in source_cursor.description]
            
            for target in targets:
                target_dict = dict(zip(source_columns, target))
                
                cursor.execute("""
                    INSERT OR REPLACE INTO unified_targets 
                    (brand, target_key, name, company_name, email, website, contact_name, 
                     contact_role, category, description, priority, last_contacted, 
                     contact_count, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    brand,
                    f"{brand}_{target_dict.get('id', target_dict.get('name', 'unknown'))}",
                    target_dict.get('name', ''),
                    target_dict.get('name', ''),  # Use name as company for now
                    target_dict.get('email', ''),
                    target_dict.get('url', ''),
                    target_dict.get('contact_name', ''),
                    target_dict.get('contact_role', ''),
                    target_dict.get('category', ''),
                    target_dict.get('description', ''),
                    target_dict.get('priority', 3),
                    target_dict.get('last_contacted'),
                    target_dict.get('contact_count', 0),
                    target_dict.get('created_at'),
                    target_dict.get('updated_at')
                ))
            
            print(f"  ✅ Migrated {len(targets)} targets")
            
            # Migrate outreach log
            source_cursor.execute("SELECT * FROM outreach_log")
            outreach_logs = source_cursor.fetchall()
            outreach_columns = [desc[0] for desc in source_cursor.description]
            
            for log in outreach_logs:
                log_dict = dict(zip(outreach_columns, log))
                
                cursor.execute("""
                    INSERT OR REPLACE INTO unified_outreach_log 
                    (brand, target_id, email_address, subject, message_template, 
                     status, response_received, delivery_time, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    brand,
                    log_dict.get('target_id'),
                    log_dict.get('email_sent'),
                    log_dict.get('subject', ''),
                    log_dict.get('message_template', ''),
                    log_dict.get('status', 'sent'),
                    log_dict.get('response_received', False),
                    log_dict.get('created_at'),
                    log_dict.get('created_at')
                ))
            
            print(f"  ✅ Migrated {len(outreach_logs)} outreach records")
            
            # Migrate daily stats as campaign metrics
            source_cursor.execute("SELECT * FROM daily_stats")
            daily_stats = source_cursor.fetchall()
            stats_columns = [desc[0] for desc in source_cursor.description]
            
            for stat in daily_stats:
                stat_dict = dict(zip(stats_columns, stat))
                
                cursor.execute("""
                    INSERT OR REPLACE INTO unified_campaign_metrics
                    (brand, metric_key, date, metric_type, targets_added, emails_sent, 
                     responses_received, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    brand,
                    f"{brand}_{stat_dict.get('date')}_daily",
                    stat_dict.get('date'),
                    'daily_stats',
                    stat_dict.get('new_targets_found', 0),
                    stat_dict.get('emails_sent', 0),
                    stat_dict.get('responses_received', 0),
                    datetime.now().isoformat()
                ))
            
            print(f"  ✅ Migrated {len(daily_stats)} daily stats records")
            
            source_conn.close()
            
        except Exception as e:
            print(f"  ❌ Error consolidating SQLite data for {brand}: {e}")
    
    def _consolidate_json_data(self, conn: sqlite3.Connection, brand: str, config: Dict):
        """Consolidate data from JSON files"""
        try:
            base_path = config['base_path']
            cursor = conn.cursor()
            
            # Process targets file
            targets_file = base_path / config['files'].get('targets', '')
            if targets_file.exists():
                with open(targets_file, 'r') as f:
                    targets_data = json.load(f)
                
                if isinstance(targets_data, list):
                    for idx, target in enumerate(targets_data):
                        cursor.execute("""
                            INSERT OR REPLACE INTO unified_targets 
                            (brand, target_key, name, company_name, email, website, 
                             category, description, created_at, updated_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            brand,
                            f"{brand}_{idx}_{target.get('name', 'unknown')}",
                            target.get('name', ''),
                            target.get('name', ''),
                            target.get('email', ''),
                            target.get('website', target.get('url', '')),
                            target.get('category', ''),
                            json.dumps(target.get('focus_areas', [])),
                            datetime.now().isoformat(),
                            datetime.now().isoformat()
                        ))
                
                print(f"  ✅ Migrated {len(targets_data)} targets from JSON")
            
            # Process outreach log
            outreach_file = base_path / config['files'].get('outreach_log', '')
            if outreach_file.exists():
                outreach_data = []
                
                if str(outreach_file).endswith('.log'):
                    # Handle log file format
                    with open(outreach_file, 'r') as f:
                        for line in f:
                            if line.strip():
                                try:
                                    outreach_data.append(json.loads(line.strip()))
                                except:
                                    continue
                else:
                    # Handle JSON file format
                    with open(outreach_file, 'r') as f:
                        outreach_data = json.load(f)
                
                for log_entry in outreach_data:
                    cursor.execute("""
                        INSERT OR REPLACE INTO unified_outreach_log 
                        (brand, email_address, subject, status, delivery_time, created_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        brand,
                        log_entry.get('contact_email', ''),
                        log_entry.get('subject', ''),
                        'sent' if 'sent' in str(log_entry).lower() else 'unknown',
                        log_entry.get('timestamp'),
                        log_entry.get('timestamp', datetime.now().isoformat())
                    ))
                
                print(f"  ✅ Migrated {len(outreach_data)} outreach records from JSON")
            
            # Process daily reports as metrics
            daily_file = base_path / config['files'].get('daily_reports', '')
            if daily_file.exists():
                with open(daily_file, 'r') as f:
                    daily_data = json.load(f)
                
                if isinstance(daily_data, list):
                    for report in daily_data:
                        cursor.execute("""
                            INSERT OR REPLACE INTO unified_campaign_metrics
                            (brand, metric_key, date, metric_type, website_visitors, 
                             website_pageviews, emails_sent, created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            brand,
                            f"{brand}_{report.get('date')}_daily",
                            report.get('date'),
                            'daily_stats',
                            report.get('website_sessions', 0),
                            report.get('website_pageviews', 0),
                            report.get('emails_sent', 0),
                            datetime.now().isoformat()
                        ))
                
                print(f"  ✅ Migrated {len(daily_data)} daily reports from JSON")
            
        except Exception as e:
            print(f"  ❌ Error consolidating JSON data for {brand}: {e}")
    
    def _create_placeholder_data(self, conn: sqlite3.Connection, brand: str, config: Dict):
        """Create placeholder data for brands without existing data"""
        try:
            cursor = conn.cursor()
            
            # Create a discovery session entry
            cursor.execute("""
                INSERT OR REPLACE INTO unified_discovery_sessions
                (brand, session_key, discovery_date, discovery_method, targets_found, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                brand,
                f"{brand}_{datetime.now().strftime('%Y-%m-%d')}_placeholder",
                datetime.now().strftime('%Y-%m-%d'),
                'placeholder',
                0,
                f"Placeholder entry for {brand} - ready for data collection"
            ))
            
            print(f"  ✅ Created placeholder entry for {brand}")
            
        except Exception as e:
            print(f"  ❌ Error creating placeholder for {brand}: {e}")
    
    def get_consolidation_summary(self) -> Dict[str, Any]:
        """Get summary of consolidated data"""
        try:
            conn = sqlite3.connect(self.unified_db_path)
            cursor = conn.cursor()
            
            # Get counts by brand
            cursor.execute("""
                SELECT brand, COUNT(*) as target_count 
                FROM unified_targets 
                GROUP BY brand
            """)
            target_counts = dict(cursor.fetchall())
            
            cursor.execute("""
                SELECT brand, COUNT(*) as outreach_count 
                FROM unified_outreach_log 
                GROUP BY brand
            """)
            outreach_counts = dict(cursor.fetchall())
            
            cursor.execute("""
                SELECT brand, COUNT(*) as metrics_count 
                FROM unified_campaign_metrics 
                GROUP BY brand
            """)
            metrics_counts = dict(cursor.fetchall())
            
            cursor.execute("SELECT COUNT(*) FROM unified_targets")
            total_targets = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM unified_outreach_log")
            total_outreach = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'database_path': self.unified_db_path,
                'total_targets': total_targets,
                'total_outreach_records': total_outreach,
                'brands': {
                    brand: {
                        'targets': target_counts.get(brand, 0),
                        'outreach_records': outreach_counts.get(brand, 0),
                        'metrics_records': metrics_counts.get(brand, 0)
                    }
                    for brand in self.data_sources.keys()
                },
                'consolidated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': str(e)}

def main():
    """Test the consolidation system"""
    print("=== Outreach Database Consolidation ===")
    
    consolidator = OutreachDatabaseConsolidator()
    
    # Perform consolidation
    success = consolidator.consolidate_all_data()
    
    if success:
        # Get summary
        summary = consolidator.get_consolidation_summary()
        
        if 'error' not in summary:
            print(f"\n=== Consolidation Summary ===")
            print(f"Database: {summary['database_path']}")
            print(f"Total Targets: {summary['total_targets']}")
            print(f"Total Outreach Records: {summary['total_outreach_records']}")
            print(f"Consolidated at: {summary['consolidated_at']}")
            
            print(f"\n=== Per Brand Summary ===")
            for brand, data in summary['brands'].items():
                print(f"{brand.title()}: {data['targets']} targets, {data['outreach_records']} outreach, {data['metrics_records']} metrics")
        else:
            print(f"Error getting summary: {summary['error']}")
    else:
        print("❌ Consolidation failed")

if __name__ == "__main__":
    main()