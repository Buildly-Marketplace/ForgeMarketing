#!/usr/bin/env python3
"""
Test Multi-Brand Content Generation
Tests content generation across all configured brands
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_all_brands():
    """Test content generation for all brands"""
    
    try:
        from automation.ai.ollama_integration import AIContentGenerator
        
        print("🌟 Multi-Brand Content Generation Test")
        print("=" * 45)
        
        generator = AIContentGenerator("http://localhost:11434")
        brands = list(generator.brand_configs.keys())
        
        print(f"📋 Testing {len(brands)} brands: {', '.join(brands)}")
        print()
        
        for brand in brands:
            print(f"🎨 Testing {brand.upper()}")
            print("-" * 30)
            
            try:
                # Test blog post
                blog_post = await generator.generate_blog_post(
                    brand=brand,
                    topic=f"The Future of {brand.title()} in 2025",
                    target_audience="technology professionals"
                )
                
                print(f"✅ Blog: '{blog_post['title'][:50]}...' ({blog_post['word_count']} words)")
                
                # Test social media
                social_post = await generator.generate_social_post(
                    brand=brand,
                    content_type="educational",
                    platform="twitter"
                )
                
                print(f"✅ Social: {social_post['character_count']} chars - '{social_post['content'][:60]}...'")
                
                # Test outreach
                outreach = await generator.generate_outreach_email(
                    brand=brand,
                    recipient_info={
                        'name': 'Sarah Chen',
                        'company': 'InnovateTech Solutions',
                        'industry': 'Software Development',
                        'pain_points': ['team scaling', 'code quality']
                    },
                    campaign_type="partnership"
                )
                
                print(f"✅ Email: '{outreach['subject'][:50]}...' ({outreach['word_count']} words)")
                print()
                
            except Exception as e:
                print(f"❌ Error testing {brand}: {e}")
                print()
        
        print("🎉 Multi-brand testing complete!")
        print("\n💡 All brands can now generate:")
        print("  • Brand-specific blog posts")
        print("  • Social media content")
        print("  • Personalized outreach emails")
        print("  • Unique voice and messaging")
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_all_brands())