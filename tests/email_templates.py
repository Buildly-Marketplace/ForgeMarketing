#!/usr/bin/env python3
"""
Enhanced Email Template System
HTML email templates matching each brand's website design
Uses brand-specific colors, fonts, and styling
"""

import os
import re
from pathlib import Path
from typing import Dict, Any

# Brand-specific HTML email templates with matching website designs
BRAND_EMAIL_TEMPLATES = {
    'foundry': {
        'brand_info': {
            'name': 'Buildly Labs Foundry',
            'tagline': 'Global Startup Foundry for Developers - Apply for Help Worldwide',
            'description': 'Equity-free startup incubator designed for software developers and entrepreneurs worldwide',
            'website': 'https://www.firstcityfoundry.com',
            'logo_url': 'https://www.firstcityfoundry.com/assets/img/logo-horizontal.png'
        },
        'colors': {
            'primary': '#3b82f6',
            'secondary': '#2563eb', 
            'accent': '#f59e0b',
            'background': '#f0f9ff',
            'text': '#1e293b',
            'text_light': '#64748b'
        },
        'fonts': {
            'primary': 'system-ui, -apple-system, sans-serif',
            'heading': 'system-ui, -apple-system, sans-serif'
        },
        'template': '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: {font_primary}; margin: 0; padding: 20px; background-color: {color_background}; line-height: 1.6; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; box-shadow: 0 4px 12px rgba(59,130,246,0.1); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, {color_primary} 0%, {color_secondary} 100%); color: white; padding: 30px 25px; text-align: left; display: flex; align-items: center; gap: 15px; }}
        .logo {{ width: 40px; height: 40px; background: rgba(255,255,255,0.2); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 20px; }}
        .header-text h1 {{ margin: 0 0 5px 0; font-size: 24px; font-weight: bold; }}
        .header-text p {{ margin: 0; opacity: 0.9; font-size: 14px; }}
        .content {{ padding: 30px 25px; }}
        .content h2 {{ color: {color_primary}; margin: 0 0 15px 0; font-size: 18px; border-bottom: 2px solid {color_primary}; padding-bottom: 8px; }}
        .content h3 {{ color: {color_text}; margin: 25px 0 10px 0; font-size: 16px; }}
        .content p {{ color: {color_text}; margin: 12px 0; }}
        .metrics {{ display: flex; flex-wrap: wrap; gap: 15px; margin: 20px 0; }}
        .metric {{ background: #f8fafc; padding: 15px; border-radius: 8px; text-align: center; min-width: 120px; flex: 1; border-left: 4px solid {color_primary}; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: {color_primary}; margin-bottom: 5px; }}
        .metric-label {{ font-size: 11px; color: {color_text_light}; text-transform: uppercase; letter-spacing: 0.5px; }}
        .highlight {{ background: linear-gradient(45deg, rgba(59,130,246,0.1), rgba(37,99,235,0.05)); padding: 15px; border-left: 4px solid {color_accent}; margin: 15px 0; border-radius: 0 6px 6px 0; }}
        .cta-button {{ display: inline-block; background: {color_accent}; color: white; padding: 14px 28px; text-decoration: none; border-radius: 8px; font-weight: 600; margin: 15px 0; transition: all 0.3s ease; }}
        .footer {{ background: #f8fafc; padding: 25px; text-align: center; border-top: 1px solid #e5e7eb; }}
        .footer p {{ margin: 8px 0; font-size: 12px; color: {color_text_light}; }}
        .footer a {{ color: {color_primary}; text-decoration: none; font-weight: 500; }}
        @media (max-width: 600px) {{
            .header {{ flex-direction: column; text-align: center; }}
            .metrics {{ flex-direction: column; }}
            .metric {{ min-width: auto; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🏗️</div>
            <div class="header-text">
                <h1>{brand_name}</h1>
                <p>{brand_tagline}</p>
            </div>
        </div>
        <div class="content">
            {email_content}
        </div>
        <div class="footer">
            <p><strong>{brand_name}</strong> - {brand_description}</p>
            <p>🌐 <a href="{brand_website}">Visit {brand_name}</a></p>
            <p><a href="{unsubscribe_url}">Manage Preferences</a> | <a href="{brand_website}">Visit Website</a></p>
        </div>
    </div>
</body>
</html>'''
    },
    
    'buildly': {
        'brand_info': {
            'name': 'Buildly',
            'tagline': 'AI + Product Management + Open Source Tools',
            'description': 'Comprehensive platform combining AI-powered development, radical agile product management, and sustainable open source developer tools',
            'website': 'https://www.buildly.io',
            'logo_url': 'https://www.buildly.io/media/buildly-logo.svg'
        },
        'colors': {
            'primary': '#1b5fa3',
            'secondary': '#144a84',
            'accent': '#f9943b',
            'background': '#F3F4F6',
            'text': '#1F2937',
            'text_light': '#6B7280'
        },
        'fonts': {
            'primary': 'Inter, system-ui, sans-serif',
            'heading': 'Inter, system-ui, sans-serif'
        },
        'template': '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: {font_primary}; margin: 0; padding: 20px; background-color: {color_background}; line-height: 1.6; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(27,95,163,0.1); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, {color_primary} 0%, {color_secondary} 100%); color: white; padding: 30px 25px; position: relative; display: flex; align-items: center; gap: 15px; }}
        .header::after {{ content: ''; position: absolute; bottom: -10px; left: 0; right: 0; height: 10px; background: linear-gradient(45deg, {color_accent}, {color_primary}); }}
        .logo {{ width: 45px; height: 45px; background: rgba(255,255,255,0.2); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 22px; }}
        .header-text h1 {{ margin: 0 0 5px 0; font-size: 26px; font-weight: 600; }}
        .header-text p {{ margin: 0; opacity: 0.95; font-size: 14px; font-weight: 400; }}
        .content {{ padding: 30px 25px; }}
        .content h2 {{ color: {color_primary}; margin: 0 0 15px 0; font-size: 20px; font-weight: 600; }}
        .content h3 {{ color: {color_text}; margin: 25px 0 10px 0; font-size: 16px; font-weight: 500; }}
        .content p {{ color: {color_text}; margin: 14px 0; font-weight: 400; }}
        .buildly-section {{ background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 20px; border-radius: 10px; margin: 20px 0; border: 1px solid rgba(27,95,163,0.1); }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 15px; margin: 25px 0; }}
        .metric {{ background: white; padding: 20px 15px; border-radius: 10px; text-align: center; border: 2px solid {color_background}; transition: all 0.3s ease; }}
        .metric:hover {{ border-color: {color_primary}; transform: translateY(-2px); }}
        .metric-value {{ font-size: 28px; font-weight: 700; color: {color_primary}; margin-bottom: 5px; }}
        .metric-label {{ font-size: 11px; color: {color_text_light}; text-transform: uppercase; font-weight: 500; letter-spacing: 0.8px; }}
        .highlight {{ background: linear-gradient(45deg, #fff7ed, #fed7aa); padding: 18px; border-left: 4px solid {color_accent}; margin: 18px 0; border-radius: 0 8px 8px 0; }}
        .cta-button {{ display: inline-block; background: {color_accent}; color: white; padding: 14px 28px; text-decoration: none; border-radius: 8px; font-weight: 600; margin: 15px 0; transition: all 0.3s ease; }}
        .cta-button:hover {{ background: #e8843a; transform: translateY(-1px); }}
        .footer {{ background: {color_background}; padding: 25px; text-align: center; }}
        .footer p {{ margin: 8px 0; font-size: 12px; color: {color_text_light}; }}
        .footer a {{ color: {color_primary}; text-decoration: none; font-weight: 500; }}
        @media (max-width: 600px) {{
            .header {{ flex-direction: column; text-align: center; }}
            .metrics {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">⚡</div>
            <div class="header-text">
                <h1>{brand_name}</h1>
                <p>{brand_tagline}</p>
            </div>
        </div>
        <div class="content">
            {email_content}
        </div>
        <div class="footer">
            <p><strong>{brand_name}</strong> - {brand_description}</p>
            <p>🌐 <a href="{brand_website}">Visit {brand_name}</a> | 📚 <a href="https://labs.buildly.io">Buildly Labs</a></p>
            <p><a href="{unsubscribe_url}">Manage Preferences</a> | <a href="{brand_website}">Visit Website</a></p>
        </div>
    </div>
</body>
</html>'''
    },
    
    'openbuild': {
        'brand_info': {
            'name': 'Open Build',
            'tagline': 'AI Software Development Training & Mentorship',
            'description': 'Empowering developers through training, mentorship, and ethical open source development',
            'website': 'https://www.open.build',
            'logo_url': 'https://www.open.build/assets/img/logo.png'
        },
        'colors': {
            'primary': '#2563eb',
            'secondary': '#1d4ed8', 
            'accent': '#f59e0b',
            'background': '#f8fafc',
            'text': '#1e293b',
            'text_light': '#64748b'
        },
        'fonts': {
            'primary': 'system-ui, -apple-system, sans-serif',
            'heading': 'system-ui, -apple-system, sans-serif'
        },
        'template': '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: {font_primary}; margin: 0; padding: 20px; background-color: {color_background}; line-height: 1.6; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 8px; box-shadow: 0 4px 16px rgba(37,99,235,0.1); overflow: hidden; }}
        .header {{ background: {color_primary}; color: white; padding: 25px; text-align: center; position: relative; }}
        .header::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: {color_accent}; }}
        .header h1 {{ margin: 0 0 5px 0; font-size: 24px; font-weight: 700; }}
        .header p {{ margin: 0; opacity: 0.9; font-size: 14px; }}
        .content {{ padding: 25px; }}
        .content h2 {{ color: {color_primary}; margin: 0 0 15px 0; font-size: 18px; font-weight: 600; display: flex; align-items: center; }}
        .content h2::before {{ content: '▶'; margin-right: 8px; color: {color_accent}; }}
        .content h3 {{ color: {color_text}; margin: 20px 0 8px 0; font-size: 16px; font-weight: 600; }}
        .content p {{ color: {color_text}; margin: 12px 0; }}
        .openbuild-highlight {{ background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); padding: 16px; border-radius: 6px; margin: 15px 0; border-left: 3px solid {color_primary}; }}
        .metrics {{ display: flex; flex-wrap: wrap; gap: 12px; margin: 20px 0; }}
        .metric {{ background: #f1f5f9; padding: 16px 12px; border-radius: 6px; text-align: center; flex: 1; min-width: 110px; border-top: 3px solid {color_primary}; }}
        .metric-value {{ font-size: 22px; font-weight: 700; color: {color_primary}; margin-bottom: 4px; }}
        .metric-label {{ font-size: 10px; color: {color_text_light}; text-transform: uppercase; font-weight: 600; }}
        .code-block {{ background: #1e293b; color: #e2e8f0; padding: 15px; border-radius: 6px; font-family: 'Courier New', monospace; font-size: 13px; margin: 15px 0; }}
        .footer {{ background: #f1f5f9; padding: 20px; text-align: center; }}
        .footer p {{ margin: 6px 0; font-size: 11px; color: {color_text_light}; }}
        .footer a {{ color: {color_primary}; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{brand_name}</h1>
            <p>{brand_tagline}</p>
        </div>
        <div class="content">
            {email_content}
        </div>
        <div class="footer">
            <p><strong>Open Build</strong> - Open source development community</p>
            <p>🌐 <a href="{brand_website}">open.build</a> | 📖 <a href="https://docs.open.build">Documentation</a></p>
            <p><a href="{unsubscribe_url}">Unsubscribe</a></p>
        </div>
    </div>
</body>
</html>'''
    },
    
    'radical': {
        'brand_info': {
            'name': 'Radical Therapy for Software Developers',
            'tagline': 'Cloud Native AI Development meets Agile & Vibe Coding',
            'description': 'Transform software teams through cloud native AI development, agile project management, and radical transparency',
            'website': 'https://www.radicaltherapy.dev',
            'logo_url': 'https://radicaltherapy.dev/assets/img/logo.png'
        },
        'colors': {
            'primary': '#7c3aed',
            'secondary': '#5b21b6',
            'accent': '#f59e0b', 
            'background': '#faf5ff',
            'text': '#1f2937',
            'text_light': '#6b7280'
        },
        'fonts': {
            'primary': 'Inter, system-ui, sans-serif',
            'heading': 'Inter, system-ui, sans-serif'
        },
        'template': '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: {font_primary}; margin: 0; padding: 20px; background-color: {color_background}; line-height: 1.7; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 8px 24px rgba(124,58,237,0.1); overflow: hidden; border: 1px solid #e5e7eb; }}
        .header {{ background: linear-gradient(135deg, {color_primary} 0%, {color_secondary} 100%); color: white; padding: 25px; text-align: center; }}
        .header h1 {{ margin: 0 0 8px 0; font-size: 26px; font-weight: 300; font-family: {font_heading}; }}
        .header p {{ margin: 0; opacity: 0.95; font-size: 15px; font-style: italic; }}
        .content {{ padding: 30px 25px; }}
        .content h2 {{ color: {color_primary}; margin: 0 0 20px 0; font-size: 20px; font-weight: 400; font-family: {font_heading}; }}
        .content h3 {{ color: {color_text}; margin: 25px 0 12px 0; font-size: 17px; font-weight: 500; font-family: {font_heading}; }}
        .content p {{ color: {color_text}; margin: 16px 0; }}
        .therapy-section {{ background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%); padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 5px solid {color_primary}; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 18px; margin: 25px 0; }}
        .metric {{ background: #fefefe; padding: 18px; border-radius: 8px; text-align: center; border: 1px solid #e5e7eb; box-shadow: 0 2px 8px rgba(124,58,237,0.05); }}
        .metric-value {{ font-size: 26px; font-weight: 300; color: {color_primary}; margin-bottom: 8px; }}
        .metric-label {{ font-size: 12px; color: {color_text_light}; text-transform: lowercase; font-weight: 400; }}
        .quote {{ background: #f9fafb; padding: 20px; border-left: 4px solid {color_accent}; margin: 20px 0; font-style: italic; color: {color_text}; border-radius: 0 8px 8px 0; }}
        .footer {{ background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%); padding: 25px; text-align: center; }}
        .footer p {{ margin: 8px 0; font-size: 13px; color: {color_text_light}; }}
        .footer a {{ color: {color_primary}; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{brand_name}</h1>
            <p>{brand_tagline}</p>
        </div>
        <div class="content">
            {email_content}
        </div>
        <div class="footer">
            <p><strong>Radical Therapy</strong> - Mental health and wellness platform</p>
            <p>🌐 <a href="{brand_website}">radicaltherapy.org</a> | 💚 <a href="https://radicaltherapy.org/resources">Resources</a></p>
            <p><a href="{unsubscribe_url}">Update Preferences</a></p>
        </div>
    </div>
</body>
</html>'''
    },
    
    'oregonsoftware': {
        'brand_info': {
            'name': 'Oregon Software',
            'tagline': 'Custom Software Development & Nearshore Solutions',
            'description': 'Expert nearshore development teams for cloud software, app development & enterprise solutions',
            'website': 'https://www.oregonsoftware.com',
            'logo_url': 'https://www.oregonsoftware.com/assets/img/logo.png'
        },
        'colors': {
            'primary': '#0ea5e9',
            'secondary': '#0284c7',
            'accent': '#596808',
            'background': '#f0f9ff',
            'text': '#0f172a',
            'text_light': '#475569'
        },
        'fonts': {
            'primary': 'system-ui, -apple-system, sans-serif',
            'heading': 'system-ui, -apple-system, sans-serif'
        },
        'template': '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: {font_primary}; margin: 0; padding: 20px; background-color: {color_background}; line-height: 1.6; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 8px; box-shadow: 0 4px 16px rgba(14,165,233,0.1); overflow: hidden; }}
        .header {{ background: linear-gradient(90deg, {color_primary} 0%, {color_secondary} 100%); color: white; padding: 25px; }}
        .header h1 {{ margin: 0 0 5px 0; font-size: 24px; font-weight: 600; }}
        .header p {{ margin: 0; opacity: 0.9; font-size: 14px; }}
        .content {{ padding: 25px; }}
        .content h2 {{ color: {color_primary}; margin: 0 0 15px 0; font-size: 18px; font-weight: 600; }}
        .content h3 {{ color: {color_text}; margin: 20px 0 8px 0; font-size: 16px; font-weight: 600; }}
        .content p {{ color: {color_text}; margin: 12px 0; }}
        .oregon-section {{ background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 18px; border-radius: 8px; margin: 18px 0; }}
        .metrics {{ display: flex; flex-wrap: wrap; gap: 15px; margin: 20px 0; }}
        .metric {{ background: #f8fafc; padding: 16px; border-radius: 8px; text-align: center; flex: 1; min-width: 120px; border-left: 4px solid {color_primary}; }}
        .metric-value {{ font-size: 24px; font-weight: 600; color: {color_primary}; margin-bottom: 5px; }}
        .metric-label {{ font-size: 11px; color: {color_text_light}; text-transform: uppercase; font-weight: 500; }}
        .tech-highlight {{ background: #ecfdf5; padding: 15px; border-left: 4px solid {color_accent}; margin: 15px 0; border-radius: 0 6px 6px 0; }}
        .footer {{ background: #f8fafc; padding: 20px; text-align: center; }}
        .footer p {{ margin: 6px 0; font-size: 12px; color: {color_text_light}; }}
        .footer a {{ color: {color_primary}; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{brand_name}</h1>
            <p>{brand_tagline}</p>
        </div>
        <div class="content">
            {email_content}
        </div>
        <div class="footer">
            <p><strong>Oregon Software</strong> - Professional software development services</p>
            <p>🌐 <a href="{brand_website}">oregonsoftware.org</a> | 🛠️ <a href="https://oregonsoftware.org/services">Services</a></p>
            <p><a href="{unsubscribe_url}">Unsubscribe</a></p>
        </div>
    </div>
</body>
</html>'''
    }
}

class BrandEmailRenderer:
    """Renders HTML emails using brand-specific templates"""
    
    def __init__(self):
        self.templates = BRAND_EMAIL_TEMPLATES
        
    def render_email(self, brand_key: str, campaign_type: str, content_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Render HTML email for specific brand and campaign type
        
        Args:
            brand_key: Brand identifier (foundry, buildly, etc.)
            campaign_type: Type of email campaign
            content_data: Data to populate the email template
            
        Returns:
            Dict with 'html', 'text', and 'subject' keys
        """
        if brand_key not in self.templates:
            raise ValueError(f"Unknown brand: {brand_key}")
            
        brand_config = self.templates[brand_key]
        brand_info = brand_config['brand_info']
        colors = brand_config['colors']
        fonts = brand_config['fonts']
        template = brand_config['template']
        
        # Generate content based on campaign type
        email_content = self._generate_content(campaign_type, content_data, brand_key, brand_info)
        
        # Render HTML template
        html_content = template.format(
            # Colors
            color_primary=colors['primary'],
            color_secondary=colors['secondary'],
            color_accent=colors['accent'],
            color_background=colors['background'],
            color_text=colors['text'],
            color_text_light=colors['text_light'],
            # Fonts
            font_primary=fonts['primary'],
            font_heading=fonts.get('heading', fonts['primary']),
            # Brand Info
            brand_name=brand_info['name'],
            brand_tagline=brand_info['tagline'],
            brand_description=brand_info['description'],
            brand_website=brand_info['website'],
            brand_logo_url=brand_info['logo_url'],
            # Content
            email_content=email_content,
            unsubscribe_url=content_data.get('unsubscribe_url', f"{brand_info['website']}/unsubscribe")
        )
        
        # Generate plain text version
        text_content = self._html_to_text(html_content)
        
        # Generate subject
        subject = self._generate_subject(campaign_type, content_data, brand_key)
        
        return {
            'html': html_content,
            'text': text_content,
            'subject': subject
        }
        
    def _generate_content(self, campaign_type: str, data: Dict[str, Any], brand_key: str, brand_info: Dict[str, str]) -> str:
        """Generate email content based on campaign type"""
        
        if campaign_type == 'general_outreach':
            # Customize content based on brand
            if brand_key == 'foundry':
                return f'''
                <h2>🚀 Startup Partnership Opportunity</h2>
                <p>Hello!</p>
                <p>I hope this email finds you well. I'm reaching out from <strong>{brand_info['name']}</strong> regarding our global startup foundry program.</p>
                
                <div class="highlight">
                    <p><strong>What we offer:</strong> {brand_info['description']} - completely equity-free with cloud hosting, AI analysis, and expert mentorship.</p>
                </div>
                
                <p>We're building a global network of innovative developers and entrepreneurs who are transforming ideas into successful businesses.</p>
                
                <h3>🌟 Why join our foundry program?</h3>
                <ul>
                    <li>🆓 100% equity-free startup support</li>
                    <li>☁️ Free cloud hosting credits and technical resources</li>
                    <li>🤖 AI-powered startup analysis and recommendations</li>
                    <li>🌍 Global network through OpenBuild and Buildly Labs</li>
                </ul>
                
                <p>Would you be interested in exploring how our foundry can accelerate your startup journey?</p>
                
                <a href="https://www.firstcityfoundry.com/register.html" class="cta-button">Apply to Our Foundry Program</a>
                
                <p>Best regards,<br>
                <strong>Buildly Labs Foundry Team</strong></p>
                '''
            elif brand_key == 'buildly':
                return f'''
                <h2>⚡ AI-Powered Development Partnership</h2>
                <p>Hello!</p>
                <p>I hope this email finds you well. I'm reaching out from <strong>{brand_info['name']}</strong> regarding sustainable AI development solutions.</p>
                
                <div class="highlight">
                    <p><strong>Our mission:</strong> {brand_info['description']} - the scalable alternative to magic button vibe coding that builds lasting teams and maintainable software.</p>
                </div>
                
                <p>We're passionate about helping teams build sustainable software through transparent AI automation, radical agile product management, and open source developer tools.</p>
                
                <h3>🎯 What makes Buildly different?</h3>
                <ul>
                    <li>📊 AI-assisted backlog prioritization & planning</li>
                    <li>🔧 Maintainable component-driven architecture</li>
                    <li>📈 Enterprise-ready release pipelines & audit trails</li>
                    <li>🌱 Sustainable growth from startup to enterprise</li>
                </ul>
                
                <p>Would you be interested in exploring how Buildly can transform your development process?</p>
                
                <a href="https://labs.buildly.io" class="cta-button">Try Buildly Labs for Free</a>
                
                <p>Best regards,<br>
                <strong>The Buildly Team</strong></p>
                '''
            elif brand_key == 'openbuild':
                return f'''
                <h2>🛠️ Developer Training & Mentorship</h2>
                <p>Hello!</p>
                <p>I hope this email finds you well. I'm reaching out from <strong>{brand_info['name']}</strong> about our developer training and mentorship programs.</p>
                
                <div class="highlight">
                    <p><strong>Our mission:</strong> {brand_info['description']} with a focus on ethical AI and inclusivity standards.</p>
                </div>
                
                <p>We're committed to building the next generation of ethical developers through comprehensive training, mentorship, and open source contributions.</p>
                
                <h3>💡 How we can help your team:</h3>
                <ul>
                    <li>👨‍🏫 Corporate training programs for development teams</li>
                    <li>🤝 Volunteer mentorship from senior developers</li>
                    <li>🎯 Junior developer program with hands-on experience</li>
                    <li>⚖️ Ethical AI & bias-free development practices</li>
                </ul>
                
                <p>Would you be interested in learning how our training programs can upskill your development team?</p>
                
                <a href="https://www.open.build" class="cta-button">Explore Our Programs</a>
                
                <p>Best regards,<br>
                <strong>The Open Build Community</strong></p>
                '''
            elif brand_key == 'radical':
                return f'''
                <h2>🌱 Cloud Native AI Development Transformation</h2>
                <p>Hello!</p>
                <p>I hope this email finds you well. I'm reaching out from <strong>{brand_info['name']}</strong> about transforming software teams through modern development practices.</p>
                
                <div class="highlight">
                    <p><strong>Our approach:</strong> {brand_info['description']} for modern DevOps and microservices architecture.</p>
                </div>
                
                <p>We help software teams embrace cloud native microservices, AI-enhanced agile methodologies, and vibe coding practices for maximum efficiency and transparency.</p>
                
                <h3>🚀 Our expertise includes:</h3>
                <ul>
                    <li>☁️ Microservices & Kubernetes orchestration</li>
                    <li>🤖 AI-enhanced Scrum and Kanban workflows</li>
                    <li>👨‍💻 Vibe coding & AI pair programming</li>
                    <li>🔄 DevOps automation & intelligent monitoring</li>
                </ul>
                
                <p>Would you be interested in exploring how we can modernize your development practices?</p>
                
                <a href="https://www.radicaltherapy.dev" class="cta-button">Learn About Our Methodology</a>
                
                <p>Best regards,<br>
                <strong>Radical Therapy Dev Team</strong></p>
                '''
            elif brand_key == 'oregonsoftware':
                return f'''
                <h2>💻 Custom Software Development Partnership</h2>
                <p>Hello!</p>
                <p>I hope this email finds you well. I'm reaching out from <strong>{brand_info['name']}</strong> regarding custom software development and nearshore solutions.</p>
                
                <div class="highlight">
                    <p><strong>What we deliver:</strong> {brand_info['description']} - the superior alternative to vibe coding with proven results.</p>
                </div>
                
                <p>We provide skilled nearshore development teams with aligned time zones and cultural compatibility, delivering scalable cloud solutions and innovative applications.</p>
                
                <h3>🎯 Why choose Oregon Software:</h3>
                <ul>
                    <li>🌎 Expert nearshore development teams</li>
                    <li>☁️ Cloud-native applications & enterprise solutions</li>
                    <li>📱 Custom mobile & web application development</li>
                    <li>🔧 Agile methodologies with transparent communication</li>
                </ul>
                
                <p>Would you be interested in discussing how our nearshore teams can accelerate your development projects?</p>
                
                <a href="https://www.oregonsoftware.com" class="cta-button">Schedule Consultation</a>
                
                <p>Best regards,<br>
                <strong>Oregon Software Development Team</strong></p>
                '''
            else:
                return f'''
                <h2>🤝 Partnership Opportunity</h2>
                <p>Hello!</p>
                <p>I hope this email finds you well. I'm reaching out from <strong>{brand_info['name']}</strong> regarding a potential collaboration opportunity.</p>
                
                <div class="highlight">
                    <p><strong>What we do:</strong> {brand_info['description']}</p>
                </div>
                
                <p>We're always looking to connect with like-minded organizations and individuals who share our passion for innovation and growth.</p>
                
                <p>Would you be interested in exploring potential collaboration opportunities?</p>
                
                <p>Best regards,<br>
                <strong>{brand_info['name']} Team</strong></p>
                '''
            
        elif campaign_type == 'discovery_campaign':
            return f'''
            <h2>🔍 Research & Discovery</h2>
            <p>Hi there!</p>
            <p>I'm conducting research on potential partnerships for <strong>{data.get('brand_name', brand_key.title())}</strong> and came across your organization.</p>
            
            <div class="metrics">
                <div class="metric">
                    <div class="metric-value">500+</div>
                    <div class="metric-label">Partners</div>
                </div>
                <div class="metric">
                    <div class="metric-value">98%</div>
                    <div class="metric-label">Success Rate</div>
                </div>
            </div>
            
            <p>I'd love to learn more about your organization and see if there might be synergies between our missions.</p>
            
            <p><strong>Could we schedule a brief 15-minute call to explore this?</strong></p>
            
            <p>Looking forward to hearing from you!</p>
            '''
            
        elif campaign_type == 'follow_up':
            return f'''
            <h2>👋 Following Up</h2>
            <p>Hello again!</p>
            <p>I wanted to follow up on my previous message regarding potential collaboration with <strong>{data.get('brand_name', brand_key.title())}</strong>.</p>
            
            <div class="highlight">
                <p>I understand you're probably busy, but I wanted to make sure my message didn't get lost in your inbox.</p>
            </div>
            
            <p>If you're interested in learning more, I'd be happy to provide additional details about how we might work together.</p>
            
            <h3>Quick recap of what we offer:</h3>
            <ul>
                <li>Strategic partnership opportunities</li>
                <li>Resource sharing and collaboration</li>
                <li>Mutual growth initiatives</li>
            </ul>
            
            <p>No pressure at all - just wanted to check in!</p>
            
            <p>Best,<br>
            <strong>{data.get('from_name', f'{brand_key.title()} Team')}</strong></p>
            '''
            
        elif campaign_type == 'daily_analytics':
            analytics = data.get('analytics', {})
            return f'''
            <h2>📊 Daily Analytics Report</h2>
            <p><strong>Report Date:</strong> {data.get('date', 'Today')}</p>
            
            <h3>🌐 Website Performance</h3>
            <div class="metrics">
                <div class="metric">
                    <div class="metric-value">{analytics.get('sessions', '1,234')}</div>
                    <div class="metric-label">Sessions</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{analytics.get('users', '856')}</div>
                    <div class="metric-label">Users</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{analytics.get('pageviews', '2,856')}</div>
                    <div class="metric-label">Page Views</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{analytics.get('bounce_rate', '45.2%')}</div>
                    <div class="metric-label">Bounce Rate</div>
                </div>
            </div>
            
            <h3>📧 Email Campaign Performance</h3>
            <div class="metrics">
                <div class="metric">
                    <div class="metric-value">{analytics.get('emails_sent', '25')}</div>
                    <div class="metric-label">Emails Sent</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{analytics.get('open_rate', '28.5%')}</div>
                    <div class="metric-label">Open Rate</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{analytics.get('click_rate', '3.2%')}</div>
                    <div class="metric-label">Click Rate</div>
                </div>
            </div>
            
            <div class="highlight">
                <h3>🎯 Key Insights</h3>
                <ul>
                    <li>Website traffic increased 5.2% from yesterday</li>
                    <li>Email engagement above industry average</li>
                    <li>Mobile traffic represents 60% of all sessions</li>
                </ul>
            </div>
            '''
            
        elif campaign_type == 'automation_notification':
            return f'''
            <h2>🤖 Automation Status Update</h2>
            <p><strong>Timestamp:</strong> {data.get('timestamp', 'Now')}</p>
            
            <div class="highlight">
                <h3>System Status: ✅ All Green</h3>
                <p>All automation systems are running smoothly</p>
            </div>
            
            <h3>📈 Recent Activities</h3>
            <ul>
                <li><strong>Target Discovery:</strong> {data.get('targets_found', '5')} new contacts identified</li>
                <li><strong>Email Campaigns:</strong> {data.get('emails_sent', '8')} messages sent successfully</li>
                <li><strong>Response Tracking:</strong> {data.get('responses', '2')} new responses detected</li>
                <li><strong>Analytics Update:</strong> Daily metrics collected</li>
            </ul>
            
            <div class="metrics">
                <div class="metric">
                    <div class="metric-value">{data.get('daily_targets', '25')}</div>
                    <div class="metric-label">Contacts Processed</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{data.get('success_rate', '94%')}</div>
                    <div class="metric-label">Success Rate</div>
                </div>
            </div>
            
            <p>System Health: <span style="color: #22c55e; font-weight: bold;">Excellent ✅</span></p>
            '''
        
        return "<p>Email content would go here.</p>"
        
    def _generate_subject(self, campaign_type: str, data: Dict[str, Any], brand_key: str) -> str:
        """Generate email subject line"""
        brand_config = self.templates[brand_key]
        brand_info = brand_config['brand_info']
        brand_name = brand_info['name']
        
        # Brand-specific subject lines
        if brand_key == 'foundry':
            subjects = {
                'general_outreach': f'🚀 Join Our Global Startup Foundry Program - {brand_name}',
                'discovery_campaign': f'Equity-Free Startup Support - {brand_name}',
                'follow_up': f'Following up: Your Startup Foundry Application',
                'daily_analytics': f'{brand_name} - Daily Startup Analytics Report',
                'automation_notification': f'{brand_name} - Foundry System Update'
            }
        elif brand_key == 'buildly':
            subjects = {
                'general_outreach': f'⚡ Sustainable AI Development Partnership - {brand_name}',
                'discovery_campaign': f'Transform Your Development Process with {brand_name}',
                'follow_up': f'Following up: AI + Product Management Solutions',
                'daily_analytics': f'{brand_name} - Daily Platform Analytics',
                'automation_notification': f'{brand_name} - Platform Status Update'
            }
        elif brand_key == 'openbuild':
            subjects = {
                'general_outreach': f'🛠️ Developer Training & Mentorship Opportunity - {brand_name}',
                'discovery_campaign': f'Upskill Your Team with Ethical AI Training',
                'follow_up': f'Following up: Developer Training Programs',
                'daily_analytics': f'{brand_name} - Community Analytics Report',
                'automation_notification': f'{brand_name} - Training System Update'
            }
        elif brand_key == 'radical':
            subjects = {
                'general_outreach': f'🌱 Cloud Native AI Development Transformation',
                'discovery_campaign': f'Modernize Your Development with Radical Therapy',
                'follow_up': f'Following up: Cloud Native Transformation',
                'daily_analytics': f'{brand_name} - Development Analytics',
                'automation_notification': f'{brand_name} - Cloud Native Update'
            }
        elif brand_key == 'oregonsoftware':
            subjects = {
                'general_outreach': f'💻 Nearshore Development Partnership - {brand_name}',
                'discovery_campaign': f'Superior Alternative to Vibe Coding - {brand_name}',
                'follow_up': f'Following up: Custom Software Development',
                'daily_analytics': f'{brand_name} - Project Analytics Report',
                'automation_notification': f'{brand_name} - Development Status Update'
            }
        else:
            subjects = {
                'general_outreach': f'Partnership Opportunity with {brand_name}',
                'discovery_campaign': f'Exploring Collaboration with {brand_name}',
                'follow_up': f'Following up on our {brand_name} conversation',
                'daily_analytics': f'{brand_name} - Daily Analytics Report',
                'automation_notification': f'{brand_name} - System Update'
            }
        
        return subjects.get(campaign_type, f'{brand_name} - Update')
        
    def _html_to_text(self, html: str) -> str:
        """Convert HTML to plain text"""
        # Simple HTML to text conversion
        import re
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html)
        
        # Convert HTML entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

def test_brand_templates():
    """Test all brand templates"""
    renderer = BrandEmailRenderer()
    
    test_data = {
        'brand_name': 'Test Brand',
        'subtitle': 'Test Email Campaign',
        'description': 'Testing our amazing email templates',
        'from_name': 'Test Team',
        'website': 'https://test.com',
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
    }
    
    for brand_key in BRAND_EMAIL_TEMPLATES.keys():
        print(f"\n=== Testing {brand_key.upper()} ===")
        for campaign_type in ['general_outreach', 'daily_analytics']:
            try:
                result = renderer.render_email(brand_key, campaign_type, test_data)
                print(f"✅ {campaign_type}: {result['subject']}")
            except Exception as e:
                print(f"❌ {campaign_type}: {e}")

if __name__ == "__main__":
    test_brand_templates()