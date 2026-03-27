#!/usr/bin/env python3
"""
Marketing Automation Setup Script - Complete Version
Complete initialization and configuration for the unified marketing system
"""

import os
import sys
import asyncio
from pathlib import Path
import subprocess
import yaml

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def print_banner():
    """Print setup banner"""
    print("🚀 Marketing Automation System Setup")
    print("=" * 50)
    print("Unified AI-powered marketing automation for:")
    print("  • Buildly - AI product development platform")
    print("  • The Foundry - Startup incubator")
    print("  • Open Build - Developer community")
    print("  • Radical Therapy - Programming methodology")
    print()

def check_requirements():
    """Check system requirements"""
    print("🔍 Checking System Requirements")
    print("-" * 30)
    
    # Check Python version
    python_version = sys.version_info
    if python_version >= (3, 8):
        print(f"✅ Python {python_version.major}.{python_version.minor}")
    else:
        print(f"❌ Python {python_version.major}.{python_version.minor} - Need Python 3.8+")
        return False
    
    # Check if Ollama is accessible
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama connection ({len(models)} models available)")
        else:
            print("❌ Ollama not accessible at localhost:11434")
            print("   Make sure Ollama is running and accessible")
            return False
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        return False
    
    # Check required packages
    required_packages = ['aiohttp', 'yaml', 'requests', 'pathlib']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'yaml':
                import yaml
            elif package == 'pathlib':
                import pathlib
            elif package == 'aiohttp':
                import aiohttp
            elif package == 'requests':
                import requests
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - missing")
            missing_packages.append(package if package != 'yaml' else 'pyyaml')
    
    if missing_packages:
        print(f"\n📦 Install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All requirements met!")
    return True

def create_directory_structure():
    """Create complete directory structure"""
    print("\n📁 Creating Directory Structure")
    print("-" * 30)
    
    directories = [
        # Core automation directories
        'automation',
        'automation/ai',
        'automation/social_media',
        'automation/outreach',
        'automation/analytics',
        'automation/scheduling',
        
        # Data directories
        'data',
        'data/analytics',
        'data/contacts',
        'data/campaigns',
        'data/content',
        
        # Configuration
        'config',
        'config/secrets',
        
        # Templates
        'templates',
        'templates/brands',
        'templates/brands/buildly',
        'templates/brands/foundry',
        'templates/brands/open_build',
        'templates/brands/radical_therapy',
        'templates/email',
        'templates/social',
        'templates/blog',
        
        # Reports and logs
        'reports',
        'logs',
        
        # Dashboard and web interface
        'dashboard',
        'dashboard/static',
        'dashboard/templates',
    ]
    
    for directory in directories:
        dir_path = project_root / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {directory}")
        else:
            print(f"📁 Exists: {directory}")

async def test_ai_integration():
    """Test AI integration"""
    print("\n🧠 Testing AI Integration")
    print("-" * 25)
    
    try:
        from automation.ai.ollama_integration import OllamaClient, AIContentGenerator
        
        # Test Ollama connection
        client = OllamaClient("http://localhost:11434")
        connected = await client.test_connection()
        
        if connected:
            print("✅ Ollama connection successful")
            
            # Test content generation
            generator = AIContentGenerator("http://localhost:11434")
            brands = list(generator.brand_configs.keys())
            
            if brands:
                print(f"✅ Brand configurations loaded: {', '.join(brands)}")
                
                # Test quick generation
                try:
                    content = await client.generate(
                        model="llama3.2:1b",
                        prompt="Write a one sentence description of AI in software development.",
                        max_tokens=50
                    )
                    if content:
                        print("✅ AI content generation working")
                        return True
                    else:
                        print("❌ AI content generation failed")
                        return False
                except Exception as e:
                    print(f"❌ AI generation error: {e}")
                    return False
            else:
                print("⚠️  No brand configurations found")
                return False
        else:
            print("❌ Ollama connection failed")
            return False
            
    except Exception as e:
        print(f"❌ AI integration error: {e}")
        return False

