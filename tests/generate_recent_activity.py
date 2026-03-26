#!/usr/bin/env python3
"""
Generate Recent Campaign Activity
=================================

Add some recent outreach activity to test the Recent Campaign Activity section
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
import random

def get_unified_db_path():
    """Get the unified database path"""
    project_root = Path(__file__).parent
    db_path = project_root / 'data' / 'unified_outreach.db'
    return db_path

def add_recent_outreach_activity():
    """Add some recent outreach activity for testing"""
    db_path = get_unified_db_path()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get some target IDs for each brand
        cursor.execute("""
            SELECT id, brand, name, email FROM unified_targets 
            WHERE brand IN ('buildly', 'radical', 'oregonsoftware')
            ORDER BY brand, id
        """)
        
        targets = cursor.fetchall()
        print(f"Found {len(targets)} targets to create activity for")
        
        activity_count = 0
        
        # Generate activity for the last few days
        for days_ago in range(5):  # Last 5 days
            activity_date = datetime.now() - timedelta(days=days_ago)
            
            # Pick some random targets for this day
            day_targets = random.sample(targets, min(3, len(targets)))
            
            for target_id, brand, name, email in day_targets:
                
                # Create outreach log entry
                subject_templates = [
                    f"Partnership Opportunity with {brand.title()}",
                    f"Collaboration Proposal - {brand.title()}",
                    f"Strategic Partnership Discussion",
                    f"Exploring Synergies with {brand.title()}",
                    f"Business Development Opportunity"
                ]
                
                subject = random.choice(subject_templates)
                
                # Simulate different delivery times throughout the day
                delivery_time = activity_date.replace(
                    hour=random.randint(9, 17),
                    minute=random.randint(0, 59),
                    second=random.randint(0, 59)
                )
                
                # Most are sent successfully, some might be pending
                status = random.choices(['sent', 'pending', 'failed'], weights=[85, 10, 5])[0]
                
                cursor.execute("""
                    INSERT INTO unified_outreach_log 
                    (brand, target_id, target_key, campaign_id, email_address, subject, 
                     status, delivery_time, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    brand,
                    target_id,
                    f"{name.lower().replace(' ', '_')}_{email.replace('@', '_at_').replace('.', '_')}",
                    f"{brand}_campaign_{activity_date.strftime('%Y%m%d')}",
                    email,
                    subject,
                    status,
                    delivery_time.isoformat(),
                    delivery_time.isoformat()
                ))
                
                # Update target's last_contacted if sent
                if status == 'sent':
                    cursor.execute("""
                        UPDATE unified_targets 
                        SET last_contacted = ?, contact_count = contact_count + 1
                        WHERE id = ?
                    """, (delivery_time.isoformat(), target_id))
                
                activity_count += 1
                print(f"   ✅ Added {status} activity: {brand} → {name}")
        
        conn.commit()
        conn.close()
        
        print(f"\n📊 Generated {activity_count} recent activities")
        return activity_count
        
    except Exception as e:
        print(f"❌ Error generating activity: {e}")
        return 0

def add_campaign_metrics():
    """Add some campaign metrics for recent days"""
    db_path = get_unified_db_path()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create metrics table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS unified_campaign_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                brand TEXT NOT NULL,
                metric_type TEXT NOT NULL,
                targets_added INTEGER DEFAULT 0,
                emails_sent INTEGER DEFAULT 0,
                responses_received INTEGER DEFAULT 0,
                bounce_rate REAL DEFAULT 0.0,
                open_rate REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(date, brand, metric_type)
            )
        """)
        
        brands = ['buildly', 'radical', 'oregonsoftware', 'foundry', 'openbuild']
        metrics_count = 0
        
        # Add daily stats for the last 7 days
        for days_ago in range(7):
            date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
            
            for brand in brands:
                # Simulate daily activity
                targets_added = random.randint(0, 3) if days_ago < 3 else 0  # More recent activity
                emails_sent = random.randint(1, 8) if days_ago < 5 else 0
                responses = random.randint(0, 2) if emails_sent > 0 else 0
                
                try:
                    cursor.execute("""
                        INSERT OR REPLACE INTO unified_campaign_metrics
                        (date, brand, metric_type, targets_added, emails_sent, responses_received)
                        VALUES (?, ?, 'daily_stats', ?, ?, ?)
                    """, (date, brand, targets_added, emails_sent, responses))
                    
                    metrics_count += 1
                    
                except sqlite3.IntegrityError:
                    # Already exists, skip
                    pass
        
        conn.commit()
        conn.close()
        
        print(f"📈 Added {metrics_count} daily metric entries")
        return metrics_count
        
    except Exception as e:
        print(f"❌ Error adding metrics: {e}")
        return 0

def main():
    """Generate recent campaign activity and metrics"""
    print("🚀 Generating Recent Campaign Activity")
    print("=" * 50)
    
    # Add recent outreach activity
    activity_count = add_recent_outreach_activity()
    
    # Add campaign metrics
    metrics_count = add_campaign_metrics()
    
    print("\n" + "=" * 50)
    print("✅ Activity Generation Complete!")
    print(f"📧 Generated {activity_count} outreach activities")
    print(f"📊 Added {metrics_count} daily metrics")
    print()
    print("🔗 View Results:")
    print("   Campaign Manager: http://127.0.0.1:5003/campaigns")
    print("   Analytics Dashboard: http://127.0.0.1:5003/analytics")
    print()
    print("🎉 Recent Campaign Activity should now be visible!")

if __name__ == "__main__":
    main()