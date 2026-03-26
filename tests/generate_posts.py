#!/usr/bin/env python3
"""
Generate Social Media Posts Tool
===============================

Interactive tool to generate AI-optimized social media posts for any article.
Supports multiple platforms with brand-specific messaging and formatting.

Usage:
    python generate_posts.py
    python generate_posts.py --article-url "https://example.com/blog/article.html"
    python generate_posts.py --title "Your Article Title" --brand "buildly"
"""

import asyncio
import argparse
import sys
from pathlib import Path
from typing import Dict, Any

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from automation.article_publisher import ArticlePublicationSystem


class PostGenerator:
    """Interactive post generator for social media platforms"""
    
    def __init__(self):
        self.publisher = ArticlePublicationSystem()
        self.platforms = ['linkedin', 'bluesky', 'mastodon', 'twitter']
    
    def create_article_from_input(self, title: str = None, url: str = None, 
                                 brand: str = None, description: str = None) -> Dict[str, Any]:
        """Create article dict from user input"""
        
        if not title:
            title = input("📝 Article title: ").strip()
        
        if not url:
            url = input("🔗 Article URL: ").strip()
        
        if not brand:
            print("\n🏷️  Available brands: buildly, open-build, radical")
            brand = input("Brand: ").strip().lower()
            if brand not in ['buildly', 'open-build', 'radical']:
                brand = 'buildly'  # default
        
        if not description:
            description = input("📄 Description (optional): ").strip()
        
        return {
            'id': f'manual-{hash(title + url)}',
            'title': title,
            'description': description,
            'url': url,
            'brand': brand,
            'file_path': '/manual/input'
        }
    
    def display_post(self, platform: str, content: str, brand: str):
        """Display a formatted post"""
        brand_colors = {
            'buildly': '🔵',
            'open-build': '🟢', 
            'radical': '🟠'
        }
        
        color = brand_colors.get(brand, '⚪')
        
        print(f"\n{color} {platform.upper()} POST ({len(content)} chars)")
        print("┌" + "─" * 58 + "┐")
        
        lines = content.split('\n')
        for line in lines:
            # Truncate long lines for display
            display_line = line[:54] + "..." if len(line) > 54 else line
            print(f"│ {display_line:<56} │")
        
        print("└" + "─" * 58 + "┘")
    
    async def generate_posts_interactive(self):
        """Interactive post generation"""
        print("🤖 AI Social Media Post Generator")
        print("=" * 50)
        
        # Get article details
        article = self.create_article_from_input()
        
        print(f"\n🎯 Generating posts for: {article['title']}")
        print(f"🏷️  Brand: {article['brand']}")
        print(f"🔗 URL: {article['url']}")
        
        # Generate posts for all platforms
        for platform in self.platforms:
            try:
                content = self.publisher.generate_social_content(article, platform)
                self.display_post(platform, content, article['brand'])
            except Exception as e:
                print(f"❌ Error generating {platform} post: {e}")
        
        # Ask if user wants to copy any post
        print(f"\n📋 Which post would you like to copy? ({'/'.join(self.platforms)}/none)")
        choice = input("Platform: ").strip().lower()
        
        if choice in self.platforms:
            content = self.publisher.generate_social_content(article, choice)
            print(f"\n📄 {choice.upper()} POST CONTENT:")
            print("-" * 30)
            print(content)
            print("-" * 30)
            print("✅ Content ready to copy and paste!")
    
    async def generate_posts_from_args(self, args):
        """Generate posts from command line arguments"""
        article = {
            'id': f'cli-{hash(args.title + args.url)}',
            'title': args.title,
            'description': args.description or '',
            'url': args.url,
            'brand': args.brand,
            'file_path': '/cli/input'
        }
        
        print(f"🤖 Generating posts for: {article['title']}")
        
        platforms = args.platforms.split(',') if args.platforms else self.platforms
        
        for platform in platforms:
            if platform in self.platforms:
                content = self.publisher.generate_social_content(article, platform)
                self.display_post(platform, content, article['brand'])
    
    async def test_sample_posts(self):
        """Generate sample posts for demonstration"""
        sample_articles = [
            {
                'id': 'sample-1',
                'title': 'The Future of Cloud-Native Development',
                'description': 'Exploring cutting-edge trends in containerization, microservices, and serverless architectures.',
                'url': 'https://buildly.io/blog/future-cloud-native.html',
                'brand': 'buildly',
                'file_path': '/sample/1'
            },
            {
                'id': 'sample-2',
                'title': 'Open Source Contribution Best Practices',
                'description': 'A comprehensive guide for developers looking to make meaningful contributions to open source projects.',
                'url': 'https://open.build/blog/contribution-guide.html',
                'brand': 'open-build',
                'file_path': '/sample/2'
            }
        ]
        
        print("🎪 Sample Post Generation")
        print("=" * 40)
        
        for article in sample_articles:
            print(f"\n📝 {article['title']} ({article['brand']})")
            for platform in ['linkedin', 'mastodon']:
                content = self.publisher.generate_social_content(article, platform)
                self.display_post(platform, content, article['brand'])


async def main():
    """Main function with argument parsing"""
    parser = argparse.ArgumentParser(description='Generate AI-optimized social media posts')
    parser.add_argument('--title', help='Article title')
    parser.add_argument('--url', help='Article URL')
    parser.add_argument('--brand', choices=['buildly', 'open-build', 'radical'], help='Brand name')
    parser.add_argument('--description', help='Article description')
    parser.add_argument('--platforms', help='Comma-separated platforms (linkedin,bluesky,mastodon,twitter)')
    parser.add_argument('--sample', action='store_true', help='Generate sample posts')
    
    args = parser.parse_args()
    generator = PostGenerator()
    
    if args.sample:
        await generator.test_sample_posts()
    elif args.title and args.url and args.brand:
        await generator.generate_posts_from_args(args)
    else:
        await generator.generate_posts_interactive()


if __name__ == "__main__":
    asyncio.run(main())