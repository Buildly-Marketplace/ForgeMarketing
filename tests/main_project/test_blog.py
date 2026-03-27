#!/usr/bin/env python3
"""
Simplified Blog Post Generation Test
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_blog_generation():
    """Test blog post generation with detailed debugging"""
    
    try:
        from automation.ai.ollama_integration import AIContentGenerator
        
        print("🔧 Testing Blog Post Generation with Debugging")
        print("=" * 60)
        
        generator = AIContentGenerator()
        print(f"✅ Generator initialized")
        print(f"✅ Brand configs loaded: {list(generator.brand_configs.keys())}")
        
        # Test with Buildly
        brand = "buildly"
        if brand in generator.brand_configs:
            print(f"✅ Found {brand} configuration")
            
            brand_config = generator.brand_configs[brand]
            print(f"Config keys: {list(brand_config.keys())}")
            
            # Test blog post generation
            print(f"\n📝 Generating blog post for {brand}...")
            
            try:
                blog_post = await generator.generate_blog_post(
                    brand=brand,
                    topic="5 Ways AI Can Improve Your Development Workflow",
                    target_audience="developers and product managers"
                )
                
                print(f"✅ Blog Post Generated Successfully!")
                print(f"   Title: {blog_post['title']}")
                print(f"   Word Count: {blog_post['word_count']}")
                print(f"   Content Preview: {blog_post['content'][:200]}...")
                
            except Exception as e:
                print(f"❌ Blog post generation error: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"❌ {brand} configuration not found")
            
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_blog_generation())