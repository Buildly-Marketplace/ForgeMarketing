#!/usr/bin/env python3
"""
Real-Time Activity Tracker
Tracks all AI content generation, email sends, campaign activities, and dashboard usage
Provides persistent storage and real-time analytics for the marketing automation dashboard
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

class ActivityTracker:
    """
    Comprehensive activity tracking system for marketing automation
    Tracks AI generation, emails, campaigns, dashboard usage, and analytics
    """
    
    def __init__(self, db_path: str = None):
        """Initialize activity tracker with database connection"""
        self.db_path = db_path or str(Path(__file__).parent.parent / 'data' / 'activity_tracker.db')
        self.logger = self._setup_logging()
        self._initialize_database()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for activity tracker"""
        logger = logging.getLogger('ActivityTracker')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _initialize_database(self):
        """Initialize database tables for activity tracking"""
        # Ensure data directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # AI Content Generation Activity
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ai_activity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    brand TEXT NOT NULL,
                    content_type TEXT NOT NULL,  -- email, social, article, subject
                    template_used TEXT,
                    prompt_tokens INTEGER DEFAULT 0,
                    completion_tokens INTEGER DEFAULT 0,
                    generation_time_ms INTEGER DEFAULT 0,
                    quality_score REAL DEFAULT 0.0,
                    used_in_campaign BOOLEAN DEFAULT FALSE,
                    campaign_id TEXT,
                    success BOOLEAN DEFAULT TRUE,
                    error_message TEXT,
                    metadata TEXT  -- JSON for additional data
                )
            """)
            
            # Email Activity Tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS email_activity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    brand TEXT NOT NULL,
                    email_type TEXT NOT NULL,  -- outreach, analytics, test, campaign
                    campaign_id TEXT,
                    recipient_email TEXT,
                    subject TEXT,
                    template_used TEXT,
                    send_status TEXT DEFAULT 'pending',  -- pending, sent, delivered, failed, bounced
                    delivery_time TIMESTAMP,
                    opened BOOLEAN DEFAULT FALSE,
                    clicked BOOLEAN DEFAULT FALSE,
                    replied BOOLEAN DEFAULT FALSE,
                    unsubscribed BOOLEAN DEFAULT FALSE,
                    service_used TEXT,  -- brevo, mailersend, etc.
                    message_id TEXT,
                    error_message TEXT,
                    metadata TEXT  -- JSON for tracking data
                )
            """)
            
            # Campaign Activity
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS campaign_activity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    brand TEXT NOT NULL,
                    campaign_id TEXT NOT NULL,
                    campaign_name TEXT,
                    campaign_type TEXT,  -- outreach, analytics, social, ads
                    status TEXT DEFAULT 'created',  -- created, running, completed, failed, paused
                    total_targets INTEGER DEFAULT 0,
                    emails_sent INTEGER DEFAULT 0,
                    emails_delivered INTEGER DEFAULT 0,
                    responses_received INTEGER DEFAULT 0,
                    conversion_rate REAL DEFAULT 0.0,
                    budget_spent REAL DEFAULT 0.0,
                    roi REAL DEFAULT 0.0,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    metadata TEXT  -- JSON for campaign details
                )
            """)
            
            # Dashboard Usage Analytics
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS dashboard_activity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    page_visited TEXT,
                    action_taken TEXT,  -- view, create, edit, delete, export
                    brand_context TEXT,
                    user_agent TEXT,
                    ip_address TEXT,
                    session_duration INTEGER DEFAULT 0,  -- seconds
                    api_endpoint TEXT,
                    response_time_ms INTEGER DEFAULT 0,
                    success BOOLEAN DEFAULT TRUE,
                    error_message TEXT,
                    metadata TEXT  -- JSON for additional context
                )
            """)
            
            # System Performance Metrics
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metric_type TEXT NOT NULL,  -- daily_summary, hourly_stats, real_time
                    metric_name TEXT NOT NULL,
                    metric_value REAL,
                    metric_unit TEXT,  -- count, percentage, seconds, bytes
                    brand_context TEXT,
                    time_period TEXT,  -- 1h, 24h, 7d, 30d
                    metadata TEXT  -- JSON for additional data
                )
            """)
            
            # Create indexes for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_ai_brand_time ON ai_activity (brand, timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_email_brand_time ON email_activity (brand, timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_campaign_brand_time ON campaign_activity (brand, timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_dashboard_time ON dashboard_activity (timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_type_time ON system_metrics (metric_type, timestamp)")
            
            conn.commit()
            self.logger.info("✅ Activity tracking database initialized")
    
    # AI Activity Tracking
    def track_ai_generation(self, brand: str, content_type: str, template_used: str = None, 
                           prompt_tokens: int = 0, completion_tokens: int = 0, 
                           generation_time_ms: int = 0, quality_score: float = 0.0, 
                           success: bool = True, error_message: str = None, 
                           metadata: Dict = None) -> int:
        """Track AI content generation activity"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ai_activity 
                (brand, content_type, template_used, prompt_tokens, completion_tokens, 
                 generation_time_ms, quality_score, success, error_message, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                brand, content_type, template_used, prompt_tokens, completion_tokens,
                generation_time_ms, quality_score, success, error_message,
                json.dumps(metadata) if metadata else None
            ))
            activity_id = cursor.lastrowid
            conn.commit()
            
        self.logger.info(f"🤖 Tracked AI generation: {brand} - {content_type}")
        return activity_id
    
    def track_email_send(self, brand: str, email_type: str, recipient_email: str = None,
                        subject: str = None, template_used: str = None, 
                        campaign_id: str = None, service_used: str = None,
                        send_status: str = 'sent', message_id: str = None,
                        error_message: str = None, metadata: Dict = None) -> int:
        """Track email sending activity"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO email_activity 
                (brand, email_type, campaign_id, recipient_email, subject, template_used,
                 send_status, service_used, message_id, error_message, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                brand, email_type, campaign_id, recipient_email, subject, template_used,
                send_status, service_used, message_id, error_message,
                json.dumps(metadata) if metadata else None
            ))
            activity_id = cursor.lastrowid
            conn.commit()
            
        self.logger.info(f"📧 Tracked email send: {brand} - {email_type} to {recipient_email}")
        return activity_id
    
    def track_campaign_activity(self, brand: str, campaign_id: str, campaign_name: str = None,
                               campaign_type: str = None, status: str = 'created',
                               total_targets: int = 0, emails_sent: int = 0,
                               metadata: Dict = None) -> int:
        """Track campaign creation and updates"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check if campaign already exists
            cursor.execute("SELECT id FROM campaign_activity WHERE campaign_id = ?", (campaign_id,))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing campaign
                cursor.execute("""
                    UPDATE campaign_activity SET
                    status = ?, total_targets = ?, emails_sent = ?, 
                    metadata = ?, timestamp = CURRENT_TIMESTAMP
                    WHERE campaign_id = ?
                """, (status, total_targets, emails_sent, 
                     json.dumps(metadata) if metadata else None, campaign_id))
                activity_id = existing[0]
            else:
                # Create new campaign record
                cursor.execute("""
                    INSERT INTO campaign_activity 
                    (brand, campaign_id, campaign_name, campaign_type, status,
                     total_targets, emails_sent, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (brand, campaign_id, campaign_name, campaign_type, status,
                     total_targets, emails_sent, json.dumps(metadata) if metadata else None))
                activity_id = cursor.lastrowid
                
            conn.commit()
            
        self.logger.info(f"📊 Tracked campaign activity: {brand} - {campaign_id} ({status})")
        return activity_id
    
    def track_dashboard_usage(self, page_visited: str, action_taken: str = 'view',
                             brand_context: str = None, api_endpoint: str = None,
                             response_time_ms: int = 0, success: bool = True,
                             error_message: str = None, metadata: Dict = None) -> int:
        """Track dashboard usage and interactions"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO dashboard_activity 
                (page_visited, action_taken, brand_context, api_endpoint,
                 response_time_ms, success, error_message, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (page_visited, action_taken, brand_context, api_endpoint,
                 response_time_ms, success, error_message,
                 json.dumps(metadata) if metadata else None))
            activity_id = cursor.lastrowid
            conn.commit()
            
        return activity_id
    
    def update_system_metric(self, metric_type: str, metric_name: str, 
                            metric_value: float, metric_unit: str = 'count',
                            brand_context: str = None, time_period: str = '24h',
                            metadata: Dict = None):
        """Update system performance metrics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO system_metrics 
                (metric_type, metric_name, metric_value, metric_unit,
                 brand_context, time_period, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (metric_type, metric_name, metric_value, metric_unit,
                 brand_context, time_period, json.dumps(metadata) if metadata else None))
            conn.commit()
    
    # Analytics and Reporting Methods
    def get_real_time_dashboard_data(self, hours_back: int = 24) -> Dict[str, Any]:
        """Get real-time dashboard data for the specified time period"""
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # AI Generation Stats
            cursor.execute("""
                SELECT brand, COUNT(*) as generations, 
                       AVG(prompt_tokens + completion_tokens) as avg_tokens,
                       AVG(generation_time_ms) as avg_time_ms,
                       AVG(quality_score) as avg_quality,
                       SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_generations
                FROM ai_activity 
                WHERE timestamp >= ? 
                GROUP BY brand
            """, (cutoff_time,))
            
            ai_stats = {}
            for row in cursor.fetchall():
                brand, generations, avg_tokens, avg_time_ms, avg_quality, successful = row
                ai_stats[brand] = {
                    'total_generations': generations,
                    'avg_tokens': round(avg_tokens or 0, 2),
                    'avg_generation_time_ms': round(avg_time_ms or 0, 2),
                    'avg_quality_score': round(avg_quality or 0, 2),
                    'success_rate': round((successful / generations * 100) if generations > 0 else 0, 2)
                }
            
            # Email Activity Stats
            cursor.execute("""
                SELECT brand, email_type, COUNT(*) as count,
                       SUM(CASE WHEN send_status = 'delivered' THEN 1 ELSE 0 END) as delivered,
                       SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END) as opened,
                       SUM(CASE WHEN clicked = 1 THEN 1 ELSE 0 END) as clicked
                FROM email_activity 
                WHERE timestamp >= ? 
                GROUP BY brand, email_type
            """, (cutoff_time,))
            
            email_stats = {}
            for row in cursor.fetchall():
                brand, email_type, count, delivered, opened, clicked = row
                if brand not in email_stats:
                    email_stats[brand] = {}
                
                email_stats[brand][email_type] = {
                    'total_sent': count,
                    'delivered': delivered,
                    'opened': opened,
                    'clicked': clicked,
                    'delivery_rate': round((delivered / count * 100) if count > 0 else 0, 2),
                    'open_rate': round((opened / delivered * 100) if delivered > 0 else 0, 2),
                    'click_rate': round((clicked / delivered * 100) if delivered > 0 else 0, 2)
                }
            
            # Campaign Stats
            cursor.execute("""
                SELECT brand, COUNT(*) as campaigns,
                       SUM(emails_sent) as total_emails,
                       SUM(responses_received) as total_responses,
                       AVG(conversion_rate) as avg_conversion_rate
                FROM campaign_activity 
                WHERE timestamp >= ? 
                GROUP BY brand
            """, (cutoff_time,))
            
            campaign_stats = {}
            for row in cursor.fetchall():
                brand, campaigns, total_emails, total_responses, avg_conversion_rate = row
                campaign_stats[brand] = {
                    'active_campaigns': campaigns,
                    'total_emails_sent': total_emails or 0,
                    'total_responses': total_responses or 0,
                    'avg_conversion_rate': round(avg_conversion_rate or 0, 2),
                    'response_rate': round((total_responses / total_emails * 100) if total_emails > 0 else 0, 2)
                }
            
            # Dashboard Usage Stats
            cursor.execute("""
                SELECT COUNT(*) as page_views,
                       COUNT(DISTINCT page_visited) as unique_pages,
                       AVG(response_time_ms) as avg_response_time,
                       SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_requests
                FROM dashboard_activity 
                WHERE timestamp >= ?
            """, (cutoff_time,))
            
            dashboard_stats = cursor.fetchone()
            page_views, unique_pages, avg_response_time, successful_requests = dashboard_stats
            
            # Overall Summary
            summary = {
                'timestamp': datetime.now().isoformat(),
                'period_hours': hours_back,
                'ai_activity': ai_stats,
                'email_activity': email_stats,
                'campaign_activity': campaign_stats,
                'dashboard_performance': {
                    'total_page_views': page_views,
                    'unique_pages_visited': unique_pages,
                    'avg_response_time_ms': round(avg_response_time or 0, 2),
                    'success_rate': round((successful_requests / page_views * 100) if page_views > 0 else 0, 2)
                },
                'system_health': {
                    'database_path': self.db_path,
                    'data_collection_active': True,
                    'last_updated': datetime.now().isoformat()
                }
            }
            
        return summary
    
    def get_brand_activity_summary(self, brand: str, days_back: int = 30) -> Dict[str, Any]:
        """Get comprehensive activity summary for a specific brand"""
        cutoff_time = datetime.now() - timedelta(days=days_back)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # AI Generation Activity
            cursor.execute("""
                SELECT content_type, COUNT(*) as count,
                       AVG(quality_score) as avg_quality,
                       SUM(prompt_tokens + completion_tokens) as total_tokens
                FROM ai_activity 
                WHERE brand = ? AND timestamp >= ?
                GROUP BY content_type
            """, (brand, cutoff_time))
            
            ai_activity = {}
            for row in cursor.fetchall():
                content_type, count, avg_quality, total_tokens = row
                ai_activity[content_type] = {
                    'generations': count,
                    'avg_quality': round(avg_quality or 0, 2),
                    'total_tokens': total_tokens or 0
                }
            
            # Email Activity
            cursor.execute("""
                SELECT email_type, COUNT(*) as sent,
                       SUM(CASE WHEN send_status = 'delivered' THEN 1 ELSE 0 END) as delivered,
                       SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END) as opened
                FROM email_activity 
                WHERE brand = ? AND timestamp >= ?
                GROUP BY email_type
            """, (brand, cutoff_time))
            
            email_activity = {}
            for row in cursor.fetchall():
                email_type, sent, delivered, opened = row
                email_activity[email_type] = {
                    'sent': sent,
                    'delivered': delivered,
                    'opened': opened,
                    'open_rate': round((opened / delivered * 100) if delivered > 0 else 0, 2)
                }
            
            # Campaign Activity
            cursor.execute("""
                SELECT COUNT(*) as campaigns,
                       SUM(total_targets) as targets,
                       SUM(emails_sent) as emails,
                       SUM(responses_received) as responses
                FROM campaign_activity 
                WHERE brand = ? AND timestamp >= ?
            """, (brand, cutoff_time))
            
            campaign_data = cursor.fetchone()
            campaigns, targets, emails, responses = campaign_data
            
            return {
                'brand': brand,
                'period_days': days_back,
                'ai_activity': ai_activity,
                'email_activity': email_activity,
                'campaign_summary': {
                    'total_campaigns': campaigns or 0,
                    'total_targets': targets or 0,
                    'total_emails': emails or 0,
                    'total_responses': responses or 0,
                    'response_rate': round((responses / emails * 100) if emails > 0 else 0, 2)
                },
                'last_updated': datetime.now().isoformat()
            }


def main():
    """Test the activity tracker"""
    tracker = ActivityTracker()
    
    # Test tracking some activities
    print("🧪 Testing Activity Tracker...")
    
    # Track AI generation
    tracker.track_ai_generation(
        brand='foundry',
        content_type='email',
        template_used='outreach',
        prompt_tokens=150,
        completion_tokens=300,
        generation_time_ms=1200,
        quality_score=8.5,
        success=True,
        metadata={'campaign_id': 'test_campaign_001'}
    )
    
    # Track email send
    tracker.track_email_send(
        brand='foundry',
        email_type='outreach',
        recipient_email='test@example.com',
        subject='Test Outreach Email',
        template_used='general_outreach',
        campaign_id='test_campaign_001',
        service_used='brevo',
        send_status='delivered'
    )
    
    # Track campaign
    tracker.track_campaign_activity(
        brand='foundry',
        campaign_id='test_campaign_001',
        campaign_name='Test Campaign',
        campaign_type='outreach',
        status='running',
        total_targets=100,
        emails_sent=50
    )
    
    # Get real-time data
    dashboard_data = tracker.get_real_time_dashboard_data(24)
    print("\n📊 Real-time Dashboard Data:")
    print(json.dumps(dashboard_data, indent=2))
    
    # Get brand summary
    brand_summary = tracker.get_brand_activity_summary('foundry', 7)
    print(f"\n🏢 Brand Summary for Foundry:")
    print(json.dumps(brand_summary, indent=2))
    
    print("\n✅ Activity tracker test completed!")


if __name__ == "__main__":
    main()