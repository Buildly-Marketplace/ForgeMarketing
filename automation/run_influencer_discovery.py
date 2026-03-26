#!/usr/bin/env python3
"""
Individual Brand Influencer Discovery Runner
==========================================

Command-line interface for running influencer discovery for specific brands.
Used by cron jobs and manual execution.

Usage:
    python run_influencer_discovery.py --brand foundry
    python run_influencer_discovery.py --all-brands
    python run_influencer_discovery.py --brand buildly --max-per-platform 10
"""

import asyncio
import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from automation.influencer_discovery import BrandInfluencerDiscovery, BRAND_INFLUENCER_STRATEGIES

async def run_brand_discovery(brand: str, max_per_platform: int = 5):
    """Run influencer discovery for a specific brand"""
    discovery = BrandInfluencerDiscovery()
    
    print(f"🔍 Starting influencer discovery for {brand}")
    print(f"📊 Target: {max_per_platform} influencers per platform")
    print("=" * 50)
    
    try:
        results = await discovery.discover_brand_influencers(brand, max_per_platform)
        
        total_discovered = 0
        for platform, influencers in results.items():
            total_discovered += len(influencers)
            print(f"📱 {platform.title()}: {len(influencers)} influencers")
            
            for influencer in influencers:
                print(f"  • {influencer.name} (@{list(influencer.social_profiles.keys())[0]})")
                print(f"    {influencer.total_reach:,} followers | {influencer.avg_engagement_rate:.1f}% engagement")
                print(f"    Alignment: {influencer.brand_alignment_score:.2f}")
        
        print("=" * 50)
        print(f"✅ Discovery complete: {total_discovered} new influencers for {brand}")
        
        return results
        
    except Exception as e:
        print(f"❌ Discovery failed for {brand}: {e}")
        return {}

async def run_all_brands_discovery(max_per_platform: int = 5):
    """Run influencer discovery for all brands"""
    print("🌟 Starting influencer discovery for ALL brands")
    print("=" * 60)
    
    all_results = {}
    total_influencers = 0
    
    for brand_key in BRAND_INFLUENCER_STRATEGIES.keys():
        brand_name = BRAND_INFLUENCER_STRATEGIES[brand_key]['name']
        print(f"\n🎯 {brand_name} ({brand_key})")
        print("-" * 30)
        
        results = await run_brand_discovery(brand_key, max_per_platform)
        all_results[brand_key] = results
        
        brand_total = sum(len(influencers) for influencers in results.values())
        total_influencers += brand_total
        
        # Brief pause between brands
        await asyncio.sleep(2)
    
    print("\n" + "=" * 60)
    print(f"🎊 ALL BRANDS DISCOVERY COMPLETE")
    print(f"📈 Total influencers discovered: {total_influencers}")
    print("=" * 60)
    
    return all_results

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='Social Media Influencer Discovery')
    parser.add_argument('--brand', type=str, help='Specific brand to discover influencers for')
    parser.add_argument('--all-brands', action='store_true', help='Run discovery for all brands')
    parser.add_argument('--max-per-platform', type=int, default=5, help='Maximum influencers per platform')
    parser.add_argument('--list-brands', action='store_true', help='List available brands')
    
    args = parser.parse_args()
    
    if args.list_brands:
        print("📋 Available Brands:")
        for brand_key, strategy in BRAND_INFLUENCER_STRATEGIES.items():
            print(f"  • {brand_key}: {strategy['name']} - {strategy['focus']}")
        return
    
    if args.all_brands:
        asyncio.run(run_all_brands_discovery(args.max_per_platform))
    elif args.brand:
        if args.brand not in BRAND_INFLUENCER_STRATEGIES:
            print(f"❌ Unknown brand: {args.brand}")
            print(f"Available brands: {', '.join(BRAND_INFLUENCER_STRATEGIES.keys())}")
            sys.exit(1)
        
        asyncio.run(run_brand_discovery(args.brand, args.max_per_platform))
    else:
        print("❌ Please specify --brand <brand_name> or --all-brands")
        print("Use --list-brands to see available brands")
        parser.print_help()

if __name__ == "__main__":
    main()