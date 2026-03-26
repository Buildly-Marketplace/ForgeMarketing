#!/usr/bin/env python3
"""
Test Ollama AI Integration
Tests connection and content generation with local Ollama instance
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from automation.ai.ollama_integration import OllamaClient, AIContentGenerator
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure to install required packages:")
    print("pip install aiohttp pyyaml")
    sys.exit(1)

async def test_ollama_connection():
    """Test basic Ollama connection and model availability"""
    print("🔌 Testing Ollama Connection")
    print("-" * 40)
    
    client = OllamaClient("http://pop-os2.local:11434")
    
    # Test connection
    connected = await client.test_connection()
    if not connected:
        print("❌ Failed to connect to Ollama at pop-os2.local:11434")
        print("\nTroubleshooting:")
        print("1. Make sure Ollama is running on pop-os2.local")
        print("2. Check if port 11434 is accessible")
        print("3. Try: curl http://pop-os2.local:11434/api/tags")
        return False
    
    # List available models
    print("\n📋 Available Models:")
    models = await client.list_models()
    if not models:
        print("❌ No models found. Install a model first:")
        print("ollama pull llama3.1")
        return False
    
    for model in models:
        model_name = model.get('name', 'Unknown')
        model_size = model.get('size', 0)
        size_gb = model_size / (1024**3) if model_size > 0 else 0
        print(f"  ✅ {model_name} ({size_gb:.1f}GB)")
    
    return True

async def test_basic_generation():
    """Test basic text generation"""
    print("\n🧠 Testing Basic AI Generation")
    print("-" * 40)
    
    client = OllamaClient("http://pop-os2.local:11434")
    
    # Simple test prompt
    test_prompt = "Write a brief introduction to AI in software development in 2-3 sentences."
    
    print(f"Prompt: {test_prompt}")
    print("Generating...")
    
    response = await client.generate(
        model="llama3.2:1b",
        prompt=test_prompt,
        temperature=0.7,
        max_tokens=200
    )
    
    if response:
        print(f"\n✅ Generated Response ({len(response)} characters):")
        print("-" * 30)
        print(response)
        print("-" * 30)
        return True
    else:
        print("❌ No response generated")
        return False

async def test_brand_content_generation():
    """Test brand-specific content generation"""
    print("\n🎨 Testing Brand-Specific Content Generation")  
    print("-" * 50)
    
    generator = AIContentGenerator("http://pop-os2.local:11434")
    
    # Test blog post generation
    print("📝 Generating Buildly blog post...")
    try:
        blog_post = await generator.generate_blog_post(
            brand="buildly",
            topic="5 Ways AI Can Improve Your Development Workflow",
            target_audience="developers and product managers"
        )
        
        print(f"✅ Blog Post Generated:")
        print(f"   Title: {blog_post['title']}")
        print(f"   Word Count: {blog_post['word_count']}")
        print(f"   Model: {blog_post['model_used']}")
        print(f"   Preview: {blog_post['content'][:200]}...")
        
    except Exception as e:
        print(f"❌ Blog post generation failed: {e}")
        return False
    
    # Test social media generation
    print(f"\n📱 Generating social media post...")
    try:
        social_post = await generator.generate_social_post(
            brand="buildly",
            content_type="educational", 
            platform="twitter"
        )
        
        print(f"✅ Social Post Generated:")
        print(f"   Platform: {social_post['platform']}")
        print(f"   Type: {social_post['content_type']}")
        print(f"   Length: {social_post['character_count']} chars")
        print(f"   Content: {social_post['content']}")
        
    except Exception as e:
        print(f"❌ Social post generation failed: {e}")
        return False
    
    # Test outreach email generation
    print(f"\n📧 Generating outreach email...")
    try:
        outreach = await generator.generate_outreach_email(
            brand="buildly",
            recipient_info={
                'name': 'Alex Johnson',
                'company': 'TechStartup Inc',
                'industry': 'SaaS Development',
                'pain_points': ['scaling development team', 'code quality consistency']
            },
            campaign_type="partnership"
        )
        
        print(f"✅ Outreach Email Generated:")
        print(f"   Subject: {outreach['subject']}")
        print(f"   Word Count: {outreach['word_count']}")
        print(f"   Preview: {outreach['body'][:200]}...")
        
    except Exception as e:
        print(f"❌ Outreach email generation failed: {e}")
        return False
    
    return True

async def test_performance_metrics():
    """Test generation speed and performance"""
    print("\n⚡ Testing Performance Metrics")
    print("-" * 35)
    
    client = OllamaClient("http://pop-os2.local:11434")
    
    import time
    
    # Test different generation sizes
    test_cases = [
        ("Short (Tweet)", "Write a tweet about AI in development", 100),
        ("Medium (Email)", "Write a professional outreach email about AI development tools", 300),
        ("Long (Blog intro)", "Write a comprehensive introduction to AI-powered development workflows", 800)
    ]
    
    for test_name, prompt, max_tokens in test_cases:
        print(f"\n🏃 {test_name} (max {max_tokens} tokens)")
        
        start_time = time.time()
        response = await client.generate(
            model="llama3.2:1b",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.7
        )
        end_time = time.time()
        
        if response:
            generation_time = end_time - start_time
            chars_generated = len(response)
            words_generated = len(response.split())
            
            print(f"   ✅ Generated in {generation_time:.2f}s")
            print(f"   📊 {chars_generated} chars, {words_generated} words")
            print(f"   🚀 {words_generated/generation_time:.1f} words/second")
        else:
            print(f"   ❌ Generation failed")

async def main():
    """Run all tests"""
    print("🧪 Ollama AI Integration Test Suite")
    print("=" * 50)
    
    # Test 1: Connection
    connected = await test_ollama_connection()
    if not connected:
        print("\n❌ Cannot proceed without Ollama connection")
        return
    
    # Test 2: Basic generation
    basic_works = await test_basic_generation()
    if not basic_works:
        print("\n❌ Basic generation failed")
        return
    
    # Test 3: Brand-specific content
    brand_works = await test_brand_content_generation()
    if not brand_works:
        print("\n⚠️  Brand content generation had issues, but basic functionality works")
    
    # Test 4: Performance
    await test_performance_metrics()
    
    # Summary
    print("\n🎉 Test Summary")
    print("=" * 30)
    print(f"✅ Ollama Connection: {'Working' if connected else 'Failed'}")
    print(f"✅ Basic Generation: {'Working' if basic_works else 'Failed'}")
    print(f"✅ Brand Content: {'Working' if brand_works else 'Needs Configuration'}")
    print("\n🚀 Ollama integration is ready for marketing automation!")
    
    if brand_works:
        print("\n💡 Next Steps:")
        print("1. Run setup_automation.py to initialize the full system")
        print("2. Configure brand templates in templates/brands/")
        print("3. Test unified content generation dashboard")
        print("4. Set up automated content scheduling")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        print("Check your Python environment and Ollama installation")