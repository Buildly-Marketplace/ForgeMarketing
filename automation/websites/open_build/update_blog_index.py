#!/usr/bin/env python3
"""
Update the training blog index page with new articles
"""

import os
import sqlite3
import json
from datetime import datetime
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BlogIndexUpdater:
    def __init__(self):
        self.project_dir = Path(__file__).parent.parent
        self.blog_db = self.project_dir / "blog_articles.db"
        self.blog_html = self.project_dir / "training-blog.html"
        
    def get_recent_articles(self, limit=10):
        """Get recent articles from database"""
        if not self.blog_db.exists():
            logger.warning("Blog database not found")
            return []
            
        conn = sqlite3.connect(self.blog_db)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT date, title, category, business_use_case, created_at 
                FROM articles 
                WHERE published = TRUE OR published IS NULL
                ORDER BY date DESC 
                LIMIT ?
            """, (limit,))
            
            articles = []
            for row in cursor.fetchall():
                # Calculate day number based on date
                article_date = datetime.strptime(row[0], '%Y-%m-%d')
                base_date = datetime(2025, 9, 29)  # Starting date
                day_number = (article_date - base_date).days + 1
                
                articles.append({
                    'date': row[0],
                    'title': row[1],
                    'category': row[2],
                    'business_use_case': row[3],
                    'created_at': row[4],
                    'day_number': max(1, day_number),
                    'url': f"blog/articles/day-{day_number}-{row[0]}.html"
                })
            
            return articles
            
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            return []
        finally:
            conn.close()
    
    def generate_article_html(self, articles):
        """Generate HTML for article list"""
        if not articles:
            return """
                <div class="text-center py-8">
                    <p class="text-gray-600 text-lg">No articles available yet.</p>
                    <p class="text-gray-500">Check back tomorrow for our first training article!</p>
                </div>
            """
        
        html = ""
        for article in articles:
            # Format date nicely
            article_date = datetime.strptime(article['date'], '%Y-%m-%d')
            formatted_date = article_date.strftime('%B %d, %Y')
            
            # Truncate business use case for preview
            preview = article['business_use_case'][:120]
            if len(article['business_use_case']) > 120:
                preview += "..."
            
            html += f"""
                <div class="border-b border-gray-200 pb-6 mb-6">
                    <div class="text-sm text-blue-600 font-medium mb-2">
                        DAY {article['day_number']} • {article['category'].upper()}
                    </div>
                    <h3 class="text-xl font-bold mb-3 text-gray-900">
                        <a href="{article['url']}" class="hover:text-blue-600 transition-colors">
                            {article['title']}
                        </a>
                    </h3>
                    <p class="text-gray-600 mb-4">{preview}</p>
                    <div class="flex items-center justify-between text-sm text-gray-500">
                        <div class="flex items-center space-x-4">
                            <span class="flex items-center">
                                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                </svg>
                                {formatted_date}
                            </span>
                            <span class="flex items-center">
                                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                                10 min read
                            </span>
                            <span class="flex items-center">
                                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                                Business Use Case
                            </span>
                        </div>
                        <a href="{article['url']}" class="text-blue-600 hover:text-blue-800 font-medium">
                            Read Article →
                        </a>
                    </div>
                </div>
            """
        
        return html
    
    def update_blog_page(self):
        """Update the training blog HTML page"""
        if not self.blog_html.exists():
            logger.error("Training blog HTML file not found")
            return False
        
        # Get recent articles
        articles = self.get_recent_articles(15)
        logger.info(f"Found {len(articles)} articles to display")
        
        # Generate article HTML
        articles_html = self.generate_article_html(articles)
        
        # Read current HTML
        with open(self.blog_html, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace the articles container
        start_marker = '<!-- Articles will be dynamically inserted here -->'
        end_marker = '<div class="text-center">'
        
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker)
        
        if start_idx == -1 or end_idx == -1:
            logger.error("Could not find article insertion markers in HTML")
            return False
        
        # Replace the content between markers
        new_content = (
            content[:start_idx + len(start_marker)] +
            f'\n                    <div id="articles-container">\n{articles_html}\n                    </div>\n                    ' +
            content[end_idx:]
        )
        
        # Update article count in sidebar
        total_articles = len(articles)
        
        # Update category counts (this is just for display, could be more sophisticated)
        category_counts = {}
        for article in articles:
            category = article['category'].title()
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Write updated HTML
        with open(self.blog_html, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        logger.info("Blog index page updated successfully")
        return True
    
    def generate_rss_feed(self):
        """Generate RSS feed for the blog (optional)"""
        articles = self.get_recent_articles(20)
        
        rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>Open Build Training Blog</title>
        <description>Daily technical articles on cloud native development with AI assistance</description>
        <link>https://open.build/training-blog.html</link>
        <lastBuildDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S %Z')}</lastBuildDate>
        <generator>Open Build Blog System</generator>
"""
        
        for article in articles:
            article_date = datetime.strptime(article['date'], '%Y-%m-%d')
            pub_date = article_date.strftime('%a, %d %b %Y 08:00:00 GMT')
            
            rss_content += f"""        <item>
            <title>{article['title']}</title>
            <description>{article['business_use_case']}</description>
            <link>https://open.build/{article['url']}</link>
            <category>{article['category']}</category>
            <pubDate>{pub_date}</pubDate>
            <guid>https://open.build/{article['url']}</guid>
        </item>
"""
        
        rss_content += """    </channel>
</rss>"""
        
        # Save RSS feed
        rss_path = self.project_dir / "blog" / "feed.xml"
        rss_path.parent.mkdir(exist_ok=True)
        
        with open(rss_path, 'w', encoding='utf-8') as f:
            f.write(rss_content)
        
        logger.info("RSS feed generated")

def main():
    """Main function"""
    updater = BlogIndexUpdater()
    
    try:
        success = updater.update_blog_page()
        if success:
            logger.info("Blog page updated successfully")
            
            # Also generate RSS feed
            updater.generate_rss_feed()
        else:
            logger.error("Failed to update blog page")
            return 1
            
    except Exception as e:
        logger.error(f"Error updating blog: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())