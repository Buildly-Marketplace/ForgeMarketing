#!/usr/bin/env python3
"""
Social Media Article Publisher - Cron Integration
================================================

Integration script for automated article publication to social media.
This script is designed to be run as a cron job or called by the automation system.
"""

import sys
import asyncio
import logging
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from automation.article_publisher import ArticlePublicationSystem

def setup_logging():
    """Setup logging for cron execution"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('social_publisher_cron')

async def run_social_publication():
    """Run the social media publication process"""
    logger = setup_logging()
    
    try:
        logger.info("🚀 Starting automated social media publication")
        
        # Initialize publisher
        publisher = ArticlePublicationSystem()
        
        # Run publication cycle (check last 6 hours for new articles)
        results = await publisher.run_publication_cycle(hours_back=6)
        
        if results:
            successful = sum(1 for r in results if r['result']['success'])
            logger.info(f"✅ Published {successful}/{len(results)} articles to social media")
            
            # Log details
            for result in results:
                if result['result']['success']:
                    platforms = result['result'].get('successful_platforms', [])
                    logger.info(f"📱 '{result['article']}' → {', '.join(platforms)}")
                else:
                    logger.error(f"❌ Failed to publish '{result['article']}': {result['result'].get('error')}")
        else:
            logger.info("📰 No new articles found for publication")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Social media publication failed: {e}")
        return False

def main():
    """Main entry point for cron execution"""
    success = asyncio.run(run_social_publication())
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()