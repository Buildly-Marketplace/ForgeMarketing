#!/usr/bin/env python3
"""
Automated Article Publication System
====================================

Monitors for new blog articles and automatically posts to social media platforms.
Supports multiple brands and platforms: LinkedIn, Bluesky, Mastodon.

Features:
- Detects new articles from blog directories
- Generates platform-specific social media content
- Posts to multiple platforms simultaneously  
- Tracks publication history to avoid duplicates
- Provides detailed logging of all activities
"""

import os
import sys
import asyncio
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import hashlib
import time
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from automation.social.social_media_manager import SocialMediaManager
    SOCIAL_AVAILABLE = True
except ImportError:
    SOCIAL_AVAILABLE = False

class ArticlePublicationSystem:
    """Automated system for publishing articles to social media"""
    
    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.setup_logging()
        self.publication_history_file = self.project_root / 'logs' / 'publication_history.json'
        self.load_publication_history()
        
        # Initialize social media manager
        if SOCIAL_AVAILABLE:
            self.social_manager = SocialMediaManager()
        else:
            self.logger.warning("Social media manager not available")
            self.social_manager = None
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = self.project_root / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'article_publication.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('article_publisher')
    
    def load_publication_history(self):
        """Load history of published articles to avoid duplicates"""
        try:
            if self.publication_history_file.exists():
                with open(self.publication_history_file, 'r') as f:
                    self.publication_history = json.load(f)
            else:
                self.publication_history = {}
            
            self.logger.info(f"📚 Loaded publication history: {len(self.publication_history)} articles")
            
        except Exception as e:
            self.logger.error(f"Error loading publication history: {e}")
            self.publication_history = {}
    
    def save_publication_history(self):
        """Save publication history to file"""
        try:
            with open(self.publication_history_file, 'w') as f:
                json.dump(self.publication_history, f, indent=2, default=str)
            
        except Exception as e:
            self.logger.error(f"Error saving publication history: {e}")
    
    def get_article_directories(self) -> Dict[str, Path]:
        """Get article directories for each brand"""
        directories = {}
        
        # Website directories
        websites_dir = self.project_root / 'websites'
        if websites_dir.exists():
            for brand_dir in websites_dir.iterdir():
                if brand_dir.is_dir():
                    # Look for blog/articles directories
                    for subdir in ['blog', 'articles', 'posts']:
                        article_dir = brand_dir / subdir
                        if article_dir.exists():
                            directories[brand_dir.name.replace('-website', '')] = article_dir
                            break
        
        # Automation website directories
        automation_dir = self.project_root / 'automation' / 'websites'
        if automation_dir.exists():
            for brand_dir in automation_dir.iterdir():
                if brand_dir.is_dir():
                    for subdir in ['blog', 'articles', 'posts']:
                        article_dir = brand_dir / subdir
                        if article_dir.exists():
                            brand_name = brand_dir.name
                            if brand_name not in directories:
                                directories[brand_name] = article_dir
                            break
        
        self.logger.info(f"📁 Found article directories: {list(directories.keys())}")
        return directories
    
    def scan_for_new_articles(self, hours_back: int = 24) -> List[Dict[str, Any]]:
        """Scan for new articles published in the last N hours"""
        new_articles = []
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        directories = self.get_article_directories()
        
        for brand, article_dir in directories.items():
            try:
                # Scan for HTML files (articles)
                for article_file in article_dir.glob('*.html'):
                    # Check modification time
                    mtime = datetime.fromtimestamp(article_file.stat().st_mtime)
                    
                    if mtime > cutoff_time:
                        # Generate unique article ID
                        article_id = self.generate_article_id(article_file)
                        
                        # Check if already published
                        if article_id not in self.publication_history:
                            article_info = self.extract_article_info(article_file, brand)
                            if article_info:
                                article_info['id'] = article_id
                                article_info['file_path'] = str(article_file)
                                article_info['modified_time'] = mtime
                                new_articles.append(article_info)
                
            except Exception as e:
                self.logger.error(f"Error scanning {brand} articles: {e}")
        
        self.logger.info(f"🆕 Found {len(new_articles)} new articles")
        return new_articles
    
    def generate_article_id(self, article_file: Path) -> str:
        """Generate unique ID for an article based on path and content"""
        content_hash = hashlib.md5(str(article_file).encode()).hexdigest()
        return f"{article_file.stem}_{content_hash[:8]}"
    
    def extract_article_info(self, article_file: Path, brand: str) -> Optional[Dict[str, Any]]:
        """Extract article information from HTML file"""
        try:
            with open(article_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title (simple HTML parsing)
            title = self.extract_html_title(content)
            if not title:
                title = article_file.stem.replace('-', ' ').replace('_', ' ').title()
            
            # Extract description/excerpt
            description = self.extract_html_description(content)
            
            # Generate article URL (assuming it matches the file structure)
            article_url = self.generate_article_url(article_file, brand)
            
            return {
                'title': title,
                'description': description,
                'url': article_url,
                'brand': brand,
                'filename': article_file.name
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting info from {article_file}: {e}")
            return None
    
    def extract_html_title(self, content: str) -> Optional[str]:
        """Extract title from HTML content"""
        import re
        
        # Try various title patterns
        patterns = [
            r'<title[^>]*>([^<]+)</title>',
            r'<h1[^>]*>([^<]+)</h1>',
            r'<meta\s+property="og:title"\s+content="([^"]+)"',
            r'<meta\s+name="title"\s+content="([^"]+)"'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def extract_html_description(self, content: str) -> Optional[str]:
        """Extract description from HTML content"""
        import re
        
        patterns = [
            r'<meta\s+name="description"\s+content="([^"]+)"',
            r'<meta\s+property="og:description"\s+content="([^"]+)"',
            r'<p[^>]*>([^<]{50,200})</p>'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                desc = match.group(1).strip()
                if len(desc) > 50:  # Ensure it's substantive
                    return desc[:200] + ('...' if len(desc) > 200 else '')
        
        return None
    
    def generate_article_url(self, article_file: Path, brand: str) -> str:
        """Generate public URL for the article"""
        # Load brand URLs from database
        import sys
        sys.path.insert(0, str(self.project_root))
        
        from config.brand_loader import get_brand_details
        
        brand_data = get_brand_details(brand)
        base_url = brand_data.get('website_url', f'https://{brand}.com') if brand_data else f'https://{brand}.com'
        
        # Assume articles are in /blog/ path
        article_name = article_file.stem
        return f"{base_url}/blog/{article_name}.html"
    
    def generate_social_content(self, article: Dict[str, Any], platform: str) -> str:
        """Generate platform-specific social media content with AI-optimized formatting"""
        title = article['title']
        description = article.get('description', '')
        url = article['url']
        brand = article['brand']
        
        # Brand-specific messaging
        brand_context = self._get_brand_context(brand)
        
        # Platform-specific content generation with enhanced AI
        if platform == 'twitter':
            # Twitter/X: Concise with hashtags (280 chars)
            content = f"🚀 New article: {title}\n\n{url}"
            if len(content) > 250:  # Leave room for hashtags
                content = f"🚀 {title}\n\n{url}"
            
        elif platform == 'linkedin':
            # LinkedIn: Professional, detailed, engagement-focused (3000 chars max)
            content = self._generate_linkedin_content(title, description, url, brand, brand_context)
            
        elif platform == 'bluesky':
            # Bluesky: Conversational, community-focused (300 chars)
            content = self._generate_bluesky_content(title, description, url, brand, brand_context)
            
        elif platform == 'mastodon':
            # Mastodon: Community-focused, hashtag-rich (500 chars)
            content = self._generate_mastodon_content(title, description, url, brand, brand_context)
            
        else:
            # Default format
            content = f"New article: {title}\n{url}"
        
        return content
    
    def _get_brand_context(self, brand: str) -> Dict[str, str]:
        """Get brand-specific context for content generation"""
        # Load brand data from database
        import sys
        sys.path.insert(0, str(self.project_root))
        
        from config.brand_loader import get_brand_details
        
        brand_data = get_brand_details(brand)
        
        if brand_data:
            return {
                'tone': 'professional',
                'focus': brand_data.get('description', 'technology and innovation'),
                'audience': 'tech professionals',
                'hashtags': f"#{brand} #tech",
                'emoji': '🚀',
                'call_to_action': f"Learn more about {brand_data.get('display_name', brand)}"
            }
        
        # Default fallback
        return {
            'tone': 'professional',
            'focus': 'technology and innovation',
            'audience': 'tech professionals',
            'hashtags': f'#{brand.replace("-", "")} #tech #innovation',
            'emoji': '📖',
            'call_to_action': 'Read more about this topic'
        }
    
    def _generate_linkedin_content(self, title: str, description: str, url: str, brand: str, context: Dict[str, str]) -> str:
        """Generate LinkedIn-optimized content"""
        emoji = context.get('emoji', '📖')
        cta = context.get('call_to_action', 'Learn more')
        hashtags = context.get('hashtags', f'#{brand} #tech')
        
        # LinkedIn hook patterns
        hooks = [
            f"{emoji} {title}",
            f"🔍 What if I told you: {title.lower()}",
            f"💭 Key insight: {title}",
            f"🎯 New perspective: {title}"
        ]
        
        # Choose hook based on title characteristics
        if '?' in title:
            hook = f"{emoji} {title}"
        elif any(word in title.lower() for word in ['how', 'why', 'what', 'when']):
            hook = f"🔍 {title}"
        else:
            hook = f"{emoji} New article: {title}"
        
        # Build content
        content = f"{hook}\n\n"
        
        if description:
            # Add description with line breaks for readability
            content += f"{description}\n\n"
        
        # Add value proposition based on brand
        if brand == 'buildly':
            content += "� For development teams looking to accelerate their cloud-native journey.\n\n"
        elif brand == 'open-build':
            content += "🌟 Essential reading for the open source community.\n\n"
        elif brand == 'radical':
            content += "💡 Transform how your team works together.\n\n"
        
        content += f"👉 {cta}: {url}\n\n"
        content += f"{hashtags}"
        
        # Ensure within LinkedIn limits (3000 chars)
        if len(content) > 2900:
            # Trim description if too long
            content = f"{hook}\n\n{cta}: {url}\n\n{hashtags}"
        
        return content
    
    def _generate_bluesky_content(self, title: str, description: str, url: str, brand: str, context: Dict[str, str]) -> str:
        """Generate Bluesky-optimized content"""
        emoji = context.get('emoji', '✨')
        
        # Bluesky is more casual and conversational
        starters = [
            f"{emoji} Just dropped:",
            f"{emoji} Fresh from the blog:",
            f"{emoji} New post is live:",
            f"{emoji} Latest thoughts:"
        ]
        
        starter = starters[hash(title) % len(starters)]
        content = f"{starter} {title}\n\n"
        
        # Add short description if available and fits
        if description and len(description) < 80:
            content += f"{description}\n\n"
        
        content += f"🔗 {url}"
        
        # Ensure within Bluesky limits (300 chars)
        if len(content) > 290:
            content = f"{starter} {title}\n\n🔗 {url}"
        
        return content
    
    def _generate_mastodon_content(self, title: str, description: str, url: str, brand: str, context: Dict[str, str]) -> str:
        """Generate Mastodon-optimized content"""
        emoji = context.get('emoji', '📝')
        hashtags = context.get('hashtags', f'#{brand} #tech')
        
        # Mastodon values community and hashtags
        content = f"{emoji} New blog post: {title}\n\n"
        
        if description:
            # Truncate description if needed
            desc = description[:150] + "..." if len(description) > 150 else description
            content += f"{desc}\n\n"
        
        content += f"🔗 {url}\n\n{hashtags}"
        
        # Ensure within Mastodon comfortable limits (500 chars)
        if len(content) > 480:
            content = f"{emoji} {title}\n\n🔗 {url}\n\n{hashtags}"
        
        return content
    
    async def publish_article_to_social(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Publish a single article to all configured social media platforms"""
        if not self.social_manager:
            return {'success': False, 'error': 'Social media manager not available'}
        
        brand = article['brand']
        results = {}
        
        # Define platforms to post to (customize per brand if needed)
        platforms = ['linkedin', 'bluesky', 'mastodon']
        
        self.logger.info(f"📢 Publishing '{article['title']}' for {brand} to {platforms}")
        
        for platform in platforms:
            try:
                content = self.generate_social_content(article, platform)
                
                # Post to platform
                result = await self.social_manager.cross_platform_post(
                    content=content,
                    platforms=[platform],
                    brand=brand
                )
                
                # Extract result for this platform
                platform_results = result.get('results', [])
                platform_result = next((r for r in platform_results if r.get('platform') == platform), 
                                     {'success': False, 'error': 'No result'})
                results[platform] = platform_result
                
                # Add delay between posts to avoid rate limiting
                await asyncio.sleep(2)
                
            except Exception as e:
                self.logger.error(f"Error posting to {platform}: {e}")
                results[platform] = {'success': False, 'error': str(e)}
        
        # Record publication
        self.publication_history[article['id']] = {
            'article': article,
            'published_at': datetime.now().isoformat(),
            'platforms': results
        }
        
        self.save_publication_history()
        
        successful_platforms = [p for p, r in results.items() if r.get('success')]
        self.logger.info(f"✅ Published to {len(successful_platforms)}/{len(platforms)} platforms")
        
        return {
            'success': len(successful_platforms) > 0,
            'platforms': results,
            'successful_platforms': successful_platforms
        }
    
    async def run_publication_cycle(self, hours_back: int = 24):
        """Run a complete publication cycle"""
        self.logger.info("🚀 Starting article publication cycle")
        
        # Scan for new articles
        new_articles = self.scan_for_new_articles(hours_back)
        
        if not new_articles:
            self.logger.info("📰 No new articles found")
            return
        
        # Publish each article
        results = []
        for article in new_articles:
            try:
                result = await self.publish_article_to_social(article)
                results.append({
                    'article': article['title'],
                    'brand': article['brand'],
                    'result': result
                })
                
                # Delay between articles
                await asyncio.sleep(5)
                
            except Exception as e:
                self.logger.error(f"Error publishing {article['title']}: {e}")
                results.append({
                    'article': article['title'],
                    'brand': article['brand'],
                    'result': {'success': False, 'error': str(e)}
                })
        
        # Summary
        successful = sum(1 for r in results if r['result']['success'])
        self.logger.info(f"📊 Publication cycle complete: {successful}/{len(results)} articles published successfully")
        
        return results

async def main():
    """Main function for testing and running the publication system"""
    publisher = ArticlePublicationSystem()
    
    # Run publication cycle
    results = await publisher.run_publication_cycle(hours_back=48)  # Check last 48 hours
    
    if results:
        print("\n=== PUBLICATION RESULTS ===")
        for result in results:
            status = "✅" if result['result']['success'] else "❌"
            print(f"{status} {result['article']} ({result['brand']})")
            if result['result'].get('successful_platforms'):
                platforms = ', '.join(result['result']['successful_platforms'])
                print(f"   Published to: {platforms}")

if __name__ == "__main__":
    asyncio.run(main())