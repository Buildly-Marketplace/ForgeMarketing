#!/usr/bin/env python3
"""
Campaign Report Generator
=========================

Generate comprehensive reports for campaign executions with metrics,
target details, performance analysis, and visual summaries.
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import uuid
import os

class CampaignReportGenerator:
    """Generate detailed reports for marketing campaigns"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.db_path = self.project_root / 'data' / 'unified_outreach.db'
        self.reports_dir = self.project_root / 'data' / 'reports'
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_campaign_report(self, campaign_id: str, brand: str) -> Dict[str, Any]:
        """Generate a comprehensive campaign report"""
        try:
            report_data = {
                'report_id': str(uuid.uuid4()),
                'campaign_id': campaign_id,
                'brand': brand,
                'generated_at': datetime.now().isoformat(),
                'summary': {},
                'targets': [],
                'performance': {},
                'timeline': [],
                'recommendations': []
            }
            
            # Get campaign summary
            report_data['summary'] = self._get_campaign_summary(campaign_id, brand)
            
            # Get target details
            report_data['targets'] = self._get_campaign_targets(campaign_id, brand)
            
            # Calculate performance metrics
            report_data['performance'] = self._calculate_performance_metrics(campaign_id, brand)
            
            # Get campaign timeline
            report_data['timeline'] = self._get_campaign_timeline(campaign_id, brand)
            
            # Generate recommendations
            report_data['recommendations'] = self._generate_recommendations(report_data)
            
            # Save report to file
            report_file = self.reports_dir / f"{report_data['report_id']}.json"
            with open(report_file, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            print(f"✅ Generated report: {report_data['report_id']}")
            return report_data
            
        except Exception as e:
            print(f"❌ Error generating campaign report: {e}")
            return {'error': str(e)}
    
    def _get_campaign_summary(self, campaign_id: str, brand: str) -> Dict[str, Any]:
        """Get basic campaign summary metrics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get campaign overview
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_emails,
                    COUNT(CASE WHEN status = 'sent' THEN 1 END) as sent_emails,
                    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_emails,
                    COUNT(CASE WHEN response_received = 1 THEN 1 END) as responses,
                    MIN(created_at) as start_time,
                    MAX(delivery_time) as end_time
                FROM unified_outreach_log
                WHERE campaign_id = ? OR (brand = ? AND DATE(created_at) = DATE('now'))
            """, (campaign_id, brand))
            
            row = cursor.fetchone()
            if row:
                total, sent, failed, responses, start_time, end_time = row
                
                # Calculate success rate
                success_rate = (sent / total * 100) if total > 0 else 0
                response_rate = (responses / sent * 100) if sent > 0 else 0
                
                return {
                    'total_emails': total or 0,
                    'sent_emails': sent or 0,
                    'failed_emails': failed or 0,
                    'pending_emails': (total or 0) - (sent or 0) - (failed or 0),
                    'responses_received': responses or 0,
                    'success_rate': round(success_rate, 1),
                    'response_rate': round(response_rate, 1),
                    'start_time': start_time,
                    'end_time': end_time,
                    'duration': self._calculate_duration(start_time, end_time)
                }
            
            conn.close()
            return {}
            
        except Exception as e:
            return {'error': str(e)}
    
    def _get_campaign_targets(self, campaign_id: str, brand: str) -> List[Dict[str, Any]]:
        """Get detailed information about campaign targets"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get targets from outreach log
            cursor.execute("""
                SELECT DISTINCT
                    o.email_address,
                    o.subject,
                    o.status,
                    o.delivery_time,
                    o.response_received,
                    t.name,
                    t.category,
                    t.website,
                    t.description,
                    t.contact_count
                FROM unified_outreach_log o
                LEFT JOIN unified_targets t ON o.target_key = t.target_key
                WHERE o.campaign_id = ? OR (o.brand = ? AND DATE(o.created_at) = DATE('now'))
                ORDER BY o.delivery_time DESC
            """, (campaign_id, brand))
            
            targets = []
            for row in cursor.fetchall():
                email, subject, status, delivery_time, response_received, name, category, website, description, contact_count = row
                
                targets.append({
                    'name': name or 'Unknown Target',
                    'email': email,
                    'category': category or 'Unknown',
                    'website': website or '',
                    'description': description or '',
                    'subject': subject,
                    'status': status,
                    'delivery_time': delivery_time,
                    'response_received': bool(response_received),
                    'total_contacts': contact_count or 0
                })
            
            conn.close()
            return targets
            
        except Exception as e:
            return [{'error': str(e)}]
    
    def _calculate_performance_metrics(self, campaign_id: str, brand: str) -> Dict[str, Any]:
        """Calculate detailed performance metrics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get performance data
            cursor.execute("""
                SELECT 
                    status,
                    COUNT(*) as count,
                    AVG(CASE WHEN delivery_time IS NOT NULL THEN 1.0 ELSE 0.0 END) as delivery_rate
                FROM unified_outreach_log
                WHERE campaign_id = ? OR (brand = ? AND DATE(created_at) = DATE('now'))
                GROUP BY status
            """, (campaign_id, brand))
            
            status_breakdown = {}
            for row in cursor.fetchall():
                status, count, delivery_rate = row
                status_breakdown[status] = {
                    'count': count,
                    'delivery_rate': round((delivery_rate or 0) * 100, 1)
                }
            
            # Get category performance
            cursor.execute("""
                SELECT 
                    t.category,
                    COUNT(*) as total,
                    COUNT(CASE WHEN o.status = 'sent' THEN 1 END) as sent,
                    COUNT(CASE WHEN o.response_received = 1 THEN 1 END) as responses
                FROM unified_outreach_log o
                LEFT JOIN unified_targets t ON o.target_key = t.target_key
                WHERE o.campaign_id = ? OR (o.brand = ? AND DATE(o.created_at) = DATE('now'))
                GROUP BY t.category
            """, (campaign_id, brand))
            
            category_performance = {}
            for row in cursor.fetchall():
                category, total, sent, responses = row
                category = category or 'Unknown'
                
                category_performance[category] = {
                    'total_contacted': total,
                    'successfully_sent': sent,
                    'responses_received': responses,
                    'response_rate': round((responses / sent * 100) if sent > 0 else 0, 1)
                }
            
            conn.close()
            
            return {
                'status_breakdown': status_breakdown,
                'category_performance': category_performance,
                'top_performing_categories': self._get_top_categories(category_performance),
                'engagement_score': self._calculate_engagement_score(status_breakdown, category_performance)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _get_campaign_timeline(self, campaign_id: str, brand: str) -> List[Dict[str, Any]]:
        """Get chronological timeline of campaign events"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    delivery_time,
                    email_address,
                    subject,
                    status,
                    response_received
                FROM unified_outreach_log
                WHERE campaign_id = ? OR (brand = ? AND DATE(created_at) = DATE('now'))
                ORDER BY delivery_time ASC
            """, (campaign_id, brand))
            
            timeline = []
            for row in cursor.fetchall():
                delivery_time, email, subject, status, response_received = row
                
                timeline.append({
                    'timestamp': delivery_time,
                    'event_type': 'response' if response_received else 'outreach',
                    'target_email': email,
                    'subject': subject,
                    'status': status,
                    'description': self._format_timeline_event(email, subject, status, response_received)
                })
            
            conn.close()
            return timeline
            
        except Exception as e:
            return [{'error': str(e)}]
    
    def _generate_recommendations(self, report_data: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on campaign performance"""
        recommendations = []
        
        try:
            performance = report_data.get('performance', {})
            summary = report_data.get('summary', {})
            
            # Response rate recommendations
            response_rate = summary.get('response_rate', 0)
            if response_rate < 2:
                recommendations.append("Consider personalizing email content more - response rate below industry average (2-5%)")
            elif response_rate > 10:
                recommendations.append("Excellent response rate! Consider scaling this campaign approach to other brands")
            
            # Success rate recommendations
            success_rate = summary.get('success_rate', 0)
            if success_rate < 90:
                recommendations.append("Investigate email deliverability issues - success rate below optimal (95%+)")
            
            # Category performance recommendations
            category_perf = performance.get('category_performance', {})
            if category_perf:
                top_category = max(category_perf.keys(), 
                                 key=lambda x: category_perf[x].get('response_rate', 0))
                recommendations.append(f"Focus more outreach on '{top_category}' targets - highest response rate")
            
            # Volume recommendations
            total_emails = summary.get('total_emails', 0)
            if total_emails < 5:
                recommendations.append("Consider increasing campaign volume for better statistical significance")
            elif total_emails > 50:
                recommendations.append("Large campaign detected - monitor for spam complaints and deliverability")
            
            # Timing recommendations
            if len(report_data.get('timeline', [])) > 0:
                recommendations.append("Analyze optimal send times based on response patterns")
            
        except Exception as e:
            recommendations.append(f"Unable to generate recommendations: {e}")
        
        return recommendations
    
    def _calculate_duration(self, start_time: str, end_time: str) -> str:
        """Calculate campaign duration"""
        try:
            if not start_time or not end_time:
                return "Unknown"
            
            start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            end = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            
            duration = end - start
            
            if duration.seconds < 60:
                return f"{duration.seconds} seconds"
            elif duration.seconds < 3600:
                return f"{duration.seconds // 60} minutes"
            else:
                return f"{duration.seconds // 3600} hours {(duration.seconds % 3600) // 60} minutes"
                
        except Exception:
            return "Unknown"
    
    def _get_top_categories(self, category_performance: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get top performing target categories"""
        try:
            categories = []
            for category, metrics in category_performance.items():
                categories.append({
                    'category': category,
                    'response_rate': metrics.get('response_rate', 0),
                    'total_contacted': metrics.get('total_contacted', 0)
                })
            
            return sorted(categories, key=lambda x: x['response_rate'], reverse=True)[:3]
            
        except Exception:
            return []
    
    def _calculate_engagement_score(self, status_breakdown: Dict[str, Any], 
                                  category_performance: Dict[str, Any]) -> float:
        """Calculate overall campaign engagement score (0-100)"""
        try:
            score = 0.0
            
            # Base score from successful delivery
            sent_count = status_breakdown.get('sent', {}).get('count', 0)
            total_count = sum(data.get('count', 0) for data in status_breakdown.values())
            
            if total_count > 0:
                score += (sent_count / total_count) * 60  # Up to 60 points for delivery
            
            # Additional score from responses
            total_responses = sum(cat.get('responses_received', 0) 
                                for cat in category_performance.values())
            if sent_count > 0:
                response_rate = total_responses / sent_count
                score += response_rate * 40  # Up to 40 points for engagement
            
            return round(min(score, 100), 1)
            
        except Exception:
            return 0.0
    
    def _format_timeline_event(self, email: str, subject: str, status: str, 
                             response_received: bool) -> str:
        """Format timeline event description"""
        if response_received:
            return f"Response received from {email}"
        else:
            return f"Email {status} to {email}: '{subject}'"
    
    def get_report(self, report_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a generated report"""
        try:
            report_file = self.reports_dir / f"{report_id}.json"
            if report_file.exists():
                with open(report_file, 'r') as f:
                    return json.load(f)
            return None
            
        except Exception as e:
            return {'error': str(e)}
    
    def list_reports(self, brand: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """List available reports with summaries"""
        try:
            reports = []
            
            for report_file in self.reports_dir.glob("*.json"):
                try:
                    with open(report_file, 'r') as f:
                        report_data = json.load(f)
                    
                    # Filter by brand if specified
                    if brand and report_data.get('brand') != brand:
                        continue
                    
                    reports.append({
                        'report_id': report_data.get('report_id'),
                        'brand': report_data.get('brand'),
                        'campaign_id': report_data.get('campaign_id'),
                        'generated_at': report_data.get('generated_at'),
                        'summary': {
                            'total_emails': report_data.get('summary', {}).get('total_emails', 0),
                            'response_rate': report_data.get('summary', {}).get('response_rate', 0),
                            'success_rate': report_data.get('summary', {}).get('success_rate', 0)
                        }
                    })
                    
                except Exception:
                    continue
            
            # Sort by generation date (newest first)
            reports.sort(key=lambda x: x.get('generated_at', ''), reverse=True)
            return reports[:limit]
            
        except Exception as e:
            return [{'error': str(e)}]

def main():
    """Test the campaign report generator"""
    print("📊 Testing Campaign Report Generator")
    print("=" * 50)
    
    generator = CampaignReportGenerator()
    
    # Generate a test report for a recent buildly campaign
    report = generator.generate_campaign_report(
        campaign_id="buildly_campaign_20251013",
        brand="buildly"
    )
    
    if 'error' not in report:
        print(f"✅ Generated report: {report['report_id']}")
        print(f"📧 Total emails: {report['summary'].get('total_emails', 0)}")
        print(f"📈 Response rate: {report['summary'].get('response_rate', 0)}%")
        print(f"🎯 Engagement score: {report['performance'].get('engagement_score', 0)}")
    else:
        print(f"❌ Error: {report['error']}")

if __name__ == "__main__":
    main()