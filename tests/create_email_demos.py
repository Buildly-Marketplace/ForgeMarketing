#!/usr/bin/env python3
"""
Branded Email Template Demo
Generates sample HTML files to preview brand designs locally
"""

from email_templates import BrandEmailRenderer
from pathlib import Path
import webbrowser

def create_demo_files():
    """Create HTML demo files for each brand"""
    renderer = BrandEmailRenderer()
    
    # Create demo directory
    demo_dir = Path("email_demos")
    demo_dir.mkdir(exist_ok=True)
    
    # Sample data for demos
    demo_data = {
        'foundry': {
            'brand_name': 'First City Foundry',
            'subtitle': 'Startup Incubator Partnership',
            'description': 'Supporting innovative startups and entrepreneurs worldwide',
            'from_name': 'First City Foundry Team',
            'website': 'https://www.firstcityfoundry.com',
            'unsubscribe_url': 'https://www.firstcityfoundry.com/unsubscribe'
        },
        'buildly': {
            'brand_name': 'Buildly',
            'subtitle': 'Low-Code Platform Innovation',
            'description': 'Rapid application development with AI-powered tools',
            'from_name': 'Buildly Team',
            'website': 'https://buildly.io',
            'unsubscribe_url': 'https://buildly.io/unsubscribe'
        },
        'openbuild': {
            'brand_name': 'Open Build',
            'subtitle': 'Open Source Community',
            'description': 'Building the future of open source development',
            'from_name': 'Open Build Team',
            'website': 'https://open.build',
            'unsubscribe_url': 'https://open.build/unsubscribe'
        },
        'radical': {
            'brand_name': 'Radical Therapy',
            'subtitle': 'Mental Health & Wellness',
            'description': 'Revolutionary approach to mental health care',
            'from_name': 'Radical Therapy Team',
            'website': 'https://radicaltherapy.org',
            'unsubscribe_url': 'https://radicaltherapy.org/unsubscribe'
        },
        'oregonsoftware': {
            'brand_name': 'Oregon Software',
            'subtitle': 'Professional Development Services',
            'description': 'Expert software solutions for modern businesses',
            'from_name': 'Oregon Software Team',
            'website': 'https://oregonsoftware.org',
            'unsubscribe_url': 'https://oregonsoftware.org/unsubscribe'
        }
    }
    
    # Create demo files for each brand
    for brand_key, brand_data in demo_data.items():
        # Add common demo data
        brand_data.update({
            'date': '2024-10-04',
            'analytics': {
                'sessions': '1,234',
                'users': '856',
                'pageviews': '2,856',
                'bounce_rate': '45.2%',
                'emails_sent': '25',
                'open_rate': '28.5%',
                'click_rate': '3.2%'
            }
        })
        
        # Generate both campaign types
        for campaign_type in ['general_outreach', 'daily_analytics']:
            try:
                email_result = renderer.render_email(brand_key, campaign_type, brand_data)
                
                # Save to file
                filename = f"{brand_key}_{campaign_type}_demo.html"
                file_path = demo_dir / filename
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(email_result['html'])
                
                print(f"✅ Created: {filename}")
                
            except Exception as e:
                print(f"❌ Failed to create {brand_key} {campaign_type}: {e}")
    
    # Create index file
    index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Brand Email Template Showcase</title>
    <style>
        body { font-family: system-ui, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; margin-bottom: 30px; }
        .brand-section { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
        .brand-title { font-size: 20px; font-weight: 600; margin-bottom: 15px; color: #2563eb; }
        .template-links { display: flex; gap: 15px; }
        .template-links a { padding: 8px 16px; background: #f0f9ff; color: #2563eb; text-decoration: none; border-radius: 6px; border: 1px solid #2563eb; }
        .template-links a:hover { background: #2563eb; color: white; }
        .description { color: #666; margin-bottom: 15px; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Brand Email Template Showcase</h1>
        <p style="text-align: center; color: #666; margin-bottom: 40px;">
            Each brand has unique HTML email templates matching their website design
        </p>
        
        <div class="brand-section">
            <div class="brand-title">🚀 First City Foundry</div>
            <div class="description">Startup incubator with purple gradient design and professional styling</div>
            <div class="template-links">
                <a href="foundry_general_outreach_demo.html" target="_blank">Partnership Outreach</a>
                <a href="foundry_daily_analytics_demo.html" target="_blank">Analytics Report</a>
            </div>
        </div>
        
        <div class="brand-section">
            <div class="brand-title">⚡ Buildly</div>
            <div class="description">Low-code platform with blue/orange branding and modern Inter font</div>
            <div class="template-links">
                <a href="buildly_general_outreach_demo.html" target="_blank">Partnership Outreach</a>
                <a href="buildly_daily_analytics_demo.html" target="_blank">Analytics Report</a>
            </div>
        </div>
        
        <div class="brand-section">
            <div class="brand-title">🔨 Open Build</div>
            <div class="description">Open source community with clean blue design and developer focus</div>
            <div class="template-links">
                <a href="openbuild_general_outreach_demo.html" target="_blank">Partnership Outreach</a>
                <a href="openbuild_daily_analytics_demo.html" target="_blank">Analytics Report</a>
            </div>
        </div>
        
        <div class="brand-section">
            <div class="brand-title">🌱 Radical Therapy</div>
            <div class="description">Mental health platform with purple branding and elegant serif typography</div>
            <div class="template-links">
                <a href="radical_general_outreach_demo.html" target="_blank">Partnership Outreach</a>
                <a href="radical_daily_analytics_demo.html" target="_blank">Analytics Report</a>
            </div>
        </div>
        
        <div class="brand-section">
            <div class="brand-title">💻 Oregon Software</div>
            <div class="description">Software consultancy with sky blue design and technical focus</div>
            <div class="template-links">
                <a href="oregonsoftware_general_outreach_demo.html" target="_blank">Partnership Outreach</a>
                <a href="oregonsoftware_daily_analytics_demo.html" target="_blank">Analytics Report</a>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 14px;">
            <p>These templates are automatically used by the marketing automation system</p>
            <p>Each email maintains brand consistency with the corresponding website design</p>
        </div>
    </div>
</body>
</html>
    """
    
    index_path = demo_dir / "index.html"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print(f"\n✅ Demo files created in: {demo_dir.absolute()}")
    print(f"🌐 Open: {index_path.absolute()}")
    
    # Optionally open in browser
    try:
        webbrowser.open(f"file://{index_path.absolute()}")
        print("📱 Opened in default browser")
    except Exception as e:
        print(f"⚠️  Could not auto-open browser: {e}")

if __name__ == "__main__":
    create_demo_files()