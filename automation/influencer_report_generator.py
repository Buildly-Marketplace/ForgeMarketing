#!/usr/bin/env python3
"""
Influencer Report Generator
==========================

Generates comprehensive, filterable reports for social media influencers
across all brands and platforms with outreach recommendations.

Features:
- Multi-brand filtered reporting
- Platform-specific insights
- Engagement analytics
- Outreach prioritization
- Export capabilities (HTML, JSON, CSV)
- Contact information compilation
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from automation.influencer_discovery import BRAND_INFLUENCER_STRATEGIES

class InfluencerReportGenerator:
    """Generate comprehensive influencer reports"""
    
    def __init__(self, db_path: str = "data/influencer_discovery.db"):
        self.db_path = Path(project_root) / db_path
        self.report_dir = Path(project_root) / "reports" / "influencers"
        self.report_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_brand_report(self, brand: str = None, format: str = "html") -> Dict[str, Any]:
        """Generate comprehensive brand influencer report"""
        
        # Get influencer data
        influencers = self._get_filtered_influencers(brand=brand)
        
        # Generate analytics
        analytics = self._calculate_analytics(influencers, brand)
        
        # Create report data
        report_data = {
            'report_id': f"influencer_report_{brand or 'all'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'brand': brand,
            'brand_name': BRAND_INFLUENCER_STRATEGIES.get(brand, {}).get('name', brand) if brand else 'All Brands',
            'generated_at': datetime.now().isoformat(),
            'summary': analytics,
            'influencers': influencers,
            'platform_breakdown': self._get_platform_breakdown(influencers),
            'outreach_recommendations': self._generate_outreach_recommendations(influencers),
            'top_performers': self._get_top_performers(influencers)
        }
        
        # Generate report file
        if format == "html":
            report_file = self._generate_html_report(report_data)
        elif format == "json":
            report_file = self._generate_json_report(report_data)
        elif format == "csv":
            report_file = self._generate_csv_report(report_data)
        else:
            report_file = self._generate_html_report(report_data)
        
        report_data['report_file'] = str(report_file)
        report_data['report_url'] = f"/reports/influencers/{report_file.name}"
        
        return report_data
    
    def _get_filtered_influencers(self, brand: str = None, platform: str = None, 
                                min_followers: int = 0, min_alignment: float = 0.0) -> List[Dict]:
        """Get filtered influencer data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main query with social profiles joined
        query = """
            SELECT 
                i.id, i.name, i.primary_platform, i.niche, i.brand,
                i.brand_alignment_score, i.total_reach, i.avg_engagement_rate,
                i.contact_email, i.website, i.location, i.bio_summary,
                i.content_themes, i.outreach_notes, i.discovery_date,
                i.contacted, i.response_received,
                sp.platform as social_platform,
                sp.username, sp.display_name, sp.profile_url,
                sp.verified, sp.followers, sp.following, sp.posts_count,
                sp.engagement_rate as platform_engagement, sp.bio
            FROM influencers i
            LEFT JOIN social_profiles sp ON i.id = sp.influencer_id
            WHERE 1=1
        """
        params = []
        
        if brand:
            query += " AND i.brand = ?"
            params.append(brand)
        
        if platform:
            query += " AND i.primary_platform = ?"
            params.append(platform)
        
        if min_followers > 0:
            query += " AND i.total_reach >= ?"
            params.append(min_followers)
        
        if min_alignment > 0.0:
            query += " AND i.brand_alignment_score >= ?"
            params.append(min_alignment)
        
        query += " ORDER BY i.brand_alignment_score DESC, i.total_reach DESC"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        # Group by influencer ID to combine social profiles
        influencers_dict = {}
        
        for row in results:
            influencer_id = row[0]
            
            if influencer_id not in influencers_dict:
                influencers_dict[influencer_id] = {
                    'id': row[0],
                    'name': row[1],
                    'primary_platform': row[2],
                    'niche': row[3],
                    'brand': row[4],
                    'brand_alignment_score': row[5],
                    'total_reach': row[6],
                    'avg_engagement_rate': row[7],
                    'contact_email': row[8],
                    'website': row[9],
                    'location': row[10],
                    'bio_summary': row[11],
                    'content_themes': json.loads(row[12]) if row[12] else [],
                    'outreach_notes': row[13],
                    'discovery_date': row[14],
                    'contacted': bool(row[15]),
                    'response_received': bool(row[16]),
                    'social_profiles': {}
                }
            
            # Add social profile if it exists
            if row[17]:  # social_platform
                influencers_dict[influencer_id]['social_profiles'][row[17]] = {
                    'platform': row[17],
                    'username': row[18],
                    'display_name': row[19],
                    'profile_url': row[20],
                    'verified': bool(row[21]),
                    'followers': row[22],
                    'following': row[23],
                    'posts_count': row[24],
                    'engagement_rate': row[25],
                    'bio': row[26]
                }
        
        conn.close()
        return list(influencers_dict.values())
    
    def _calculate_analytics(self, influencers: List[Dict], brand: str = None) -> Dict[str, Any]:
        """Calculate summary analytics"""
        if not influencers:
            return {
                'total_influencers': 0,
                'total_reach': 0,
                'avg_engagement': 0.0,
                'avg_alignment': 0.0,
                'platforms_covered': 0,
                'contact_rate': 0.0,
                'response_rate': 0.0
            }
        
        total_reach = sum(inf['total_reach'] for inf in influencers)
        avg_engagement = sum(inf['avg_engagement_rate'] for inf in influencers) / len(influencers)
        avg_alignment = sum(inf['brand_alignment_score'] for inf in influencers) / len(influencers)
        
        platforms = set(inf['primary_platform'] for inf in influencers)
        
        contacted_count = sum(1 for inf in influencers if inf['contacted'])
        response_count = sum(1 for inf in influencers if inf['response_received'])
        
        contact_rate = (contacted_count / len(influencers)) * 100 if influencers else 0
        response_rate = (response_count / contacted_count) * 100 if contacted_count > 0 else 0
        
        return {
            'total_influencers': len(influencers),
            'total_reach': total_reach,
            'avg_engagement': round(avg_engagement, 2),
            'avg_alignment': round(avg_alignment, 2),
            'platforms_covered': len(platforms),
            'contact_rate': round(contact_rate, 1),
            'response_rate': round(response_rate, 1),
            'top_platform': max(platforms, key=lambda p: len([inf for inf in influencers if inf['primary_platform'] == p])) if platforms else None
        }
    
    def _get_platform_breakdown(self, influencers: List[Dict]) -> List[Dict]:
        """Get platform-wise breakdown"""
        platforms = {}
        
        for influencer in influencers:
            platform = influencer['primary_platform']
            if platform not in platforms:
                platforms[platform] = {
                    'platform': platform,
                    'count': 0,
                    'total_reach': 0,
                    'avg_engagement': 0,
                    'avg_alignment': 0,
                    'top_influencer': None
                }
            
            platforms[platform]['count'] += 1
            platforms[platform]['total_reach'] += influencer['total_reach']
            
            # Update top influencer for platform
            if (platforms[platform]['top_influencer'] is None or 
                influencer['total_reach'] > platforms[platform]['top_influencer']['total_reach']):
                platforms[platform]['top_influencer'] = influencer
        
        # Calculate averages
        for platform_data in platforms.values():
            platform_influencers = [inf for inf in influencers if inf['primary_platform'] == platform_data['platform']]
            platform_data['avg_engagement'] = round(
                sum(inf['avg_engagement_rate'] for inf in platform_influencers) / len(platform_influencers), 2
            )
            platform_data['avg_alignment'] = round(
                sum(inf['brand_alignment_score'] for inf in platform_influencers) / len(platform_influencers), 2
            )
        
        return sorted(platforms.values(), key=lambda x: x['total_reach'], reverse=True)
    
    def _generate_outreach_recommendations(self, influencers: List[Dict]) -> List[Dict]:
        """Generate prioritized outreach recommendations"""
        recommendations = []
        
        # Filter non-contacted influencers and sort by priority
        non_contacted = [inf for inf in influencers if not inf['contacted']]
        
        # Priority scoring: alignment * 0.4 + (reach/1000000) * 0.3 + engagement * 0.3
        for influencer in non_contacted:
            reach_score = min(influencer['total_reach'] / 1000000, 1.0)  # Normalize to 1M followers
            priority_score = (
                influencer['brand_alignment_score'] * 0.4 +
                reach_score * 0.3 +
                (influencer['avg_engagement_rate'] / 10.0) * 0.3
            )
            
            # Determine outreach approach
            if influencer['total_reach'] > 100000:
                approach = "Partnership/Sponsorship"
                timeline = "2-4 weeks"
            elif influencer['total_reach'] > 10000:
                approach = "Product Collaboration"
                timeline = "1-2 weeks"
            else:
                approach = "Authentic Engagement"
                timeline = "3-7 days"
            
            recommendations.append({
                'influencer': influencer,
                'priority_score': round(priority_score, 3),
                'approach': approach,
                'timeline': timeline,
                'contact_method': self._suggest_contact_method(influencer),
                'talking_points': self._generate_talking_points(influencer)
            })
        
        # Sort by priority score and return top 20
        recommendations.sort(key=lambda x: x['priority_score'], reverse=True)
        return recommendations[:20]
    
    def _suggest_contact_method(self, influencer: Dict) -> str:
        """Suggest best contact method"""
        if influencer['contact_email']:
            return f"Email: {influencer['contact_email']}"
        elif influencer['primary_platform'] == 'linkedin':
            return "LinkedIn Message"
        elif influencer['primary_platform'] == 'instagram':
            return "Instagram DM"
        elif influencer['primary_platform'] == 'twitter':
            return "Twitter DM"
        else:
            return f"{influencer['primary_platform'].title()} Message"
    
    def _generate_talking_points(self, influencer: Dict) -> List[str]:
        """Generate personalized talking points"""
        points = []
        
        # Content theme alignment
        if influencer['content_themes']:
            points.append(f"Shared interest in {', '.join(influencer['content_themes'][:2])}")
        
        # Platform-specific points
        if influencer['primary_platform'] == 'youtube':
            points.append("Video collaboration opportunity")
        elif influencer['primary_platform'] == 'instagram':
            points.append("Visual content partnership")
        elif influencer['primary_platform'] == 'linkedin':
            points.append("Professional thought leadership")
        
        # Engagement compliment
        if influencer['avg_engagement_rate'] > 5:
            points.append("Impressive audience engagement")
        
        # Location-based if available
        if influencer['location']:
            points.append(f"Local connection ({influencer['location']})")
        
        return points[:3]  # Limit to 3 talking points
    
    def _get_top_performers(self, influencers: List[Dict]) -> Dict[str, Any]:
        """Get top performing influencers by various metrics"""
        if not influencers:
            return {}
        
        return {
            'highest_reach': max(influencers, key=lambda x: x['total_reach']),
            'best_engagement': max(influencers, key=lambda x: x['avg_engagement_rate']),
            'best_alignment': max(influencers, key=lambda x: x['brand_alignment_score']),
            'most_versatile': max(influencers, key=lambda x: len(x['social_profiles']))
        }
    
    def _generate_html_report(self, report_data: Dict) -> Path:
        """Generate HTML report"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Influencer Report - {report_data['brand_name']}</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6; margin: 0; padding: 20px; background-color: #f5f5f5;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 40px; padding-bottom: 20px; border-bottom: 2px solid #e0e0e0; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 40px; }}
        .metric {{ text-align: center; padding: 20px; background: #f8f9fa; border-radius: 8px; }}
        .metric-value {{ font-size: 2em; font-weight: bold; color: #2563eb; }}
        .metric-label {{ color: #666; font-size: 0.9em; }}
        .influencer-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 40px; }}
        .influencer-card {{ 
            border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; background: white;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .influencer-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }}
        .platform-badge {{ 
            display: inline-block; padding: 4px 8px; border-radius: 12px; font-size: 0.8em;
            background: #e3f2fd; color: #1976d2; margin-right: 8px;
        }}
        .alignment-score {{ 
            font-weight: bold; padding: 4px 8px; border-radius: 4px;
            color: white; font-size: 0.9em;
        }}
        .score-high {{ background: #4caf50; }}
        .score-medium {{ background: #ff9800; }}
        .score-low {{ background: #f44336; }}
        .social-links {{ margin-top: 10px; }}
        .social-link {{ 
            display: inline-block; padding: 6px 12px; margin: 2px; background: #2563eb;
            color: white; text-decoration: none; border-radius: 15px; font-size: 0.8em;
        }}
        .social-link:hover {{ background: #1d4ed8; }}
        .recommendations {{ margin-top: 40px; }}
        .recommendation {{ 
            border-left: 4px solid #2563eb; padding: 15px; margin: 10px 0;
            background: #f8f9ff; border-radius: 0 8px 8px 0;
        }}
        .talking-points {{ list-style: none; padding: 0; }}
        .talking-points li {{ 
            padding: 4px 0; position: relative; padding-left: 20px;
        }}
        .talking-points li:before {{ 
            content: "•"; color: #2563eb; font-weight: bold; position: absolute; left: 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌟 Influencer Discovery Report</h1>
            <h2>{report_data['brand_name']}</h2>
            <p>Generated on {datetime.fromisoformat(report_data['generated_at']).strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>

        <div class="summary">
            <div class="metric">
                <div class="metric-value">{report_data['summary']['total_influencers']}</div>
                <div class="metric-label">Total Influencers</div>
            </div>
            <div class="metric">
                <div class="metric-value">{report_data['summary']['total_reach']:,}</div>
                <div class="metric-label">Combined Reach</div>
            </div>
            <div class="metric">
                <div class="metric-value">{report_data['summary']['avg_engagement']}%</div>
                <div class="metric-label">Avg Engagement</div>
            </div>
            <div class="metric">
                <div class="metric-value">{report_data['summary']['avg_alignment']}</div>
                <div class="metric-label">Brand Alignment</div>
            </div>
            <div class="metric">
                <div class="metric-value">{report_data['summary']['platforms_covered']}</div>
                <div class="metric-label">Platforms</div>
            </div>
        </div>

        <h3>📱 Platform Breakdown</h3>
        <div class="influencer-grid">
        """
        
        for platform in report_data['platform_breakdown']:
            html_content += f"""
            <div class="influencer-card">
                <h4><span class="platform-badge">{platform['platform'].title()}</span></h4>
                <p><strong>{platform['count']}</strong> influencers</p>
                <p><strong>{platform['total_reach']:,}</strong> combined reach</p>
                <p><strong>{platform['avg_engagement']}%</strong> avg engagement</p>
                <p><strong>{platform['avg_alignment']}</strong> avg alignment</p>
            </div>
            """
        
        html_content += """
        </div>

        <h3>🎯 Top Influencers</h3>
        <div class="influencer-grid">
        """
        
        for influencer in report_data['influencers'][:12]:  # Show top 12
            alignment_class = "score-high" if influencer['brand_alignment_score'] > 0.7 else "score-medium" if influencer['brand_alignment_score'] > 0.4 else "score-low"
            
            social_links_html = ""
            for platform, profile in influencer.get('social_profiles', {}).items():
                social_links_html += f'<a href="{profile["profile_url"]}" class="social-link" target="_blank">{platform.title()}</a>'
            
            content_themes = ", ".join(influencer.get('content_themes', [])[:3])
            
            html_content += f"""
            <div class="influencer-card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                    <h4 style="margin: 0;">{influencer['name']}</h4>
                    <span class="alignment-score {alignment_class}">{influencer['brand_alignment_score']}</span>
                </div>
                <span class="platform-badge">{influencer['primary_platform'].title()}</span>
                <p><strong>{influencer['total_reach']:,}</strong> followers • <strong>{influencer['avg_engagement_rate']}%</strong> engagement</p>
                <p style="color: #666; font-size: 0.9em; margin-bottom: 10px;">{influencer['bio_summary'][:100]}...</p>
                {f'<p><strong>Themes:</strong> {content_themes}</p>' if content_themes else ''}
                <div class="social-links">{social_links_html}</div>
                <p style="font-size: 0.8em; color: #666; margin-top: 10px;">{influencer['outreach_notes']}</p>
            </div>
            """
        
        html_content += """
        </div>

        <div class="recommendations">
            <h3>🚀 Outreach Recommendations</h3>
        """
        
        for i, rec in enumerate(report_data['outreach_recommendations'][:10], 1):
            influencer = rec['influencer']
            html_content += f"""
            <div class="recommendation">
                <h4>#{i} {influencer['name']} - {rec['approach']}</h4>
                <p><strong>Priority Score:</strong> {rec['priority_score']} • <strong>Timeline:</strong> {rec['timeline']}</p>
                <p><strong>Contact:</strong> {rec['contact_method']}</p>
                <p><strong>Talking Points:</strong></p>
                <ul class="talking-points">
                    {''.join(f'<li>{point}</li>' for point in rec['talking_points'])}
                </ul>
            </div>
            """
        
        html_content += """
        </div>
    </div>
</body>
</html>
        """
        
        # Save HTML file
        filename = f"{report_data['report_id']}.html"
        report_file = self.report_dir / filename
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return report_file
    
    def _generate_json_report(self, report_data: Dict) -> Path:
        """Generate JSON report"""
        filename = f"{report_data['report_id']}.json"
        report_file = self.report_dir / filename
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        return report_file
    
    def _generate_csv_report(self, report_data: Dict) -> Path:
        """Generate CSV report"""
        import csv
        
        filename = f"{report_data['report_id']}.csv"
        report_file = self.report_dir / filename
        
        with open(report_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Name', 'Platform', 'Brand', 'Followers', 'Engagement_Rate',
                'Alignment_Score', 'Contact_Email', 'Website', 'Location',
                'Bio_Summary', 'Content_Themes', 'Profile_URLs', 'Outreach_Notes'
            ])
            
            # Data
            for influencer in report_data['influencers']:
                profile_urls = [profile['profile_url'] for profile in influencer.get('social_profiles', {}).values()]
                
                writer.writerow([
                    influencer['name'],
                    influencer['primary_platform'],
                    influencer['brand'],
                    influencer['total_reach'],
                    influencer['avg_engagement_rate'],
                    influencer['brand_alignment_score'],
                    influencer.get('contact_email', ''),
                    influencer.get('website', ''),
                    influencer.get('location', ''),
                    influencer['bio_summary'],
                    ', '.join(influencer.get('content_themes', [])),
                    ', '.join(profile_urls),
                    influencer['outreach_notes']
                ])
        
        return report_file

def generate_all_brand_reports():
    """Generate reports for all brands"""
    generator = InfluencerReportGenerator()
    
    print("📊 Generating influencer reports for all brands...")
    
    reports = []
    
    # Generate individual brand reports
    for brand_key in BRAND_INFLUENCER_STRATEGIES.keys():
        try:
            report = generator.generate_brand_report(brand=brand_key, format="html")
            reports.append(report)
            print(f"✅ {report['brand_name']}: {report['summary']['total_influencers']} influencers")
        except Exception as e:
            print(f"❌ Error generating report for {brand_key}: {e}")
    
    # Generate combined report
    try:
        combined_report = generator.generate_brand_report(brand=None, format="html")
        reports.append(combined_report)
        print(f"✅ Combined Report: {combined_report['summary']['total_influencers']} total influencers")
    except Exception as e:
        print(f"❌ Error generating combined report: {e}")
    
    print(f"\n📁 Reports saved to: {generator.report_dir}")
    return reports

if __name__ == "__main__":
    generate_all_brand_reports()