def create_brand_configurations():
    """Create missing brand configurations"""
    print("\n🎨 Setting Up Brand Configurations")
    print("-" * 35)
    
    brands_to_create = [
        {
            'name': 'foundry',
            'display_name': 'The Foundry',
            'description': 'Startup incubator with proven outreach system',
            'focus': 'startup acceleration and mentorship'
        },
        {
            'name': 'open_build',
            'display_name': 'Open Build',
            'description': 'Community-focused platform for developer tutorials',
            'focus': 'open source development and education'
        },
        {
            'name': 'radical_therapy',
            'display_name': 'Radical Therapy',
            'description': 'Programming methodology with developer humor',
            'focus': 'development philosophy and best practices'
        }
    ]
    
    for brand in brands_to_create:
        config_path = project_root / f"templates/brands/{brand['name']}/brand_config.yaml"
        
        if not config_path.exists():
            print(f"📝 Creating {brand['display_name']} configuration...")
            
            config = {
                'brand': {
                    'name': brand['display_name'],
                    'tagline': f"Professional {brand['focus']}",
                    'description': brand['description'],
                    'website': f"https://www.{brand['name']}.io"
                },
                'voice': {
                    'tone': ['professional', 'helpful', 'expert'],
                    'style': ['clear', 'informative', 'engaging'],
                    'personality': ['knowledgeable', 'approachable', 'innovative']
                },
                'key_messages': {
                    'primary': f"Leading solutions in {brand['focus']}",
                    'secondary': f"Empowering teams with {brand['focus']} expertise"
                },
                'target_audience': {
                    'primary': ['developers', 'product managers', 'tech leads'],
                    'secondary': ['startup founders', 'technology teams']
                },
                'social_media': {
                    'platforms': ['twitter', 'linkedin'],
                    'hashtags': [f"#{brand['display_name'].replace(' ', '')}", '#TechInnovation', '#Development'],
                    'posting_frequency': {
                        'twitter': '2-3 times daily',
                        'linkedin': '1 time daily'
                    }
                }
            }
            
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            
            print(f"✅ Created {brand['display_name']} brand configuration")
        else:
            print(f"📁 {brand['display_name']} configuration exists")

def create_dashboard_config():
    """Create dashboard configuration"""
    print("\n📊 Setting Up Dashboard Configuration")
    print("-" * 35)
    
    dashboard_config = {
        'dashboard': {
            'title': 'Marketing Automation Dashboard',
            'port': 5000,
            'host': '0.0.0.0'
        },
        'features': {
            'content_generation': True,
            'social_media_management': True,
            'outreach_automation': True,
            'analytics_reporting': True,
            'campaign_management': True
        },
        'ai': {
            'ollama_url': 'http://localhost:11434',
            'default_model': 'llama3.2:1b',
            'content_generation_enabled': True
        },
        'brands': {
            'buildly': {'enabled': True, 'priority': 1},
            'foundry': {'enabled': True, 'priority': 2},
            'open_build': {'enabled': True, 'priority': 3},
            'radical_therapy': {'enabled': True, 'priority': 4}
        }
    }
    
    config_path = project_root / 'config/dashboard_config.yaml'
    with open(config_path, 'w') as f:
        yaml.dump(dashboard_config, f, default_flow_style=False, sort_keys=False)
    
    print("✅ Dashboard configuration created")

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎯 Next Steps")
    print("-" * 15)
    print("1. 🧪 Test AI integration:")
    print("   python3 test_ollama.py")
    print()
    print("2. 🚀 Start generating content:")
    print("   python3 -c \"from automation.ai.ollama_integration import AIContentGenerator; import asyncio; generator = AIContentGenerator(); print('Ready!')\"")
    print()
    print("3. 📊 Launch dashboard (when implemented):")
    print("   python3 dashboard/app.py")
    print()
    print("4. 📝 Create content:")
    print("   • Blog posts for all brands")
    print("   • Social media campaigns")
    print("   • Outreach email templates")
    print("   • Analytics reports")
    print()
    print("5. 🔧 Customize brand templates in templates/brands/")
    print()
    print("💡 The system is now ready for unified marketing automation!")
    print("   All brand-specific configurations maintain unique voice")
    print("   while sharing AI-powered content generation infrastructure.")

async def main():
    """Main setup function"""
    print_banner()
    
    # Step 1: Check requirements
    if not check_requirements():
        print("\n❌ Setup failed. Please resolve requirements first.")
        return
    
    # Step 2: Create directory structure
    create_directory_structure()
    
    # Step 3: Test AI integration
    ai_working = await test_ai_integration()
    if not ai_working:
        print("\n⚠️  AI integration has issues, but setup will continue")
    
    # Step 4: Create brand configurations
    create_brand_configurations()
    
    # Step 5: Create dashboard config
    create_dashboard_config()
    
    # Step 6: Print completion and next steps
    print("\n" + "=" * 50)
    print("✅ Marketing Automation System Setup Complete!")
    print("=" * 50)
    
    print_next_steps()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup interrupted by user")
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        import traceback
        traceback.print_exc()