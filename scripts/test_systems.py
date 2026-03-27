#!/usr/bin/env python3
"""Test all core automation systems for functionality."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("=" * 60)
print("FORGE MARKETING - SYSTEM HEALTH CHECK")
print("=" * 60)

# 1. Module imports
print("\n--- 1. MODULE IMPORTS ---")
import_results = {}
modules = {
    'contacts_manager': 'automation.contacts_manager',
    'multi_brand_outreach': 'automation.multi_brand_outreach',
    'influencer_discovery': 'automation.influencer_discovery',
    'cron_manager': 'automation.centralized_cron_manager',
    'social_media': 'automation.social.social_media_manager',
    'article_publisher': 'automation.article_publisher',
    'ai_ollama': 'automation.ai.ollama_integration',
    'daily_emailer': 'automation.daily_analytics_emailer',
}
for name, mod in modules.items():
    try:
        __import__(mod)
        import_results[name] = True
        print(f"  OK  {name}")
    except Exception as e:
        import_results[name] = False
        print(f"  ERR {name}: {e}")

# 2. Contacts Manager
print("\n--- 2. CONTACTS MANAGER ---")
try:
    from automation.contacts_manager import UnifiedContactsManager
    cm = UnifiedContactsManager()
    print(f"  DB path: {cm.db_path}")
    print(f"  DB exists: {cm.db_path.exists()}")
    contacts = cm.get_contacts(limit=5)
    print(f"  Contacts count: {len(contacts)}")
    stats = cm.get_dashboard_stats()
    print(f"  Dashboard stats: {stats}")
except Exception as e:
    print(f"  ERROR: {e}")

# 3. Multi-Brand Outreach
print("\n--- 3. MULTI-BRAND OUTREACH ---")
try:
    from automation.multi_brand_outreach import MultiBrandOutreachCampaign, BRAND_DISCOVERY_STRATEGIES
    print(f"  Brands configured: {list(BRAND_DISCOVERY_STRATEGIES.keys())}")
    campaign = MultiBrandOutreachCampaign()
    for brand in list(BRAND_DISCOVERY_STRATEGIES.keys())[:2]:
        targets = campaign.get_campaign_targets(brand, limit=3)
        print(f"  {brand}: {len(targets)} targets available")
except Exception as e:
    print(f"  ERROR: {e}")

# 4. Influencer Discovery
print("\n--- 4. INFLUENCER DISCOVERY ---")
try:
    from automation.influencer_discovery import BrandInfluencerDiscovery, BRAND_INFLUENCER_STRATEGIES
    print(f"  Brand strategies: {list(BRAND_INFLUENCER_STRATEGIES.keys())}")
    for brand_key, strategy in list(BRAND_INFLUENCER_STRATEGIES.items())[:2]:
        print(f"  {brand_key}: {strategy.get('name', '?')} - focus: {strategy.get('focus', '?')}")
        print(f"    Keywords: {strategy.get('keywords', [])[:5]}")
        print(f"    Platforms: {strategy.get('platforms', [])}")
except Exception as e:
    print(f"  ERROR: {e}")

# 5. AI Integration
print("\n--- 5. AI INTEGRATION ---")
try:
    from automation.ai.ollama_integration import OllamaClient
    import asyncio
    
    # Check Ollama at localhost
    ollama_url = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    client = OllamaClient(base_url=ollama_url)
    
    async def test_ollama():
        connected = await client.test_connection()
        return connected
    
    loop = asyncio.new_event_loop()
    connected = loop.run_until_complete(test_ollama())
    loop.close()
    
    print(f"  Ollama URL: {ollama_url}")
    print(f"  Connected: {connected}")
except Exception as e:
    print(f"  ERROR: {e}")

# 6. Social Media
print("\n--- 6. SOCIAL MEDIA ---")
try:
    from automation.social.social_media_manager import SocialMediaManager
    sm = SocialMediaManager()
    print(f"  Manager loaded: True")
    print(f"  Platforms configured: {list(sm.platform_configs.keys()) if hasattr(sm, 'platform_configs') else 'N/A'}")
except Exception as e:
    print(f"  ERROR: {e}")

# 7. Cron Manager
print("\n--- 7. CRON SCHEDULING ---")
try:
    from automation.centralized_cron_manager import CentralizedCronManager
    print(f"  CronManager class loaded")
except Exception as e:
    print(f"  ERROR: {e}")

# 8. Email Config
print("\n--- 8. EMAIL CONFIG ---")
try:
    os.environ.pop('DATABASE_URL', None)
    from dashboard.app import app
    from dashboard.models import db, BrandEmailConfig, Brand
    with app.app_context():
        brands = Brand.query.filter_by(is_active=True).all()
        print(f"  Active brands: {[b.name for b in brands]}")
        for b in brands:
            email_cfg = BrandEmailConfig.query.filter_by(brand_id=b.id).first()
            if email_cfg:
                print(f"  {b.name}: provider={email_cfg.provider}, from={email_cfg.from_email}")
            else:
                print(f"  {b.name}: NO email config")
except Exception as e:
    print(f"  ERROR: {e}")

# 9. Data files check
print("\n--- 9. DATA FILES ---")
from pathlib import Path
data_dir = Path(__file__).parent.parent / 'data'
for f in sorted(data_dir.glob('*.db')):
    size_kb = f.stat().st_size / 1024
    print(f"  {f.name}: {size_kb:.1f} KB")

print("\n" + "=" * 60)
print("HEALTH CHECK COMPLETE")
print("=" * 60)
