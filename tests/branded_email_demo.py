#!/usr/bin/env python3
"""
Branded Email Template Demo
Example usage of the branded email template system
"""

from email_templates import BrandEmailRenderer

def demo_branded_emails():
    """Demonstrate how to use the branded email templates"""
    renderer = BrandEmailRenderer()
    
    print("🎨 Branded Email Template System Demo")
    print("=" * 50)
    
    # Example 1: General outreach email for Buildly
    print("\n📧 Example 1: Buildly Partnership Proposal")
    buildly_email = renderer.render_email(
        'buildly', 
        'general_outreach',
        {
            'recipient_name': 'potential partner',
            'custom_message': 'We believe Buildly could be perfect for your team',
            'unsubscribe_url': 'https://buildly.io/unsubscribe'
        }
    )
    print(f"Subject: {buildly_email['subject']}")
    print("✅ HTML email generated with Buildly branding")
    
    # Example 2: Analytics report for Open Build
    print("\n📊 Example 2: Open Build Analytics Report")
    openbuild_email = renderer.render_email(
        'openbuild',
        'daily_analytics',
        {
            'metrics_data': {
                'active_users': 2300,
                'new_projects': 156,
                'success_rate': 89
            },
            'date': '2025-01-01',
            'unsubscribe_url': 'https://open.build/unsubscribe'
        }
    )
    print(f"Subject: {openbuild_email['subject']}")
    print("✅ HTML email generated with Open Build branding")
    
    # Example 3: Foundry program invitation
    print("\n🚀 Example 3: Foundry Program Invitation")
    foundry_email = renderer.render_email(
        'foundry',
        'general_outreach',
        {
            'recipient_name': 'startup founder',
            'custom_message': 'Your innovative approach caught our attention',
            'unsubscribe_url': 'https://firstcityfoundry.com/unsubscribe'
        }
    )
    print(f"Subject: {foundry_email['subject']}")
    print("✅ HTML email generated with Foundry branding")
    
    print("\n🎉 All branded email templates are working perfectly!")
    print("\n📋 Available brands:", list(renderer.templates.keys()))
    print("📋 Available email types: general_outreach, daily_analytics")
    
    # Show brand comparison
    print("\n🎨 Brand Identity Comparison:")
    for brand, template in renderer.templates.items():
        colors = template['colors']
        print(f"• {template['brand_info']['name']}: {colors['primary']} (primary) | {template['brand_info']['tagline']}")

if __name__ == "__main__":
    demo_branded_emails()